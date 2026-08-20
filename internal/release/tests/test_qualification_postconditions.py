from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_postconditions as postconditions


class QualificationPostconditionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.execution = self.root / "execution"
        self.execution.mkdir()
        self.matrix = {
            "scenarios": [
                {
                    "id": "semantic-check",
                    "expected_project_changes": [
                        "/index.md",
                        "/roles/index.md",
                    ],
                }
            ]
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_run(self, project_changes: list[dict[str, str]]) -> None:
        journal = self.execution / "scenarios/semantic-check/project/.ava/state/upgrade.json"
        journal.parent.mkdir(parents=True)
        journal.write_text(json.dumps({"project_changes": project_changes}), encoding="utf-8")
        (self.execution / "summary.json").write_text(
            json.dumps(
                {
                    "outcomes": [{"id": "semantic-check", "outcome": "pass"}],
                    "exit_status": 0,
                }
            ),
            encoding="utf-8",
        )

    def test_upgrade_schema_and_role_define_inspection_only_records(self) -> None:
        schema = postconditions.load_json(
            postconditions.REPOSITORY_ROOT / "distribution/schemas/upgrade.schema.json"
        )
        change_types = schema["$defs"]["projectChange"]["properties"]["change_type"]["enum"]
        self.assertIn("inspected", change_types)
        role = (
            postconditions.REPOSITORY_ROOT / "templates/base/roles/upgrade-role/instructions.md"
        ).read_text(encoding="utf-8")
        self.assertIn("change_type: inspected", role)
        self.assertIn("every project-owned path inspected or changed", role)
        self.assertIn("recorded exactly once", role)
        self.assertIn("explicitly state that the exact recorded path was inspected", role)
        self.assertIn("listing the path or its journal classification alone is not sufficient", role)

    def test_inspection_only_records_satisfy_required_path_accounting(self) -> None:
        self.write_run(
            [
                {
                    "path": "/index.md",
                    "change_type": "inspected",
                    "recorded_at": "2026-08-15T00:00:00Z",
                    "resolution": "retained",
                },
                {
                    "path": "/roles/index.md",
                    "change_type": "inspected",
                    "recorded_at": "2026-08-15T00:00:01Z",
                    "resolution": "retained",
                },
            ]
        )
        self.assertEqual(postconditions.apply_postconditions(self.execution, self.matrix), 0)
        summary = json.loads((self.execution / "summary.json").read_text())
        self.assertEqual(summary["outcomes"][0]["outcome"], "pass")

    def test_missing_inspected_path_changes_passing_summary_to_failure(self) -> None:
        self.write_run(
            [
                {
                    "path": "/index.md",
                    "change_type": "inspected",
                    "recorded_at": "2026-08-15T00:00:00Z",
                    "resolution": "retained",
                }
            ]
        )
        self.assertEqual(postconditions.apply_postconditions(self.execution, self.matrix), 1)
        summary = json.loads((self.execution / "summary.json").read_text())
        self.assertEqual(summary["exit_status"], 1)
        self.assertEqual(summary["outcomes"][0]["outcome"], "fail")
        self.assertIn("/roles/index.md", summary["outcomes"][0]["detail"])

    def test_duplicate_or_unresolved_path_is_not_accepted(self) -> None:
        self.write_run(
            [
                {"path": "/index.md", "change_type": "inspected", "resolution": "retained"},
                {"path": "/index.md", "change_type": "modified", "resolution": "reconciled"},
                {"path": "/roles/index.md", "change_type": "modified", "resolution": "unresolved"},
            ]
        )
        errors = postconditions.semantic_project_change_errors(self.execution, self.matrix)
        self.assertIn("duplicate inspected paths", errors["semantic-check"])
        self.assertIn("unresolved inspected paths", errors["semantic-check"])

    def test_checked_in_semantic_scenarios_name_required_paths(self) -> None:
        matrix = postconditions.load_json(postconditions.MATRIX_PATH)
        scenarios = {item["id"]: item for item in matrix["scenarios"]}
        expected = ["/index.md", "/roles/index.md", "/shared/index.md", "/workflows/index.md"]
        self.assertEqual(scenarios["interrupted-finalize"]["expected_project_changes"], expected)
        self.assertEqual(scenarios["pending-semantic-reconciliation"]["expected_project_changes"], expected)
        self.assertEqual(
            scenarios["pending-semantic-reconciliation"]["expected_reported_project_owned_paths"],
            expected,
        )


if __name__ == "__main__":
    unittest.main()
