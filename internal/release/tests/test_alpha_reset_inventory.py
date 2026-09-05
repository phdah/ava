from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INVENTORY_PATH = ROOT / "internal/release/history/alpha-reset-inventory.json"
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")
ALPHA_TAG_RE = re.compile(r"^v1\.0\.0-alpha\.(\d+)$")
ALPHA_REF_RE = re.compile(r"^refs/tags/v1\.0\.0-alpha\.(\d+)$")


class AlphaResetInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))

    def test_inventory_identity_and_counts_are_exact(self) -> None:
        inventory = self.inventory
        reconciliation = inventory["reconciliation"]
        self.assertEqual(inventory["schema_version"], 1)
        self.assertEqual(inventory["kind"], "alpha-public-reset-inventory")
        self.assertRegex(inventory["capture_repository_revision"], REVISION_RE)
        self.assertEqual(reconciliation["alpha_release_object_count"], 19)
        self.assertEqual(reconciliation["alpha_tag_ref_count"], 19)
        self.assertEqual(reconciliation["published_release_count"], 17)
        self.assertEqual(reconciliation["stale_draft_release_count"], 2)
        self.assertEqual(reconciliation["release_collection_exhausted_after_object_count"], 19)
        self.assertTrue(reconciliation["all_release_objects_are_alpha"])
        self.assertTrue(reconciliation["all_tag_refs_are_alpha"])
        self.assertEqual(len(inventory["release_objects"]), 19)
        self.assertEqual(len(inventory["tag_refs"]), 19)

    def test_tag_refs_are_exact_alpha_1_through_19(self) -> None:
        refs = self.inventory["tag_refs"]
        versions = []
        revisions = set()
        for entry in refs:
            match = ALPHA_REF_RE.fullmatch(entry["ref"])
            self.assertIsNotNone(match)
            versions.append(int(match.group(1)))
            self.assertRegex(entry["revision"], REVISION_RE)
            revisions.add(entry["revision"])
        self.assertEqual(versions, list(range(1, 20)))
        self.assertEqual(len(revisions), 19)

    def test_release_objects_are_only_alpha_and_ids_are_unique(self) -> None:
        releases = self.inventory["release_objects"]
        release_ids = [entry["release_id"] for entry in releases]
        self.assertEqual(len(release_ids), len(set(release_ids)))
        versions = []
        for entry in releases:
            match = ALPHA_TAG_RE.fullmatch(entry["tag_name"])
            self.assertIsNotNone(match)
            versions.append(int(match.group(1)))
            self.assertTrue(entry["prerelease"])
            self.assertRegex(entry["target_commitish"], REVISION_RE)
        self.assertEqual(versions, list(range(1, 20)))

    def test_published_alpha_3_through_19_match_tag_revisions(self) -> None:
        tag_revisions = {
            entry["ref"].removeprefix("refs/tags/"): entry["revision"]
            for entry in self.inventory["tag_refs"]
        }
        published = [
            entry for entry in self.inventory["release_objects"] if entry["state"] == "published"
        ]
        self.assertEqual(len(published), 17)
        self.assertEqual(
            [int(ALPHA_TAG_RE.fullmatch(entry["tag_name"]).group(1)) for entry in published],
            list(range(3, 20)),
        )
        for entry in published:
            self.assertFalse(entry["draft"])
            self.assertTrue(entry["immutable"])
            self.assertEqual(entry["target_commitish"], tag_revisions[entry["tag_name"]])

    def test_alpha_1_and_2_are_stale_drafts_with_distinct_tag_targets(self) -> None:
        drafts = [
            entry for entry in self.inventory["release_objects"] if entry["state"] == "stale-draft"
        ]
        self.assertEqual([entry["tag_name"] for entry in drafts], ["v1.0.0-alpha.1", "v1.0.0-alpha.2"])
        self.assertTrue(all(entry["draft"] for entry in drafts))
        self.assertTrue(all(not entry["immutable"] for entry in drafts))

        mismatches = self.inventory["stale_draft_mismatches"]
        self.assertEqual([entry["tag_name"] for entry in mismatches], ["v1.0.0-alpha.1", "v1.0.0-alpha.2"])
        for mismatch in mismatches:
            self.assertRegex(mismatch["release_target_commitish"], REVISION_RE)
            self.assertRegex(mismatch["tag_revision"], REVISION_RE)
            self.assertNotEqual(mismatch["release_target_commitish"], mismatch["tag_revision"])

    def test_deletion_policy_is_exact_id_and_exact_ref_only(self) -> None:
        policy = self.inventory["selection_policy"]
        self.assertIn("exact GitHub Release IDs", policy["release_objects"])
        self.assertIn("exact refs", policy["tag_refs"])
        self.assertIn("Fail closed", policy["tag_refs"])


if __name__ == "__main__":
    unittest.main()
