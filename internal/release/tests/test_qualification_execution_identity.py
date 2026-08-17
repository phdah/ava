from __future__ import annotations

import unittest
from pathlib import Path

from internal.release import qualification_automation as automation
from internal.release import qualification_runner


class QualificationExecutionIdentityTests(unittest.TestCase):
    @staticmethod
    def release(name: str, asset_digest: str) -> automation.ResolvedRelease:
        identity = qualification_runner.ReleaseIdentity(
            directory=Path(f"/tmp/{name}"),
            version=f"1.0.0-{name}",
            tag=f"v1.0.0-{name}",
            revision=("a" if name == "source" else "b") * 40,
            semantic_review_required=True,
            manifest={},
        )
        return automation.ResolvedRelease(
            kind="local",
            identity=identity,
            release_manifest_sha256=asset_digest,
            asset_sha256={"asset": asset_digest},
            attested=False,
        )

    def test_every_reuse_boundary_changes_execution_namespace(self) -> None:
        source = self.release("source", "1" * 64)
        target = self.release("target", "2" * 64)
        baseline = {
            "source": source,
            "target": target,
            "image_manifest_sha256": "3" * 64,
            "pinned_images": [
                {"file": "a.png", "sha256": "4" * 64, "destination": "corpus/a.png"}
            ],
            "fixture_generator_sha256": "5" * 64,
            "fixture_inventory_sha256": "6" * 64,
            "matrix_sha256": "7" * 64,
            "repository_revision_value": "8" * 40,
            "runner_sha256": "9" * 64,
            "automation_sha256": "a" * 64,
            "opencode_version_value": "1.2.3",
            "qualification_model": "openai/gpt-5.6-sol",
            "audit_model": "openai/gpt-5.6-sol",
        }
        expected, _ = automation.execution_identity(**baseline)
        changed_source = automation.ResolvedRelease(
            kind=source.kind,
            identity=source.identity,
            release_manifest_sha256="b" * 64,
            asset_sha256={"asset": "b" * 64},
            attested=source.attested,
        )
        variations = {
            "source asset": {"source": changed_source},
            "target asset": {"target": self.release("target", "c" * 64)},
            "image manifest": {"image_manifest_sha256": "d" * 64},
            "pinned image": {
                "pinned_images": [
                    {"file": "a.png", "sha256": "e" * 64, "destination": "corpus/a.png"}
                ]
            },
            "fixture generator": {"fixture_generator_sha256": "f" * 64},
            "fixture inventory": {"fixture_inventory_sha256": "0" * 64},
            "matrix": {"matrix_sha256": "1" * 64},
            "repository": {"repository_revision_value": "2" * 40},
            "runner": {"runner_sha256": "3" * 64},
            "automation": {"automation_sha256": "4" * 64},
            "OpenCode": {"opencode_version_value": "1.2.4"},
            "qualification model": {"qualification_model": "openai/other"},
            "audit model": {"audit_model": "openai/other"},
        }
        parent = Path("/tmp/execution")
        expected_root = automation.execution_root_for_identity(parent, expected)
        for label, change in variations.items():
            with self.subTest(label=label):
                actual, _ = automation.execution_identity(**{**baseline, **change})
                self.assertNotEqual(expected, actual)
                self.assertNotEqual(
                    expected_root,
                    automation.execution_root_for_identity(parent, actual),
                )


if __name__ == "__main__":
    unittest.main()
