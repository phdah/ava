from __future__ import annotations

import json
import unittest
from pathlib import Path

from internal.release.assemble import read_payloads

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/inbox-scoped-history.json"
SCOPED_HISTORY = SOURCE_ROOT / "templates/base/shared/instructions/scoped-history.md"


def assert_prior_entries_preserved(before: list[str], after: list[str]) -> None:
    cursor = 0
    for entry in before:
        try:
            position = after.index(entry, cursor)
        except ValueError as error:
            raise AssertionError(f"pre-existing history entry changed or disappeared: {entry}") from error
        cursor = position + 1


class InboxScopedHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}
        cls.payloads = {item.destination: item.data.decode("utf-8") for item in read_payloads(SOURCE_ROOT)}

    def test_fixture_covers_routine_qualifying_and_cleanup_cases(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 1)
        self.assertEqual(
            set(self.cases),
            {
                "routine-ingestion-does-not-touch-history",
                "qualifying-ingestion-adds-one-entry-and-preserves-prior-history",
                "history-cleanup-requires-prerequisite-handoff",
            },
        )

    def test_assembled_inbox_role_has_additive_only_history_authority(self) -> None:
        index = self.payloads["/.ava/base/roles/inbox-ingester/index.md"]
        instructions = self.payloads["/.ava/base/roles/inbox-ingester/instructions.md"]
        capabilities = self.payloads["/.ava/base/roles/inbox-ingester/capabilities.md"]
        constraints = self.payloads["/.ava/base/roles/inbox-ingester/constraints.md"]

        self.assertIn("[Scoped history](../../shared/instructions/scoped-history.md)", index)
        self.assertIn("additive-only authority", instructions)
        self.assertIn("preserve every pre-existing entry verbatim", instructions)
        self.assertIn("at most one new entry", capabilities)
        self.assertIn("delete, rewrite, consolidate, correct", constraints)
        self.assertIn("keep the source pending", constraints)

    def test_assembled_reviewer_checks_history_preservation(self) -> None:
        reviewer = self.payloads["/.ava/base/roles/change-reviewer/index.md"]
        self.assertIn("[Scoped history](../../shared/instructions/scoped-history.md)", reviewer)
        self.assertIn("every pre-existing history entry remains verbatim", reviewer)
        self.assertIn("separately authorized Project Steward or fixture-preparation operation", reviewer)

    def test_shared_history_threshold_remains_authoritative(self) -> None:
        scoped_history = SCOPED_HISTORY.read_text()
        self.assertIn("conceptually or structurally significant", scoped_history)
        self.assertIn("routine additions", scoped_history)
        self.assertIn("nearest relevant `log.md`", scoped_history)

    def test_routine_ingestion_leaves_log_unchanged(self) -> None:
        case = self.cases["routine-ingestion-does-not-touch-history"]
        self.assertFalse(case["crosses_history_threshold"])
        self.assertEqual(case["expected_after_entries"], case["before_entries"])
        self.assertEqual(case["expected_added_entries"], [])
        assert_prior_entries_preserved(case["before_entries"], case["expected_after_entries"])

    def test_qualifying_ingestion_adds_exactly_one_entry(self) -> None:
        case = self.cases["qualifying-ingestion-adds-one-entry-and-preserves-prior-history"]
        self.assertTrue(case["crosses_history_threshold"])
        self.assertEqual(len(case["expected_added_entries"]), 1)
        self.assertEqual(
            len(case["expected_after_entries"]),
            len(case["before_entries"]) + 1,
        )
        assert_prior_entries_preserved(case["before_entries"], case["expected_after_entries"])
        self.assertNotIn(case["nearest_log"], case["forbidden_duplicate_logs"])

    def test_regression_rejects_deleted_or_rewritten_prior_entries(self) -> None:
        before = ["old entry one", "old entry two"]
        with self.assertRaises(AssertionError):
            assert_prior_entries_preserved(before, ["old entry one"])
        with self.assertRaises(AssertionError):
            assert_prior_entries_preserved(before, ["old entry one", "rewritten entry two"])

    def test_cleanup_case_stays_pending_without_log_mutation(self) -> None:
        case = self.cases["history-cleanup-requires-prerequisite-handoff"]
        self.assertFalse(case["source_may_move"])
        self.assertEqual(case["expected_action"], "leave-source-pending-and-handoff")
        self.assertEqual(case["required_handoff"], "project-steward-or-fixture-preparation")
        self.assertEqual(case["expected_after_entries"], case["before_entries"])
        assert_prior_entries_preserved(case["before_entries"], case["expected_after_entries"])


if __name__ == "__main__":
    unittest.main()
