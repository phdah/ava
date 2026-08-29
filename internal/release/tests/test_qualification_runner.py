from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_runner as runner


REVISION_A = "0123456789abcdef0123456789abcdef01234567"
REVISION_B = "89abcdef0123456789abcdef0123456789abcdef"


class QualificationRunnerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.qualification = self.root / "qualification"
        (self.qualification / "corpus").mkdir(parents=True)
        (self.qualification / "corpus/source.txt").write_text("baseline\n", encoding="utf-8")
        self.test_project = self.root / "project"
        self.test_project.mkdir()
        self.source_assets = self.root / "source-assets"
        self.target_assets = self.root / "target-assets"

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def make_assets(
        self,
        directory: Path,
        *,
        version: str,
        revision: str,
        semantic_review_required: bool,
        edges: list[dict] | None = None,
    ) -> runner.ReleaseIdentity:
        directory.mkdir()
        manifest = {
            "ava_version": version,
            "tag": f"v{version}",
            "source_revision": revision,
            "semantic_review_required": semantic_review_required,
            "assets": [{"name": name} for name in runner.RELEASE_ASSETS],
            "upgrade_paths": {"edges": edges or []},
        }
        for name in runner.RELEASE_ASSETS:
            if name in {"ava-release.json", "SHA256SUMS"}:
                continue
            (directory / name).write_text(f"{name}:{version}\n", encoding="utf-8")
        (directory / "ava-release.json").write_text(
            json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8"
        )
        checksums = []
        for name in runner.RELEASE_ASSETS:
            if name == "SHA256SUMS":
                continue
            checksums.append(f"{self.digest(directory / name)}  {name}")
        (directory / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")
        return runner.validate_asset_dir(directory, directory.name)

    def test_matrix_is_complete_and_deterministically_ordered(self) -> None:
        matrix = runner.load_matrix()
        self.assertEqual(len(matrix["families"]), 8)
        self.assertEqual(len(matrix["scenarios"]), 17)
        self.assertEqual(
            [item["id"] for item in matrix["scenarios"] if item["kind"] == "managed-damage"],
            ["managed-modified", "managed-missing", "managed-corrupt", "managed-unexpected"],
        )
        expected_rules = {
            item["damage"]: item["expected_rule"]
            for item in matrix["scenarios"]
            if item["kind"] == "managed-damage"
        }
        self.assertEqual(
            expected_rules,
            {
                "modified": "AVA-MANAGED-CHECKSUM",
                "missing": "AVA-MANAGED-MISSING",
                "corrupt": "AVA-UPGRADE-READ",
                "unexpected": "AVA-MANAGED-UNEXPECTED",
            },
        )
        calendar = next(item for item in matrix["scenarios"] if item["kind"] == "registered-calendar")
        self.assertEqual(calendar["expected_weekday"], "Friday")
        self.assertEqual(calendar["expected_date"], "2026-08-14")
        self.assertEqual(calendar["forbidden_date"], "2026-08-15")
        inbox = next(item for item in matrix["scenarios"] if item["kind"] == "complete-inbox")
        self.assertIn("personal expense incurred for work", inbox["prompt"])
        self.assertIn("source-attributed claim", inbox["prompt"])
        self.assertTrue(inbox["semantic_audit_required"])

    def test_asset_validation_requires_pinned_checksummed_identity(self) -> None:
        source = self.make_assets(
            self.source_assets,
            version="1.0.0-alpha.14",
            revision=REVISION_A,
            semantic_review_required=False,
        )
        edge = {
            "from": source.version,
            "to": "1.0.0-alpha.15",
            "mode": "direct",
            "intermediates": [],
            "carry_unresolved_semantic_state": False,
            "migration_ids": [],
            "guidance_paths": ["guidance/alpha-14-to-alpha-15.json"],
            "semantic_review_required": True,
        }
        target = self.make_assets(
            self.target_assets,
            version="1.0.0-alpha.15",
            revision=REVISION_B,
            semantic_review_required=True,
            edges=[edge],
        )
        runner.validate_upgrade_pair(source, target)

        (self.target_assets / "ava-base.tar.gz").write_text("tampered\n", encoding="utf-8")
        with self.assertRaisesRegex(runner.QualificationError, "checksum mismatch"):
            runner.validate_asset_dir(self.target_assets, "target assets")

    def test_latest_asset_selection_is_refused(self) -> None:
        latest = self.root / "latest"
        latest.mkdir()
        with self.assertRaisesRegex(runner.QualificationError, "latest selection"):
            runner.validate_asset_dir(latest, "target assets")

    def test_execution_root_requires_ownership_and_stable_corpus(self) -> None:
        execution = self.root / "execution"
        execution.mkdir()
        (execution / "unrelated.txt").write_text("do not delete\n", encoding="utf-8")
        with self.assertRaisesRegex(runner.QualificationError, "unsafe pre-existing execution root"):
            runner.validate_execution_root(
                execution,
                repository_root=self.repo,
                qualification_root=self.qualification,
                test_project=self.test_project,
                source_assets=self.source_assets,
                target_assets=self.target_assets,
            )

        (execution / "unrelated.txt").unlink()
        runner.initialize_execution_root(execution, self.qualification)
        runner.validate_execution_root(
            execution,
            repository_root=self.repo,
            qualification_root=self.qualification,
            test_project=self.test_project,
            source_assets=self.source_assets,
            target_assets=self.target_assets,
        )
        (self.qualification / "corpus/source.txt").write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(runner.QualificationError, "finalized corpus differs"):
            runner.validate_execution_root(
                execution,
                repository_root=self.repo,
                qualification_root=self.qualification,
                test_project=self.test_project,
                source_assets=self.source_assets,
                target_assets=self.target_assets,
            )

    def test_execution_root_rejects_overlapping_input_boundaries(self) -> None:
        with self.assertRaisesRegex(runner.QualificationError, "disjoint"):
            runner.validate_execution_root(
                self.qualification / "run",
                repository_root=self.repo,
                qualification_root=self.qualification,
                test_project=self.test_project,
                source_assets=self.source_assets,
                target_assets=self.target_assets,
            )

    def test_interrupted_rerun_retains_pass_and_recreates_nonpass(self) -> None:
        source = self.qualification / "variants/01-empty-before-installation"
        (source / "project").mkdir(parents=True)
        (source / "project/baseline.txt").write_text("clean\n", encoding="utf-8")
        execution = self.root / "execution"
        runner.initialize_execution_root(execution, self.qualification)
        scenario = {
            "id": "fresh-empty-install",
            "source": "variants/01-empty-before-installation",
        }
        state = {"schema_version": 1, "scenarios": {}}
        workspace, already = runner.scenario_workspace(execution, self.qualification, scenario, state)
        self.assertFalse(already)
        (workspace / "project/baseline.txt").write_text("interrupted\n", encoding="utf-8")

        state["scenarios"]["fresh-empty-install"] = {"outcome": "fail"}
        workspace, already = runner.scenario_workspace(execution, self.qualification, scenario, state)
        self.assertFalse(already)
        self.assertEqual((workspace / "project/baseline.txt").read_text(), "clean\n")

        state["scenarios"]["fresh-empty-install"] = {"outcome": "pass"}
        (workspace / "project/baseline.txt").write_text("evidence\n", encoding="utf-8")
        retained, already = runner.scenario_workspace(execution, self.qualification, scenario, state)
        self.assertTrue(already)
        self.assertEqual((retained / "project/baseline.txt").read_text(), "evidence\n")

    def test_opencode_role_announcement_matches_installed_contract(self) -> None:
        qualification = runner.Runner.__new__(runner.Runner)
        qualification.opencode = "opencode"
        qualification.model = "provider/model"
        qualification.transcript_dir = None
        qualification.run_command = lambda *args, **kwargs: runner.CommandResult(
            0, "Active role: Private Life Steward\n", ""
        )

        result = qualification.opencode_prompt(
            "private-routing",
            self.root,
            "record private context",
            expected_role="Private Life Steward",
        )

        self.assertIn("Active role: Private Life Steward", result.stdout)

    def test_summary_is_nonzero_for_fail_skip_or_required_decision(self) -> None:
        self.assertEqual(runner.summary_exit_status([{"outcome": "pass"}]), 0)
        for outcome in ("fail", "skipped", "user-decision-required"):
            self.assertEqual(
                runner.summary_exit_status([{"outcome": "pass"}, {"outcome": outcome}]),
                1,
            )

    def test_cli_requires_explicit_inputs_and_supports_preflight_only(self) -> None:
        args = runner.parse_args(
            [
                "--qualification-root", str(self.qualification),
                "--execution-root", str(self.root / "execution"),
                "--source-assets", str(self.source_assets),
                "--target-assets", str(self.target_assets),
                "--test-project", str(self.test_project),
                "--opencode", "opencode",
                "--model", "provider/model",
                "--preflight-only",
            ]
        )
        self.assertTrue(args.preflight_only)
        self.assertEqual(args.model, "provider/model")

    def test_rollback_is_planned_as_one_installer_operation(self) -> None:
        import inspect

        source = inspect.getsource(runner.Runner.run_scenario)
        self.assertEqual(source.count('"--rollback"'), 1)

    def test_complete_runner_is_not_executed_by_release_test_gate(self) -> None:
        test_script = (runner.REPOSITORY_ROOT / "internal/release/test.sh").read_text(encoding="utf-8")
        matching = [line.strip() for line in test_script.splitlines() if "qualify-synthetic.sh" in line]
        self.assertEqual(len(matching), 1)
        self.assertTrue(matching[0].startswith("sh -n "))

    def test_runner_and_matrix_remain_internal_release_inputs(self) -> None:
        self.assertTrue(str(Path(runner.__file__).resolve()).startswith(str(runner.REPOSITORY_ROOT / "internal")))
        matrix = runner.MATRIX_PATH.resolve()
        self.assertTrue(matrix.is_relative_to(runner.REPOSITORY_ROOT / "internal"))
        self.assertFalse(matrix.is_relative_to(runner.REPOSITORY_ROOT / "templates"))


if __name__ == "__main__":
    unittest.main()
