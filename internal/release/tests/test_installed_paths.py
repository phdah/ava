from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

SOURCE_ROOT = Path(__file__).resolve().parents[3]
VALIDATOR_PATH = SOURCE_ROOT / "internal/release/validate-installed-paths.py"

spec = importlib.util.spec_from_file_location("validate_installed_paths", VALIDATOR_PATH)
assert spec and spec.loader
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


def schema_accepts(definition: dict[str, Any], value: str) -> bool:
    if re.fullmatch(definition["pattern"], value) is None:
        return False
    excluded = definition.get("not", {}).get("anyOf", [])
    return not any(re.search(item["pattern"], value) for item in excluded)


class InstalledPathTests(unittest.TestCase):
    def test_distributed_sources_have_no_ambiguous_absolute_paths(self) -> None:
        self.assertEqual(validator.ambiguous_findings(SOURCE_ROOT), [])

    def test_root_router_project_paths_resolve(self) -> None:
        self.assertEqual(validator.unresolved_router_paths(SOURCE_ROOT), [])

    def test_root_router_inline_code_paths_are_validated(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "templates/base").mkdir(parents=True)
            (root / "templates/project-scaffolds").mkdir(parents=True)
            (root / "templates/base/AGENTS.md").write_text(
                "Read `./.ava/base/shared/missing.md`.\n"
            )
            self.assertEqual(
                validator.unresolved_router_paths(root),
                ["./.ava/base/shared/missing.md"],
            )

    def test_regression_reference_is_explicitly_project_relative(self) -> None:
        router = (SOURCE_ROOT / "templates/base/AGENTS.md").read_text()
        expected = "./.ava/base/shared/instructions/upgrade-state-and-routing.md"
        self.assertIn(expected, router)
        self.assertNotRegex(
            router,
            r"(?<!\.)/\.ava/base/shared/instructions/upgrade-state-and-routing\.md",
        )

    def test_ambiguous_reference_blocks_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "templates/base/roles").mkdir(parents=True)
            (root / "templates/project-scaffolds").mkdir(parents=True)
            (root / "templates/base/AGENTS.md").write_text(
                "Read [state](/.ava/base/shared/instructions/upgrade-state-and-routing.md).\n"
            )
            findings = validator.ambiguous_findings(root)
            self.assertEqual(len(findings), 1)
            self.assertEqual(findings[0].token, "/.ava")

    def test_document_relative_links_are_not_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "templates/base/roles").mkdir(parents=True)
            (root / "templates/project-scaffolds").mkdir(parents=True)
            (root / "templates/base/AGENTS.md").write_text(
                "Read [root](../../AGENTS.md) and [index](../index.md).\n"
            )
            self.assertEqual(validator.ambiguous_findings(root), [])

    def test_manifest_schema_path_contracts(self) -> None:
        schema = json.loads(
            (SOURCE_ROOT / "distribution/schemas/manifest.schema.json").read_text()
        )
        project_path = schema["$defs"]["projectPath"]
        payload_path = schema["$defs"]["payloadFile"]["properties"]["path"]

        self.assertTrue(schema_accepts(project_path, "./CODEX.md"))
        for invalid in (
            "CODEX.md",
            "/CODEX.md",
            "./AGENTS.md",
            "./.ava/host.md",
            "./../CODEX.md",
            "./folder\\CODEX.md",
            "./folder\x00CODEX.md",
        ):
            self.assertFalse(schema_accepts(project_path, invalid), invalid)

        self.assertTrue(schema_accepts(payload_path, "/AGENTS.md"))
        for invalid in ("AGENTS.md", "/../AGENTS.md", "/folder\\file.md", "/folder\x00file.md"):
            self.assertFalse(schema_accepts(payload_path, invalid), invalid)

    def test_manifest_paths_remain_machine_identifiers(self) -> None:
        schema = (SOURCE_ROOT / "distribution/schemas/manifest.schema.json").read_text()
        self.assertIn('"const": "/AGENTS.md"', schema)
        self.assertIn('"const": "/.ava/state/manifest.json"', schema)

    def test_host_entrypoint_uses_explicit_project_root_form(self) -> None:
        schema = (SOURCE_ROOT / "distribution/schemas/manifest.schema.json").read_text()
        self.assertIn('"pattern": "^\\\\./', schema)


if __name__ == "__main__":
    unittest.main()
