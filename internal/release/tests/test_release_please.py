from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from internal.release.validate_pr_title import TitleError, classify

ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "release-please-config.json"
MANIFEST_PATH = ROOT / ".release-please-manifest.json"
FIXTURE_PATH = ROOT / "internal/release/fixtures/release-please-policy.json"
RELEASE_WORKFLOW_PATH = ROOT / ".github/workflows/release-please.yml"
TITLE_WORKFLOW_PATH = ROOT / ".github/workflows/conventional-pr-title.yml"


class ReleasePleasePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(CONFIG_PATH.read_text())
        cls.manifest = json.loads(MANIFEST_PATH.read_text())
        cls.fixture = json.loads(FIXTURE_PATH.read_text())
        cls.release_workflow = RELEASE_WORKFLOW_PATH.read_text()
        cls.title_workflow = TITLE_WORKFLOW_PATH.read_text()

    def test_title_cases(self) -> None:
        for case in self.fixture["title_cases"]:
            with self.subTest(title=case["title"]):
                if not case["valid"]:
                    with self.assertRaises(TitleError):
                        classify(case["title"])
                    continue
                result = classify(case["title"])
                self.assertEqual(result.release_level, case["release_level"])

    def test_bootstrap_and_managed_version_states(self) -> None:
        bootstrap = self.fixture["bootstrap"]
        self.assertRegex(bootstrap["baseline_sha"], r"^[0-9a-f]{40}$")
        self.assertEqual(self.config["bootstrap-sha"], bootstrap["baseline_sha"])
        self.assertEqual(self.config["initial-version"], bootstrap["initial_version"])

        version = (ROOT / "version.txt").read_text().strip()
        if not self.manifest:
            self.assertEqual(version, bootstrap["version_file_sentinel"])
            return

        self.assertEqual(set(self.manifest), {"."})
        self.assertEqual(version, self.manifest["."])
        self.assertNotEqual(version, bootstrap["version_file_sentinel"])

    def test_single_package_draft_release_configuration(self) -> None:
        self.assertEqual(set(self.config["packages"]), {"."})
        self.assertFalse(self.config["separate-pull-requests"])
        self.assertTrue(self.config["draft"])
        self.assertTrue(self.config["force-tag-creation"])
        self.assertTrue(self.config["include-v-in-tag"])
        self.assertFalse(self.config["include-component-in-tag"])
        self.assertNotIn("skip-github-release", self.config)

    def test_release_pr_title_uses_parseable_default(self) -> None:
        self.assertNotIn("pull-request-title-pattern", self.config)
        package = self.config["packages"]["."]
        self.assertEqual(package["component"], "ava")
        self.assertEqual(package["package-name"], "ava")

        title = "chore(main): release ava 1.0.0-alpha.1"
        classification = classify(title)
        self.assertEqual(classification.type, "chore")
        self.assertEqual(classification.scope, "main")
        self.assertIsNone(classification.release_level)

    def test_current_channel_and_planned_transitions(self) -> None:
        channels = {item["name"]: item for item in self.fixture["channels"]}
        self.assertRegex(channels["alpha"]["example"], r"^1\.0\.0-alpha\.[1-9][0-9]*$")
        self.assertRegex(channels["rc"]["example"], r"^1\.0\.0-rc\.[1-9][0-9]*$")
        self.assertEqual(channels["stable"]["example"], "1.0.0")
        for key, value in channels["alpha"]["settings"].items():
            self.assertEqual(self.config[key], value)
        self.assertFalse(channels["stable"]["settings"]["prerelease"])
        self.assertEqual(channels["stable"]["settings"]["versioning"], "default")

    def test_changelog_sections_match_title_policy(self) -> None:
        sections = {item["type"]: item for item in self.config["changelog-sections"]}
        for case in self.fixture["title_cases"]:
            if not case["valid"]:
                continue
            change_type = classify(case["title"]).type
            section = sections[change_type]
            if case["section"] is None:
                self.assertTrue(section["hidden"])
            else:
                self.assertEqual(section["section"], case["section"])
                self.assertFalse(section.get("hidden", False))

    def test_pr_title_check_uses_repository_validator(self) -> None:
        self.assertIn("pull_request:", self.title_workflow)
        self.assertIn("validate_pr_title.py", self.title_workflow)
        self.assertIn("github.event.pull_request.title", self.title_workflow)

    def test_release_workflow_preserves_publication_boundary(self) -> None:
        self.assertIn("googleapis/release-please-action@v5", self.release_workflow)
        self.assertIn("secrets.RELEASE_PLEASE_TOKEN", self.release_workflow)
        self.assertIn("steps.release.outputs.sha", self.release_workflow)
        self.assertIn("git rev-list -n 1", self.release_workflow)
        self.assertIn("internal/release/test.sh", self.release_workflow)
        self.assertEqual(self.release_workflow.count("internal/release/assemble.sh"), 1)
        self.assertIn("for output in release-a release-b", self.release_workflow)
        self.assertIn("actions/attest@v4", self.release_workflow)
        self.assertIn("gh release upload", self.release_workflow)
        self.assertNotIn("--clobber", self.release_workflow)
        self.assertIn("--json isDraft", self.release_workflow)
        self.assertNotRegex(self.release_workflow, re.compile(r"gh release (?:edit|create).*--draft=false"))


if __name__ == "__main__":
    unittest.main()
