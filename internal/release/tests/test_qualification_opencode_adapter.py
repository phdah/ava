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
        self.config_log = self.root / "config.log"
        self.fake = self.root / "opencode"
        self.fake.write_text(
            "#!/bin/sh\n"
            "set -eu\n"
            "printf '%s\\n' \"$*\" >> \"$AVA_TEST_LOG\"\n"
            "printf '%s\\n' \"${OPENCODE_CONFIG_CONTENT-}\" >> \"$AVA_TEST_CONFIG_LOG\"\n"
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
            "AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS": json.dumps(["/tmp/root"]),
            "AVA_TEST_LOG": str(self.log),
            "AVA_TEST_CONFIG_LOG": str(self.config_log),
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

    def test_repository_opencode_config_tracks_tmp_permission(self) -> None:
        config_path = automation.REPOSITORY_ROOT / "opencode.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        self.assertEqual(
            config,
            {
                "$schema": "https://opencode.ai/config.json",
                "permission": {"external_directory": {"/tmp/**": "allow"}},
            },
        )
        ignored = {
            line.strip()
            for line in (automation.REPOSITORY_ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        self.assertNotIn("opencode.json", ignored)

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
        config = json.loads(self.config_log.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(
            config["permission"]["external_directory"]["/tmp/root/**"],
            "allow",
        )

    def test_run_preserves_existing_inline_config_and_appends_exact_roots(self) -> None:
        run_root = self.root / "qualification-run"
        target_assets = self.root / "target-assets"
        existing = {
            "model": "openai/example",
            "permission": {
                "bash": "ask",
                "external_directory": {
                    "*": "deny",
                    "/tmp/other/**": "allow",
                },
            },
        }
        env = {
            **self.env,
            "OPENCODE_CONFIG_CONTENT": json.dumps(existing),
            "AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS": json.dumps(
                [str(run_root), str(target_assets)]
            ),
        }
        self.run_adapter("run", "--dir", str(run_root), "Audit this run.", env=env)
        config = json.loads(self.config_log.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(config["model"], "openai/example")
        self.assertEqual(config["permission"]["bash"], "ask")
        external = config["permission"]["external_directory"]
        self.assertEqual(external["*"], "deny")
        self.assertEqual(external["/tmp/other/**"], "allow")
        self.assertEqual(external[f"{run_root.resolve().as_posix()}/**"], "allow")
        self.assertEqual(external[f"{target_assets.resolve().as_posix()}/**"], "allow")
        self.assertEqual(
            list(external)[-2:],
            [
                f"{run_root.resolve().as_posix()}/**",
                f"{target_assets.resolve().as_posix()}/**",
            ],
        )

    def test_run_preserves_scalar_permission_as_default(self) -> None:
        env = {
            **self.env,
            "OPENCODE_CONFIG_CONTENT": json.dumps({"permission": "deny"}),
        }
        self.run_adapter("run", "--dir", "/tmp/root", "Audit this run.", env=env)
        config = json.loads(self.config_log.read_text(encoding="utf-8").splitlines()[-1])
        self.assertEqual(config["permission"]["*"], "deny")
        self.assertEqual(
            config["permission"]["external_directory"]["/tmp/root/**"],
            "allow",
        )

    def test_run_requires_qualification_owned_external_root_scope(self) -> None:
        env = {**self.env}
        env.pop("AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS")
        result = subprocess.run(
            ["sh", str(self.adapter), "run", "--dir", "/tmp/root", "Audit this run."],
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS", result.stderr)
        self.assertFalse(self.log.exists())

    def test_audit_style_run_receives_permission_for_generated_evidence_root(self) -> None:
        evidence_root = self.root / "evidence"
        evidence_root.mkdir()
        (evidence_root / "summary.json").write_text('{"outcome":"pass"}\n', encoding="utf-8")
        guard = self.root / "opencode-permission-guard"
        guard.write_text(
            "#!/usr/bin/env python3\n"
            "import json\n"
            "import os\n"
            "from pathlib import Path\n"
            "root = Path(os.environ['AVA_TEST_REQUIRED_ROOT']).resolve()\n"
            "config = json.loads(os.environ['OPENCODE_CONFIG_CONTENT'])\n"
            "pattern = f'{root.as_posix()}/**'\n"
            "if config['permission']['external_directory'].get(pattern) != 'allow':\n"
            "    raise SystemExit('missing exact external-directory permission')\n"
            "print((root / 'summary.json').read_text(encoding='utf-8').strip())\n",
            encoding="utf-8",
        )
        guard.chmod(0o755)
        env = {
            **self.env,
            "AVA_QUALIFICATION_OPENCODE": str(guard),
            "AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS": json.dumps([str(evidence_root)]),
            "AVA_TEST_REQUIRED_ROOT": str(evidence_root),
        }
        env.pop("OPENCODE_CONFIG_CONTENT", None)
        result = self.run_adapter(
            "run",
            "--dir",
            str(automation.REPOSITORY_ROOT),
            "--model",
            "openai/gpt-5.6-sol",
            "Audit the generated evidence.",
            env=env,
        )
        self.assertEqual(json.loads(result.stdout), {"outcome": "pass"})

    def test_qualify_release_wires_unique_operation_scope_into_adapter(self) -> None:
        source = (automation.REPOSITORY_ROOT / "internal/release/qualify-release.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("ava-qualification-operation.XXXXXX", source)
        self.assertIn("AVA_QUALIFICATION_OPENCODE_EXTERNAL_ROOTS", source)
        self.assertIn('set -- "$@" --run-root-parent "$operation_parent"', source)
        self.assertIn('"$source_assets" "$target_assets"', source)

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
