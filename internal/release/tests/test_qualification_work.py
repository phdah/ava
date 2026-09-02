from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_runner
from internal.release import qualification_work as work


class QualificationWorkTests(unittest.TestCase):
    def test_matrix_modes_preserve_all_scenarios(self) -> None:
        matrix = qualification_runner.load_matrix()
        modes = {scenario["id"]: work.scenario_mode(scenario) for scenario in matrix["scenarios"]}
        self.assertEqual(len(modes), 17)
        self.assertEqual(
            {scenario_id for scenario_id, mode in modes.items() if mode == "subagent"},
            {
                "registered-private-routing",
                "registered-work-routing",
                "registered-calendar-regression",
                "registered-ambiguous-routing",
                "complete-pending-inbox",
                "interrupted-finalize",
                "pending-semantic-reconciliation",
                "uninstall-reinstall",
            },
        )
        self.assertEqual(
            {scenario_id for scenario_id, mode in modes.items() if mode == "deterministic"},
            set(modes) - {scenario_id for scenario_id, mode in modes.items() if mode == "subagent"},
        )

    def test_subagent_response_is_bound_to_baseline_and_forbids_external_tools(self) -> None:
        prompt = "Persist qualification context."
        baseline = {
            "AGENTS.md": hashlib.sha256(b"router\n").hexdigest(),
            ".ava/base/roles/example/index.md": hashlib.sha256(b"role\n").hexdigest(),
        }
        request = {
            "interaction_id": "work-001-scenario-route",
            "scenario": "scenario",
            "stage": "route",
            "prompt_sha256": work.automation.sha256_text(prompt),
            "model": "openai/gpt-5.6-sol",
            "workspace_root": "/tmp/work/project",
            "baseline_files": baseline,
        }
        response = {
            "schema_version": 1,
            "interaction_id": request["interaction_id"],
            "scenario": request["scenario"],
            "stage": request["stage"],
            "prompt_sha256": request["prompt_sha256"],
            "model": request["model"],
            "workspace_root": request["workspace_root"],
            "final_response": "Active role: Example\nDone.",
            "required_reading": [
                {"order": 1, "path": "AGENTS.md", "sha256": baseline["AGENTS.md"]},
                {
                    "order": 2,
                    "path": ".ava/base/roles/example/index.md",
                    "sha256": baseline[".ava/base/roles/example/index.md"],
                },
            ],
            "external_tools_used": [],
        }
        work.validate_response(request, response)

        contaminated = dict(response)
        contaminated["external_tools_used"] = ["github"]
        with self.assertRaisesRegex(work.WorkQualificationError, "external tools"):
            work.validate_response(request, contaminated)

        wrong_digest = json.loads(json.dumps(response))
        wrong_digest["required_reading"][0]["sha256"] = "0" * 64
        with self.assertRaisesRegex(work.WorkQualificationError, "pre-interaction workspace"):
            work.validate_response(request, wrong_digest)

    def test_required_reading_starts_with_root_router(self) -> None:
        digest = "1" * 64
        request = {
            "interaction_id": "work-001-scenario-route",
            "scenario": "scenario",
            "stage": "route",
            "prompt_sha256": "2" * 64,
            "model": "openai/gpt-5.6-sol",
            "workspace_root": "/tmp/work/project",
            "baseline_files": {"AGENTS.md": digest, "index.md": digest},
        }
        response = {
            "schema_version": 1,
            "interaction_id": request["interaction_id"],
            "scenario": request["scenario"],
            "stage": request["stage"],
            "prompt_sha256": request["prompt_sha256"],
            "model": request["model"],
            "workspace_root": request["workspace_root"],
            "final_response": "Need clarification.",
            "required_reading": [{"order": 1, "path": "index.md", "sha256": digest}],
            "external_tools_used": [],
        }
        with self.assertRaisesRegex(work.WorkQualificationError, "AGENTS.md first"):
            work.validate_response(request, response)

    def test_canonical_entrypoint_has_no_agent_runtime(self) -> None:
        release_root = work.REPOSITORY_ROOT / "internal/release"
        shell = (release_root / "qualify-release.sh").read_text(encoding="utf-8")
        self.assertIn("qualification_work.py", shell)
        self.assertNotIn("opencode", shell.lower())
        self.assertNotIn("qualification_phase_automation.py", shell)
        self.assertNotIn("qualification_host_automation.py", shell)

    def test_work_procedure_forbids_local_fallback(self) -> None:
        text = (work.REPOSITORY_ROOT / "internal/release/qualification-work.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("ChatGPT Work Cloud", text)
        self.assertIn("fresh Work subagent", text)
        self.assertIn("No local fallback", text)
        self.assertIn("Do not fall back to OpenCode", text)

    def test_work_run_schemas_have_no_opencode_or_session_contract(self) -> None:
        schema_root = work.REPOSITORY_ROOT / "internal/release/qualification/schemas"
        for name in ("work-run-record.schema.json", "work-edge-independent-run.schema.json"):
            text = (schema_root / name).read_text(encoding="utf-8")
            self.assertIn("chatgpt-work-cloud", text)
            self.assertNotIn("opencode", text.lower())
            self.assertNotIn("session_inventory", text)

    def test_rejected_local_host_modules_are_absent(self) -> None:
        release_root = work.REPOSITORY_ROOT / "internal/release"
        for name in (
            "qualification_host.py",
            "qualification_host_runner.py",
            "qualification_host_automation.py",
        ):
            self.assertFalse((release_root / name).exists(), name)

    def test_summary_is_durable_work_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            state = {
                "phase": "edge-independent",
                "run_id": "run",
                "source": {"version": "1", "tag": "v1", "source_revision": "1" * 40},
                "target": {"version": "2", "tag": "v2", "source_revision": "2" * 40},
                "execution_root": str(root),
                "scenario_order": ["one"],
                "scenarios": {
                    "one": {"outcome": "pass", "detail": None},
                },
                "integrity_outcomes": [],
            }
            summary = work.write_summary(state)
            self.assertEqual(summary["qualification_host"], work.WORK_HOST)
            self.assertEqual(summary["exit_status"], 0)
            self.assertTrue((root / work.SUMMARY_NAME).is_file())


if __name__ == "__main__":
    unittest.main()
