from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from internal.release.tests.test_installer import InstallerTests


class InstallerConformanceTests(unittest.TestCase):
    _create_repository_fixture = InstallerTests._create_repository_fixture
    run_command = InstallerTests.run_command
    build = InstallerTests.build
    install = InstallerTests.install
    manifest = InstallerTests.manifest
    journal = InstallerTests.journal
    setUp = InstallerTests.setUp
    tearDown = InstallerTests.tearDown

    def test_unknown_historical_ava_layout_is_refused(self) -> None:
        (self.target / ".ava").mkdir()
        (self.target / ".ava/legacy.md").write_text("legacy\n")

        failed = self.install(self.build("0.1.0"), check=False)

        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("UNRECOGNIZED_AVA", failed.stderr)
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertEqual((self.target / ".ava/legacy.md").read_text(), "legacy\n")

    def test_dry_run_does_not_mutate_target(self) -> None:
        existing = self.target / "project.txt"
        existing.write_text("project-owned\n")

        result = self.install(self.build("0.1.0"), "--dry-run")

        self.assertEqual(existing.read_text(), "project-owned\n")
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / ".ava").exists())
        self.assertIn("CREATE", result.stdout)

    def test_apply_failure_restores_grouped_changes(self) -> None:
        fragment = self.repo / "internal/release/installer/06.py"
        source = fragment.read_text()
        marker = "        for scaffold in scaffolds:\n"
        self.assertIn(marker, source)
        fragment.write_text(
            source.replace(
                marker,
                '        raise OSError("injected grouped apply failure")\n' + marker,
                1,
            )
        )
        project_file = self.target / "project.txt"
        project_file.write_text("preserve\n")

        failed = self.install(self.build("0.1.0"), check=False)

        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("injected grouped apply failure", failed.stderr)
        self.assertEqual(project_file.read_text(), "preserve\n")
        self.assertFalse((self.target / "AGENTS.md").exists())
        self.assertFalse((self.target / ".ava").exists())
        self.assertFalse((self.target / ".ava-install").exists())

    def test_failed_migration_does_not_publish_candidate(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        source_manifest = (self.target / ".ava/state/manifest.json").read_bytes()
        source_router = (self.target / "AGENTS.md").read_bytes()

        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        migrations = self.root / "failing-migrations"
        (migrations / "steps").mkdir(parents=True)
        payload = migrations / "steps/router.txt"
        payload.write_text("# Router 0.2.0\n")
        (migrations / "steps/apply.json").write_text(
            json.dumps(
                {
                    "operations": [
                        {
                            "operation": "write",
                            "path": "/AGENTS.md",
                            "source": "steps/router.txt",
                        }
                    ]
                }
            )
        )
        (migrations / "steps/verify.json").write_text(
            json.dumps(
                {
                    "checks": [
                        {
                            "path": "/AGENTS.md",
                            "exists": True,
                            "sha256": hashlib.sha256(b"not the router").hexdigest(),
                        }
                    ]
                }
            )
        )
        (migrations / "router.json").write_text(
            json.dumps(
                {
                    "id": "failing-router",
                    "from": "0.1.0",
                    "to": "0.2.0",
                    "order": 0,
                    "depends_on": [],
                    "apply_path": "steps/apply.json",
                    "verify_path": "steps/verify.json",
                    "idempotent": True,
                }
            )
        )
        second = self.build(
            "0.2.0",
            upgrade_from=["0.1.0"],
            migrations_dir=migrations,
        )

        failed = self.install(second, check=False)

        self.assertNotEqual(failed.returncode, 0)
        self.assertEqual((self.target / ".ava/state/manifest.json").read_bytes(), source_manifest)
        self.assertEqual((self.target / "AGENTS.md").read_bytes(), source_router)
        self.assertEqual(self.manifest()["ava_version"], "0.1.0")

    def test_exact_version_must_match_release_assets(self) -> None:
        assets = self.build("0.1.0")

        failed = self.run_command(
            "sh",
            str(assets / "ava-install.sh"),
            "--target",
            str(self.target),
            "--asset-dir",
            str(assets),
            "--version",
            "0.2.0",
            check=False,
        )

        self.assertNotEqual(failed.returncode, 0)
        self.assertFalse((self.target / ".ava").exists())
        self.assertFalse((self.target / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
