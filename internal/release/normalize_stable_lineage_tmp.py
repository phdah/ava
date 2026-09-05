from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from internal.release.adjacent_edges import make_edge

root = Path.cwd()


def rewrite(path: str, transform) -> None:
    file = root / path
    before = file.read_text(encoding="utf-8")
    after = transform(before)
    if before == after:
        raise SystemExit(f"expected normalization did not change {path}")
    file.write_text(after, encoding="utf-8")


def replace_once(text: str, old: str, new: str, *, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one occurrence, found {count}")
    return text.replace(old, new)


def versioning(text: str) -> str:
    pattern = re.compile(r"# Pre-1\.0 and prerelease policy\n.*?\n# Direct and chained upgrades", re.S)
    replacement = """# Prerelease policy

Ava's supported public lineage begins at stable `1.0.0`. No prerelease is a predecessor of that root release.

SemVer prerelease identifiers remain valid syntax for future release channels when Ava intentionally uses them. Neutral examples are:

- `2.0.0-alpha.1`
- `2.0.0-beta.1`
- `2.0.0-rc.1`

Prereleases may change incompatibly between identifiers. A target prerelease must explicitly declare whether direct upgrade from an earlier prerelease is supported.

Channel representation is derived from the SemVer prerelease identifier:

| Version | Channel |
|---|---|
| `1.2.3` | `stable` |
| `2.0.0-rc.1` | `rc` |
| `2.0.0-beta.1` | `beta` |
| `2.0.0-alpha.1` | `alpha` |

Stable installers must not select prereleases automatically. Exact asset names, URLs, development snapshots, and channel publication rules belong to the GitHub release-assets contract.

# Direct and chained upgrades"""
    result, count = pattern.subn(replacement, text)
    if count != 1:
        raise SystemExit(f"distribution/versioning.md: expected one prerelease policy block, found {count}")
    return result


rewrite("distribution/versioning.md", versioning)

guidance_path = "1.0.0-to-1.0.1/UPGRADE.md"
guidance = {
    "guidance_id": "stable-1-project-contract",
    "path": guidance_path,
    "from_version": "1.0.0",
    "to_version": "1.0.1",
    "supersedes": [],
    "sha256": hashlib.sha256(guidance_path.encode()).hexdigest(),
}
fixture = {
    "catalog_schema": 1,
    "target_version": "1.0.2",
    "supported_sources": ["1.0.0", "1.0.1"],
    "edges": [
        make_edge(
            "1.0.0",
            "1.0.1",
            carry_unresolved_semantic_state=True,
            guidance_paths=[guidance_path],
            semantic_review_required=True,
        ),
        make_edge(
            "1.0.1",
            "1.0.2",
            carry_unresolved_semantic_state=True,
        ),
    ],
    "guidance": [guidance],
}
(root / "internal/release/fixtures/adjacent-upgrade-catalog.json").write_text(
    json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)

matrix_path = root / "internal/release/fixtures/conformance-matrix.json"
matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
matrix["prerelease_transitions"] = [
    {"from": "2.0.0-alpha.1", "to": "2.0.0-alpha.2", "channel": "alpha", "must_be_declared": True},
    {"from": "2.0.0-alpha.2", "to": "2.0.0-alpha.3", "channel": "alpha", "must_be_declared": True},
    {"from": "2.0.0-alpha.3", "to": "2.0.0-alpha.5", "channel": "alpha", "must_be_declared": True},
    {"from": "2.0.0-alpha.4", "to": "2.0.0-alpha.5", "channel": "alpha", "must_be_declared": True},
    {"from": "2.0.0-alpha.6", "to": "2.0.0-alpha.7", "channel": "alpha", "must_be_declared": True},
    {"from": "2.0.0-alpha.5", "to": "2.0.0-rc.1", "channel": "rc", "must_be_declared": True},
    {"from": "2.0.0-rc.1", "to": "2.0.0", "channel": "stable", "must_be_declared": True},
]
matrix_path.write_text(json.dumps(matrix, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def adjacent_tests(text: str) -> str:
    for old, new in (
        ("1.0.0-alpha.1", "1.0.0"),
        ("1.0.0-alpha.2", "1.0.1"),
        ("1.0.0-alpha.3", "1.0.2"),
        ("1.0.0-alpha.4", "1.0.3"),
    ):
        text = text.replace(old, new)
    ambiguous = re.compile(
        r"    def test_rejects_ambiguous_paths\(self\):\n.*?\n    def test_rejects_tampered_edge_digest",
        re.S,
    )
    replacement = '''    def test_rejects_ambiguous_paths(self):
        edges = [
            make_edge("1.0.0", "1.0.1"),
            make_edge("1.0.0", "1.1.0"),
            make_edge("1.0.1", "2.0.0"),
            make_edge("1.1.0", "2.0.0"),
        ]
        with self.assertRaisesRegex(AdjacentEdgeError, "ambiguous"):
            resolve_unique_path(edges, "1.0.0", "2.0.0")

    def test_rejects_tampered_edge_digest'''
    text, count = ambiguous.subn(replacement, text)
    if count != 1:
        raise SystemExit(f"test_adjacent_edges ambiguous block: {count}")
    channel = re.compile(
        r"    def test_model_is_channel_agnostic\(self\):\n.*?\n\n\nif __name__",
        re.S,
    )
    replacement = '''    def test_model_is_channel_agnostic(self):
        catalog = validate_catalog(
            {
                "catalog_schema": 1,
                "target_version": "2.0.0",
                "supported_sources": [
                    "2.0.0-alpha.9",
                    "2.0.0-beta.1",
                    "2.0.0-rc.1",
                ],
                "edges": [
                    make_edge("2.0.0-alpha.9", "2.0.0-beta.1"),
                    make_edge("2.0.0-beta.1", "2.0.0-rc.1"),
                    make_edge("2.0.0-rc.1", "2.0.0"),
                ],
                "guidance": [],
            }
        )
        self.assertEqual(
            3,
            len(
                resolve_unique_path(
                    catalog["edges"], "2.0.0-alpha.9", "2.0.0"
                )
            ),
        )


if __name__'''
    text, count = channel.subn(replacement, text)
    if count != 1:
        raise SystemExit(f"test_adjacent_edges channel block: {count}")
    return text


rewrite("internal/release/tests/test_adjacent_edges.py", adjacent_tests)


def assemble_candidate(text: str) -> str:
    text = text.replace("1.0.0-alpha.15", "1.0.1")
    return replace_once(
        text,
        '            "--channel",\n            "alpha",',
        '            "--channel",\n            "stable",',
        label="assemble candidate channel",
    )


rewrite("internal/release/tests/test_assemble_candidate.py", assemble_candidate)
rewrite(
    "internal/release/tests/test_assembly_contract.py",
    lambda text: text.replace("1.0.0-alpha.1", "1.0.0").replace("1.0.0-alpha.2", "1.0.1"),
)


def conformance_tests(text: str) -> str:
    text = text.replace("1.0.0-alpha.", "2.0.0-alpha.")
    text = text.replace("1.0.0-rc.1", "2.0.0-rc.1")
    return text.replace(
        '                    "from": "2.0.0-rc.1",\n                    "to": "1.0.0",',
        '                    "from": "2.0.0-rc.1",\n                    "to": "2.0.0",',
    )


rewrite("internal/release/tests/test_conformance_matrix.py", conformance_tests)


def publication_tests(text: str) -> str:
    text = text.replace("1.0.0-alpha.17", "1.0.1")
    text = text.replace("1.0.0-alpha.16", "1.0.0")
    text = text.replace('channel="alpha"', 'channel="stable"')
    return text.replace('"prerelease": True', '"prerelease": False')


rewrite("internal/release/tests/test_publication.py", publication_tests)


def acceptance_tests(text: str) -> str:
    historical = re.compile(
        r"    def test_historical_release_ledger_must_cover_catalog_history\(self\) -> None:\n.*?\n    def test_user_signoff_promotes_clean_run_to_release_acceptance",
        re.S,
    )
    historical_replacement = '''    def test_historical_release_ledger_must_cover_catalog_history(self) -> None:
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

    def test_user_signoff_promotes_clean_run_to_release_acceptance'''
    text, count = historical.subn(historical_replacement, text)
    if count != 1:
        raise SystemExit(f"acceptance historical block: {count}")

    text = text.replace('"source": {"version": "1.0.0-alpha.14"}', '"source": {"version": "1.0.0"}')
    text = text.replace('"version": "1.0.0-alpha.15",', '"version": "1.0.1",')
    text = text.replace('accepted = state["release_acceptance"]["1.0.0-alpha.15"]', 'accepted = state["release_acceptance"]["1.0.1"]')

    gate = re.compile(
        r"    def test_release_pr_gate_allows_only_qualification_state_changes_after_run\(self\) -> None:\n.*?\n\n\nif __name__",
        re.S,
    )
    gate_replacement = '''    def test_release_pr_gate_allows_only_qualification_state_changes_after_run(self) -> None:
        self.git("init")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        (self.root / "version.txt").write_text("1.0.0\\n")
        self.write_state({})
        base = self.commit("base")

        self.write_json(
            self.root / "internal/release/catalogs/1.0.1.json",
            self.record("1.0.0", "1.0.1"),
        )
        (self.root / "version.txt").write_text("1.0.1\\n")
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

        (self.root / "README.md").write_text("changed after qualification\\n")
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


if __name__'''
    text, count = gate.subn(gate_replacement, text)
    if count != 1:
        raise SystemExit(f"acceptance release gate block: {count}")
    return text


rewrite("internal/release/tests/test_qualification_acceptance.py", acceptance_tests)
rewrite(
    "internal/release/tests/test_qualification_runner.py",
    lambda text: text.replace("1.0.0-alpha.14", "1.0.0")
    .replace("1.0.0-alpha.15", "1.0.1")
    .replace("guidance/alpha-14-to-alpha-15.json", "guidance/1.0.0-to-1.0.1.json"),
)
rewrite(
    "internal/release/tests/test_synthetic_qualification_vault.py",
    lambda text: text.replace("1.0.0-alpha.11", "1.0.0"),
)
