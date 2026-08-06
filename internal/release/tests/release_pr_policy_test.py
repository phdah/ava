from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from internal.release.validate_release_pr import (
    ReleasePrValidationError,
    validate_release_pr,
)


class ReleasePrPolicyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
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
    def impact(target: str) -> dict[str, object]:
        return {
            "schema_version": 1,
            "target_version": target,
            "retired_sources": [],
            "sources": [],
        }

    def write_fixture(self, *, target: str, channel: str) -> None:
        (self.root / "version.txt").write_text(f"{target}\n")
        (self.root / ".release-please-manifest.json").write_text(json.dumps({".": target}))
        if channel == "stable":
            config = {"prerelease": False, "versioning": "default"}
        else:
            config = {
                "prerelease": True,
                "versioning": "prerelease",
                "prerelease-type": channel,
            }
        (self.root / "release-please-config.json").write_text(json.dumps(config))
        (self.root / "internal/release/upgrade-impact.json").write_text(
            json.dumps(self.impact(target))
        )

    def test_accepts_alpha_release(self) -> None:
        self.write_fixture(target="2.0.0-alpha.4", channel="alpha")
        message = validate_release_pr(self.root, "2.0.0-alpha.3")
        self.assertIn("channel: alpha", message)

    def test_accepts_rc_release(self) -> None:
        self.write_fixture(target="2.0.0-rc.1", channel="rc")
        message = validate_release_pr(self.root, "2.0.0-alpha.9")
        self.assertIn("channel: rc", message)

    def test_accepts_stable_release(self) -> None:
        self.write_fixture(target="2.0.0", channel="stable")
        message = validate_release_pr(self.root, "2.0.0-rc.2")
        self.assertIn("channel: stable", message)

    def test_accepts_stable_patch_release(self) -> None:
        self.write_fixture(target="2.0.1", channel="stable")
        message = validate_release_pr(self.root, "2.0.0")
        self.assertIn("2.0.0 -> 2.0.1", message)

    def test_rejects_channel_configuration_mismatch(self) -> None:
        self.write_fixture(target="2.0.0-rc.1", channel="alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "rc release requires"):
            validate_release_pr(self.root, "2.0.0-alpha.9")

    def test_rejects_non_advancing_release(self) -> None:
        self.write_fixture(target="2.0.0-alpha.3", channel="alpha")
        with self.assertRaisesRegex(ReleasePrValidationError, "must advance Ava"):
            validate_release_pr(self.root, "2.0.0-alpha.3")

    def test_rejects_missing_release_impact(self) -> None:
        self.write_fixture(target="2.0.0-alpha.4", channel="alpha")
        (self.root / "internal/release/upgrade-impact.json").unlink()
        with self.assertRaisesRegex(ReleasePrValidationError, "cannot read"):
            validate_release_pr(self.root, "2.0.0-alpha.3")

    def test_accepts_configured_first_release(self) -> None:
        self.write_fixture(target="1.0.0-alpha.1", channel="alpha")
        message = validate_release_pr(self.root, "0.0.0")
        self.assertIn("0.0.0 -> 1.0.0-alpha.1", message)


if __name__ == "__main__":
    unittest.main()
