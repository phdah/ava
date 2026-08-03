from __future__ import annotations

import hashlib
import io
import json
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
ASSEMBLER = SOURCE_ROOT / "internal/release/assemble.py"
INSTALLER_SOURCE = SOURCE_ROOT / "internal/release/ava-install.sh"
REVISION = "0123456789abcdef0123456789abcdef01234567"


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.target = self.root / "target"
        self.assets = self.root / "assets"
        self.target.mkdir()
        self._create_repository_fixture()

    def tearDown(self) -> None:
        self.temp.cleanup()

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

    def run_command(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(args, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check and result.returncode != 0:
            self.fail(
                f"command failed ({result.returncode}): {' '.join(args)}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    def build(
        self,
        version: str,
        *,
        upgrade_from: list[str] | None = None,
        semantic: bool = False,
        guidance: bool = False,
        migrations_dir: Path | None = None,
        destination: Path | None = None,
    ) -> Path:
        output = destination or self.assets / f"v{version}"
        output.mkdir(parents=True, exist_ok=True)
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
        for source in upgrade_from or []:
            args.extend(("--upgrade-from", source))
        if semantic:
            args.append("--semantic-review-required")
        if guidance:
            guidance_dir = self.root / f"guidance-{version}"
            guidance_dir.mkdir()
            (guidance_dir / "UPGRADE.md").write_text(f"# Upgrade to {version}\n")
            args.extend(("--guidance-dir", str(guidance_dir)))
        if migrations_dir:
            args.extend(("--migrations-dir", str(migrations_dir)))
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

    def manifest(self) -> dict:
        return json.loads((self.target / ".ava/state/manifest.json").read_text())

    def journal(self) -> dict:
        return json.loads((self.target / ".ava/state/upgrade.json").read_text())

    def test_clean_install_preserves_existing_project_content(self) -> None:
        assets = self.build("0.1.0")
        (self.target / "knowledge").mkdir()
        (self.target / "knowledge/index.md").write_text("# Existing knowledge\n")
        self.install(assets)
        self.assertEqual(self.manifest()["ava_version"], "0.1.0")
        self.assertEqual((self.target / "knowledge/index.md").read_text(), "# Existing knowledge\n")
        managed = {item["path"] for item in self.manifest()["managed_files"]}
        self.assertNotIn("/knowledge/index.md", managed)
        self.assertIsNone(self.manifest()["host_integration"])
        self.assertEqual(self.journal()["status"], "idle")

    def test_existing_agents_requires_explicit_adoption(self) -> None:
        assets = self.build("0.1.0")
        (self.target / "AGENTS.md").write_text("# Existing project router\n")
        failed = self.install(assets, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("PATH_COLLISION", failed.stderr)
        self.install(assets, "--adopt-existing-agents")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.1.0\n")

    def test_modified_managed_file_blocks_upgrade(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        (self.target / "AGENTS.md").write_text("modified\n")
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        second = self.build("0.2.0", upgrade_from=["0.1.0"])
        failed = self.install(second, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("MANAGED_CONFLICT", failed.stderr)
        self.assertEqual(self.manifest()["ava_version"], "0.1.0")

    def test_semantic_upgrade_blocks_then_rolls_back(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        second = self.build("0.2.0", upgrade_from=["0.1.0"], semantic=True, guidance=True)
        self.install(second)
        self.assertEqual(self.manifest()["semantic_compatibility"]["status"], "pending")
        self.assertEqual(self.journal()["stage"], "semantic")
        self.install(second, "--rollback")
        self.assertEqual(self.manifest()["ava_version"], "0.1.0")
        self.assertEqual(self.journal()["status"], "rolled-back")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.1.0\n")

    def test_rollback_rejects_post_upgrade_managed_edit(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        second = self.build("0.2.0", upgrade_from=["0.1.0"], semantic=True, guidance=True)
        self.install(second)
        (self.target / "AGENTS.md").write_text("changed after upgrade\n")
        failed = self.install(second, "--rollback", check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("ROLLBACK_CONFLICT", failed.stderr)

    def test_checksum_failure_precedes_mutation(self) -> None:
        assets = self.build("0.1.0")
        with (assets / "ava-base.tar.gz").open("ab") as handle:
            handle.write(b"corruption")
        failed = self.install(assets, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("CHECKSUM_MISMATCH", failed.stderr)
        self.assertFalse((self.target / ".ava").exists())
        self.assertFalse((self.target / "AGENTS.md").exists())

    def test_unsafe_archive_entry_is_rejected(self) -> None:
        assets = self.build("0.1.0")
        archive = assets / "ava-base.tar.gz"
        rebuilt = assets / "rebuilt.tar.gz"
        with tarfile.open(archive, "r:gz") as source, tarfile.open(rebuilt, "w:gz") as target:
            for member in source.getmembers():
                fileobj = source.extractfile(member) if member.isfile() else None
                target.addfile(member, fileobj)
            payload = b"escape"
            info = tarfile.TarInfo("../outside")
            info.size = len(payload)
            target.addfile(info, io.BytesIO(payload))
        rebuilt.replace(archive)
        self._refresh_asset_metadata(assets, "ava-base.tar.gz")
        failed = self.install(assets, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("UNSAFE_PATH", failed.stderr)
        self.assertFalse((self.root / "outside").exists())

    def _refresh_asset_metadata(self, assets: Path, changed_name: str) -> None:
        manifest_path = assets / "ava-release.json"
        manifest = json.loads(manifest_path.read_text())
        path = assets / changed_name
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        for item in manifest["assets"]:
            if item["name"] == changed_name:
                item["sha256"] = digest
                item["size"] = path.stat().st_size
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        lines = []
        for name in (
            "ava-install.sh",
            "ava-base.tar.gz",
            "ava-guidance.tar.gz",
            "ava-migrations.tar.gz",
            "ava-release.json",
            "ava-release-notes.md",
        ):
            lines.append(f"{hashlib.sha256((assets / name).read_bytes()).hexdigest()}  {name}\n")
        (assets / "SHA256SUMS").write_text("".join(lines))

    def test_declarative_migration_executes_inside_candidate_tree(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        migrations = self.root / "migrations"
        (migrations / "steps").mkdir(parents=True)
        (migrations / "steps/router.txt").write_text("# Router 0.2.0\n")
        router_sha = hashlib.sha256((migrations / "steps/router.txt").read_bytes()).hexdigest()
        (migrations / "steps/apply.json").write_text(
            json.dumps({"operations": [{"operation": "write", "path": "/AGENTS.md", "source": "steps/router.txt"}]})
        )
        (migrations / "steps/verify.json").write_text(
            json.dumps({"checks": [{"path": "/AGENTS.md", "exists": True, "sha256": router_sha}]})
        )
        (migrations / "router.json").write_text(
            json.dumps(
                {
                    "id": "rewrite-router",
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
        second = self.build("0.2.0", upgrade_from=["0.1.0"], migrations_dir=migrations)
        self.install(second)
        self.assertEqual(self.manifest()["ava_version"], "0.2.0")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.2.0\n")

    def test_project_owned_host_entrypoint_is_recorded_not_managed(self) -> None:
        content = "Read and follow ./AGENTS.md.\nAdditional project instructions remain here.\n"
        (self.target / "CODEX.md").write_text(content)
        assets = self.build("0.1.0")
        self.install(assets, "--host-entrypoint", "CODEX.md")
        self.assertEqual((self.target / "CODEX.md").read_text(), content)
        self.assertEqual(
            self.manifest()["host_integration"],
            {
                "entrypoint": "./CODEX.md",
                "ownership": "project-owned",
                "discovery": "project-provided",
            },
        )
        managed = {item["path"] for item in self.manifest()["managed_files"]}
        self.assertNotIn("/CODEX.md", managed)
        release = json.loads((assets / "ava-release.json").read_text())
        self.assertNotIn("/CODEX.md", {item["destination"] for item in release["installed_files"]})

    def test_host_entrypoint_is_preserved_across_upgrade(self) -> None:
        (self.target / ".github").mkdir()
        entrypoint = self.target / ".github/copilot-instructions.md"
        entrypoint.write_text("Read ../../AGENTS.md.\n")
        first = self.build("0.1.0")
        self.install(first, "--host-entrypoint", ".github/copilot-instructions.md")
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        second = self.build("0.2.0", upgrade_from=["0.1.0"])
        self.install(second)
        self.assertEqual(
            self.manifest()["host_integration"]["entrypoint"],
            "./.github/copilot-instructions.md",
        )
        self.assertEqual(entrypoint.read_text(), "Read ../../AGENTS.md.\n")

    def test_invalid_host_entrypoint_is_rejected_without_mutation(self) -> None:
        assets = self.build("0.1.0")
        missing = self.install(assets, "--host-entrypoint", "CODEX.md", check=False)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("INVALID_HOST_ENTRYPOINT", missing.stderr)
        reserved = self.install(assets, "--host-entrypoint", ".ava/host.md", check=False)
        self.assertNotEqual(reserved.returncode, 0)
        self.assertIn("INVALID_HOST_ENTRYPOINT", reserved.stderr)
        absolute = self.install(assets, "--host-entrypoint", "/tmp/CODEX.md", check=False)
        self.assertNotEqual(absolute.returncode, 0)
        self.assertIn("INVALID_HOST_ENTRYPOINT", absolute.stderr)
        self.assertFalse((self.target / ".ava").exists())
        self.assertFalse((self.target / "AGENTS.md").exists())

    def test_chained_upgrade_verifies_each_adjacent_edge(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        self.build("0.2.0", upgrade_from=["0.1.0"])
        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.3.0\n")
        third = self.build("0.3.0", upgrade_from=["0.1.0:0.2.0", "0.2.0"])
        self.install(third)
        self.assertEqual(self.manifest()["ava_version"], "0.3.0")
        self.assertEqual((self.target / "AGENTS.md").read_text(), "# Router 0.3.0\n")

    def test_symlink_scaffold_escape_is_rejected(self) -> None:
        assets = self.build("0.1.0")
        outside = self.root / "outside"
        outside.mkdir()
        (self.target / "knowledge").symlink_to(outside, target_is_directory=True)
        failed = self.install(assets, check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("SYMLINK_ESCAPE", failed.stderr)
        self.assertEqual(list(outside.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
