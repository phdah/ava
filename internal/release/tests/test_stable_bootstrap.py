from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from internal.release.stable_bootstrap import (
    StableBootstrapError,
    load_bootstrap,
    reconstruct_source_assets,
    verify_alpha_empty,
    verify_alpha_reset,
)

ROOT = Path(__file__).resolve().parents[3]
INVENTORY_PATH = ROOT / "internal/release/history/alpha-reset-inventory.json"
RESET_WORKFLOW = ROOT / ".github/workflows/stable-alpha-reset.yml"
QUALIFICATION_RUNNER = ROOT / "internal/release/run-release-qualification.sh"


class StableBootstrapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = json.loads(INVENTORY_PATH.read_text())

    def test_bootstrap_is_exactly_alpha19_to_stable_100(self) -> None:
        config, evidence = load_bootstrap(ROOT)
        self.assertTrue(config["enabled"])
        self.assertTrue(config["alpha_reset_requested"])
        self.assertEqual(config["source_version"], "1.0.0-alpha.19")
        self.assertEqual(config["source_tag"], "v1.0.0-alpha.19")
        self.assertEqual(
            config["source_revision"],
            "4aeb06b4292b9c768ea745ca5989e94c24d4be7c",
        )
        self.assertEqual(config["target_version"], "1.0.0")
        self.assertEqual(
            evidence["published_final_alpha"]["tag_revision"],
            config["source_revision"],
        )

    def test_reconstructs_exact_published_final_alpha_assets(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "assets"
            reconstruct_source_assets(ROOT, output)
            expected = self.inventory["release_objects"][-1]
            self.assertEqual(expected["tag_name"], "v1.0.0-alpha.19")
            self.assertEqual(expected["state"], "published")
            self.assertEqual(len(list(output.iterdir())), 7)

    def test_frozen_inventory_accepts_only_exact_live_state(self) -> None:
        releases = [
            {
                "id": item["release_id"],
                "tag_name": item["tag_name"],
                "target_commitish": item["target_commitish"],
                "draft": item["draft"],
                "prerelease": item["prerelease"],
                "immutable": item["immutable"],
            }
            for item in self.inventory["release_objects"]
        ]
        refs = [
            {"ref": item["ref"], "object": {"sha": item["revision"]}}
            for item in self.inventory["tag_refs"]
        ]
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            releases_path = root / "releases.json"
            refs_path = root / "refs.json"
            releases_path.write_text(json.dumps([releases]))
            refs_path.write_text(json.dumps([refs]))
            verify_alpha_reset(ROOT, releases_path, refs_path)

            refs[0]["object"]["sha"] = "0" * 40
            refs_path.write_text(json.dumps([refs]))
            with self.assertRaisesRegex(
                StableBootstrapError,
                "alpha tag refs no longer match",
            ):
                verify_alpha_reset(ROOT, releases_path, refs_path)

    def test_zero_alpha_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            releases = root / "releases.json"
            refs = root / "refs.json"
            releases.write_text("[[]]\n")
            refs.write_text("[[]]\n")
            verify_alpha_empty(releases, refs)

            releases.write_text('[ [{"tag_name":"v1.0.0-alpha.19"}] ]')
            with self.assertRaisesRegex(StableBootstrapError, "alpha reset incomplete"):
                verify_alpha_empty(releases, refs)

    def test_reset_workflow_enforces_release_then_tag_order(self) -> None:
        workflow = RESET_WORKFLOW.read_text()
        release_delete = workflow.index("Delete exactly the frozen alpha Release objects")
        tag_delete = workflow.index("Delete exactly the frozen alpha tag refs")
        empty_verify = workflow.index("Verify zero alpha Releases and tags remain")
        self.assertLess(release_delete, tag_delete)
        self.assertLess(tag_delete, empty_verify)
        self.assertIn("verify-alpha-reset", workflow)
        self.assertIn("alpha-reset-inventory.json", workflow)
        self.assertIn("secrets.RELEASE_PLEASE_TOKEN", workflow)

    def test_qualification_reconstructs_only_the_stable_bootstrap_source(self) -> None:
        runner = QUALIFICATION_RUNNER.read_text()
        self.assertIn('source_tag" = "v1.0.0-alpha.19', runner)
        self.assertIn('target_version" = "1.0.0', runner)
        self.assertIn("internal.release.stable_bootstrap", runner)
        self.assertIn("source-assets", runner)
        self.assertIn("gh release download", runner)


if __name__ == "__main__":
    unittest.main()
