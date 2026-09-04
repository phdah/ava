from __future__ import annotations

import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from internal.release.publication import (
    PublicationError,
    PublicationIdentity,
    extract_release_notes,
    plan_assets,
    resolve_identity,
    select_release,
    stage_missing_assets,
)


def digest(value: bytes) -> str:
    return "sha256:" + hashlib.sha256(value).hexdigest()


class PublicationTests(unittest.TestCase):
    def identity(self) -> PublicationIdentity:
        return PublicationIdentity(
            version="1.0.0-alpha.17",
            tag="v1.0.0-alpha.17",
            source_revision="a" * 40,
            previous_revision="b" * 40,
            previous_version="1.0.0-alpha.16",
            channel="alpha",
            source_date_epoch="1",
            published_at="1970-01-01T00:00:01Z",
        )

    def release(
        self,
        assets,
        *,
        draft=True,
        body="## [1.0.0-alpha.17]\n\nNotes\n",
        release_id=1,
    ):
        identity = self.identity()
        return {
            "id": release_id,
            "tag_name": identity.tag,
            "name": identity.tag,
            "target_commitish": identity.source_revision,
            "prerelease": True,
            "draft": draft,
            "body": body,
            "assets": assets,
        }

    def write_assets(self, root: Path) -> dict[str, bytes]:
        values = {
            "ava-install.sh": b"installer\n",
            "ava-base.tar.gz": b"base",
            "SHA256SUMS": b"sums\n",
        }
        for name, value in values.items():
            (root / name).write_bytes(value)
        return values

    def asset(self, name: str, value: bytes) -> dict[str, str]:
        return {"name": name, "digest": digest(value)}

    def test_extract_release_notes_selects_exact_section(self) -> None:
        changelog = (
            "# Changelog\n\n"
            "## [1.0.0-alpha.17](compare) (2026-09-02)\n\n"
            "### Features\n\n* current\n\n"
            "## [1.0.0-alpha.16](compare) (2026-09-01)\n\n* previous\n"
        )
        self.assertEqual(
            extract_release_notes(changelog, "1.0.0-alpha.17"),
            "## [1.0.0-alpha.17](compare) (2026-09-02)\n\n"
            "### Features\n\n* current\n",
        )

    def test_missing_release_stages_every_asset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory) / "release"
            release_dir.mkdir()
            values = self.write_assets(release_dir)
            state, missing, complete = plan_assets(
                release_dir,
                None,
                identity=self.identity(),
                expected_body="## [1.0.0-alpha.17]\n\nNotes\n",
            )
            self.assertEqual(state, "missing")
            self.assertEqual({path.name for path in missing}, set(values))
            self.assertFalse(complete)

    def test_draft_partial_release_reuses_matching_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory) / "release"
            release_dir.mkdir()
            values = self.write_assets(release_dir)
            release = self.release(
                [self.asset("ava-install.sh", values["ava-install.sh"])]
            )
            state, missing, complete = plan_assets(
                release_dir,
                release,
                identity=self.identity(),
                expected_body=release["body"],
            )
            self.assertEqual(state, "draft")
            self.assertEqual(
                {path.name for path in missing},
                {"ava-base.tar.gz", "SHA256SUMS"},
            )
            self.assertFalse(complete)

    def test_mismatched_existing_asset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            self.write_assets(release_dir)
            release = self.release([self.asset("ava-install.sh", b"wrong")])
            with self.assertRaisesRegex(PublicationError, "digest mismatch"):
                plan_assets(
                    release_dir,
                    release,
                    identity=self.identity(),
                    expected_body=release["body"],
                )

    def test_unexpected_asset_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            self.write_assets(release_dir)
            release = self.release(
                [{"name": "unexpected.txt", "digest": digest(b"x")}]
            )
            with self.assertRaisesRegex(PublicationError, "unexpected assets"):
                plan_assets(
                    release_dir,
                    release,
                    identity=self.identity(),
                    expected_body=release["body"],
                )

    def test_published_exact_release_is_safe_noop(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            values = self.write_assets(release_dir)
            release = self.release(
                [self.asset(name, value) for name, value in values.items()],
                draft=False,
            )
            state, missing, complete = plan_assets(
                release_dir,
                release,
                identity=self.identity(),
                expected_body=release["body"],
            )
            self.assertEqual(state, "published")
            self.assertEqual(missing, [])
            self.assertTrue(complete)

    def test_published_incomplete_release_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            values = self.write_assets(release_dir)
            release = self.release(
                [self.asset("ava-install.sh", values["ava-install.sh"])],
                draft=False,
            )
            with self.assertRaisesRegex(
                PublicationError,
                "published GitHub Release is missing",
            ):
                plan_assets(
                    release_dir,
                    release,
                    identity=self.identity(),
                    expected_body=release["body"],
                )

    def test_release_metadata_mismatch_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            self.write_assets(release_dir)
            release = self.release([])
            release["target_commitish"] = "c" * 40
            with self.assertRaisesRegex(
                PublicationError,
                "target_commitish mismatch",
            ):
                plan_assets(
                    release_dir,
                    release,
                    identity=self.identity(),
                    expected_body=release["body"],
                )

    def test_select_release_returns_missing_when_no_tag_matches(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            self.write_assets(release_dir)
            unrelated = self.release([], release_id=2)
            unrelated["tag_name"] = "v1.0.0-alpha.16"
            selected, state, redundant = select_release(
                release_dir,
                [unrelated],
                identity=self.identity(),
                expected_body="## [1.0.0-alpha.17]\n\nNotes\n",
            )
            self.assertIsNone(selected)
            self.assertEqual(state, "missing")
            self.assertEqual(redundant, [])

    def test_select_release_prefers_most_complete_compatible_draft(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            values = self.write_assets(release_dir)
            empty = self.release([], release_id=10)
            partial = self.release(
                [self.asset("ava-install.sh", values["ava-install.sh"])],
                release_id=11,
            )
            selected, state, redundant = select_release(
                release_dir,
                [empty, partial],
                identity=self.identity(),
                expected_body=empty["body"],
            )
            self.assertIsNotNone(selected)
            assert selected is not None
            self.assertEqual(selected["id"], 11)
            self.assertEqual(state, "draft")
            self.assertEqual(redundant, [10])

    def test_select_release_prefers_oldest_id_when_drafts_are_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            self.write_assets(release_dir)
            older = self.release([], release_id=10)
            newer = self.release([], release_id=11)
            selected, state, redundant = select_release(
                release_dir,
                [newer, older],
                identity=self.identity(),
                expected_body=older["body"],
            )
            self.assertIsNotNone(selected)
            assert selected is not None
            self.assertEqual(selected["id"], 10)
            self.assertEqual(state, "draft")
            self.assertEqual(redundant, [11])

    def test_select_release_rejects_incompatible_duplicate_before_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            self.write_assets(release_dir)
            valid = self.release([], release_id=10)
            invalid = self.release([], release_id=11)
            invalid["target_commitish"] = "c" * 40
            with self.assertRaisesRegex(PublicationError, "target_commitish mismatch"):
                select_release(
                    release_dir,
                    [valid, invalid],
                    identity=self.identity(),
                    expected_body=valid["body"],
                )

    def test_select_release_never_deduplicates_published_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            release_dir = Path(directory)
            values = self.write_assets(release_dir)
            published = self.release(
                [self.asset(name, value) for name, value in values.items()],
                draft=False,
                release_id=10,
            )
            draft = self.release([], release_id=11)
            with self.assertRaisesRegex(PublicationError, "published state"):
                select_release(
                    release_dir,
                    [published, draft],
                    identity=self.identity(),
                    expected_body=published["body"],
                )

    def test_stage_missing_assets_replaces_old_staging_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "a").write_text("a")
            upload = root / "upload"
            upload.mkdir()
            (upload / "stale").write_text("stale")
            stage_missing_assets([source / "a"], upload)
            self.assertEqual({path.name for path in upload.iterdir()}, {"a"})

    def test_identity_recovery_uses_durable_tag_not_action_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", root], check=True)
            subprocess.run(
                ["git", "-C", root, "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", root, "config", "user.email", "test@example.com"],
                check=True,
            )

            (root / "version.txt").write_text("1.0.0-alpha.16\n")
            subprocess.run(["git", "-C", root, "add", "version.txt"], check=True)
            subprocess.run(
                ["git", "-C", root, "commit", "-qm", "previous"],
                check=True,
            )

            (root / "version.txt").write_text("1.0.0-alpha.17\n")
            subprocess.run(["git", "-C", root, "add", "version.txt"], check=True)
            subprocess.run(
                ["git", "-C", root, "commit", "-qm", "release"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", root, "tag", "v1.0.0-alpha.17"],
                check=True,
            )

            identity = resolve_identity(root)
            self.assertIsNotNone(identity)
            assert identity is not None
            self.assertEqual(identity.version, "1.0.0-alpha.17")
            self.assertEqual(identity.previous_version, "1.0.0-alpha.16")

    def test_normal_nonrelease_push_is_not_eligible(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", root], check=True)
            subprocess.run(
                ["git", "-C", root, "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", root, "config", "user.email", "test@example.com"],
                check=True,
            )
            (root / "version.txt").write_text("1.0.0-alpha.16\n")
            subprocess.run(["git", "-C", root, "add", "version.txt"], check=True)
            subprocess.run(
                ["git", "-C", root, "commit", "-qm", "release"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", root, "tag", "v1.0.0-alpha.16"],
                check=True,
            )
            (root / "README.md").write_text("later\n")
            subprocess.run(["git", "-C", root, "add", "README.md"], check=True)
            subprocess.run(
                ["git", "-C", root, "commit", "-qm", "later"],
                check=True,
            )

            self.assertIsNone(resolve_identity(root))

    def test_requested_recovery_tag_must_target_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", root], check=True)
            subprocess.run(
                ["git", "-C", root, "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", root, "config", "user.email", "test@example.com"],
                check=True,
            )
            (root / "version.txt").write_text("1.0.0-alpha.17\n")
            subprocess.run(["git", "-C", root, "add", "version.txt"], check=True)
            subprocess.run(
                ["git", "-C", root, "commit", "-qm", "tagged"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", root, "tag", "v1.0.0-alpha.17"],
                check=True,
            )
            (root / "README.md").write_text("later\n")
            subprocess.run(["git", "-C", root, "add", "README.md"], check=True)
            subprocess.run(
                ["git", "-C", root, "commit", "-qm", "later"],
                check=True,
            )

            with self.assertRaisesRegex(PublicationError, "points to"):
                resolve_identity(root, requested_tag="v1.0.0-alpha.17")


if __name__ == "__main__":
    unittest.main()
