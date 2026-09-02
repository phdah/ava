from __future__ import annotations

import inspect
import unittest

from internal.release import qualification_host as host
from internal.release import qualification_host_automation as host_automation
from internal.release import qualification_host_runner as host_runner
from internal.release import qualification_runner


class QualificationHostTests(unittest.TestCase):
    def test_local_host_satisfies_full_matrix_and_chatgpt_github_does_not(self) -> None:
        matrix = qualification_runner.load_matrix()
        local = host.assess_host(host.local_host_profile(), matrix)
        chatgpt = host.assess_host(host.chatgpt_github_profile(), matrix)

        self.assertTrue(local.complete)
        self.assertEqual(local.global_missing, ())
        self.assertFalse(chatgpt.complete)
        self.assertEqual(
            set(chatgpt.global_missing),
            {host.CAP_EXTERNAL_EVIDENCE_READ, host.CAP_INDEPENDENT_AUDIT},
        )
        self.assertEqual(set(chatgpt.scenario_missing), {item["id"] for item in matrix["scenarios"]})
        for missing in chatgpt.scenario_missing.values():
            self.assertIn(host.CAP_LOCAL_PROCESS, missing)
            self.assertIn(host.CAP_MUTABLE_EXTERNAL_WORKSPACE, missing)
            self.assertIn(host.CAP_LOCAL_RELEASE_ASSETS, missing)

    def test_opencode_inventory_is_normalized_without_session_ids(self) -> None:
        raw = {
            "schema_version": 1,
            "sessions": [
                {
                    "session_id": "ses_root123",
                    "parent_session_id": None,
                    "scenario": "registered-private-routing",
                    "prompt_sha256": "1" * 64,
                    "model": "openai/gpt-5.6-sol",
                    "project_root": "/tmp/run/scenarios/registered-private-routing/project",
                    "transcript_sha256": "2" * 64,
                    "terminal_state": "completed",
                },
                {
                    "session_id": "ses_child456",
                    "parent_session_id": "ses_root123",
                    "scenario": "registered-private-routing",
                    "prompt_sha256": "3" * 64,
                    "model": "openai/gpt-5.6-sol",
                    "project_root": "/tmp/run/scenarios/registered-private-routing/project",
                    "transcript_sha256": "4" * 64,
                    "terminal_state": "completed",
                },
            ],
        }
        transcript_paths = {
            "ses_root123": "/tmp/evidence/int_root.json",
            "ses_child456": "/tmp/evidence/int_child.json",
        }

        inventory = host.normalize_opencode_inventory(raw, transcript_paths)
        host.validate_interaction_inventory(inventory)
        serialized = host.canonical_json(inventory)

        self.assertEqual(inventory["host_adapter"], "opencode")
        self.assertEqual(len(inventory["interactions"]), 2)
        self.assertNotIn("ses_root123", serialized)
        self.assertNotIn("ses_child456", serialized)
        self.assertNotIn("session_id", serialized)
        root = next(
            item
            for item in inventory["interactions"]
            if item["prompt_sha256"] == "1" * 64
        )
        child = next(
            item
            for item in inventory["interactions"]
            if item["prompt_sha256"] == "3" * 64
        )
        self.assertIsNone(root["parent_interaction_id"])
        self.assertEqual(child["parent_interaction_id"], root["interaction_id"])
        self.assertEqual(root["transcript_path"], transcript_paths["ses_root123"])
        self.assertEqual(child["transcript_path"], transcript_paths["ses_child456"])

    def test_host_neutral_runner_injects_interaction_command(self) -> None:
        source = inspect.getsource(host_runner.HostNeutralRunner.opencode_prompt)
        self.assertIn("self.agent_host.interaction_command", source)
        self.assertNotIn('"opencode"', source)
        self.assertIn('label="agent host prompt"', source)

    def test_host_neutral_audit_prompt_rejects_host_specific_evidence_requirements(self) -> None:
        source = inspect.getsource(host_automation.build_audit_prompt)
        self.assertIn("interaction_inventory", source)
        self.assertIn("Do not require host-specific session IDs", source)
        self.assertNotIn("session_inventory_path", source)

    def test_active_shell_entrypoint_routes_through_host_automation(self) -> None:
        release_root = host.REPOSITORY_ROOT / "internal/release"
        source = (release_root / "qualify-release.sh").read_text(encoding="utf-8")
        self.assertIn("qualification_host_automation.py", source)
        self.assertIn("--host-kind opencode", source)
        self.assertIn("qualification-opencode.sh", source)
        self.assertNotIn("qualification_phase_automation.py", source)

    def test_host_evidence_schemas_do_not_require_opencode_state(self) -> None:
        schema_root = host.REPOSITORY_ROOT / "internal/release/qualification/schemas"
        for name in (
            "interaction-inventory.schema.json",
            "host-run-record.schema.json",
            "host-edge-independent-run.schema.json",
        ):
            text = (schema_root / name).read_text(encoding="utf-8")
            self.assertNotIn("session_inventory_file", text)
            self.assertNotIn("opencode_version", text)

    def test_chatgpt_profile_documents_connector_execution_boundary(self) -> None:
        profile = host.chatgpt_github_profile()
        self.assertIn("GitHub connector", profile.description)
        self.assertNotIn(host.CAP_LOCAL_PROCESS, profile.capabilities)
        self.assertNotIn(host.CAP_MUTABLE_EXTERNAL_WORKSPACE, profile.capabilities)
        self.assertNotIn(host.CAP_LOCAL_RELEASE_ASSETS, profile.capabilities)
        self.assertNotIn(host.CAP_EXTERNAL_EVIDENCE_READ, profile.capabilities)


if __name__ == "__main__":
    unittest.main()
