#!/usr/bin/env python3
"""Run the repository-external synthetic Ava qualification matrix."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_ROOT = REPOSITORY_ROOT / "internal/release/fixtures/synthetic-qualification-vault"
FIXTURE = FIXTURE_ROOT / "fixture.py"
CHECKPOINT = FIXTURE_ROOT / "checkpoint.py"
MATRIX_PATH = FIXTURE_ROOT / "qualification-matrix.json"
RELEASE_ASSETS = (
    "ava-install.sh",
    "ava-base.tar.gz",
    "ava-guidance.tar.gz",
    "ava-migrations.tar.gz",
    "ava-release.json",
    "ava-release-notes.md",
    "SHA256SUMS",
)
SENTINEL = ".ava-qualification-runner.json"
STATE_FILE = "runner-state.json"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
OUTCOMES = {"pass", "fail", "skipped", "user-decision-required"}


class QualificationError(RuntimeError):
    pass


@dataclass(frozen=True)
class ReleaseIdentity:
    directory: Path
    version: str
    tag: str
    revision: str
    semantic_review_required: bool
    manifest: dict[str, Any]


@dataclass
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def resolve_path(value: Path | str) -> Path:
    return Path(value).expanduser().resolve()


def is_within(path: Path, root: Path) -> bool:
    return path == root or path.is_relative_to(root)


def require_external(path: Path, repository_root: Path, label: str) -> None:
    if is_within(path, repository_root):
        raise QualificationError(f"{label} must be outside the Ava repository: {path}")


def require_disjoint(path: Path, other: Path, label: str, other_label: str) -> None:
    if is_within(path, other) or is_within(other, path):
        raise QualificationError(f"{label} must be disjoint from {other_label}: {path} versus {other}")


def tree_inventory(root: Path, *, exclude: Iterable[Path] = ()) -> list[dict[str, Any]]:
    excluded = tuple(item.resolve() for item in exclude)
    records: list[dict[str, Any]] = []
    if not root.exists():
        return records
    for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix().encode()):
        resolved = path.resolve()
        if any(is_within(resolved, base) for base in excluded):
            continue
        records.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    return records


def inventory_digest(root: Path, *, exclude: Iterable[Path] = ()) -> str:
    return hashlib.sha256(canonical_json(tree_inventory(root, exclude=exclude)).encode()).hexdigest()


def project_owned_inventory(project: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    if not project.exists():
        return records
    for path in sorted((item for item in project.rglob("*") if item.is_file()), key=lambda item: item.relative_to(project).as_posix().encode()):
        relative = path.relative_to(project)
        if relative.as_posix() == "AGENTS.md" or relative.parts[:1] == (".ava",):
            continue
        records.append(
            {
                "path": relative.as_posix(),
                "sha256": sha256_file(path),
                "bytes": path.stat().st_size,
            }
        )
    return records


def project_owned_digest(project: Path) -> str:
    return hashlib.sha256(canonical_json(project_owned_inventory(project)).encode()).hexdigest()


def parse_checksums(path: Path) -> dict[str, str]:
    checksums: dict[str, str] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9._-]+)", line)
        if not match:
            raise QualificationError(f"invalid SHA256SUMS line {line_number}: {path}")
        digest, name = match.groups()
        if name in checksums:
            raise QualificationError(f"duplicate checksum entry for {name}: {path}")
        checksums[name] = digest
    expected = set(RELEASE_ASSETS) - {"SHA256SUMS"}
    if set(checksums) != expected:
        raise QualificationError(f"checksum inventory mismatch in {path}: expected {sorted(expected)}")
    return checksums


def reject_mutable_asset_selection(path: Path, label: str) -> None:
    if any(part.lower() == "latest" for part in path.parts):
        raise QualificationError(f"{label} must be an exact pinned asset directory, not a latest selection: {path}")


def validate_asset_dir(path: Path, label: str) -> ReleaseIdentity:
    reject_mutable_asset_selection(path, label)
    if not path.is_dir() or path.is_symlink():
        raise QualificationError(f"{label} is not a normal directory: {path}")
    missing = [name for name in RELEASE_ASSETS if not (path / name).is_file() or (path / name).is_symlink()]
    if missing:
        raise QualificationError(f"{label} is missing exact release assets: {', '.join(missing)}")
    checksums = parse_checksums(path / "SHA256SUMS")
    for name, expected in checksums.items():
        actual = sha256_file(path / name)
        if actual != expected:
            raise QualificationError(f"{label} checksum mismatch for {name}: expected {expected}, got {actual}")
    try:
        manifest = json.loads((path / "ava-release.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationError(f"{label} has an unreadable ava-release.json: {exc}") from exc
    required = {"ava_version", "tag", "source_revision", "semantic_review_required", "assets", "upgrade_paths"}
    missing_fields = sorted(required - set(manifest))
    if missing_fields:
        raise QualificationError(f"{label} release manifest is missing fields: {', '.join(missing_fields)}")
    version = manifest["ava_version"]
    tag = manifest["tag"]
    revision = manifest["source_revision"]
    if not isinstance(version, str) or not version or tag != f"v{version}":
        raise QualificationError(f"{label} has inconsistent version/tag identity")
    if not isinstance(revision, str) or not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise QualificationError(f"{label} has invalid source revision")
    if not isinstance(manifest["semantic_review_required"], bool):
        raise QualificationError(f"{label} has invalid semantic_review_required")
    asset_rows = manifest["assets"]
    if not isinstance(asset_rows, list) or {row.get("name") for row in asset_rows if isinstance(row, dict)} != set(RELEASE_ASSETS):
        raise QualificationError(f"{label} release manifest asset inventory is ambiguous or incomplete")
    return ReleaseIdentity(path, version, tag, revision, manifest["semantic_review_required"], manifest)


def validate_upgrade_pair(source: ReleaseIdentity, target: ReleaseIdentity) -> None:
    if source.version == target.version or source.revision == target.revision:
        raise QualificationError("source and target assets must identify distinct pinned releases")
    edges = target.manifest.get("upgrade_paths", {}).get("edges")
    if not isinstance(edges, list):
        raise QualificationError("target release does not declare an upgrade edge inventory")
    matching = [
        edge
        for edge in edges
        if isinstance(edge, dict) and edge.get("from") == source.version and edge.get("to") == target.version
    ]
    if len(matching) != 1:
        raise QualificationError(
            f"target assets must declare exactly one supported {source.version} -> {target.version} edge; found {len(matching)}"
        )
    if not target.semantic_review_required:
        raise QualificationError(
            "the complete synthetic matrix requires a semantic target so rollback, semantic reconciliation, and finalization are authentic"
        )


def load_matrix(path: Path = MATRIX_PATH) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationError(f"cannot read qualification matrix: {exc}") from exc
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise QualificationError("qualification matrix schema_version must be 1")
    families = value.get("families")
    scenarios = value.get("scenarios")
    if families != [
        "empty-before-installation",
        "mature-mixed-project",
        "registered-private-work-roles",
        "complete-pending-inbox",
        "managed-content-damage",
        "interrupted-upgrade-states",
        "pending-semantic-reconciliation",
        "uninstall-reinstallation",
    ]:
        raise QualificationError("qualification matrix family order differs from the maintained eight-family contract")
    if not isinstance(scenarios, list) or not scenarios:
        raise QualificationError("qualification matrix has no scenarios")
    ids = [item.get("id") for item in scenarios if isinstance(item, dict)]
    if len(ids) != len(scenarios) or len(set(ids)) != len(ids):
        raise QualificationError("qualification matrix scenario IDs must be unique non-empty values")
    if [item.get("order") for item in scenarios] != list(range(1, len(scenarios) + 1)):
        raise QualificationError("qualification matrix scenario order must be contiguous from 1")
    family_order = {name: index for index, name in enumerate(families)}
    seen_order = [family_order.get(item.get("family"), -1) for item in scenarios]
    if any(index < 0 for index in seen_order) or seen_order != sorted(seen_order):
        raise QualificationError("qualification scenarios are not ordered by the maintained family order")
    return value


def validate_materialized_variants(qualification_root: Path, matrix: dict[str, Any]) -> None:
    variants_index = qualification_root / "variants/index.json"
    finalized = qualification_root / "oracle/finalized-inventory.json"
    if not variants_index.is_file() or not finalized.is_file():
        raise QualificationError("qualification root must contain finalized inventory and materialized variants")
    index = json.loads(variants_index.read_text(encoding="utf-8"))
    families = index.get("families")
    if not isinstance(families, list):
        raise QualificationError("variants/index.json has no family inventory")
    actual = [item.get("id") for item in families if isinstance(item, dict)]
    if actual != matrix["families"]:
        raise QualificationError(f"materialized family order differs from matrix: {actual}")
    for scenario in matrix["scenarios"]:
        source = qualification_root / scenario["source"]
        project = source / "project"
        if not source.is_dir() or not project.is_dir():
            raise QualificationError(f"missing materialized scenario template for {scenario['id']}: {source}")


def repository_is_clean(repository_root: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repository_root), "status", "--porcelain", "--untracked-files=no"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise QualificationError(f"cannot inspect repository cleanliness: {result.stderr.strip()}")
    return not result.stdout.strip()


def resolve_executable(value: str) -> str:
    if os.sep in value:
        path = resolve_path(value)
        if not path.is_file() or not os.access(path, os.X_OK):
            raise QualificationError(f"OpenCode executable is unavailable: {path}")
        return str(path)
    resolved = shutil.which(value)
    if not resolved:
        raise QualificationError(f"OpenCode executable is unavailable on PATH: {value}")
    return resolved


def validate_execution_root(
    execution_root: Path,
    *,
    repository_root: Path,
    qualification_root: Path,
    test_project: Path,
    source_assets: Path,
    target_assets: Path,
) -> None:
    require_external(execution_root, repository_root, "execution root")
    for other, label in (
        (qualification_root, "qualification root"),
        (test_project, "test project"),
        (source_assets, "source assets"),
        (target_assets, "target assets"),
    ):
        require_disjoint(execution_root, other, "execution root", label)
    if execution_root.exists():
        if execution_root.is_symlink() or not execution_root.is_dir():
            raise QualificationError(f"execution root must be a normal directory: {execution_root}")
        entries = list(execution_root.iterdir())
        if entries:
            sentinel = execution_root / SENTINEL
            if not sentinel.is_file() or sentinel.is_symlink():
                raise QualificationError(
                    f"refusing unsafe pre-existing execution root without {SENTINEL}: {execution_root}"
                )
            data = json.loads(sentinel.read_text(encoding="utf-8"))
            if data.get("schema_version") != 1 or resolve_path(data.get("qualification_root", "")) != qualification_root:
                raise QualificationError("execution-root ownership sentinel does not match this qualification root")
            recorded_corpus = data.get("corpus_sha256")
            if not isinstance(recorded_corpus, str) or recorded_corpus != inventory_digest(qualification_root / "corpus"):
                raise QualificationError("finalized corpus differs from the execution-root ownership record")


def initialize_execution_root(execution_root: Path, qualification_root: Path) -> None:
    execution_root.mkdir(parents=True, exist_ok=True)
    sentinel = execution_root / SENTINEL
    if not sentinel.exists():
        sentinel.write_text(
            canonical_json(
                {
                    "schema_version": 1,
                    "qualification_root": str(qualification_root),
                    "corpus_sha256": inventory_digest(qualification_root / "corpus"),
                    "owner": "internal/release/qualify-synthetic.sh",
                }
            ),
            encoding="utf-8",
        )
    (execution_root / "scenarios").mkdir(exist_ok=True)


def load_state(execution_root: Path) -> dict[str, Any]:
    path = execution_root / STATE_FILE
    if not path.exists():
        return {"schema_version": 1, "scenarios": {}}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("scenarios"), dict):
        raise QualificationError(f"invalid runner state: {path}")
    return value


def save_state(execution_root: Path, state: dict[str, Any]) -> None:
    (execution_root / STATE_FILE).write_text(canonical_json(state), encoding="utf-8")


def scenario_workspace(
    execution_root: Path,
    qualification_root: Path,
    scenario: dict[str, Any],
    state: dict[str, Any],
) -> tuple[Path, bool]:
    scenario_id = scenario["id"]
    prior = state["scenarios"].get(scenario_id)
    destination = execution_root / "scenarios" / scenario_id
    if isinstance(prior, dict) and prior.get("outcome") == "pass" and destination.is_dir():
        return destination, True
    if destination.exists():
        shutil.rmtree(destination)
    source = qualification_root / scenario["source"]
    shutil.copytree(source, destination)
    return destination, False


def command_text(args: Sequence[str]) -> str:
    return " ".join(args)


class Runner:
    def __init__(
        self,
        *,
        repository_root: Path,
        qualification_root: Path,
        execution_root: Path,
        source: ReleaseIdentity,
        target: ReleaseIdentity,
        test_project: Path,
        opencode: str,
        model: str,
        transcript_dir: Path | None,
        matrix: dict[str, Any],
    ) -> None:
        self.repository_root = repository_root
        self.qualification_root = qualification_root
        self.execution_root = execution_root
        self.source = source
        self.target = target
        self.test_project = test_project
        self.opencode = opencode
        self.model = model
        self.transcript_dir = transcript_dir
        self.matrix = matrix
        self.state = load_state(execution_root)

    def run_command(
        self,
        scenario_id: str,
        args: Sequence[str],
        *,
        cwd: Path | None = None,
        check: bool = True,
        label: str = "command",
    ) -> CommandResult:
        env = os.environ.copy()
        existing = env.get("PYTHONPATH")
        env["PYTHONPATH"] = str(self.repository_root) + (os.pathsep + existing if existing else "")
        result = subprocess.run(
            list(args),
            cwd=str(cwd or self.repository_root),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        record = {
            "label": label,
            "command": list(args),
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        log = self.execution_root / "scenarios" / scenario_id / "runner-commands.jsonl"
        with log.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")
        if check and result.returncode != 0:
            raise QualificationError(
                f"{scenario_id}: {label} failed ({result.returncode}): {command_text(args)}\n{result.stderr.strip()}"
            )
        return CommandResult(result.returncode, result.stdout, result.stderr)

    def install(self, scenario_id: str, project: Path, assets: ReleaseIdentity, *extra: str) -> CommandResult:
        return self.run_command(
            scenario_id,
            [
                "sh",
                str(assets.directory / "ava-install.sh"),
                "--target",
                str(project),
                "--asset-dir",
                str(assets.directory),
                *extra,
            ],
            label=f"Ava {assets.version} installer",
        )

    def conformance(self, scenario_id: str, project: Path, *, check: bool = True) -> tuple[CommandResult, dict[str, Any]]:
        result = self.run_command(
            scenario_id,
            [
                sys.executable,
                "-m",
                "internal.release.conformance",
                "--root",
                str(project),
                "--mode",
                "installed",
                "--format",
                "json",
            ],
            check=False,
            label="installed conformance",
        )
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise QualificationError(f"{scenario_id}: conformance did not emit JSON") from exc
        if check and result.returncode != 0:
            ids = [item.get("rule_id") for item in payload.get("findings", []) if isinstance(item, dict)]
            raise QualificationError(f"{scenario_id}: installed conformance failed: {ids}")
        if check and payload.get("normal_routing_permitted") is not True:
            raise QualificationError(f"{scenario_id}: installed conformance did not permit normal routing")
        return result, payload

    def opencode_prompt(
        self,
        scenario_id: str,
        project: Path,
        prompt: str,
        *,
        expected_role: str | None = None,
    ) -> CommandResult:
        result = self.run_command(
            scenario_id,
            [
                self.opencode,
                "run",
                "--dir",
                str(project),
                "--model",
                self.model,
                "--format",
                "json",
                prompt,
            ],
            label="OpenCode prompt",
        )
        combined = result.stdout + "\n" + result.stderr
        if expected_role and f"Active primary role: {expected_role}" not in combined:
            raise QualificationError(f"{scenario_id}: OpenCode did not announce expected role {expected_role}")
        if self.transcript_dir:
            self.transcript_dir.mkdir(parents=True, exist_ok=True)
            (self.transcript_dir / f"{scenario_id}.jsonl").write_text(result.stdout, encoding="utf-8")
        return result

    def fresh_install(self, scenario_id: str, project: Path, assets: ReleaseIdentity) -> None:
        before = project_owned_digest(project)
        self.install(scenario_id, project, assets, "--dry-run")
        if project_owned_digest(project) != before:
            raise QualificationError(f"{scenario_id}: installer dry-run changed project-owned content")
        self.install(scenario_id, project, assets)
        self.conformance(scenario_id, project)

    def upgrade_to_target(self, scenario_id: str, project: Path) -> str:
        self.fresh_install(scenario_id, project, self.source)
        before = project_owned_digest(project)
        self.install(scenario_id, project, self.target)
        after = project_owned_digest(project)
        if before != after:
            raise QualificationError(f"{scenario_id}: deterministic upgrade changed project-owned content")
        manifest = read_manifest(project)
        if manifest["ava_version"] != self.target.version:
            raise QualificationError(f"{scenario_id}: target release identity was not installed")
        return before

    def run_scenario(self, scenario: dict[str, Any], workspace: Path) -> dict[str, Any]:
        scenario_id = scenario["id"]
        project = workspace / "project"
        kind = scenario["kind"]

        if kind == "fresh-install":
            self.fresh_install(scenario_id, project, self.target)
        elif kind == "mature-install":
            self.fresh_install(scenario_id, project, self.target)
            # Existing content is asserted explicitly because create-if-absent scaffolds may be new.
            for relative in ("index.md", "knowledge/private/home.md", "knowledge/work/platform.md", "opencode.json"):
                path = project / relative
                if not path.is_file():
                    raise QualificationError(f"{scenario_id}: existing mature-project file disappeared: {relative}")
            for relative in ("index.md", "knowledge/private/home.md", "knowledge/work/platform.md", "opencode.json"):
                original = self.qualification_root / scenario["source"] / "project" / relative
                if sha256_file(project / relative) != sha256_file(original):
                    raise QualificationError(f"{scenario_id}: installer changed existing project-owned file: {relative}")
        elif kind == "registered-routing":
            self.fresh_install(scenario_id, project, self.target)
            private_before = inventory_digest(project / "knowledge/private")
            work_before = inventory_digest(project / "knowledge/work")
            self.opencode_prompt(
                scenario_id,
                project,
                scenario["prompt"],
                expected_role=scenario["expected_role"],
            )
            private_after = inventory_digest(project / "knowledge/private")
            work_after = inventory_digest(project / "knowledge/work")
            boundary = scenario["mutation_boundary"]
            if boundary == "private" and not (private_after != private_before and work_after == work_before):
                raise QualificationError(f"{scenario_id}: private/work mutation boundary was not preserved")
            if boundary == "work" and not (work_after != work_before and private_after == private_before):
                raise QualificationError(f"{scenario_id}: work/private mutation boundary was not preserved")
        elif kind == "registered-calendar":
            self.fresh_install(scenario_id, project, self.target)
            private_before = inventory_digest(project / "knowledge/private")
            self.opencode_prompt(scenario_id, project, scenario["prompt"], expected_role=scenario["expected_role"])
            if inventory_digest(project / "knowledge/private") != private_before:
                raise QualificationError(f"{scenario_id}: calendar scenario changed private context")
            work_text = "\n".join(
                path.read_text(encoding="utf-8", errors="replace")
                for path in (project / "knowledge/work").rglob("*")
                if path.is_file()
            )
            if scenario["expected_date"] not in work_text or scenario["expected_weekday"].lower() not in work_text.lower():
                raise QualificationError(
                    f"{scenario_id}: persisted work context does not contain {scenario['expected_weekday']} {scenario['expected_date']}"
                )
            if scenario["forbidden_date"] in work_text:
                raise QualificationError(f"{scenario_id}: persisted the known-wrong calendar date {scenario['forbidden_date']}")
        elif kind == "registered-clarification":
            self.fresh_install(scenario_id, project, self.target)
            before = project_owned_digest(project)
            result = self.opencode_prompt(scenario_id, project, scenario["prompt"])
            if project_owned_digest(project) != before:
                raise QualificationError(f"{scenario_id}: ambiguous routing mutated project-owned content")
            lower = (result.stdout + result.stderr).lower()
            if not any(token in lower for token in ("clarif", "which", "ambiguous", "need you to")):
                raise QualificationError(f"{scenario_id}: ambiguous routing did not visibly request clarification")
        elif kind == "complete-inbox":
            self.fresh_install(scenario_id, project, self.target)
            self.opencode_prompt(scenario_id, project, scenario["prompt"], expected_role="Inbox Ingester")
            pending = [
                path
                for path in (project / "inbox").iterdir()
                if path.is_file() and path.name not in {"index.md", "log.md"}
            ]
            if pending:
                raise QualificationError(f"{scenario_id}: {len(pending)} direct inbox sources remain pending")
            self.conformance(scenario_id, project)
        elif kind == "managed-damage":
            self.fresh_install(scenario_id, project, self.target)
            injected = inject_damage(project, scenario["damage"])
            result, payload = self.conformance(scenario_id, project, check=False)
            if result.returncode == 0:
                raise QualificationError(f"{scenario_id}: damaged managed state unexpectedly passed conformance")
            observed = {
                item.get("rule_id")
                for item in payload.get("findings", [])
                if isinstance(item, dict)
            }
            expected_rule = scenario["expected_rule"]
            if expected_rule not in observed:
                raise QualificationError(f"{scenario_id}: expected {expected_rule}, observed {sorted(observed)}")
            verify_damage_unchanged(project, injected)
        elif kind == "resume":
            before = self.upgrade_source_checkpoint(scenario_id, project)
            self.run_command(
                scenario_id,
                [
                    sys.executable,
                    str(CHECKPOINT),
                    "resume",
                    "--target",
                    str(project),
                    "--asset-dir",
                    str(self.target.directory),
                ],
                label="resume checkpoint",
            )
            self.install(scenario_id, project, self.target, "--resume")
            assert_project_owned_digest(project, before, scenario_id)
            manifest = read_manifest(project)
            if manifest["ava_version"] != self.target.version:
                raise QualificationError(f"{scenario_id}: resume did not complete deterministic target installation")
            journal = read_journal(project)
            if read_manifest(project)["semantic_compatibility"].get("status") == "complete":
                assert_no_transactions(project, scenario_id)
                assert_terminal_journal(project, scenario_id, allowed_status={"complete"})
            elif journal.get("status") != "active" or journal.get("stage") != "semantic" or "reconcile-semantic" not in journal.get("allowed_operations", []):
                raise QualificationError(f"{scenario_id}: resume did not reach the target's authentic semantic stage")
        elif kind == "abort":
            before = self.upgrade_source_checkpoint(scenario_id, project)
            self.run_command(
                scenario_id,
                [
                    sys.executable,
                    str(CHECKPOINT),
                    "abort",
                    "--target",
                    str(project),
                    "--asset-dir",
                    str(self.target.directory),
                ],
                label="abort checkpoint",
            )
            self.install(scenario_id, project, self.target, "--abort")
            assert_project_owned_digest(project, before, scenario_id)
            if read_manifest(project)["ava_version"] != self.source.version:
                raise QualificationError(f"{scenario_id}: abort did not restore source release")
            assert_terminal_journal(project, scenario_id, allowed_status={"idle", "aborted"})
            assert_no_transactions(project, scenario_id)
            self.conformance(scenario_id, project)
        elif kind == "rollback":
            before = self.upgrade_to_target(scenario_id, project)
            journal = read_journal(project)
            if "rollback" not in journal.get("allowed_operations", []):
                raise QualificationError(f"{scenario_id}: target state does not authentically allow rollback")
            self.install(scenario_id, project, self.target, "--rollback")
            assert_project_owned_digest(project, before, scenario_id)
            if read_manifest(project)["ava_version"] != self.source.version:
                raise QualificationError(f"{scenario_id}: rollback did not restore source release")
            semantic = read_manifest(project)["semantic_compatibility"]
            if semantic.get("status") != "complete" or semantic.get("compatible_through") != self.source.version:
                raise QualificationError(f"{scenario_id}: rollback did not restore source semantic state")
            assert_terminal_journal(project, scenario_id, allowed_status={"rolled-back"})
            assert_no_transactions(project, scenario_id)
            self.conformance(scenario_id, project)
        elif kind == "finalize":
            self.upgrade_to_target(scenario_id, project)
            outcome = self.reconcile_semantic(scenario_id, project, scenario["semantic_prompt"])
            if outcome:
                return outcome
            self.opencode_prompt(scenario_id, project, scenario["finalize_prompt"], expected_role="Ava Maintenance")
            assert_target_complete(project, self.target.version, scenario_id)
            assert_no_transactions(project, scenario_id)
            self.conformance(scenario_id, project)
        elif kind == "semantic-reconciliation":
            self.upgrade_to_target(scenario_id, project)
            outcome = self.reconcile_semantic(scenario_id, project, scenario["prompt"])
            if outcome:
                return outcome
            manifest = read_manifest(project)
            if manifest["semantic_compatibility"].get("status") != "complete":
                raise QualificationError(f"{scenario_id}: semantic reconciliation did not reach complete")
        elif kind == "lifecycle":
            self.fresh_install(scenario_id, project, self.target)
            before = project_owned_digest(project)
            self.opencode_prompt(scenario_id, project, scenario["uninstall_prompt"], expected_role="Ava Maintenance")
            if (project / ".ava").exists() or (project / "AGENTS.md").exists():
                raise QualificationError(f"{scenario_id}: role-led uninstall left Ava-managed content")
            assert_project_owned_digest(project, before, scenario_id)
            self.install(scenario_id, project, self.target)
            assert_project_owned_digest(project, before, scenario_id)
            self.conformance(scenario_id, project)
        else:
            raise QualificationError(f"{scenario_id}: unsupported scenario kind: {kind}")
        return {"outcome": "pass"}

    def upgrade_source_checkpoint(self, scenario_id: str, project: Path) -> str:
        self.fresh_install(scenario_id, project, self.source)
        return project_owned_digest(project)

    def reconcile_semantic(self, scenario_id: str, project: Path, prompt: str) -> dict[str, Any] | None:
        result = self.opencode_prompt(scenario_id, project, prompt, expected_role="Upgrade Role")
        status = read_manifest(project)["semantic_compatibility"].get("status")
        if status == "complete":
            return None
        combined = (result.stdout + result.stderr).lower()
        if status in {"partial", "blocked"} or any(token in combined for token in ("decision", "approval", "clarif")):
            return {
                "outcome": "user-decision-required",
                "detail": f"semantic compatibility remains {status}",
            }
        raise QualificationError(f"{scenario_id}: semantic reconciliation ended in unexpected state {status}")

    def run(self) -> int:
        baseline_before = inventory_digest(self.qualification_root / "corpus")
        test_project_before = inventory_digest(self.test_project)
        outcomes: list[dict[str, Any]] = []
        blocked_by: str | None = None
        for scenario in self.matrix["scenarios"]:
            scenario_id = scenario["id"]
            if blocked_by is not None:
                outcomes.append(
                    {
                        "id": scenario_id,
                        "outcome": "skipped",
                        "detail": f"not run after non-passing scenario {blocked_by}",
                    }
                )
                continue
            workspace, already_passed = scenario_workspace(
                self.execution_root, self.qualification_root, scenario, self.state
            )
            if already_passed:
                outcome = self.state["scenarios"][scenario_id]
                outcomes.append({"id": scenario_id, **outcome})
                continue
            try:
                result = self.run_scenario(scenario, workspace)
            except QualificationError as exc:
                result = {"outcome": "fail", "detail": str(exc)}
            if result["outcome"] not in OUTCOMES:
                result = {"outcome": "fail", "detail": f"invalid runner outcome {result['outcome']!r}"}
            self.state["scenarios"][scenario_id] = result
            save_state(self.execution_root, self.state)
            outcomes.append({"id": scenario_id, **result})
            if result["outcome"] != "pass":
                blocked_by = scenario_id

        if inventory_digest(self.qualification_root / "corpus") != baseline_before:
            outcomes.append({"id": "finalized-corpus-integrity", "outcome": "fail", "detail": "corpus bytes changed"})
        if inventory_digest(self.test_project) != test_project_before:
            outcomes.append({"id": "test-project-integrity", "outcome": "fail", "detail": "original test project bytes changed"})
        write_summary(self.execution_root, outcomes, self.source, self.target)
        print_summary(outcomes)
        return summary_exit_status(outcomes)


def read_manifest(project: Path) -> dict[str, Any]:
    return json.loads((project / ".ava/state/manifest.json").read_text(encoding="utf-8"))


def read_journal(project: Path) -> dict[str, Any]:
    return json.loads((project / ".ava/state/upgrade.json").read_text(encoding="utf-8"))


def assert_project_owned_digest(project: Path, expected: str, scenario_id: str) -> None:
    actual = project_owned_digest(project)
    if actual != expected:
        raise QualificationError(f"{scenario_id}: project-owned bytes changed unexpectedly")


def assert_no_transactions(project: Path, scenario_id: str) -> None:
    transactions = project / ".ava/state/transactions"
    if transactions.exists() and any(transactions.iterdir()):
        raise QualificationError(f"{scenario_id}: transaction workspace remains after terminal operation")


def assert_terminal_journal(project: Path, scenario_id: str, allowed_status: set[str]) -> None:
    journal = read_journal(project)
    if journal.get("status") not in allowed_status or journal.get("allowed_operations") != ["normal"]:
        raise QualificationError(
            f"{scenario_id}: journal is not terminal: {journal.get('status')}/{journal.get('allowed_operations')}"
        )


def assert_target_complete(project: Path, target_version: str, scenario_id: str) -> None:
    manifest = read_manifest(project)
    journal = read_journal(project)
    semantic = manifest.get("semantic_compatibility", {})
    if (
        manifest.get("ava_version") != target_version
        or semantic.get("status") != "complete"
        or semantic.get("compatible_through") != target_version
        or semantic.get("target_version") is not None
        or semantic.get("unresolved_decisions")
        or journal.get("status") != "complete"
        or journal.get("allowed_operations") != ["normal"]
    ):
        raise QualificationError(f"{scenario_id}: target installation is not completely final")


def managed_payload_path(project: Path) -> Path:
    manifest = read_manifest(project)
    candidates = [
        entry.get("path")
        for entry in manifest.get("managed_files", [])
        if isinstance(entry, dict)
        and entry.get("kind") == "payload"
        and isinstance(entry.get("path"), str)
        and entry["path"].startswith("/.ava/base/")
    ]
    if not candidates:
        raise QualificationError("installed manifest has no .ava/base payload to damage")
    return project / sorted(candidates)[0].removeprefix("/")


def inject_damage(project: Path, kind: str) -> dict[str, Any]:
    if kind == "modified":
        path = managed_payload_path(project)
        path.write_bytes(path.read_bytes() + b"\nqualification-damage\n")
        return {"kind": kind, "path": str(path), "sha256": sha256_file(path)}
    if kind == "missing":
        path = managed_payload_path(project)
        path.unlink()
        return {"kind": kind, "path": str(path)}
    if kind == "corrupt":
        path = project / ".ava/state/upgrade.json"
        path.write_text("{not-json\n", encoding="utf-8")
        return {"kind": kind, "path": str(path), "sha256": sha256_file(path)}
    if kind == "unexpected":
        path = project / ".ava/base/.qualification-unexpected"
        path.write_text("qualification evidence\n", encoding="utf-8")
        return {"kind": kind, "path": str(path), "sha256": sha256_file(path)}
    raise QualificationError(f"unsupported managed damage kind: {kind}")


def verify_damage_unchanged(project: Path, evidence: dict[str, Any]) -> None:
    path = Path(evidence["path"])
    if evidence["kind"] == "missing":
        if path.exists():
            raise QualificationError("conformance changed the deliberately missing managed file")
        return
    if not path.is_file() or sha256_file(path) != evidence["sha256"]:
        raise QualificationError("conformance changed deliberately injected managed-damage evidence")


def summary_exit_status(outcomes: list[dict[str, Any]]) -> int:
    return 0 if outcomes and all(item.get("outcome") == "pass" for item in outcomes) else 1


def write_summary(
    execution_root: Path,
    outcomes: list[dict[str, Any]],
    source: ReleaseIdentity,
    target: ReleaseIdentity,
) -> None:
    payload = {
        "schema_version": 1,
        "source": {"version": source.version, "tag": source.tag, "revision": source.revision},
        "target": {"version": target.version, "tag": target.tag, "revision": target.revision},
        "outcomes": outcomes,
        "exit_status": summary_exit_status(outcomes),
    }
    (execution_root / "summary.json").write_text(canonical_json(payload), encoding="utf-8")


def print_summary(outcomes: list[dict[str, Any]]) -> None:
    print("Synthetic qualification summary")
    for item in outcomes:
        detail = f": {item['detail']}" if item.get("detail") else ""
        print(f"{item['outcome'].upper():22} {item['id']}{detail}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--qualification-root", type=Path, required=True)
    parser.add_argument("--execution-root", type=Path, required=True)
    parser.add_argument("--source-assets", type=Path, required=True)
    parser.add_argument("--target-assets", type=Path, required=True)
    parser.add_argument("--test-project", type=Path, required=True)
    parser.add_argument("--opencode", required=True, help="OpenCode executable path or name")
    parser.add_argument("--model", required=True, help="Explicit OpenCode provider/model identifier")
    parser.add_argument("--transcript-dir", type=Path)
    parser.add_argument("--preflight-only", action="store_true")
    return parser.parse_args(argv)


def preflight(args: argparse.Namespace) -> tuple[dict[str, Any], ReleaseIdentity, ReleaseIdentity, str]:
    repository_root = resolve_path(args.repository_root)
    qualification_root = resolve_path(args.qualification_root)
    execution_root = resolve_path(args.execution_root)
    source_assets = resolve_path(args.source_assets)
    target_assets = resolve_path(args.target_assets)
    test_project = resolve_path(args.test_project)

    if sys.version_info < (3, 11):
        raise QualificationError("qualification runner requires Python 3.11 or newer")
    if not repository_root.is_dir():
        raise QualificationError(f"repository root does not exist: {repository_root}")
    if not repository_is_clean(repository_root):
        raise QualificationError("Ava repository must be clean before qualification")
    require_external(qualification_root, repository_root, "qualification root")
    require_external(source_assets, repository_root, "source assets")
    require_external(target_assets, repository_root, "target assets")
    require_external(test_project, repository_root, "test project")
    if not qualification_root.is_dir() or not test_project.is_dir():
        raise QualificationError("qualification root and test project must be existing directories")
    matrix = load_matrix(repository_root / "internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json")
    validate_materialized_variants(qualification_root, matrix)
    source = validate_asset_dir(source_assets, "source assets")
    target = validate_asset_dir(target_assets, "target assets")
    validate_upgrade_pair(source, target)
    validate_execution_root(
        execution_root,
        repository_root=repository_root,
        qualification_root=qualification_root,
        test_project=test_project,
        source_assets=source_assets,
        target_assets=target_assets,
    )
    opencode = resolve_executable(args.opencode)
    version = subprocess.run([opencode, "--version"], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if version.returncode != 0:
        raise QualificationError(f"OpenCode version check failed: {version.stderr.strip()}")
    if not args.model.strip() or "/" not in args.model:
        raise QualificationError("--model must be an explicit provider/model identifier")
    fixture = subprocess.run(
        [sys.executable, str(repository_root / "internal/release/fixtures/synthetic-qualification-vault/fixture.py"), "verify", str(qualification_root)],
        cwd=str(repository_root),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if fixture.returncode != 0:
        raise QualificationError(f"finalized qualification vault verification failed: {fixture.stderr.strip()}")
    return matrix, source, target, opencode


def planned_summary(
    args: argparse.Namespace,
    matrix: dict[str, Any],
    source: ReleaseIdentity,
    target: ReleaseIdentity,
    opencode: str,
) -> None:
    print(f"qualification root: {resolve_path(args.qualification_root)}")
    print(f"execution root:     {resolve_path(args.execution_root)}")
    print(f"source assets:      {source.tag} {source.revision}")
    print(f"target assets:      {target.tag} {target.revision}")
    print(f"test project:       {resolve_path(args.test_project)} (read-only source boundary)")
    print(f"OpenCode:           {opencode}")
    print(f"model:              {args.model}")
    print("scenarios:")
    for scenario in matrix["scenarios"]:
        print(f"  {scenario['order']:02d}. {scenario['id']} [{scenario['family']}]")


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        matrix, source, target, opencode = preflight(args)
        planned_summary(args, matrix, source, target, opencode)
        if args.preflight_only:
            return 0
        repository_root = resolve_path(args.repository_root)
        qualification_root = resolve_path(args.qualification_root)
        execution_root = resolve_path(args.execution_root)
        test_project = resolve_path(args.test_project)
        transcript_dir = resolve_path(args.transcript_dir) if args.transcript_dir else None
        if transcript_dir:
            require_external(transcript_dir, repository_root, "transcript directory")
            require_disjoint(transcript_dir, qualification_root, "transcript directory", "qualification root")
        initialize_execution_root(execution_root, qualification_root)
        runner = Runner(
            repository_root=repository_root,
            qualification_root=qualification_root,
            execution_root=execution_root,
            source=source,
            target=target,
            test_project=test_project,
            opencode=opencode,
            model=args.model,
            transcript_dir=transcript_dir,
            matrix=matrix,
        )
        return runner.run()
    except (QualificationError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"synthetic qualification runner error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
