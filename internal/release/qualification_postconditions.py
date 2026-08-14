#!/usr/bin/env python3
"""Apply deterministic postconditions to a completed synthetic qualification run."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = REPOSITORY_ROOT / "internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json"


class PostconditionError(RuntimeError):
    pass


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PostconditionError(f"cannot read JSON {path}: {exc}") from exc


def semantic_project_change_errors(execution_root: Path, matrix: dict[str, Any]) -> dict[str, str]:
    errors: dict[str, str] = {}
    for scenario in matrix.get("scenarios", []):
        if not isinstance(scenario, dict):
            continue
        expected = scenario.get("expected_project_changes")
        if not expected:
            continue
        scenario_id = scenario.get("id")
        if not isinstance(scenario_id, str):
            raise PostconditionError("qualification matrix semantic postcondition has no scenario id")
        journal_path = execution_root / "scenarios" / scenario_id / "project/.ava/state/upgrade.json"
        journal = load_json(journal_path)
        records = journal.get("project_changes")
        if not isinstance(records, list):
            errors[scenario_id] = "upgrade journal has no project_changes array"
            continue
        paths = [record.get("path") for record in records if isinstance(record, dict)]
        counts = Counter(path for path in paths if isinstance(path, str))
        missing = [path for path in expected if counts[path] == 0]
        duplicates = [path for path in expected if counts[path] > 1]
        unresolved = [
            path
            for path in expected
            for record in records
            if isinstance(record, dict)
            and record.get("path") == path
            and record.get("resolution") == "unresolved"
        ]
        if missing or duplicates or unresolved:
            details: list[str] = []
            if missing:
                details.append(f"missing inspected paths {missing}")
            if duplicates:
                details.append(f"duplicate inspected paths {duplicates}")
            if unresolved:
                details.append(f"unresolved inspected paths {sorted(set(unresolved))}")
            errors[scenario_id] = "; ".join(details)
    return errors


def apply_postconditions(execution_root: Path, matrix: dict[str, Any]) -> int:
    summary_path = execution_root / "summary.json"
    summary = load_json(summary_path)
    outcomes = summary.get("outcomes")
    if not isinstance(outcomes, list):
        raise PostconditionError("qualification summary has no outcomes array")

    by_id = {
        item.get("id"): item
        for item in outcomes
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    errors = semantic_project_change_errors(execution_root, matrix)
    for scenario_id, detail in errors.items():
        outcome = by_id.get(scenario_id)
        if outcome is None:
            raise PostconditionError(f"qualification summary is missing scenario {scenario_id}")
        if outcome.get("outcome") == "pass":
            outcome["outcome"] = "fail"
            outcome["detail"] = f"semantic project-change accounting failed: {detail}"

    summary["exit_status"] = 0 if outcomes and all(
        isinstance(item, dict) and item.get("outcome") == "pass" for item in outcomes
    ) else 1
    summary_path.write_text(canonical_json(summary), encoding="utf-8")
    return int(summary["exit_status"])


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--execution-root", type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    args, _ = parser.parse_known_args(argv)
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.preflight_only:
        return 0
    if args.execution_root is None:
        raise SystemExit("qualification postconditions require --execution-root")
    repository_root = args.repository_root.expanduser().resolve()
    matrix = load_json(repository_root / MATRIX_PATH.relative_to(REPOSITORY_ROOT))
    try:
        return apply_postconditions(args.execution_root.expanduser().resolve(), matrix)
    except PostconditionError as exc:
        print(f"qualification postcondition error: {exc}", flush=True)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
