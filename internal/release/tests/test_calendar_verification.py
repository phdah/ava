from __future__ import annotations

import json
import unittest
from datetime import date, timedelta
from pathlib import Path

from internal.release.assemble import read_payloads

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/calendar-verification.json"
CONTRACT = SOURCE_ROOT / "templates/base/shared/instructions/calendar-verification.md"
SHARED_INDEX = SOURCE_ROOT / "templates/base/shared/instructions/index.md"
ROUTER = SOURCE_ROOT / "templates/base/AGENTS.md"
ROLE_INDEXES = {
    "role-manager": SOURCE_ROOT / "templates/base/roles/role-manager/index.md",
    "project-steward": SOURCE_ROOT / "templates/base/roles/project-steward/index.md",
    "inbox-ingester": SOURCE_ROOT / "templates/base/roles/inbox-ingester/index.md",
    "upgrade-role": SOURCE_ROOT / "templates/base/roles/upgrade-role/index.md",
}
REVIEWER_INDEX = SOURCE_ROOT / "templates/base/roles/change-reviewer/index.md"


class CalendarVerificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}
        cls.contract = CONTRACT.read_text()
        cls.shared_index = SHARED_INDEX.read_text()
        cls.router = ROUTER.read_text()
        cls.role_indexes = {name: path.read_text() for name, path in ROLE_INDEXES.items()}
        cls.reviewer_index = REVIEWER_INDEX.read_text()

    def test_fixture_covers_required_calendar_boundaries(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 1)
        self.assertEqual(
            set(self.cases),
            {
                "thursday-friday-regression",
                "week-boundary-next-monday",
                "month-boundary-tomorrow",
                "year-boundary-tomorrow",
                "leap-day-tomorrow",
                "source-relative-historical-tomorrow",
                "unresolved-next-week-without-week-convention",
                "contradictory-weekday-date-review",
            },
        )

        month_case = self.cases["month-boundary-tomorrow"]
        self.assertEqual(
            date.fromisoformat(month_case["reference_date"]) + timedelta(days=1),
            date.fromisoformat(month_case["expected_absolute"]),
        )

        year_case = self.cases["year-boundary-tomorrow"]
        self.assertEqual(
            date.fromisoformat(year_case["reference_date"]) + timedelta(days=1),
            date.fromisoformat(year_case["expected_absolute"]),
        )

        leap_case = self.cases["leap-day-tomorrow"]
        self.assertEqual(
            date.fromisoformat(leap_case["reference_date"]) + timedelta(days=1),
            date.fromisoformat(leap_case["expected_absolute"]),
        )

    def test_thursday_friday_regression_is_frozen(self) -> None:
        case = self.cases["thursday-friday-regression"]
        reference = date.fromisoformat(case["reference_date"])
        expected = date.fromisoformat(case["expected_absolute"])
        forbidden = date.fromisoformat(case["forbidden_absolute"])

        self.assertEqual(reference.weekday(), 3)
        self.assertEqual(expected, reference + timedelta(days=1))
        self.assertEqual(expected.weekday(), 4)
        self.assertEqual(forbidden.weekday(), 5)
        self.assertEqual(case["expected_absolute"], "2026-08-14")
        self.assertEqual(case["forbidden_absolute"], "2026-08-15")

    def test_week_boundary_and_historical_source_reference_are_deterministic(self) -> None:
        week_case = self.cases["week-boundary-next-monday"]
        self.assertEqual(
            date.fromisoformat(week_case["reference_date"]) + timedelta(days=1),
            date.fromisoformat(week_case["expected_absolute"]),
        )
        self.assertEqual(date.fromisoformat(week_case["expected_absolute"]).weekday(), 0)

        source_case = self.cases["source-relative-historical-tomorrow"]
        self.assertEqual(
            date.fromisoformat(source_case["reference_date"]) + timedelta(days=1),
            date.fromisoformat(source_case["expected_absolute"]),
        )
        self.assertNotEqual(source_case["expected_absolute"], source_case["host_date"])
        self.assertEqual(source_case["reference_kind"], "source-document")

    def test_unresolved_period_is_preserved_instead_of_invented(self) -> None:
        case = self.cases["unresolved-next-week-without-week-convention"]
        self.assertIsNone(case["locale"])
        self.assertIsNone(case["week_start"])
        self.assertIsNone(case["expected_absolute"])
        self.assertEqual(case["expected_action"], "preserve-or-clarify")

    def test_contract_requires_only_the_calendar_verification_invariant(self) -> None:
        self.assertIn("persist a calendar value derived", self.contract)
        self.assertIn("establish the reference date, time, or source context", self.contract)
        self.assertIn("available deterministic date or calendar operation", self.contract)
        self.assertIn("weekday/date agreement or week number", self.contract)
        self.assertIn("Do not rely on mental calendar arithmetic", self.contract)
        self.assertIn("preserve the original wording or ask for clarification", self.contract)
        self.assertIn("Source-relative wording must remain anchored to its source context", self.contract)
        self.assertNotIn("2026-08-14", self.contract)
        self.assertNotIn("2026-08-15", self.contract)

    def test_calendar_contract_is_discoverable_but_not_global(self) -> None:
        self.assertIn("[Calendar verification](calendar-verification.md)", self.shared_index)
        self.assertNotIn("calendar-verification", self.router)

        for role, text in self.role_indexes.items():
            with self.subTest(role=role):
                required, additional = text.split("## Additional context", 1)
                self.assertNotIn("calendar-verification", required)
                self.assertIn("calendar-verification", additional)
                self.assertIn("relative calendar language", additional)

    def test_reviewer_treats_weekday_date_contradiction_as_semantic_fidelity(self) -> None:
        required, additional = self.reviewer_index.split("## Additional context", 1)
        self.assertNotIn("calendar-verification", required)
        self.assertIn("calendar-verification", additional)
        self.assertIn("contradictory weekday and date", additional)
        self.assertIn("semantic-fidelity defect", self.contract)
        self.assertEqual(
            self.cases["contradictory-weekday-date-review"]["expected_action"],
            "semantic-fidelity-finding",
        )

    def test_assembled_payload_contains_conditional_contract(self) -> None:
        payloads = {item.destination: item for item in read_payloads(SOURCE_ROOT)}
        contract_destination = "/.ava/base/shared/instructions/calendar-verification.md"
        self.assertIn(contract_destination, payloads)
        self.assertIn(
            "Use this instruction only when a task would persist a calendar value derived",
            payloads[contract_destination].data.decode("utf-8"),
        )
        self.assertNotIn("calendar-verification", payloads["/AGENTS.md"].data.decode("utf-8"))

        for role in ROLE_INDEXES:
            destination = f"/.ava/base/roles/{role}/index.md"
            self.assertIn(destination, payloads)
            text = payloads[destination].data.decode("utf-8")
            required, additional = text.split("## Additional context", 1)
            self.assertNotIn("calendar-verification", required)
            self.assertIn("calendar-verification", additional)


if __name__ == "__main__":
    unittest.main()
