from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from internal.release.assemble import read_payloads
from internal.release.conformance import validate

SOURCE_ROOT = Path(__file__).resolve().parents[3]
ROUTER = SOURCE_ROOT / "templates/base/AGENTS.md"
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/root-routing.json"


def router_contract_errors(text: str) -> list[str]:
    required = (
        "Every user request must enter this router before any substantive answer, refusal, task execution, or project action.",
        "Apparent simplicity, apparent subject matter, or the host agent's generic persona does not create an exception.",
        "Before role activation, reads and checks are permitted only when required to complete this routing procedure.",
        "For every user request, before any other handling:",
        "When the pre-routing check permits normal operation, continue routing before any substantive handling:",
        "Only after the preceding routing and required-reading steps may the active role provide a substantive answer, refusal, task execution, or project action.",
        "This routing clarification is the only response permitted before role activation during normal operation.",
        "Do not substitute a generic host-persona answer, refusal, or scope disclaimer.",
    )
    errors = [f"missing required router invariant: {item}" for item in required if item not in text]

    forbidden = (
        "Before reading any project-owned registry or performing ordinary routing:",
    )
    errors.extend(f"legacy conditional router language remains: {item}" for item in forbidden if item in text)

    ordered = (
        "Every user request must enter this router",
        "For every user request, before any other handling:",
        "Perform its minimal check of `./.ava/state/upgrade.json` and `./.ava/state/manifest.json`.",
        "When the pre-routing check permits normal operation, continue routing before any substantive handling:",
        "inspect the managed role registry at `./.ava/base/roles/index.md`",
        "Read the selected role's `index.md` and every document it marks as required.",
        "Announce the selected role using `Active role: <role title>`",
        "Only after the preceding routing and required-reading steps",
    )
    positions = [text.find(item) for item in ordered]
    if any(position < 0 for position in positions):
        errors.append("router sequence cannot be established from the required markers")
    elif positions != sorted(positions):
        errors.append("router sequence allows handling or announcement before prerequisite routing")

    return errors


class RootRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.router = ROUTER.read_text()
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}

    def create_installed_project(self, root: Path, router: str) -> None:
        (root / ".ava/base").mkdir(parents=True)
        (root / ".ava/state").mkdir(parents=True)
        (root / "AGENTS.md").write_text(router)
        (root / ".ava/base/index.md").write_text("---\nokf_version: \"0.2\"\n---\n\n# Base\n")
        (root / "opencode.json").write_text(
            json.dumps(
                {
                    "$schema": "https://opencode.ai/config.json",
                    "permission": {
                        "read": {".ava/**": "allow"},
                        "edit": {".ava/**": "ask"},
                    },
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

        manifest = {
            "manifest_schema": 1,
            "ava_version": "1.0.0",
            "okf_version": "0.2",
            "installed_at": "2026-08-08T16:00:00Z",
            "release": {
                "tag": "v1.0.0",
                "channel": "stable",
                "source_revision": "0" * 40,
                "release_manifest_sha256": "0" * 64,
            },
            "managed_files": [
                {
                    "path": "/AGENTS.md",
                    "role": "router",
                    "kind": "payload",
                    "sha256": hashlib.sha256((root / "AGENTS.md").read_bytes()).hexdigest(),
                },
                {
                    "path": "/.ava/base/index.md",
                    "role": "base",
                    "kind": "payload",
                    "sha256": hashlib.sha256((root / ".ava/base/index.md").read_bytes()).hexdigest(),
                },
                {"path": "/.ava/state/manifest.json", "role": "state", "kind": "state"},
                {"path": "/.ava/state/upgrade.json", "role": "state", "kind": "state"},
            ],
            "host_integration": None,
            "semantic_compatibility": {
                "compatible_through": "1.0.0",
                "target_version": None,
                "status": "complete",
                "unresolved_decisions": [],
            },
        }
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
            "updated_at": "2026-08-08T16:00:00Z",
            "staging": None,
            "migrations": {"resolved_order": [], "active_id": None, "completed": []},
            "managed_changes": [],
            "project_changes": [],
            "failure": None,
            "allowed_operations": ["normal"],
        }
        (root / ".ava/state/manifest.json").write_text(json.dumps(manifest))
        (root / ".ava/state/upgrade.json").write_text(json.dumps(upgrade))

    def test_fixture_covers_warranty_and_unresolved_routing_failures(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 1)
        self.assertEqual(
            set(self.cases),
            {"apparently-out-of-domain-warranty", "no-clear-role-match"},
        )
        warranty = self.cases["apparently-out-of-domain-warranty"]
        self.assertEqual(warranty["request"], "Has my warranty run out on my glasses?")
        self.assertIn("managed-state-gate", warranty["required_before_handling"])
        self.assertIn("managed-and-project-role-registry-evaluation", warranty["required_before_handling"])
        self.assertIn("role-announcement", warranty["required_before_handling"])
        self.assertIn("generic coding-assistant scope refusal", warranty["forbidden_before_routing"])

        unresolved = self.cases["no-clear-role-match"]
        self.assertEqual(unresolved["acceptable_outcomes"], ["explicit-routing-clarification"])
        self.assertIn("invented role authority", unresolved["forbidden_before_routing"])

    def test_source_router_is_unconditional_and_ordered(self) -> None:
        self.assertEqual(router_contract_errors(self.router), [])

    def test_legacy_conditional_router_is_rejected(self) -> None:
        legacy = self.router.replace(
            "For every user request, before any other handling:",
            "Before reading any project-owned registry or performing ordinary routing:",
        )
        errors = router_contract_errors(legacy)
        self.assertTrue(any("missing required router invariant" in error for error in errors))
        self.assertTrue(any("legacy conditional router language remains" in error for error in errors))

    def test_assembled_installed_router_and_opencode_model_preserve_the_gate(self) -> None:
        payload = next(item for item in read_payloads(SOURCE_ROOT) if item.destination == "/AGENTS.md")
        installed_router = payload.data.decode("utf-8")
        self.assertEqual(installed_router, self.router)
        self.assertEqual(router_contract_errors(installed_router), [])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_installed_project(root, installed_router)
            result = validate(root, "installed")

        self.assertTrue(result.valid)
        self.assertTrue(result.normal_routing_permitted)
        self.assertFalse(any(item.rule_id.startswith("AVA-HOST-OPENCODE") for item in result.findings))


if __name__ == "__main__":
    unittest.main()
