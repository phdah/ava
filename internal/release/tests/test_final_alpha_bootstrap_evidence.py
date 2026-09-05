from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE_PATH = ROOT / "internal/release/history/final-alpha-1.0.0-alpha.19.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
EXPECTED_ASSETS = {
    "SHA256SUMS",
    "ava-base.tar.gz",
    "ava-guidance.tar.gz",
    "ava-install.sh",
    "ava-migrations.tar.gz",
    "ava-release-notes.md",
    "ava-release.json",
}


class FinalAlphaBootstrapEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))

    def test_published_final_alpha_identity_is_exact(self) -> None:
        evidence = self.evidence
        published = evidence["published_final_alpha"]
        self.assertEqual(evidence["schema_version"], 1)
        self.assertEqual(evidence["kind"], "stable-bootstrap-final-alpha-evidence")
        self.assertEqual(published["version"], "1.0.0-alpha.19")
        self.assertEqual(published["tag"], "v1.0.0-alpha.19")
        self.assertRegex(published["tag_revision"], REVISION_RE)
        self.assertRegex(published["tag_tree"], REVISION_RE)
        self.assertTrue(published["immutable"])
        self.assertTrue(published["prerelease"])
        self.assertEqual(published["release_id"], 383159767)
        self.assertEqual(published["publication_workflow_run_id"], 33954172775)
        self.assertEqual(set(published["asset_sha256"]), EXPECTED_ASSETS)
        for digest in published["asset_sha256"].values():
            self.assertRegex(digest, SHA256_RE)

    def test_qualification_evidence_is_accepted_and_distinct_from_publication(self) -> None:
        qualification = self.evidence["qualification"]
        published = self.evidence["published_final_alpha"]
        self.assertEqual(qualification["status"], "accepted")
        self.assertEqual(qualification["accepted_by"], "user:phdah")
        self.assertEqual(
            qualification["run_id"],
            "20260905T062356253224Z-alpha18-to-alpha19-local",
        )
        self.assertEqual(qualification["pair_id"], "alpha18-to-alpha19-local")
        self.assertRegex(qualification["qualified_revision"], REVISION_RE)
        self.assertRegex(qualification["execution_identity_sha256"], SHA256_RE)
        self.assertRegex(qualification["driver_sha256"], SHA256_RE)
        self.assertRegex(qualification["matrix_sha256"], SHA256_RE)
        self.assertEqual(set(qualification["qualified_target_asset_sha256"]), EXPECTED_ASSETS)
        self.assertNotEqual(
            qualification["qualified_target_asset_sha256"],
            published["asset_sha256"],
            "published alpha.19 assets must not be conflated with the pre-merge qualification build",
        )

    def test_transition_records_no_new_guidance_or_migrations(self) -> None:
        transition = self.evidence["transition"]
        self.assertFalse(transition["semantic_review_required"])
        self.assertEqual(transition["guidance_paths"], [])
        self.assertEqual(transition["migration_ids"], [])
        self.assertTrue(transition["carry_unresolved_semantic_state"])
        self.assertRegex(transition["edge_sha256"], SHA256_RE)
        for key in (
            "catalog_blob_sha",
            "qualification_config_blob_sha",
            "qualification_pair_catalog_blob_sha",
        ):
            self.assertRegex(transition[key], r"^[0-9a-f]{40}$")

    def test_bootstrap_uses_published_final_alpha_as_source_of_truth(self) -> None:
        bootstrap = self.evidence["stable_bootstrap"]
        published = self.evidence["published_final_alpha"]
        self.assertEqual(bootstrap["source_of_truth"], "published-final-alpha")
        self.assertEqual(
            bootstrap["authoritative_source_revision"],
            published["tag_revision"],
        )
        self.assertEqual(
            bootstrap["authoritative_asset_identity"],
            "published_final_alpha.asset_sha256",
        )
        self.assertIn("before deleting any alpha", bootstrap["destructive_cleanup_guard"])

    def test_recovery_provenance_is_bounded_to_alpha_19_incident(self) -> None:
        recovery = self.evidence["recovery_provenance"]
        published = self.evidence["published_final_alpha"]
        self.assertEqual(recovery["release_pr"], 129)
        self.assertEqual(recovery["recovery_fix_pr"], 130)
        self.assertEqual(recovery["manual_recovery_workflow_run_id"], 33954172775)
        self.assertEqual(recovery["tagged_squash_revision"], published["tag_revision"])
        self.assertEqual(recovery["accepted_release_pr_tree"], published["tag_tree"])


if __name__ == "__main__":
    unittest.main()
