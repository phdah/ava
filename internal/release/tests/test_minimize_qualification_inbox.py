from __future__ import annotations

import hashlib
import json
import runpy
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[3]
MINIMIZER = SOURCE_ROOT / "internal/release/fixtures/synthetic-qualification-vault/minimize_inbox.py"
MODULE = runpy.run_path(str(MINIMIZER))
minimize = MODULE["minimize"]
select_minimum_records = MODULE["select_minimum_records"]
FORMAT_ORDER = MODULE["FORMAT_ORDER"]
REQUIRED_DISPOSITIONS = MODULE["REQUIRED_DISPOSITIONS"]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def record(name: str, format_name: str, dispositions: tuple[str, ...]) -> dict:
    payload = f"source:{name}\n".encode()
    return {
        "path": f"corpus/01-pre-move/{name}.{format_name}",
        "format": format_name,
        "sha256": sha256_bytes(payload),
        "sections": [
            {"locator": disposition, "disposition": disposition}
            for disposition in dispositions
        ],
    }


class MinimizeQualificationInboxTests(unittest.TestCase):
    def test_selection_is_the_exact_format_lower_bound_and_preserves_dispositions(self) -> None:
        records = [
            record("a", "md", ("mapped", "non-durable")),
            record("b", "txt", ("mapped", "non-durable")),
            record("c", "csv", ("mapped", "non-durable", "pending")),
            record("d", "docx", ("mapped",)),
            record("e", "pdf", ("mapped", "non-durable")),
            record("f", "pptx", ("mapped", "non-durable")),
            record("g", "ics", ("mapped", "non-durable")),
            record("extra", "md", ("mapped",)),
        ]

        selected = select_minimum_records(records)

        self.assertEqual(len(selected), len(FORMAT_ORDER))
        self.assertEqual({item["format"] for item in selected}, set(FORMAT_ORDER))
        self.assertEqual(
            {
                section["disposition"]
                for item in selected
                for section in item["sections"]
            },
            REQUIRED_DISPOSITIONS,
        )

    def test_minimize_prunes_materialized_inbox_and_records_selection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            inbox = root / "variants/04-complete-pending-inbox/project/inbox"
            inbox.mkdir(parents=True)
            (root / "oracle").mkdir()

            records = [
                record("a", "md", ("mapped", "non-durable")),
                record("b", "txt", ("mapped", "non-durable")),
                record("c", "csv", ("mapped", "non-durable", "pending")),
                record("d", "docx", ("mapped",)),
                record("e", "pdf", ("mapped", "non-durable")),
                record("f", "pptx", ("mapped", "non-durable")),
                record("g", "ics", ("mapped", "non-durable")),
                record("extra", "md", ("mapped",)),
            ]
            for item in records:
                name = Path(item["path"]).name
                stem = Path(name).stem
                (inbox / name).write_bytes(f"source:{stem}\n".encode())

            (root / "oracle/baseline.json").write_text(
                json.dumps({"files": records}), encoding="utf-8"
            )
            variant = root / "variants/04-complete-pending-inbox"
            (variant / "scenario.json").write_text(
                json.dumps({"schema_version": 1, "scenario_id": "complete-pending-inbox"}),
                encoding="utf-8",
            )
            (root / "variants/index.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "families": [
                            {"id": "complete-pending-inbox", "inventory": []}
                        ],
                    }
                ),
                encoding="utf-8",
            )

            selected = minimize(root)

            remaining = {path.name for path in inbox.iterdir() if path.is_file()}
            self.assertEqual(len(remaining), 7)
            self.assertEqual(
                remaining,
                {Path(item["path"]).name for item in selected},
            )
            selection = json.loads((variant / "selection.json").read_text())
            self.assertEqual(selection["minimum_source_count"], 7)
            self.assertEqual(set(selection["required_formats"]), set(FORMAT_ORDER))
            self.assertEqual(
                set(selection["required_dispositions"]), REQUIRED_DISPOSITIONS
            )
            family = json.loads((root / "variants/index.json").read_text())["families"][0]
            self.assertTrue(any(item["path"] == "selection.json" for item in family["inventory"]))


if __name__ == "__main__":
    unittest.main()
