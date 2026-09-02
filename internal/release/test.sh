#!/bin/sh
set -eu

ROOT=$(CDPATH= cd "$(dirname "$0")/../.." && pwd)
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"
cd "$ROOT"

sh "$ROOT/internal/release/validate-boundaries.sh"
sh -n "$ROOT/internal/release/assemble.sh"
sh -n "$ROOT/internal/release/assemble-candidate.sh"
sh -n "$ROOT/internal/release/ava-install.sh"
sh -n "$ROOT/internal/release/qualify-release.sh"
sh -n "$ROOT/internal/release/accept-release-qualification.sh"
sh -n "$ROOT/internal/release/qualification-opencode.sh"
sh -n "$ROOT/internal/release/test-project-backlog.sh"
python3 -m py_compile \
  "$ROOT/internal/release/adjacent_edges.py" \
  "$ROOT/internal/release/release_catalog.py" \
  "$ROOT/internal/release/compose_adjacent_catalog.py" \
  "$ROOT/internal/release/validate_adjacent_catalog.py" \
  "$ROOT/internal/release/assemble.py" \
  "$ROOT/internal/release/assemble_reviewed.py" \
  "$ROOT/internal/release/conformance.py" \
  "$ROOT/internal/release/conformance_common.py" \
  "$ROOT/internal/release/conformance_repository.py" \
  "$ROOT/internal/release/conformance_installed.py" \
  "$ROOT/internal/release/interaction_evidence.py" \
  "$ROOT/internal/release/_qualification_runner_core.py" \
  "$ROOT/internal/release/_qualification_automation_core.py" \
  "$ROOT/internal/release/qualification_runner.py" \
  "$ROOT/internal/release/qualification_automation.py" \
  "$ROOT/internal/release/qualification_acceptance.py" \
  "$ROOT/internal/release/qualification_phase_runner.py" \
  "$ROOT/internal/release/qualification_phase_automation.py" \
  "$ROOT/internal/release/qualification_phase_gate.py" \
  "$ROOT/internal/release/fixtures/synthetic-qualification-vault/checkpoint.py" \
  "$ROOT/internal/release/fixtures/synthetic-qualification-vault/fixture.py" \
  "$ROOT/internal/release/validate-installed-paths.py" \
  "$ROOT/internal/release/validate_pr_title.py" \
  "$ROOT/internal/release/validate_release_pr.py" \
  "$ROOT/internal/release/validate_upgrade_impact.py"
python3 "$ROOT/internal/release/validate-installed-paths.py" --root "$ROOT"
python3 "$ROOT/internal/release/validate_adjacent_catalog.py" \
  "$ROOT/internal/release/catalogs/1.0.0-alpha.12.json" \
  --guidance-root "$ROOT/internal/release/guidance" \
  --installed-version 1.0.0-alpha.11 \
  --compatible-through 1.0.0-alpha.9
python3 "$ROOT/internal/release/conformance.py" \
  --root "$ROOT" \
  --mode repository \
  --format text
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v \
  internal.release.tests.test_installed_paths \
  internal.release.tests.test_installer \
  internal.release.tests.test_transaction_cleanup \
  internal.release.tests.test_semantic_upgrade \
  internal.release.tests.test_installer_conformance \
  internal.release.tests.test_host_config \
  internal.release.tests.test_root_routing \
  internal.release.tests.test_project_task_board \
  internal.release.tests.test_review_sufficiency \
  internal.release.tests.test_calendar_verification \
  internal.release.tests.test_document_update_metadata_fixtures \
  internal.release.tests.test_knowledge_hierarchy_promotion \
  internal.release.tests.test_inbox_ingestion_fidelity \
  internal.release.tests.test_inbox_scoped_history \
  internal.release.tests.test_interaction_evidence \
  internal.release.tests.test_ava_maintenance \
  internal.release.tests.test_synthetic_qualification_vault \
  internal.release.tests.test_qualification_checkpoints \
  internal.release.tests.test_qualification_runner \
  internal.release.tests.test_qualification_automation \
  internal.release.tests.test_qualification_execution_identity \
  internal.release.tests.test_qualification_opencode_adapter \
  internal.release.tests.test_qualification_phases \
  internal.release.tests.test_assemble_candidate \
  internal.release.tests.test_qualification_acceptance \
  internal.release.tests.test_adjacent_edges \
  internal.release.tests.test_release_catalog \
  internal.release.tests.test_release_catalog_history \
  internal.release.tests.test_conformance \
  internal.release.tests.test_conformance_matrix \
  internal.release.tests.test_alpha_qualification \
  internal.release.tests.test_release_please \
  internal.release.tests.test_semantic_impact_assessment \
  internal.release.tests.release_pr_policy_test
