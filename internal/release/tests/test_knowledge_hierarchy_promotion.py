from __future__ import annotations

import json
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/knowledge-hierarchy-promotion.json"
KNOWLEDGE = SOURCE_ROOT / "templates/base/shared/instructions/knowledge-organization.md"
INBOX = SOURCE_ROOT / "templates/base/roles/inbox-ingester/instructions.md"
STEWARD = SOURCE_ROOT / "templates/base/roles/project-steward/instructions.md"
REVIEWER = SOURCE_ROOT / "templates/base/roles/change-reviewer/instructions.md"


class KnowledgeHierarchyPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}
        cls.knowledge = KNOWLEDGE.read_text()
        cls.inbox = INBOX.read_text()
        cls.steward = STEWARD.read_text()
        cls.reviewer = REVIEWER.read_text()

    def test_fixture_covers_required_semantic_decisions(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 1)
        self.assertIsNone(self.fixture["numeric_split_threshold"])
        self.assertEqual(
            set(self.cases),
            {
                "durable-subject-remains-concept",
                "stable-index-group-promotes-to-collection",
                "temporary-heading-remains-heading",
                "cross-cutting-relationship-uses-link",
                "ambiguous-promotion-requires-steward-handoff",
            },
        )
        for case in self.cases.values():
            self.assertTrue(case["existing_branch"], case["id"])
            self.assertTrue(case["existing_shape"], case["id"])
            self.assertTrue(case["incoming_material"], case["id"])
            self.assertTrue(case["expected_action"], case["id"])
            self.assertTrue(case["review_checks"], case["id"])

    def test_shared_contract_distinguishes_concepts_and_collections(self) -> None:
        self.assertIn("# Concepts and collections", self.knowledge)
        self.assertIn("# Semantic hierarchy promotion", self.knowledge)
        self.assertIn("durable subject", self.knowledge)
        self.assertIn("Ava defines no numeric split threshold", self.knowledge)
        self.assertIn(
            "Move the affected canonical concepts into that collection before adding another sibling",
            self.knowledge,
        )
        self.assertIn("lists direct children only", self.knowledge)

    def test_inbox_ingester_blocks_flat_growth_and_hands_off(self) -> None:
        self.assertIn("# Durable subject classification", self.inbox)
        self.assertIn("# Hierarchy promotion gate", self.inbox)
        self.assertIn(
            "Inspect the target branch's current direct children and stable index headings before adding another sibling",
            self.inbox,
        )
        self.assertIn("Do not use document counts as the promotion rule", self.inbox)
        self.assertIn("must not move or broadly reorganize existing trusted concepts", self.inbox)
        self.assertIn("leave the source pending and request the project steward", self.inbox.lower())

    def test_project_steward_owns_broader_reorganization(self) -> None:
        self.assertIn("# Knowledge hierarchy maintenance", self.steward)
        self.assertIn("Promote a reusable class into a child collection before further flat growth", self.steward)
        self.assertIn("Preserve unknown metadata, OKF source provenance", self.steward)
        self.assertIn("Do not use file counts as a split threshold", self.steward)

    def test_change_reviewer_has_independent_semantic_checks(self) -> None:
        self.assertIn("## Knowledge hierarchy review", self.reviewer)
        self.assertIn("canonical concepts follow durable subject identity", self.reviewer)
        self.assertIn("promotion was not based on a numeric file-count threshold", self.reviewer)
        self.assertIn("parent and child indexes preserve direct-child navigation", self.reviewer)
        self.assertIn("identify the Project Steward", self.reviewer)

    def test_observed_mixed_branch_requires_steward_promotion(self) -> None:
        case = self.cases["stable-index-group-promotes-to-collection"]
        self.assertEqual(case["expected_action"], "request-promotion-before-ingestion")
        self.assertEqual(case["required_follow_up"], "Project Steward")
        self.assertEqual(case["expected_collection"], "knowledge/work/integrations/")
        self.assertTrue(
            any("Project Steward" in check for check in case["review_checks"]),
            case,
        )

    def test_ambiguous_taxonomy_remains_project_owned(self) -> None:
        case = self.cases["ambiguous-promotion-requires-steward-handoff"]
        self.assertEqual(case["expected_action"], "leave-source-pending")
        self.assertEqual(case["required_follow_up"], "Project Steward")


if __name__ == "__main__":
    unittest.main()
