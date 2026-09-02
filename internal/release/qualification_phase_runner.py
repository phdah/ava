#!/usr/bin/env python3
"""Run one explicit phase of the synthetic Ava qualification matrix."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from internal.release import qualification_runner

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PHASES = ("edge-independent", "edge-dependent")


class QualificationPhaseError(RuntimeError):
    pass


def validate_release_pair(
    source: qualification_runner.ReleaseIdentity,
    target: qualification_runner.ReleaseIdentity,
) -> None:
    if source.version == target.version or source.revision == target.revision:
        raise QualificationPhaseError(
            "source and target assets must identify distinct pinned releases"
        )


def load_phase_matrix(repository_root: Path, phase: str) -> tuple[dict[str, Any], dict[str, Any]]:
    matrix = qualification_runner.load_matrix(
        repository_root
        / "internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json"
    )
    classifications = {
        scenario.get("qualification_phase")
        for scenario in matrix["scenarios"]
    }
    invalid = sorted(
        value for value in classifications if value not in PHASES
    )
    if invalid or None in classifications:
        raise QualificationPhaseError(
            "every maintained qualification scenario must declare qualification_phase "
            f"as one of {PHASES}; observed invalid values: {invalid}"
        )
    selected = [
        scenario
        for scenario in matrix["scenarios"]
        if scenario["qualification_phase"] == phase
    ]
    if not selected:
        raise QualificationPhaseError(f"qualification phase has no scenarios: {phase}")
    phase_matrix = dict(matrix)
    phase_matrix["scenarios"] = selected
    return matrix, phase_matrix


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=PHASES, required=True)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--qualification-root", type=Path, required=True)
    parser.add_argument("--execution-root", type=Path, required=True)
    parser.add_argument("--source-assets", type=Path, required=True)
    parser.add_argument("--target-assets", type=Path, required=True)
    parser.add_argument("--test-project", type=Path, required=True)
    parser.add_argument("--opencode", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--transcript-dir", type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    return parser.parse_args(argv)


def preflight(
    args: argparse.Namespace,
) -> tuple[
    dict[str, Any],
    qualification_runner.ReleaseIdentity,
    qualification_runner.ReleaseIdentity,
    str,
]:
    repository_root = qualification_runner.resolve_path(args.repository_root)
    qualification_root = qualification_runner.resolve_path(args.qualification_root)
    execution_root = qualification_runner.resolve_path(args.execution_root)
    source_assets = qualification_runner.resolve_path(args.source_assets)
    target_assets = qualification_runner.resolve_path(args.target_assets)
    test_project = qualification_runner.resolve_path(args.test_project)

    if sys.version_info < (3, 11):
        raise QualificationPhaseError("qualification runner requires Python 3.11 or newer")
    if not repository_root.is_dir():
        raise QualificationPhaseError(f"repository root does not exist: {repository_root}")
    if not qualification_runner.repository_is_clean(repository_root):
        raise QualificationPhaseError("Ava repository must be clean before qualification")

    qualification_runner.require_external(
        qualification_root, repository_root, "qualification root"
    )
    qualification_runner.require_external(source_assets, repository_root, "source assets")
    qualification_runner.require_external(target_assets, repository_root, "target assets")
    qualification_runner.require_external(test_project, repository_root, "test project")
    if not qualification_root.is_dir() or not test_project.is_dir():
        raise QualificationPhaseError(
            "qualification root and test project must be existing directories"
        )

    full_matrix, phase_matrix = load_phase_matrix(repository_root, args.phase)
    qualification_runner.validate_materialized_variants(qualification_root, full_matrix)
    source = qualification_runner.validate_asset_dir(source_assets, "source assets")
    target = qualification_runner.validate_asset_dir(target_assets, "target assets")
    validate_release_pair(source, target)
    if args.phase == "edge-dependent":
        qualification_runner.validate_upgrade_pair(source, target)

    qualification_runner.validate_execution_root(
        execution_root,
        repository_root=repository_root,
        qualification_root=qualification_root,
        test_project=test_project,
        source_assets=source_assets,
        target_assets=target_assets,
    )
    opencode = qualification_runner.resolve_executable(args.opencode)
    version = subprocess.run(
        [opencode, "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if version.returncode != 0:
        raise QualificationPhaseError(
            f"OpenCode version check failed: {version.stderr.strip()}"
        )
    if not args.model.strip() or "/" not in args.model:
        raise QualificationPhaseError(
            "--model must be an explicit provider/model identifier"
        )

    fixture = subprocess.run(
        [
            sys.executable,
            str(
                repository_root
                / "internal/release/fixtures/synthetic-qualification-vault/fixture.py"
            ),
            "verify",
            str(qualification_root),
        ],
        cwd=str(repository_root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if fixture.returncode != 0:
        raise QualificationPhaseError(
            "finalized qualification vault verification failed: "
            + fixture.stderr.strip()
        )
    return phase_matrix, source, target, opencode


def planned_summary(
    args: argparse.Namespace,
    matrix: dict[str, Any],
    source: qualification_runner.ReleaseIdentity,
    target: qualification_runner.ReleaseIdentity,
    opencode: str,
) -> None:
    print(f"qualification phase:    {args.phase}")
    print(f"qualification root:     {qualification_runner.resolve_path(args.qualification_root)}")
    print(f"execution root:         {qualification_runner.resolve_path(args.execution_root)}")
    print(f"source assets:          {source.tag} {source.revision}")
    print(f"target assets:          {target.tag} {target.revision}")
    print(
        "test project:           "
        f"{qualification_runner.resolve_path(args.test_project)} (read-only source boundary)"
    )
    print(f"OpenCode:               {opencode}")
    print(f"model:                  {args.model}")
    print("scenarios:")
    for scenario in matrix["scenarios"]:
        print(f"  {scenario['order']:02d}. {scenario['id']} [{scenario['family']}]")


def annotate_summary(execution_root: Path, phase: str) -> None:
    path = execution_root / "summary.json"
    if not path.is_file():
        return
    summary = json.loads(path.read_text(encoding="utf-8"))
    summary["qualification_phase"] = phase
    path.write_text(qualification_runner.canonical_json(summary), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        matrix, source, target, opencode = preflight(args)
        planned_summary(args, matrix, source, target, opencode)
        if args.preflight_only:
            return 0

        repository_root = qualification_runner.resolve_path(args.repository_root)
        qualification_root = qualification_runner.resolve_path(args.qualification_root)
        execution_root = qualification_runner.resolve_path(args.execution_root)
        test_project = qualification_runner.resolve_path(args.test_project)
        transcript_dir = (
            qualification_runner.resolve_path(args.transcript_dir)
            if args.transcript_dir
            else None
        )
        if transcript_dir:
            qualification_runner.require_external(
                transcript_dir, repository_root, "transcript directory"
            )
            qualification_runner.require_disjoint(
                transcript_dir,
                qualification_root,
                "transcript directory",
                "qualification root",
            )

        qualification_runner.initialize_execution_root(
            execution_root, qualification_root
        )
        runner = qualification_runner.Runner(
            repository_root=repository_root,
            qualification_root=qualification_root,
            execution_root=execution_root,
            source=source,
            target=target,
            test_project=test_project,
            opencode=opencode,
            model=args.model,
            transcript_dir=transcript_dir,
            matrix=matrix,
        )
        result = runner.run()
        annotate_summary(execution_root, args.phase)
        return result
    except (
        QualificationPhaseError,
        qualification_runner.QualificationError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(f"phased qualification runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
