from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_runner as runner


class QualificationSemanticStatusTests(unittest.TestCase):
    def test_complete_inbox_requires_semantic_audit(self) -> None:
        matrix = runner.load_matrix()
        inbox = next(
            scenario
            for scenario in matrix["scenarios"]
            if scenario["id"] == "complete-pending-inbox"
        )
        self.assertIs(inbox["semantic_audit_required"], True)

    def test_structural_pass_is_runner_success_but_not_semantic_pass(self) -> None:
        outcomes = [
            {"outcome": "pass"},
            {"outcome": "structural-pass", "semantic_status": "pending-audit"},
        ]
        self.assertEqual(runner.summary_exit_status(outcomes), 0)
        self.assertEqual(outcomes[1]["semantic_status"], "pending-audit")

    def test_nonpassing_outcome_still_blocks_runner(self) -> None:
        for outcome in ("fail", "skipped", "user-decision-required"):
            outcomes = [{"outcome": "pass"}, {"outcome": outcome}]
            self.assertEqual(runner.summary_exit_status(outcomes), 1)

    def test_structural_pass_workspace_is_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            qualification = root / "qualification"
            source = qualification / "variants/complete-pending-inbox/project"
            source.mkdir(parents=True)
            (source / "baseline.txt").write_text("clean\n", encoding="utf-8")
            execution = root / "execution"
            runner.initialize_execution_root(execution, qualification)
            scenario = {
                "id": "complete-pending-inbox",
                "source": "variants/complete-pending-inbox",
            }
            state = {
                "schema_version": 1,
                "scenarios": {
                    "complete-pending-inbox": {
                        "outcome": "structural-pass",
                        "semantic_status": "pending-audit",
                    }
                },
            }
            workspace = execution / "scenarios/complete-pending-inbox"
            (workspace / "project").mkdir(parents=True)
            (workspace / "project/evidence.txt").write_text("retained\n", encoding="utf-8")

            retained, already_passed = runner.scenario_workspace(
                execution,
                qualification,
                scenario,
                state,
            )

            self.assertTrue(already_passed)
            self.assertEqual(
                (retained / "project/evidence.txt").read_text(encoding="utf-8"),
                "retained\n",
            )


if __name__ == "__main__":
    unittest.main()
