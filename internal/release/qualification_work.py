#!/usr/bin/env python3
"""Drive Ava release qualification inside ChatGPT Work Cloud.

The script owns deterministic setup, validation, evidence and release-state updates.
It never starts an LLM process. When semantic agent work is required it emits a
request for a fresh ChatGPT Work subagent, then resumes after that subagent has
written the requested structured response into the shared Work Cloud filesystem.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

from internal.release import qualification_automation as automation
from internal.release import qualification_phase_gate as phase_gate
from internal.release import qualification_phase_runner as phase_runner
from internal.release import qualification_runner
from internal.release.qualification_inbox import (
    InboxStructuralError,
    validate_inbox_structural_fidelity,
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
STATE_NAME = "chatgpt-work-state.json"
SUMMARY_NAME = "summary.json"
WORK_PROTOCOL_VERSION = 1
WORK_HOST = "chatgpt-work-cloud"
AGENT_KINDS = {
    "registered-routing",
    "registered-calendar",
    "registered-clarification",
    "complete-inbox",
    "finalize",
    "semantic-reconciliation",
    "lifecycle",
}
PASSING_OUTCOMES = qualification_runner.PASSING_OUTCOMES


class WorkQualificationError(RuntimeError):
    pass


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def state_path(execution_root: Path) -> Path:
    return execution_root / STATE_NAME


def load_state(execution_root: Path) -> dict[str, Any]:
    path = state_path(execution_root)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise WorkQualificationError(f"cannot read Work qualification state {path}: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise WorkQualificationError(f"invalid Work qualification state: {path}")
    if value.get("work_protocol_version") != WORK_PROTOCOL_VERSION:
        raise WorkQualificationError("Work qualification protocol version mismatch")
    return value


def save_state(state: dict[str, Any]) -> None:
    path = Path(state["execution_root"]) / STATE_NAME
    path.write_text(canonical_json(state), encoding="utf-8")


def resolve(value: str | Path) -> Path:
    return Path(value).expanduser().resolve()


def scenario_mode(scenario: dict[str, Any]) -> str:
    return "subagent" if scenario.get("kind") in AGENT_KINDS else "deterministic"


def file_manifest(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not root.exists():
        return result
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        result[path.relative_to(root).as_posix()] = automation.sha256_file(path)
    return result


def bind_release(selection: dict[str, Any], directory: Path, *, label: str) -> tuple[qualification_runner.ReleaseIdentity, dict[str, Any]]:
    identity = qualification_runner.validate_asset_dir(directory, label)
    if identity.version != selection.get("version") or identity.tag != selection.get("tag"):
        raise WorkQualificationError(
            f"{label} identity differs from active pair: {identity.tag}"
        )
    expected_revision = selection.get("source_revision")
    if expected_revision is not None and identity.revision != expected_revision:
        raise WorkQualificationError(
            f"{label} source revision differs from active pair: {identity.revision}"
        )
    manifest_sha = automation.sha256_file(directory / "ava-release.json")
    asset_sha = automation.release_asset_digests(directory)
    if selection.get("kind") == "published":
        if manifest_sha != selection.get("release_manifest_sha256"):
            raise WorkQualificationError(f"{label} published manifest digest differs from pair catalog")
        if asset_sha != selection.get("asset_sha256"):
            raise WorkQualificationError(f"{label} published asset digests differ from pair catalog")
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


def load_phase_state(repository_root: Path) -> dict[str, Any]:
    path = repository_root / "internal/release/qualification/phase-state.json"
    value = automation.load_json(path)
    if value.get("schema_version") != 1 or not isinstance(value.get("pairs"), dict):
        raise WorkQualificationError(f"invalid edge-independent phase state: {path}")
    return value


def prerequisite(
    repository_root: Path,
    *,
    pair_id: str,
) -> tuple[str, dict[str, Any]]:
    phase_state = load_phase_state(repository_root)
    pair_state = phase_state["pairs"].get(pair_id)
    if not isinstance(pair_state, dict) or pair_state.get("status") != "passed":
        raise WorkQualificationError(
            "edge-dependent qualification requires one committed clean edge-independent Work run"
        )
    run_id = pair_state.get("latest_run_id")
    if not isinstance(run_id, str) or not run_id:
        raise WorkQualificationError("edge-independent phase state has no prerequisite run id")
    run = automation.load_json(
        repository_root / "internal/release/qualification/phase-runs" / f"{run_id}.json"
    )
    return run_id, run


def validate_fixture(repository_root: Path, qualification_root: Path) -> None:
    result = automation.run_command(
        [
            sys.executable,
            str(repository_root / "internal/release/fixtures/synthetic-qualification-vault/fixture.py"),
            "verify",
            str(qualification_root),
        ],
        cwd=repository_root,
        check=False,
    )
    if result.returncode != 0:
        raise WorkQualificationError(
            "finalized qualification vault verification failed: " + result.stderr.strip()
        )


def init_run(args: argparse.Namespace) -> int:
    repository_root = resolve(args.repository_root)
    qualification_root = resolve(args.qualification_root)
    execution_root = resolve(args.execution_root)
    source_assets = resolve(args.source_assets)
    target_assets = resolve(args.target_assets)
    test_project = resolve(args.test_project)

    if sys.version_info < (3, 11):
        raise WorkQualificationError("qualification requires Python 3.11 or newer")
    automation.require_clean_repository(repository_root)
    config, catalog, _ = automation.load_configuration(repository_root)
    pair = automation.active_pair(config, catalog)
    full_matrix, phase_matrix = phase_runner.load_phase_matrix(repository_root, args.phase)

    for path, label in (
        (qualification_root, "qualification root"),
        (source_assets, "source assets"),
        (target_assets, "target assets"),
        (test_project, "test project"),
        (execution_root, "execution root"),
    ):
        qualification_runner.require_external(path, repository_root, label)
    if not qualification_root.is_dir() or not test_project.is_dir():
        raise WorkQualificationError("qualification root and test project must exist")

    qualification_runner.validate_materialized_variants(qualification_root, full_matrix)
    validate_fixture(repository_root, qualification_root)
    source_identity, source = bind_release(pair["source"], source_assets, label="source assets")
    target_identity, target = bind_release(pair["target"], target_assets, label="target assets")
    phase_runner.validate_release_pair(source_identity, target_identity)
    if args.phase == "edge-dependent":
        qualification_runner.validate_upgrade_pair(source_identity, target_identity)

    repo_revision = automation.repository_revision(repository_root)
    if target["kind"] != "local" or target["source_revision"] != repo_revision:
        raise WorkQualificationError(
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
    qualification_runner.initialize_execution_root(execution_root, qualification_root)

    prerequisite_run_id: str | None = None
    prerequisite_revision: str | None = None
    if args.phase == "edge-dependent":
        prerequisite_run_id, early = prerequisite(repository_root, pair_id=pair["id"])
        early_identity = early.get("execution_identity")
        if not isinstance(early_identity, dict):
            raise WorkQualificationError("edge-independent prerequisite has no execution identity")
        prerequisite_revision = early_identity.get("repository_revision")
        preview = {
            "pair_id": pair["id"],
            "source": source,
            "target": target,
            "execution_identity": {
                "qualification_phase": "edge-dependent",
                "repository_revision": repo_revision,
                "prerequisite_edge_independent_run_id": prerequisite_run_id,
                "prerequisite_repository_revision": prerequisite_revision,
            },
        }
        phase_gate.validate_phase_prerequisite(
            repository_root,
            preview,
            previous_version=source_identity.version,
            target_version=target_identity.version,
        )

    identity_payload = {
        "schema_version": 1,
        "work_protocol_version": WORK_PROTOCOL_VERSION,
        "qualification_host": WORK_HOST,
        "qualification_phase": args.phase,
        "repository_revision": repo_revision,
        "source": source,
        "target": target,
        "matrix_sha256": automation.matrix_digest(repository_root),
        "work_driver_sha256": automation.sha256_file(
            repository_root / "internal/release/qualification_work.py"
        ),
        "qualification_root_sha256": automation.tree_digest(qualification_root),
        "qualification_model": config["qualification_model"],
        "audit_model": config["audit_model"],
        "prerequisite_edge_independent_run_id": prerequisite_run_id,
        "prerequisite_repository_revision": prerequisite_revision,
    }
    identity_sha = automation.sha256_text(canonical_json(identity_payload))
    run_id = automation.utc_run_id(pair["id"])
    state = {
        "schema_version": 1,
        "work_protocol_version": WORK_PROTOCOL_VERSION,
        "qualification_host": WORK_HOST,
        "run_id": run_id,
        "pair_id": pair["id"],
        "phase": args.phase,
        "repository_root": str(repository_root),
        "qualification_root": str(qualification_root),
        "execution_root": str(execution_root),
        "source_assets": str(source_assets),
        "target_assets": str(target_assets),
        "test_project": str(test_project),
        "qualification_model": config["qualification_model"],
        "audit_model": config["audit_model"],
        "source": source,
        "target": target,
        "execution_identity_sha256": identity_sha,
        "execution_identity": identity_payload,
        "baseline_corpus_sha256": qualification_runner.inventory_digest(qualification_root / "corpus"),
        "baseline_test_project_sha256": qualification_runner.inventory_digest(test_project),
        "scenario_order": [scenario["id"] for scenario in phase_matrix["scenarios"]],
        "scenarios": {
            scenario["id"]: {
                "status": "pending",
                "outcome": None,
                "detail": None,
                "stage": None,
                "checkpoints": {},
            }
            for scenario in phase_matrix["scenarios"]
        },
        "current_request": None,
        "interaction_counter": 0,
        "integrity_outcomes": [],
        "audit": {"status": "not-requested", "request_path": None, "response_path": None},
        "finalized": False,
    }
    save_state(state)
    print(f"Work qualification initialized: {run_id}")
    print(f"state: {state_path(execution_root)}")
    return 0


def phase_matrix_for_state(state: dict[str, Any]) -> dict[str, Any]:
    _, matrix = phase_runner.load_phase_matrix(resolve(state["repository_root"]), state["phase"])
    return matrix


def scenario_by_id(state: dict[str, Any], scenario_id: str) -> dict[str, Any]:
    matrix = phase_matrix_for_state(state)
    matches = [scenario for scenario in matrix["scenarios"] if scenario["id"] == scenario_id]
    if len(matches) != 1:
        raise WorkQualificationError(f"cannot resolve qualification scenario: {scenario_id}")
    return matches[0]


def runner_for_state(state: dict[str, Any]) -> qualification_runner.Runner:
    source = qualification_runner.validate_asset_dir(resolve(state["source_assets"]), "source assets")
    target = qualification_runner.validate_asset_dir(resolve(state["target_assets"]), "target assets")
    return qualification_runner.Runner(
        repository_root=resolve(state["repository_root"]),
        qualification_root=resolve(state["qualification_root"]),
        execution_root=resolve(state["execution_root"]),
        source=source,
        target=target,
        test_project=resolve(state["test_project"]),
        opencode="unsupported-in-chatgpt-work",
        model=state["qualification_model"],
        transcript_dir=None,
        matrix=phase_matrix_for_state(state),
    )


def workspace_for(state: dict[str, Any], scenario: dict[str, Any]) -> Path:
    execution_root = resolve(state["execution_root"])
    destination = execution_root / "scenarios" / scenario["id"]
    source = resolve(state["qualification_root"]) / scenario["source"]
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)
    return destination


def response_schema_text() -> str:
    return (
        "Write exactly one JSON object with fields: schema_version=1, interaction_id, scenario, stage, "
        "prompt_sha256, model, workspace_root, final_response, required_reading, external_tools_used. "
        "required_reading is an ordered array of {order,path,sha256} records for project files read before "
        "the first project mutation. external_tools_used must be an empty array."
    )


def create_request(
    state: dict[str, Any],
    scenario: dict[str, Any],
    *,
    stage: str,
    project: Path,
    prompt: str,
    expected_role: str | None,
) -> int:
    execution_root = resolve(state["execution_root"])
    state["interaction_counter"] += 1
    interaction_id = f"work-{state['interaction_counter']:03d}-{scenario['id']}-{stage}"
    interaction_root = execution_root / "interactions"
    interaction_root.mkdir(parents=True, exist_ok=True)
    request_path = interaction_root / f"{interaction_id}.request.json"
    response_path = interaction_root / f"{interaction_id}.response.json"
    request = {
        "schema_version": 1,
        "work_protocol_version": WORK_PROTOCOL_VERSION,
        "interaction_id": interaction_id,
        "scenario": scenario["id"],
        "stage": stage,
        "model": state["qualification_model"],
        "workspace_root": str(project.resolve()),
        "prompt": prompt,
        "prompt_sha256": automation.sha256_text(prompt),
        "expected_role": expected_role,
        "baseline_files": file_manifest(project),
        "response_path": str(response_path.resolve()),
        "execution_contract": [
            "Execute this request as one fresh ChatGPT Work Cloud subagent, not in ordinary Chat and not on a local machine.",
            "Operate only inside workspace_root except for reading this request and writing response_path.",
            "Do not use web search, cloud browser, plugins, apps, MCPs, external repositories, or any user-local files.",
            "Read and follow workspace_root/AGENTS.md and every required role/workflow file before announcing the role or mutating project content.",
            "Treat prompt as the user request for the isolated qualification project.",
            response_schema_text(),
        ],
    }
    request_path.write_text(canonical_json(request), encoding="utf-8")
    state["current_request"] = {
        "interaction_id": interaction_id,
        "scenario": scenario["id"],
        "stage": stage,
        "request_path": str(request_path.resolve()),
        "response_path": str(response_path.resolve()),
    }
    scenario_state = state["scenarios"][scenario["id"]]
    scenario_state["status"] = "waiting-subagent"
    scenario_state["stage"] = stage
    save_state(state)
    print(f"SUBAGENT_REQUIRED {request_path}")
    return 3


def prepare_agent_scenario(
    state: dict[str, Any],
    scenario: dict[str, Any],
    workspace: Path,
) -> int:
    engine = runner_for_state(state)
    scenario_id = scenario["id"]
    project = workspace / "project"
    scenario_state = state["scenarios"][scenario_id]
    checkpoints = scenario_state["checkpoints"]
    kind = scenario["kind"]

    if kind == "registered-routing":
        engine.fresh_install(scenario_id, project, engine.target)
        checkpoints["private_before"] = qualification_runner.inventory_digest(project / "knowledge/private")
        checkpoints["work_before"] = qualification_runner.inventory_digest(project / "knowledge/work")
        return create_request(
            state,
            scenario,
            stage="route",
            project=project,
            prompt=scenario["prompt"],
            expected_role=scenario["expected_role"],
        )
    if kind == "registered-calendar":
        engine.fresh_install(scenario_id, project, engine.target)
        checkpoints["private_before"] = qualification_runner.inventory_digest(project / "knowledge/private")
        return create_request(
            state,
            scenario,
            stage="calendar",
            project=project,
            prompt=scenario["prompt"],
            expected_role=scenario["expected_role"],
        )
    if kind == "registered-clarification":
        engine.fresh_install(scenario_id, project, engine.target)
        checkpoints["project_before"] = qualification_runner.project_owned_digest(project)
        return create_request(
            state,
            scenario,
            stage="clarification",
            project=project,
            prompt=scenario["prompt"],
            expected_role=None,
        )
    if kind == "complete-inbox":
        engine.fresh_install(scenario_id, project, engine.target)
        checkpoints["selected_sources"] = [
            {
                "path": path.relative_to(project).as_posix(),
                "sha256": qualification_runner.sha256_file(path),
            }
            for path in sorted((project / "inbox").iterdir())
            if path.is_file() and path.name not in {"index.md", "log.md"}
        ]
        return create_request(
            state,
            scenario,
            stage="ingest",
            project=project,
            prompt=scenario["prompt"],
            expected_role="Inbox Ingester",
        )
    if kind == "finalize":
        engine.upgrade_to_target(scenario_id, project)
        return create_request(
            state,
            scenario,
            stage="semantic-reconciliation",
            project=project,
            prompt=scenario["semantic_prompt"],
            expected_role="Upgrade Role",
        )
    if kind == "semantic-reconciliation":
        engine.upgrade_to_target(scenario_id, project)
        return create_request(
            state,
            scenario,
            stage="semantic-reconciliation",
            project=project,
            prompt=scenario["prompt"],
            expected_role="Upgrade Role",
        )
    if kind == "lifecycle":
        engine.fresh_install(scenario_id, project, engine.target)
        checkpoints["project_before"] = qualification_runner.project_owned_digest(project)
        return create_request(
            state,
            scenario,
            stage="uninstall",
            project=project,
            prompt=scenario["uninstall_prompt"],
            expected_role="Ava Maintenance",
        )
    raise WorkQualificationError(f"unsupported Work subagent scenario kind: {kind}")


def validate_response(request: dict[str, Any], response: dict[str, Any]) -> None:
    required = {
        "schema_version",
        "interaction_id",
        "scenario",
        "stage",
        "prompt_sha256",
        "model",
        "workspace_root",
        "final_response",
        "required_reading",
        "external_tools_used",
    }
    if not isinstance(response, dict) or set(response) != required:
        raise WorkQualificationError("subagent response differs from the Work evidence contract")
    if response["schema_version"] != 1:
        raise WorkQualificationError("subagent response schema_version must be 1")
    for field in ("interaction_id", "scenario", "stage", "prompt_sha256", "model", "workspace_root"):
        if response[field] != request[field]:
            raise WorkQualificationError(f"subagent response identity mismatch: {field}")
    if not isinstance(response["final_response"], str) or not response["final_response"].strip():
        raise WorkQualificationError("subagent response has no final_response")
    if response["external_tools_used"] != []:
        raise WorkQualificationError(
            "qualification subagent used external tools; Work scenarios permit only the isolated cloud workspace"
        )
    reading = response["required_reading"]
    if not isinstance(reading, list) or not reading:
        raise WorkQualificationError("subagent response has no required-reading evidence")
    baseline = request["baseline_files"]
    for index, item in enumerate(reading, 1):
        if not isinstance(item, dict) or set(item) != {"order", "path", "sha256"}:
            raise WorkQualificationError("invalid required-reading evidence record")
        if item["order"] != index:
            raise WorkQualificationError("required-reading evidence order must be contiguous")
        path = item["path"]
        if not isinstance(path, str) or path.startswith("/") or ".." in Path(path).parts:
            raise WorkQualificationError(f"unsafe required-reading path: {path!r}")
        if baseline.get(path) != item["sha256"]:
            raise WorkQualificationError(
                f"required-reading digest is not bound to the pre-interaction workspace: {path}"
            )
    if reading[0]["path"] != "AGENTS.md":
        raise WorkQualificationError("qualification subagent must load AGENTS.md first")


def load_current_response(state: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    current = state.get("current_request")
    if not isinstance(current, dict):
        raise WorkQualificationError("no current Work subagent request")
    request = automation.load_json(Path(current["request_path"]))
    response_path = Path(current["response_path"])
    if not response_path.is_file():
        raise WorkQualificationError(f"subagent response is not ready: {response_path}")
    response = automation.load_json(response_path)
    validate_response(request, response)
    return request, response


def complete_scenario(state: dict[str, Any], scenario: dict[str, Any], outcome: dict[str, Any]) -> None:
    scenario_state = state["scenarios"][scenario["id"]]
    scenario_state["status"] = "complete"
    scenario_state["outcome"] = outcome["outcome"]
    scenario_state["detail"] = outcome.get("detail")
    scenario_state["stage"] = None
    state["current_request"] = None
    save_state(state)


def verify_agent_scenario(
    state: dict[str, Any],
    scenario: dict[str, Any],
    request: dict[str, Any],
    response: dict[str, Any],
) -> int | None:
    engine = runner_for_state(state)
    scenario_id = scenario["id"]
    project = Path(request["workspace_root"])
    scenario_state = state["scenarios"][scenario_id]
    checkpoints = scenario_state["checkpoints"]
    text = response["final_response"]
    expected_role = request.get("expected_role")
    if expected_role and f"Active role: {expected_role}" not in text:
        raise WorkQualificationError(
            f"{scenario_id}: Work subagent did not announce expected role {expected_role}"
        )

    kind = scenario["kind"]
    if kind == "registered-routing":
        private_after = qualification_runner.inventory_digest(project / "knowledge/private")
        work_after = qualification_runner.inventory_digest(project / "knowledge/work")
        boundary = scenario["mutation_boundary"]
        if boundary == "private" and not (
            private_after != checkpoints["private_before"]
            and work_after == checkpoints["work_before"]
        ):
            raise WorkQualificationError(f"{scenario_id}: private/work mutation boundary was not preserved")
        if boundary == "work" and not (
            work_after != checkpoints["work_before"]
            and private_after == checkpoints["private_before"]
        ):
            raise WorkQualificationError(f"{scenario_id}: work/private mutation boundary was not preserved")
    elif kind == "registered-calendar":
        if qualification_runner.inventory_digest(project / "knowledge/private") != checkpoints["private_before"]:
            raise WorkQualificationError(f"{scenario_id}: calendar scenario changed private context")
        work_text = "\n".join(
            path.read_text(encoding="utf-8", errors="replace")
            for path in (project / "knowledge/work").rglob("*")
            if path.is_file()
        )
        if scenario["expected_date"] not in work_text or scenario["expected_weekday"].lower() not in work_text.lower():
            raise WorkQualificationError(
                f"{scenario_id}: persisted work context does not contain {scenario['expected_weekday']} {scenario['expected_date']}"
            )
        if scenario["forbidden_date"] in work_text:
            raise WorkQualificationError(f"{scenario_id}: persisted the known-wrong calendar date")
    elif kind == "registered-clarification":
        if qualification_runner.project_owned_digest(project) != checkpoints["project_before"]:
            raise WorkQualificationError(f"{scenario_id}: ambiguous routing mutated project-owned content")
        lower = text.lower()
        if not any(token in lower for token in ("clarif", "which", "ambiguous", "need you to")):
            raise WorkQualificationError(f"{scenario_id}: ambiguous routing did not request clarification")
    elif kind == "complete-inbox":
        pending = [
            path
            for path in (project / "inbox").iterdir()
            if path.is_file() and path.name not in {"index.md", "log.md"}
        ]
        if pending:
            raise WorkQualificationError(f"{scenario_id}: {len(pending)} direct inbox sources remain pending")
        try:
            validate_inbox_structural_fidelity(project, checkpoints["selected_sources"])
        except InboxStructuralError as exc:
            raise WorkQualificationError(
                f"{scenario_id}: inbox structural fidelity failed: {exc}"
            ) from exc
        engine.conformance(scenario_id, project)
    elif kind == "finalize":
        semantic = qualification_runner.read_manifest(project)["semantic_compatibility"].get("status")
        if request["stage"] == "semantic-reconciliation":
            if semantic == "complete":
                state["current_request"] = None
                save_state(state)
                return create_request(
                    state,
                    scenario,
                    stage="finalize",
                    project=project,
                    prompt=scenario["finalize_prompt"],
                    expected_role="Ava Maintenance",
                )
            lower = text.lower()
            if semantic in {"partial", "blocked"} or any(
                token in lower for token in ("decision", "approval", "clarif")
            ):
                complete_scenario(
                    state,
                    scenario,
                    {"outcome": "user-decision-required", "detail": f"semantic compatibility remains {semantic}"},
                )
                return 1
            raise WorkQualificationError(
                f"{scenario_id}: semantic reconciliation ended in unexpected state {semantic}"
            )
        qualification_runner.assert_target_complete(project, engine.target.version, scenario_id)
        qualification_runner.assert_no_transactions(project, scenario_id)
        engine.conformance(scenario_id, project)
    elif kind == "semantic-reconciliation":
        semantic = qualification_runner.read_manifest(project)["semantic_compatibility"].get("status")
        if semantic != "complete":
            lower = text.lower()
            if semantic in {"partial", "blocked"} or any(
                token in lower for token in ("decision", "approval", "clarif")
            ):
                complete_scenario(
                    state,
                    scenario,
                    {"outcome": "user-decision-required", "detail": f"semantic compatibility remains {semantic}"},
                )
                return 1
            raise WorkQualificationError(
                f"{scenario_id}: semantic reconciliation ended in unexpected state {semantic}"
            )
    elif kind == "lifecycle":
        if (project / ".ava").exists() or (project / "AGENTS.md").exists():
            raise WorkQualificationError(f"{scenario_id}: role-led uninstall left Ava-managed content")
        qualification_runner.assert_project_owned_digest(project, checkpoints["project_before"], scenario_id)
        engine.install(scenario_id, project, engine.target)
        qualification_runner.assert_project_owned_digest(project, checkpoints["project_before"], scenario_id)
        engine.conformance(scenario_id, project)
    else:
        raise WorkQualificationError(f"unsupported Work subagent scenario kind: {kind}")

    outcome = (
        {"outcome": "structural-pass", "semantic_status": "pending-audit"}
        if scenario.get("semantic_audit_required") is True
        else {"outcome": "pass"}
    )
    complete_scenario(state, scenario, outcome)
    return None


def block_after_nonpass(state: dict[str, Any], blocked_by: str) -> None:
    seen = False
    for scenario_id in state["scenario_order"]:
        if scenario_id == blocked_by:
            seen = True
            continue
        if seen and state["scenarios"][scenario_id]["status"] == "pending":
            state["scenarios"][scenario_id].update(
                {
                    "status": "complete",
                    "outcome": "skipped",
                    "detail": f"not run after non-passing scenario {blocked_by}",
                }
            )
    save_state(state)


def write_summary(state: dict[str, Any]) -> dict[str, Any]:
    outcomes = []
    for scenario_id in state["scenario_order"]:
        item = state["scenarios"][scenario_id]
        if item["outcome"] is None:
            continue
        record = {"id": scenario_id, "outcome": item["outcome"]}
        if item.get("detail"):
            record["detail"] = item["detail"]
        outcomes.append(record)
    outcomes.extend(state.get("integrity_outcomes", []))
    summary = {
        "schema_version": 1,
        "qualification_phase": state["phase"],
        "qualification_host": WORK_HOST,
        "run_id": state["run_id"],
        "source": {
            "version": state["source"]["version"],
            "tag": state["source"]["tag"],
            "revision": state["source"]["source_revision"],
        },
        "target": {
            "version": state["target"]["version"],
            "tag": state["target"]["tag"],
            "revision": state["target"]["source_revision"],
        },
        "outcomes": outcomes,
        "exit_status": qualification_runner.summary_exit_status(outcomes),
    }
    (resolve(state["execution_root"]) / SUMMARY_NAME).write_text(
        canonical_json(summary), encoding="utf-8"
    )
    return summary


def finalize_integrity(state: dict[str, Any]) -> None:
    qualification_root = resolve(state["qualification_root"])
    test_project = resolve(state["test_project"])
    failures: list[dict[str, Any]] = []
    if qualification_runner.inventory_digest(qualification_root / "corpus") != state["baseline_corpus_sha256"]:
        failures.append(
            {"id": "finalized-corpus-integrity", "outcome": "fail", "detail": "corpus bytes changed"}
        )
    if qualification_runner.inventory_digest(test_project) != state["baseline_test_project_sha256"]:
        failures.append(
            {"id": "test-project-integrity", "outcome": "fail", "detail": "original test project bytes changed"}
        )
    state["integrity_outcomes"] = failures
    save_state(state)


def advance_run(args: argparse.Namespace) -> int:
    execution_root = resolve(args.execution_root)
    state = load_state(execution_root)
    if state.get("finalized"):
        raise WorkQualificationError("qualification run is already finalized")

    current = state.get("current_request")
    if isinstance(current, dict):
        response_path = Path(current["response_path"])
        if not response_path.is_file():
            print(f"SUBAGENT_REQUIRED {current['request_path']}")
            return 3
        request, response = load_current_response(state)
        scenario = scenario_by_id(state, current["scenario"])
        try:
            state["current_request"] = None
            save_state(state)
            result = verify_agent_scenario(state, scenario, request, response)
            if result == 3:
                return 3
            if result == 1:
                block_after_nonpass(state, scenario["id"])
                write_summary(state)
                return 1
        except (WorkQualificationError, qualification_runner.QualificationError) as exc:
            complete_scenario(state, scenario, {"outcome": "fail", "detail": str(exc)})
            block_after_nonpass(state, scenario["id"])
            write_summary(state)
            return 1

    matrix = phase_matrix_for_state(state)
    by_id = {scenario["id"]: scenario for scenario in matrix["scenarios"]}
    for scenario_id in state["scenario_order"]:
        item = state["scenarios"][scenario_id]
        if item["status"] == "complete":
            if item["outcome"] not in PASSING_OUTCOMES:
                write_summary(state)
                return 1
            continue
        scenario = by_id[scenario_id]
        workspace = workspace_for(state, scenario)
        if scenario_mode(scenario) == "subagent":
            try:
                return prepare_agent_scenario(state, scenario, workspace)
            except (WorkQualificationError, qualification_runner.QualificationError) as exc:
                complete_scenario(state, scenario, {"outcome": "fail", "detail": str(exc)})
                block_after_nonpass(state, scenario_id)
                write_summary(state)
                return 1
        engine = runner_for_state(state)
        try:
            outcome = engine.run_scenario(scenario, workspace)
        except qualification_runner.QualificationError as exc:
            outcome = {"outcome": "fail", "detail": str(exc)}
        complete_scenario(state, scenario, outcome)
        if outcome["outcome"] not in PASSING_OUTCOMES:
            block_after_nonpass(state, scenario_id)
            write_summary(state)
            return 1

    finalize_integrity(state)
    summary = write_summary(state)
    if summary["exit_status"] != 0:
        return 1
    print(f"Work qualification scenarios complete: {state['run_id']}")
    return 0


def audit_request(args: argparse.Namespace) -> int:
    execution_root = resolve(args.execution_root)
    state = load_state(execution_root)
    if state.get("current_request") is not None:
        raise WorkQualificationError("complete the current subagent request before audit")
    summary_path = execution_root / SUMMARY_NAME
    if not summary_path.is_file():
        raise WorkQualificationError("run scenarios to completion before requesting audit")
    summary = automation.load_json(summary_path)
    if qualification_runner.summary_exit_status(summary.get("outcomes", [])) != 0:
        raise WorkQualificationError("independent audit requires an all-passing mechanical summary")

    audit_root = execution_root / "audit"
    audit_root.mkdir(parents=True, exist_ok=True)
    response_path = audit_root / "response.json"
    prompt_path = audit_root / "request.md"
    repository_root = resolve(state["repository_root"])
    maintained = (
        repository_root / "internal/release/qualification/audit-prompt.md"
    ).read_text(encoding="utf-8")
    prompt = (
        maintained
        + "\n\n# Work Cloud run inputs\n\n"
        + f"- pair_id: `{state['pair_id']}`\n"
        + f"- run_id: `{state['run_id']}`\n"
        + f"- qualification_phase: `{state['phase']}`\n"
        + f"- execution_identity_sha256: `{state['execution_identity_sha256']}`\n"
        + f"- runner_summary: `{summary_path}`\n"
        + f"- interactions: `{execution_root / 'interactions'}`\n"
        + f"- scenario_workspaces: `{execution_root / 'scenarios'}`\n"
        + f"- qualification_root: `{state['qualification_root']}`\n"
        + f"- source_assets: `{state['source_assets']}`\n"
        + f"- target_assets: `{state['target_assets']}`\n"
        + f"- response_path: `{response_path}`\n\n"
        + "Execute this audit as one fresh ChatGPT Work Cloud subagent. Use only read operations on the repository, "
        + "qualification root, assets, interactions, and scenario workspaces. Do not use web search, cloud browser, "
        + "plugins, apps, MCPs, external repositories, or user-local files. The only permitted write is the final "
        + "audit JSON object to response_path.\n"
    )
    prompt_path.write_text(prompt, encoding="utf-8")
    state["audit"] = {
        "status": "requested",
        "request_path": str(prompt_path.resolve()),
        "response_path": str(response_path.resolve()),
        "repository_sha256": automation.tree_digest(repository_root, exclude=[repository_root / ".git"]),
        "execution_sha256": automation.tree_digest(execution_root, exclude=[audit_root]),
        "qualification_root_sha256": automation.tree_digest(resolve(state["qualification_root"])),
        "source_assets_sha256": automation.tree_digest(resolve(state["source_assets"])),
        "target_assets_sha256": automation.tree_digest(resolve(state["target_assets"])),
    }
    save_state(state)
    print(f"AUDIT_SUBAGENT_REQUIRED {prompt_path}")
    return 3


def interaction_payload(state: dict[str, Any]) -> dict[str, Any]:
    root = resolve(state["execution_root"]) / "interactions"
    records: list[dict[str, Any]] = []
    if root.is_dir():
        for path in sorted(root.glob("*.response.json")):
            response = automation.load_json(path)
            records.append(
                {
                    "interaction_id": response["interaction_id"],
                    "scenario": response["scenario"],
                    "stage": response["stage"],
                    "prompt_sha256": response["prompt_sha256"],
                    "model": response["model"],
                    "workspace_root": response["workspace_root"],
                    "final_response": response["final_response"],
                    "required_reading": response["required_reading"],
                    "external_tools_used": response["external_tools_used"],
                    "response_sha256": automation.sha256_file(path),
                }
            )
    return {
        "schema_version": 1,
        "work_protocol_version": WORK_PROTOCOL_VERSION,
        "qualification_host": WORK_HOST,
        "run_id": state["run_id"],
        "qualification_phase": state["phase"],
        "interactions": records,
    }


def validate_audit_immutability(state: dict[str, Any]) -> dict[str, Any]:
    audit_state = state.get("audit")
    if not isinstance(audit_state, dict) or audit_state.get("status") != "requested":
        raise WorkQualificationError("independent audit has not been requested")
    response_path = Path(audit_state["response_path"])
    if not response_path.is_file():
        raise WorkQualificationError(f"audit subagent response is not ready: {response_path}")
    repository_root = resolve(state["repository_root"])
    execution_root = resolve(state["execution_root"])
    audit_root = execution_root / "audit"
    if automation.tree_digest(repository_root, exclude=[repository_root / ".git"]) != audit_state["repository_sha256"]:
        raise WorkQualificationError("independent audit mutated the Ava repository")
    if automation.tree_digest(execution_root, exclude=[audit_root]) != audit_state["execution_sha256"]:
        raise WorkQualificationError("independent audit mutated scenario or interaction evidence")
    for field, path in (
        ("qualification_root_sha256", resolve(state["qualification_root"])),
        ("source_assets_sha256", resolve(state["source_assets"])),
        ("target_assets_sha256", resolve(state["target_assets"])),
    ):
        if automation.tree_digest(path) != audit_state[field]:
            raise WorkQualificationError("independent audit mutated immutable qualification inputs")
    audit = automation.load_json(response_path)
    schema = automation.load_json(
        repository_root / "internal/release/qualification/schemas/audit-output.schema.json"
    )
    automation.validate_schema(audit, schema, label="Work independent audit")
    return audit


def write_compact_evidence(state: dict[str, Any], audit: dict[str, Any]) -> tuple[str, int]:
    repository_root = resolve(state["repository_root"])
    state_root = repository_root / "internal/release/qualification"
    run_id = state["run_id"]
    summary = automation.load_json(resolve(state["execution_root"]) / SUMMARY_NAME)
    interactions = interaction_payload(state)
    issues = {"schema_version": 1, "run_id": run_id, "issues": audit.get("findings", [])}
    audit_state, audit_exit = automation.audit_status(audit)
    if state["phase"] == "edge-independent":
        automated_state = "needs-review" if audit_state == "needs-review" else "passed"
        final_exit = 1 if automated_state == "needs-review" else 0
        runs_root = state_root / "phase-runs"
        run_record = {
            "schema_version": 1,
            "run_id": run_id,
            "pair_id": state["pair_id"],
            "qualification_phase": "edge-independent",
            "execution_identity_sha256": state["execution_identity_sha256"],
            "execution_identity": state["execution_identity"],
            "source": state["source"],
            "target": state["target"],
            "qualification_model": state["qualification_model"],
            "audit_model": state["audit_model"],
            "qualification_host": WORK_HOST,
            "work_protocol_version": WORK_PROTOCOL_VERSION,
            "runner_summary_file": f"{run_id}.summary.json",
            "interaction_evidence_file": f"{run_id}.interactions.json",
            "audit_report_file": f"{run_id}.audit.json",
            "issues_file": f"{run_id}.issues.json",
            "automated_state": automated_state,
            "mechanical_error": None,
        }
        schema_name = "work-edge-independent-run.schema.json"
    else:
        automated_state, final_exit = audit_state, audit_exit
        runs_root = state_root / "runs"
        run_record = {
            "schema_version": 1,
            "run_id": run_id,
            "pair_id": state["pair_id"],
            "execution_identity_sha256": state["execution_identity_sha256"],
            "execution_identity": state["execution_identity"],
            "source": state["source"],
            "target": state["target"],
            "qualification_model": state["qualification_model"],
            "audit_model": state["audit_model"],
            "qualification_host": WORK_HOST,
            "work_protocol_version": WORK_PROTOCOL_VERSION,
            "runner_summary_file": f"{run_id}.summary.json",
            "interaction_evidence_file": f"{run_id}.interactions.json",
            "audit_report_file": f"{run_id}.audit.json",
            "issues_file": f"{run_id}.issues.json",
            "automated_state": automated_state,
            "mechanical_error": None,
            "user_signoff": None,
        }
        schema_name = "work-run-record.schema.json"

    schema = automation.load_json(state_root / "schemas" / schema_name)
    automation.validate_schema(run_record, schema, label="Work qualification run record")
    runs_root.mkdir(parents=True, exist_ok=True)
    for suffix, payload in (
        ("json", run_record),
        ("summary.json", summary),
        ("interactions.json", interactions),
        ("audit.json", audit),
        ("issues.json", issues),
    ):
        filename = f"{run_id}.{suffix}" if suffix != "json" else f"{run_id}.json"
        (runs_root / filename).write_text(canonical_json(payload), encoding="utf-8")

    if state["phase"] == "edge-independent":
        phase_state = load_phase_state(repository_root)
        phase_state["pairs"][state["pair_id"]] = {
            "latest_run_id": run_id,
            "status": automated_state,
        }
        (state_root / "phase-state.json").write_text(
            canonical_json(phase_state), encoding="utf-8"
        )
    else:
        current_path = state_root / "current-state.json"
        current = automation.load_json(current_path)
        pair_state = current["pairs"][state["pair_id"]]
        pair_state["latest_run_id"] = run_id
        pair_state["status"] = automated_state
        pair_state["user_signoff"] = None
        current_path.write_text(canonical_json(current), encoding="utf-8")
    return automated_state, final_exit


def finalize_run(args: argparse.Namespace) -> int:
    execution_root = resolve(args.execution_root)
    state = load_state(execution_root)
    if state.get("finalized"):
        raise WorkQualificationError("qualification run is already finalized")
    summary = automation.load_json(execution_root / SUMMARY_NAME)
    if qualification_runner.summary_exit_status(summary.get("outcomes", [])) != 0:
        raise WorkQualificationError("cannot finalize a mechanically non-passing Work qualification run")
    audit = validate_audit_immutability(state)
    automated_state, final_exit = write_compact_evidence(state, audit)
    state["audit"]["status"] = "complete"
    state["finalized"] = True
    save_state(state)
    print(f"qualification phase run: {state['run_id']}")
    print(f"qualification phase: {state['phase']}")
    print(f"qualification host: {WORK_HOST}")
    print(f"automated state: {automated_state}")
    return final_exit


def validate_config(args: argparse.Namespace) -> int:
    repository_root = resolve(args.repository_root)
    config, _, _ = automation.load_configuration(repository_root)
    phase_runner.load_phase_state if False else None
    print(f"qualification configuration valid: active pair {config['active_pair']}")
    print(f"required execution host: {WORK_HOST}")
    return 0


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-config")

    init = subparsers.add_parser("init")
    init.add_argument("--phase", choices=phase_runner.PHASES, required=True)
    init.add_argument("--qualification-root", type=Path, required=True)
    init.add_argument("--execution-root", type=Path, required=True)
    init.add_argument("--source-assets", type=Path, required=True)
    init.add_argument("--target-assets", type=Path, required=True)
    init.add_argument("--test-project", type=Path, required=True)

    for name in ("advance", "audit-request", "finalize"):
        item = subparsers.add_parser(name)
        item.add_argument("--execution-root", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "validate-config":
            return validate_config(args)
        if args.command == "init":
            return init_run(args)
        if args.command == "advance":
            return advance_run(args)
        if args.command == "audit-request":
            return audit_request(args)
        return finalize_run(args)
    except (
        WorkQualificationError,
        automation.AutomationError,
        phase_gate.QualificationPhaseGateError,
        phase_runner.QualificationPhaseError,
        qualification_runner.QualificationError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(f"ChatGPT Work qualification error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
