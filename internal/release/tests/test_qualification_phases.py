from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_phase_gate as gate
from internal.release import qualification_phase_runner as phase_runner
from internal.release import qualification_runner


class QualificationPhaseTests(unittest.TestCase):
    def test_every_matrix_scenario_has_exactly_one_phase(self) -> None:
        _, early = phase_runner.load_phase_matrix(
            phase_runner.REPOSITORY_ROOT,
            "edge-independent",
        )
        _, dependent = phase_runner.load_phase_matrix(
            phase_runner.REPOSITORY_ROOT,
            "edge-dependent",
        )
        self.assertEqual(
            [scenario["id"] for scenario in early["scenarios"]],
            [
                "fresh-empty-install",
                "mature-project-install",
                "registered-private-routing",
                "registered-work-routing",
                "registered-calendar-regression",
                "registered-ambiguous-routing",
                "complete-pending-inbox",
                "managed-modified",
                "managed-missing",
                "managed-corrupt",
                "managed-unexpected",
                "uninstall-reinstall",
            ],
        )
        self.assertEqual(
            [scenario["id"] for scenario in dependent["scenarios"]],
            [
                "interrupted-resume",
                "interrupted-abort",
                "interrupted-rollback",
                "interrupted-finalize",
                "pending-semantic-reconciliation",
            ],
        )

    def test_edge_independent_pair_does_not_require_authored_edge(self) -> None:
        source = qualification_runner.ReleaseIdentity(
            Path("/source"),
            "1.0.0-alpha.1",
            "v1.0.0-alpha.1",
            "1" * 40,
            False,
            {"upgrade_paths": {"edges": []}},
        )
        target = qualification_runner.ReleaseIdentity(
            Path("/target"),
            "1.0.0-alpha.2",
            "v1.0.0-alpha.2",
            "2" * 40,
            False,
            {"upgrade_paths": {"edges": []}},
        )
        phase_runner.validate_release_pair(source, target)
        with self.assertRaises(qualification_runner.QualificationError):
            qualification_runner.validate_upgrade_pair(source, target)

    def test_only_edge_authoring_and_early_evidence_preserve_early_result(self) -> None:
        run_id = "20260902T100000000000Z-pair"
        allowed = {
            "internal/release/qualification/phase-state.json",
            f"internal/release/qualification/phase-runs/{run_id}.json",
            f"internal/release/qualification/phase-runs/{run_id}.audit.json",
            "internal/release/catalogs/1.2.3.json",
            "internal/release/guidance/1.2.3/from-1.2.2/UPGRADE.md",
            "internal/release/migrations/1.2.2-to-1.2.3/apply.py",
        }
        self.assertEqual(
            gate.invalidating_phase_changes(
                allowed,
                target_version="1.2.3",
                prerequisite_run_id=run_id,
            ),
            [],
        )
        self.assertEqual(
            gate.invalidating_phase_changes(
                {*allowed, "templates/base/AGENTS.md", "internal/release/qualification_runner.py"},
                target_version="1.2.3",
                prerequisite_run_id=run_id,
            ),
            ["internal/release/qualification_runner.py", "templates/base/AGENTS.md"],
        )

    def test_final_phase_requires_early_before_edge_and_rejects_invalidating_change(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self._git(root, "init")
            self._git(root, "config", "user.email", "qualification@example.invalid")
            self._git(root, "config", "user.name", "Qualification Test")
            (root / "version.txt").write_text("1.0.0-alpha.2\n", encoding="utf-8")
            (root / "templates/base").mkdir(parents=True)
            (root / "templates/base/AGENTS.md").write_text("early target\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "early target")
            early_revision = self._git(root, "rev-parse", "HEAD").stdout.strip()

            run_id = "20260902T100000000000Z-alpha1-to-alpha2"
            source = {
                "kind": "published",
                "version": "1.0.0-alpha.1",
                "tag": "v1.0.0-alpha.1",
                "source_revision": "1" * 40,
            }
            early_target = {
                "kind": "local",
                "version": "1.0.0-alpha.2",
                "tag": "v1.0.0-alpha.2",
                "source_revision": early_revision,
            }
            early_run = {
                "schema_version": 1,
                "run_id": run_id,
                "pair_id": "alpha1-to-alpha2",
                "qualification_phase": "edge-independent",
                "automated_state": "passed",
                "mechanical_error": None,
                "source": source,
                "target": early_target,
                "execution_identity": {"repository_revision": early_revision},
            }
            phase_runs = root / "internal/release/qualification/phase-runs"
            phase_runs.mkdir(parents=True)
            (phase_runs / f"{run_id}.json").write_text(
                json.dumps(early_run), encoding="utf-8"
            )
            state_path = root / "internal/release/qualification/phase-state.json"
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "pairs": {
                            "alpha1-to-alpha2": {
                                "latest_run_id": run_id,
                                "status": "passed",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            catalog = root / "internal/release/catalogs/1.0.0-alpha.2.json"
            catalog.parent.mkdir(parents=True)
            catalog.write_text("{}\n", encoding="utf-8")
            guidance = (
                root
                / "internal/release/guidance/1.0.0-alpha.2/1.0.0-alpha.1-to-1.0.0-alpha.2/UPGRADE.md"
            )
            guidance.parent.mkdir(parents=True)
            guidance.write_text("# Upgrade\n", encoding="utf-8")
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "author edge")
            final_revision = self._git(root, "rev-parse", "HEAD").stdout.strip()

            final_run = self._final_run(
                source=source,
                final_revision=final_revision,
                prerequisite_run_id=run_id,
                prerequisite_revision=early_revision,
            )
            gate.validate_phase_prerequisite(
                root,
                final_run,
                previous_version="1.0.0-alpha.1",
                target_version="1.0.0-alpha.2",
            )

            (root / "templates/base/AGENTS.md").write_text(
                "changed after early qualification\n", encoding="utf-8"
            )
            self._git(root, "add", ".")
            self._git(root, "commit", "-m", "invalidate early result")
            invalid_revision = self._git(root, "rev-parse", "HEAD").stdout.strip()
            invalid_run = self._final_run(
                source=source,
                final_revision=invalid_revision,
                prerequisite_run_id=run_id,
                prerequisite_revision=early_revision,
            )
            with self.assertRaisesRegex(
                gate.QualificationPhaseGateError,
                "invalidated by post-phase changes",
            ):
                gate.validate_phase_prerequisite(
                    root,
                    invalid_run,
                    previous_version="1.0.0-alpha.1",
                    target_version="1.0.0-alpha.2",
                )

    @staticmethod
    def _final_run(
        *,
        source: dict[str, str],
        final_revision: str,
        prerequisite_run_id: str,
        prerequisite_revision: str,
    ) -> dict[str, object]:
        return {
            "pair_id": "alpha1-to-alpha2",
            "source": source,
            "target": {
                "kind": "local",
                "version": "1.0.0-alpha.2",
                "tag": "v1.0.0-alpha.2",
                "source_revision": final_revision,
            },
            "execution_identity": {
                "qualification_phase": "edge-dependent",
                "repository_revision": final_revision,
                "prerequisite_edge_independent_run_id": prerequisite_run_id,
                "prerequisite_repository_revision": prerequisite_revision,
            },
        }

    @staticmethod
    def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )


if __name__ == "__main__":
    unittest.main()
