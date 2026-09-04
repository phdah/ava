from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

OBSOLETE_PATHS = (
    "internal/release/qualification_automation.py",
    "internal/release/qualification_work.py",
    "internal/release/qualification_phase_runner.py",
    "internal/release/qualification_phase_automation.py",
    "internal/release/qualification_phase_gate.py",
    "internal/release/qualification/phase-state.json",
    "internal/release/qualification/audit-prompt.md",
    "internal/release/qualification/schemas/audit-output.schema.json",
    "internal/release/qualification/schemas/edge-independent-run.schema.json",
    "internal/release/qualification/schemas/session-inventory.schema.json",
    "internal/release/qualification/schemas/run-record.schema.json",
    "internal/release/qualification/schemas/work-run-record.schema.json",
    "internal/release/tests/test_qualification_automation.py",
    "internal/release/tests/test_qualification_execution_identity.py",
    "internal/release/tests/test_qualification_work.py",
    "internal/release/tests/test_qualification_phases.py",
    "internal/release/alpha-qualification.md",
    "internal/release/fixtures/alpha-qualification.json",
    "internal/release/tests/test_alpha_qualification.py",
    "internal/release/validate_upgrade_impact.py",
    "internal/release/tests/test_upgrade_impact.py",
)

LIVE_DOCS = (
    "internal/release/index.md",
    "internal/release/procedure.md",
    "internal/release/qualification-automation.md",
    "internal/release/qualification-execution.md",
    "internal/release/qualification/index.md",
    "internal/release/qualification/schemas/index.md",
)

LIVE_IMPLEMENTATION = (
    "internal/release/qualification.py",
    "internal/release/qualification_engine.py",
    "internal/release/qualification_state.py",
    "internal/release/qualification_ci.py",
    "internal/release/run-release-qualification.sh",
    "internal/release/validate-boundaries.sh",
    "internal/release/test.sh",
)


class ReleaseSurfaceTests(unittest.TestCase):
    def test_obsolete_release_paths_are_absent(self) -> None:
        for relative in OBSOLETE_PATHS:
            with self.subTest(path=relative):
                self.assertFalse((ROOT / relative).exists(), relative)

    def test_live_release_docs_use_current_terminology(self) -> None:
        forbidden = (
            "session-neutral",
            "ChatGPT Work",
            "qualification_work.py",
            "qualification_phase_",
            "alpha-qualification",
            "validate_upgrade_impact.py",
        )
        for relative in LIVE_DOCS:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for term in forbidden:
                with self.subTest(path=relative, term=term):
                    self.assertNotIn(term, text)

    def test_live_implementation_has_no_deleted_path_references(self) -> None:
        forbidden = (
            "qualification_automation.py",
            "qualification_work.py",
            "qualification_phase_runner.py",
            "qualification_phase_automation.py",
            "qualification_phase_gate.py",
            "work-run-record.schema.json",
            "validate_upgrade_impact.py",
            "qualification_model",
            "audit_model",
        )
        for relative in LIVE_IMPLEMENTATION:
            text = (ROOT / relative).read_text(encoding="utf-8")
            for term in forbidden:
                with self.subTest(path=relative, term=term):
                    self.assertNotIn(term, text)

    def test_current_qualification_entrypoints_have_distinct_roles(self) -> None:
        cli = (ROOT / "internal/release/qualification.py").read_text(encoding="utf-8")
        engine = (ROOT / "internal/release/qualification_engine.py").read_text(encoding="utf-8")
        state = (ROOT / "internal/release/qualification_state.py").read_text(encoding="utf-8")
        ci = (ROOT / "internal/release/qualification_ci.py").read_text(encoding="utf-8")
        setup = (ROOT / "internal/release/run-release-qualification.sh").read_text(encoding="utf-8")
        self.assertIn("qualification_engine", cli)
        self.assertIn("deterministic Ava release qualification engine", engine)
        self.assertIn("Current deterministic release qualification state helpers", state)
        self.assertIn("run-release-qualification.sh", ci)
        self.assertIn("qualify-release.sh", setup)


if __name__ == "__main__":
    unittest.main()
