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
INSTRUCTION_RESOLUTION = (
    SOURCE_ROOT / "templates/base/shared/instructions/instruction-resolution.md"
)
WORKFLOW_ROUTING = SOURCE_ROOT / "templates/base/shared/instructions/workflow-routing.md"
ROLE_INDEX = SOURCE_ROOT / "templates/base/roles/index.md"
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/root-routing.json"


def router_contract_errors(text: str) -> list[str]:
    required = (
        "Every user request must enter this router before any substantive answer, refusal, task execution, or project action.",
        "Every request must perform the managed-state gate before any other substantive handling:",
        "classify the turn before deciding whether fresh workflow or role resolution is required.",
        "### Roleless conversational follow-up",
        "A roleless turn ends active-role continuity.",
        "### Same-role continuation",
        "Active role remains: <role title>",
        "do not repeat workflow or role registry traversal and do not reload unchanged required reading.",
        "### Fresh routing",
        "the request introduces a new task or objective",
        "a prior roleless turn ended active-role continuity and scoped work is now requested",
        "An explicit workflow invocation always uses fresh routing.",
        "A turn may have zero or one active role.",
        "Do not substitute a generic host-persona answer, refusal, or scope disclaimer.",
    )
    errors = [
        f"missing required router invariant: {item}"
        for item in required
        if item not in text
    ]

    forbidden = (
        "When the pre-routing check permits normal operation, continue routing before any substantive handling:",
        "Exactly one role may be active at a time.",
    )
    errors.extend(
        f"legacy unconditional full-routing language remains: {item}"
        for item in forbidden
        if item in text
    )

    ordered = (
        "Every user request must enter this router",
        "## Managed-state gate for every request",
        "Perform its minimal check of `./.ava/state/upgrade.json` and `./.ava/state/manifest.json`.",
        "## Conversation-aware routing",
        "### Roleless conversational follow-up",
        "### Same-role continuation",
        "### Fresh routing",
        "inspect the managed role registry at `./.ava/base/roles/index.md`",
        "Read the selected role's `index.md` and every document it marks as required.",
        "Announce the selected role using `Active role: <role title>`",
        "Only after the preceding routing and required-reading steps",
    )
    positions = [text.find(item) for item in ordered]
    if any(position < 0 for position in positions):
        errors.append("router sequence cannot be established from the required markers")
    elif positions != sorted(positions):
        errors.append("router sequence allows fresh handling before prerequisite routing")

    return errors


def shared_contract_errors(
    instruction_resolution: str,
    workflow_routing: str,
    role_index: str,
) -> list[str]:
    required_resolution = (
        "# Per-request state gate and routing decision",
        "Roleless conversational follow-up",
        "Same-role continuation",
        "Fresh routing",
        "A roleless turn clears role continuity.",
        "A new task requires fresh routing even when it is likely to select the same role again.",
        "Ava permits zero or one active role on a turn.",
        "Workflow procedural scope does not continue implicitly",
    )
    errors = [
        f"instruction-resolution contract missing: {item}"
        for item in required_resolution
        if item not in instruction_resolution
    ]

    required_workflow = (
        "An explicit workflow invocation always forces fresh routing.",
        "# Routing precedence and conversational continuity",
        "A roleless conversational follow-up does not traverse workflow registries",
        "A same-role continuation does not traverse workflow registries",
        "# Fresh free-form routing",
        "Workflow procedural scope does not persist implicitly across turns.",
    )
    errors.extend(
        f"workflow-routing contract missing: {item}"
        for item in required_workflow
        if item not in workflow_routing
    )

    required_role_index = (
        "when fresh role routing is required",
        "A valid same-role continuation may retain the already-active role",
        "a roleless conversational follow-up activates no role",
    )
    errors.extend(
        f"role catalog continuity boundary missing: {item}"
        for item in required_role_index
        if item not in role_index
    )
    return errors


class RootRoutingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.router = ROUTER.read_text()
        cls.instruction_resolution = INSTRUCTION_RESOLUTION.read_text()
        cls.workflow_routing = WORKFLOW_ROUTING.read_text()
        cls.role_index = ROLE_INDEX.read_text()
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}

    def create_installed_project(self, root: Path, router: str) -> None:
        (root / ".ava/base").mkdir(parents=True)
        (root / ".ava/state").mkdir(parents=True)
        (root / "AGENTS.md").write_text(router)
        (root / ".ava/base/index.md").write_text(
            "---\nokf_version: \"0.2\"\n---\n\n# Base\n"
        )
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
                    "sha256": hashlib.sha256(
                        (root / ".ava/base/index.md").read_bytes()
                    ).hexdigest(),
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

    def test_fixture_covers_continuity_and_no_bypass_cases(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 2)
        self.assertEqual(
            set(self.cases),
            {
                "apparently-out-of-domain-warranty",
                "roleless-clarification",
                "same-role-continuation",
                "role-transition",
                "scoped-work-after-roleless",
                "no-clear-role-match",
            },
        )

        for case in self.cases.values():
            with self.subTest(case=case["id"]):
                self.assertEqual(case["managed_state"], "normal")
                self.assertIn("managed-state-gate", case["required_before_handling"])
                self.assertIn(
                    "conversation-routing-classification",
                    case["required_before_handling"],
                )

        warranty = self.cases["apparently-out-of-domain-warranty"]
        self.assertEqual(warranty["routing_mode"], "fresh-routing")
        self.assertEqual(warranty["request"], "Has my warranty run out on my glasses?")
        self.assertIn(
            "managed-and-project-role-registry-evaluation",
            warranty["required_before_handling"],
        )
        self.assertIn("role-announcement", warranty["required_before_handling"])
        self.assertIn(
            "generic coding-assistant scope refusal",
            warranty["forbidden_before_routing"],
        )

        roleless = self.cases["roleless-clarification"]
        self.assertEqual(roleless["routing_mode"], "roleless-followup")
        self.assertIsNone(roleless["active_role_after_turn"])
        self.assertNotIn(
            "managed-and-project-role-registry-evaluation",
            roleless["required_before_handling"],
        )
        self.assertIn("project-mutation", roleless["forbidden_before_routing"])

        same_role = self.cases["same-role-continuation"]
        self.assertEqual(same_role["routing_mode"], "same-role-continuation")
        self.assertEqual(same_role["active_role_after_turn"], "Project Steward")
        self.assertIn(
            "role-continuation-announcement",
            same_role["required_before_handling"],
        )
        self.assertIn(
            "role-required-reading-reload",
            same_role["forbidden_before_routing"],
        )

        transition = self.cases["role-transition"]
        self.assertEqual(transition["routing_mode"], "fresh-routing")
        self.assertEqual(transition["acceptable_outcomes"], ["Change Reviewer"])

        after_roleless = self.cases["scoped-work-after-roleless"]
        self.assertEqual(after_roleless["routing_mode"], "fresh-routing")
        self.assertIn(
            "reuse role from before roleless turn",
            after_roleless["forbidden_before_routing"],
        )

        unresolved = self.cases["no-clear-role-match"]
        self.assertEqual(unresolved["acceptable_outcomes"], ["explicit-routing-clarification"])
        self.assertIn("invented role authority", unresolved["forbidden_before_routing"])

    def test_source_router_is_state_gated_and_conversation_aware(self) -> None:
        self.assertEqual(router_contract_errors(self.router), [])
        self.assertEqual(
            shared_contract_errors(
                self.instruction_resolution,
                self.workflow_routing,
                self.role_index,
            ),
            [],
        )

    def test_legacy_unconditional_full_routing_is_rejected(self) -> None:
        legacy = self.router.replace(
            "## Conversation-aware routing",
            "When the pre-routing check permits normal operation, continue routing before any substantive handling:",
        )
        errors = router_contract_errors(legacy)
        self.assertTrue(
            any("legacy unconditional full-routing language remains" in error for error in errors)
        )

    def test_assembled_installed_router_and_opencode_model_preserve_the_gate(self) -> None:
        payload = next(
            item for item in read_payloads(SOURCE_ROOT) if item.destination == "/AGENTS.md"
        )
        installed_router = payload.data.decode("utf-8")
        self.assertEqual(installed_router, self.router)
        self.assertEqual(router_contract_errors(installed_router), [])

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.create_installed_project(root, installed_router)
            result = validate(root, "installed")

        self.assertTrue(result.valid)
        self.assertTrue(result.normal_routing_permitted)
        self.assertFalse(
            any(item.rule_id.startswith("AVA-HOST-OPENCODE") for item in result.findings)
        )


if __name__ == "__main__":
    unittest.main()
