#!/usr/bin/env python3
"""Run one release qualification phase through a host-neutral execution contract."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from internal.release import qualification_automation as automation
from internal.release import qualification_host
from internal.release import qualification_phase_gate as phase_gate
from internal.release import qualification_phase_runner as phase_contract
from internal.release import qualification_runner

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
STATE_ROOT = automation.STATE_ROOT
PHASE_RUNS_ROOT = STATE_ROOT / "phase-runs"
PHASE_STATE_PATH = STATE_ROOT / "phase-state.json"
PHASES = phase_contract.PHASES


class QualificationHostAutomationError(RuntimeError):
    pass


def load_phase_state(repository_root: Path) -> dict[str, Any]:
    path = repository_root / PHASE_STATE_PATH.relative_to(automation.REPOSITORY_ROOT)
    state = automation.load_json(path)
    if state.get("schema_version") != 1 or not isinstance(state.get("pairs"), dict):
        raise QualificationHostAutomationError(
            f"invalid edge-independent qualification state: {path}"
        )
    return state


def prerequisite_run(
    repository_root: Path,
    *,
    pair_id: str,
) -> tuple[str, dict[str, Any]]:
    state = load_phase_state(repository_root)
    pair_state = state["pairs"].get(pair_id)
    if not isinstance(pair_state, dict) or pair_state.get("status") != "passed":
        raise QualificationHostAutomationError(
            "edge-dependent qualification requires a committed clean edge-independent phase first"
        )
    run_id = pair_state.get("latest_run_id")
    if not isinstance(run_id, str) or not run_id:
        raise QualificationHostAutomationError(
            "edge-independent phase state has no prerequisite run id"
        )
    path = (
        repository_root
        / PHASE_RUNS_ROOT.relative_to(automation.REPOSITORY_ROOT)
        / f"{run_id}.json"
    )
    return run_id, automation.load_json(path)


def execution_identity(
    *,
    repository_root: Path,
    phase: str,
    source: automation.ResolvedRelease,
    target: automation.ResolvedRelease,
    pinned_image_manifest: dict[str, Any],
    fixture_inventory_sha256: str,
    repository_revision_value: str,
    qualification_host_descriptor: qualification_host.HostDescriptor,
    audit_host_descriptor: qualification_host.HostDescriptor,
    qualification_model: str,
    audit_model: str,
    prerequisite_run_id: str | None,
    prerequisite_repository_revision: str | None,
) -> tuple[str, dict[str, Any]]:
    payload = {
        "schema_version": 1,
        "qualification_phase": phase,
        "source": source.compact(),
        "target": target.compact(),
        "image_manifest_sha256": automation.sha256_file(
            repository_root
            / automation.IMAGE_MANIFEST_PATH.relative_to(automation.REPOSITORY_ROOT)
        ),
        "pinned_images": [
            {
                "file": item["file"],
                "sha256": item["sha256"],
                "destination": item["destination"],
            }
            for item in pinned_image_manifest["images"]
        ],
        "fixture_generator_sha256": automation.sha256_file(
            repository_root / "internal/release/generate-synthetic-qualification-vault.sh"
        ),
        "fixture_inventory_sha256": fixture_inventory_sha256,
        "matrix_sha256": automation.matrix_digest(repository_root),
        "repository_revision": repository_revision_value,
        "host_runner_sha256": automation.sha256_file(
            repository_root / "internal/release/qualification_host_runner.py"
        ),
        "host_contract_sha256": automation.sha256_file(
            repository_root / "internal/release/qualification_host.py"
        ),
        "scenario_engine_sha256": automation.sha256_file(
            repository_root / "internal/release/qualification_runner.py"
        ),
        "qualification_host": qualification_host_descriptor.compact(),
        "audit_host": audit_host_descriptor.compact(),
        "qualification_model": qualification_model,
        "audit_model": audit_model,
        "prerequisite_edge_independent_run_id": prerequisite_run_id,
        "prerequisite_repository_revision": prerequisite_repository_revision,
    }
    return automation.sha256_text(automation.canonical_json(payload)), payload


def build_audit_prompt(
    *,
    phase: str,
    pair_id: str,
    run_id: str,
    execution_identity_sha256: str,
    interaction_inventory_path: Path,
    runner_summary_path: Path,
    qualification_root: Path,
    source_assets: Path,
    target_assets: Path,
    repository_root: Path,
) -> str:
    maintained = (
        repository_root
        / automation.AUDIT_PROMPT_PATH.relative_to(automation.REPOSITORY_ROOT)
    ).read_text(encoding="utf-8")
    return (
        maintained
        + "\n\n# Run inputs\n\n"
        + f"- pair_id: `{pair_id}`\n"
        + f"- run_id: `{run_id}`\n"
        + f"- qualification_phase: `{phase}`\n"
        + f"- execution_identity_sha256: `{execution_identity_sha256}`\n"
        + f"- interaction_inventory: `{interaction_inventory_path}`\n"
        + f"- runner_summary: `{runner_summary_path}`\n"
        + f"- qualification_root: `{qualification_root}`\n"
        + f"- source_assets: `{source_assets}`\n"
        + f"- target_assets: `{target_assets}`\n"
        + f"- release_contracts: `{repository_root / 'distribution'}` and `{repository_root / 'internal/release'}`\n"
        + "\nThe interaction inventory is host-neutral evidence. Do not require host-specific session IDs, database rows, export formats, or token metadata. "
        + "Audit only scenarios present in this phase's runner summary and interaction inventory; scenarios assigned to the other phase are intentionally absent.\n\n"
        + "Return only the JSON object required by the maintained audit-output schema.\n"
    )


def write_evidence(
    *,
    repository_root: Path,
    phase: str,
    run_id: str,
    pair_id: str,
    execution_identity_sha256: str,
    execution_identity_payload: dict[str, Any],
    source: automation.ResolvedRelease,
    target: automation.ResolvedRelease,
    qualification_host_descriptor: qualification_host.HostDescriptor,
    audit_host_descriptor: qualification_host.HostDescriptor,
    qualification_model: str,
    audit_model: str,
    qualification_root: Path,
    raw_evidence_root: Path,
    interaction_inventory: dict[str, Any] | None,
    audit: dict[str, Any] | None,
    runner_summary: dict[str, Any] | None,
    automated_state: str,
    mechanical_error: str | None,
) -> None:
    state_root = repository_root / STATE_ROOT.relative_to(automation.REPOSITORY_ROOT)
    is_early = phase == "edge-independent"
    runs_root = state_root / ("phase-runs" if is_early else "runs")
    runs_root.mkdir(parents=True, exist_ok=True)
    issues = audit.get("findings", []) if audit else []

    run_record: dict[str, Any] = {
        "schema_version": 1,
        "run_id": run_id,
        "pair_id": pair_id,
        "execution_identity_sha256": execution_identity_sha256,
        "execution_identity": execution_identity_payload,
        "source": source.compact(),
        "target": target.compact(),
        "qualification_model": qualification_model,
        "audit_model": audit_model,
        "qualification_host": qualification_host_descriptor.compact(),
        "audit_host": audit_host_descriptor.compact(),
        "qualification_root_sha256": automation.tree_digest(qualification_root),
        "runner_summary_sha256": (
            automation.sha256_text(automation.canonical_json(runner_summary))
            if runner_summary is not None
            else None
        ),
        "interaction_inventory_file": (
            f"{run_id}.interactions.json" if interaction_inventory is not None else None
        ),
        "audit_report_file": f"{run_id}.audit.json" if audit else None,
        "issues_file": f"{run_id}.issues.json",
        "raw_evidence": {
            "path": str(raw_evidence_root.resolve()),
            "sha256": automation.tree_digest(raw_evidence_root),
        },
        "automated_state": automated_state,
        "mechanical_error": mechanical_error,
    }
    if is_early:
        run_record["qualification_phase"] = "edge-independent"
        schema_name = "host-edge-independent-run.schema.json"
    else:
        run_record["user_signoff"] = None
        schema_name = "host-run-record.schema.json"

    schema = automation.load_json(state_root / "schemas" / schema_name)
    automation.validate_schema(run_record, schema, label="host-neutral run record")

    (runs_root / f"{run_id}.json").write_text(
        automation.canonical_json(run_record),
        encoding="utf-8",
    )
    (runs_root / f"{run_id}.issues.json").write_text(
        automation.canonical_json(
            {"schema_version": 1, "run_id": run_id, "issues": issues}
        ),
        encoding="utf-8",
    )
    if interaction_inventory is not None:
        qualification_host.validate_interaction_inventory(interaction_inventory)
        interaction_schema = automation.load_json(
            state_root / "schemas/interaction-inventory.schema.json"
        )
        automation.validate_schema(
            interaction_inventory,
            interaction_schema,
            label="interaction inventory",
        )
        (runs_root / f"{run_id}.interactions.json").write_text(
            automation.canonical_json(interaction_inventory),
            encoding="utf-8",
        )
    if audit:
        (runs_root / f"{run_id}.audit.json").write_text(
            automation.canonical_json(audit),
            encoding="utf-8",
        )

    if is_early:
        phase_state = load_phase_state(repository_root)
        phase_state["pairs"][pair_id] = {
            "latest_run_id": run_id,
            "status": automated_state,
        }
        (state_root / "phase-state.json").write_text(
            automation.canonical_json(phase_state),
            encoding="utf-8",
        )
    else:
        current_path = state_root / "current-state.json"
        current = automation.load_json(current_path)
        pair_state = current["pairs"][pair_id]
        pair_state["latest_run_id"] = run_id
        pair_state["status"] = automated_state
        pair_state["user_signoff"] = None
        schema = automation.load_json(state_root / "schemas/current-state.schema.json")
        automation.validate_schema(current, schema, label="current qualification state")
        current_path.write_text(automation.canonical_json(current), encoding="utf-8")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--phase", choices=PHASES)
    parser.add_argument("--source-assets", type=Path)
    parser.add_argument("--target-assets", type=Path)
    parser.add_argument("--run-root-parent", type=Path)
    parser.add_argument("--host-kind", default="opencode")
    parser.add_argument("--host-executable", default="opencode")
    parser.add_argument("--gh", default="gh")
    parser.add_argument("--validate-config-only", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repository_root = args.repository_root.expanduser().resolve()
    try:
        config, catalog, _ = automation.load_configuration(repository_root)
        pinned_image_manifest = automation.validate_pinned_images(repository_root)
        load_phase_state(repository_root)
        matrix = qualification_runner.load_matrix(
            repository_root
            / "internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json"
        )
        chatgpt = qualification_host.assess_host(
            qualification_host.chatgpt_github_profile(),
            matrix,
        )
        if chatgpt.complete:
            raise QualificationHostAutomationError(
                "ChatGPT GitHub capability profile unexpectedly satisfies local qualification requirements"
            )
        if args.validate_config_only:
            print(f"qualification configuration valid: active pair {config['active_pair']}")
            print(
                "ChatGPT GitHub execution remains partial: missing "
                + ", ".join(chatgpt.global_missing)
            )
            return 0
        if args.phase not in PHASES:
            raise QualificationHostAutomationError(
                "release qualification requires --phase edge-independent or --phase edge-dependent"
            )

        automation.require_clean_repository(repository_root)
        pair = automation.active_pair(config, catalog)
        run_id = automation.utc_run_id(pair["id"])
        parent = (
            args.run_root_parent.expanduser().resolve()
            if args.run_root_parent
            else Path(os.environ.get("TMPDIR", tempfile.gettempdir())).expanduser().resolve()
        )
        if parent == repository_root or parent.is_relative_to(repository_root):
            raise QualificationHostAutomationError(
                "run root parent must be outside the Ava repository"
            )

        run_root = parent / f"ava-qualification-{args.phase}-{run_id}"
        run_root.mkdir(parents=True)
        assets_root = run_root / "assets"
        fixture_parent = run_root / "fixture"
        execution_parent = run_root / "execution"
        transcript_root = run_root / "transcripts"
        audit_root = run_root / "audit"
        test_project = run_root / "test-project"
        for path in (
            assets_root,
            fixture_parent,
            execution_parent,
            transcript_root,
            audit_root,
        ):
            path.mkdir(parents=True, exist_ok=True)
        automation.create_test_project(test_project)

        source = automation.resolve_release(
            pair["source"],
            local_path=args.source_assets,
            destination=assets_root / "source",
            repository=config["repository"],
            gh=args.gh,
            label="source assets",
        )
        target = automation.resolve_release(
            pair["target"],
            local_path=args.target_assets,
            destination=assets_root / "target",
            repository=config["repository"],
            gh=args.gh,
            label="target assets",
        )
        phase_contract.validate_release_pair(source.identity, target.identity)
        if args.phase == "edge-dependent":
            qualification_runner.validate_upgrade_pair(source.identity, target.identity)

        qualification_root = automation.generate_fixture(repository_root, fixture_parent)
        fixture_inventory_sha256 = automation.tree_digest(qualification_root)
        host = qualification_host.resolve_host_adapter(
            args.host_kind,
            args.host_executable,
        )
        host_descriptor = host.descriptor()
        repo_revision = automation.repository_revision(repository_root)

        prerequisite_run_id: str | None = None
        prerequisite_revision: str | None = None
        if args.phase == "edge-dependent":
            prerequisite_run_id, early = prerequisite_run(
                repository_root,
                pair_id=pair["id"],
            )
            early_identity = early.get("execution_identity")
            if not isinstance(early_identity, dict):
                raise QualificationHostAutomationError(
                    "edge-independent prerequisite has no execution identity"
                )
            prerequisite_revision = early_identity.get("repository_revision")
            preview_run = {
                "pair_id": pair["id"],
                "source": source.compact(),
                "target": target.compact(),
                "execution_identity": {
                    "qualification_phase": "edge-dependent",
                    "repository_revision": repo_revision,
                    "prerequisite_edge_independent_run_id": prerequisite_run_id,
                    "prerequisite_repository_revision": prerequisite_revision,
                },
            }
            phase_gate.validate_phase_prerequisite(
                repository_root,
                preview_run,
                previous_version=source.identity.version,
                target_version=target.identity.version,
            )

        identity_sha, identity_payload = execution_identity(
            repository_root=repository_root,
            phase=args.phase,
            source=source,
            target=target,
            pinned_image_manifest=pinned_image_manifest,
            fixture_inventory_sha256=fixture_inventory_sha256,
            repository_revision_value=repo_revision,
            qualification_host_descriptor=host_descriptor,
            audit_host_descriptor=host_descriptor,
            qualification_model=config["qualification_model"],
            audit_model=config["audit_model"],
            prerequisite_run_id=prerequisite_run_id,
            prerequisite_repository_revision=prerequisite_revision,
        )
        execution_root = automation.execution_root_for_identity(
            execution_parent,
            identity_sha,
        )
        source_path = source.identity.directory
        target_path = target.identity.directory

        base_command = [
            sys.executable,
            str(repository_root / "internal/release/qualification_host_runner.py"),
            "--phase",
            args.phase,
            "--repository-root",
            str(repository_root),
            "--qualification-root",
            str(qualification_root),
            "--execution-root",
            str(execution_root),
            "--source-assets",
            str(source_path),
            "--target-assets",
            str(target_path),
            "--test-project",
            str(test_project),
            "--host-kind",
            args.host_kind,
            "--host-executable",
            args.host_executable,
            "--model",
            config["qualification_model"],
            "--transcript-dir",
            str(transcript_root),
        ]
        automation.run_command([*base_command, "--preflight-only"], cwd=repository_root)
        interactions_before = host.snapshot()
        runner_result = automation.run_command(
            base_command,
            cwd=repository_root,
            check=False,
        )
        summary_path = execution_root / "summary.json"
        summary = automation.load_json(summary_path) if summary_path.is_file() else None

        interaction_inventory: dict[str, Any] | None = None
        audit: dict[str, Any] | None = None
        mechanical_error: str | None = None
        automated_state = "failed"
        final_exit = 1

        runner_passed = (
            runner_result.returncode == 0
            and summary is not None
            and summary.get("qualification_phase") == args.phase
            and automation.qualification_exit(summary) == 0
        )
        if not runner_passed:
            mechanical_error = (
                f"qualification runner exited {runner_result.returncode}"
                if runner_result.returncode != 0
                else "qualification runner did not produce an all-pass phase summary"
            )

        try:
            interactions_after = host.snapshot()
            interaction_inventory = host.collect_interactions(
                before=interactions_before,
                after=interactions_after,
                execution_root=execution_root,
                configured_model=config["qualification_model"],
                allow_empty=not runner_passed,
            )
        except (
            qualification_host.QualificationHostError,
            automation.AutomationError,
        ) as exc:
            if runner_passed:
                mechanical_error = f"interaction evidence failed: {exc}"
                runner_passed = False
            else:
                mechanical_error = f"{mechanical_error}; interaction evidence failed: {exc}"

        inventory_path = audit_root / "interaction-inventory.json"
        if interaction_inventory is not None:
            inventory_path.write_text(
                automation.canonical_json(interaction_inventory),
                encoding="utf-8",
            )

        if (
            summary is not None
            and interaction_inventory is not None
            and interaction_inventory["interactions"]
        ):
            try:
                prompt = build_audit_prompt(
                    phase=args.phase,
                    pair_id=pair["id"],
                    run_id=run_id,
                    execution_identity_sha256=identity_sha,
                    interaction_inventory_path=inventory_path,
                    runner_summary_path=summary_path,
                    qualification_root=qualification_root,
                    source_assets=source_path,
                    target_assets=target_path,
                    repository_root=repository_root,
                )
                prompt_path = audit_root / "prompt.md"
                prompt_path.write_text(prompt, encoding="utf-8")
                audit, raw_audit = qualification_host.run_independent_audit(
                    adapter=host,
                    audit_model=config["audit_model"],
                    prompt=prompt,
                    repository_root=repository_root,
                    raw_evidence_root=run_root,
                )
                (audit_root / "raw.jsonl").write_text(raw_audit, encoding="utf-8")
            except (
                qualification_host.QualificationHostError,
                automation.AutomationError,
            ) as exc:
                mechanical_error = (
                    f"{mechanical_error}; independent audit failed: {exc}"
                    if mechanical_error
                    else f"independent audit failed: {exc}"
                )
                runner_passed = False

        if runner_passed and audit is not None:
            audit_state, audit_exit = automation.audit_status(audit)
            if args.phase == "edge-independent":
                if audit_state == "needs-review":
                    automated_state, final_exit = "needs-review", 1
                else:
                    automated_state, final_exit = "passed", 0
            else:
                automated_state, final_exit = audit_state, audit_exit
        elif runner_passed:
            mechanical_error = (
                mechanical_error
                or "successful qualification phase produced no independent audit"
            )
            automated_state, final_exit = "failed", 1

        write_evidence(
            repository_root=repository_root,
            phase=args.phase,
            run_id=run_id,
            pair_id=pair["id"],
            execution_identity_sha256=identity_sha,
            execution_identity_payload=identity_payload,
            source=source,
            target=target,
            qualification_host_descriptor=host_descriptor,
            audit_host_descriptor=host_descriptor,
            qualification_model=config["qualification_model"],
            audit_model=config["audit_model"],
            qualification_root=qualification_root,
            raw_evidence_root=run_root,
            interaction_inventory=interaction_inventory,
            audit=audit,
            runner_summary=summary,
            automated_state=automated_state,
            mechanical_error=mechanical_error,
        )

        print(f"qualification phase run: {run_id}")
        print(f"qualification phase: {args.phase}")
        print(
            f"qualification host: {host_descriptor.adapter} {host_descriptor.version}"
        )
        print(f"automated state: {automated_state}")
        print(f"external evidence: {run_root}")
        if args.phase == "edge-independent" and automated_state == "passed":
            print(
                "commit compact edge-independent evidence before authoring the adjacent release edge"
            )
        else:
            print(
                "compact evidence written under internal/release/qualification/ without committing"
            )
        return final_exit
    except (
        QualificationHostAutomationError,
        qualification_host.QualificationHostError,
        automation.AutomationError,
        phase_gate.QualificationPhaseGateError,
        phase_contract.QualificationPhaseError,
        qualification_runner.QualificationError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(f"release qualification host error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
