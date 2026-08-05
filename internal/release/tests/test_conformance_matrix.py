from __future__ import annotations

import ast
import json
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
MATRIX = SOURCE_ROOT / "internal/release/fixtures/conformance-matrix.json"


class ConformanceMatrixTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.matrix = json.loads(MATRIX.read_text())
        cls.cases = {case["id"]: case for case in cls.matrix["cases"]}

    def test_matrix_schema_and_case_ids_are_stable(self) -> None:
        self.assertEqual(self.matrix["schema_version"], 1)
        self.assertEqual(
            self.matrix["finding_severities"],
            ["error", "warning", "recommendation"],
        )
        self.assertEqual(len(self.cases), len(self.matrix["cases"]))
        for case in self.cases.values():
            self.assertTrue(
                {"id", "area", "expected", "evidence"}.issubset(case),
                case["id"],
            )
            self.assertFalse(
                set(case) - {"id", "area", "expected", "evidence", "fixture_kind", "rules", "notes"},
                case["id"],
            )
            self.assertTrue(case["area"], case["id"])
            self.assertTrue(case["expected"], case["id"])
            self.assertTrue(case["evidence"], case["id"])
            self.assertTrue(all("/" in item for item in case["evidence"]), case["id"])

    def test_evidence_references_resolve(self) -> None:
        for case in self.cases.values():
            for reference in case["evidence"]:
                path_value, separator, selector = reference.partition("::")
                path = SOURCE_ROOT / path_value
                self.assertTrue(path.exists(), f"{case['id']}: missing evidence {path_value}")
                if not separator:
                    continue
                if path.suffix == ".py":
                    tree = ast.parse(path.read_text())
                    names = {
                        node.name
                        for node in ast.walk(tree)
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
                    }
                    self.assertIn(selector, names, f"{case['id']}: missing test {reference}")
                elif path.suffix == ".json":
                    value = json.loads(path.read_text())
                    case_ids = {
                        item["id"]
                        for item in value.get("cases", [])
                        if isinstance(item, dict) and isinstance(item.get("id"), str)
                    }
                    self.assertIn(selector, case_ids, f"{case['id']}: missing fixture case {reference}")

    def test_required_conformance_areas_are_present(self) -> None:
        expected = {
            "structure",
            "metadata",
            "discovery",
            "roles",
            "workflows",
            "boundary",
            "installation",
            "managed-integrity",
            "managed-state",
            "routing",
            "filesystem-safety",
            "transaction",
            "migration",
            "semantic",
            "role-routing",
            "ownership",
            "maintenance",
            "uninstall",
            "host",
            "release",
            "trust",
            "upgrade-graph",
            "publication",
        }
        self.assertTrue(expected.issubset({case["area"] for case in self.cases.values()}))

    def test_required_scenarios_are_present(self) -> None:
        required = {
            "repository-minimal-valid",
            "frontmatter-missing",
            "internal-link-missing",
            "installed-link-missing",
            "installed-link-root-escape",
            "role-required-file-missing",
            "workflow-primary-role-missing",
            "duplicate-identifier",
            "orphaned-document",
            "deprecated-reference",
            "internal-content-leakage",
            "fresh-install-minimal",
            "fresh-install-complete-base",
            "non-empty-project-preserved",
            "pre-existing-root-router-refused",
            "unknown-historical-ava-refused",
            "managed-file-modified",
            "managed-file-missing",
            "managed-file-unexpected",
            "manifest-malformed",
            "journal-malformed",
            "parent-traversal-refused",
            "symlink-escape-refused",
            "unsafe-archive-entry-refused",
            "out-of-root-write-refused",
            "dry-run-no-mutation",
            "grouped-change-partial-apply-prevented",
            "post-validation-failure-rollback",
            "migration-success",
            "migration-failure",
            "migration-interruption-resume",
            "migration-interruption-abort",
            "migration-interruption-rollback",
            "migration-finalization",
            "semantic-pending",
            "semantic-partial",
            "semantic-blocked",
            "semantic-complete",
            "installed-new-base-compatible-through-old",
            "maintenance-pre-routing-deterministic",
            "upgrade-pre-routing-semantic",
            "semantic-completion-inconsistent-files",
            "project-owned-content-not-managed",
            "uninstall-healthy",
            "uninstall-active-work-refused",
            "uninstall-uncertain-ownership-refused",
            "uninstall-preserves-project-owned",
            "opencode-default-config",
            "opencode-existing-config-preserved",
            "opencode-permission-missing",
            "host-neutral-explicit-discovery",
            "unsupported-named-host-not-claimed",
            "release-asset-inventory",
            "release-asset-checksum-mismatch",
            "release-manifest-asset-metadata",
            "convenience-bootstrap-trust",
            "verified-bootstrap-success",
            "verified-bootstrap-attestation-failure",
            "exact-tag-selection",
            "alpha-to-alpha",
            "alpha-to-rc",
            "rc-to-stable",
            "direct-upgrade",
            "chained-upgrade",
            "release-immutability-disabled",
            "published-release-not-immutable",
        }
        self.assertTrue(required.issubset(self.cases))

    def test_prerelease_transition_matrix_is_explicit(self) -> None:
        self.assertEqual(
            self.matrix["prerelease_transitions"],
            [
                {
                    "from": "1.0.0-alpha.1",
                    "to": "1.0.0-alpha.2",
                    "channel": "alpha",
                    "must_be_declared": True,
                },
                {
                    "from": "1.0.0-alpha.2",
                    "to": "1.0.0-alpha.3",
                    "channel": "alpha",
                    "must_be_declared": True,
                },
                {
                    "from": "1.0.0-alpha.3",
                    "to": "1.0.0-alpha.5",
                    "channel": "alpha",
                    "must_be_declared": True,
                },
                {
                    "from": "1.0.0-alpha.4",
                    "to": "1.0.0-alpha.5",
                    "channel": "alpha",
                    "must_be_declared": True,
                },
                {
                    "from": "1.0.0-alpha.5",
                    "to": "1.0.0-rc.1",
                    "channel": "rc",
                    "must_be_declared": True,
                },
                {
                    "from": "1.0.0-rc.1",
                    "to": "1.0.0",
                    "channel": "stable",
                    "must_be_declared": True,
                },
            ],
        )
        for case_id in ("alpha-to-alpha", "alpha-to-rc", "rc-to-stable"):
            self.assertEqual(self.cases[case_id]["expected"], "supported-when-declared")

    def test_semantic_completion_scope_is_frozen(self) -> None:
        self.assertEqual(
            set(self.matrix["semantic_completion_scope"]),
            {
                "roles",
                "workflows",
                "shared instructions",
                "knowledge",
                "registries",
                "index.md",
                "log.md",
                "metadata",
                "links",
                "filenames",
                "directory layout",
            },
        )
        self.assertEqual(
            self.cases["semantic-completion-inconsistent-files"]["expected"],
            "refuse-completion",
        )

    def test_host_claim_scope_is_frozen(self) -> None:
        claims = self.matrix["host_claims"]
        self.assertEqual(claims["maintained"], ["OpenCode"])
        self.assertTrue(claims["host_neutral_discovery"])
        self.assertFalse(claims["unsupported_named_hosts_claimed"])
        self.assertEqual(claims["host_entrypoints"], "project-owned")

    def test_trust_modes_are_frozen(self) -> None:
        self.assertEqual(set(self.matrix["trust_modes"]), {"convenience", "verified"})
        self.assertIn("attestation", self.matrix["trust_modes"]["verified"])
        self.assertEqual(
            self.cases["verified-bootstrap-attestation-failure"]["expected"],
            "error",
        )


if __name__ == "__main__":
    unittest.main()
