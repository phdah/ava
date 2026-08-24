from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
ASSEMBLER = SOURCE_ROOT / "internal/release/assemble.py"
INSTALLER_SOURCE = SOURCE_ROOT / "internal/release/ava-install.sh"
REVISION = "0123456789abcdef0123456789abcdef01234567"


class SemanticUpgradeContractTests(unittest.TestCase):
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
        shutil.copytree(
            SOURCE_ROOT / "internal/release/installer",
            self.repo / "internal/release/installer",
        )
        base = self.repo / "templates/base"
        for directory in (
            "roles",
            "workflows",
            "shared/instructions",
            "knowledge",
            "inbox/processed",
        ):
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
        for directory in (
            "roles",
            "workflows",
            "shared",
            "knowledge",
            "inbox/processed",
        ):
            (scaffolds / directory).mkdir(parents=True, exist_ok=True)
        (scaffolds / "index.md").write_text("# Project\n")
        for directory in ("roles", "workflows", "shared", "knowledge", "inbox"):
            (scaffolds / directory / "index.md").write_text(f"# {directory}\n")
        (scaffolds / "inbox/processed/index.md").write_text("# Processed\n")

    def run_command(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            args,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
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
    ) -> Path:
        output = self.assets / f"v{version}"
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
            (guidance_dir / "UPGRADE.md").write_text(
                f"# Exact guidance for {version}\n"
            )
            args.extend(("--guidance-dir", str(guidance_dir)))
        self.run_command(*args)
        return output

    def install(
        self,
        assets: Path,
        *extra: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
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

    @staticmethod
    def _rewrite_checksums(assets: Path) -> None:
        names = (
            "ava-install.sh",
            "ava-base.tar.gz",
            "ava-guidance.tar.gz",
            "ava-migrations.tar.gz",
            "ava-release.json",
            "ava-release-notes.md",
        )
        (assets / "SHA256SUMS").write_text(
            "".join(
                f"{hashlib.sha256((assets / name).read_bytes()).hexdigest()}  {name}\n"
                for name in names
            )
        )

    def set_edge_semantics(self, assets: Path, decisions: dict[str, bool]) -> None:
        path = assets / "ava-release.json"
        manifest = json.loads(path.read_text())
        edges = manifest["upgrade_paths"]["edges"]
        self.assertEqual({edge["from"] for edge in edges}, set(decisions))
        for edge in edges:
            required = decisions[edge["from"]]
            edge["semantic_review_required"] = required
            if not required:
                edge["guidance_paths"] = []
        manifest["semantic_review_required"] = any(decisions.values())
        path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        self._rewrite_checksums(assets)

    def test_semantic_edge_installs_exact_guidance_and_blocks_normal_routing(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        project_path = self.target / "roles/project-role.md"
        project_path.write_text("project-owned before upgrade\n")

        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        second = self.build(
            "0.2.0",
            upgrade_from=["0.1.0"],
            semantic=True,
            guidance=True,
        )
        self.set_edge_semantics(second, {"0.1.0": True})
        release = json.loads((second / "ava-release.json").read_text())
        expected_guidance = release["upgrade_paths"]["edges"][0]["guidance_paths"]
        self.assertEqual(expected_guidance, ["UPGRADE.md"])

        self.install(second)

        compatibility = self.manifest()["semantic_compatibility"]
        journal = self.journal()
        edge = journal["path"][0]
        self.assertEqual(compatibility["status"], "pending")
        self.assertEqual(compatibility["compatible_through"], "0.1.0")
        self.assertEqual(compatibility["target_version"], "0.2.0")
        self.assertEqual(journal["stage"], "semantic")
        self.assertEqual(
            journal["allowed_operations"],
            ["inspect", "reconcile-semantic", "rollback"],
        )
        self.assertNotIn("normal", journal["allowed_operations"])
        self.assertIs(edge["semantic_review_required"], True)
        self.assertEqual(edge["guidance_paths"], expected_guidance)
        self.assertEqual(
            (self.target / ".ava/guidance/UPGRADE.md").read_text(),
            "# Exact guidance for 0.2.0\n",
        )
        self.assertEqual(project_path.read_text(), "project-owned before upgrade\n")

        failed = self.install(second, "--finalize", check=False)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn("SEMANTIC_STATE_BLOCKED", failed.stderr)

        project_path.write_text("project-owned after Upgrade Role guidance\n")
        manifest = self.manifest()
        manifest["semantic_compatibility"] = {
            "compatible_through": "0.2.0",
            "target_version": None,
            "status": "complete",
            "unresolved_decisions": [],
        }
        (self.target / ".ava/state/manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        )
        journal = self.journal()
        journal["project_changes"] = [
            {
                "path": "/roles/project-role.md",
                "change_type": "modified",
                "recorded_at": "2026-08-06T14:00:00Z",
                "resolution": "reconciled",
            }
        ]
        (self.target / ".ava/state/upgrade.json").write_text(
            json.dumps(journal, indent=2, sort_keys=True) + "\n"
        )

        self.install(second, "--finalize")
        final = self.journal()
        self.assertEqual(final["status"], "complete")
        self.assertEqual(final["stage"], "complete")
        self.assertEqual(final["allowed_operations"], ["normal"])
        self.assertEqual(final["project_changes"][0]["path"], "/roles/project-role.md")

    def test_selected_no_impact_edge_ignores_release_wide_semantic_summary(self) -> None:
        first = self.build("0.1.0")
        self.install(first)
        project_path = self.target / "knowledge/project.md"
        project_path.write_text("project-owned unchanged\n")

        (self.repo / "templates/base/AGENTS.md").write_text("# Router 0.3.0\n")
        third = self.build(
            "0.3.0",
            upgrade_from=["0.1.0", "0.2.0"],
            semantic=True,
            guidance=True,
        )
        self.set_edge_semantics(
            third,
            {
                "0.1.0": False,
                "0.2.0": True,
            },
        )

        release = json.loads((third / "ava-release.json").read_text())
        self.assertIs(release["semantic_review_required"], True)
        selected = next(
            edge for edge in release["upgrade_paths"]["edges"]
            if edge["from"] == "0.1.0"
        )
        self.assertIs(selected["semantic_review_required"], False)
        self.assertEqual(selected["guidance_paths"], [])

        self.install(third)

        self.assertEqual(
            self.manifest()["semantic_compatibility"],
            {
                "compatible_through": "0.3.0",
                "target_version": None,
                "status": "complete",
                "unresolved_decisions": [],
            },
        )
        self.assertEqual(self.journal()["status"], "complete")
        self.assertEqual(self.journal()["allowed_operations"], ["normal"])
        self.assertEqual(project_path.read_text(), "project-owned unchanged\n")


class InspectionOnlyProjectChangeContractTests(unittest.TestCase):
    def test_upgrade_schema_and_role_define_inspection_only_records(self) -> None:
        schema = json.loads(
            (SOURCE_ROOT / "distribution/schemas/upgrade.schema.json").read_text(encoding="utf-8")
        )
        change_types = schema["$defs"]["projectChange"]["properties"]["change_type"]["enum"]
        self.assertIn("inspected", change_types)
        role = (
            SOURCE_ROOT / "templates/base/roles/upgrade-role/instructions.md"
        ).read_text(encoding="utf-8")
        self.assertIn("change_type: inspected", role)
        self.assertIn("every project-owned path inspected or changed", role)
        self.assertIn("recorded exactly once", role)
        self.assertIn("explicitly state that the exact recorded path was inspected", role)
        self.assertIn("listing the path or its journal classification alone is not sufficient", role)


if __name__ == "__main__":
    unittest.main()
