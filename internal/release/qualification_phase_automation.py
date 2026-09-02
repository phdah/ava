#!/usr/bin/env python3
"""Run one mechanically ordered phase of Ava release qualification."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from internal.release import qualification_automation as automation
from internal.release import qualification_phase_gate as phase_gate
from internal.release import qualification_phase_runner as phase_runner
from internal.release import qualification_runner

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
PHASE_RUNS_ROOT = automation.STATE_ROOT / "phase-runs"
PHASE_STATE_PATH = automation.STATE_ROOT / "phase-state.json"
PHASES = phase_runner.PHASES


class QualificationPhaseAutomationError(RuntimeError):
    pass


def load_phase_state(repository_root: Path) -> dict[str, Any]:
    path = repository_root / PHASE_STATE_PATH.relative_to(automation.REPOSITORY_ROOT)
    state = automation.load_json(path)
    if state.get("schema_version") != 1 or not isinstance(state.get("pairs"), dict):
        raise QualificationPhaseAutomationError(
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
        raise QualificationPhaseAutomationError(
            "edge-dependent qualification requires a committed clean edge-independent phase first"
        )
    run_id = pair_state.get("latest_run_id")
    if not isinstance(run_id, str) or not run_id:
        raise QualificationPhaseAutomationError(
            "edge-independent phase state has no prerequisite run id"
        )
    path = (
        repository_root
        / PHASE_RUNS_ROOT.relative_to(automation.REPOSITORY_ROOT)
        / f"{run_id}.json"
    )
    return run_id, automation.load_json(path)


def phase_execution_identity(
    *,
    repository_root: Path,
    phase: str,
    source: automation.ResolvedRelease,
    target: automation.ResolvedRelease,
    pinned_image_manifest: dict[str, Any],
    fixture_inventory_sha256: str,
    repository_revision_value: str,
    opencode_version_value: str,
    qualification_model: str,
    audit_model: str,
    prerequisite_run_id: str | None,
    prerequisite_repository_revision: str | None,
) -> tuple[str, dict[str, Any]]:
    _, payload = automation.execution_identity(
        source=source,
        target=target,
        image_manifest_sha256=automation.sha256_file(
            repository_root
            / automation.IMAGE_MANIFEST_PATH.relative_to(automation.REPOSITORY_ROOT)
        ),
        pinned_images=[
            {
                "file": item["file"],
                "sha256": item["sha256"],
                "destination": item["destination"],
            }
            for item in pinned_image_manifest["images"]
        ],
        fixture_generator_sha256=automation.sha256_file(
            repository_root / "internal/release/generate-synthetic-qualification-vault.sh"
        ),
        fixture_inventory_sha256=fixture_inventory_sha256,
        matrix_sha256=automation.matrix_digest(repository_root),
        repository_revision_value=repository_revision_value,
        runner_sha256=automation.sha256_file(
            repository_root / "internal/release/qualification_phase_runner.py"
        ),
        automation_sha256=automation.sha256_file(
            repository_root / "internal/release/qualification_phase_automation.py"
        ),
        opencode_version_value=opencode_version_value,
        qualification_model=qualification_model,
        audit_model=audit_model,
    )
    payload["qualification_phase"] = phase
    payload["qualification_component_sha256"] = automation.sha256_file(
        repository_root / "internal/release/qualification_runner.py"
    )
    payload["prerequisite_edge_independent_run_id"] = prerequisite_run_id
    payload["prerequisite_repository_revision"] = prerequisite_repository_revision
    return automation.sha256_text(automation.canonical_json(payload)), payload


def build_phase_audit_prompt(
    *,
    phase: str,
    pair_id: str,
    run_id: str,
    execution_identity_sha256: str,
    session_inventory_path: Path,
    runner_summary_path: Path,
    qualification_root: Path,
    source_assets: Path,
    target_assets: Path,
    repository_root: Path,
) -> str:
    prompt = automation.build_audit_prompt(
        pair_id=pair_id,
        run_id=run_id,
        execution_identity_sha256=execution_identity_sha256,
        session_inventory_path=session_inventory_path,
        runner_summary_path=runner_summary_path,
        qualification_root=qualification_root,
        source_assets=source_assets,
        target_assets=target_assets,
        repository_root=repository_root,
    )
    return (
        prompt
        + "\n# Qualification phase\n\n"
        + f"qualification_phase: `{phase}`\n\n"
        + "Audit only the scenarios present in this phase's runner summary and session inventory. "
        + "Scenarios assigned to the other qualification phase are intentionally absent and are not missing evidence.\n"
    )


def write_edge_independent_evidence(
    *,
    repository_root: Path,
    run_id: str,
    pair_id: str,
    execution_identity_sha256: str,
    execution_identity_payload: dict[str, Any],
    source: automation.ResolvedRelease,
    target: automation.ResolvedRelease,
    opencode_version_value: str,
    qualification_model: str,
    audit_model: str,
    qualification_root: Path,
    raw_evidence_root: Path,
    session_inventory: dict[str, Any] | None,
    audit: dict[str, Any] | None,
    runner_summary: dict[str, Any] | None,
    automated_state: str,
    mechanical_error: str | None,
) -> None:
    state_root = repository_root / automation.STATE_ROOT.relative_to(automation.REPOSITORY_ROOT)
    runs_root = state_root / "phase-runs"
    runs_root.mkdir(parents=True, exist_ok=True)

    issues = audit.get("findings", []) if audit else []
    run_record = {
        "schema_version": 1,
        "run_id": run_id,
        "pair_id": pair_id,
        "qualification_phase": "edge-independent",
        "execution_identity_sha256": execution_identity_sha256,
        "execution_identity": execution_identity_payload,
        "source": source.compact(),
        "target": target.compact(),
        "qualification_model": qualification_model,
        "audit_model": audit_model,
        "opencode_version": opencode_version_value,
        "qualification_root_sha256": automation.tree_digest(qualification_root),
        "runner_summary_sha256": (
            automation.sha256_text(automation.canonical_json(runner_summary))
            if runner_summary is not None
            else None
        ),
        "session_inventory_file": f"{run_id}.sessions.json" if session_inventory else None,
        "audit_report_file": f"{run_id}.audit.json" if audit else None,
        "issues_file": f"{run_id}.issues.json",
        "raw_evidence": {
            "path": str(raw_evidence_root.resolve()),
            "sha256": automation.tree_digest(raw_evidence_root),
        },
        "automated_state": automated_state,
        "mechanical_error": mechanical_error,
    }
    schema = automation.load_json(state_root / "schemas/edge-independent-run.schema.json")
    automation.validate_schema(run_record, schema, label="edge-independent run record")

    (runs_root / f"{run_id}.json").write_text(
        automation.canonical_json(run_record), encoding="utf-8"
    )
    (runs_root / f"{run_id}.issues.json").write_text(
        automation.canonical_json(
            {"schema_version": 1, "run_id": run_id, "issues": issues}
        ),
        encoding="utf-8",
    )
    if session_inventory:
        session_schema = automation.load_json(
            state_root / "schemas/session-inventory.schema.json"
        )
        automation.validate_schema(
            session_inventory, session_schema, label="edge-independent session inventory"
        )
        (runs_root / f"{run_id}.sessions.json").write_text(
            automation.canonical_json(session_inventory), encoding="utf-8"
        )
    if audit:
        (runs_root / f"{run_id}.audit.json").write_text(
            automation.canonical_json(audit), encoding="utf-8"
        )

    phase_state = load_phase_state(repository_root)
    phase_state["pairs"][pair_id] = {
        "latest_run_id": run_id,
        "status": automated_state,
    }
    phase_state_path = state_root / "phase-state.json"
    phase_state_path.write_text(
        automation.canonical_json(phase_state), encoding="utf-8"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--phase", choices=PHASES)
    parser.add_argument("--source-assets", type=Path)
    parser.add_argument("--target-assets", type=Path)
    parser.add_argument("--run-root-parent", type=Path)
    parser.add_argument("--opencode", default="opencode")
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
        if args.validate_config_only:
            print(f"qualification configuration valid: active pair {config['active_pair']}")
            return 0
        if args.phase not in PHASES:
            raise QualificationPhaseAutomationError(
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
            raise QualificationPhaseAutomationError(
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
        phase_runner.validate_release_pair(source.identity, target.identity)
        if args.phase == "edge-dependent":
            qualification_runner.validate_upgrade_pair(source.identity, target.identity)

        qualification_root = automation.generate_fixture(repository_root, fixture_parent)
        fixture_inventory_sha256 = automation.tree_digest(qualification_root)
        oc_version = automation.opencode_version(args.opencode)
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
                raise QualificationPhaseAutomationError(
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

        identity_sha, identity_payload = phase_execution_identity(
            repository_root=repository_root,
            phase=args.phase,
            source=source,
            target=target,
            pinned_image_manifest=pinned_image_manifest,
            fixture_inventory_sha256=fixture_inventory_sha256,
            repository_revision_value=repo_revision,
            opencode_version_value=oc_version,
            qualification_model=config["qualification_model"],
            audit_model=config["audit_model"],
            prerequisite_run_id=prerequisite_run_id,
            prerequisite_repository_revision=prerequisite_revision,
        )
        execution_root = automation.execution_root_for_identity(
            execution_parent, identity_sha
        )
        source_path = source.identity.directory
        target_path = target.identity.directory

        base_command = [
            sys.executable,
            str(repository_root / "internal/release/qualification_phase_runner.py"),
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
            "--opencode",
            args.opencode,
            "--model",
            config["qualification_model"],
            "--transcript-dir",
            str(transcript_root),
        ]
        automation.run_command(
            [*base_command, "--preflight-only"], cwd=repository_root
        )
        sessions_before = automation.snapshot_sessions(args.opencode)
        runner_result = automation.run_command(
            base_command, cwd=repository_root, check=False
        )
        summary_path = execution_root / "summary.json"
        summary = automation.load_json(summary_path) if summary_path.is_file() else None

        session_inventory: dict[str, Any] | None = None
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
            sessions_after = automation.snapshot_sessions(args.opencode)
            session_inventory = automation.build_session_inventory(
                before=sessions_before,
                after=sessions_after,
                execution_root=execution_root,
                opencode=args.opencode,
                configured_model=config["qualification_model"],
                allow_empty=not runner_passed,
            )
        except automation.AutomationError as exc:
            if runner_passed:
                mechanical_error = f"session inventory failed: {exc}"
                runner_passed = False
            else:
                mechanical_error = f"{mechanical_error}; session inventory failed: {exc}"

        if session_inventory is not None:
            inventory_path = audit_root / "session-inventory.json"
            inventory_path.write_text(
                automation.canonical_json(session_inventory), encoding="utf-8"
            )

        if (
            summary is not None
            and session_inventory is not None
            and session_inventory["sessions"]
        ):
            try:
                prompt = build_phase_audit_prompt(
                    phase=args.phase,
                    pair_id=pair["id"],
                    run_id=run_id,
                    execution_identity_sha256=identity_sha,
                    session_inventory_path=inventory_path,
                    runner_summary_path=summary_path,
                    qualification_root=qualification_root,
                    source_assets=source_path,
                    target_assets=target_path,
                    repository_root=repository_root,
                )
                prompt_path = audit_root / "prompt.md"
                prompt_path.write_text(prompt, encoding="utf-8")
                audit, raw_audit = automation.run_audit(
                    opencode=args.opencode,
                    audit_model=config["audit_model"],
                    prompt=prompt,
                    repository_root=repository_root,
                    raw_evidence_root=run_root,
                )
                (audit_root / "raw.jsonl").write_text(raw_audit, encoding="utf-8")
            except automation.AutomationError as exc:
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

        if args.phase == "edge-independent":
            write_edge_independent_evidence(
                repository_root=repository_root,
                run_id=run_id,
                pair_id=pair["id"],
                execution_identity_sha256=identity_sha,
                execution_identity_payload=identity_payload,
                source=source,
                target=target,
                opencode_version_value=oc_version,
                qualification_model=config["qualification_model"],
                audit_model=config["audit_model"],
                qualification_root=qualification_root,
                raw_evidence_root=run_root,
                session_inventory=session_inventory,
                audit=audit,
                runner_summary=summary,
                automated_state=automated_state,
                mechanical_error=mechanical_error,
            )
        else:
            automation.write_compact_evidence(
                repository_root=repository_root,
                run_id=run_id,
                pair_id=pair["id"],
                execution_identity_sha256=identity_sha,
                execution_identity_payload=identity_payload,
                source=source,
                target=target,
                opencode_version_value=oc_version,
                qualification_model=config["qualification_model"],
                audit_model=config["audit_model"],
                qualification_root=qualification_root,
                execution_root=execution_root,
                raw_evidence_root=run_root,
                session_inventory=session_inventory,
                audit=audit,
                runner_summary=summary,
                automated_state=automated_state,
                mechanical_error=mechanical_error,
            )

        print(f"qualification phase run: {run_id}")
        print(f"qualification phase: {args.phase}")
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
        QualificationPhaseAutomationError,
        automation.AutomationError,
        phase_gate.QualificationPhaseGateError,
        phase_runner.QualificationPhaseError,
        qualification_runner.QualificationError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(f"release qualification phase error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
