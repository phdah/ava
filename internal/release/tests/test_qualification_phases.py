from __future__ import annotations

import unittest
from pathlib import Path

from internal.release import qualification_work as work


class QualificationStageTests(unittest.TestCase):
    def test_release_qualification_has_single_shell_entrypoint(self) -> None:
        release_root = work.REPOSITORY_ROOT / "internal/release"
        entrypoints = sorted(path.name for path in release_root.glob("qualify-*.sh"))
        self.assertEqual(entrypoints, ["qualify-release.sh"])
        index = (release_root / "index.md").read_text(encoding="utf-8")
        self.assertIn("qualification execution entry point", index)

    def test_pre_edge_is_ephemeral_and_final_is_authoritative(self) -> None:
        procedure = (
            work.REPOSITORY_ROOT / "internal/release/procedure.md"
        ).read_text(encoding="utf-8")
        automation = (
            work.REPOSITORY_ROOT / "internal/release/qualification-automation.md"
        ).read_text(encoding="utf-8")
        for text in (procedure, automation):
            self.assertIn("pre-edge", text)
            self.assertIn("final", text)
            self.assertIn("writes no", text.lower())
            self.assertIn("authoritative", text.lower())
        self.assertIn("There is no committed early-run ancestry chain", procedure)
        self.assertIn("single authoritative release qualification", automation)

    def test_acceptance_no_longer_depends_on_two_phase_gate(self) -> None:
        release_root = work.REPOSITORY_ROOT / "internal/release"
        shell = (release_root / "accept-release-qualification.sh").read_text(
            encoding="utf-8"
        )
        workflow = (
            work.REPOSITORY_ROOT / ".github/workflows/release-pr-policy.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("qualification_acceptance.py", shell)
        self.assertNotIn("qualification_phase_gate.py", shell)
        self.assertNotIn("qualification_phase_gate", workflow)

    def test_historical_phase_modules_are_not_canonical(self) -> None:
        index = (
            work.REPOSITORY_ROOT / "internal/release/index.md"
        ).read_text(encoding="utf-8")
        self.assertIn("Historical phase contract", index)
        self.assertIn("Historical two-phase gate", index)
        self.assertIn("not the canonical execution or acceptance path", index)


if __name__ == "__main__":
    unittest.main()
