from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release.conformance_common import RELEASE_ASSETS
from internal.release.conformance_release import validate_release

SOURCE_ROOT = Path(__file__).resolve().parents[3]
ASSEMBLER = SOURCE_ROOT / "internal/release/assemble.py"
INSTALLER_SOURCE = SOURCE_ROOT / "internal/release/ava-install.sh"
INSTALLER_FRAGMENTS = SOURCE_ROOT / "internal/release/installer"
POLICY = SOURCE_ROOT / "internal/release/fixtures/alpha-qualification.json"
MATRIX = SOURCE_ROOT / "internal/release/fixtures/conformance-matrix.json"
RELEASE_SCHEMA = SOURCE_ROOT / "distribution/schemas/release.schema.json"
REVISION = "0123456789abcdef0123456789abcdef01234567"


class AlphaQualificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self._create_repository_fixture()
        self.policy = json.loads(POLICY.read_text())
        self.matrix = json.loads(MATRIX.read_text())

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
        (base / "AGENTS.md").write_text("# Router\n")
        (base / "index.md").write_text("# Base\n")
        (base / "roles/index.md").write_text("# Roles\n")
        (base / "workflows/index.md").write_text("# Workflows\n")
        (base / "shared/index.md").write_text("# Shared\n")
        (base / "shared/instructions/test.md").write_text("# Test\n")

        scaffolds = self.repo / "templates/project-scaffolds"
        for directory in ("roles", "workflows", "shared", "knowledge", "inbox/processed"):
            (scaffolds / directory).mkdir(parents=True, exist_ok=True)
        (scaffolds / "index.md").write_text("# Project\n")
        for directory in ("roles", "workflows", "shared", "knowledge", "inbox"):
            (scaffolds / directory / "index.md").write_text(f"# {directory}\n")
        (scaffolds / "inbox/processed/index.md").write_text("# Processed\n")

    def _build(
        self,
        version: str,
        destination: Path,
        *,
        upgrade_from: list[str] | None = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        destination.mkdir(parents=True, exist_ok=True)
        command = [
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
        ]
        for source in upgrade_from or []:
            command.extend(("--upgrade-from", source))
        result = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if check and result.returncode != 0:
            self.fail(
                f"command failed ({result.returncode}): {' '.join(command)}\n"
                f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
            )
        return result

    @staticmethod
    def _digests(directory: Path) -> dict[str, str]:
        return {
            name: hashlib.sha256((directory / name).read_bytes()).hexdigest()
            for name in RELEASE_ASSETS
        }

    def test_policy_schema_and_gate_identifiers_are_stable(self) -> None:
        self.assertEqual(self.policy["schema_version"], 1)
        self.assertEqual(self.policy["target_version"], "1.0.0-alpha.1")
        self.assertEqual(self.policy["result_values"], ["ready", "blocked"])
        gates = self.policy["gates"]
        self.assertEqual(len({gate["id"] for gate in gates}), len(gates))
        self.assertEqual(
            [gate["id"] for gate in gates],
            [
                "roadmap-complete",
                "contracts-consistent",
                "role-authority-separated",
                "opencode-supported",
                "installation-lifecycle-safe",
                "release-assembly-reproducible",
                "notes-guidance-consistent",
                "protected-state-defects-closed",
                "publication-approved",
            ],
        )
        self.assertTrue(all(gate["required"] is True for gate in gates))

    def test_gate_evidence_resolves_to_files_and_conformance_cases(self) -> None:
        matrix_cases = {case["id"] for case in self.matrix["cases"]}
        for gate in self.policy["gates"]:
            for path in gate["documents"]:
                self.assertTrue((SOURCE_ROOT / path).exists(), f"{gate['id']}: {path}")
            for case_id in gate["matrix_cases"]:
                self.assertIn(case_id, matrix_cases, f"{gate['id']}: {case_id}")

    def test_phase_one_through_four_tasks_are_complete(self) -> None:
        completed_root = SOURCE_ROOT / "internal/todo/completed"
        task_files: list[tuple[int, Path]] = []
        for path in sorted(completed_root.glob("ava-* - *.md")):
            task_id_text = path.name.split(" ", 1)[0].removeprefix("ava-")
            if not task_id_text.isdigit():
                continue
            task_id = int(task_id_text)
            if 100 <= task_id < 500:
                task_files.append((task_id, path))

        self.assertTrue(task_files)
        self.assertEqual({task_id // 100 for task_id, _path in task_files}, {1, 2, 3, 4})
        for _task_id, path in task_files:
            frontmatter = path.read_text().split("---", 2)[1]
            self.assertRegex(
                frontmatter,
                r'(?m)^status:\s*["\']?Done["\']?\s*$',
                path.relative_to(SOURCE_ROOT),
            )

    def test_finding_classes_and_protected_impacts_block_correctly(self) -> None:
        classes = {item["id"]: item for item in self.policy["finding_classes"]}
        self.assertEqual(set(classes), {"blocker", "required-v1", "post-v1"})
        self.assertEqual(classes["blocker"]["current_publication"], "blocked")
        self.assertEqual(classes["blocker"]["stable_publication"], "blocked")
        self.assertEqual(classes["required-v1"]["stable_publication"], "blocked")
        self.assertTrue(classes["blocker"]["task_required"])
        self.assertTrue(classes["required-v1"]["task_required"])
        self.assertFalse(classes["post-v1"]["task_required"])
        self.assertEqual(
            set(self.policy["protected_impacts"]),
            {
                "managed-state-corruption",
                "project-owned-content-overwrite",
                "target-root-escape",
                "authority-bypass",
                "unrecoverable-installation",
            },
        )

    def test_first_alpha_is_reproducible_and_has_no_supported_source(self) -> None:
        first = self.root / "alpha-first"
        second = self.root / "alpha-second"
        self._build("1.0.0-alpha.1", first)
        self._build("1.0.0-alpha.1", second)

        self.assertEqual(self._digests(first), self._digests(second))
        manifest = json.loads((first / "ava-release.json").read_text())
        self.assertEqual(manifest["ava_version"], "1.0.0-alpha.1")
        self.assertEqual(manifest["channel"], "alpha")
        self.assertEqual(manifest["upgrade_paths"], {"edges": []})
        self.assertTrue(validate_release(first).valid)

    def test_assembly_rejects_links_that_break_after_destination_mapping(self) -> None:
        base = self.repo / "templates/base"
        (base / "inbox").mkdir()
        source_target = base / "inbox/index.md"
        source_target.write_text("# Source-only inbox\n")
        role_directory = base / "roles/inbox-ingester"
        role_directory.mkdir()
        role_index = role_directory / "index.md"
        role_index.write_text("# Inbox Ingester\n\n[Inbox](../../inbox/index.md)\n")

        self.assertEqual((role_index.parent / "../../inbox/index.md").resolve(), source_target)
        self.assertTrue(source_target.is_file())
        result = self._build("1.0.0-alpha.1", self.root / "broken-links", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unresolved installed Markdown links", result.stderr)
        self.assertIn("/.ava/base/inbox/index.md", result.stderr)

        role_index.write_text(role_index.read_text().replace("../../inbox/index.md", "./inbox/index.md"))
        self._build("1.0.0-alpha.1", self.root / "resolved-links")

    def test_assembly_rejects_links_that_escape_the_installed_root(self) -> None:
        base = self.repo / "templates/base"
        role_directory = base / "roles/test-role"
        role_directory.mkdir()
        role_index = role_directory / "index.md"

        role_index.write_text("# Test role\n\n[Router](../../../../../AGENTS.md)\n")
        result = self._build("1.0.0-alpha.1", self.root / "document-escape", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("<outside installed project>", result.stderr)

        role_index.write_text("# Test role\n\n[Router](./../AGENTS.md)\n")
        result = self._build("1.0.0-alpha.1", self.root / "project-escape", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("<outside installed project>", result.stderr)

        role_index.write_text("# Test role\n\n[Router](../../../../AGENTS.md)\n")
        (base / "shared/instructions/target_(draft).md").write_text("# Draft target\n")
        (base / "shared/instructions/target file.md").write_text("# Spaced target\n")
        (base / "shared/instructions/target's.md").write_text("# Apostrophe target\n")
        (base / "index.md").write_text(
            "# Base\n\n"
            "Example: `[Missing](missing.md)`\n\n"
            "Escaped example: \\[Missing](missing.md)\n\n"
            "[Draft](shared/instructions/target_(draft).md)\n\n"
            "[Spaced](<shared/instructions/target file.md>)\n\n"
            "[Apostrophe](shared/instructions/target's.md)\n"
        )
        self._build("1.0.0-alpha.1", self.root / "exact-root")

    def test_prerelease_transitions_are_machine_readable_release_edges(self) -> None:
        # Group declared transitions by target so releases with multiple sources
        # (e.g. alpha.5 from both alpha.3 and alpha.4) are assembled correctly.
        by_target: dict[str, list[dict]] = {}
        for transition in self.policy["prerelease_support"]["transitions"]:
            by_target.setdefault(transition["to"], []).append(transition)

        actual = []
        for version, transitions in sorted(by_target.items()):
            sources = [t["from"] for t in transitions]
            channel = transitions[0]["channel"]
            output = self.root / version
            self._build(version, output, upgrade_from=sources)
            manifest = json.loads((output / "ava-release.json").read_text())
            self.assertEqual(manifest["channel"], channel)
            expected_edges = sorted(
                [
                    {
                        "from": source,
                        "to": version,
                        "mode": "direct",
                        "intermediates": [],
                        "carry_unresolved_semantic_state": False,
                        "migration_ids": [],
                        "guidance_paths": [],
                    }
                    for source in sources
                ],
                key=lambda e: e["from"],
            )
            self.assertEqual(
                sorted(manifest["upgrade_paths"]["edges"], key=lambda e: e["from"]),
                expected_edges,
            )
            for source in sources:
                actual.append({"from": source, "to": version, "channel": channel, "must_be_declared": True})

        sort_key = lambda t: (t["to"], t["from"])  # noqa: E731
        self.assertEqual(sorted(actual, key=sort_key), sorted(self.policy["prerelease_support"]["transitions"], key=sort_key))
        self.assertEqual(sorted(actual, key=sort_key), sorted(self.matrix["prerelease_transitions"], key=sort_key))

    def test_historical_unversioned_source_is_rejected(self) -> None:
        result = self._build(
            "1.0.0-alpha.2",
            self.root / "invalid-source",
            upgrade_from=["unversioned"],
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid Ava version", result.stderr)
        self.assertFalse(self.policy["prerelease_support"]["historical_unversioned_supported"])

    def test_non_first_release_with_empty_edges_fails_conformance(self) -> None:
        output = self.root / "no-edges"
        self._build("1.0.0-alpha.2", output)
        result = validate_release(output)
        rule_ids = {finding.rule_id for finding in result.findings}
        self.assertIn("AVA-RELEASE-UPGRADE-EDGES", rule_ids)

    def test_first_alpha_with_empty_edges_passes_conformance(self) -> None:
        output = self.root / "first-alpha-edges"
        self._build("1.0.0-alpha.1", output)
        result = validate_release(output)
        rule_ids = {finding.rule_id for finding in result.findings}
        self.assertNotIn("AVA-RELEASE-UPGRADE-EDGES", rule_ids)

    def test_public_release_schema_requires_explicit_upgrade_edges(self) -> None:
        schema = json.loads(RELEASE_SCHEMA.read_text())
        self.assertIn("upgrade_paths", schema["required"])
        upgrade_paths = schema["properties"]["upgrade_paths"]
        self.assertEqual(upgrade_paths["required"], ["edges"])
        self.assertEqual(
            upgrade_paths["properties"]["edges"]["items"],
            {"$ref": "#/$defs/upgradeEdge"},
        )
        edge = schema["$defs"]["upgradeEdge"]
        self.assertTrue(
            {
                "from",
                "to",
                "mode",
                "intermediates",
                "carry_unresolved_semantic_state",
                "migration_ids",
                "guidance_paths",
            }.issubset(edge["required"])
        )

    def test_publication_approval_is_exact_and_revision_bound(self) -> None:
        approval = self.policy["publication_approval"]
        self.assertTrue(approval["required"])
        self.assertEqual(approval["scope"], ["ava_version", "source_revision"])
        self.assertTrue(approval["invalidated_by_source_revision_change"])
        self.assertEqual(
            self.policy["prerelease_support"]["first_alpha"],
            {"version": "1.0.0-alpha.1", "supported_sources": []},
        )
        self.assertEqual(self.policy["prerelease_support"]["selection"], "exact-version-only")
        self.assertEqual(self.policy["prerelease_support"]["stable_guarantees_begin"], "1.0.0")


if __name__ == "__main__":
    unittest.main()
