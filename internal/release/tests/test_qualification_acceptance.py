from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_acceptance as acceptance


class QualificationAcceptanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "internal/release/catalogs").mkdir(parents=True)
        (self.root / "internal/release/qualification/runs").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def write_json(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def record(self, previous: str, target: str) -> dict:
        return {
            "catalog_schema": 1,
            "target_version": target,
            "edge": {"from": previous, "to": target},
            "guidance": [],
            "retired_sources": [],
        }

    def accepted(self, previous: str, *, basis: str = "historical-backfill", run_id=None, revision=None) -> dict:
        return {
            "previous_version": previous,
            "status": "accepted",
            "basis": basis,
            "run_id": run_id,
            "qualified_revision": revision,
            "accepted_at": "2026-08-17T10:26:00Z",
            "accepted_by": "user:test" if basis == "qualified-run" else "historical-backfill",
        }

    def write_state(self, ledger: dict, *, pair_status: str = "not-run", run_id=None) -> None:
        self.write_json(
            self.root / "internal/release/qualification/current-state.json",
            {
                "schema_version": 2,
                "active_pair": "pair",
                "pairs": {
                    "pair": {
                        "historical": False,
                        "latest_run_id": run_id,
                        "status": pair_status,
                        "user_signoff": None,
                    }
                },
                "release_acceptance": ledger,
            },
        )

    def test_historical_release_ledger_must_cover_catalog_history(self) -> None:
        self.write_json(
            self.root / "internal/release/catalogs/1.0.1.json",
            self.record("1.0.0", "1.0.1"),
        )
        self.write_json(
            self.root / "internal/release/catalogs/1.0.2.json",
            self.record("1.0.1", "1.0.2"),
        )
        self.write_state(
            {
                "1.0.1": self.accepted("1.0.0"),
                "1.0.2": self.accepted("1.0.1"),
            }
        )
        acceptance.validate_acceptance_ledger(self.root, through_version="1.0.2")

        state = json.loads(
            (self.root / "internal/release/qualification/current-state.json").read_text()
        )
        del state["release_acceptance"]["1.0.2"]
        self.write_json(self.root / "internal/release/qualification/current-state.json", state)
        with self.assertRaisesRegex(acceptance.QualificationAcceptanceError, "no accepted"):
            acceptance.validate_acceptance_ledger(self.root, through_version="1.0.2")

    def test_user_signoff_promotes_clean_run_to_release_acceptance(self) -> None:
        revision = "1" * 40
        run_id = "run-1"
        self.write_state({}, pair_status="awaiting-user-signoff", run_id=run_id)
        self.write_json(
            self.root / f"internal/release/qualification/runs/{run_id}.json",
            {
                "pair_id": "pair",
                "automated_state": "awaiting-user-signoff",
                "mechanical_error": None,
                "user_signoff": None,
                "source": {"version": "1.0.0"},
                "target": {
                    "version": "1.0.1",
                    "kind": "local",
                    "source_revision": revision,
                },
                "execution_identity": {"repository_revision": revision},
            },
        )

        acceptance.accept_run(
            self.root,
            identity="user:test",
            run_id=run_id,
            accepted_at="2026-08-17T10:26:00Z",
        )
        state = json.loads(
            (self.root / "internal/release/qualification/current-state.json").read_text()
        )
        self.assertEqual(state["pairs"]["pair"]["status"], "accepted")
        accepted = state["release_acceptance"]["1.0.1"]
        self.assertEqual(accepted["basis"], "qualified-run")
        self.assertEqual(accepted["qualified_revision"], revision)
        run = json.loads(
            (self.root / f"internal/release/qualification/runs/{run_id}.json").read_text()
        )
        self.assertEqual(run["user_signoff"]["identity"], "user:test")

    def git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.strip()

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def test_release_pr_gate_allows_only_qualification_state_changes_after_run(self) -> None:
        self.git("init")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        (self.root / "version.txt").write_text("1.0.0\n")
        self.write_state({})
        base = self.commit("base")

        self.write_json(
            self.root / "internal/release/catalogs/1.0.1.json",
            self.record("1.0.0", "1.0.1"),
        )
        (self.root / "version.txt").write_text("1.0.1\n")
        qualified_revision = self.commit("release candidate")

        run_id = "run-2"
        signoff = {"identity": "user:test", "time": "2026-08-17T10:26:00Z"}
        self.write_json(
            self.root / f"internal/release/qualification/runs/{run_id}.json",
            {
                "pair_id": "pair",
                "automated_state": "awaiting-user-signoff",
                "mechanical_error": None,
                "user_signoff": signoff,
                "source": {"version": "1.0.0"},
                "target": {
                    "version": "1.0.1",
                    "kind": "local",
                    "source_revision": qualified_revision,
                },
                "execution_identity": {"repository_revision": qualified_revision},
            },
        )
        self.write_state(
            {
                "1.0.1": self.accepted(
                    "1.0.0",
                    basis="qualified-run",
                    run_id=run_id,
                    revision=qualified_revision,
                ),
            },
            pair_status="accepted",
            run_id=run_id,
        )
        state = json.loads(
            (self.root / "internal/release/qualification/current-state.json").read_text()
        )
        state["pairs"]["pair"]["user_signoff"] = signoff
        self.write_json(self.root / "internal/release/qualification/current-state.json", state)
        self.commit("accept qualification")

        message = acceptance.validate_release_pr_acceptance(
            self.root,
            "1.0.0",
            base_revision=base,
        )
        self.assertIn(run_id, message)

        (self.root / "README.md").write_text("changed after qualification\n")
        self.commit("change release content")
        with self.assertRaisesRegex(
            acceptance.QualificationAcceptanceError,
            "changed after qualification",
        ):
            acceptance.validate_release_pr_acceptance(
                self.root,
                "1.0.0",
                base_revision=base,
            )


if __name__ == "__main__":
    unittest.main()
