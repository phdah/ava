from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
WORKFLOW = (ROOT / ".github/workflows/release-please.yml").read_text()


class PublicationWorkflowTests(unittest.TestCase):
    def test_release_and_pr_maintenance_are_split(self) -> None:
        self.assertGreaterEqual(
            WORKFLOW.count("googleapis/release-please-action@v5"),
            2,
        )
        self.assertIn("skip-github-pull-request: true", WORKFLOW)
        self.assertIn("skip-github-release: true", WORKFLOW)
        self.assertIn("continue-on-error: true", WORKFLOW)
        self.assertNotIn("steps.release.outputs.release_created", WORKFLOW)

    def test_publication_uses_durable_identity_and_acceptance(self) -> None:
        self.assertIn("Resolve durable publication identity", WORKFLOW)
        self.assertIn("python3 -m internal.release.publication", WORKFLOW)
        self.assertIn("internal.release.qualification_acceptance", WORKFLOW)
        self.assertIn("validate-release-pr", WORKFLOW)
        self.assertIn("git rev-list -n 1", WORKFLOW)

    def test_recovery_is_explicit_and_idempotent(self) -> None:
        self.assertIn("workflow_dispatch:", WORKFLOW)
        self.assertIn("release_tag:", WORKFLOW)
        self.assertIn("gh release create", WORKFLOW)
        self.assertIn("Plan idempotent asset recovery", WORKFLOW)
        self.assertIn("python3 -m internal.release.publication", WORKFLOW)
        self.assertIn("release-upload/*", WORKFLOW)
        self.assertNotIn("--clobber", WORKFLOW)
        self.assertIn("gh release verify", WORKFLOW)
        self.assertIn("--json isDraft", WORKFLOW)


if __name__ == "__main__":
    unittest.main()
