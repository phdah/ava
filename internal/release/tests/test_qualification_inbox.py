from __future__ import annotations

import hashlib
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_inbox


class QualificationInboxTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.project = Path(self.temp.name) / "project"
        (self.project / "inbox/processed").mkdir(parents=True)
        (self.project / "knowledge").mkdir()

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def source(self, name: str = "source.md") -> tuple[Path, list[dict[str, str]]]:
        path = self.project / "inbox/processed" / name
        path.write_text("# Source\n\nA durable fact.\n", encoding="utf-8")
        return path, [{"path": f"inbox/{name}", "sha256": self.digest(path)}]

    def destination(self, source_name: str = "source.md", *, definition: str | None = None) -> Path:
        path = self.project / "knowledge/topic.md"
        definition = definition or f"[Source](../inbox/processed/{source_name}), \"Fact\"."
        path.write_text(
            "---\n"
            "type: Knowledge\n"
            "sources:\n"
            "  - id: source-fact\n"
            f"    resource: ./inbox/processed/{source_name}\n"
            "    title: Source\n"
            "---\n\n"
            "# Topic\n\n"
            "A durable fact.[^source-fact]\n\n"
            f"[^source-fact]: {definition}\n",
            encoding="utf-8",
        )
        return path

    def test_accepts_project_root_metadata_and_document_relative_footnote(self) -> None:
        _, selected = self.source()
        self.destination()
        qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_processed_source_without_trusted_metadata_reference(self) -> None:
        _, selected = self.source()
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "not referenced by trusted sources metadata",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_used_marker_without_definition(self) -> None:
        _, selected = self.source()
        destination = self.destination()
        destination.write_text(
            destination.read_text(encoding="utf-8").replace(
                '\n[^source-fact]: [Source](../inbox/processed/source.md), "Fact".\n',
                "\n",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "requires exactly one definition",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_footnote_link_that_disagrees_with_metadata(self) -> None:
        _, selected = self.source()
        other = self.project / "inbox/processed/other.md"
        other.write_text("other\n", encoding="utf-8")
        self.destination(definition='[Other](../inbox/processed/other.md), "Fact".')
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "does not resolve to the same source as metadata",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_selected_source_not_preserved_exactly_once(self) -> None:
        source, selected = self.source()
        self.destination()
        duplicate = self.project / "inbox/processed/duplicate.md"
        duplicate.write_bytes(source.read_bytes())
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "preserved exactly once",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)


if __name__ == "__main__":
    unittest.main()
