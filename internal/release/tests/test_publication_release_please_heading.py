from __future__ import annotations

import unittest

from internal.release.publication import extract_release_notes


class ReleasePleaseHeadingTests(unittest.TestCase):
    def test_extracts_unbracketed_release_please_heading(self) -> None:
        changelog = (
            "# Changelog\n\n"
            "## 1.0.0 (2026-09-05)\n\n"
            "### Features\n\n* stable root\n\n"
            "## Changelog\n\n"
            "Release Please footer.\n"
        )
        self.assertEqual(
            extract_release_notes(changelog, "1.0.0"),
            "## 1.0.0 (2026-09-05)\n\n"
            "### Features\n\n* stable root\n",
        )

    def test_stable_version_does_not_match_prerelease_heading(self) -> None:
        changelog = "# Changelog\n\n## 1.0.0-rc.1 (2026-09-05)\n\n* candidate\n"
        with self.assertRaisesRegex(ValueError, "no release section for 1.0.0"):
            extract_release_notes(changelog, "1.0.0")


if __name__ == "__main__":
    unittest.main()
