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


def record(edge, retirements=()):
    return {
        "catalog_schema": 1,
        "target_version": edge["to"],
        "edge": edge,
        "guidance": [],
        "retired_sources": list(retirements),
    }


class ReleasePrPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "internal/release/catalogs").mkdir(parents=True)
        (self.root / "internal/release/guidance").mkdir(parents=True)
        (self.root / "internal/release/fixtures").mkdir(parents=True)
        self.write_policy("1.0.0")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_policy(self, initial: str, protected=()) -> None:
        (self.root / "internal/release/fixtures/release-upgrade-policy.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "initial_release_version": initial,
                    "protected_direct_sources": list(protected),
                }
            )
        )

    def write_record(self, value) -> None:
        target = value["target_version"]
        (self.root / f"internal/release/catalogs/{target}.json").write_text(
            json.dumps(value)
        )

    def write_identity(self, target: str, channel: str = "stable") -> None:
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

    def write_stable_chain(self, *versions: str) -> None:
        previous = "1.0.0"
        for target in versions:
            self.write_record(record(make_edge(previous, target)))
            previous = target

    def test_accepts_first_stable_release_without_edge(self) -> None:
        self.write_identity("1.0.0")
        message = validate_release_pr(self.root, "0.0.0")
        self.assertIn("first stable release identity valid for 1.0.0", message)
        self.assertIn("no previous published release or upgrade edge", message)

    def test_rejects_first_release_with_edge_record(self) -> None:
        self.write_identity("1.0.0")
        self.write_record(record(make_edge("0.9.0", "1.0.0")))
        with self.assertRaisesRegex(ReleasePrValidationError, "root release"):
            validate_release_pr(self.root, "0.0.0")

    def test_rejects_wrong_first_release_version(self) -> None:
        self.write_identity("1.1.0")
        with self.assertRaisesRegex(ReleasePrValidationError, "first release target"):
            validate_release_pr(self.root, "0.0.0")

    def test_accepts_stable_patch_release(self) -> None:
        self.write_stable_chain("1.0.1")
        self.write_identity("1.0.1")
        message = validate_release_pr(self.root, "1.0.0")
        self.assertIn("1.0.0 -> 1.0.1", message)
        self.assertIn("channel: stable", message)

    def test_accepts_recursive_stable_chain(self) -> None:
        self.write_stable_chain("1.0.1", "1.0.2")
        self.write_identity("1.0.2")
        message = validate_release_pr(self.root, "1.0.1")
        self.assertIn("1.0.1 -> 1.0.2", message)

    def test_accepts_generic_rc_transition(self) -> None:
        self.write_policy("2.0.0-rc.1")
        self.write_record(record(make_edge("1.0.0", "2.0.0-rc.1")))
        self.write_record(record(make_edge("2.0.0-rc.1", "2.0.0")))
        self.write_identity("2.0.0", "stable")
        message = validate_release_pr(self.root, "2.0.0-rc.1")
        self.assertIn("channel: stable", message)

    def test_rejects_channel_configuration_mismatch(self) -> None:
        self.write_stable_chain("1.0.1")
        self.write_identity("1.0.1", "beta")
        with self.assertRaisesRegex(ReleasePrValidationError, "stable release requires"):
            validate_release_pr(self.root, "1.0.0")

    def test_rejects_non_advancing_release(self) -> None:
        self.write_identity("1.0.0")
        with self.assertRaisesRegex(ReleasePrValidationError, "must advance Ava"):
            validate_release_pr(self.root, "1.0.0")

    def test_rejects_missing_target_record_after_root(self) -> None:
        self.write_identity("1.0.1")
        with self.assertRaisesRegex(ReleasePrValidationError, "cannot read"):
            validate_release_pr(self.root, "1.0.0")

    def test_rejects_record_whose_edge_skips_previous_release(self) -> None:
        self.write_record(record(make_edge("1.0.0", "1.0.1")))
        self.write_record(record(make_edge("1.0.0", "1.0.2")))
        self.write_identity("1.0.2")
        with self.assertRaisesRegex(ReleasePrValidationError, "immediately previous"):
            validate_release_pr(self.root, "1.0.1")

    def test_rejects_legacy_upgrade_impact_authoring(self) -> None:
        self.write_stable_chain("1.0.1")
        self.write_identity("1.0.1")
        (self.root / "internal/release/upgrade-impact.json").write_text("{}")
        with self.assertRaisesRegex(ReleasePrValidationError, "archival compatibility"):
            validate_release_pr(self.root, "1.0.0")

    def test_rejects_protected_source_retirement(self) -> None:
        self.write_policy("1.0.0", protected=["1.0.0"])
        self.write_record(record(make_edge("1.0.0", "1.0.1")))
        self.write_record(
            record(
                make_edge("1.0.1", "1.0.2"),
                retirements=[
                    {"version": "1.0.0", "reason": "Support window ended."}
                ],
            )
        )
        self.write_identity("1.0.2")
        with self.assertRaisesRegex(
            ReleasePrValidationError,
            "separate policy change",
        ):
            validate_release_pr(self.root, "1.0.1")


if __name__ == "__main__":
    unittest.main()
