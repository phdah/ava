#!/usr/bin/env python3
"""Accept a completed qualification run and validate release-PR qualification state."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from internal.release.adjacent_edges import version_key

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = Path("internal/release/qualification")
RUNS_ROOT = STATE_ROOT / "runs"
CATALOG_ROOT = Path("internal/release/catalogs")
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


class QualificationAcceptanceError(ValueError):
    pass


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationAcceptanceError(f"cannot read {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise QualificationAcceptanceError(f"{path} must contain a JSON object")
    return value


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise QualificationAcceptanceError(
            f"git {' '.join(args)} failed: {result.stderr.strip()}"
        )
    return result


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def validate_acceptance_ledger(root: Path, *, through_version: str | None = None) -> None:
    state = read_json(root / STATE_ROOT / "current-state.json")
    ledger = state.get("release_acceptance")
    if not isinstance(ledger, dict):
        raise QualificationAcceptanceError("current-state.json is missing release_acceptance")

    catalog_dir = root / CATALOG_ROOT
    for path in sorted(catalog_dir.glob("*.json")):
        record = read_json(path)
        target = record.get("target_version")
        edge = record.get("edge")
        if not isinstance(target, str) or not isinstance(edge, dict):
            raise QualificationAcceptanceError(f"invalid release catalog record: {path}")
        if through_version is not None and version_key(target) > version_key(through_version):
            continue
        previous = edge.get("from")
        entry = ledger.get(target)
        if not isinstance(entry, dict) or entry.get("status") != "accepted":
            raise QualificationAcceptanceError(
                f"release {target} has no accepted qualification state"
            )
        if entry.get("previous_version") != previous:
            raise QualificationAcceptanceError(
                f"release {target} qualification state does not match catalog edge {previous} -> {target}"
            )
        basis = entry.get("basis")
        if basis not in {"historical-backfill", "qualified-run"}:
            raise QualificationAcceptanceError(
                f"release {target} has invalid qualification acceptance basis"
            )


def _qualified_run(root: Path, target_version: str) -> tuple[dict[str, Any], dict[str, Any]]:
    state = read_json(root / STATE_ROOT / "current-state.json")
    ledger = state.get("release_acceptance", {})
    entry = ledger.get(target_version)
    if not isinstance(entry, dict) or entry.get("status") != "accepted":
        raise QualificationAcceptanceError(
            f"release {target_version} is not accepted by release qualification"
        )
    if entry.get("basis") != "qualified-run":
        raise QualificationAcceptanceError(
            f"release {target_version} must be accepted from a current qualified run"
        )
    run_id = entry.get("run_id")
    if not isinstance(run_id, str) or not run_id:
        raise QualificationAcceptanceError(
            f"release {target_version} accepted state has no qualification run"
        )
    return entry, read_json(root / RUNS_ROOT / f"{run_id}.json")


def validate_release_pr_acceptance(
    root: Path,
    previous_version: str,
    *,
    base_revision: str | None = None,
) -> str:
    root = root.resolve()
    target_version = (root / "version.txt").read_text(encoding="utf-8").strip()

    validate_acceptance_ledger(root, through_version=previous_version)
    entry, run = _qualified_run(root, target_version)

    if entry.get("previous_version") != previous_version:
        raise QualificationAcceptanceError(
            f"release qualification accepts {entry.get('previous_version')} -> {target_version}, "
            f"not {previous_version} -> {target_version}"
        )
    if run.get("automated_state") != "awaiting-user-signoff" or run.get("mechanical_error") is not None:
        raise QualificationAcceptanceError("accepted run was not a clean automated qualification")
    signoff = run.get("user_signoff")
    if not isinstance(signoff, dict):
        raise QualificationAcceptanceError("accepted run is missing explicit user signoff")
    if signoff.get("identity") != entry.get("accepted_by") or signoff.get("time") != entry.get("accepted_at"):
        raise QualificationAcceptanceError("release acceptance and run signoff disagree")

    source = run.get("source")
    target = run.get("target")
    if not isinstance(source, dict) or source.get("version") != previous_version:
        raise QualificationAcceptanceError("accepted run source does not match previous release")
    if not isinstance(target, dict) or target.get("version") != target_version:
        raise QualificationAcceptanceError("accepted run target does not match release PR target")
    if target.get("kind") != "local":
        raise QualificationAcceptanceError("pre-merge release qualification target must be local")

    identity = run.get("execution_identity")
    qualified_revision = entry.get("qualified_revision")
    if not isinstance(identity, dict) or identity.get("repository_revision") != qualified_revision:
        raise QualificationAcceptanceError("accepted run repository revision does not match release state")
    if not isinstance(qualified_revision, str) or REVISION_RE.fullmatch(qualified_revision) is None:
        raise QualificationAcceptanceError("accepted qualification revision is invalid")
    if target.get("source_revision") != qualified_revision:
        raise QualificationAcceptanceError(
            "qualified local release assets were not assembled from the qualified repository revision"
        )

    if base_revision is not None:
        base_ok = git(root, "merge-base", "--is-ancestor", base_revision, qualified_revision, check=False)
        if base_ok.returncode != 0:
            raise QualificationAcceptanceError(
                "accepted qualification revision is not part of this release PR"
            )

    head_ok = git(root, "merge-base", "--is-ancestor", qualified_revision, "HEAD", check=False)
    if head_ok.returncode != 0:
        raise QualificationAcceptanceError(
            "accepted qualification revision is not an ancestor of the current release PR head"
        )
    changed = {
        line.strip()
        for line in git(root, "diff", "--name-only", qualified_revision, "HEAD").stdout.splitlines()
        if line.strip()
    }
    invalid = sorted(
        path for path in changed if not path.startswith("internal/release/qualification/")
    )
    if invalid:
        raise QualificationAcceptanceError(
            "release content changed after qualification; rerun qualification after changes to: "
            + ", ".join(invalid)
        )

    return (
        f"release qualification accepted for {previous_version} -> {target_version}; "
        f"run: {entry['run_id']}"
    )


def accept_run(
    root: Path,
    *,
    identity: str,
    run_id: str | None = None,
    accepted_at: str | None = None,
) -> str:
    root = root.resolve()
    if not identity.strip():
        raise QualificationAcceptanceError("acceptance identity must be non-empty")
    state_path = root / STATE_ROOT / "current-state.json"
    state = read_json(state_path)
    pairs = state.get("pairs")
    if not isinstance(pairs, dict):
        raise QualificationAcceptanceError("current qualification pair state is invalid")

    if run_id is None:
        active_pair = state.get("active_pair")
        pair_state = pairs.get(active_pair)
        if not isinstance(pair_state, dict):
            raise QualificationAcceptanceError("active qualification pair state is missing")
        run_id = pair_state.get("latest_run_id")
    matches = [
        (pair_id, pair_state)
        for pair_id, pair_state in pairs.items()
        if isinstance(pair_state, dict) and pair_state.get("latest_run_id") == run_id
    ]
    if len(matches) != 1 or not isinstance(run_id, str) or not run_id:
        raise QualificationAcceptanceError("qualification run does not resolve to exactly one pair")
    pair_id, pair_state = matches[0]
    if pair_state.get("status") != "awaiting-user-signoff":
        raise QualificationAcceptanceError(
            f"qualification run is not awaiting user signoff: {pair_state.get('status')}"
        )

    run_path = root / RUNS_ROOT / f"{run_id}.json"
    run = read_json(run_path)
    if run.get("pair_id") != pair_id:
        raise QualificationAcceptanceError("run record pair does not match current state")
    if run.get("automated_state") != "awaiting-user-signoff" or run.get("mechanical_error") is not None:
        raise QualificationAcceptanceError("only a clean awaiting-user-signoff run may be accepted")
    if run.get("user_signoff") is not None:
        raise QualificationAcceptanceError("qualification run already has user signoff")

    source = run.get("source")
    target = run.get("target")
    execution_identity = run.get("execution_identity")
    if not isinstance(source, dict) or not isinstance(target, dict) or not isinstance(execution_identity, dict):
        raise QualificationAcceptanceError("qualification run identity is incomplete")
    source_version = source.get("version")
    target_version = target.get("version")
    revision = execution_identity.get("repository_revision")
    if not isinstance(source_version, str) or not isinstance(target_version, str):
        raise QualificationAcceptanceError("qualification run release versions are missing")
    if not isinstance(revision, str) or REVISION_RE.fullmatch(revision) is None:
        raise QualificationAcceptanceError("qualification run repository revision is invalid")
    if target.get("source_revision") != revision:
        raise QualificationAcceptanceError(
            "qualification target assets are not bound to the qualified repository revision"
        )

    timestamp = accepted_at or now_utc()
    signoff = {"identity": identity.strip(), "time": timestamp}
    run["user_signoff"] = signoff
    pair_state["status"] = "accepted"
    pair_state["user_signoff"] = signoff
    ledger = state.setdefault("release_acceptance", {})
    if not isinstance(ledger, dict):
        raise QualificationAcceptanceError("release_acceptance must be an object")
    ledger[target_version] = {
        "previous_version": source_version,
        "status": "accepted",
        "basis": "qualified-run",
        "run_id": run_id,
        "qualified_revision": revision,
        "accepted_at": timestamp,
        "accepted_by": identity.strip(),
    }

    run_path.write_text(canonical_json(run), encoding="utf-8")
    state_path.write_text(canonical_json(state), encoding="utf-8")
    return f"accepted release qualification {source_version} -> {target_version}: {run_id}"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    accept = subparsers.add_parser("accept")
    accept.add_argument("--identity", required=True)
    accept.add_argument("--run-id")

    validate = subparsers.add_parser("validate-release-pr")
    validate.add_argument("--previous-version", required=True)
    validate.add_argument("--base-revision")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "accept":
            message = accept_run(args.root, identity=args.identity, run_id=args.run_id)
        else:
            message = validate_release_pr_acceptance(
                args.root,
                args.previous_version,
                base_revision=args.base_revision,
            )
    except QualificationAcceptanceError as exc:
        print(f"release qualification invalid: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
