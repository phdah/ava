#!/usr/bin/env python3
"""Deterministic Ava release qualification engine.

The engine runs the mechanical release gate against pinned source and target
assets. GitHub Actions is the normal executor; the CLI facade in
`qualification.py` may also invoke it directly for diagnostics.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from internal.release import qualification_runner
from internal.release import qualification_state as state

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
QUALIFICATION_EXECUTOR = "direct-shell"
QUALIFICATION_MODE = "deterministic"
STAGES = ("pre-edge", "final")
PRE_EDGE_KINDS = {"fresh-install", "mature-install", "managed-damage"}
FINAL_KINDS = PRE_EDGE_KINDS | {"resume", "abort", "rollback"}
BEHAVIORAL_KINDS = {
    "registered-routing",
    "registered-calendar",
    "registered-clarification",
    "complete-inbox",
    "finalize",
    "semantic-reconciliation",
    "lifecycle",
}


class QualificationExecutionError(RuntimeError):
    pass


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def resolve(value: str | Path) -> Path:
    return Path(value).expanduser().resolve()


def bind_release(
    selection: dict[str, Any],
    directory: Path,
    *,
    label: str,
) -> tuple[qualification_runner.ReleaseIdentity, dict[str, Any]]:
    identity = qualification_runner.validate_asset_dir(directory, label)
    if identity.version != selection.get("version") or identity.tag != selection.get("tag"):
        raise QualificationExecutionError(
            f"{label} identity differs from active pair: {identity.tag}"
        )
    expected_revision = selection.get("source_revision")
    if expected_revision is not None and identity.revision != expected_revision:
        raise QualificationExecutionError(
            f"{label} source revision differs from active pair: {identity.revision}"
        )
    manifest_sha = state.sha256_file(directory / "ava-release.json")
    asset_sha = state.release_asset_digests(directory)
    if selection.get("kind") == "published":
        if manifest_sha != selection.get("release_manifest_sha256"):
            raise QualificationExecutionError(
                f"{label} published manifest digest differs from pair catalog"
            )
        if asset_sha != selection.get("asset_sha256"):
            raise QualificationExecutionError(
                f"{label} published asset digests differ from pair catalog"
            )
    compact = {
        "kind": selection["kind"],
        "version": identity.version,
        "tag": identity.tag,
        "source_revision": identity.revision,
        "release_manifest_sha256": manifest_sha,
        "asset_sha256": asset_sha,
        "attested": selection["kind"] == "published",
    }
    return identity, compact


def validate_fixture(repository_root: Path, qualification_root: Path) -> None:
    result = state.run_command(
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
    if result.returncode != 0:
        raise QualificationExecutionError(
            "finalized qualification vault verification failed: "
            + result.stderr.strip()
        )


def deterministic_scenarios(
    matrix: dict[str, Any], stage: str
) -> list[dict[str, Any]]:
    allowed = PRE_EDGE_KINDS if stage == "pre-edge" else FINAL_KINDS
    selected = [scenario for scenario in matrix["scenarios"] if scenario.get("kind") in allowed]
    if not selected:
        raise QualificationExecutionError(f"no deterministic scenarios selected for {stage}")
    if any(scenario.get("kind") in BEHAVIORAL_KINDS for scenario in selected):
        raise QualificationExecutionError("release qualification selected a behavioral scenario")
    return selected


def validate_final_edge(
    source: qualification_runner.ReleaseIdentity,
    target: qualification_runner.ReleaseIdentity,
) -> None:
    if source.version == target.version or source.revision == target.revision:
        raise QualificationExecutionError(
            "source and target assets must identify distinct pinned releases"
        )
    edges = target.manifest.get("upgrade_paths", {}).get("edges")
    if not isinstance(edges, list):
        raise QualificationExecutionError(
            "final target release does not declare an upgrade edge inventory"
        )
    matching = [
        edge
        for edge in edges
        if isinstance(edge, dict)
        and edge.get("from") == source.version
        and edge.get("to") == target.version
    ]
    if len(matching) != 1:
        raise QualificationExecutionError(
            f"final target must declare exactly one {source.version} -> {target.version} edge; "
            f"found {len(matching)}"
        )


def prepare_workspace(
    execution_root: Path,
    qualification_root: Path,
    *,
    scenario_id: str,
    source: str,
) -> Path:
    destination = execution_root / "scenarios" / scenario_id
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(qualification_root / source, destination)
    return destination


def verify_deterministic_upgrade_state(
    engine: qualification_runner.Runner,
    *,
    scenario_id: str,
    project: Path,
) -> None:
    manifest = qualification_runner.read_manifest(project)
    journal = qualification_runner.read_journal(project)
    if manifest.get("ava_version") != engine.target.version:
        raise QualificationExecutionError(
            f"{scenario_id}: deterministic upgrade did not install target release"
        )
    semantic = manifest.get("semantic_compatibility", {})
    status = semantic.get("status")
    if status == "complete":
        qualification_runner.assert_target_complete(
            project, engine.target.version, scenario_id
        )
        qualification_runner.assert_no_transactions(project, scenario_id)
        engine.conformance(scenario_id, project)
        return
    if (
        status != "pending"
        or semantic.get("target_version") != engine.target.version
        or journal.get("status") != "active"
        or journal.get("stage") != "semantic"
        or "reconcile-semantic" not in journal.get("allowed_operations", [])
    ):
        raise QualificationExecutionError(
            f"{scenario_id}: deterministic upgrade did not reach an authentic pending semantic state"
        )


def run_deterministic_upgrade(
    engine: qualification_runner.Runner,
    *,
    execution_root: Path,
    qualification_root: Path,
    full_matrix: dict[str, Any],
) -> dict[str, Any]:
    scenario_id = "deterministic-upgrade"
    source_scenario = next(
        (
            scenario
            for scenario in full_matrix["scenarios"]
            if scenario.get("id") == "interrupted-finalize"
        ),
        None,
    )
    if not isinstance(source_scenario, dict):
        raise QualificationExecutionError(
            "qualification matrix has no lifecycle project for deterministic upgrade"
        )
    workspace = prepare_workspace(
        execution_root,
        qualification_root,
        scenario_id=scenario_id,
        source=source_scenario["source"],
    )
    project = workspace / "project"
    try:
        engine.upgrade_to_target(scenario_id, project)
        verify_deterministic_upgrade_state(
            engine, scenario_id=scenario_id, project=project
        )
    except (qualification_runner.QualificationError, QualificationExecutionError) as exc:
        return {"id": scenario_id, "outcome": "fail", "detail": str(exc)}
    return {"id": scenario_id, "outcome": "pass"}


def run_selected_scenarios(
    *,
    repository_root: Path,
    qualification_root: Path,
    execution_root: Path,
    test_project: Path,
    source_identity: qualification_runner.ReleaseIdentity,
    target_identity: qualification_runner.ReleaseIdentity,
    full_matrix: dict[str, Any],
    stage: str,
) -> tuple[int, dict[str, Any]]:
    selected = deterministic_scenarios(full_matrix, stage)
    stage_matrix = dict(full_matrix)
    stage_matrix["scenarios"] = selected
    qualification_runner.initialize_execution_root(execution_root, qualification_root)
    engine = qualification_runner.Runner(
        repository_root=repository_root,
        qualification_root=qualification_root,
        execution_root=execution_root,
        source=source_identity,
        target=target_identity,
        test_project=test_project,
        opencode="disabled",
        model="disabled",
        transcript_dir=None,
        matrix=stage_matrix,
    )
    result = engine.run()
    summary_path = execution_root / "summary.json"
    summary = state.load_json(summary_path)
    outcomes = list(summary.get("outcomes", []))

    if stage == "final" and result == 0:
        upgrade = run_deterministic_upgrade(
            engine,
            execution_root=execution_root,
            qualification_root=qualification_root,
            full_matrix=full_matrix,
        )
        outcomes.append(upgrade)
        result = 0 if upgrade["outcome"] == "pass" else 1

    summary.update(
        {
            "qualification_stage": stage,
            "qualification_mode": QUALIFICATION_MODE,
            "qualification_executor": QUALIFICATION_EXECUTOR,
            "outcomes": outcomes,
            "exit_status": result,
        }
    )
    summary_path.write_text(canonical_json(summary), encoding="utf-8")
    return result, summary


def write_final_evidence(
    *,
    repository_root: Path,
    execution_root: Path,
    pair: dict[str, Any],
    source: dict[str, Any],
    target: dict[str, Any],
    summary: dict[str, Any],
) -> str:
    run_id = state.utc_run_id(pair["id"])
    state_root = repository_root / "internal/release/qualification"
    runs_root = state_root / "runs"
    revision = state.repository_revision(repository_root)
    identity = {
        "schema_version": 1,
        "qualification_stage": "final",
        "qualification_mode": QUALIFICATION_MODE,
        "qualification_executor": QUALIFICATION_EXECUTOR,
        "repository_revision": revision,
        "source": source,
        "target": target,
        "matrix_sha256": state.matrix_digest(repository_root),
        "driver_sha256": state.sha256_file(
            repository_root / "internal/release/qualification_engine.py"
        ),
    }
    identity_sha = state.sha256_text(canonical_json(identity))
    run_record = {
        "schema_version": 1,
        "run_id": run_id,
        "pair_id": pair["id"],
        "execution_identity_sha256": identity_sha,
        "execution_identity": identity,
        "source": source,
        "target": target,
        "qualification_executor": QUALIFICATION_EXECUTOR,
        "qualification_mode": QUALIFICATION_MODE,
        "runner_summary_file": f"{run_id}.summary.json",
        "automated_state": "awaiting-user-signoff",
        "mechanical_error": None,
        "user_signoff": None,
    }
    schema = state.load_json(
        state_root / "schemas/qualification-run-record.schema.json"
    )
    state.validate_schema(
        run_record, schema, label="deterministic release qualification run"
    )
    runs_root.mkdir(parents=True, exist_ok=True)
    (runs_root / f"{run_id}.json").write_text(
        canonical_json(run_record), encoding="utf-8"
    )
    (runs_root / f"{run_id}.summary.json").write_text(
        canonical_json(summary), encoding="utf-8"
    )

    current_path = state_root / "current-state.json"
    current = state.load_json(current_path)
    pair_state = current.get("pairs", {}).get(pair["id"])
    if not isinstance(pair_state, dict):
        raise QualificationExecutionError(
            f"current qualification state has no active pair {pair['id']}"
        )
    pair_state["latest_run_id"] = run_id
    pair_state["status"] = "awaiting-user-signoff"
    pair_state["user_signoff"] = None
    current_path.write_text(canonical_json(current), encoding="utf-8")
    return run_id


def execute(args: argparse.Namespace) -> int:
    repository_root = resolve(args.repository_root)
    qualification_root = resolve(args.qualification_root)
    execution_root = resolve(args.execution_root)
    source_assets = resolve(args.source_assets)
    target_assets = resolve(args.target_assets)
    test_project = resolve(args.test_project)

    if sys.version_info < (3, 11):
        raise QualificationExecutionError("qualification requires Python 3.11 or newer")
    state.require_clean_repository(repository_root)
    config, catalog, _ = state.load_configuration(repository_root)
    pair = state.active_pair(config, catalog)
    full_matrix = qualification_runner.load_matrix(
        repository_root
        / "internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json"
    )

    for path, label in (
        (qualification_root, "qualification root"),
        (source_assets, "source assets"),
        (target_assets, "target assets"),
        (test_project, "test project"),
        (execution_root, "execution root"),
    ):
        qualification_runner.require_external(path, repository_root, label)
    if not qualification_root.is_dir() or not test_project.is_dir():
        raise QualificationExecutionError("qualification root and test project must exist")

    qualification_runner.validate_materialized_variants(
        qualification_root, full_matrix
    )
    validate_fixture(repository_root, qualification_root)
    source_identity, source = bind_release(
        pair["source"], source_assets, label="source assets"
    )
    target_identity, target = bind_release(
        pair["target"], target_assets, label="target assets"
    )
    if source_identity.version == target_identity.version:
        raise QualificationExecutionError("qualification source and target versions must differ")
    if args.stage == "final":
        validate_final_edge(source_identity, target_identity)

    revision = state.repository_revision(repository_root)
    if target.get("kind") != "local" or target.get("source_revision") != revision:
        raise QualificationExecutionError(
            "qualification target must be exact local assets assembled from the current repository revision"
        )
    qualification_runner.validate_execution_root(
        execution_root,
        repository_root=repository_root,
        qualification_root=qualification_root,
        test_project=test_project,
        source_assets=source_assets,
        target_assets=target_assets,
    )

    result, summary = run_selected_scenarios(
        repository_root=repository_root,
        qualification_root=qualification_root,
        execution_root=execution_root,
        test_project=test_project,
        source_identity=source_identity,
        target_identity=target_identity,
        full_matrix=full_matrix,
        stage=args.stage,
    )
    if result != 0:
        print(f"deterministic {args.stage} qualification failed")
        return 1

    if args.stage == "pre-edge":
        print("deterministic pre-edge qualification passed; no repository evidence was written")
        return 0

    run_id = write_final_evidence(
        repository_root=repository_root,
        execution_root=execution_root,
        pair=pair,
        source=source,
        target=target,
        summary=summary,
    )
    print(f"deterministic final qualification passed: {run_id}")
    print("automated state: awaiting-user-signoff")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate-config")
    for stage in STAGES:
        item = subparsers.add_parser(stage)
        item.set_defaults(stage=stage)
        item.add_argument("--qualification-root", type=Path, required=True)
        item.add_argument("--execution-root", type=Path, required=True)
        item.add_argument("--source-assets", type=Path, required=True)
        item.add_argument("--target-assets", type=Path, required=True)
        item.add_argument("--test-project", type=Path, required=True)
    return parser.parse_args(argv)
