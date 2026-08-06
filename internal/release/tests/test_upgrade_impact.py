from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from internal.release.assemble_reviewed import apply_reviewed_impact, main as assemble_reviewed_main
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
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.email", "test@example.com"],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.root), "config", "user.name", "Test"],
            check=True,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def assessment(source: str, notes: list[str]) -> dict[str, object]:
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
            "release_note_versions": notes,
            "release_note_assessment": "These are all cumulative releases after the source.",
        }

    def write_policy(self, protected: list[str] | None = None) -> None:
        (self.root / "internal/release/fixtures/release-upgrade-policy.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "initial_release_version": "1.0.0-alpha.1",
                    "protected_direct_sources": protected or [],
                }
            )
        )

    def tag_previous(
        self,
        previous: str,
        *,
        prior_sources: list[str] | None = None,
        legacy: bool = False,
    ) -> None:
        self.write_policy()
        (self.root / "version.txt").write_text(f"{previous}\n")
        if legacy:
            (self.root / "internal/release/upgrade-sources.txt").write_text(
                "".join(f"{source}\n" for source in prior_sources or [])
            )
        else:
            (self.root / "internal/release/upgrade-impact.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "target_version": previous,
                        "retired_sources": [],
                        "sources": [
                            self.assessment(source, [previous])
                            for source in prior_sources or []
                        ],
                    }
                )
            )
        (self.root / "CHANGELOG.md").write_text(f"## [{previous}]\n\nNotes.\n")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "previous"], check=True)
        subprocess.run(["git", "-C", str(self.root), "tag", f"v{previous}"], check=True)

    def write_target(
        self,
        target: str,
        sources: list[tuple[str, list[str]]],
        *,
        retired: list[tuple[str, str]] | None = None,
        headings: list[str] | None = None,
    ) -> None:
        (self.root / "version.txt").write_text(f"{target}\n")
        headings = headings or [target]
        (self.root / "CHANGELOG.md").write_text(
            "".join(f"## [{version}]\n\nNotes.\n\n" for version in reversed(headings))
        )
        (self.root / "internal/release/upgrade-impact.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "target_version": target,
                    "retired_sources": [
                        {"version": version, "reason": reason}
                        for version, reason in retired or []
                    ],
                    "sources": [self.assessment(source, notes) for source, notes in sources],
                }
            )
        )

    def test_inherits_previous_release_and_legacy_sources(self) -> None:
        self.tag_previous(
            "3.0.0-alpha.7",
            prior_sources=["3.0.0-alpha.6"],
            legacy=True,
        )
        self.write_policy(["3.0.0-alpha.5"])
        headings = ["3.0.0-alpha.6", "3.0.0-alpha.7", "3.0.0-alpha.8"]
        self.write_target(
            "3.0.0-alpha.8",
            [
                ("3.0.0-alpha.5", headings),
                ("3.0.0-alpha.6", headings[1:]),
                ("3.0.0-alpha.7", headings[2:]),
            ],
            headings=headings,
        )
        message = validate_upgrade_impact(
            self.root, "3.0.0-alpha.7", verify_managed_delta=False
        )
        self.assertIn("3.0.0-alpha.5", message)

    def test_accepts_rc_release(self) -> None:
        self.tag_previous("2.0.0-alpha.9")
        self.write_target(
            "2.0.0-rc.1",
            [("2.0.0-alpha.9", ["2.0.0-rc.1"])],
        )
        self.assertIn(
            "rc",
            validate_upgrade_impact(
                self.root, "2.0.0-alpha.9", verify_managed_delta=False
            ),
        )

    def test_accepts_stable_release(self) -> None:
        self.tag_previous("2.0.0-rc.1")
        self.write_target("2.0.0", [("2.0.0-rc.1", ["2.0.0"])])
        self.assertIn(
            "stable",
            validate_upgrade_impact(self.root, "2.0.0-rc.1", verify_managed_delta=False),
        )

    def test_accepts_stable_patch_release(self) -> None:
        self.tag_previous("2.0.0")
        self.write_target("2.0.1", [("2.0.0", ["2.0.1"])])
        validate_upgrade_impact(self.root, "2.0.0", verify_managed_delta=False)

    def test_rejects_omitted_inherited_source(self) -> None:
        self.tag_previous("2.0.0-alpha.3", prior_sources=["2.0.0-alpha.2"])
        self.write_target(
            "2.0.0-alpha.4",
            [("2.0.0-alpha.3", ["2.0.0-alpha.4"])],
        )
        with self.assertRaisesRegex(
            UpgradeImpactValidationError,
            "strands required direct sources: 2.0.0-alpha.2",
        ):
            validate_upgrade_impact(
                self.root, "2.0.0-alpha.3", verify_managed_delta=False
            )

    def test_explicit_retirement_allows_dropping_inherited_source(self) -> None:
        self.tag_previous("2.0.0-rc.1", prior_sources=["2.0.0-alpha.9"])
        self.write_target(
            "2.0.0",
            [("2.0.0-rc.1", ["2.0.0"])],
            retired=[("2.0.0-alpha.9", "Stable support begins at the release candidate.")],
        )
        validate_upgrade_impact(self.root, "2.0.0-rc.1", verify_managed_delta=False)

    def test_protected_source_requires_policy_change_before_retirement(self) -> None:
        self.tag_previous("2.0.0-alpha.3")
        self.write_policy(["2.0.0-alpha.1"])
        self.write_target(
            "2.0.0-alpha.4",
            [("2.0.0-alpha.3", ["2.0.0-alpha.4"])],
            retired=[("2.0.0-alpha.1", "No longer supported.")],
        )
        with self.assertRaisesRegex(
            UpgradeImpactValidationError,
            "separate policy change before retirement",
        ):
            validate_upgrade_impact(
                self.root, "2.0.0-alpha.3", verify_managed_delta=False
            )

    def test_requires_exact_cumulative_changelog_entries(self) -> None:
        self.tag_previous("2.0.0-alpha.2")
        self.write_target(
            "2.0.0-alpha.4",
            [("2.0.0-alpha.2", ["2.0.0-alpha.4"])],
            headings=["2.0.0-alpha.3", "2.0.0-alpha.4"],
        )
        with self.assertRaisesRegex(
            UpgradeImpactValidationError,
            "must exactly cover every release",
        ):
            validate_upgrade_impact(
                self.root, "2.0.0-alpha.2", verify_managed_delta=False
            )

    def test_managed_delta_maps_repository_sources_to_installed_paths(self) -> None:
        self.write_policy()
        base = self.root / "templates/base"
        (base / "roles/example").mkdir(parents=True)
        (base / "index.md").write_text("old\n")
        (base / "roles/example/index.md").write_text("delete\n")
        subprocess.run(["git", "-C", str(self.root), "add", "."], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "base"], check=True)
        subprocess.run(["git", "-C", str(self.root), "tag", "v2.0.0"], check=True)

        (base / "index.md").write_text("new\n")
        (base / "roles/example/index.md").unlink()
        (base / "shared").mkdir()
        (base / "shared/index.md").write_text("created\n")
        subprocess.run(["git", "-C", str(self.root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(self.root), "commit", "-qm", "target"], check=True)

        self.assertEqual(
            managed_delta(self.root, "2.0.0"),
            {
                "replaced": ["/.ava/base/index.md"],
                "created": ["/.ava/base/shared/index.md"],
                "deleted": ["/.ava/base/roles/example/index.md"],
            },
        )

    def test_reviewed_assembly_uses_impact_as_edge_source(self) -> None:
        output = self.root / "output"
        output.mkdir()
        manifest = {
            "semantic_review_required": False,
            "upgrade_paths": {
                "edges": [
                    {
                        "from": "2.0.0-rc.1",
                        "to": "2.0.0",
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
            "target_version": "2.0.0",
            "retired_sources": [],
            "sources": [self.assessment("2.0.0-rc.1", ["2.0.0"])],
        }
        impact_path = self.root / "impact.json"
        impact_path.write_text(json.dumps(impact))

        apply_reviewed_impact(output, impact_path, "2.0.0")
        result = json.loads((output / "ava-release.json").read_text())
        self.assertEqual(result["upgrade_paths"]["edges"][0]["migration_ids"], [])
        expected = hashlib.sha256((output / "ava-release.json").read_bytes()).hexdigest()
        self.assertIn(f"{expected}  ava-release.json", (output / "SHA256SUMS").read_text())

        captured = {}
        with mock.patch("internal.release.assemble_reviewed.assemble.build") as build:
            def capture(args):
                captured["sources"] = args.upgrade_from
                args.output.mkdir(exist_ok=True)
            build.side_effect = capture
            with mock.patch("internal.release.assemble_reviewed.apply_reviewed_impact"):
                assemble_reviewed_main(
                    [
                        "--root", str(self.root),
                        "--output", str(self.root / "built"),
                        "--version", "2.0.0",
                        "--channel", "stable",
                        "--source-revision", "0" * 40,
                        "--source-date-epoch", "1",
                        "--upgrade-impact", str(impact_path),
                    ]
                )
        self.assertEqual(captured["sources"], ["2.0.0-rc.1"])


if __name__ == "__main__":
    unittest.main()
