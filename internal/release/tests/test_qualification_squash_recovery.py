from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from internal.release import qualification_squash_recovery as recovery


class QualificationSquashRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "internal/release/catalogs").mkdir(parents=True)
        (self.root / "internal/release/qualification/runs").mkdir(parents=True)
        self.git("init")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def git(self, *args: str, input_text: str | None = None) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            check=True,
            text=True,
            input=input_text,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result.stdout.strip()

    def write_json(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-m", message)
        return self.git("rev-parse", "HEAD")

    def historical_acceptance(self, previous: str) -> dict:
        return {
            "previous_version": previous,
            "status": "accepted",
            "basis": "historical-backfill",
            "run_id": None,
            "qualified_revision": None,
            "accepted_at": "2026-08-17T10:26:00Z",
            "accepted_by": "historical-backfill",
        }

    def build_squash_history(self, *, change_release_content: bool = False) -> tuple[str, str, str, str]:
        self.write_json(
            self.root / "internal/release/catalogs/1.0.0-alpha.18.json",
            {
                "catalog_schema": 1,
                "target_version": "1.0.0-alpha.18",
                "edge": {"from": "1.0.0-alpha.17", "to": "1.0.0-alpha.18"},
                "guidance": [],
                "retired_sources": [],
            },
        )
        (self.root / "version.txt").write_text("1.0.0-alpha.18\n", encoding="utf-8")
        self.write_json(
            self.root / "internal/release/qualification/current-state.json",
            {
                "schema_version": 2,
                "active_pair": "alpha18-to-alpha19-local",
                "pairs": {
                    "alpha18-to-alpha19-local": {
                        "historical": False,
                        "latest_run_id": None,
                        "status": "not-run",
                        "user_signoff": None,
                    }
                },
                "release_acceptance": {
                    "1.0.0-alpha.18": self.historical_acceptance("1.0.0-alpha.17")
                },
            },
        )
        base = self.commit("release PR base")

        (self.root / "version.txt").write_text("1.0.0-alpha.19\n", encoding="utf-8")
        (self.root / "release-content.txt").write_text("qualified\n", encoding="utf-8")
        qualified = self.commit("qualified release candidate")

        if change_release_content:
            (self.root / "release-content.txt").write_text("changed after qualification\n", encoding="utf-8")

        run_id = "run-alpha19"
        signoff = {"identity": "user:test", "time": "2026-09-05T06:40:09Z"}
        self.write_json(
            self.root / f"internal/release/qualification/runs/{run_id}.json",
            {
                "pair_id": "alpha18-to-alpha19-local",
                "automated_state": "awaiting-user-signoff",
                "mechanical_error": None,
                "user_signoff": signoff,
                "source": {"version": "1.0.0-alpha.18"},
                "target": {
                    "version": "1.0.0-alpha.19",
                    "kind": "local",
                    "source_revision": qualified,
                },
                "execution_identity": {"repository_revision": qualified},
            },
        )
        self.write_json(
            self.root / "internal/release/qualification/current-state.json",
            {
                "schema_version": 2,
                "active_pair": "alpha18-to-alpha19-local",
                "pairs": {
                    "alpha18-to-alpha19-local": {
                        "historical": False,
                        "latest_run_id": run_id,
                        "status": "accepted",
                        "user_signoff": signoff,
                    }
                },
                "release_acceptance": {
                    "1.0.0-alpha.18": self.historical_acceptance("1.0.0-alpha.17"),
                    "1.0.0-alpha.19": {
                        "previous_version": "1.0.0-alpha.18",
                        "status": "accepted",
                        "basis": "qualified-run",
                        "run_id": run_id,
                        "qualified_revision": qualified,
                        "accepted_at": signoff["time"],
                        "accepted_by": signoff["identity"],
                    },
                },
            },
        )
        accepted_head = self.commit("record qualification acceptance")
        accepted_tree = self.git("rev-parse", f"{accepted_head}^{{tree}}")
        squash = self.git(
            "commit-tree",
            accepted_tree,
            "-p",
            base,
            input_text="squash release PR\n",
        )
        self.git("reset", "--hard", squash)
        return base, qualified, squash, accepted_tree

    def test_exact_recorded_squash_tree_is_recoverable(self) -> None:
        base, _, squash, tree = self.build_squash_history()
        with (
            mock.patch.object(recovery, "TAGGED_REVISION", squash),
            mock.patch.object(recovery, "BASE_REVISION", base),
            mock.patch.object(recovery, "ACCEPTED_TREE", tree),
        ):
            message = recovery.validate_alpha19_squash_recovery(
                self.root,
                previous_version="1.0.0-alpha.18",
                base_revision=base,
            )
        self.assertIn("validated one-time alpha.19 squash recovery", message)

    def test_recovery_rejects_release_content_changed_after_qualification(self) -> None:
        base, _, squash, tree = self.build_squash_history(change_release_content=True)
        with (
            mock.patch.object(recovery, "TAGGED_REVISION", squash),
            mock.patch.object(recovery, "BASE_REVISION", base),
            mock.patch.object(recovery, "ACCEPTED_TREE", tree),
        ):
            with self.assertRaisesRegex(
                recovery.acceptance.QualificationAcceptanceError,
                "outside qualification bookkeeping",
            ):
                recovery.validate_alpha19_squash_recovery(
                    self.root,
                    previous_version="1.0.0-alpha.18",
                    base_revision=base,
                )


if __name__ == "__main__":
    unittest.main()
