from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "conformance.py"
SPEC = importlib.util.spec_from_file_location("ava_conformance", MODULE_PATH)
assert SPEC and SPEC.loader
CONFORMANCE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CONFORMANCE
SPEC.loader.exec_module(CONFORMANCE)


class ConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, path: str, content: str = "") -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        return target

    def public_doc(self, title: str, *, extra: str = "") -> str:
        return (
            "---\n"
            "type: Test Document\n"
            f"title: {title}\n"
            f"{extra}"
            "generated:\n"
            "  by: agent:test\n"
            "  at: 2026-08-03T00:00:00+00:00\n"
            "---\n\n"
            f"# {title}\n"
        )

    def create_repository(self) -> None:
        for path in CONFORMANCE.REPOSITORY_REQUIRED:
            if path.endswith(".json"):
                self.write(path, "{}\n")
            elif path.endswith(".py"):
                self.write(path, "# placeholder\n")
            elif path.endswith(".sh"):
                self.write(path, "#!/bin/sh\n")
            elif path.endswith("index.md"):
                self.write(path, f"# {Path(path).stem}\n")
            else:
                self.write(path, self.public_doc(Path(path).stem))

        role_root = "templates/base/roles/test-role"
        self.write(
            f"{role_root}/index.md",
            "# Test role\n\n"
            "- [Role](role.md)\n"
            "- [Instructions](instructions.md)\n"
            "- [Capabilities](capabilities.md)\n"
            "- [Constraints](constraints.md)\n",
        )
        for name in ("role.md", "instructions.md", "capabilities.md", "constraints.md"):
            self.write(f"{role_root}/{name}", self.public_doc(name))
        self.write(
            "templates/base/roles/index.md",
            "# Roles\n\n### [Test Role](test-role/)\n",
        )

        workflow = self.public_doc(
            "Test workflow",
            extra="primary_role: ./.ava/base/roles/test-role/role.md\n",
        )
        self.write("templates/base/workflows/test.md", workflow)
        self.write("templates/base/workflows/index.md", "# Workflows\n\n- [Test](test.md)\n")

        self.write("templates/base/shared/instructions/index.md", "# Instructions\n")
        self.write("templates/base/shared/index.md", "# Shared\n\n- [Instructions](instructions/)\n")
        self.write("templates/base/index.md", "# Base\n")
        self.write("templates/project-scaffolds/index.md", "# Project\n")

    def create_installed(self, *, semantic_status: str = "complete", journal_status: str = "idle") -> None:
        self.write("AGENTS.md", "# Router\n")
        self.write(".ava/base/index.md", "# Base\n")
        router_sha = hashlib.sha256((self.root / "AGENTS.md").read_bytes()).hexdigest()
        base_sha = hashlib.sha256((self.root / ".ava/base/index.md").read_bytes()).hexdigest()
        if semantic_status == "complete":
            semantic = {
                "compatible_through": "1.0.0",
                "target_version": None,
                "status": "complete",
                "unresolved_decisions": [],
            }
        else:
            semantic = {
                "compatible_through": "0.9.0",
                "target_version": "1.0.0",
                "status": semantic_status,
                "unresolved_decisions": ["choose migration"] if semantic_status == "blocked" else [],
            }
        manifest = {
            "manifest_schema": 1,
            "ava_version": "1.0.0",
            "okf_version": "0.2",
            "installed_at": "2026-08-03T00:00:00Z",
            "release": {
                "tag": "v1.0.0",
                "channel": "stable",
                "source_revision": "0" * 40,
                "release_manifest_sha256": "0" * 64,
            },
            "managed_files": [
                {"path": "/AGENTS.md", "role": "router", "kind": "payload", "sha256": router_sha},
                {"path": "/.ava/base/index.md", "role": "base", "kind": "payload", "sha256": base_sha},
                {"path": "/.ava/state/manifest.json", "role": "state", "kind": "state"},
                {"path": "/.ava/state/upgrade.json", "role": "state", "kind": "state"},
            ],
            "host_integration": None,
            "semantic_compatibility": semantic,
        }
        if journal_status == "idle":
            upgrade = {
                "upgrade_schema": 1,
                "transaction_id": None,
                "status": "idle",
                "stage": "idle",
                "source": None,
                "target": None,
                "path": [],
                "current_edge": None,
                "created_at": None,
                "updated_at": "2026-08-03T00:00:00Z",
                "staging": None,
                "migrations": {"resolved_order": [], "active_id": None, "completed": []},
                "managed_changes": [],
                "project_changes": [],
                "failure": None,
                "allowed_operations": ["normal"],
            }
        else:
            upgrade = {
                "upgrade_schema": 1,
                "transaction_id": "tx",
                "status": "active",
                "stage": "semantic" if semantic_status != "complete" else "preflight",
                "source": {},
                "target": {},
                "path": [{}],
                "current_edge": 0,
                "created_at": "2026-08-03T00:00:00Z",
                "updated_at": "2026-08-03T00:00:00Z",
                "staging": {},
                "migrations": {"resolved_order": [], "active_id": None, "completed": []},
                "managed_changes": [],
                "project_changes": [],
                "failure": None,
                "allowed_operations": ["inspect", "reconcile-semantic"],
            }
        self.write(".ava/state/manifest.json", json.dumps(manifest))
        self.write(".ava/state/upgrade.json", json.dumps(upgrade))

    def create_release(self) -> None:
        payloads = {
            "ava-install.sh": "#!/bin/sh\n",
            "ava-base.tar.gz": "base",
            "ava-guidance.tar.gz": "guidance",
            "ava-migrations.tar.gz": "migrations",
            "ava-release-notes.md": "# Notes\n",
        }
        for name, content in payloads.items():
            self.write(name, content)
        assets = []
        for name in payloads:
            path = self.root / name
            assets.append(
                {
                    "name": name,
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "size": path.stat().st_size,
                }
            )
        assets.extend(({"name": "ava-release.json"}, {"name": "SHA256SUMS"}))
        self.write(
            "ava-release.json",
            json.dumps(
                {
                    "ava_version": "1.0.0",
                    "tag": "v1.0.0",
                    "channel": "stable",
                    "assets": assets,
                }
            ),
        )
        checksum_names = [*payloads, "ava-release.json"]
        checksums = "".join(
            f"{hashlib.sha256((self.root / name).read_bytes()).hexdigest()}  {name}\n"
            for name in checksum_names
        )
        self.write("SHA256SUMS", checksums)

    def rule_ids(self, result: object) -> set[str]:
        return {item.rule_id for item in result.findings}

    def test_finding_schema_is_stable_and_machine_readable(self) -> None:
        finding = CONFORMANCE.Finding(
            "AVA-TEST-RULE",
            "warning",
            "path.md",
            "message",
            fix_available=True,
            decision_required=False,
            category="structural",
            related={"role": "test"},
        )
        self.assertEqual(
            set(finding.to_dict()),
            {"rule_id", "severity", "path", "message", "fix_available", "decision_required", "category", "related"},
        )
        with self.assertRaises(ValueError):
            CONFORMANCE.Finding("AVA-TEST-RULE", "fatal", "path", "message")

    def test_valid_repository_fixture_has_no_blocking_findings(self) -> None:
        self.create_repository()
        result = CONFORMANCE.validate(self.root, "repository")
        errors = [item for item in result.findings if item.severity == "error"]
        self.assertEqual(errors, [])

    def test_repository_reports_required_metadata_links_and_boundaries(self) -> None:
        self.create_repository()
        (self.root / "distribution/paths.md").unlink()
        self.write("templates/base/shared/instructions/bad.md", "# Missing metadata\n[Missing](nope.md)\n")
        self.write("templates/base/roles/test-role/leak.md", self.public_doc("Leak") + "[Internal](../../../internal/todo.md)\n")
        result = CONFORMANCE.validate(self.root, "repository")
        self.assertTrue(
            {"AVA-REPOSITORY-REQUIRED", "AVA-DOC-FRONTMATTER", "AVA-LINK-MISSING", "AVA-INTERNAL-LEAKAGE"}.issubset(self.rule_ids(result))
        )

    def test_repository_reports_role_registry_and_workflow_role_failures(self) -> None:
        self.create_repository()
        (self.root / "templates/base/roles/test-role/constraints.md").unlink()
        self.write("templates/base/roles/index.md", "# Roles\n")
        workflow = self.public_doc("Bad", extra="primary_role: ./.ava/base/roles/missing/role.md\n")
        self.write("templates/base/workflows/test.md", workflow)
        result = CONFORMANCE.validate(self.root, "repository")
        self.assertTrue(
            {"AVA-ROLE-STRUCTURE", "AVA-REGISTRY-MISSING", "AVA-WORKFLOW-ROLE"}.issubset(self.rule_ids(result))
        )

    def test_healthy_install_is_valid_and_allows_normal_routing(self) -> None:
        self.create_installed()
        result = CONFORMANCE.validate(self.root, "installed")
        self.assertTrue(result.valid)
        self.assertTrue(result.normal_routing_permitted)

    def test_managed_checksum_failure_is_blocking(self) -> None:
        self.create_installed()
        self.write("AGENTS.md", "changed\n")
        result = CONFORMANCE.validate(self.root, "installed")
        self.assertIn("AVA-MANAGED-CHECKSUM", self.rule_ids(result))
        self.assertFalse(result.normal_routing_permitted)

    def test_semantic_pending_is_separate_from_deterministic_failure(self) -> None:
        self.create_installed(semantic_status="pending", journal_status="active")
        result = CONFORMANCE.validate(self.root, "installed")
        self.assertIn("AVA-SEMANTIC-INCOMPLETE", self.rule_ids(result))
        self.assertIn("AVA-DETERMINISTIC-INCOMPLETE", self.rule_ids(result))
        self.assertFalse(result.normal_routing_permitted)
        self.assertFalse(any(item.rule_id == "AVA-MANAGED-CHECKSUM" for item in result.findings))

    def test_unexpected_managed_content_is_blocking(self) -> None:
        self.create_installed()
        self.write(".ava/base/unexpected.md", "unexpected\n")
        result = CONFORMANCE.validate(self.root, "installed")
        self.assertIn("AVA-MANAGED-UNEXPECTED", self.rule_ids(result))

    def test_opencode_permissions_are_non_destructive_findings(self) -> None:
        self.create_installed()
        self.write("opencode.json", '{"permission": {}}\n')
        result = CONFORMANCE.validate(self.root, "installed")
        findings = [item for item in result.findings if item.rule_id.startswith("AVA-HOST-OPENCODE")]
        self.assertTrue(findings)
        self.assertTrue(all(item.decision_required for item in findings))
        self.assertTrue(all(not item.fix_available for item in findings))

    def test_release_checksums_and_publication_evidence(self) -> None:
        self.create_release()
        result = CONFORMANCE.validate(self.root, "release")
        self.assertTrue(result.valid)
        self.assertIn("AVA-RELEASE-PUBLICATION-EVIDENCE", self.rule_ids(result))
        qualified = CONFORMANCE.validate(
            self.root,
            "release",
            require_publication_evidence=True,
        )
        self.assertFalse(qualified.valid)
        self.write(
            "publication.json",
            json.dumps(
                {
                    "immutable_releases_enabled": True,
                    "release_immutable": True,
                    "attestation_verified": True,
                }
            ),
        )
        qualified = CONFORMANCE.validate(
            self.root,
            "release",
            require_publication_evidence=True,
        )
        self.assertTrue(qualified.valid)

    def test_repository_reports_duplicate_identifiers_and_orphans(self) -> None:
        self.create_repository()
        self.write(
            "templates/base/shared/instructions/one.md",
            self.public_doc("One", extra="id: duplicate\n"),
        )
        self.write(
            "templates/base/shared/instructions/two.md",
            self.public_doc("Two", extra="id: duplicate\n"),
        )
        result = CONFORMANCE.validate(self.root, "repository")
        self.assertIn("AVA-ID-DUPLICATE", self.rule_ids(result))
        self.assertIn("AVA-INDEX-ORPHAN", self.rule_ids(result))

    def test_repository_reports_deprecated_references(self) -> None:
        self.create_repository()
        self.write("templates/host-bootstraps/legacy.md", "legacy\n")
        self.write(
            "templates/base/shared/instructions/legacy.md",
            self.public_doc("Legacy") + "templates/release-guidance.md\n",
        )
        result = CONFORMANCE.validate(self.root, "repository")
        self.assertIn("AVA-BOUNDARY-OBSOLETE", self.rule_ids(result))
        self.assertIn("AVA-DEPRECATED-REFERENCE", self.rule_ids(result))

    def test_managed_missing_file_is_blocking(self) -> None:
        self.create_installed()
        (self.root / ".ava/base/index.md").unlink()
        result = CONFORMANCE.validate(self.root, "installed")
        self.assertIn("AVA-MANAGED-MISSING", self.rule_ids(result))
        self.assertFalse(result.normal_routing_permitted)

    def test_missing_or_malformed_state_is_blocking(self) -> None:
        self.create_installed()
        (self.root / ".ava/state/manifest.json").write_text("not json")
        result = CONFORMANCE.validate(self.root, "installed")
        self.assertIn("AVA-MANIFEST-READ", self.rule_ids(result))
        self.assertFalse(result.normal_routing_permitted)

        self.create_installed()
        (self.root / ".ava/state/upgrade.json").write_text("not json")
        result = CONFORMANCE.validate(self.root, "installed")
        self.assertIn("AVA-UPGRADE-READ", self.rule_ids(result))
        self.assertFalse(result.normal_routing_permitted)

    def test_semantic_state_variants_remain_blocking(self) -> None:
        for status in ("partial", "blocked"):
            with self.subTest(status=status):
                self.create_installed(semantic_status=status, journal_status="active")
                result = CONFORMANCE.validate(self.root, "installed")
                self.assertIn("AVA-SEMANTIC-INCOMPLETE", self.rule_ids(result))
                self.assertFalse(result.normal_routing_permitted)

    def test_release_manifest_asset_metadata_is_verified(self) -> None:
        self.create_release()
        manifest_path = self.root / "ava-release.json"
        manifest = json.loads(manifest_path.read_text())
        next(item for item in manifest["assets"] if item["name"] == "ava-base.tar.gz")["size"] += 1
        manifest_path.write_text(json.dumps(manifest))
        checksums = (self.root / "SHA256SUMS").read_text().splitlines()
        checksums = [
            f"{hashlib.sha256(manifest_path.read_bytes()).hexdigest()}  ava-release.json"
            if line.endswith("  ava-release.json")
            else line
            for line in checksums
        ]
        (self.root / "SHA256SUMS").write_text("\n".join(checksums) + "\n")
        result = CONFORMANCE.validate(self.root, "release")
        self.assertIn("AVA-RELEASE-ASSET-METADATA", self.rule_ids(result))

    def test_publication_evidence_failures_are_blocking(self) -> None:
        self.create_release()
        self.write(
            "publication.json",
            json.dumps(
                {
                    "immutable_releases_enabled": False,
                    "release_immutable": False,
                    "attestation_verified": False,
                }
            ),
        )
        result = CONFORMANCE.validate(
            self.root,
            "release",
            require_publication_evidence=True,
        )
        self.assertIn("AVA-RELEASE-IMMUTABILITY", self.rule_ids(result))
        self.assertFalse(result.valid)

    def test_release_checksum_mismatch_is_blocking(self) -> None:
        self.create_release()
        self.write("ava-base.tar.gz", "corrupt")
        result = CONFORMANCE.validate(self.root, "release")
        self.assertIn("AVA-RELEASE-CHECKSUM", self.rule_ids(result))


if __name__ == "__main__":
    unittest.main()
