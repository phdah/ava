from __future__ import annotations

import json
import unittest

from internal.release.tests.test_installer import InstallerTests


EXPECTED_CONFIG = {
    "$schema": "https://opencode.ai/config.json",
    "permission": {
        "read": {".ava/**": "allow"},
        "edit": {".ava/**": "ask"},
    },
}


class HostConfigurationTests(unittest.TestCase):
    _create_repository_fixture = InstallerTests._create_repository_fixture
    run_command = InstallerTests.run_command
    build = InstallerTests.build
    install = InstallerTests.install
    manifest = InstallerTests.manifest
    setUp = InstallerTests.setUp
    tearDown = InstallerTests.tearDown

    def test_default_install_creates_project_owned_opencode_config(self) -> None:
        result = self.install(self.build("0.1.0"))

        self.assertEqual(
            json.loads((self.target / "opencode.json").read_text()),
            EXPECTED_CONFIG,
        )
        managed = {item["path"] for item in self.manifest()["managed_files"]}
        self.assertNotIn("/opencode.json", managed)
        self.assertIn("project-owned OpenCode configuration", result.stdout)

    def test_host_none_skips_opencode_config(self) -> None:
        self.install(self.build("0.1.0"), "--host", "none")

        self.assertFalse((self.target / "opencode.json").exists())
        self.assertFalse((self.target / "opencode.jsonc").exists())

    def test_existing_opencode_config_is_preserved_and_install_continues(self) -> None:
        existing = b'{\n  // project configuration\n  "share": "disabled"\n}\n'
        (self.target / "opencode.jsonc").write_bytes(existing)

        result = self.install(self.build("0.1.0"))

        self.assertEqual((self.target / "opencode.jsonc").read_bytes(), existing)
        self.assertTrue((self.target / ".ava/state/manifest.json").is_file())
        self.assertIn("already exists", result.stdout)
        self.assertIn('".ava/**": "allow"', result.stdout)

    def test_upgrade_does_not_replace_project_owned_opencode_config(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        customized = b'{"permission":{"read":{".ava/**":"allow"}},"model":"local"}\n'
        (self.target / "opencode.json").write_bytes(customized)

        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        second = self.build("0.2.0", upgrade_from=["0.1.0"])
        self.install(second)

        self.assertEqual((self.target / "opencode.json").read_bytes(), customized)
        self.assertEqual(self.manifest()["ava_version"], "0.2.0")


if __name__ == "__main__":
    unittest.main()
