from __future__ import annotations

import json
import re
import unittest
from datetime import datetime
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/document-update-metadata.json"


class DocumentUpdateMetadataFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}

    def test_required_scenarios_are_present(self) -> None:
        self.assertTrue(
            {
                "creation",
                "meaningful-mutation",
                "trivial-mutation",
                "repeated-mutation",
                "legacy-timestamp",
                "reserved-index",
            }.issubset(self.cases)
        )

    def test_actor_identifiers_follow_the_contract(self) -> None:
        pattern = re.compile(self.fixture["actor_pattern"])
        for case in self.cases.values():
            for state_name in ("before", "after"):
                state = case[state_name]
                if not isinstance(state, dict):
                    continue
                for field in ("generated", "updated"):
                    value = state.get(field)
                    if isinstance(value, dict):
                        self.assertRegex(value["by"], pattern, case["id"])
                for value in state.get("verified", []):
                    self.assertRegex(value["by"], pattern, case["id"])

    def test_creation_uses_generated_without_updated(self) -> None:
        after = self.cases["creation"]["after"]
        self.assertIn("generated", after)
        self.assertNotIn("updated", after)

    def test_meaningful_mutation_preserves_creation_provenance(self) -> None:
        case = self.cases["meaningful-mutation"]
        self.assertEqual(case["before"]["generated"], case["after"]["generated"])
        self.assertIn("updated", case["after"])

    def test_trivial_mutation_does_not_churn_updated(self) -> None:
        case = self.cases["trivial-mutation"]
        self.assertEqual(case["before"]["updated"], case["after"]["updated"])

    def test_repeated_mutation_replaces_latest_update(self) -> None:
        case = self.cases["repeated-mutation"]
        before = datetime.fromisoformat(case["before"]["updated"]["at"])
        after = datetime.fromisoformat(case["after"]["updated"]["at"])
        self.assertGreater(after, before)

    def test_legacy_timestamp_is_not_reinterpreted(self) -> None:
        case = self.cases["legacy-timestamp"]
        self.assertEqual(case["before"]["timestamp"], case["after"]["timestamp"])
        self.assertIn("updated", case["after"])

    def test_reserved_documents_do_not_gain_update_frontmatter(self) -> None:
        case = self.cases["reserved-index"]
        self.assertIsNone(case["before"])
        self.assertIsNone(case["after"])

    def test_invalid_cases_freeze_stable_rule_ids(self) -> None:
        expected = {
            "malformed-updated": "AVA-META-UPDATE-SHAPE",
            "regressive-updated": "AVA-META-UPDATE-REGRESSION",
            "stale-verification": "AVA-META-VERIFICATION-STALE",
        }
        for case_id, rule in expected.items():
            diagnostics = self.cases[case_id]["expected_diagnostics"]
            self.assertIn({"rule": rule, "severity": "error"}, diagnostics)


if __name__ == "__main__":
    unittest.main()
