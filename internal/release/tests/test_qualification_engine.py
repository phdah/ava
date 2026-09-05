from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_ci
from internal.release import qualification_engine as implementation
from internal.release import qualification_runner


class QualificationExecutionTests(unittest.TestCase):
    def test_release_gate_selects_only_deterministic_scenarios(self) -> None:
        matrix = qualification_runner.load_matrix()
        pre = implementation.deterministic_scenarios(matrix, "pre-edge")
        final = implementation.deterministic_scenarios(matrix, "final")

        expected_target_only = [
            "fresh-empty-install",
            "mature-project-install",
            "managed-modified",
            "managed-missing",
            "managed-corrupt",
            "managed-unexpected",
        ]
        self.assertEqual([scenario["id"] for scenario in pre], expected_target_only)
        self.assertEqual(
            [scenario["id"] for scenario in final],
            [
                *expected_target_only,
                "interrupted-resume",
                "interrupted-abort",
                "interrupted-rollback",
            ],
        )
        self.assertTrue(
            all(
                scenario["kind"] not in implementation.BEHAVIORAL_KINDS
                for scenario in pre + final
            )
        )

    def test_root_release_final_uses_target_only_scenarios(self) -> None:
        matrix = qualification_runner.load_matrix()
        target_only = implementation.deterministic_scenarios(
            matrix,
            "final",
            bootstrap=True,
        )
        self.assertEqual(
            [scenario["id"] for scenario in target_only],
            [
                "fresh-empty-install",
                "mature-project-install",
                "managed-modified",
                "managed-missing",
                "managed-corrupt",
                "managed-unexpected",
            ],
        )

    def test_ci_stage_selection_treats_root_release_as_final_without_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixtures = root / "internal/release/fixtures"
            fixtures.mkdir(parents=True)
            (fixtures / "release-upgrade-policy.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "initial_release_version": "1.0.0",
                        "protected_direct_sources": [],
                    }
                ),
                encoding="utf-8",
            )
            (root / "version.txt").write_text("1.0.0\n", encoding="utf-8")

            self.assertEqual(qualification_ci.qualification_stage(root), "final")

    def test_ci_stage_selection_keeps_post_root_release_pre_edge_until_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixtures = root / "internal/release/fixtures"
            fixtures.mkdir(parents=True)
            (fixtures / "release-upgrade-policy.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "initial_release_version": "1.0.0",
                        "protected_direct_sources": [],
                    }
                ),
                encoding="utf-8",
            )
            (root / "version.txt").write_text("1.0.1\n", encoding="utf-8")

            self.assertEqual(qualification_ci.qualification_stage(root), "pre-edge")

            catalogs = root / "internal/release/catalogs"
            catalogs.mkdir(parents=True)
            (catalogs / "1.0.1.json").write_text("{}\n", encoding="utf-8")
            self.assertEqual(qualification_ci.qualification_stage(root), "final")

    def test_ci_stage_selection_rejects_root_upgrade_catalog(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            fixtures = root / "internal/release/fixtures"
            fixtures.mkdir(parents=True)
            (fixtures / "release-upgrade-policy.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "initial_release_version": "1.0.0",
                        "protected_direct_sources": [],
                    }
                ),
                encoding="utf-8",
            )
            (root / "version.txt").write_text("1.0.0\n", encoding="utf-8")
            catalogs = root / "internal/release/catalogs"
            catalogs.mkdir(parents=True)
            (catalogs / "1.0.0.json").write_text("{}\n", encoding="utf-8")

            with self.assertRaisesRegex(
                qualification_ci.QualificationCiError,
                "root release must not define",
            ):
                qualification_ci.qualification_stage(root)

    def test_behavioral_scenarios_remain_outside_release_gate(self) -> None:
        matrix = qualification_runner.load_matrix()
        behavioral = {
            scenario["id"]
            for scenario in matrix["scenarios"]
            if scenario["kind"] in implementation.BEHAVIORAL_KINDS
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
            "1.0.0",
            "v1.0.0",
            "1" * 40,
            False,
            {"upgrade_paths": {"edges": []}},
        )
        for semantic_review_required in (False, True):
            target = qualification_runner.ReleaseIdentity(
                Path("/target"),
                "1.0.1",
                "v1.0.1",
                "2" * 40,
                semantic_review_required,
                {
                    "upgrade_paths": {
                        "edges": [
                            {
                                "from": source.version,
                                "to": "1.0.1",
                            }
                        ]
                    }
                },
            )
            implementation.validate_final_edge(source, target)

    def test_root_target_requires_no_upgrade_edge(self) -> None:
        target = qualification_runner.ReleaseIdentity(
            Path("/target"),
            "1.0.0",
            "v1.0.0",
            "2" * 40,
            False,
            {"upgrade_paths": {"edges": []}},
        )
        implementation.validate_bootstrap_target(target)

    def test_root_target_rejects_upgrade_edge(self) -> None:
        target = qualification_runner.ReleaseIdentity(
            Path("/target"),
            "1.0.0",
            "v1.0.0",
            "2" * 40,
            False,
            {"upgrade_paths": {"edges": [{"from": "0.9.0", "to": "1.0.0"}]}},
        )
        with self.assertRaises(implementation.QualificationExecutionError):
            implementation.validate_bootstrap_target(target)

    def test_canonical_entrypoint_uses_current_engine(self) -> None:
        release_root = implementation.REPOSITORY_ROOT / "internal/release"
        shell = (release_root / "qualify-release.sh").read_text(encoding="utf-8")
        driver = (release_root / "qualification.py").read_text(encoding="utf-8")
        engine = (release_root / "qualification_engine.py").read_text(encoding="utf-8")
        self.assertIn("qualification.py", shell)
        self.assertIn("qualification_engine", driver)
        self.assertIn("AVA_QUALIFICATION_EXECUTOR", driver)
        for obsolete in ("qualification_work", "ChatGPT Work", "session-neutral"):
            self.assertNotIn(obsolete, driver)
            self.assertNotIn(obsolete, engine)

    def test_final_evidence_schema_is_executor_based(self) -> None:
        schema_path = (
            implementation.REPOSITORY_ROOT
            / "internal/release/qualification/schemas/qualification-run-record.schema.json"
        )
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        fields = set(schema["properties"])
        self.assertIn("qualification_mode", fields)
        self.assertIn("qualification_executor", fields)
        self.assertNotIn("qualification_host", fields)
        self.assertNotIn("const", schema["properties"]["qualification_executor"])
        self.assertNotIn("qualification_model", fields)
        self.assertNotIn("audit_model", fields)
        self.assertNotIn("audit_report_file", fields)
        self.assertNotIn("interaction_evidence_file", fields)

    def test_execution_procedure_describes_current_gate(self) -> None:
        root = implementation.REPOSITORY_ROOT
        text = (root / "internal/release/qualification-execution.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("GitHub Actions", text)
        self.assertIn("deterministic", text.lower())
        self.assertIn("pre-edge", text)
        self.assertIn("final", text)
        self.assertIn("Root release", text)
        self.assertNotIn("session-neutral", text.lower())
        self.assertNotIn("ChatGPT Work", text)
        self.assertNotIn("OpenCode", text)

    def test_github_actions_owns_mandatory_execution(self) -> None:
        root = implementation.REPOSITORY_ROOT
        procedure = (root / "internal/release/procedure.md").read_text(encoding="utf-8")
        qualification_workflow = (
            root / ".github/workflows/release-qualification.yml"
        ).read_text(encoding="utf-8")
        ci_driver = (root / "internal/release/qualification_ci.py").read_text(
            encoding="utf-8"
        )
        python_workflow = (root / ".github/workflows/python-tests.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("internal/release/test.sh", python_workflow)
        self.assertIn("GitHub Actions", procedure)
        self.assertNotIn("session-neutral", procedure.lower())
        self.assertIn("python3 -m internal.release.qualification_ci", qualification_workflow)
        self.assertNotIn("python3 - <<", qualification_workflow)
        self.assertNotIn("package_changes()", qualification_workflow)
        self.assertNotIn("acceptance-request.json", qualification_workflow)
        self.assertIn("run-release-qualification.sh", ci_driver)
        self.assertIn("acceptance-request.json", ci_driver)
        self.assertIn("AVA_QUALIFICATION_EXECUTOR", qualification_workflow)

    def test_ci_driver_validates_acceptance_request_shape(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "request.json"
            path.write_text(
                json.dumps(
                    {
                        "identity": "user:test",
                        "run_id": "run-test",
                        "schema_version": 1,
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                qualification_ci.load_acceptance_request(path),
                {
                    "identity": "user:test",
                    "run_id": "run-test",
                    "schema_version": 1,
                },
            )
            path.write_text(
                json.dumps(
                    {
                        "identity": "user:test",
                        "run_id": "run-test",
                        "schema_version": 1,
                        "unexpected": True,
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(qualification_ci.QualificationCiError):
                qualification_ci.load_acceptance_request(path)


if __name__ == "__main__":
    unittest.main()
