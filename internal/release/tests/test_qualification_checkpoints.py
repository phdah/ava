from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[3]
ASSEMBLER = SOURCE_ROOT / "internal/release/assemble.py"
INSTALLER_SOURCE = SOURCE_ROOT / "internal/release/ava-install.sh"
CHECKPOINT = SOURCE_ROOT / "internal/release/fixtures/synthetic-qualification-vault/checkpoint.py"
REVISION = "0123456789abcdef0123456789abcdef01234567"


class QualificationCheckpointTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.target = self.root / "project"
        self.assets = self.root / "assets"
        self.target.mkdir()
        self._create_repository_fixture()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_command(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check and result.returncode != 0:
            self.fail(
                f"command failed ({result.returncode}): {' '.join(args)}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def _create_repository_fixture(self) -> None:
        (self.repo / "internal/release").mkdir(parents=True)
        shutil.copyfile(ASSEMBLER, self.repo / "internal/release/assemble.py")
        shutil.copyfile(INSTALLER_SOURCE, self.repo / "internal/release/ava-install.sh")
        shutil.copytree(SOURCE_ROOT / "internal/release/installer", self.repo / "internal/release/installer")
        base = self.repo / "templates/base"
        for directory in ("roles", "workflows", "shared/instructions", "knowledge", "inbox/processed"):
            (base / directory).mkdir(parents=True, exist_ok=True)
        (base / "AGENTS.md").write_text("# Router 0.1.0\n")
        (base / "index.md").write_text("# Base\n")
        (base / "roles/index.md").write_text("# Roles\n")
        (base / "workflows/index.md").write_text("# Workflows\n")
        (base / "shared/index.md").write_text("# Shared\n")
        (base / "shared/instructions/test.md").write_text("# Test instruction\n")
        (base / "knowledge/index.md").write_text("# Source knowledge\n")
        (base / "inbox/index.md").write_text("# Source inbox\n")
        (base / "inbox/processed/index.md").write_text("# Source processed\n")
        scaffolds = self.repo / "templates/project-scaffolds"
        for directory in ("roles", "workflows", "shared", "knowledge", "inbox/processed"):
            (scaffolds / directory).mkdir(parents=True, exist_ok=True)
        (scaffolds / "index.md").write_text("# Project\n")
        for directory in ("roles", "workflows", "shared", "knowledge", "inbox"):
            (scaffolds / directory / "index.md").write_text(f"# {directory}\n")
        (scaffolds / "inbox/processed/index.md").write_text("# Processed\n")

    def build(self, version: str, *, upgrade_from: str | None = None) -> Path:
        output = self.assets / f"v{version}"
        output.mkdir(parents=True)
        args = [
            "python3",
            str(self.repo / "internal/release/assemble.py"),
            "--root",
            str(self.repo),
            "--output",
            str(output),
            "--version",
            version,
            "--source-revision",
            REVISION,
            "--source-date-epoch",
            "1700000000",
        ]
        if upgrade_from:
            args.extend(("--upgrade-from", upgrade_from))
        self.run_command(*args)
        return output

    def install(self, assets: Path, *extra: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return self.run_command(
            "sh",
            str(assets / "ava-install.sh"),
            "--target",
            str(self.target),
            "--asset-dir",
            str(assets),
            *extra,
            check=check,
        )

    def prepare_upgrade(self) -> tuple[Path, Path]:
        source = self.build("0.1.0")
        (self.target / "project-owned.txt").write_text("preserve me\n")
        self.install(source)
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        target = self.build("0.2.0", upgrade_from="0.1.0")
        return source, target

    def checkpoint(self, mode: str, target_assets: Path) -> dict:
        result = self.run_command(
            "python3",
            str(CHECKPOINT),
            mode,
            "--target",
            str(self.target),
            "--asset-dir",
            str(target_assets),
        )
        return json.loads(result.stdout)

    def manifest(self) -> dict:
        return json.loads((self.target / ".ava/state/manifest.json").read_text())

    def journal(self) -> dict:
        return json.loads((self.target / ".ava/state/upgrade.json").read_text())

    def assert_transaction_cleaned(self) -> None:
        transactions = self.target / ".ava/state/transactions"
        self.assertFalse(transactions.exists(), list(transactions.iterdir()) if transactions.exists() else None)

    def test_abort_checkpoint_uses_real_transaction_and_restores_source(self) -> None:
        _, target = self.prepare_upgrade()
        evidence = self.checkpoint("abort", target)
        self.assertEqual(evidence["stage"], "staged")
        self.assertFalse(evidence["live_mutation_started"])
        self.assertFalse(evidence["managed_commit_complete"])
        self.assertIn("abort", evidence["allowed_operations"])
        self.assertTrue((self.target / evidence["transaction_relative"] / "plan.json").is_file())
        self.assertEqual(self.manifest()["ava_version"], "0.1.0")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.1.0\n")

        self.install(target, "--abort")
        self.assertEqual(self.manifest()["ava_version"], "0.1.0")
        self.assertEqual(self.journal()["status"], "idle")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.1.0\n")
        self.assertEqual((self.target / "project-owned.txt").read_text(), "preserve me\n")
        self.assert_transaction_cleaned()

    def test_resume_checkpoint_completes_target_and_cleans_transaction(self) -> None:
        _, target = self.prepare_upgrade()
        evidence = self.checkpoint("resume", target)
        self.assertEqual(evidence["stage"], "validating")
        self.assertTrue(evidence["live_mutation_started"])
        self.assertFalse(evidence["managed_commit_complete"])
        self.assertIn("resume", evidence["allowed_operations"])
        self.assertEqual(self.manifest()["ava_version"], "0.1.0")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.2.0\n")

        self.install(target, "--resume")
        self.assertEqual(self.manifest()["ava_version"], "0.2.0")
        self.assertEqual(self.journal()["status"], "complete")
        self.assertEqual(self.journal()["allowed_operations"], ["normal"])
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.2.0\n")
        self.assertEqual((self.target / "project-owned.txt").read_text(), "preserve me\n")
        self.assert_transaction_cleaned()

    def test_resume_rejects_unrelated_managed_edit_then_accepts_recorded_source_checksum(self) -> None:
        _, target = self.prepare_upgrade()
        self.checkpoint("resume", target)
        (self.target / "AGENTS.md").write_text("unrelated edit\n")
        failed = self.install(target, "--resume", check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("RESUME_CONFLICT", failed.stderr)

        (self.target / "AGENTS.md").write_text("# Router 0.1.0\n")
        self.install(target, "--resume")
        self.assertEqual(self.manifest()["ava_version"], "0.2.0")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.2.0\n")
        self.assertEqual((self.target / "project-owned.txt").read_text(), "preserve me\n")
        self.assert_transaction_cleaned()

    def test_checkpoint_harness_is_not_embedded_in_release_assets(self) -> None:
        assets = self.build("0.1.0")
        installer = (assets / "ava-install.sh").read_text()
        self.assertNotIn("CheckpointReached", installer)
        self.assertNotIn("qualification checkpoint", installer.lower())
        release = json.loads((assets / "ava-release.json").read_text())
        self.assertNotIn("checkpoint.py", {Path(item["source_path"]).name for item in release["installed_files"]})


if __name__ == "__main__":
    unittest.main()
