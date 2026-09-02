#!/usr/bin/env python3
"""Validate the two-phase release qualification chain before acceptance or merge."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

from internal.release import qualification_acceptance

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = Path("internal/release/qualification")
RUNS_ROOT = STATE_ROOT / "runs"
PHASE_RUNS_ROOT = STATE_ROOT / "phase-runs"
PHASE_STATE_PATH = STATE_ROOT / "phase-state.json"
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


class QualificationPhaseGateError(ValueError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationPhaseGateError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise QualificationPhaseGateError(f"{path} must contain a JSON object")
    return value


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise QualificationPhaseGateError(
            f"git {' '.join(args)} failed: {result.stderr.strip()}"
        )
    return result


def allowed_intervening_path(path: str, *, target_version: str, prerequisite_run_id: str) -> bool:
    early_prefix = f"{PHASE_RUNS_ROOT.as_posix()}/{prerequisite_run_id}."
    return (
        path == PHASE_STATE_PATH.as_posix()
        or path.startswith(early_prefix)
        or path == f"internal/release/catalogs/{target_version}.json"
        or path.startswith(f"internal/release/guidance/{target_version}/")
        or path.startswith("internal/release/migrations/")
    )


def invalidating_phase_changes(
    paths: Iterable[str],
    *,
    target_version: str,
    prerequisite_run_id: str,
) -> list[str]:
    return sorted(
        path
        for path in paths
        if path
        and not allowed_intervening_path(
            path,
            target_version=target_version,
            prerequisite_run_id=prerequisite_run_id,
        )
    )


def require_edge_absent_at_early_revision(
    root: Path,
    *,
    early_revision: str,
    target_version: str,
) -> None:
    catalog = f"internal/release/catalogs/{target_version}.json"
    if git(root, "cat-file", "-e", f"{early_revision}:{catalog}", check=False).returncode == 0:
        raise QualificationPhaseGateError(
            "edge-independent qualification was recorded after the target adjacent catalog already existed"
        )
    guidance_prefix = f"internal/release/guidance/{target_version}/"
    guidance = git(
        root,
        "ls-tree",
        "-r",
        "--name-only",
        early_revision,
        "--",
        guidance_prefix,
    ).stdout.strip()
    if guidance:
        raise QualificationPhaseGateError(
            "edge-independent qualification was recorded after target semantic guidance already existed"
        )


def validate_phase_prerequisite(
    root: Path,
    final_run: dict[str, Any],
    *,
    previous_version: str,
    target_version: str,
) -> dict[str, Any]:
    root = root.resolve()
    identity = final_run.get("execution_identity")
    if not isinstance(identity, dict):
        raise QualificationPhaseGateError("final qualification run has no execution identity")
    if identity.get("qualification_phase") != "edge-dependent":
        raise QualificationPhaseGateError(
            "release acceptance requires an edge-dependent final qualification run"
        )

    prerequisite_run_id = identity.get("prerequisite_edge_independent_run_id")
    prerequisite_revision = identity.get("prerequisite_repository_revision")
    if not isinstance(prerequisite_run_id, str) or not prerequisite_run_id:
        raise QualificationPhaseGateError(
            "edge-dependent qualification is not linked to an edge-independent prerequisite run"
        )
    if not isinstance(prerequisite_revision, str) or REVISION_RE.fullmatch(prerequisite_revision) is None:
        raise QualificationPhaseGateError(
            "edge-dependent qualification has an invalid prerequisite repository revision"
        )

    early_path = root / PHASE_RUNS_ROOT / f"{prerequisite_run_id}.json"
    early = read_json(early_path)
    if early.get("qualification_phase") != "edge-independent":
        raise QualificationPhaseGateError(
            "qualification prerequisite is not an edge-independent phase run"
        )
    if early.get("automated_state") != "passed" or early.get("mechanical_error") is not None:
        raise QualificationPhaseGateError(
            "edge-independent qualification prerequisite did not pass cleanly"
        )
    if early.get("pair_id") != final_run.get("pair_id"):
        raise QualificationPhaseGateError(
            "qualification phases were executed for different release pairs"
        )

    early_identity = early.get("execution_identity")
    if not isinstance(early_identity, dict):
        raise QualificationPhaseGateError(
            "edge-independent qualification has no execution identity"
        )
    early_revision = early_identity.get("repository_revision")
    final_revision = identity.get("repository_revision")
    if (
        not isinstance(early_revision, str)
        or REVISION_RE.fullmatch(early_revision) is None
        or early_revision != prerequisite_revision
    ):
        raise QualificationPhaseGateError(
            "edge-dependent prerequisite revision does not match early qualification evidence"
        )
    if not isinstance(final_revision, str) or REVISION_RE.fullmatch(final_revision) is None:
        raise QualificationPhaseGateError("final qualification repository revision is invalid")

    early_source = early.get("source")
    final_source = final_run.get("source")
    early_target = early.get("target")
    final_target = final_run.get("target")
    if not isinstance(early_source, dict) or not isinstance(final_source, dict):
        raise QualificationPhaseGateError("qualification source identities are incomplete")
    if early_source != final_source or early_source.get("version") != previous_version:
        raise QualificationPhaseGateError(
            "qualification phases do not use the same intended source release"
        )
    if not isinstance(early_target, dict) or not isinstance(final_target, dict):
        raise QualificationPhaseGateError("qualification target identities are incomplete")
    if (
        early_target.get("version") != target_version
        or final_target.get("version") != target_version
        or early_target.get("kind") != "local"
        or final_target.get("kind") != "local"
    ):
        raise QualificationPhaseGateError(
            "qualification phases do not use the same intended local target release"
        )
    if early_target.get("source_revision") != early_revision:
        raise QualificationPhaseGateError(
            "edge-independent target assets are not bound to the early qualified revision"
        )
    if final_target.get("source_revision") != final_revision:
        raise QualificationPhaseGateError(
            "edge-dependent target assets are not bound to the final qualified revision"
        )

    if git(
        root,
        "merge-base",
        "--is-ancestor",
        early_revision,
        final_revision,
        check=False,
    ).returncode != 0:
        raise QualificationPhaseGateError(
            "edge-independent qualification revision is not an ancestor of final qualification"
        )

    require_edge_absent_at_early_revision(
        root,
        early_revision=early_revision,
        target_version=target_version,
    )
    changed = {
        line.strip()
        for line in git(
            root,
            "diff",
            "--name-only",
            early_revision,
            final_revision,
        ).stdout.splitlines()
        if line.strip()
    }
    invalid = invalidating_phase_changes(
        changed,
        target_version=target_version,
        prerequisite_run_id=prerequisite_run_id,
    )
    if invalid:
        raise QualificationPhaseGateError(
            "edge-independent qualification was invalidated by post-phase changes; rerun the early phase after changes to: "
            + ", ".join(invalid)
        )
    return early


def resolve_run_for_acceptance(root: Path, run_id: str | None) -> tuple[str, dict[str, Any]]:
    state = read_json(root / STATE_ROOT / "current-state.json")
    if run_id is None:
        active_pair = state.get("active_pair")
        pairs = state.get("pairs")
        pair_state = pairs.get(active_pair) if isinstance(pairs, dict) else None
        if not isinstance(pair_state, dict):
            raise QualificationPhaseGateError("active qualification pair state is missing")
        run_id = pair_state.get("latest_run_id")
    if not isinstance(run_id, str) or not run_id:
        raise QualificationPhaseGateError("final qualification run id is missing")
    return run_id, read_json(root / RUNS_ROOT / f"{run_id}.json")


def validate_acceptance_candidate(root: Path, run_id: str | None = None) -> str:
    root = root.resolve()
    run_id, run = resolve_run_for_acceptance(root, run_id)
    source = run.get("source")
    target = run.get("target")
    if not isinstance(source, dict) or not isinstance(target, dict):
        raise QualificationPhaseGateError("final qualification release identities are incomplete")
    previous_version = source.get("version")
    target_version = target.get("version")
    if not isinstance(previous_version, str) or not isinstance(target_version, str):
        raise QualificationPhaseGateError("final qualification release versions are missing")
    validate_phase_prerequisite(
        root,
        run,
        previous_version=previous_version,
        target_version=target_version,
    )
    return f"two-phase qualification chain valid for {previous_version} -> {target_version}: {run_id}"


def validate_release_pr_phase_gate(root: Path, previous_version: str) -> str:
    root = root.resolve()
    target_version = (root / "version.txt").read_text(encoding="utf-8").strip()
    state = read_json(root / STATE_ROOT / "current-state.json")
    ledger = state.get("release_acceptance")
    entry = ledger.get(target_version) if isinstance(ledger, dict) else None
    if not isinstance(entry, dict) or entry.get("basis") != "qualified-run":
        raise QualificationPhaseGateError(
            f"release {target_version} has no accepted current qualification run"
        )
    run_id = entry.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise QualificationPhaseGateError(
            f"release {target_version} accepted state has no qualification run"
        )
    run = read_json(root / RUNS_ROOT / f"{run_id}.json")
    validate_phase_prerequisite(
        root,
        run,
        previous_version=previous_version,
        target_version=target_version,
    )
    return f"release PR has valid edge-independent and edge-dependent qualification: {run_id}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    accept = subparsers.add_parser("accept")
    accept.add_argument("--identity", required=True)
    accept.add_argument("--run-id")

    validate = subparsers.add_parser("validate-release-pr")
    validate.add_argument("--previous-version", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "accept":
            validate_acceptance_candidate(args.root, args.run_id)
            message = qualification_acceptance.accept_run(
                args.root,
                identity=args.identity,
                run_id=args.run_id,
            )
        else:
            message = validate_release_pr_phase_gate(
                args.root,
                args.previous_version,
            )
    except (
        QualificationPhaseGateError,
        qualification_acceptance.QualificationAcceptanceError,
        OSError,
        ValueError,
        KeyError,
    ) as exc:
        print(f"two-phase qualification invalid: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
