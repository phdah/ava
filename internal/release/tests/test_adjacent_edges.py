from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from internal.release.adjacent_edges import (
    AdjacentEdgeError,
    compose_guidance,
    inherit_catalog,
    make_edge,
    resolve_unique_path,
    resolve_upgrade,
    validate_catalog,
)


def guidance(guidance_id: str, path: str, source: str, target: str, supersedes=()):
    return {
        "guidance_id": guidance_id,
        "path": path,
        "from_version": source,
        "to_version": target,
        "supersedes": list(supersedes),
        "sha256": hashlib.sha256(path.encode()).hexdigest(),
    }


class AdjacentEdgeTests(unittest.TestCase):
    def catalog(self):
        g1 = guidance("g-1", "edges/a1-a2.md", "1.0.0", "1.0.1")
        e1 = make_edge(
            "1.0.0",
            "1.0.1",
            guidance_paths=[g1["path"]],
            semantic_review_required=True,
            carry_unresolved_semantic_state=True,
        )
        e2 = make_edge(
            "1.0.1",
            "1.0.2",
            carry_unresolved_semantic_state=True,
        )
        return validate_catalog(
            {
                "catalog_schema": 1,
                "target_version": "1.0.2",
                "supported_sources": ["1.0.0", "1.0.1"],
                "edges": [e1, e2],
                "guidance": [g1],
            }
        )

    def test_repository_fixture_is_valid(self):
        root = Path(__file__).resolve().parents[3]
        fixture = json.loads(
            (root / "internal/release/fixtures/adjacent-upgrade-catalog.json").read_text()
        )
        validated = validate_catalog(fixture)
        self.assertEqual("1.0.2", validated["target_version"])
        self.assertEqual(2, len(validated["edges"]))

    def test_resolves_direct_and_multi_edge_paths(self):
        catalog = self.catalog()
        self.assertEqual(
            1,
            len(
                resolve_unique_path(
                    catalog["edges"], "1.0.1", "1.0.2"
                )
            ),
        )
        self.assertEqual(
            2,
            len(
                resolve_unique_path(
                    catalog["edges"], "1.0.0", "1.0.2"
                )
            ),
        )

    def test_rejects_gap(self):
        with self.assertRaisesRegex(AdjacentEdgeError, "no upgrade path"):
            validate_catalog(
                {
                    "catalog_schema": 1,
                    "target_version": "1.0.2",
                    "supported_sources": ["1.0.0"],
                    "edges": [make_edge("1.0.1", "1.0.2")],
                    "guidance": [],
                }
            )

    def test_rejects_ambiguous_paths(self):
        edges = [
            make_edge("1.0.0", "1.0.1"),
            make_edge("1.0.0", "1.1.0"),
            make_edge("1.0.1", "2.0.0"),
            make_edge("1.1.0", "2.0.0"),
        ]
        with self.assertRaisesRegex(AdjacentEdgeError, "ambiguous"):
            resolve_unique_path(edges, "1.0.0", "2.0.0")

    def test_rejects_tampered_edge_digest(self):
        edge = make_edge("1.0.0", "1.0.1")
        edge["carry_unresolved_semantic_state"] = True
        with self.assertRaisesRegex(AdjacentEdgeError, "does not match"):
            validate_catalog(
                {
                    "catalog_schema": 1,
                    "target_version": "1.0.1",
                    "supported_sources": ["1.0.0"],
                    "edges": [edge],
                    "guidance": [],
                }
            )

    def test_inherits_prior_edges_without_reauthoring(self):
        prior = self.catalog()
        extended = inherit_catalog(
            prior,
            make_edge(
                "1.0.2",
                "1.0.3",
                carry_unresolved_semantic_state=True,
            ),
        )
        self.assertEqual(
            [edge["edge_sha256"] for edge in prior["edges"]],
            [edge["edge_sha256"] for edge in extended["edges"][:2]],
        )
        self.assertIn("1.0.2", extended["supported_sources"])

    def test_requires_explicit_retirement_for_inherited_source(self):
        prior = self.catalog()
        with self.assertRaisesRegex(AdjacentEdgeError, "omitted"):
            inherit_catalog(
                prior,
                make_edge("1.0.2", "1.0.3"),
                supported_sources=["1.0.1", "1.0.2"],
            )
        extended = inherit_catalog(
            prior,
            make_edge("1.0.2", "1.0.3"),
            retired_sources=["1.0.0"],
        )
        self.assertNotIn("1.0.0", extended["supported_sources"])

    def test_resolves_managed_and_semantic_paths_separately(self):
        catalog = self.catalog()
        resolved = resolve_upgrade(
            catalog,
            installed_version="1.0.1",
            compatible_through="1.0.0",
            semantic_status="complete",
        )
        self.assertEqual(1, len(resolved.managed_path))
        self.assertEqual(2, len(resolved.semantic_path))
        self.assertEqual(
            ["g-1"],
            [item["guidance_id"] for item in resolved.effective_guidance],
        )
        self.assertTrue(resolved.semantic_review_required)
        self.assertFalse(resolved.may_advance_compatibility_mechanically)

    def test_no_guidance_path_advances_compatibility_mechanically(self):
        edge = make_edge("2.0.0", "2.0.1")
        catalog = validate_catalog(
            {
                "catalog_schema": 1,
                "target_version": "2.0.1",
                "supported_sources": ["2.0.0"],
                "edges": [edge],
                "guidance": [],
            }
        )
        resolved = resolve_upgrade(
            catalog,
            installed_version="2.0.0",
            compatible_through="2.0.0",
            semantic_status="complete",
        )
        self.assertTrue(resolved.may_advance_compatibility_mechanically)
        self.assertFalse(resolved.semantic_review_required)

    def test_unresolved_semantic_state_requires_every_edge_to_allow_carry(self):
        edge = make_edge(
            "2.0.0",
            "2.0.1",
            carry_unresolved_semantic_state=False,
        )
        catalog = validate_catalog(
            {
                "catalog_schema": 1,
                "target_version": "2.0.1",
                "supported_sources": ["2.0.0"],
                "edges": [edge],
                "guidance": [],
            }
        )
        with self.assertRaisesRegex(AdjacentEdgeError, "does not permit"):
            resolve_upgrade(
                catalog,
                installed_version="2.0.0",
                compatible_through="2.0.0",
                semantic_status="partial",
            )

    def test_guidance_supersession_is_ordered_and_effective_once(self):
        g1 = guidance(
            "old-rule",
            "g/old.md",
            "1.0.0",
            "1.0.1",
        )
        g2 = guidance(
            "new-rule",
            "g/new.md",
            "1.0.1",
            "1.0.2",
            supersedes=["old-rule"],
        )
        path = [
            make_edge(
                "1.0.0",
                "1.0.1",
                guidance_paths=[g1["path"]],
                semantic_review_required=True,
            ),
            make_edge(
                "1.0.1",
                "1.0.2",
                guidance_paths=[g2["path"]],
                semantic_review_required=True,
            ),
        ]
        effective = compose_guidance(path, [g1, g2])
        self.assertEqual(
            ["new-rule"],
            [item["guidance_id"] for item in effective],
        )

    def test_rejects_duplicate_guidance_application(self):
        g1 = guidance(
            "rule",
            "g/rule.md",
            "1.0.0",
            "1.0.1",
        )
        edge = make_edge(
            "1.0.0",
            "1.0.1",
            guidance_paths=[g1["path"]],
            semantic_review_required=True,
        )
        with self.assertRaisesRegex(AdjacentEdgeError, "more than once"):
            compose_guidance([edge, edge], [g1])

    def test_model_is_channel_agnostic(self):
        catalog = validate_catalog(
            {
                "catalog_schema": 1,
                "target_version": "2.0.0",
                "supported_sources": [
                    "2.0.0-alpha.9",
                    "2.0.0-beta.1",
                    "2.0.0-rc.1",
                ],
                "edges": [
                    make_edge("2.0.0-alpha.9", "2.0.0-beta.1"),
                    make_edge("2.0.0-beta.1", "2.0.0-rc.1"),
                    make_edge("2.0.0-rc.1", "2.0.0"),
                ],
                "guidance": [],
            }
        )
        self.assertEqual(
            3,
            len(
                resolve_unique_path(
                    catalog["edges"], "2.0.0-alpha.9", "2.0.0"
                )
            ),
        )


if __name__ == "__main__":
    unittest.main()
