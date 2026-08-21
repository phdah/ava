from __future__ import annotations

import datetime
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_automation as automation


class AssembleCandidateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        (self.repo / "internal/release/catalogs").mkdir(parents=True)

        source = automation.REPOSITORY_ROOT / "internal/release/assemble-candidate.sh"
        self.script = self.repo / "internal/release/assemble-candidate.sh"
        shutil.copy2(source, self.script)
        self.script.chmod(0o755)

        self.capture = self.root / "assemble-args.txt"
        assembler = self.repo / "internal/release/assemble.sh"
        assembler.write_text(
            "#!/bin/sh\n"
            "set -eu\n"
            "printf '%s\\n' \"$AVA_UPGRADE_CATALOG\" > \"$AVA_TEST_CAPTURE\"\n"
            "printf '%s\\n' \"$@\" >> \"$AVA_TEST_CAPTURE\"\n"
            "while [ \"$#\" -gt 0 ]; do\n"
            "  if [ \"$1\" = --output ]; then\n"
            "    mkdir -p \"$2\"\n"
            "    break\n"
            "  fi\n"
            "  shift\n"
            "done\n"
            "printf '%s\\n' 'fake candidate assembled' >&2\n",
            encoding="utf-8",
        )
        assembler.chmod(0o755)

        (self.repo / "version.txt").write_text("1.0.0-alpha.15\n", encoding="utf-8")
        (self.repo / "CHANGELOG.md").write_text("# Changes\n", encoding="utf-8")
        (self.repo / "internal/release/catalogs/1.0.0-alpha.15.json").write_text(
            "{}\n", encoding="utf-8"
        )

        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Ava Tests")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

        self.candidate_root = self.root / "candidates"
        self.env = {
            **os.environ,
            "AVA_CANDIDATE_ROOT": str(self.candidate_root),
            "AVA_TEST_CAPTURE": str(self.capture),
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        ).stdout.strip()

    def run_script(self, *, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [str(self.script)],
            cwd=self.repo,
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=check,
        )

    def test_derives_candidate_identity_and_prints_only_output_path(self) -> None:
        revision = self.git("rev-parse", "HEAD")
        epoch = int(self.git("show", "-s", "--format=%ct", revision))
        published_at = datetime.datetime.fromtimestamp(
            epoch, datetime.timezone.utc
        ).isoformat().replace("+00:00", "Z")

        result = self.run_script()
        expected_output = self.candidate_root / f"ava-1.0.0-alpha.15-{revision[:7]}"
        self.assertEqual(result.stdout.strip(), str(expected_output.resolve()))
        self.assertTrue(expected_output.is_dir())

        captured = self.capture.read_text(encoding="utf-8").splitlines()
        self.assertEqual(
            captured[0],
            str((self.repo / "internal/release/catalogs/1.0.0-alpha.15.json").resolve()),
        )
        arguments = captured[1:]
        for expected in (
            "--output",
            str(expected_output.resolve()),
            "--version",
            "1.0.0-alpha.15",
            "--channel",
            "alpha",
            "--source-revision",
            revision,
            "--source-date-epoch",
            str(epoch),
            "--published-at",
            published_at,
            "--release-notes",
            str((self.repo / "CHANGELOG.md").resolve()),
        ):
            self.assertIn(expected, arguments)

    def test_refuses_dirty_checkout(self) -> None:
        (self.repo / "dirty.txt").write_text("dirty\n", encoding="utf-8")
        result = self.run_script(check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be clean", result.stderr)
        self.assertFalse(self.capture.exists())

    def test_refuses_reusing_existing_candidate_directory(self) -> None:
        first = self.run_script()
        self.assertEqual(first.returncode, 0)
        second = self.run_script(check=False)
        self.assertNotEqual(second.returncode, 0)
        self.assertIn("already exists", second.stderr)


if __name__ == "__main__":
    unittest.main()
