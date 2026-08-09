from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from internal.release.adjacent_edges import AdjacentEdgeError, make_edge, resolve_upgrade
from internal.release.release_catalog import (
    manifest_edges,
    validate_guidance_artifacts,
    validate_release_delta,
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


def catalog(target: str, sources, edges, guidance_items=()):
    return {
        "catalog_schema": 1,
        "target_version": target,
        "supported_sources": list(sources),
        "edges": list(edges),
        "guidance": list(guidance_items),
    }


class ReleaseCatalogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.guidance_root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

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

    def base(self):
        g = self.write_guidance("a1-a2/UPGRADE.md")
        e1 = make_edge(
            "1.0.0-alpha.1",
            "1.0.0-alpha.2",
            guidance_paths=[g["path"]],
            semantic_review_required=True,
            carry_unresolved_semantic_state=True,
        )
        e2 = make_edge(
            "1.0.0-alpha.2",
            "1.0.0-alpha.3",
            carry_unresolved_semantic_state=True,
        )
        return catalog(
            "1.0.0-alpha.3",
            ["1.0.0-alpha.1", "1.0.0-alpha.2"],
            [e1, e2],
            [g],
        )

    def extend(self, prior, target="1.0.0-alpha.4", *, edge=None, guidance_items=()):
        edge = edge or make_edge(prior["target_version"], target, carry_unresolved_semantic_state=True)
        return catalog(
            target,
            [*prior["supported_sources"], prior["target_version"]],
            [*prior["edges"], edge],
            [*prior["guidance"], *guidance_items],
        )

    def test_exactly_one_adjacent_edge_passes(self):
        prior = self.base()
        current = self.extend(prior)
        validate_release_delta(prior, current, guidance_root=self.guidance_root)

    def test_zero_new_edges_fails(self):
        prior = self.base()
        current = dict(prior)
        current["target_version"] = "1.0.0-alpha.4"
        current["supported_sources"] = [*prior["supported_sources"], prior["target_version"]]
        with self.assertRaisesRegex(AdjacentEdgeError, "exactly one"):
            validate_release_delta(prior, current)

    def test_two_new_edges_fails(self):
        prior = self.base()
        current = self.extend(prior)
        current["edges"] = [
            *current["edges"],
            make_edge("1.0.0-alpha.2", "1.0.0-alpha.4"),
        ]
        with self.assertRaisesRegex(AdjacentEdgeError, "exactly one"):
            validate_release_delta(prior, current)

    def test_adjacent_plus_cumulative_shortcut_fails(self):
        prior = self.base()
        current = self.extend(prior)
        current["edges"] = [
            *current["edges"],
            make_edge("1.0.0-alpha.1", "1.0.0-alpha.4"),
        ]
        with self.assertRaises(AdjacentEdgeError):
            validate_release_delta(prior, current)

    def test_skipped_edge_fails(self):
        prior = self.base()
        edge = make_edge("1.0.0-alpha.2", "1.0.0-alpha.4")
        current = catalog(
            "1.0.0-alpha.4",
            [*prior["supported_sources"], prior["target_version"]],
            [*prior["edges"], edge],
            prior["guidance"],
        )
        with self.assertRaisesRegex(AdjacentEdgeError, "immediately previous"):
            validate_release_delta(prior, current)

    def test_mutated_inherited_edge_fails(self):
        prior = self.base()
        current = self.extend(prior)
        current["edges"][0] = make_edge(
            "1.0.0-alpha.1",
            "1.0.0-alpha.2",
            guidance_paths=[prior["guidance"][0]["path"]],
            semantic_review_required=True,
            carry_unresolved_semantic_state=False,
        )
        with self.assertRaisesRegex(AdjacentEdgeError, "mutates inherited edge"):
            validate_release_delta(prior, current)

    def test_mutated_inherited_guidance_metadata_fails(self):
        prior = self.base()
        current = self.extend(prior)
        current["guidance"][0] = {
            **current["guidance"][0],
            "sha256": "1" * 64,
        }
        with self.assertRaisesRegex(AdjacentEdgeError, "mutates inherited guidance"):
            validate_release_delta(prior, current)

    def test_mutated_guidance_artifact_fails(self):
        prior = self.base()
        current = self.extend(prior)
        (self.guidance_root / prior["guidance"][0]["path"]).write_text("changed\n")
        with self.assertRaisesRegex(AdjacentEdgeError, "artifact digest changed"):
            validate_release_delta(prior, current, guidance_root=self.guidance_root)

    def test_copied_cumulative_guidance_fails(self):
        prior = self.base()
        edge = make_edge(
            "1.0.0-alpha.3",
            "1.0.0-alpha.4",
            guidance_paths=[prior["guidance"][0]["path"]],
            semantic_review_required=True,
        )
        current = self.extend(prior, edge=edge)
        with self.assertRaisesRegex(AdjacentEdgeError, "do not copy cumulative guidance"):
            validate_release_delta(prior, current)

    def test_no_impact_edge_is_explicit_and_passes(self):
        prior = self.base()
        current = self.extend(
            prior,
            edge=make_edge(
                "1.0.0-alpha.3",
                "1.0.0-alpha.4",
                semantic_review_required=False,
            ),
        )
        validate_release_delta(prior, current)

    def test_source_retirement_requires_explicit_reason(self):
        prior = self.base()
        current = self.extend(prior)
        current["supported_sources"] = [
            "1.0.0-alpha.2",
            "1.0.0-alpha.3",
        ]
        validate_release_delta(
            prior,
            current,
            retired_sources={"1.0.0-alpha.1": "Support window ended."},
        )

    def test_silent_source_retirement_fails(self):
        prior = self.base()
        current = self.extend(prior)
        current["supported_sources"] = [
            "1.0.0-alpha.2",
            "1.0.0-alpha.3",
        ]
        with self.assertRaisesRegex(AdjacentEdgeError, "silently omitted"):
            validate_release_delta(prior, current)

    def test_three_historical_sources_project_to_direct_manifest_edges(self):
        prior = self.base()
        current = self.extend(prior)
        projections = manifest_edges(current)
        self.assertEqual(
            [
                "1.0.0-alpha.1",
                "1.0.0-alpha.2",
                "1.0.0-alpha.3",
            ],
            [item["from"] for item in projections],
        )
        self.assertEqual(
            [prior["guidance"][0]["path"]],
            projections[0]["guidance_paths"],
        )
        self.assertEqual([], projections[1]["guidance_paths"])
        self.assertTrue(projections[0]["semantic_review_required"])

    def test_semantic_lag_receives_guidance_exactly_once(self):
        prior = self.base()
        current = self.extend(prior)
        resolved = resolve_upgrade(
            current,
            installed_version="1.0.0-alpha.3",
            compatible_through="1.0.0-alpha.1",
            semantic_status="complete",
        )
        self.assertEqual(
            [prior["guidance"][0]["guidance_id"]],
            [item["guidance_id"] for item in resolved.effective_guidance],
        )

    def test_channel_neutral_stable_edge(self):
        prior = catalog(
            "2.0.0-rc.1",
            ["2.0.0-beta.1"],
            [make_edge("2.0.0-beta.1", "2.0.0-rc.1")],
        )
        current = catalog(
            "2.0.0",
            ["2.0.0-beta.1", "2.0.0-rc.1"],
            [
                *prior["edges"],
                make_edge("2.0.0-rc.1", "2.0.0"),
            ],
        )
        validate_release_delta(prior, current)


if __name__ == "__main__":
    unittest.main()
