from __future__ import annotations

import json
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE = SOURCE_ROOT / "internal/release/fixtures/inbox-ingestion-fidelity.json"
FIDELITY = SOURCE_ROOT / "templates/base/shared/instructions/inbox-ingestion-fidelity.md"
DOCUMENT_METADATA = SOURCE_ROOT / "templates/base/shared/instructions/document-metadata.md"
KNOWLEDGE_ORGANIZATION = SOURCE_ROOT / "templates/base/shared/instructions/knowledge-organization.md"
INBOX_INDEX = SOURCE_ROOT / "templates/base/roles/inbox-ingester/index.md"
INBOX_INSTRUCTIONS = SOURCE_ROOT / "templates/base/roles/inbox-ingester/instructions.md"
REVIEWER_INDEX = SOURCE_ROOT / "templates/base/roles/change-reviewer/index.md"
WORKFLOW = SOURCE_ROOT / "templates/base/workflows/ingest-inbox.md"


class InboxIngestionFidelityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fixture = json.loads(FIXTURE.read_text())
        cls.cases = {case["id"]: case for case in cls.fixture["cases"]}
        cls.fidelity = FIDELITY.read_text()
        cls.document_metadata = DOCUMENT_METADATA.read_text()
        cls.knowledge_organization = KNOWLEDGE_ORGANIZATION.read_text()
        cls.inbox_index = INBOX_INDEX.read_text()
        cls.inbox_instructions = INBOX_INSTRUCTIONS.read_text()
        cls.reviewer_index = REVIEWER_INDEX.read_text()
        cls.workflow = WORKFLOW.read_text()

    def test_fixture_covers_required_failure_modes(self) -> None:
        self.assertEqual(self.fixture["schema_version"], 1)
        self.assertFalse(self.fixture["deterministic_validation_proves_semantic_fidelity"])
        self.assertEqual(
            set(self.cases),
            {
                "long-multi-topic-source-requires-complete-inventory",
                "uncertain-causal-language-remains-uncertain",
                "claims-from-different-sources-keep-distinct-attribution",
                "delegated-batch-requires-coordinator-reconciliation",
                "unresolved-footnote-marker-blocks-completion",
                "incorrect-source-attribution-blocks-completion",
                "frontmatter-only-source-remains-unchanged",
                "completion-counts-use-final-inventories",
            },
        )
        for case in self.cases.values():
            self.assertTrue(case["expected_action"], case["id"])
            self.assertTrue(case["review_checks"], case["id"])
            if "source" in case or "sources" in case:
                self.assertIn("source_may_move", case, case["id"])

    def test_inbox_role_requires_fidelity_contract(self) -> None:
        self.assertIn(
            "[Inbox ingestion fidelity](../../shared/instructions/inbox-ingestion-fidelity.md)",
            self.inbox_index,
        )
        self.assertIn("Substantive-section inventory", self.inbox_index)
        self.assertIn("final-state reconciliation", self.inbox_index)

    def test_contract_requires_complete_section_dispositions(self) -> None:
        self.assertIn("# Substantive section inventory", self.fidelity)
        self.assertIn("There is no implicit ignored state", self.fidelity)
        self.assertIn("`mapped`", self.fidelity)
        self.assertIn("`non-durable`", self.fidelity)
        self.assertIn("`pending`", self.fidelity)
        self.assertIn("zero substantive sections", self.fidelity)
        self.assertIn("remains unchanged and pending", self.fidelity)

    def test_contract_preserves_uncertainty_and_attribution(self) -> None:
        self.assertIn("# Epistemic and attribution fidelity", self.fidelity)
        self.assertIn(
            "plausible, unconfirmed contributor` must not become `reduced worker capacity caused",
            self.fidelity,
        )
        self.assertIn("who made, observed, proposed, approved, rejected, or questioned", self.fidelity)
        self.assertIn("source content, trusted project knowledge, and a user-approved decision", self.fidelity)

    def test_contract_defines_grouped_renderable_claim_provenance(self) -> None:
        self.assertIn("# Renderable claim provenance", self.fidelity)
        self.assertIn("id: incident-2026-06-10", self.fidelity)
        self.assertIn("id: remediation-2026-06-11", self.fidelity)
        self.assertIn("[^1]", self.fidelity)
        self.assertIn(
            "[^1]: Sources: `source:incident-2026-06-10` - \"Incident review\"; `source:remediation-2026-06-11` - \"Remediation\".",
            self.fidelity,
        )
        self.assertIn("one claim uses one grouped marker", self.fidelity)
        self.assertIn("`source:<sources[].id>`", self.fidelity)
        self.assertIn("must not repeat source `resource` paths or source `title` text", self.fidelity)
        self.assertNotIn("footnote label must exactly equal one `sources[].id`", self.fidelity)
        self.assertIn("actual source passages must support the attributed claim", self.fidelity)
        self.assertIn("source-specific claims", self.fidelity)
        self.assertIn("differ in author, date, chronology, certainty, status", self.fidelity)
        self.assertIn("A bare marker", self.fidelity)

        case = self.cases["claims-from-different-sources-keep-distinct-attribution"]
        self.assertEqual(case["grouped_marker"], "[^1]")
        self.assertEqual(len(case["supporting_sources"]), 2)
        self.assertEqual(
            case["expected_definition_source_refs"],
            ["source:incident-2026-06-10", "source:remediation-2026-06-11"],
        )
        self.assertEqual(case["expected_action"], "use-one-grouped-renderable-footnote")

    def test_grouped_provenance_guidance_is_consistent(self) -> None:
        for document in (
            self.document_metadata,
            self.knowledge_organization,
            self.inbox_instructions,
            self.workflow,
        ):
            with self.subTest(document=document[:80]):
                self.assertIn("sources[].id", document)
                self.assertIn("resource", document)
                self.assertIn("title", document)
        self.assertIn("one numbered Markdown footnote marker", self.document_metadata)
        self.assertIn("one numbered grouped Markdown footnote per claim", self.knowledge_organization)
        self.assertIn("one numbered grouped Markdown footnote per claim", self.inbox_instructions)
        self.assertIn("one renderable grouped Markdown footnote per claim", self.workflow)

    def test_delegated_batches_require_one_coordinator_ledger(self) -> None:
        case = self.cases["delegated-batch-requires-coordinator-reconciliation"]
        self.assertFalse(case["source_may_move"])
        self.assertEqual(len(case["sources"]), 4)
        self.assertEqual(
            set(case["child_assignments"]["child-a"]) & set(case["child_assignments"]["child-b"]),
            set(),
        )
        self.assertIn("# Delegated and large-batch ingestion", self.fidelity)
        self.assertIn("owns one complete selected-source ledger", self.fidelity)
        self.assertIn("explicit, disjoint source subset", self.fidelity)
        self.assertIn("Child-session success is provisional batch evidence", self.fidelity)
        self.assertIn("reconcile every originally selected source exactly once", self.workflow)
        self.assertIn("Missing or overlapping child evidence prevents a complete batch result", self.workflow)

    def test_workflow_requires_inventory_and_final_reconciliation(self) -> None:
        self.assertIn("inventory every substantive section", self.workflow)
        self.assertIn("preserving uncertainty, causality, attribution", self.workflow)
        self.assertIn("one renderable grouped Markdown footnote per claim", self.workflow)
        self.assertIn("read-only final-state reconciliation", self.workflow)
        self.assertIn("reconciled final pending, processed, destination, and index inventories", self.workflow)

    def test_reviewer_loads_semantic_fidelity_contract(self) -> None:
        self.assertIn(
            "[Inbox ingestion fidelity](../../shared/instructions/inbox-ingestion-fidelity.md)",
            self.reviewer_index,
        )
        self.assertIn("processed-source completion", self.reviewer_index)
        self.assertIn("# Independent semantic review", self.fidelity)
        self.assertIn("every selected source", self.fidelity)
        self.assertIn("delegated or parallel work still provides complete per-source evidence", self.fidelity)
        self.assertIn("deterministic validation is reported separately", self.fidelity)
        self.assertIn(
            "must not claim that machine-readable fixtures or link validation prove meaning preservation",
            self.fidelity,
        )

    def test_final_counts_exclude_reserved_entries(self) -> None:
        case = self.cases["completion-counts-use-final-inventories"]
        self.assertEqual(case["expected_selected_source_count"], 3)
        self.assertEqual(case["expected_final_pending_direct_children"], 1)
        self.assertIn("inbox/index.md", case["review_checks"][0])
        self.assertIn("inbox/processed/", case["review_checks"][0])
        self.assertIn("Pending direct-child counts exclude", self.fidelity)
        self.assertIn("Compute the completion report from the final filesystem state", self.fidelity)

    def test_semantic_failures_block_source_movement(self) -> None:
        for case_id in (
            "long-multi-topic-source-requires-complete-inventory",
            "delegated-batch-requires-coordinator-reconciliation",
            "unresolved-footnote-marker-blocks-completion",
            "incorrect-source-attribution-blocks-completion",
            "frontmatter-only-source-remains-unchanged",
        ):
            with self.subTest(case_id=case_id):
                self.assertFalse(self.cases[case_id]["source_may_move"])


if __name__ == "__main__":
    unittest.main()
