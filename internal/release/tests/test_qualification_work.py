from __future__ import annotations

import json
import unittest
from pathlib import Path

from internal.release import qualification_runner
from internal.release import qualification_work as implementation


class QualificationExecutionTests(unittest.TestCase):
    def test_release_gate_selects_only_deterministic_scenarios(self) -> None:
        matrix = qualification_runner.load_matrix()
        pre = implementation.deterministic_scenarios(matrix, "pre-edge")
        final = implementation.deterministic_scenarios(matrix, "final")

        self.assertEqual(
            [scenario["id"] for scenario in pre],
            [
                "fresh-empty-install",
                "mature-project-install",
                "managed-modified",
                "managed-missing",
                "managed-corrupt",
                "managed-unexpected",
            ],
        )
        self.assertEqual(
            [scenario["id"] for scenario in final],
            [
                "fresh-empty-install",
                "mature-project-install",
                "managed-modified",
                "managed-missing",
                "managed-corrupt",
                "managed-unexpected",
                "interrupted-resume",
                "interrupted-abort",
                "interrupted-rollback",
            ],
        )
        self.assertTrue(
            all(
                scenario["kind"] not in implementation.AGENT_KINDS
                for scenario in pre + final
            )
        )

    def test_behavioral_scenarios_remain_outside_release_gate(self) -> None:
        matrix = qualification_runner.load_matrix()
        behavioral = {
            scenario["id"]
            for scenario in matrix["scenarios"]
            if scenario["kind"] in implementation.AGENT_KINDS
        }
        selected = {
            scenario["id"]
            for stage in implementation.STAGES
            for scenario in implementation.deterministic_scenarios(matrix, stage)
        }
        self.assertTrue(
            {
                "registered-private-routing",
                "registered-work-routing",
                "registered-calendar-regression",
                "registered-ambiguous-routing",
                "complete-pending-inbox",
                "interrupted-finalize",
                "pending-semantic-reconciliation",
                "uninstall-reinstall",
            }.issubset(behavioral)
        )
        self.assertTrue(behavioral.isdisjoint(selected))

    def test_final_edge_accepts_semantic_or_mechanical_targets(self) -> None:
        source = qualification_runner.ReleaseIdentity(
            Path("/source"),
            "1.0.0-alpha.16",
            "v1.0.0-alpha.16",
            "1" * 40,
            False,
            {"upgrade_paths": {"edges": []}},
        )
        for semantic_review_required in (False, True):
            target = qualification_runner.ReleaseIdentity(
                Path("/target"),
                "1.0.0-alpha.17",
                "v1.0.0-alpha.17",
                "2" * 40,
                semantic_review_required,
                {
                    "upgrade_paths": {
                        "edges": [
                            {
                                "from": source.version,
                                "to": "1.0.0-alpha.17",
                            }
                        ]
                    }
                },
            )
            implementation.validate_final_edge(source, target)

    def test_canonical_entrypoint_selects_no_chatgpt_mode(self) -> None:
        release_root = implementation.REPOSITORY_ROOT / "internal/release"
        shell = (release_root / "qualify-release.sh").read_text(encoding="utf-8")
        driver = (release_root / "qualification.py").read_text(encoding="utf-8")
        self.assertIn("qualification.py", shell)
        self.assertNotIn("qualification_work.py", shell)
        self.assertNotIn("opencode", shell.lower())
        self.assertNotIn("subagent", shell.lower())
        self.assertIn("AVA_QUALIFICATION_EXECUTOR", driver)
        self.assertIn("ordinary ChatGPT chat", driver)

    def test_final_evidence_schema_is_executor_neutral(self) -> None:
        schema_path = (
            implementation.REPOSITORY_ROOT
            / "internal/release/qualification/schemas/work-run-record.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fields = set(schema["properties"])
        self.assertIn("qualification_mode", fields)
        self.assertIn("qualification_host", fields)
        self.assertNotIn("const", schema["properties"]["qualification_host"])
        self.assertNotIn("qualification_model", fields)
        self.assertNotIn("audit_model", fields)
        self.assertNotIn("audit_report_file", fields)
        self.assertNotIn("interaction_evidence_file", fields)
        self.assertNotIn("work_protocol_version", fields)

    def test_execution_procedure_is_session_neutral(self) -> None:
        root = implementation.REPOSITORY_ROOT
        text = (root / "internal/release/qualification-execution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("session-neutral", text.lower())
        self.assertIn("zero delegated qualification agents", text.lower())
        self.assertIn("ordinary ChatGPT chat", text)
        self.assertIn("There is no requirement to switch from normal Chat to Work", text)
        self.assertIn("GitHub Actions", text)

    def test_github_actions_owns_mandatory_execution(self) -> None:
        root = implementation.REPOSITORY_ROOT
        procedure = (root / "internal/release/procedure.md").read_text(encoding="utf-8")
        qualification_workflow = (
            root / ".github/workflows/release-qualification.yml"
        ).read_text(encoding="utf-8")
        python_workflow = (root / ".github/workflows/python-tests.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("internal/release/test.sh", python_workflow)
        self.assertIn("session-neutral", procedure.lower())
        self.assertIn("GitHub Actions", procedure)
        self.assertIn("run-release-qualification.sh", qualification_workflow)
        self.assertIn("acceptance-request.json", qualification_workflow)
        self.assertIn("AVA_QUALIFICATION_EXECUTOR", qualification_workflow)


if __name__ == "__main__":
    unittest.main()
