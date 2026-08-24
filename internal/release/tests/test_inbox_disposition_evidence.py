from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = SOURCE_ROOT / "internal/release/fixtures/synthetic-qualification-vault"
GENERATOR = FIXTURE_ROOT / "fixture.py"
MATRIX = FIXTURE_ROOT / "qualification-matrix.json"
AUDIT_PROMPT = SOURCE_ROOT / "internal/release/qualification/audit-prompt.md"
FIDELITY_CONTRACT = SOURCE_ROOT / "templates/base/shared/instructions/inbox-ingestion-fidelity.md"


class InboxDispositionEvidenceTests(unittest.TestCase):
    def test_complete_inbox_requires_rendered_disposition_reconciliation(self) -> None:
        matrix = json.loads(MATRIX.read_text())
        scenario = next(item for item in matrix["scenarios"] if item["id"] == "complete-pending-inbox")
        prompt = scenario["prompt"]
        self.assertIn("final rendered trusted destinations", prompt)
        self.assertIn("non-durable section remains absent", prompt)
        self.assertIn("ambiguous section or source pending", prompt)
        self.assertIn("Derive final disposition totals only after", prompt)

        fidelity = FIDELITY_CONTRACT.read_text()
        self.assertIn("# Rendered disposition reconciliation", fidelity)
        self.assertIn("A running tally, child-reported tally, or section ledger by itself is not completion evidence", fidelity)
        self.assertIn("Whole-source copying, whole-source summarization", fidelity)
        self.assertIn("no `non-durable` meaning was promoted into trusted destinations", fidelity)

        audit = AUDIT_PROMPT.read_text()
        self.assertIn("review section dispositions against the final rendered trusted destinations", audit)
        self.assertIn("non-durable source passages or meaning are absent from trusted destinations", audit)
        self.assertIn("A whole-source copy or summary", audit)
        self.assertIn("totals were not reconciled against the rendered destinations", audit)

    def test_fixture_contains_mixed_sources_that_expose_whole_source_promotion(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "vault"
            result = subprocess.run(
                ["python3", str(GENERATOR), "generate", str(output)],
                cwd=SOURCE_ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

            oracle = json.loads((output / "oracle/baseline.json").read_text())
            non_durable = [
                section
                for record in oracle["files"]
                for section in record["sections"]
                if section["disposition"] == "non-durable"
            ]
            self.assertTrue(non_durable)
            self.assertTrue(all(not section["destinations"] for section in non_durable))

            mixed_records = [
                record
                for record in oracle["files"]
                if {section["disposition"] for section in record["sections"]} >= {"mapped", "non-durable"}
            ]
            self.assertTrue(mixed_records)


if __name__ == "__main__":
    unittest.main()
