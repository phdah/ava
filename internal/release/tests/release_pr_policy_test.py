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


def bootstrap_record(target: str):
    return record(
        make_edge("0.0.0", target, carry_unresolved_semantic_state=True),
        retirements=[
            {
                "version": "0.0.0",
                "reason": "Bootstrap sentinel is not an installed release.",
            }
        ],
    )


class ReleasePrPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "internal/release/catalogs").mkdir(parents=True)
        (self.root / "internal/release/guidance").mkdir(parents=True)
        (self.root / "internal/release/fixtures").mkdir(parents=True)
        self.write_policy("1.0.0-alpha.1")

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

    def write_release(self, previous: str, target: str, channel: str) -> None:
        self.write_record(bootstrap_record(previous))
        self.write_record(record(make_edge(previous, target)))
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

    def test_rejects_missing_target_record(self) -> None:
        previous = "2.0.0-alpha.3"
        self.write_record(bootstrap_record(previous))
        self.write_identity("2.0.0-alpha.4", "alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "cannot read"):
            validate_release_pr(self.root, previous)

    def test_rejects_missing_previous_release_record(self) -> None:
        previous = "2.0.0-alpha.3"
        target = "2.0.0-alpha.4"
        self.write_record(record(make_edge(previous, target)))
        self.write_identity(target, "alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "missing release catalog record"):
            validate_release_pr(self.root, previous)

    def test_rejects_legacy_upgrade_impact_authoring(self) -> None:
        self.write_release("2.0.0-alpha.3", "2.0.0-alpha.4", "alpha")
        (self.root / "internal/release/upgrade-impact.json").write_text("{}")
        with self.assertRaisesRegex(ReleasePrValidationError, "archival compatibility"):
            validate_release_pr(self.root, "2.0.0-alpha.3")

    def test_accepts_configured_first_release_with_bootstrap_edge(self) -> None:
        target = "1.0.0-alpha.1"
        self.write_policy(target)
        self.write_identity(target, "alpha")
        self.write_record(bootstrap_record(target))
        message = validate_release_pr(self.root, "0.0.0")
        self.assertIn("0.0.0 -> 1.0.0-alpha.1", message)

    def test_rejects_first_release_without_edge_record(self) -> None:
        target = "1.0.0-alpha.1"
        self.write_policy(target)
        self.write_identity(target, "alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "cannot read"):
            validate_release_pr(self.root, "0.0.0")

    def test_rejects_first_release_with_wrong_bootstrap_edge(self) -> None:
        target = "1.0.0-alpha.1"
        self.write_policy(target)
        self.write_identity(target, "alpha")
        self.write_record(record(make_edge("0.9.0", target)))
        with self.assertRaisesRegex(ReleasePrValidationError, "immediately previous"):
            validate_release_pr(self.root, "0.0.0")

    def test_rejects_record_whose_edge_skips_previous_release(self) -> None:
        previous = "2.0.0-alpha.3"
        target = "2.0.0-alpha.4"
        self.write_record(bootstrap_record(previous))
        self.write_identity(target, "alpha")
        self.write_record(
            record(make_edge("2.0.0-alpha.2", target))
        )
        with self.assertRaisesRegex(ReleasePrValidationError, "immediately previous"):
            validate_release_pr(self.root, previous)

    def test_rejects_protected_source_retirement(self) -> None:
        initial = "1.0.0-alpha.1"
        previous = "1.0.0-alpha.2"
        target = "1.0.0-alpha.3"
        self.write_policy(initial, protected=[initial])
        self.write_record(bootstrap_record(initial))
        self.write_record(record(make_edge(initial, previous)))
        self.write_record(
            record(
                make_edge(previous, target),
                retirements=[
                    {
                        "version": initial,
                        "reason": "Support window ended.",
                    }
                ],
            )
        )
        self.write_identity(target, "alpha")
        with self.assertRaisesRegex(
            ReleasePrValidationError,
            "separate policy change",
        ):
            validate_release_pr(self.root, previous)


if __name__ == "__main__":
    unittest.main()
