from __future__ import annotations

import json
import unittest
from pathlib import Path

from internal.release import qualification_runner
from internal.release import qualification_work as work


class QualificationWorkTests(unittest.TestCase):
    def test_release_gate_selects_only_deterministic_scenarios(self) -> None:
        matrix = qualification_runner.load_matrix()
        pre = work.deterministic_scenarios(matrix, "pre-edge")
        final = work.deterministic_scenarios(matrix, "final")

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
            all(scenario["kind"] not in work.AGENT_KINDS for scenario in pre + final)
        )

    def test_behavioral_scenarios_remain_outside_release_gate(self) -> None:
        matrix = qualification_runner.load_matrix()
        behavioral = {
            scenario["id"]
            for scenario in matrix["scenarios"]
            if scenario["kind"] in work.AGENT_KINDS
        }
        selected = {
            scenario["id"]
            for stage in work.STAGES
            for scenario in work.deterministic_scenarios(matrix, stage)
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
            work.validate_final_edge(source, target)

    def test_canonical_entrypoint_has_no_agent_runtime(self) -> None:
        release_root = work.REPOSITORY_ROOT / "internal/release"
        shell = (release_root / "qualify-release.sh").read_text(encoding="utf-8")
        self.assertIn("qualification_work.py", shell)
        self.assertNotIn("opencode", shell.lower())
        self.assertNotIn("subagent", shell.lower())

    def test_final_evidence_schema_has_no_agent_or_audit_contract(self) -> None:
        schema_path = (
            work.REPOSITORY_ROOT
            / "internal/release/qualification/schemas/work-run-record.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fields = set(schema["properties"])
        self.assertIn("qualification_mode", fields)
        self.assertNotIn("qualification_model", fields)
        self.assertNotIn("audit_model", fields)
        self.assertNotIn("audit_report_file", fields)
        self.assertNotIn("interaction_evidence_file", fields)
        self.assertNotIn("work_protocol_version", fields)

    def test_work_procedure_requires_zero_delegated_qualification_agents(self) -> None:
        text = (
            work.REPOSITORY_ROOT / "internal/release/qualification-work.md"
        ).read_text(encoding="utf-8")
        self.assertIn("zero delegated qualification agents", text.lower())
        self.assertIn("optional behavioral QA", text)
        self.assertIn("pre-edge", text)
        self.assertIn("final", text)

    def test_github_actions_owns_repository_test_suite(self) -> None:
        root = work.REPOSITORY_ROOT
        procedure = (root / "internal/release/procedure.md").read_text(encoding="utf-8")
        work_procedure = (root / "internal/release/qualification-work.md").read_text(
            encoding="utf-8"
        )
        workflow = (root / ".github/workflows/python-tests.yml").read_text(encoding="utf-8")
        self.assertIn("internal/release/test.sh", workflow)
        self.assertIn("GitHub Actions boundary", procedure)
        self.assertIn("does not need to rerun", procedure)
        self.assertIn("GitHub Actions boundary", work_procedure)
        self.assertIn("does not duplicate", work_procedure)


if __name__ == "__main__":
    unittest.main()
