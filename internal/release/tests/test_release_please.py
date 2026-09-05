from __future__ import annotations

import json
import unittest
from pathlib import Path

from internal.release.validate_pr_title import TitleError, classify

ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = ROOT / "release-please-config.json"
MANIFEST_PATH = ROOT / ".release-please-manifest.json"
FIXTURE_PATH = ROOT / "internal/release/fixtures/release-please-policy.json"
UPGRADE_POLICY_PATH = ROOT / "internal/release/fixtures/release-upgrade-policy.json"
POLICY_DOC_PATH = ROOT / "internal/release/release-please.md"
RELEASE_WORKFLOW_PATH = ROOT / ".github/workflows/release-please.yml"
PYTHON_WORKFLOW_PATH = ROOT / ".github/workflows/python-tests.yml"
TITLE_WORKFLOW_PATH = ROOT / ".github/workflows/conventional-pr-title.yml"


class ReleasePleasePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(CONFIG_PATH.read_text())
        cls.manifest = json.loads(MANIFEST_PATH.read_text())
        cls.fixture = json.loads(FIXTURE_PATH.read_text())
        cls.upgrade_policy = json.loads(UPGRADE_POLICY_PATH.read_text())
        cls.policy_doc = POLICY_DOC_PATH.read_text()
        cls.release_workflow = RELEASE_WORKFLOW_PATH.read_text()
        cls.python_workflow = PYTHON_WORKFLOW_PATH.read_text()
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

    def test_release_impact_cases_match_documented_policy(self) -> None:
        cases = self.fixture["impact_cases"]
        self.assertEqual(
            {case["expected_type"] for case in cases},
            {"feat", "fix", "test", "docs", "chore"},
        )
        self.assertTrue(any(case["release_level"] == "major" for case in cases))
        self.assertTrue(
            any(
                case["source_scope"] == "internal"
                and case["release_level"] is not None
                for case in cases
            )
        )
        for case in cases:
            with self.subTest(title=case["title"]):
                result = classify(case["title"])
                self.assertEqual(result.type, case["expected_type"])
                self.assertEqual(result.release_level, case["release_level"])
                self.assertIn(f"`{case['title']}`", self.policy_doc)
                if case["impact"] == "repository-only":
                    self.assertIsNone(result.release_level)
        self.assertIn("Select change types from supported distribution impact", self.policy_doc)
        self.assertIn("Implementation novelty alone never justifies `feat`", self.policy_doc)
        self.assertIn("Repository location is not the classification boundary", self.policy_doc)
        self.assertIn("Ava Versioning and Compatibility", self.policy_doc)

    def test_post_bootstrap_managed_version_state(self) -> None:
        version = (ROOT / "version.txt").read_text().strip()
        self.assertEqual(set(self.manifest), {"."})
        self.assertEqual(version, self.manifest["."])
        self.assertRegex(version, r"^[1-9][0-9]*\.[0-9]+\.[0-9]+$")
        self.assertNotEqual(version, "0.0.0")
        self.assertNotIn("bootstrap-sha", self.config)
        self.assertNotIn("initial-version", self.config)
        self.assertNotIn("release-as", self.config["packages"]["."])

    def test_single_package_draft_release_configuration(self) -> None:
        self.assertEqual(set(self.config["packages"]), {"."})
        self.assertFalse(self.config["separate-pull-requests"])
        self.assertTrue(self.config["draft"])
        self.assertTrue(self.config["force-tag-creation"])
        self.assertTrue(self.config["include-v-in-tag"])
        self.assertFalse(self.config["include-component-in-tag"])
        self.assertNotIn("skip-github-release", self.config)
        self.assertNotIn("release-as", self.config["packages"]["."])

    def test_release_pr_footer_requires_merge_commit(self) -> None:
        footer = self.config["pull-request-footer"]
        self.assertIn("merge commit", footer)
        self.assertIn("Do not squash or rebase", footer)
        self.assertIn("accepted qualification is bound", footer)

    def test_current_channel_and_supported_prerelease_examples(self) -> None:
        channels = {item["name"]: item for item in self.fixture["channels"]}
        self.assertRegex(channels["beta"]["example"], r"^2\.0\.0-beta\.[1-9][0-9]*$")
        self.assertRegex(channels["rc"]["example"], r"^2\.0\.0-rc\.[1-9][0-9]*$")
        self.assertEqual(channels["stable"]["example"], "1.0.0")
        for key, value in channels["stable"]["settings"].items():
            if value is None:
                self.assertNotIn(key, self.config)
            else:
                self.assertEqual(self.config[key], value)
        self.assertFalse(self.config["prerelease"])
        self.assertEqual(self.config["versioning"], "default")
        self.assertNotIn("prerelease-type", self.config)

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

    def test_pull_requests_run_release_qualification(self) -> None:
        self.assertIn("pull_request:", self.python_workflow)
        self.assertIn("actions/checkout@v6", self.python_workflow)
        self.assertIn("actions/setup-python@v6", self.python_workflow)
        self.assertIn("internal/release/test.sh", self.python_workflow)
        self.assertNotIn("python -m unittest discover", self.python_workflow)

    def test_release_workflow_qualifies_then_publishes(self) -> None:
        self.assertIn("googleapis/release-please-action@v5", self.release_workflow)
        self.assertIn("secrets.RELEASE_PLEASE_TOKEN", self.release_workflow)
        self.assertIn("steps.release.outputs.sha", self.release_workflow)
        self.assertIn("git rev-list -n 1", self.release_workflow)
        self.assertIn("-m internal.release.validate_release_pr", self.release_workflow)
        self.assertNotIn("-m internal.release.validate_upgrade_impact", self.release_workflow)
        self.assertIn("internal/release/test.sh", self.release_workflow)
        self.assertEqual(self.release_workflow.count("internal/release/assemble.sh"), 1)
        self.assertIn("for output in release-a release-b", self.release_workflow)
        self.assertNotIn("PYTHONPATH:", self.release_workflow)
        self.assertIn("python3 -m internal.release.conformance", self.release_workflow)
        self.assertNotIn("python3 internal/release/conformance.py", self.release_workflow)
        self.assertIn("actions/attest@v4", self.release_workflow)
        self.assertIn("releases/$RELEASE_ID/assets", self.release_workflow)
        self.assertNotIn("gh release upload", self.release_workflow)
        self.assertNotIn("--clobber", self.release_workflow)
        self.assertIn("--json isDraft", self.release_workflow)
        self.assertIn("--method PATCH", self.release_workflow)
        self.assertIn('"repos/$GITHUB_REPOSITORY/releases/$RELEASE_ID"', self.release_workflow)
        self.assertLess(
            self.release_workflow.index("Upload only missing draft assets"),
            self.release_workflow.index("Publish qualified release"),
        )

    def test_release_workflow_has_no_removed_transition_recovery_path(self) -> None:
        removed_tag = "v1.0.0-" + "al" + "pha.19"
        self.assertNotIn(removed_tag, self.release_workflow)
        self.assertNotIn("internal.release.qualification_squash_recovery", self.release_workflow)
        self.assertNotIn("git fetch --no-tags origin", self.release_workflow)

    def test_release_workflow_uses_reviewed_adjacent_catalog(self) -> None:
        self.assertIn("AVA_UPGRADE_CATALOG=internal/release/catalogs/", self.release_workflow)
        self.assertNotIn("AVA_UPGRADE_IMPACT", self.release_workflow)
        self.assertNotIn("internal/release/upgrade-impact.json", self.release_workflow)
        self.assertNotIn("internal/release/upgrade-sources.txt", self.release_workflow)
        self.assertNotIn("--upgrade-from", self.release_workflow)
        self.assertLess(
            self.release_workflow.index("-m internal.release.validate_release_pr"),
            self.release_workflow.index("internal/release/assemble.sh"),
        )

    def test_upgrade_policy_contains_valid_versions(self) -> None:
        import re
        semver_re = re.compile(
            r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
            r"(?:-(alpha|beta|rc)\.[1-9][0-9]*)?$"
        )
        self.assertEqual(self.upgrade_policy["schema_version"], 1)
        self.assertRegex(self.upgrade_policy["initial_release_version"], semver_re)
        self.assertEqual(self.upgrade_policy["initial_release_version"], "1.0.0")
        self.assertEqual(self.upgrade_policy["protected_direct_sources"], [])


if __name__ == "__main__":
    unittest.main()
