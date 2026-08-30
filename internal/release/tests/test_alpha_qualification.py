from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

from internal.release import conformance_common

SOURCE_ROOT = Path(__file__).resolve().parents[3]
POLICY_PATH = SOURCE_ROOT / "internal/release/alpha-qualification.json"
MATRIX_PATH = SOURCE_ROOT / "internal/release/conformance-matrix.json"
ASSEMBLE = SOURCE_ROOT / "internal/release/assemble.py"


class AlphaQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.policy = json.loads(POLICY_PATH.read_text())
        cls.matrix = json.loads(MATRIX_PATH.read_text())

    def test_policy_schema_and_gate_identifiers_are_stable(self) -> None:
        self.assertEqual(self.policy["schema_version"], 1)
        self.assertEqual(
            [gate["id"] for gate in self.policy["gates"]],
            [
                "repository",
                "clean-install",
                "normal-routing",
                "managed-upgrade",
                "semantic-upgrade",
                "rollback",
                "trust-and-provenance",
            ],
        )

    def test_gate_evidence_resolves_to_files_and_conformance_cases(self) -> None:
        matrix_cases = {case["id"] for case in self.matrix["cases"]}
        for gate in self.policy["gates"]:
            for path in gate["documents"]:
                self.assertTrue((SOURCE_ROOT / path).exists(), f"{gate['id']}: {path}")
            for case_id in gate["matrix_cases"]:
                self.assertIn(case_id, matrix_cases, f"{gate['id']}: {case_id}")

    def test_phase_one_through_four_tasks_are_complete(self) -> None:
        tasks_root = SOURCE_ROOT / "internal/todo/tasks"
        task_files: list[tuple[int, Path]] = []
        for path in sorted(tasks_root.glob("ava-* - *.md")):
            task_id_text = path.name.split(" ", 1)[0].removeprefix("ava-")
            if not task_id_text.isdigit():
                continue
            task_id = int(task_id_text)
            if 100 <= task_id < 500:
                task_files.append((task_id, path))

        self.assertTrue(task_files)
        self.assertEqual({task_id // 100 for task_id, _path in task_files}, {1, 2, 3, 4})
        for _task_id, path in task_files:
            frontmatter = path.read_text().split("---", 2)[1]
            self.assertRegex(
                frontmatter,
                r'(?m)^status:\s*["\']?Done["\']?\s*$',
                path.relative_to(SOURCE_ROOT),
            )

    def test_finding_classes_and_protected_impacts_block_correctly(self) -> None:
        classes = {item["id"]: item for item in self.policy["finding_classes"]}
        self.assertEqual(set(classes), {"blocker", "required-v1", "post-v1"})
        self.assertEqual(classes["blocker"]["current_publication"], "blocked")
        self.assertEqual(classes["required-v1"]["current_publication"], "blocked")
        self.assertEqual(classes["post-v1"]["current_publication"], "allowed")
        self.assertTrue(classes["blocker"]["protected_trust_impacts"])
        self.assertTrue(classes["required-v1"]["protected_trust_impacts"])
        self.assertFalse(classes["post-v1"]["protected_trust_impacts"])

    def test_publication_approval_is_exact_and_revision_bound(self) -> None:
        approval = self.policy["publication_approval"]
        self.assertEqual(approval["required_state"], "approved")
        self.assertTrue(approval["exact_release_identity"])
        self.assertTrue(approval["exact_source_revision"])
        self.assertTrue(approval["exact_asset_checksums"])
        self.assertTrue(approval["exact_qualification_run"])

    def test_public_release_schema_requires_explicit_upgrade_edges(self) -> None:
        release_schema = json.loads((SOURCE_ROOT / "distribution/schemas/release.schema.json").read_text())
        upgrade_paths = release_schema["properties"]["upgrade_paths"]
        self.assertEqual(upgrade_paths["required"], ["edges"])
        edge = upgrade_paths["properties"]["edges"]["items"]
        self.assertIn("semantic_review_required", edge["properties"])

    def test_prerelease_transitions_are_machine_readable_release_edges(self) -> None:
        releases = sorted((SOURCE_ROOT / "internal/release/releases").glob("1.0.0-alpha.*.json"))
        self.assertTrue(releases)
        for release in releases:
            record = json.loads(release.read_text())
            self.assertIn("upgrade_edge", record)
            self.assertEqual(record["upgrade_edge"]["to"], record["version"])

    def test_first_alpha_is_reproducible_and_has_no_supported_source(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_path = Path(first)
            second_path = Path(second)
            self._assemble(first_path, "1.0.0-alpha.1", "0" * 40, 1)
            self._assemble(second_path, "1.0.0-alpha.1", "0" * 40, 1)
            first_manifest = json.loads((first_path / "ava-release.json").read_text())
            second_manifest = json.loads((second_path / "ava-release.json").read_text())
            self.assertEqual(first_manifest["upgrade_paths"]["edges"], [])
            self.assertEqual(first_manifest, second_manifest)
            for asset_name in ("ava-base.tar.gz", "ava-guidance.tar.gz", "ava-migrations.tar.gz"):
                self.assertEqual(
                    hashlib.sha256((first_path / asset_name).read_bytes()).hexdigest(),
                    hashlib.sha256((second_path / asset_name).read_bytes()).hexdigest(),
                )

    def test_first_alpha_with_empty_edges_passes_conformance(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target = Path(target_dir)
            self._assemble(target, "1.0.0-alpha.1", "0" * 40, 1)
            findings = conformance_common.validate_release_directory(target, expected_version="1.0.0-alpha.1")
            self.assertFalse([finding for finding in findings if finding["severity"] == "blocking"])

    def test_non_first_release_with_empty_edges_fails_conformance(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target = Path(target_dir)
            self._assemble(target, "1.0.0-alpha.2", "0" * 40, 2)
            manifest_path = target / "ava-release.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["upgrade_paths"]["edges"] = []
            manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            findings = conformance_common.validate_release_directory(target, expected_version="1.0.0-alpha.2")
            rules = {finding["rule_id"] for finding in findings if finding["severity"] == "blocking"}
            self.assertIn("AVA-RELEASE-UPGRADE-PATH-MISSING", rules)

    def test_historical_unversioned_source_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as target_dir:
            target = Path(target_dir)
            self._assemble(target, "1.0.0-alpha.1", "0" * 40, 1)
            manifest_path = target / "ava-release.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["upgrade_paths"]["edges"] = [
                {
                    "from": "0.0.0",
                    "to": "1.0.0-alpha.1",
                    "mode": "direct",
                    "intermediates": [],
                    "carry_unresolved_semantic_state": False,
                    "migration_ids": [],
                    "guidance_paths": [],
                    "semantic_review_required": False,
                }
            ]
            manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            findings = conformance_common.validate_release_directory(target, expected_version="1.0.0-alpha.1")
            rules = {finding["rule_id"] for finding in findings if finding["severity"] == "blocking"}
            self.assertIn("AVA-RELEASE-BOOTSTRAP-EDGE", rules)

    def test_assembly_rejects_links_that_break_after_destination_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as root_dir, tempfile.TemporaryDirectory() as output_dir:
            root = Path(root_dir)
            self._copy_source(root)
            path = root / "templates/base/roles/role-manager/index.md"
            path.write_text(path.read_text() + "\n[broken](../../../outside.md)\n")
            result = self._assemble_process(root, Path(output_dir), "1.0.0-alpha.1", "0" * 40, 1)
            self.assertNotEqual(result.returncode, 0)

    def test_assembly_rejects_links_that_escape_the_installed_root(self) -> None:
        with tempfile.TemporaryDirectory() as root_dir, tempfile.TemporaryDirectory() as output_dir:
            root = Path(root_dir)
            self._copy_source(root)
            path = root / "templates/base/roles/role-manager/index.md"
            path.write_text(path.read_text() + "\n[broken](../../../../outside.md)\n")
            result = self._assemble_process(root, Path(output_dir), "1.0.0-alpha.1", "0" * 40, 1)
            self.assertNotEqual(result.returncode, 0)

    @staticmethod
    def _copy_source(destination: Path) -> None:
        for item in SOURCE_ROOT.iterdir():
            if item.name in {".git", "__pycache__"}:
                continue
            target = destination / item.name
            if item.is_dir():
                shutil.copytree(item, target)
            else:
                shutil.copy2(item, target)

    def _assemble(self, output: Path, version: str, revision: str, epoch: int) -> None:
        result = self._assemble_process(SOURCE_ROOT, output, version, revision, epoch)
        if result.returncode != 0:
            self.fail(result.stderr)

    @staticmethod
    def _assemble_process(root: Path, output: Path, version: str, revision: str, epoch: int) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env["PYTHONPATH"] = str(root)
        return subprocess.run(
            [
                "python3",
                str(root / "internal/release/assemble.py"),
                "--root",
                str(root),
                "--output",
                str(output),
                "--version",
                version,
                "--source-revision",
                revision,
                "--source-date-epoch",
                str(epoch),
            ],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
