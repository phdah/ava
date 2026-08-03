from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
ASSEMBLER = SOURCE_ROOT / "internal/release/assemble.py"
INSTALLER_SOURCE = SOURCE_ROOT / "internal/release/ava-install.sh"
REVISION = "0123456789abcdef0123456789abcdef01234567"
PROJECT_LINK = re.compile(r"(?:\(|`)(\./[^)`\s]+)")


class OpenCodeHostTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.target = self.root / "target"
        self.assets = self.root / "assets"
        self.home = self.root / "home"
        self.target.mkdir()
        self.home.mkdir()
        self._create_repository_fixture()

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _create_repository_fixture(self) -> None:
        release = self.repo / "internal/release"
        release.mkdir(parents=True)
        shutil.copyfile(ASSEMBLER, release / "assemble.py")
        shutil.copyfile(INSTALLER_SOURCE, release / "ava-install.sh")
        shutil.copytree(SOURCE_ROOT / "internal/release/installer", release / "installer")
        shutil.copytree(SOURCE_ROOT / "templates/base", self.repo / "templates/base")
        shutil.copytree(
            SOURCE_ROOT / "templates/project-scaffolds",
            self.repo / "templates/project-scaffolds",
        )

    def run_command(
        self,
        *args: str,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
        timeout: int = 60,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            args,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        if result.returncode != 0:
            self.fail(
                f"command failed ({result.returncode}): {' '.join(args)}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

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

    def install(self, assets: Path) -> None:
        self.run_command(
            "sh",
            str(assets / "ava-install.sh"),
            "--target",
            str(self.target),
            "--asset-dir",
            str(assets),
        )

    def test_clean_install_uses_native_agents_without_opencode_config(self) -> None:
        self.install(self.build("0.1.0"))

        self.assertTrue((self.target / "AGENTS.md").is_file())
        self.assertTrue((self.target / ".ava/state/manifest.json").is_file())
        self.assertFalse((self.target / "opencode.json").exists())
        self.assertFalse((self.target / "opencode.jsonc").exists())
        self.assertFalse((self.target / ".opencode").exists())

        manifest = json.loads((self.target / ".ava/state/manifest.json").read_text())
        self.assertIsNone(manifest["host_integration"])

    def test_project_and_global_opencode_config_survive_install_and_upgrade(self) -> None:
        project_json = b'{"permission":{"edit":"ask"}}\n'
        project_jsonc = b'{\n  // project-owned\n  "share": "disabled"\n}\n'
        global_config = b'{"permission":{"bash":"deny"}}\n'

        (self.target / "opencode.json").write_bytes(project_json)
        (self.target / "opencode.jsonc").write_bytes(project_jsonc)
        global_path = self.home / ".config/opencode/opencode.json"
        global_path.parent.mkdir(parents=True)
        global_path.write_bytes(global_config)

        self.install(self.build("0.1.0"))
        router = self.repo / "templates/base/AGENTS.md"
        router.write_text(router.read_text() + "\n")
        self.install(self.build("0.2.0", upgrade_from="0.1.0"))

        self.assertEqual((self.target / "opencode.json").read_bytes(), project_json)
        self.assertEqual((self.target / "opencode.jsonc").read_bytes(), project_jsonc)
        self.assertEqual(global_path.read_bytes(), global_config)

    def test_installed_router_paths_are_project_local_and_resolvable(self) -> None:
        self.install(self.build("0.1.0"))
        router = (self.target / "AGENTS.md").read_text()
        links = sorted(set(PROJECT_LINK.findall(router)))
        managed_links = [link for link in links if link.startswith("./.ava/")]

        self.assertGreater(len(managed_links), 5)
        for link in managed_links:
            path = (self.target / link[2:]).resolve()
            self.assertTrue(path.is_relative_to(self.target.resolve()), link)
            self.assertTrue(path.is_file(), link)

    def test_host_neutral_router_fixture_uses_same_relative_paths(self) -> None:
        self.install(self.build("0.1.0"))
        router = (self.target / "AGENTS.md").read_text()

        resolved = []
        for link in sorted(set(PROJECT_LINK.findall(router))):
            path = (self.target / link[2:]).resolve()
            if path.exists():
                resolved.append(path)

        self.assertIn((self.target / ".ava/state/manifest.json").resolve(), resolved)
        self.assertIn(
            (self.target / ".ava/base/shared/instructions/instruction-resolution.md").resolve(),
            resolved,
        )

    @unittest.skipUnless(
        os.environ.get("AVA_OPENCODE_LIVE") == "1",
        "set AVA_OPENCODE_LIVE=1 after installing the pinned OpenCode CLI",
    )
    def test_real_opencode_starts_from_installed_project_without_setup(self) -> None:
        executable = shutil.which("opencode")
        self.assertIsNotNone(executable, "opencode is not installed")
        self.install(self.build("0.1.0"))

        env = os.environ.copy()
        env.update(
            {
                "HOME": str(self.home),
                "XDG_CONFIG_HOME": str(self.home / ".config"),
                "XDG_DATA_HOME": str(self.home / ".local/share"),
                "XDG_CACHE_HOME": str(self.home / ".cache"),
                "OPENCODE_DISABLE_CLAUDE_CODE": "1",
            }
        )
        self.run_command(
            executable or "opencode",
            "debug",
            "config",
            cwd=self.target,
            env=env,
            timeout=120,
        )

        self.assertFalse((self.target / "opencode.json").exists())
        self.assertFalse((self.target / "opencode.jsonc").exists())
        self.assertTrue((self.target / ".ava/base/index.md").is_file())


if __name__ == "__main__":
    unittest.main()
