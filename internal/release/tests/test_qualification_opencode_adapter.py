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
        self.adapter = automation.REPOSITORY_ROOT / "internal/release/qualification-opencode.sh"
        self.env = {
            **os.environ,
            "AVA_QUALIFICATION_OPENCODE": str(self.fake),
            "AVA_TEST_LOG": str(self.log),
        }

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_adapter(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["sh", str(self.adapter), *args],
            env=self.env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

    def test_session_list_uses_unfiltered_database_rows_with_parent_ids(self) -> None:
        result = self.run_adapter("session", "list", "--format", "json")
        rows = json.loads(result.stdout)
        self.assertEqual([row["id"] for row in rows], ["ses_root123", "ses_child456"])
        self.assertEqual(rows[1]["parentID"], "ses_root123")
        call = self.log.read_text(encoding="utf-8").strip()
        self.assertIn("db --format json", call)
        self.assertIn("parent_id AS parentID", call)

    def test_non_inventory_commands_are_forwarded_unchanged(self) -> None:
        result = self.run_adapter("export", "ses_root123")
        self.assertEqual(json.loads(result.stdout), {"session": "exported"})
        self.assertEqual(
            self.log.read_text(encoding="utf-8").strip(),
            "export ses_root123",
        )


if __name__ == "__main__":
    unittest.main()
