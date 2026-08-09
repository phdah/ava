from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from internal.release.adjacent_edges import AdjacentEdgeError, make_edge, resolve_upgrade
from internal.release.release_catalog import (
    append_release,
    initial_catalog,
    manifest_edges,
    read_catalog,
    read_release_chain,
    validate_guidance_artifacts,
    validate_release_record,
)


def guidance(guidance_id: str, path: str, source: str, target: str, content: bytes):
    return {
        "guidance_id": guidance_id,
        "path": path,
        "from_version": source,
        "to_version": target,
        "supersedes": [],
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def record(edge, guidance_items=(), retirements=()):
    return {
        "catalog_schema": 1,
        "target_version": edge["to"],
        "edge": edge,
        "guidance": list(guidance_items),
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


class ReleaseCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.catalog_dir = self.root / "internal/release/catalogs"
        self.guidance_root = self.root / "internal/release/guidance"
        self.catalog_dir.mkdir(parents=True)
        self.guidance_root.mkdir(parents=True)

    def tearDown(self):
        self.temp.cleanup()

    def write_record(self, value) -> None:
        target = value["target_version"]
        (self.catalog_dir / f"{target}.json").write_text(json.dumps(value))

    def write_guidance(self, path: str, content: bytes = b"guidance\n") -> dict:
        target = self.guidance_root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return guidance(
            path.replace("/", "-"),
            path,
            "1.0.0-alpha.1",
            "1.0.0-alpha.2",
            content,
        )

    def write_chain(self):
        item = self.write_guidance("a1-a2/UPGRADE.md")
        records = [
            bootstrap_record("1.0.0-alpha.1"),
            record(
                make_edge(
                    "1.0.0-alpha.1",
                    "1.0.0-alpha.2",
                    guidance_paths=[item["path"]],
                    semantic_review_required=True,
                    carry_unresolved_semantic_state=True,
                ),
                [item],
            ),
            record(
                make_edge(
                    "1.0.0-alpha.2",
                    "1.0.0-alpha.3",
                    carry_unresolved_semantic_state=True,
                )
            ),
            record(
                make_edge(
                    "1.0.0-alpha.3",
                    "1.0.0-alpha.4",
                    carry_unresolved_semantic_state=True,
                )
            ),
        ]
        for value in records:
            self.write_record(value)
        return item, records

    def test_every_release_file_contains_only_its_own_edge(self):
        _, records = self.write_chain()
        chain = read_release_chain(self.root, "1.0.0-alpha.4")
        self.assertEqual(records, list(chain))
        self.assertEqual(
            [
                ("0.0.0", "1.0.0-alpha.1"),
                ("1.0.0-alpha.1", "1.0.0-alpha.2"),
                ("1.0.0-alpha.2", "1.0.0-alpha.3"),
                ("1.0.0-alpha.3", "1.0.0-alpha.4"),
            ],
            [(item["edge"]["from"], item["edge"]["to"]) for item in chain],
        )

    def test_recursive_chain_composes_supported_sources(self):
        self.write_chain()
        catalog = read_catalog(self.root, "1.0.0-alpha.4")
        self.assertEqual(
            ["1.0.0-alpha.1", "1.0.0-alpha.2", "1.0.0-alpha.3"],
            catalog["supported_sources"],
        )
        self.assertEqual(4, len(catalog["edges"]))

    def test_first_published_release_requires_bootstrap_edge_record(self):
        with self.assertRaisesRegex(AdjacentEdgeError, "missing release catalog record"):
            read_catalog(self.root, "1.0.0-alpha.1")

    def test_missing_any_intermediate_release_record_fails(self):
        _, records = self.write_chain()
        (self.catalog_dir / "1.0.0-alpha.2.json").unlink()
        with self.assertRaisesRegex(AdjacentEdgeError, "missing release catalog record"):
            read_catalog(self.root, records[-1]["target_version"])

    def test_wrong_previous_release_fails(self):
        base = initial_catalog()
        skipped = record(make_edge("1.0.0-alpha.1", "1.0.0-alpha.2"))
        with self.assertRaisesRegex(AdjacentEdgeError, "immediately previous"):
            append_release(base, skipped)

    def test_record_rejects_more_than_edge_local_guidance(self):
        item = self.write_guidance("a1-a2/UPGRADE.md")
        value = record(make_edge("1.0.0-alpha.1", "1.0.0-alpha.2"), [item])
        with self.assertRaisesRegex(AdjacentEdgeError, "exactly the guidance"):
            validate_release_record(value)

    def test_guidance_artifact_digest_is_immutable(self):
        item, records = self.write_chain()
        validate_guidance_artifacts(records[1], self.guidance_root)
        (self.guidance_root / item["path"]).write_text("changed\n")
        with self.assertRaisesRegex(AdjacentEdgeError, "artifact digest changed"):
            validate_guidance_artifacts(records[1], self.guidance_root)

    def test_bootstrap_sentinel_must_be_retired_by_first_release(self):
        self.write_record(record(make_edge("0.0.0", "1.0.0-alpha.1")))
        catalog = read_catalog(self.root, "1.0.0-alpha.1")
        self.assertEqual(["0.0.0"], catalog["supported_sources"])
        self.assertNotEqual([], catalog["supported_sources"])

    def test_bootstrap_sentinel_can_be_retired_by_first_release(self):
        self.write_record(bootstrap_record("1.0.0-alpha.1"))
        catalog = read_catalog(self.root, "1.0.0-alpha.1")
        self.assertEqual([], catalog["supported_sources"])

    def test_release_local_retirement_removes_inherited_source(self):
        self.write_record(bootstrap_record("1.0.0-alpha.1"))
        self.write_record(
            record(make_edge("1.0.0-alpha.1", "1.0.0-alpha.2"))
        )
        self.write_record(
            record(
                make_edge("1.0.0-alpha.2", "1.0.0-alpha.3"),
                retirements=[
                    {
                        "version": "1.0.0-alpha.1",
                        "reason": "Support window ended.",
                    }
                ],
            )
        )
        catalog = read_catalog(self.root, "1.0.0-alpha.3")
        self.assertEqual(["1.0.0-alpha.2"], catalog["supported_sources"])

    def test_unknown_retirement_fails(self):
        base = initial_catalog()
        value = record(
            make_edge("0.0.0", "1.0.0-alpha.1"),
            retirements=[
                {"version": "0.9.0", "reason": "Not supported."}
            ],
        )
        with self.assertRaisesRegex(AdjacentEdgeError, "not inherited"):
            append_release(base, value)

    def test_non_bootstrap_previous_release_cannot_be_retired(self):
        value = record(
            make_edge("1.0.0-alpha.1", "1.0.0-alpha.2"),
            retirements=[
                {"version": "1.0.0-alpha.1", "reason": "No longer supported."}
            ],
        )
        with self.assertRaisesRegex(AdjacentEdgeError, "immediately previous"):
            validate_release_record(value)

    def test_three_historical_sources_project_to_direct_manifest_edges(self):
        item, _ = self.write_chain()
        catalog = read_catalog(self.root, "1.0.0-alpha.4")
        projections = manifest_edges(catalog)
        self.assertEqual(
            ["1.0.0-alpha.1", "1.0.0-alpha.2", "1.0.0-alpha.3"],
            [entry["from"] for entry in projections],
        )
        self.assertEqual([item["path"]], projections[0]["guidance_paths"])
        self.assertEqual([], projections[1]["guidance_paths"])
        self.assertTrue(projections[0]["semantic_review_required"])

    def test_semantic_lag_receives_guidance_exactly_once(self):
        item, _ = self.write_chain()
        catalog = read_catalog(self.root, "1.0.0-alpha.4")
        resolved = resolve_upgrade(
            catalog,
            installed_version="1.0.0-alpha.3",
            compatible_through="1.0.0-alpha.1",
            semantic_status="complete",
        )
        self.assertEqual(
            [item["guidance_id"]],
            [entry["guidance_id"] for entry in resolved.effective_guidance],
        )

    def test_channel_neutral_stable_edge(self):
        catalog = append_release(
            initial_catalog(),
            bootstrap_record("2.0.0-rc.1"),
        )
        current = append_release(
            catalog,
            record(make_edge("2.0.0-rc.1", "2.0.0")),
        )
        self.assertEqual("2.0.0", current["target_version"])
        self.assertEqual(["2.0.0-rc.1"], current["supported_sources"])


if __name__ == "__main__":
    unittest.main()
