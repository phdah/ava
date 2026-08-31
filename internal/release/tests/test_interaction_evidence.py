from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from internal.release.interaction_evidence import validate_interaction_evidence


class InteractionEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.processed = self.root / "inbox/processed"
        self.processed.mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write(self, path: str, content: str) -> Path:
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        return target

    def record(self, interaction_id: str, *, target: str = "./knowledge/project.md", extra: str = "", directory: str = "inbox/processed") -> Path:
        evidence_path = f"./{directory}/interaction-{interaction_id}.md"
        self.write(
            target.removeprefix("./"),
            "---\ntype: Project\nsources:\n"
            f"  - id: interaction-{interaction_id}\n"
            f"    resource: {evidence_path}\n"
            "---\n\n# Project\n",
        )
        return self.write(
            f"{directory}/interaction-{interaction_id}.md",
            "---\n"
            "type: Interaction Evidence\n"
            "title: User decision\n"
            "generated:\n"
            "  by: agent:project-steward\n"
            "  at: 2026-08-31T08:19:00+02:00\n"
            f"interaction_id: {interaction_id}\n"
            "evidence_kind: authorization\n"
            "supplier:\n"
            "  kind: human\n"
            "  identity: unverified\n"
            f"targets:\n  - {target}\n"
            "supersedes: []\n"
            "redactions: []\n"
            f"{extra}"
            "---\n\n"
            "# Statement\n\n"
            "> Implement the approved change.\n\n"
            "# Context\n\n"
            "Approval for the linked semantic mutation.\n",
        )

    def rule_ids(self) -> set[str]:
        findings = []
        validate_interaction_evidence(self.root, findings)
        return {finding.rule_id for finding in findings}

    def test_valid_processed_interaction_evidence(self) -> None:
        self.record("7f3c1c2a4b5d6e7f")
        self.assertEqual(self.rule_ids(), set())

    def test_interaction_specific_subdirectory_is_rejected(self) -> None:
        self.record("8f3c1c2a4b5d6e7f", directory="inbox/processed/interactions")
        self.assertIn("AVA-INTERACTION-PATH", self.rule_ids())

    def test_missing_target_and_reverse_reference_are_reported(self) -> None:
        path = self.record("9f3c1c2a4b5d6e7f")
        (self.root / "knowledge/project.md").unlink()
        self.assertIn("AVA-INTERACTION-TARGET", self.rule_ids())

        self.write("knowledge/project.md", "---\ntype: Project\n---\n\n# Project\n")
        self.assertIn("AVA-INTERACTION-REVERSE-REF", self.rule_ids())
        self.assertTrue(path.is_file())

    def test_duplicate_id_and_bad_supersession_are_reported(self) -> None:
        interaction_id = "af3c1c2a4b5d6e7f"
        self.record(interaction_id)
        nested = self.root / f"inbox/processed/nested/interaction-{interaction_id}.md"
        nested.parent.mkdir(parents=True)
        nested.write_text((self.processed / f"interaction-{interaction_id}.md").read_text(), encoding="utf-8")
        ids = self.rule_ids()
        self.assertIn("AVA-INTERACTION-DUPLICATE-ID", ids)
        self.assertIn("AVA-INTERACTION-PATH", ids)

        second = "bf3c1c2a4b5d6e7f"
        self.record(second)
        evidence = self.processed / f"interaction-{second}.md"
        evidence.write_text(evidence.read_text().replace("supersedes: []", "supersedes:\n  - ./inbox/processed/interaction-missing00000000.md"), encoding="utf-8")
        self.assertIn("AVA-INTERACTION-SUPERSEDES", self.rule_ids())

    def test_supplier_and_statement_shape_are_validated(self) -> None:
        interaction_id = "cf3c1c2a4b5d6e7f"
        path = self.record(interaction_id)
        text = path.read_text(encoding="utf-8")
        text = text.replace("identity: unverified", "identity: verified")
        text = text.replace("> Implement the approved change.", "Implement the approved change.")
        path.write_text(text, encoding="utf-8")
        ids = self.rule_ids()
        self.assertIn("AVA-INTERACTION-SUPPLIER", ids)
        self.assertIn("AVA-INTERACTION-STATEMENT", ids)


if __name__ == "__main__":
    unittest.main()
