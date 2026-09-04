from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release.conformance_release import validate_release

SOURCE_ROOT = Path(__file__).resolve().parents[3]
ASSEMBLER = SOURCE_ROOT / "internal/release/assemble.py"
INSTALLER_SOURCE = SOURCE_ROOT / "internal/release/ava-install.sh"
INSTALLER_FRAGMENTS = SOURCE_ROOT / "internal/release/installer"
REVISION = "0123456789abcdef0123456789abcdef01234567"


class AssemblyContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self._create_repository_fixture()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _create_repository_fixture(self) -> None:
        release_root = self.repo / "internal/release"
        release_root.mkdir(parents=True)
        shutil.copyfile(ASSEMBLER, release_root / "assemble.py")
        shutil.copyfile(INSTALLER_SOURCE, release_root / "ava-install.sh")
        shutil.copytree(INSTALLER_FRAGMENTS, release_root / "installer")

        base = self.repo / "templates/base"
        for directory in ("roles", "workflows", "shared/instructions"):
            (base / directory).mkdir(parents=True, exist_ok=True)
        (base / "AGENTS.md").write_text("# Router\n", encoding="utf-8")
        (base / "index.md").write_text("# Base\n", encoding="utf-8")
        (base / "roles/index.md").write_text("# Roles\n", encoding="utf-8")
        (base / "workflows/index.md").write_text("# Workflows\n", encoding="utf-8")
        (base / "shared/index.md").write_text("# Shared\n", encoding="utf-8")
        (base / "shared/instructions/test.md").write_text("# Test\n", encoding="utf-8")

        scaffolds = self.repo / "templates/project-scaffolds"
        for directory in ("roles", "workflows", "shared", "knowledge", "inbox/processed"):
            (scaffolds / directory).mkdir(parents=True, exist_ok=True)
        (scaffolds / "index.md").write_text("# Project\n", encoding="utf-8")
        for directory in ("roles", "workflows", "shared", "knowledge", "inbox"):
            (scaffolds / directory / "index.md").write_text(
                f"# {directory}\n", encoding="utf-8"
            )
        (scaffolds / "inbox/processed/index.md").write_text(
            "# Processed\n", encoding="utf-8"
        )

    def _build(
        self,
        version: str,
        destination: Path,
        *,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        destination.mkdir(parents=True, exist_ok=True)
        result = subprocess.run(
            [
                "python3",
                str(self.repo / "internal/release/assemble.py"),
                "--root",
                str(self.repo),
                "--output",
                str(destination),
                "--version",
                version,
                "--source-revision",
                REVISION,
                "--source-date-epoch",
                "1700000000",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if check and result.returncode != 0:
            self.fail(
                f"assembly failed ({result.returncode})\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def test_destination_mapping_rejects_missing_installed_link(self) -> None:
        base = self.repo / "templates/base"
        (base / "inbox").mkdir()
        source_target = base / "inbox/index.md"
        source_target.write_text("# Source-only inbox\n", encoding="utf-8")
        role_directory = base / "roles/inbox-ingester"
        role_directory.mkdir()
        role_index = role_directory / "index.md"
        role_index.write_text(
            "# Inbox Ingester\n\n[Inbox](../../inbox/index.md)\n",
            encoding="utf-8",
        )

        result = self._build("1.0.0-alpha.1", self.root / "broken-links", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unresolved installed Markdown links", result.stderr)
        self.assertIn("/.ava/base/inbox/index.md", result.stderr)

        role_index.write_text(
            role_index.read_text(encoding="utf-8").replace(
                "../../inbox/index.md", "./inbox/index.md"
            ),
            encoding="utf-8",
        )
        self._build("1.0.0-alpha.1", self.root / "resolved-links")

    def test_installed_link_rejects_root_escape(self) -> None:
        base = self.repo / "templates/base"
        role_directory = base / "roles/test-role"
        role_directory.mkdir()
        role_index = role_directory / "index.md"

        for target, output in (
            ("../../../../../AGENTS.md", "document-escape"),
            ("./../AGENTS.md", "project-escape"),
        ):
            with self.subTest(target=target):
                role_index.write_text(
                    f"# Test role\n\n[Router]({target})\n", encoding="utf-8"
                )
                result = self._build(
                    "1.0.0-alpha.1", self.root / output, check=False
                )
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("<outside installed project>", result.stderr)

    def test_non_first_release_requires_upgrade_edges(self) -> None:
        output = self.root / "no-edges"
        self._build("1.0.0-alpha.2", output)
        result = validate_release(output)
        self.assertIn(
            "AVA-RELEASE-UPGRADE-EDGES",
            {finding.rule_id for finding in result.findings},
        )


if __name__ == "__main__":
    unittest.main()
