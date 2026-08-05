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

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_fixture(
        self,
        *,
        target: str,
        sources: list[str],
        transitions: list[dict[str, object]],
    ) -> None:
        (self.root / "version.txt").write_text(f"{target}\n")
        (self.root / ".release-please-manifest.json").write_text(
            json.dumps({".": target})
        )
        (self.root / "internal/release/upgrade-sources.txt").write_text(
            "".join(f"{source}\n" for source in sources)
        )
        policy = {
            "prerelease_support": {
                "first_alpha": {"version": "1.0.0-alpha.1"},
                "transitions": transitions,
            }
        }
        matrix = {"prerelease_transitions": transitions}
        (self.root / "internal/release/fixtures/alpha-qualification.json").write_text(
            json.dumps(policy)
        )
        (self.root / "internal/release/fixtures/conformance-matrix.json").write_text(
            json.dumps(matrix)
        )

    @staticmethod
    def transition(source: str, target: str) -> dict[str, object]:
        return {
            "from": source,
            "to": target,
            "channel": "alpha",
            "must_be_declared": True,
        }

    def test_rejects_stale_sources_for_new_prerelease(self) -> None:
        self.write_fixture(
            target="1.0.0-alpha.6",
            sources=["1.0.0-alpha.3", "1.0.0-alpha.4"],
            transitions=[
                self.transition("1.0.0-alpha.3", "1.0.0-alpha.5"),
                self.transition("1.0.0-alpha.4", "1.0.0-alpha.5"),
            ],
        )
        with self.assertRaisesRegex(
            ReleasePrValidationError,
            "must include the current main version 1.0.0-alpha.5",
        ):
            validate_release_pr(self.root, "1.0.0-alpha.5")

    def test_accepts_matching_prerelease_edge(self) -> None:
        transition = self.transition("1.0.0-alpha.5", "1.0.0-alpha.6")
        self.write_fixture(
            target="1.0.0-alpha.6",
            sources=["1.0.0-alpha.5"],
            transitions=[transition],
        )
        message = validate_release_pr(self.root, "1.0.0-alpha.5")
        self.assertIn("1.0.0-alpha.5 -> 1.0.0-alpha.6", message)

    def test_rejects_fixture_and_source_mismatch(self) -> None:
        transition = self.transition("1.0.0-alpha.5", "1.0.0-alpha.6")
        self.write_fixture(
            target="1.0.0-alpha.6",
            sources=["1.0.0-alpha.5", "1.0.0-alpha.4"],
            transitions=[transition],
        )
        with self.assertRaisesRegex(
            ReleasePrValidationError,
            "does not exactly match the declared transitions",
        ):
            validate_release_pr(self.root, "1.0.0-alpha.5")

    def test_accepts_stable_patch_with_previous_version(self) -> None:
        self.write_fixture(
            target="1.0.1",
            sources=["1.0.0"],
            transitions=[],
        )
        message = validate_release_pr(self.root, "1.0.0")
        self.assertIn("1.0.0 -> 1.0.1", message)

    def test_first_alpha_requires_empty_upgrade_sources(self) -> None:
        self.write_fixture(
            target="1.0.0-alpha.1",
            sources=[],
            transitions=[],
        )
        message = validate_release_pr(self.root, "0.0.0")
        self.assertIn("first alpha", message)


if __name__ == "__main__":
    unittest.main()
