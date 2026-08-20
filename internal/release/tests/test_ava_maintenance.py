from __future__ import annotations

import json
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/ava-maintenance.json"
ROLE_ROOT = SOURCE_ROOT / "templates/base/roles/ava-maintenance"
ROUTER = SOURCE_ROOT / "templates/base/AGENTS.md"
ROUTING = SOURCE_ROOT / "templates/base/shared/instructions/upgrade-state-and-routing.md"
ROLE_CATALOG = SOURCE_ROOT / "templates/base/roles/index.md"
UPGRADE_ROLE = SOURCE_ROOT / "templates/base/roles/upgrade-role/role.md"
UPGRADE_PROTOCOL = SOURCE_ROOT / "distribution/upgrades.md"


class AvaMaintenanceFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}

    def test_required_role_files_exist(self) -> None:
        required = {
            "index.md",
            "role.md",
            "instructions.md",
            "capabilities.md",
            "constraints.md",
        }
        self.assertTrue(required.issubset({path.name for path in ROLE_ROOT.iterdir()}))
        index = (ROLE_ROOT / "index.md").read_text()
        for name in sorted(required - {"index.md"}):
            self.assertIn(f"({name})", index)
        self.assertIn("upgrade-state-and-routing.md", index)
        self.assertIn("ownership-and-mutation.md", index)

    def test_required_scenarios_are_present(self) -> None:
        required = {
            "healthy-report",
            "missing-managed-file",
            "modified-managed-file",
            "corrupt-state-file",
            "unexpected-managed-file",
            "interrupted-planning-abort",
            "interrupted-preflight-resume",
            "interrupted-live-rollback",
            "semantic-reconciliation-route",
            "semantic-status-inspection-route",
            "semantic-finalization-route",
            "terminal-cleanup-replay",
            "rolled-back-cleanup-replay",
            "idle-cleanup-replay",
            "prior-terminal-cleanup-replay",
            "idle-ambiguous-cleanup",
            "unavailable-host-capability",
            "opencode-accessible",
            "opencode-permission-missing",
            "uninstall-healthy",
            "uninstall-active-deterministic",
            "uninstall-active-semantic",
            "uninstall-modified-router",
            "uninstall-modified-managed-directory",
            "uninstall-preserves-project-owned",
            "uninstall-stale-host-entrypoint",
        }
        self.assertTrue(required.issubset(self.cases))

    def test_fixture_schema_tracks_agent_finalization_contract(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 2)

    def test_healthy_report_separates_installed_and_semantic_state(self) -> None:
        fields = set(self.cases["healthy-report"]["expected_report_fields"])
        self.assertTrue(
            {
                "ava_version",
                "release.channel",
                "release.source_revision",
                "okf_version",
                "semantic_compatibility.compatible_through",
                "semantic_compatibility.target_version",
                "semantic_compatibility.status",
            }.issubset(fields)
        )

    def test_deterministic_states_route_to_maintenance(self) -> None:
        for case_id in (
            "corrupt-state-file",
            "interrupted-planning-abort",
            "interrupted-preflight-resume",
            "interrupted-live-rollback",
            "semantic-status-inspection-route",
            "semantic-finalization-route",
            "terminal-cleanup-replay",
            "rolled-back-cleanup-replay",
            "idle-cleanup-replay",
            "prior-terminal-cleanup-replay",
            "idle-ambiguous-cleanup",
        ):
            self.assertEqual(self.cases[case_id]["expected_role"], "maintenance", case_id)

    def test_semantic_reconciliation_routes_to_upgrade_role(self) -> None:
        case = self.cases["semantic-reconciliation-route"]
        self.assertEqual(case["expected_role"], "upgrade")
        self.assertEqual(case["expected_operation"], "reconcile-semantic")

    def test_recovery_uses_existing_installer_mechanisms(self) -> None:
        for case_id in (
            "interrupted-planning-abort",
            "interrupted-preflight-resume",
            "interrupted-live-rollback",
        ):
            self.assertIn("existing-installer", self.cases[case_id]["mechanism"], case_id)

    def test_semantic_finalization_is_agent_driven_and_bounded(self) -> None:
        case = self.cases["semantic-finalization-route"]
        self.assertEqual(case["expected_operation"], "finalize")
        self.assertEqual(case["mechanism"], "agent-terminal-state-transition")
        self.assertFalse(case["requires_installer_binary"])
        self.assertEqual(case["cleanup"], "exact-transaction-id-directory-and-empty-container")
        self.assertEqual(
            set(case["required_preconditions"]),
            {
                "semantic-compatibility-complete",
                "no-unresolved-decisions",
                "managed-commit-complete",
                "path-edges-complete",
                "managed-changes-classified",
                "journal-finalizable",
                "transaction-directory-safe",
            },
        )
        self.assertEqual(
            case["expected_terminal_state"],
            {
                "journal_status": "complete",
                "journal_stage": "complete",
                "current_edge": None,
                "staging": None,
                "failure": None,
                "allowed_operations": ["normal"],
            },
        )

        instructions = (ROLE_ROOT / "instructions.md").read_text()
        capabilities = (ROLE_ROOT / "capabilities.md").read_text()
        constraints = (ROLE_ROOT / "constraints.md").read_text()
        routing = ROUTING.read_text()
        protocol = UPGRADE_PROTOCOL.read_text()
        self.assertIn("Finalization is the only deterministic journal transition Ava Maintenance performs directly", instructions)
        self.assertIn("must not trigger a search for an `ava` binary", instructions)
        self.assertIn("`./.ava/state/transactions/<transaction_id>/` directory recursively", instructions)
        self.assertIn("any sibling transaction directory", instructions)
        self.assertIn("non-recursive empty-directory operation", capabilities)
        self.assertIn("The finalization exception permits only the terminal fields", constraints)
        self.assertIn("sibling transaction directories", constraints)
        self.assertIn("This transition is the agent's finalization mechanism", routing)
        self.assertIn("does not require or imply an installed `ava` command", routing)
        self.assertIn("transaction-directory absence", routing)
        self.assertIn("Finalization is agent-driven and does not require an `ava` binary", protocol)
        self.assertIn("This is the only direct journal-mutation exception for Ava Maintenance", protocol)
        self.assertIn("not only the nested path recorded in `staging.workspace`", protocol)

    def test_interrupted_terminal_cleanup_blocks_normal_routing_and_replays_bounded_cleanup(self) -> None:
        case = self.cases["terminal-cleanup-replay"]
        self.assertEqual(case["expected_role"], "maintenance")
        self.assertEqual(case["expected_operation"], "replay-finalization-cleanup")
        self.assertEqual(case["mechanism"], "agent-bounded-filesystem-cleanup")
        self.assertFalse(case["journal_rewrite"])
        self.assertFalse(case["ordinary_routing"])
        self.assertEqual(case["cleanup"], "exact-transaction-id-directory-and-empty-container")

        instructions = (ROLE_ROOT / "instructions.md").read_text()
        routing = ROUTING.read_text()
        protocol = UPGRADE_PROTOCOL.read_text()
        for text in (instructions, routing, protocol):
            self.assertIn("interrupted terminal cleanup", text.lower())
            self.assertIn("non-recursive empty-directory operation", text)
        self.assertIn("`./.ava/state/transactions/` is absent", routing)
        self.assertIn("no `/.ava/state/transactions/` container", protocol)

    def test_terminal_cleanup_replay_covers_recorded_and_restored_source_states(self) -> None:
        rolled_back = self.cases["rolled-back-cleanup-replay"]
        self.assertEqual(rolled_back["cleanup_authority"], "journal-transaction-id")
        self.assertFalse(rolled_back["journal_rewrite"])

        idle = self.cases["idle-cleanup-replay"]
        self.assertEqual(idle["cleanup_authority"], "proven-restored-source")
        self.assertEqual(idle["state"]["transaction_container_entries"], 1)
        self.assertEqual(idle["state"]["source_manifest_backup"], "matches-live")
        self.assertEqual(idle["state"]["source_journal_backup"], "matches-live")
        self.assertEqual(idle["state"]["managed_payload"], "matches-source")
        self.assertFalse(idle["journal_rewrite"])

        prior_terminal = self.cases["prior-terminal-cleanup-replay"]
        self.assertEqual(prior_terminal["state"]["journal_status"], "complete")
        self.assertNotEqual(
            prior_terminal["state"]["transaction_id"],
            prior_terminal["state"]["residual_transaction_id"],
        )
        self.assertEqual(prior_terminal["cleanup_authority"], "proven-restored-source")
        self.assertEqual(prior_terminal["state"]["source_journal_backup"], "matches-live")
        self.assertFalse(prior_terminal["journal_rewrite"])

        ambiguous = self.cases["idle-ambiguous-cleanup"]
        self.assertEqual(ambiguous["expected_outcome"], "report-managed-state-conflict")
        self.assertFalse(ambiguous["automatic_delete"])

        instructions = (ROLE_ROOT / "instructions.md").read_text()
        capabilities = (ROLE_ROOT / "capabilities.md").read_text()
        routing = ROUTING.read_text()
        protocol = UPGRADE_PROTOCOL.read_text()
        for text in (instructions, capabilities, routing, protocol):
            self.assertIn("source manifest backup", text)
            self.assertIn("source journal backup", text)
        self.assertIn(
            "live valid `idle`, `complete`, `aborted`, or `rolled-back` journal",
            instructions,
        )
        self.assertIn("More than one direct entry", instructions)

    def test_uninstall_removes_only_managed_roots(self) -> None:
        case = self.cases["uninstall-healthy"]
        self.assertEqual(case["removed"], ["./.ava/", "./AGENTS.md"])
        self.assertTrue(
            {
                "./roles/",
                "./workflows/",
                "./shared/",
                "./knowledge/",
                "./inbox/",
                "./index.md",
                "./log.md",
            }.issubset(case["preserved"])
        )

    def test_uninstall_refuses_active_or_uncertain_state(self) -> None:
        for case_id in (
            "uninstall-active-deterministic",
            "uninstall-active-semantic",
            "uninstall-modified-router",
            "uninstall-modified-managed-directory",
        ):
            self.assertTrue(self.cases[case_id]["expected_outcome"].startswith("refuse"), case_id)

    def test_project_owned_host_entrypoints_are_preserved(self) -> None:
        case = self.cases["uninstall-stale-host-entrypoint"]
        self.assertIn("./CODEX.md", case["preserved"])
        self.assertFalse(case["automatic_host_edit"])
        self.assertIn("stale-reference", case["expected_outcome"])

    def test_opencode_access_and_missing_permission_are_distinct(self) -> None:
        self.assertEqual(
            self.cases["opencode-accessible"]["expected_outcome"],
            "managed-context-readable",
        )
        missing = self.cases["opencode-permission-missing"]
        self.assertEqual(missing["expected_outcome"], "report-minimal-merge")
        self.assertFalse(missing["automatic_project_config_edit"])

    def test_router_and_catalog_define_distinct_role_ownership(self) -> None:
        router = ROUTER.read_text()
        routing = ROUTING.read_text()
        catalog = ROLE_CATALOG.read_text()
        upgrade = UPGRADE_ROLE.read_text()
        for text in (router, routing, catalog):
            self.assertIn("Ava Maintenance", text)
            self.assertIn("Upgrade Role", text)
        self.assertIn("deterministic", routing)
        self.assertIn("semantic reconciliation", routing)
        self.assertIn("Do not activate it for installation status", upgrade)

    def test_role_does_not_add_command_surface_or_load_internal_role(self) -> None:
        instructions = (ROLE_ROOT / "instructions.md").read_text()
        constraints = (ROLE_ROOT / "constraints.md").read_text()
        combined = instructions + constraints
        self.assertIn(
            "Do not add or require standalone status, version, repair, finalization, or uninstall command modes",
            instructions,
        )
        self.assertNotIn("/internal/roles/ava-internal", combined)
        self.assertIn("must never load", constraints)


if __name__ == "__main__":
    unittest.main()
