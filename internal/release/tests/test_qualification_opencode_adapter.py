from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_automation as automation


class QualificationOpenCodeAdapterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.log = self.root / "calls.log"
        self.fake = self.root / "opencode"
        self.fake.write_text(
            "#!/bin/sh\n"
            "set -eu\n"
            "printf '%s\\n' \"$*\" >> \"$AVA_TEST_LOG\"\n"
            "if [ \"${1:-}\" = db ]; then\n"
            "  printf '%s\\n' '[{\"id\":\"ses_root123\",\"parentID\":null,\"directory\":\"/tmp/root\"},{\"id\":\"ses_child456\",\"parentID\":\"ses_root123\",\"directory\":\"/tmp/root\"}]'\n"
            "elif [ \"${1:-}\" = export ]; then\n"
            "  printf '%s\\n' '{\"session\":\"exported\"}'\n"
            "else\n"
            "  printf '%s\\n' 'forwarded'\n"
            "fi\n",
            encoding="utf-8",
        )
        self.fake.chmod(0o755)
        self.pipe_sensitive_fake = self.root / "opencode-pipe-sensitive"
        self.pipe_sensitive_fake.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "import os\n"
            "import stat\n"
            "import sys\n"
            "if sys.argv[1] == 'db':\n"
            "    payload = [{\"id\": \"ses_large\", \"parentID\": None, \"directory\": \"/tmp/root\", \"padding\": \"x\" * 70000}]\n"
            "elif sys.argv[1] == 'export':\n"
            "    payload = {\"session\": \"exported\", \"padding\": \"x\" * 70000}\n"
            "else:\n"
            "    payload = {\"forwarded\": True}\n"
            "text = json.dumps(payload, separators=(',', ':')) + '\\n'\n"
            "if stat.S_ISFIFO(os.fstat(sys.stdout.fileno()).st_mode):\n"
            "    text = text[:65536]\n"
            "sys.stdout.write(text)\n",
            encoding="utf-8",
        )
        self.pipe_sensitive_fake.chmod(0o755)
        self.adapter = automation.REPOSITORY_ROOT / "internal/release/qualification-opencode.sh"
        self.env = {
            **os.environ,
            "AVA_QUALIFICATION_OPENCODE": str(self.fake),
            "AVA_TEST_LOG": str(self.log),
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_adapter(
        self,
        *args: str,
        env: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(self.adapter), *args],
            env=env or self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    def pipe_sensitive_env(self) -> dict[str, str]:
        return {
            **self.env,
            "AVA_QUALIFICATION_OPENCODE": str(self.pipe_sensitive_fake),
        }

    def test_session_list_uses_unfiltered_database_rows_with_parent_ids(self) -> None:
        result = self.run_adapter("session", "list", "--format", "json")
        rows = json.loads(result.stdout)
        self.assertEqual([row["id"] for row in rows], ["ses_root123", "ses_child456"])
        self.assertEqual(rows[1]["parentID"], "ses_root123")
        call = self.log.read_text(encoding="utf-8").strip()
        self.assertIn("db --format json", call)
        self.assertIn("parent_id AS parentID", call)

    def test_large_session_list_is_buffered_before_opencode_stdout_pipe(self) -> None:
        result = self.run_adapter(
            "session",
            "list",
            "--format",
            "json",
            env=self.pipe_sensitive_env(),
        )
        self.assertGreater(len(result.stdout.encode("utf-8")), 65536)
        rows = json.loads(result.stdout)
        self.assertEqual(rows[0]["id"], "ses_large")
        self.assertEqual(len(rows[0]["padding"]), 70000)

    def test_run_separates_yaml_frontmatter_prompt_from_options(self) -> None:
        prompt = "---\ntype: Internal Release Qualification Audit\n---\nAudit this run."
        result = self.run_adapter(
            "run",
            "--dir",
            "/tmp/root",
            "--model",
            "openai/gpt-5.6-sol",
            "--format",
            "json",
            "--title",
            "Ava qualification independent audit",
            prompt,
        )
        self.assertEqual(result.stdout.strip(), "forwarded")
        call = self.log.read_text(encoding="utf-8")
        self.assertIn("--title Ava qualification independent audit -- ---", call)
        self.assertIn("type: Internal Release Qualification Audit", call)

    def test_export_is_buffered_without_changing_arguments(self) -> None:
        result = self.run_adapter("export", "ses_root123")
        self.assertEqual(json.loads(result.stdout), {"session": "exported"})
        self.assertEqual(
            self.log.read_text(encoding="utf-8").strip(),
            "export ses_root123",
        )

    def test_large_export_is_buffered_before_opencode_stdout_pipe(self) -> None:
        result = self.run_adapter(
            "export",
            "ses_root123",
            env=self.pipe_sensitive_env(),
        )
        self.assertGreater(len(result.stdout.encode("utf-8")), 65536)
        exported = json.loads(result.stdout)
        self.assertEqual(exported["session"], "exported")
        self.assertEqual(len(exported["padding"]), 70000)


if __name__ == "__main__":
    unittest.main()
