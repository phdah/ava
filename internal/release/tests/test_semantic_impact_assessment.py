from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FIXTURE_PATH = ROOT / "internal/release/fixtures/semantic-impact-assessment.json"
PROCEDURE_PATH = ROOT / "internal/release/procedure.md"
AUTOMATION_PATH = ROOT / "internal/release/release-please.md"
MAINTAINER_PATH = ROOT / "internal/roles/ava-internal/instructions.md"


class SemanticImpactAssessmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE_PATH.read_text())
        cls.procedure = PROCEDURE_PATH.read_text()
        cls.automation = AUTOMATION_PATH.read_text()
        cls.maintainer = MAINTAINER_PATH.read_text()

    def test_regression_cases_cover_true_and_false_decisions(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 1)
        cases = self.fixture["cases"]
        self.assertGreaterEqual(len(cases), 2)
        self.assertEqual(
            {case["semantic_review_required"] for case in cases},
            {False, True},
        )
        for case in cases:
            with self.subTest(case=case["name"]):
                self.assertTrue(case["rationale"].strip())
                self.assertEqual(
                    case["project_owned_dependency_possible"],
                    case["semantic_review_required"],
                )

    def test_false_case_allows_mechanical_advance_without_guidance(self) -> None:
        case = next(
            item
            for item in self.fixture["cases"]
            if not item["semantic_review_required"]
        )
        self.assertEqual(case["affected_project_owned_concepts"], [])
        self.assertEqual(case["discovery_conditions"], [])
        self.assertEqual(case["completion_criteria"], [])
        self.assertTrue(
            case["may_advance_compatibility_mechanically_when_previous_complete"]
        )

    def test_true_case_requires_bounded_reconciliation_guidance(self) -> None:
        case = next(
            item
            for item in self.fixture["cases"]
            if item["semantic_review_required"]
        )
        self.assertTrue(case["affected_project_owned_concepts"])
        self.assertTrue(case["discovery_conditions"])
        self.assertTrue(case["completion_criteria"])
        self.assertFalse(
            case["may_advance_compatibility_mechanically_when_previous_complete"]
        )
        self.assertIn("roles", case["affected_project_owned_concepts"])
        self.assertIn("workflows", case["affected_project_owned_concepts"])
        self.assertIn("shared instructions", case["affected_project_owned_concepts"])
        self.assertIn("indexes", case["affected_project_owned_concepts"])
        self.assertIn("host entrypoints", case["affected_project_owned_concepts"])

    def test_release_instructions_preserve_semantic_judgment_boundary(self) -> None:
        for text in (self.procedure, self.automation):
            with self.subTest(document=text[:40]):
                self.assertIn("Managed delta", text)
                self.assertIn("Project-owned compatibility", text)
                self.assertIn("Required reconciliation", text)
                self.assertIn("deterministic project-file", text)
                self.assertIn("managed behavior change", text.lower())
                self.assertIn("reviewed", text.lower())
                self.assertIn("rationale", text.lower())

        self.assertIn(
            "Tooling must not guess semantic migration need",
            self.procedure,
        )
        self.assertIn(
            "do not infer the result solely from managed behavioral change",
            self.maintainer,
        )
        self.assertIn(
            "presence or absence of deterministic project-file migrations",
            self.maintainer,
        )

    def test_fixture_states_validation_does_not_make_semantic_decision(self) -> None:
        boundary = self.fixture["validation_boundary"]
        self.assertIn("maintainer", boundary["maintainer_judgment"].lower())
        self.assertIn("Do not infer semantic impact", boundary["deterministic_validation"])


if __name__ == "__main__":
    unittest.main()
