from __future__ import annotations

import json
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/review-sufficiency.json"
ROLE = SOURCE_ROOT / "templates/base/roles/change-reviewer/role.md"
INSTRUCTIONS = SOURCE_ROOT / "templates/base/roles/change-reviewer/instructions.md"
CAPABILITIES = SOURCE_ROOT / "templates/base/roles/change-reviewer/capabilities.md"
CONSTRAINTS = SOURCE_ROOT / "templates/base/roles/change-reviewer/constraints.md"
REVIEW_CHANGE = SOURCE_ROOT / "templates/base/workflows/review-change.md"
REVIEW_CATALOG = SOURCE_ROOT / "templates/base/workflows/review-role-catalog.md"


class ReviewSufficiencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}
        cls.role = ROLE.read_text()
        cls.instructions = INSTRUCTIONS.read_text()
        cls.capabilities = CAPABILITIES.read_text()
        cls.constraints = CONSTRAINTS.read_text()
        cls.review_change = REVIEW_CHANGE.read_text()
        cls.review_catalog = REVIEW_CATALOG.read_text()

    def test_fixture_covers_required_termination_scenarios(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 1)
        self.assertEqual(
            self.fixture["finding_admission_test"],
            ["evidence", "consequence", "confidence", "threshold"],
        )
        self.assertEqual(
            set(self.cases),
            {
                "clean-first-review",
                "satisfied-rereview",
                "remediation-introduces-regression",
                "explicit-exhaustive-audit",
            },
        )
        self.assertEqual(
            self.cases["clean-first-review"]["expected_conclusion"],
            "acceptance threshold met",
        )
        self.assertEqual(
            self.cases["satisfied-rereview"]["expected_new_findings"],
            [],
        )
        self.assertTrue(
            self.cases["remediation-introduces-regression"]["regression"],
        )
        self.assertEqual(
            self.cases["explicit-exhaustive-audit"]["review_standard"],
            "audit",
        )

    def test_acceptance_is_default_and_audit_is_explicit(self) -> None:
        self.assertIn("Ordinary bounded review uses the `acceptance` standard", self.instructions)
        self.assertIn("Use the `audit` standard only when", self.instructions)
        self.assertIn("Default: `acceptance`", self.review_change)
        self.assertIn("Default: `audit`", self.review_catalog)
        self.assertIn("explicitly broad catalog audit", self.review_catalog)

    def test_findings_have_an_admission_threshold(self) -> None:
        self.assertIn("# Finding admission test", self.instructions)
        for marker in ("**Evidence**", "**Consequence**", "**Confidence**", "**Threshold**"):
            self.assertIn(marker, self.instructions)
        self.assertIn("alternative valid design", self.instructions)
        self.assertIn("# Optional observations", self.instructions)
        self.assertIn("Do not assign finding severity", self.instructions)
        self.assertIn("report optional observations as findings", self.constraints)

    def test_rereview_is_monotonic_and_can_terminate(self) -> None:
        self.assertIn("# Re-review and termination", self.instructions)
        self.assertIn("A re-review is a continuation of the prior review", self.instructions)
        self.assertIn("classify each prior finding as `resolved`, `unresolved`, or `superseded`", self.instructions)
        self.assertIn("The new concern must independently pass the finding admission test", self.instructions)
        self.assertIn("Terminate the re-review successfully", self.instructions)
        self.assertIn("restart unrestricted discovery", self.constraints)
        self.assertIn("prior_review", self.review_change)
        self.assertIn("prior_review", self.review_catalog)

    def test_terminal_conclusions_preserve_advisory_authority(self) -> None:
        for conclusion in (
            "acceptance threshold not met",
            "acceptance threshold met with non-blocking findings",
            "acceptance threshold met",
            "audit completed",
        ):
            self.assertIn(conclusion, self.instructions)
        self.assertIn("read-only, advisory authority", self.role)
        self.assertIn("does not approve the change", self.instructions)
        self.assertIn("Such a recommendation is advisory", self.capabilities)
        self.assertIn("present an advisory threshold conclusion as user approval", self.constraints)


if __name__ == "__main__":
    unittest.main()
