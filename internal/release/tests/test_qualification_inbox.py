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

    def source(
        self,
        name: str = "source.md",
        *,
        body: str | None = None,
    ) -> tuple[Path, list[dict[str, str]]]:
        path = self.project / "inbox/processed" / name
        path.write_text(
            body or f"# Source {name}\n\nA durable fact from {name}.\n",
            encoding="utf-8",
        )
        return path, [{"path": f"inbox/{name}", "sha256": self.digest(path)}]

    def destination(
        self,
        *,
        source_rows: list[tuple[str, str]] | None = None,
        marker: str = "1",
        definition: str | None = None,
    ) -> Path:
        path = self.project / "knowledge/topic.md"
        source_rows = source_rows or [("source-fact", "source.md")]
        metadata = "".join(
            f"  - id: {source_id}\n"
            f"    resource: ./inbox/processed/{source_name}\n"
            f"    title: Source {source_name}\n"
            for source_id, source_name in source_rows
        )
        definition = definition or 'Sources: `source:source-fact` - "Fact".'
        path.write_text(
            "---\n"
            "type: Knowledge\n"
            "sources:\n"
            f"{metadata}"
            "---\n\n"
            "# Topic\n\n"
            f"A durable fact.[^{marker}]\n\n"
            f"[^{marker}]: {definition}\n",
            encoding="utf-8",
        )
        return path

    def test_accepts_grouped_project_root_metadata_reference(self) -> None:
        _, selected = self.source()
        self.destination()
        qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_accepts_one_marker_grouping_multiple_sources(self) -> None:
        _, selected_a = self.source("incident.md")
        _, selected_b = self.source("remediation.md")
        self.destination(
            source_rows=[
                ("incident", "incident.md"),
                ("remediation", "remediation.md"),
            ],
            definition=(
                'Sources: `source:incident` - "Incident review"; '
                '`source:remediation` - "Remediation".'
            ),
        )
        qualification_inbox.validate_inbox_structural_fidelity(
            self.project,
            selected_a + selected_b,
        )

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
                '\n[^1]: Sources: `source:source-fact` - "Fact".\n',
                "\n",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "requires exactly one definition",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_unknown_grouped_source_reference(self) -> None:
        _, selected = self.source()
        self.destination(definition='Sources: `source:other-fact` - "Fact".')
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "references unknown sources id 'other-fact'",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_old_source_id_marker_format(self) -> None:
        _, selected = self.source()
        self.destination(marker="source-fact")
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "must be a positive decimal integer",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_group_without_source_local_detail(self) -> None:
        _, selected = self.source()
        self.destination(definition="Sources: `source:source-fact`")
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "malformed grouped source attribution",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_group_that_repeats_source_link(self) -> None:
        _, selected = self.source()
        self.destination(
            definition=(
                "Sources: `source:source-fact` - "
                "[Source](../inbox/processed/source.md)."
            )
        )
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "must not repeat source links from metadata",
        ):
            qualification_inbox.validate_inbox_structural_fidelity(self.project, selected)

    def test_rejects_repeated_source_reference_in_one_group(self) -> None:
        _, selected = self.source()
        self.destination(
            definition=(
                'Sources: `source:source-fact` - "Fact"; '
                '`source:source-fact` - "Same fact".'
            )
        )
        with self.assertRaisesRegex(
            qualification_inbox.InboxStructuralError,
            "repeats sources id 'source-fact'",
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
