from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release.assemble_reviewed import apply_reviewed_impact
from internal.release.validate_upgrade_impact import (
    UpgradeImpactValidationError,
    managed_delta,
    validate_upgrade_impact,
)


class UpgradeImpactTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "internal/release/fixtures").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def assessment(source: str, release_note_versions: list[str]) -> dict[str, object]:
        return {
            "from": source,
            "managed_changes": {
                "retained": "all-unlisted-managed-payload-files",
                "replaced": [],
                "created": [],
                "deleted": [],
            },
            "migration_ids": [],
            "migration_assessment": "Normal managed reconciliation is sufficient.",
            "guidance_paths": [],
            "semantic_review_required": False,
            "semantic_assessment": "No project-owned semantic contracts change.",
            "release_note_versions": release_note_versions,
            "release_note_assessment": "These are the cumulative relevant changes.",
        }

    def write_fixture(
        self,
        *,
        target: str = "1.0.0-alpha.8",
        sources: list[str] | None = None,
        protected: list[str] | None = None,
        assessments: list[dict[str, object]] | None = None,
    ) -> None:
        sources = sources or ["1.0.0-alpha.5", "1.0.0-alpha.6", "1.0.0-alpha.7"]
        protected = protected or ["1.0.0-alpha.5", "1.0.0-alpha.6", "1.0.0-alpha.7"]
        assessments = assessments or [
            self.assessment(
                "1.0.0-alpha.5",
                ["1.0.0-alpha.6", "1.0.0-alpha.7", target],
            ),
            self.assessment("1.0.0-alpha.6", ["1.0.0-alpha.7", target]),
            self.assessment("1.0.0-alpha.7", [target]),
        ]
        (self.root / "version.txt").write_text(f"{target}\n")
        (self.root / "internal/release/upgrade-sources.txt").write_text(
            "".join(f"{source}\n" for source in sources)
        )
        (self.root / "internal/release/upgrade-impact.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "target_version": target,
                    "sources": assessments,
                }
            )
        )
        (self.root / "internal/release/fixtures/alpha-qualification.json").write_text(
            json.dumps(
                {"prerelease_support": {"protected_direct_sources": protected}}
            )
        )
        versions = {
            version
            for assessment in assessments
            for version in assessment["release_note_versions"]
        }
        (self.root / "CHANGELOG.md").write_text(
            "".join(
                f"## [{version}]\n\nNotes.\n\n" for version in sorted(versions)
            )
        )

    def test_accepts_complete_reviewed_source_set(self) -> None:
        self.write_fixture()
        message = validate_upgrade_impact(
            self.root,
            "1.0.0-alpha.7",
            verify_managed_delta=False,
        )
        self.assertIn("1.0.0-alpha.5, 1.0.0-alpha.6, 1.0.0-alpha.7", message)

    def test_rejects_stranded_protected_source(self) -> None:
        assessments = [self.assessment("1.0.0-alpha.7", ["1.0.0-alpha.8"])]
        self.write_fixture(sources=["1.0.0-alpha.7"], assessments=assessments)
        with self.assertRaisesRegex(
            UpgradeImpactValidationError,
            "strands protected installed prereleases: 1.0.0-alpha.5, 1.0.0-alpha.6",
        ):
            validate_upgrade_impact(
                self.root,
                "1.0.0-alpha.7",
                verify_managed_delta=False,
            )

    def test_rejects_unreviewed_declared_source(self) -> None:
        assessments = [
            self.assessment("1.0.0-alpha.5", ["1.0.0-alpha.8"]),
            self.assessment("1.0.0-alpha.7", ["1.0.0-alpha.8"]),
        ]
        self.write_fixture(assessments=assessments)
        with self.assertRaisesRegex(
            UpgradeImpactValidationError,
            "sources do not exactly match upgrade-sources.txt",
        ):
            validate_upgrade_impact(
                self.root,
                "1.0.0-alpha.7",
                verify_managed_delta=False,
            )

    def test_requires_explicit_empty_migration_assessment(self) -> None:
        assessments = [self.assessment("1.0.0-alpha.7", ["1.0.0-alpha.8"])]
        assessments[0]["migration_assessment"] = ""
        self.write_fixture(
            sources=["1.0.0-alpha.7"],
            protected=["1.0.0-alpha.7"],
            assessments=assessments,
        )
        with self.assertRaisesRegex(
            UpgradeImpactValidationError,
            "migration_assessment must be non-empty",
        ):
            validate_upgrade_impact(
                self.root,
                "1.0.0-alpha.7",
                verify_managed_delta=False,
            )

    def test_requires_cumulative_changelog_entries(self) -> None:
        self.write_fixture()
        changelog = self.root / "CHANGELOG.md"
        changelog.write_text(
            changelog.read_text().replace("## [1.0.0-alpha.6]", "## Missing")
        )
        with self.assertRaisesRegex(
            UpgradeImpactValidationError,
            "require missing changelog versions: 1.0.0-alpha.6",
        ):
            validate_upgrade_impact(
                self.root,
                "1.0.0-alpha.7",
                verify_managed_delta=False,
            )

    def test_managed_delta_maps_repository_sources_to_installed_paths(self) -> None:
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.email", "test@example.com"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.name", "Test"],
            check=True,
        )
        base = self.root / "templates/base"
        (base / "roles/example").mkdir(parents=True)
        (base / "index.md").write_text("old\n")
        (base / "roles/example/index.md").write_text("delete\n")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "commit", "-qm", "base"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.root), "tag", "v1.0.0-alpha.7"],
            check=True,
        )

        (base / "index.md").write_text("new\n")
        (base / "roles/example/index.md").unlink()
        (base / "shared").mkdir()
        (base / "shared/index.md").write_text("created\n")
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "commit", "-qm", "target"],
            check=True,
        )

        self.assertEqual(
            managed_delta(self.root, "1.0.0-alpha.7"),
            {
                "replaced": ["/.ava/base/index.md"],
                "created": ["/.ava/base/shared/index.md"],
                "deleted": ["/.ava/base/roles/example/index.md"],
            },
        )

    def test_reviewed_assembly_overrides_each_edge_exactly(self) -> None:
        output = self.root / "output"
        output.mkdir()
        manifest = {
            "semantic_review_required": False,
            "upgrade_paths": {
                "edges": [
                    {
                        "from": "1.0.0-alpha.7",
                        "to": "1.0.0-alpha.8",
                        "migration_ids": ["unexpected"],
                        "guidance_paths": ["unexpected.md"],
                    }
                ]
            },
            "migrations": {"steps": []},
            "guidance": {"entries": []},
        }
        (output / "ava-release.json").write_text(json.dumps(manifest))
        for name in (
            "ava-install.sh",
            "ava-base.tar.gz",
            "ava-guidance.tar.gz",
            "ava-migrations.tar.gz",
            "ava-release-notes.md",
        ):
            (output / name).write_text(name)
        impact = {
            "schema_version": 1,
            "target_version": "1.0.0-alpha.8",
            "sources": [
                self.assessment("1.0.0-alpha.7", ["1.0.0-alpha.8"])
            ],
        }
        impact_path = self.root / "impact.json"
        impact_path.write_text(json.dumps(impact))

        apply_reviewed_impact(output, impact_path, "1.0.0-alpha.8")

        result = json.loads((output / "ava-release.json").read_text())
        edge = result["upgrade_paths"]["edges"][0]
        self.assertEqual(edge["migration_ids"], [])
        self.assertEqual(edge["guidance_paths"], [])
        expected = hashlib.sha256(
            (output / "ava-release.json").read_bytes()
        ).hexdigest()
        self.assertIn(
            f"{expected}  ava-release.json",
            (output / "SHA256SUMS").read_text(),
        )


if __name__ == "__main__":
    unittest.main()
