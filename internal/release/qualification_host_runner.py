#!/usr/bin/env python3
"""Run one release qualification phase through a host-neutral agent boundary."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from internal.release import qualification_host
from internal.release import qualification_phase_runner as phase_contract
from internal.release import qualification_runner

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PHASES = phase_contract.PHASES


class QualificationHostRunnerError(RuntimeError):
    pass


class HostNeutralRunner(qualification_runner.Runner):
    """Shared deterministic scenario engine with injected agent-host execution."""

    def __init__(self, *, agent_host: qualification_host.AgentHostAdapter, **kwargs: Any) -> None:
        super().__init__(opencode=agent_host.adapter_id, **kwargs)
        self.agent_host = agent_host

    def opencode_prompt(
        self,
        scenario_id: str,
        project: Path,
        prompt: str,
        *,
        expected_role: str | None = None,
    ) -> qualification_runner.CommandResult:
        result = self.run_command(
            scenario_id,
            self.agent_host.interaction_command(
                project=project,
                model=self.model,
                prompt=prompt,
            ),
            label="agent host prompt",
        )
        combined = result.stdout + "\n" + result.stderr
        if expected_role and f"Active role: {expected_role}" not in combined:
            raise qualification_runner.QualificationError(
                f"{scenario_id}: agent host did not announce expected role {expected_role}"
            )
        if self.transcript_dir:
            self.transcript_dir.mkdir(parents=True, exist_ok=True)
            (self.transcript_dir / f"{scenario_id}.jsonl").write_text(
                result.stdout,
                encoding="utf-8",
            )
        return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=PHASES, required=True)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--qualification-root", type=Path, required=True)
    parser.add_argument("--execution-root", type=Path, required=True)
    parser.add_argument("--source-assets", type=Path, required=True)
    parser.add_argument("--target-assets", type=Path, required=True)
    parser.add_argument("--test-project", type=Path, required=True)
    parser.add_argument("--host-kind", default="opencode")
    parser.add_argument("--host-executable", required=True)
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
    qualification_host.AgentHostAdapter,
]:
    repository_root = qualification_runner.resolve_path(args.repository_root)
    qualification_root = qualification_runner.resolve_path(args.qualification_root)
    execution_root = qualification_runner.resolve_path(args.execution_root)
    source_assets = qualification_runner.resolve_path(args.source_assets)
    target_assets = qualification_runner.resolve_path(args.target_assets)
    test_project = qualification_runner.resolve_path(args.test_project)

    if sys.version_info < (3, 11):
        raise QualificationHostRunnerError("qualification runner requires Python 3.11 or newer")
    if not repository_root.is_dir():
        raise QualificationHostRunnerError(f"repository root does not exist: {repository_root}")
    if not qualification_runner.repository_is_clean(repository_root):
        raise QualificationHostRunnerError("Ava repository must be clean before qualification")

    qualification_runner.require_external(
        qualification_root,
        repository_root,
        "qualification root",
    )
    qualification_runner.require_external(source_assets, repository_root, "source assets")
    qualification_runner.require_external(target_assets, repository_root, "target assets")
    qualification_runner.require_external(test_project, repository_root, "test project")
    if not qualification_root.is_dir() or not test_project.is_dir():
        raise QualificationHostRunnerError(
            "qualification root and test project must be existing directories"
        )

    full_matrix, phase_matrix = phase_contract.load_phase_matrix(repository_root, args.phase)
    qualification_runner.validate_materialized_variants(qualification_root, full_matrix)
    source = qualification_runner.validate_asset_dir(source_assets, "source assets")
    target = qualification_runner.validate_asset_dir(target_assets, "target assets")
    phase_contract.validate_release_pair(source, target)
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
    host = qualification_host.resolve_host_adapter(
        args.host_kind,
        args.host_executable,
    )
    if not args.model.strip() or "/" not in args.model:
        raise QualificationHostRunnerError(
            "--model must be an explicit provider/model identifier"
        )

    fixture = qualification_host.legacy_automation.run_command(
        [
            sys.executable,
            str(
                repository_root
                / "internal/release/fixtures/synthetic-qualification-vault/fixture.py"
            ),
            "verify",
            str(qualification_root),
        ],
        cwd=repository_root,
        check=False,
    )
    if fixture.returncode != 0:
        raise QualificationHostRunnerError(
            "finalized qualification vault verification failed: "
            + fixture.stderr.strip()
        )
    return phase_matrix, source, target, host


def planned_summary(
    args: argparse.Namespace,
    matrix: dict[str, Any],
    source: qualification_runner.ReleaseIdentity,
    target: qualification_runner.ReleaseIdentity,
    host: qualification_host.AgentHostAdapter,
) -> None:
    descriptor = host.descriptor()
    print(f"qualification phase:    {args.phase}")
    print(f"qualification root:     {qualification_runner.resolve_path(args.qualification_root)}")
    print(f"execution root:         {qualification_runner.resolve_path(args.execution_root)}")
    print(f"source assets:          {source.tag} {source.revision}")
    print(f"target assets:          {target.tag} {target.revision}")
    print(
        "test project:           "
        f"{qualification_runner.resolve_path(args.test_project)} (read-only source boundary)"
    )
    print(f"agent host:             {descriptor.adapter} {descriptor.version}")
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
        matrix, source, target, host = preflight(args)
        planned_summary(args, matrix, source, target, host)
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
                transcript_dir,
                repository_root,
                "transcript directory",
            )
            qualification_runner.require_disjoint(
                transcript_dir,
                qualification_root,
                "transcript directory",
                "qualification root",
            )

        qualification_runner.initialize_execution_root(execution_root, qualification_root)
        runner = HostNeutralRunner(
            repository_root=repository_root,
            qualification_root=qualification_root,
            execution_root=execution_root,
            source=source,
            target=target,
            test_project=test_project,
            agent_host=host,
            model=args.model,
            transcript_dir=transcript_dir,
            matrix=matrix,
        )
        result = runner.run()
        annotate_summary(execution_root, args.phase)
        return result
    except (
        QualificationHostRunnerError,
        qualification_host.QualificationHostError,
        phase_contract.QualificationPhaseError,
        qualification_runner.QualificationError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(f"host-neutral qualification runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
