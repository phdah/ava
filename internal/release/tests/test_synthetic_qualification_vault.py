from __future__ import annotations

import hashlib
import json
import runpy
import struct
import subprocess
import tarfile
import tempfile
import unittest
import zipfile
import zlib
from collections import Counter
from datetime import date
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parents[3]
FIXTURE_ROOT = SOURCE_ROOT / "internal/release/fixtures/synthetic-qualification-vault"
GENERATOR = FIXTURE_ROOT / "fixture.py"
BLUEPRINT = FIXTURE_ROOT / "blueprint.json"
ORACLE_SCHEMA = FIXTURE_ROOT / "oracle.schema.json"
RUN_SCHEMA = FIXTURE_ROOT / "run-manifest.schema.json"
ASSEMBLER = SOURCE_ROOT / "internal/release/assemble.py"
REVISION = "0123456789abcdef0123456789abcdef01234567"


def png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)


PNG = (
    b"\x89PNG\r\n\x1a\n"
    + png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0))
    + png_chunk(b"IDAT", zlib.compress(b"\x00\xff\xff\xff\xff", level=9))
    + png_chunk(b"IEND", b"")
)
class SyntheticQualificationVaultTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def run_fixture(self, command: str, output: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(GENERATOR), command, str(output)],
            cwd=SOURCE_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if check and result.returncode != 0:
            self.fail(f"fixture command failed: {command}\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")
        return result

    @staticmethod
    def inventory(root: Path) -> dict[str, str]:
        return {
            path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(item for item in root.rglob("*") if item.is_file())
        }

    def add_images(self, output: Path) -> None:
        blueprint = json.loads(BLUEPRINT.read_text())
        for slot in blueprint["image_slots"]:
            payload = PNG if slot["format"] == "png" else JPEG
            path = output / slot["path"]
            path.write_bytes(payload)

    def test_blueprint_fixes_narrative_counts_formats_and_image_slots(self) -> None:
        blueprint = json.loads(BLUEPRINT.read_text())
        oracle_schema = json.loads(ORACLE_SCHEMA.read_text())
        run_schema = json.loads(RUN_SCHEMA.read_text())
        self.assertEqual(blueprint["seed"], 20250101)
        self.assertEqual(blueprint["interval"], {"start": "2025-01-01", "end": "2025-06-30"})
        self.assertEqual(blueprint["identity"]["full_name"], "Adam Lind")
        self.assertEqual(blueprint["dog"]["name"], "Uno")
        self.assertEqual(blueprint["move"]["completed"], "2025-02-22")
        self.assertEqual(blueprint["renovation"]["completed"], "2025-03-28")
        self.assertEqual(sum(blueprint["counts"]["classes"].values()), 300)
        self.assertEqual(sum(blueprint["counts"]["formats"].values()), 300)
        self.assertEqual(blueprint["counts"]["formats"]["md"], 254)
        self.assertEqual(len(blueprint["image_slots"]), 5)
        self.assertEqual({slot["format"] for slot in blueprint["image_slots"]}, {"png"})
        self.assertTrue(any("receipt" in slot["path"] for slot in blueprint["image_slots"]))
        self.assertEqual(len(blueprint["variant_families"]), 8)
        self.assertIn("source_excerpt", oracle_schema["$defs"]["file"]["properties"]["claims"]["items"]["required"])
        self.assertIn("destinations", oracle_schema["$defs"]["file"]["properties"]["sections"]["items"]["required"])
        self.assertIn("prompt_sha256", oracle_schema["$defs"]["image"]["required"])
        self.assertEqual(len(run_schema["allOf"]), 2)
        completed_run = run_schema["allOf"][0]["then"]["properties"]
        self.assertEqual(completed_run["release"]["properties"]["asset_sha256"]["minProperties"], 7)
        self.assertEqual(completed_run["routing"]["properties"]["loaded_paths"]["minItems"], 1)
        self.assertEqual(set(run_schema["$defs"]["completedAssetUrls"]["required"]), {"ava-install.sh", "ava-base.tar.gz", "ava-guidance.tar.gz", "ava-migrations.tar.gz", "ava-release.json", "ava-release-notes.md", "SHA256SUMS"})

    def test_corpus_batch_boundaries_are_exact(self) -> None:
        corpus_batch = runpy.run_path(str(GENERATOR))["corpus_batch"]
        cases = {
            date(2025, 2, 14): "01-pre-move",
            date(2025, 2, 15): "02-move-transition",
            date(2025, 3, 2): "02-move-transition",
            date(2025, 3, 3): "03-renovation",
            date(2025, 3, 31): "03-renovation",
            date(2025, 4, 1): "04-settled",
        }
        for source_date, expected in cases.items():
            self.assertEqual(corpus_batch(source_date), expected)

    def test_two_clean_generations_are_byte_identical_and_verify(self) -> None:
        blueprint = json.loads(BLUEPRINT.read_text())
        first = self.root / "first"
        second = self.root / "second"
        self.run_fixture("generate", first)
        self.run_fixture("generate", second)
        self.assertEqual(self.inventory(first), self.inventory(second))

        oracle = json.loads((first / "oracle/baseline.json").read_text())
        self.assertEqual(len(oracle["files"]), 300)
        self.assertEqual(len(oracle["image_slots"]), 5)
        self.assertEqual({record["domain"] for record in oracle["files"]}, {"private", "work", "overlapping", "ambiguous"})
        self.assertTrue(all(record["sections"] for record in oracle["files"]))
        self.assertTrue(any(claim["certainty"] == "uncertain" for record in oracle["files"] for claim in record["claims"]))
        self.assertTrue(any(claim["attribution"] != "Adam Lind" for record in oracle["files"] for claim in record["claims"]))
        pending_sections = [section for record in oracle["files"] for section in record["sections"] if section["disposition"] == "pending"]
        self.assertTrue(pending_sections)
        self.assertTrue(all(section["blocker"] and not section["destinations"] for section in pending_sections))
        self.assertTrue(all(section["destinations"] for record in oracle["files"] for section in record["sections"] if section["disposition"] == "mapped"))
        self.assertTrue(all(claim["source_excerpt"] for record in oracle["files"] for claim in record["claims"]))
        self.assertTrue(any(record["duplicates"] for record in oracle["files"]))
        finance_sections = [section for record in oracle["files"] if record["class"] == "household-finance" for section in record["sections"]]
        mapped_finance = [section for section in finance_sections if section["disposition"] == "mapped"]
        self.assertTrue(all(section["destinations"] == ["knowledge/private/household-finance.md"] for section in mapped_finance))
        reading_state_claims = [claim for record in oracle["files"] if record["class"] == "reading" for claim in record["claims"] if claim["text"].startswith("Reading state for")]
        self.assertTrue(all(claim["source_excerpt"].startswith("Progress:") for claim in reading_state_claims))
        self.assertEqual(Counter(record["month"] for record in oracle["files"] if record["class"] == "diary"), {f"2025-{month:02d}": 25 for month in range(1, 7)})

        corpus = first / "corpus"
        batch_names = {"01-pre-move", "02-move-transition", "03-renovation", "04-settled"}
        self.assertEqual({path.name for path in corpus.iterdir()}, batch_names)
        for record in [*oracle["files"], *oracle["image_slots"]]:
            if record["date"] < "2025-02-15":
                expected_batch = "01-pre-move"
            elif record["date"] < "2025-03-03":
                expected_batch = "02-move-transition"
            elif record["date"] < "2025-04-01":
                expected_batch = "03-renovation"
            else:
                expected_batch = "04-settled"
            self.assertEqual(Path(record["path"]).parts[1], expected_batch)

        markdown = list(corpus.rglob("*.md"))
        self.assertEqual(len(markdown), 254)
        self.assertTrue(all(path.read_text().startswith("#") for path in markdown))
        self.assertTrue(all(not path.read_text().startswith("---") for path in markdown))
        self.assertEqual(len(list((first / "image-prompts").glob("*.md"))), 5)
        for prompt in (first / "image-prompts").glob("*.md"):
            text = prompt.read_text()
            for heading in ("## Visible Scene", "## Required Canonical Facts", "## Must Not Appear", "## Expected Durable Outcomes", "## Expected Non-Durable Outcomes"):
                self.assertIn(heading, text)
        self.assertFalse(any((first / slot["path"]).exists() for slot in oracle["image_slots"]))
        reading_text = "\n".join(path.read_text() for path in corpus.rglob("*-reading-*.md"))
        self.assertIn("## Copied quotation", reading_text)
        for book in blueprint["reading"]["books"]:
            completion_source = next(path for path in corpus.rglob(f"{book['completed']}-reading-*.md"))
            self.assertIn(f"# Reading notes - {book['title']}", completion_source.read_text())
            self.assertIn(f"Progress: Completed on {book['completed']}", completion_source.read_text())
            for diary in corpus.rglob("*-diary-*.md"):
                if diary.name[:10] > book["completed"]:
                    self.assertNotIn(f"continued {book['title']}", diary.read_text())
        todo_text = "\n".join(path.read_text() for path in corpus.rglob("*-todo-*.md"))
        self.assertIn("P-MOVE-02", todo_text)
        self.assertIn("W-INC-02", todo_text)
        race = next(path for path in corpus.rglob("2025-05-17-running-*.md"))
        self.assertIn(blueprint["running"]["race_finish_time"], race.read_text())
        march_two_renovation = next(path for path in corpus.rglob("2025-03-02-kitchen-renovation-*.md"))
        self.assertIn("Approved materials:", march_two_renovation.read_text())
        self.assertNotIn("Materials under review:", march_two_renovation.read_text())
        march_completion_diary = next(path for path in corpus.rglob(f"{blueprint['renovation']['completed']}-diary-*.md"))
        self.assertIn("renovated kitchen complete", march_completion_diary.read_text())
        commute = next(item for item in blueprint["transitions"] if item["id"] == "commute-change")
        diary_text = "\n".join(path.read_text() for path in corpus.rglob("*-diary-*.md"))
        self.assertIn(f"Current commute: {commute['from']}", diary_text)
        self.assertIn(f"Current commute: {commute['to']}", diary_text)
        uncertain_claims = [claim for record in oracle["files"] for claim in record["claims"] if claim["certainty"] == "uncertain"]
        self.assertTrue(any("seemed" in claim["source_excerpt"] for claim in uncertain_claims))
        attributed_proposals = [claim for record in oracle["files"] for claim in record["claims"] if claim["decision_status"] == "proposal" and claim["attribution"] != blueprint["identity"]["full_name"]]
        self.assertTrue(all(claim["attribution"].split()[0] in claim["source_excerpt"] or "supplier" in claim["source_excerpt"].lower() for claim in attributed_proposals))

        for record in oracle["files"]:
            path = first / record["path"]
            if record["format"] == "docx":
                with zipfile.ZipFile(path) as archive:
                    self.assertGreater(len(archive.read("word/document.xml")), 500)
            elif record["format"] == "pptx":
                with zipfile.ZipFile(path) as archive:
                    self.assertGreater(len(archive.read("ppt/slides/slide1.xml")), 500)
            elif record["format"] == "pdf":
                self.assertIn(b"Ava synthetic fixture", path.read_bytes())
            elif record["format"] == "ics":
                lines = path.read_bytes().split(b"\r\n")
                self.assertTrue(all(len(line) <= 75 for line in lines))
                self.assertIn(b"\\;", path.read_bytes())

    def test_output_boundary_rejects_repository_and_resolved_symlink(self) -> None:
        inside = SOURCE_ROOT / "synthetic-vault-must-not-exist"
        result = self.run_fixture("generate", inside, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the Ava repository", result.stderr)
        self.assertFalse(inside.exists())

        link = self.root / "repository-link"
        link.symlink_to(SOURCE_ROOT, target_is_directory=True)
        result = self.run_fixture("generate", link / "nested", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the Ava repository", result.stderr)

    def test_image_finalization_and_all_variants_preserve_baseline(self) -> None:
        output = self.root / "finalized"
        self.run_fixture("generate", output)
        pending = self.run_fixture("finalize-images", output, check=False)
        self.assertNotEqual(pending.returncode, 0)
        self.assertIn("all five externally generated image files", pending.stderr)

        self.add_images(output)
        ready = self.run_fixture("verify", output)
        self.assertEqual(json.loads(ready.stdout)["image_state"], "ready")
        self.run_fixture("finalize-images", output)
        verified = self.run_fixture("verify", output)
        self.assertEqual(json.loads(verified.stdout)["image_state"], "finalized")
        finalized = json.loads((output / "oracle/finalized-inventory.json").read_text())
        self.assertEqual(finalized["deterministic_count"], 300)
        self.assertEqual(finalized["finalized_count"], 305)
        self.assertEqual(len(finalized["external_images"]), 5)
        baseline_before = self.inventory(output / "corpus")

        self.run_fixture("materialize-variants", output)
        baseline_after = self.inventory(output / "corpus")
        self.assertEqual(baseline_before, baseline_after)
        variants = json.loads((output / "variants/index.json").read_text())
        self.assertEqual(len(variants["families"]), 8)
        self.assertTrue(all(item["materialization"] == "workspace-and-execution-plan" for item in variants["families"]))
        pending_inbox = output / "variants/04-complete-pending-inbox/project/inbox"
        self.assertEqual(len([path for path in pending_inbox.iterdir() if path.is_file()]), 305)
        self.assertFalse(any(path.name in {"baseline.json", "finalized-inventory.json"} for path in pending_inbox.iterdir()))
        private_role = output / "variants/03-registered-private-work-roles/project/roles/private-life-steward"
        self.assertIn("# Activation", (private_role / "role.md").read_text())
        self.assertIn("Document metadata", (private_role / "index.md").read_text())
        self.assertIn("Knowledge organization", (private_role / "index.md").read_text())

    def test_oracle_and_prompt_tampering_are_rejected(self) -> None:
        output = self.root / "tampered"
        self.run_fixture("generate", output)
        baseline_path = output / "oracle/baseline.json"
        baseline_bytes = baseline_path.read_bytes()
        oracle = json.loads(baseline_bytes)
        oracle["schema_version"] = 2
        baseline_path.write_text(json.dumps(oracle))
        result = self.run_fixture("verify", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("oracle identity", result.stderr)

        baseline_path.write_bytes(baseline_bytes)
        oracle = json.loads(baseline_bytes)
        prompt_path = output / oracle["image_slots"][0]["prompt_path"]
        prompt_path.write_text(prompt_path.read_text() + "tampered\n")
        result = self.run_fixture("verify", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("image prompt digest mismatch", result.stderr)

    def test_finalized_inventory_symlink_is_rejected(self) -> None:
        output = self.root / "symlinked-finalized-inventory"
        outside = self.root / "outside-finalized-inventory.json"
        self.run_fixture("generate", output)
        self.add_images(output)
        (output / "oracle/finalized-inventory.json").symlink_to(outside)
        result = self.run_fixture("finalize-images", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must not be a symlink", result.stderr)
        self.assertFalse(outside.exists())

    def test_wrong_or_partial_image_set_is_rejected(self) -> None:
        output = self.root / "bad-images"
        self.run_fixture("generate", output)
        blueprint = json.loads(BLUEPRINT.read_text())
        self.add_images(output)
        first = output / blueprint["image_slots"][0]["path"]
        corrupt_png = b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) + png_chunk(b"IDAT", b"not-zlib-data") + png_chunk(b"IEND", b"")
        first.write_bytes(corrupt_png)
        result = self.run_fixture("verify", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("does not decompress", result.stderr)

        invalid_header_png = b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 1, 6, 0, 0, 0)) + png_chunk(b"IDAT", zlib.compress(b"\x00\x00")) + png_chunk(b"IEND", b"")
        first.write_bytes(invalid_header_png)
        result = self.run_fixture("verify", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid PNG image header", result.stderr)

        late_palette_png = b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) + png_chunk(b"IDAT", zlib.compress(b"\x00\xff\xff\xff\xff")) + png_chunk(b"PLTE", b"\x00\x00\x00") + png_chunk(b"IEND", b"")
        first.write_bytes(late_palette_png)
        result = self.run_fixture("verify", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid PNG image header", result.stderr)

        nonempty_iend_png = b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", struct.pack(">IIBBBBB", 1, 1, 8, 6, 0, 0, 0)) + png_chunk(b"IDAT", zlib.compress(b"\x00\xff\xff\xff\xff")) + png_chunk(b"IEND", b"x")
        first.write_bytes(nonempty_iend_png)
        result = self.run_fixture("verify", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("IEND chunk must be empty", result.stderr)

        first.write_bytes(PNG)
        second_png = output / next(slot["path"] for slot in blueprint["image_slots"] if output / slot["path"] != first)
        first.unlink()
        first.symlink_to(second_png)
        result = self.run_fixture("verify", output, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("regular non-symlink", result.stderr)

    def test_completed_run_manifest_rejects_unbound_release_identity(self) -> None:
        output = self.root / "run-manifest"
        self.run_fixture("generate", output)
        manifest = json.loads((output / "oracle/run-manifest.template.json").read_text())
        manifest["decision"].update({"result": "pass", "actual": "claimed pass", "reviewer": "reviewer"})
        manifest["release"].update({"ava_version": "banana", "tag": "not-a-tag", "source_revision": "a" * 40})
        names = {"ava-install.sh", "ava-base.tar.gz", "ava-guidance.tar.gz", "ava-migrations.tar.gz", "ava-release.json", "ava-release-notes.md", "SHA256SUMS"}
        manifest["release"]["asset_urls"] = {name: f"file:///tmp/{name}" for name in names}
        manifest["release"]["asset_sha256"] = {name: "b" * 64 for name in names}
        manifest_path = output / "oracle/invalid-pass.json"
        manifest_path.write_text(json.dumps(manifest))
        result = subprocess.run(["python3", str(GENERATOR), "verify-run-manifest", str(manifest_path)], cwd=SOURCE_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Ava version is invalid", result.stderr)

        pending = json.loads((output / "oracle/run-manifest.template.json").read_text())
        pending["scenario"]["variant"] = "not-a-variant"
        pending_path = output / "oracle/invalid-pending.json"
        pending_path.write_text(json.dumps(pending))
        result = subprocess.run(["python3", str(GENERATOR), "verify-run-manifest", str(pending_path)], cwd=SOURCE_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("scenario identity", result.stderr)

        pending = json.loads((output / "oracle/run-manifest.template.json").read_text())
        pending["release"]["asset_urls"] = {name: "arbitrary" for name in names}
        pending["release"]["asset_sha256"] = {name: "c" * 64 for name in names}
        pending_path.write_text(json.dumps(pending))
        result = subprocess.run(["python3", str(GENERATOR), "verify-run-manifest", str(pending_path)], cwd=SOURCE_ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("asset URL is not pinned", result.stderr)

    def test_registered_role_workspace_installs_and_is_conformant(self) -> None:
        output = self.root / "installed-variant"
        self.run_fixture("generate", output)
        self.add_images(output)
        self.run_fixture("finalize-images", output)
        self.run_fixture("materialize-variants", output)

        assets = self.root / "assets"
        assembly = subprocess.run(
            ["python3", str(ASSEMBLER), "--root", str(SOURCE_ROOT), "--output", str(assets), "--version", "1.0.0-alpha.11", "--source-revision", REVISION, "--source-date-epoch", "1700000000"],
            cwd=SOURCE_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(assembly.returncode, 0, assembly.stderr)
        project = output / "variants/03-registered-private-work-roles/project"
        installation = subprocess.run(
            ["sh", str(assets / "ava-install.sh"), "--target", str(project), "--asset-dir", str(assets)],
            cwd=SOURCE_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(installation.returncode, 0, installation.stderr)
        conformance = subprocess.run(
            ["python3", "-m", "internal.release.conformance", "--root", str(project), "--mode", "installed", "--format", "json"],
            cwd=SOURCE_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertEqual(conformance.returncode, 0, f"{conformance.stdout}\n{conformance.stderr}")

    def test_release_assembly_excludes_fixture_and_generated_markers(self) -> None:
        output = self.root / "release"
        result = subprocess.run(
            [
                "python3",
                str(ASSEMBLER),
                "--root",
                str(SOURCE_ROOT),
                "--output",
                str(output),
                "--version",
                "1.0.0-alpha.11",
                "--source-revision",
                REVISION,
                "--source-date-epoch",
                "1700000000",
            ],
            cwd=SOURCE_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if result.returncode != 0:
            self.fail(f"assembly failed\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}")

        forbidden_names = ("synthetic-qualification-vault", "blueprint.json", "oracle.schema.json", "requirements.lock")
        marker = b"synthetic-v1-qualification-vault"
        for path in output.iterdir():
            if not path.is_file():
                continue
            self.assertFalse(any(name in path.name for name in forbidden_names), path.name)
            if path.name.endswith(".tar.gz"):
                with tarfile.open(path, "r:gz") as archive:
                    for member in archive.getmembers():
                        self.assertFalse(any(name in member.name for name in forbidden_names), member.name)
                        if member.isfile():
                            extracted = archive.extractfile(member)
                            self.assertIsNotNone(extracted)
                            self.assertNotIn(marker, extracted.read(), f"{path.name}:{member.name}")
            else:
                self.assertNotIn(marker, path.read_bytes(), path.name)


if __name__ == "__main__":
    unittest.main()
