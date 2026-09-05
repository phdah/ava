#!/usr/bin/env python3
"""Drive deterministic Ava release qualification from GitHub Actions.

The workflow YAML deliberately stays thin. This module owns release-PR stage
selection, exact acceptance-request validation, reusable-evidence detection,
qualification execution, and packaging repository state transitions for the
active maintainer session to apply.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from internal.release import qualification_state as state

REPOSITORY_ROOT = state.REPOSITORY_ROOT
QUALIFICATION_ROOT = REPOSITORY_ROOT / "internal/release/qualification"
ACCEPTANCE_REQUEST = QUALIFICATION_ROOT / "acceptance-request.json"
ALLOWED_ARTIFACT_KINDS = {"evidence", "acceptance"}


class QualificationCiError(RuntimeError):
    pass


def run(command: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPOSITORY_ROOT,
        check=check,
        text=True,
        capture_output=False,
    )


def load_acceptance_request(path: Path = ACCEPTANCE_REQUEST) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationCiError(f"invalid acceptance request: {exc}") from exc
    if not isinstance(value, dict):
        raise QualificationCiError("acceptance request must be an object")
    if set(value) != {"identity", "run_id", "schema_version"}:
        raise QualificationCiError("acceptance request has unexpected fields")
    if value.get("schema_version") != 1:
        raise QualificationCiError("acceptance request schema_version must be 1")
    for field in ("identity", "run_id"):
        if not isinstance(value.get(field), str) or not value[field]:
            raise QualificationCiError(f"acceptance request {field} must be non-empty")
    return value


def reusable_final_evidence() -> bool:
    config, catalog, _ = state.load_configuration(REPOSITORY_ROOT)
    pair = state.active_pair(config, catalog)
    current = state.load_json(QUALIFICATION_ROOT / "current-state.json")
    pair_state = current.get("pairs", {}).get(pair["id"])
    if not isinstance(pair_state, dict):
        return False
    if pair_state.get("status") not in {"awaiting-user-signoff", "accepted"}:
        return False
    run_id = pair_state.get("latest_run_id")
    if not isinstance(run_id, str) or not run_id:
        return False
    run_path = QUALIFICATION_ROOT / "runs" / f"{run_id}.json"
    if not run_path.is_file():
        return False
    run_record = state.load_json(run_path)
    identity = run_record.get("execution_identity")
    if (
        run_record.get("automated_state") != "awaiting-user-signoff"
        or not isinstance(identity, dict)
        or identity.get("qualification_stage") != "final"
        or identity.get("qualification_mode") != "deterministic"
    ):
        return False
    revision = identity.get("repository_revision")
    if not isinstance(revision, str) or not revision:
        return False
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", revision, "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=False,
    ).returncode != 0:
        return False
    changed = subprocess.run(
        ["git", "diff", "--name-only", revision, "HEAD"],
        cwd=REPOSITORY_ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    if any(
        path and not path.startswith("internal/release/qualification/")
        for path in changed
    ):
        return False
    print(f"reusing final deterministic qualification evidence: {run_id}")
    return True


def changed_qualification_paths() -> tuple[list[Path], list[Path]]:
    result = subprocess.run(
        [
            "git",
            "status",
            "--porcelain",
            "--untracked-files=all",
            "--",
            "internal/release/qualification",
        ],
        cwd=REPOSITORY_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    files: list[Path] = []
    deleted: list[Path] = []
    for line in result.stdout.splitlines():
        if len(line) < 4:
            continue
        path = Path(line[3:])
        if path.is_file():
            files.append(path)
        elif not path.exists():
            deleted.append(path)
    return sorted(files), sorted(deleted)


def package_changes(kind: str, artifact_root: Path) -> None:
    if kind not in ALLOWED_ARTIFACT_KINDS:
        raise QualificationCiError(f"unsupported artifact kind: {kind}")
    if artifact_root.exists():
        shutil.rmtree(artifact_root)
    artifact_root.mkdir(parents=True)

    files, deleted = changed_qualification_paths()
    if not files and not deleted:
        raise QualificationCiError("qualification produced no repository changes to package")

    for path in files:
        destination = artifact_root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPOSITORY_ROOT / path, destination)

    manifest = {
        "schema_version": 1,
        "kind": kind,
        "files": [path.as_posix() for path in files],
        "delete": [path.as_posix() for path in deleted],
    }
    (artifact_root / "artifact-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def initial_release_version(root: Path = REPOSITORY_ROOT) -> str:
    policy_path = root / "internal/release/fixtures/release-upgrade-policy.json"
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationCiError(f"invalid release upgrade policy: {exc}") from exc
    initial = policy.get("initial_release_version") if isinstance(policy, dict) else None
    if not isinstance(initial, str) or not initial:
        raise QualificationCiError(
            "release upgrade policy initial_release_version must be non-empty"
        )
    return initial


def qualification_stage(root: Path = REPOSITORY_ROOT) -> str:
    target_version = (root / "version.txt").read_text(encoding="utf-8").strip()
    if not target_version:
        raise QualificationCiError("version.txt is empty")
    target_catalog = root / "internal/release/catalogs" / f"{target_version}.json"
    if target_version == initial_release_version(root):
        if target_catalog.exists():
            raise QualificationCiError(
                "the root release must not define an upgrade-edge catalog"
            )
        return "final"
    return "final" if target_catalog.is_file() else "pre-edge"


def write_output(name: str, value: str) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        print(f"{name}={value}")
        return
    with Path(output_path).open("a", encoding="utf-8") as handle:
        handle.write(f"{name}={value}\n")


def artifact_root() -> Path:
    runner_temp = os.environ.get("RUNNER_TEMP")
    if not runner_temp:
        raise QualificationCiError("RUNNER_TEMP is required")
    return Path(runner_temp) / "release-qualification-artifact"


def apply_acceptance_request() -> None:
    request = load_acceptance_request()
    run(
        [
            str(REPOSITORY_ROOT / "internal/release/accept-release-qualification.sh"),
            "--identity",
            request["identity"],
            "--run-id",
            request["run_id"],
        ]
    )
    ACCEPTANCE_REQUEST.unlink()
    package_changes("acceptance", artifact_root())
    write_output("artifact_ready", "true")
    write_output("artifact_name", f"release-qualification-acceptance-{os.environ['GITHUB_SHA']}")
    write_output("artifact_path", str(artifact_root()))


def execute_qualification() -> None:
    stage = qualification_stage()
    run(
        [
            str(REPOSITORY_ROOT / "internal/release/run-release-qualification.sh"),
            stage,
        ]
    )
    if stage == "pre-edge":
        return
    package_changes("evidence", artifact_root())
    write_output("artifact_ready", "true")
    write_output("artifact_name", f"release-qualification-evidence-{os.environ['GITHUB_SHA']}")
    write_output("artifact_path", str(artifact_root()))


def main() -> int:
    write_output("artifact_ready", "false")
    try:
        if ACCEPTANCE_REQUEST.is_file():
            apply_acceptance_request()
            return 0
        if reusable_final_evidence():
            return 0
        execute_qualification()
        return 0
    except (
        QualificationCiError,
        state.QualificationStateError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"release qualification CI error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
