from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_automation as automation
from internal.release import qualification_runner


REVISION_A = "0123456789abcdef0123456789abcdef01234567"
REVISION_B = "89abcdef0123456789abcdef0123456789abcdef"


class QualificationAutomationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    @staticmethod
    def digest(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def make_assets(
        self,
        directory: Path,
        *,
        version: str,
        revision: str,
        semantic_review_required: bool = True,
        edge_from: str | None = None,
    ) -> qualification_runner.ReleaseIdentity:
        directory.mkdir(parents=True, exist_ok=True)
        edges = []
        if edge_from:
            edges.append(
                {
                    "from": edge_from,
                    "to": version,
                    "mode": "direct",
                    "intermediates": [],
                    "carry_unresolved_semantic_state": False,
                    "migration_ids": [],
                    "guidance_paths": ["guidance/edge.json"],
                    "semantic_review_required": semantic_review_required,
                }
            )
        manifest = {
            "ava_version": version,
            "tag": f"v{version}",
            "source_revision": revision,
            "semantic_review_required": semantic_review_required,
            "assets": [{"name": name} for name in qualification_runner.RELEASE_ASSETS],
            "upgrade_paths": {"edges": edges},
        }
        for name in qualification_runner.RELEASE_ASSETS:
            if name in {"ava-release.json", "SHA256SUMS"}:
                continue
            (directory / name).write_text(f"{name}:{version}\n", encoding="utf-8")
        (directory / "ava-release.json").write_text(
            json.dumps(manifest, sort_keys=True) + "\n", encoding="utf-8"
        )
        checksums = []
        for name in qualification_runner.RELEASE_ASSETS:
            if name == "SHA256SUMS":
                continue
            checksums.append(f"{self.digest(directory / name)}  {name}")
        (directory / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")
        return qualification_runner.validate_asset_dir(directory, directory.name)

    def resolved(
        self,
        directory: Path,
        *,
        version: str,
        revision: str,
        kind: str = "local",
        edge_from: str | None = None,
    ) -> automation.ResolvedRelease:
        identity = self.make_assets(
            directory,
            version=version,
            revision=revision,
            edge_from=edge_from,
        )
        return automation.ResolvedRelease(
            kind=kind,
            identity=identity,
            release_manifest_sha256=automation.sha256_file(directory / "ava-release.json"),
            asset_sha256=automation.release_asset_digests(directory),
            attested=kind == "published",
        )

    def test_checked_in_configuration_has_separate_historical_and_active_pairs(self) -> None:
        config, catalog, current = automation.load_configuration()
        automation.validate_model_identifier(config["qualification_model"], field="qualification_model")
        automation.validate_model_identifier(config["audit_model"], field="audit_model")
        self.assertEqual(config["active_pair"], "alpha14-to-alpha15-corrective-local")
        pairs = {item["id"]: item for item in catalog["pairs"]}
        historical = pairs["alpha13-to-alpha14"]
        self.assertTrue(historical["historical"])
        self.assertEqual(historical["source"]["tag"], "v1.0.0-alpha.13")
        self.assertEqual(historical["target"]["tag"], "v1.0.0-alpha.14")
        active = pairs[config["active_pair"]]
        self.assertFalse(active["historical"])
        self.assertEqual(active["source"]["tag"], "v1.0.0-alpha.14")
        self.assertEqual(
            active["target"],
            {"kind": "local", "tag": "v1.0.0-alpha.15", "version": "1.0.0-alpha.15"},
        )
        self.assertEqual(current["pairs"]["alpha13-to-alpha14"]["status"], "not-run")

    def test_model_identifiers_require_an_explicit_author_for_any_provider_or_tool(self) -> None:
        for value in (
            "openai/gpt-5.6-sol",
            "opencode/big-pickle",
            "anthropic/claude-4",
            "opencode/deepseek-v4-flash-free",
        ):
            automation.validate_model_identifier(value, field="qualification_model")
        for value in ("big-pickle", "/big-pickle", "opencode/", "", "opencode"):
            with self.assertRaises(automation.AutomationError):
                automation.validate_model_identifier(value, field="qualification_model")

    def test_pinned_image_manifest_validates_exact_five_committed_pngs(self) -> None:
        manifest = automation.validate_pinned_images()
        self.assertEqual(len(manifest["images"]), 5)
        self.assertEqual(len({item["destination"] for item in manifest["images"]}), 5)

    def test_mutable_release_aliases_are_refused(self) -> None:
        for value in ("latest", "v1.0.0/latest", "LATEST"):
            with self.assertRaises(automation.AutomationError):
                automation.reject_mutable_tag(value)

    def test_local_assets_are_bound_to_exact_manifest_identity(self) -> None:
        assets = self.root / "assets"
        self.make_assets(assets, version="1.0.0-alpha.15", revision=REVISION_B)
        selection = {"kind": "local", "version": "1.0.0-alpha.15", "tag": "v1.0.0-alpha.15"}
        resolved = automation.resolve_local_release(selection, assets, label="target")
        self.assertEqual(resolved.identity.revision, REVISION_B)
        self.assertFalse(resolved.attested)
        (assets / "ava-base.tar.gz").write_text("tampered\n", encoding="utf-8")
        with self.assertRaisesRegex(qualification_runner.QualificationError, "checksum mismatch"):
            automation.resolve_local_release(selection, assets, label="target")

    def test_published_assets_require_immutable_release_and_attestation(self) -> None:
        destination = self.root / "published"
        selection = {"kind": "published", "version": "1.0.0-alpha.14", "tag": "v1.0.0-alpha.14"}

        def fake(args, **kwargs):
            if args[1:3] == ["release", "view"]:
                return automation.CommandResult(
                    0,
                    json.dumps({"tagName": selection["tag"], "isDraft": False, "isImmutable": True}),
                    "",
                )
            if args[1:3] == ["release", "download"]:
                self.make_assets(destination, version="1.0.0-alpha.14", revision=REVISION_A)
                return automation.CommandResult(0, "", "")
            if args[1:3] == ["release", "verify"]:
                return automation.CommandResult(1, "", "missing attestation")
            raise AssertionError(args)

        with self.assertRaisesRegex(automation.AutomationError, "attestation verification failed"):
            automation.acquire_published_release(
                selection,
                destination,
                repository="phdah/ava",
                gh="gh",
                command_runner=fake,
            )

    def test_fixture_generation_composes_only_the_maintained_wrapper(self) -> None:
        fixture_parent = self.root / "fixture-parent"
        calls = []

        def fake(args, *, cwd=None, env=None, check=True):
            calls.append((args, cwd, env, check))
            generated = fixture_parent / "ava-synthetic-qualification-vault.test"
            generated.mkdir(parents=True)
            return automation.CommandResult(0, f"synthetic qualification vault ready: {generated}\n", "")

        result = automation.generate_fixture(
            automation.REPOSITORY_ROOT,
            fixture_parent,
            command_runner=fake,
        )
        self.assertTrue(result.is_dir())
        self.assertEqual(len(calls), 1)
        self.assertTrue(str(calls[0][0][-1]).endswith("generate-synthetic-qualification-vault.sh"))
        self.assertEqual(calls[0][2]["TMPDIR"], str(fixture_parent))

    def test_execution_identity_namespaces_retained_runner_state(self) -> None:
        source = self.resolved(self.root / "source", version="1.0.0-alpha.14", revision=REVISION_A)
        target = self.resolved(
            self.root / "target",
            version="1.0.0-alpha.15",
            revision=REVISION_B,
            edge_from="1.0.0-alpha.14",
        )
        kwargs = dict(
            source=source,
            target=target,
            image_manifest_sha256="1" * 64,
            pinned_images=[{"file": "a.png", "sha256": "7" * 64, "destination": "corpus/a.png"}],
            fixture_generator_sha256="8" * 64,
            fixture_inventory_sha256="2" * 64,
            matrix_sha256="3" * 64,
            repository_revision_value="4" * 40,
            runner_sha256="5" * 64,
            automation_sha256="6" * 64,
            opencode_version_value="1.2.3",
            qualification_model="openai/gpt-5.6-sol",
            audit_model="openai/gpt-5.6-sol",
        )
        first, _ = automation.execution_identity(**kwargs)
        second, _ = automation.execution_identity(**{**kwargs, "audit_model": "openai/other"})
        self.assertNotEqual(first, second)
        parent = self.root / "execution"
        self.assertNotEqual(
            automation.execution_root_for_identity(parent, first),
            automation.execution_root_for_identity(parent, second),
        )

    def test_session_inventory_includes_nested_sessions_and_binds_them_to_scenario(self) -> None:
        execution = self.root / "execution"
        scenario = execution / "scenarios/calendar-check"
        project = scenario / "project"
        project.mkdir(parents=True)
        prompt = "Persist tomorrow's date after verifying it."
        (scenario / "runner-commands.jsonl").write_text(
            json.dumps(
                {
                    "label": "OpenCode prompt",
                    "command": ["opencode", "run", prompt],
                    "returncode": 0,
                    "stdout": '{"sessionID":"ses_root123"}',
                    "stderr": "",
                }
            )
            + "\n",
            encoding="utf-8",
        )
        after = [
            {"id": "ses_root123", "directory": str(project)},
            {"id": "ses_child456", "parentID": "ses_root123", "directory": str(project)},
        ]
        exports = {
            "ses_root123": {"messages": [{"role": "user", "parts": [{"text": prompt}]}]},
            "ses_child456": {
                "messages": [
                    {"role": "user", "parts": [{"text": "Inspect the calendar instruction."}]}
                ],
                "providerID": "openai",
                "modelID": "gpt-5.6-sol",
            },
        }

        def fake(args, **kwargs):
            self.assertEqual(args[:2], ["opencode", "export"])
            return automation.CommandResult(0, json.dumps(exports[args[2]]), "")

        inventory = automation.build_session_inventory(
            before=[],
            after=after,
            execution_root=execution,
            opencode="opencode",
            configured_model="openai/gpt-5.6-sol",
            command_runner=fake,
        )
        self.assertEqual({item["session_id"] for item in inventory["sessions"]}, set(exports))
        child = next(item for item in inventory["sessions"] if item["session_id"] == "ses_child456")
        self.assertEqual(child["parent_session_id"], "ses_root123")
        self.assertEqual(child["scenario"], "calendar-check")

    def test_audit_schema_and_severity_gate_are_deterministic(self) -> None:
        schema = automation.load_json(automation.SCHEMA_ROOT / "audit-output.schema.json")
        clean = {
            "schema_version": 1,
            "findings": [],
            "limitations": [],
            "terminal_conclusion": "pass",
        }
        automation.validate_schema(clean, schema, label="audit")
        self.assertEqual(automation.audit_status(clean), ("awaiting-user-signoff", 0))
        blocking = {
            "schema_version": 1,
            "findings": [
                {
                    "id": "A1",
                    "severity": "major",
                    "summary": "Runner claim lacks evidence",
                    "evidence": ["session ses_root123"],
                    "consequence": "Qualification cannot support acceptance.",
                    "correction": "Tighten the runner assertion.",
                    "remediation_owner": "runner",
                    "limitations": "None",
                }
            ],
            "limitations": [],
            "terminal_conclusion": "needs-review",
        }
        automation.validate_schema(blocking, schema, label="audit")
        self.assertEqual(automation.audit_status(blocking), ("needs-review", 1))

    def test_compact_evidence_writes_only_internal_state_and_never_signs_off(self) -> None:
        repo = self.root / "repo"
        state = repo / "internal/release/qualification"
        shutil.copytree(automation.STATE_ROOT, state)
        qualification_root = self.root / "qualification"
        qualification_root.mkdir()
        (qualification_root / "fixture.txt").write_text("fixture\n", encoding="utf-8")
        raw = self.root / "raw"
        raw.mkdir()
        (raw / "log.txt").write_text("raw\n", encoding="utf-8")
        source = self.resolved(
            self.root / "source-evidence",
            version="1.0.0-alpha.14",
            revision=REVISION_A,
        )
        target = self.resolved(
            self.root / "target-evidence",
            version="1.0.0-alpha.15",
            revision=REVISION_B,
            edge_from="1.0.0-alpha.14",
        )
        audit = {
            "schema_version": 1,
            "findings": [],
            "limitations": [],
            "terminal_conclusion": "pass",
        }
        automation.write_compact_evidence(
            repository_root=repo,
            run_id="run-test",
            pair_id="alpha14-to-alpha15-corrective-local",
            execution_identity_sha256="a" * 64,
            execution_identity_payload={"schema_version": 1},
            source=source,
            target=target,
            opencode_version_value="1.2.3",
            qualification_model="openai/gpt-5.6-sol",
            audit_model="openai/gpt-5.6-sol",
            qualification_root=qualification_root,
            execution_root=self.root / "unused-execution",
            raw_evidence_root=raw,
            session_inventory={"schema_version": 1, "sessions": []},
            audit=audit,
            runner_summary={"outcomes": [{"outcome": "pass"}]},
            automated_state="awaiting-user-signoff",
            mechanical_error=None,
        )
        record = json.loads((state / "runs/run-test.json").read_text(encoding="utf-8"))
        current = json.loads((state / "current-state.json").read_text(encoding="utf-8"))
        self.assertIsNone(record["user_signoff"])
        self.assertEqual(
            current["pairs"]["alpha14-to-alpha15-corrective-local"]["status"],
            "awaiting-user-signoff",
        )
        self.assertIsNone(
            current["pairs"]["alpha14-to-alpha15-corrective-local"]["user_signoff"]
        )
        self.assertFalse((repo / "internal/todo/05-release-qualification/dogfood").exists())

    def test_automation_is_internal_and_not_run_by_repository_test_gate(self) -> None:
        module = Path(automation.__file__).resolve()
        self.assertTrue(module.is_relative_to(automation.REPOSITORY_ROOT / "internal"))
        source = module.read_text(encoding="utf-8")
        self.assertNotIn("git commit", source)
        test_script = (automation.REPOSITORY_ROOT / "internal/release/test.sh").read_text(
            encoding="utf-8"
        )
        matching = [line.strip() for line in test_script.splitlines() if "qualify-release.sh" in line]
        self.assertEqual(len(matching), 1)
        self.assertTrue(matching[0].startswith("sh -n "))


if __name__ == "__main__":
    unittest.main()
