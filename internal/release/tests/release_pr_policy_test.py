from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from internal.release.adjacent_edges import make_edge
from internal.release.validate_release_pr import (
    ReleasePrValidationError,
    validate_release_pr,
)


class ReleasePrPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "internal/release/catalogs").mkdir(parents=True)
        (self.root / "internal/release/guidance").mkdir(parents=True)
        (self.root / "internal/release/fixtures").mkdir(parents=True)
        (self.root / "internal/release/fixtures/release-upgrade-policy.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "initial_release_version": "1.0.0-alpha.1",
                    "protected_direct_sources": [],
                }
            )
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def catalog(target: str, sources, edges):
        return {
            "catalog_schema": 1,
            "target_version": target,
            "supported_sources": list(sources),
            "edges": list(edges),
            "guidance": [],
        }

    def write_catalog(self, value) -> None:
        target = value["target_version"]
        (self.root / f"internal/release/catalogs/{target}.json").write_text(
            json.dumps(value)
        )

    def write_identity(self, target: str, channel: str) -> None:
        (self.root / "version.txt").write_text(f"{target}\n")
        (self.root / ".release-please-manifest.json").write_text(
            json.dumps({".": target})
        )
        if channel == "stable":
            config = {"prerelease": False, "versioning": "default"}
        else:
            config = {
                "prerelease": True,
                "versioning": "prerelease",
                "prerelease-type": channel,
            }
        (self.root / "release-please-config.json").write_text(json.dumps(config))
        (self.root / "internal/release/catalog-retirements.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "target_version": target,
                    "retired_sources": [],
                }
            )
        )

    def write_release(
        self,
        previous: str,
        target: str,
        channel: str,
    ) -> None:
        prior_source = (
            "1.0.0-alpha.1"
            if previous == "1.0.0-alpha.2"
            else "1.0.0-alpha.2"
        )
        prior_edge = make_edge(prior_source, previous)
        prior = self.catalog(previous, [prior_source], [prior_edge])
        current = self.catalog(
            target,
            [prior_source, previous],
            [prior_edge, make_edge(previous, target)],
        )
        self.write_catalog(prior)
        self.write_catalog(current)
        self.write_identity(target, channel)

    def test_accepts_alpha_release(self) -> None:
        self.write_release("2.0.0-alpha.3", "2.0.0-alpha.4", "alpha")
        message = validate_release_pr(self.root, "2.0.0-alpha.3")
        self.assertIn("channel: alpha", message)

    def test_accepts_rc_release(self) -> None:
        self.write_release("2.0.0-alpha.9", "2.0.0-rc.1", "rc")
        message = validate_release_pr(self.root, "2.0.0-alpha.9")
        self.assertIn("channel: rc", message)

    def test_accepts_stable_release(self) -> None:
        self.write_release("2.0.0-rc.2", "2.0.0", "stable")
        message = validate_release_pr(self.root, "2.0.0-rc.2")
        self.assertIn("channel: stable", message)

    def test_accepts_stable_patch_release(self) -> None:
        self.write_release("2.0.0", "2.0.1", "stable")
        message = validate_release_pr(self.root, "2.0.0")
        self.assertIn("2.0.0 -> 2.0.1", message)

    def test_rejects_channel_configuration_mismatch(self) -> None:
        self.write_release("2.0.0-alpha.9", "2.0.0-rc.1", "alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "rc release requires"):
            validate_release_pr(self.root, "2.0.0-alpha.9")

    def test_rejects_non_advancing_release(self) -> None:
        self.write_identity("2.0.0-alpha.3", "alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "must advance Ava"):
            validate_release_pr(self.root, "2.0.0-alpha.3")

    def test_rejects_missing_target_catalog(self) -> None:
        self.write_identity("2.0.0-alpha.4", "alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "cannot read"):
            validate_release_pr(self.root, "2.0.0-alpha.3")

    def test_rejects_legacy_upgrade_impact_authoring(self) -> None:
        self.write_release("2.0.0-alpha.3", "2.0.0-alpha.4", "alpha")
        (self.root / "internal/release/upgrade-impact.json").write_text("{}")
        with self.assertRaisesRegex(ReleasePrValidationError, "archival compatibility"):
            validate_release_pr(self.root, "2.0.0-alpha.3")

    def test_accepts_configured_first_release(self) -> None:
        target = "1.0.0-alpha.1"
        self.write_identity(target, "alpha")
        self.write_catalog(self.catalog(target, [], []))
        message = validate_release_pr(self.root, "0.0.0")
        self.assertIn("0.0.0 -> 1.0.0-alpha.1", message)

    def test_rejects_protected_source_retirement(self) -> None:
        self.write_release("2.0.0-alpha.3", "2.0.0-alpha.4", "alpha")
        policy = {
            "schema_version": 1,
            "initial_release_version": "1.0.0-alpha.1",
            "protected_direct_sources": ["1.0.0-alpha.2"],
        }
        (self.root / "internal/release/fixtures/release-upgrade-policy.json").write_text(
            json.dumps(policy)
        )
        current_path = self.root / "internal/release/catalogs/2.0.0-alpha.4.json"
        current = json.loads(current_path.read_text())
        current["supported_sources"] = ["2.0.0-alpha.3"]
        current_path.write_text(json.dumps(current))
        (self.root / "internal/release/catalog-retirements.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "target_version": "2.0.0-alpha.4",
                    "retired_sources": [
                        {
                            "version": "1.0.0-alpha.2",
                            "reason": "Support window ended.",
                        }
                    ],
                }
            )
        )
        with self.assertRaisesRegex(
            ReleasePrValidationError,
            "separate policy change",
        ):
            validate_release_pr(self.root, "2.0.0-alpha.3")


if __name__ == "__main__":
    unittest.main()
