"""Installed-project conformance checks."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath
from typing import Any

from internal.release.conformance_common import (
    MANAGED_PATH_RE,
    PROJECT_PATH_RE,
    SEMVER_RE,
    SHA256_RE,
    Finding,
    ValidationResult,
    read_json,
)


def safe_managed_path(root: Path, value: str) -> Path | None:
    if not MANAGED_PATH_RE.fullmatch(value):
        return None
    path = PurePosixPath(value)
    if any(part in {"", ".", ".."} for part in path.parts[1:]):
        return None
    return root.joinpath(*path.parts[1:])


def validate_manifest_shape(root: Path, manifest: Any, findings: list[Finding]) -> None:
    path = ".ava/state/manifest.json"
    if not isinstance(manifest, dict):
        findings.append(Finding("AVA-MANIFEST-SHAPE", "error", path, "manifest must be a JSON object", category="deterministic"))
        return
    required = {
        "manifest_schema",
        "ava_version",
        "okf_version",
        "installed_at",
        "release",
        "managed_files",
        "host_integration",
        "semantic_compatibility",
    }
    missing = sorted(required - set(manifest))
    if missing:
        findings.append(
            Finding(
                "AVA-MANIFEST-FIELD",
                "error",
                path,
                f"manifest is missing required fields: {', '.join(missing)}",
                category="deterministic",
            )
        )
    version = manifest.get("ava_version")
    if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
        findings.append(Finding("AVA-MANIFEST-VERSION", "error", path, "ava_version is not valid SemVer", category="deterministic"))
    if manifest.get("manifest_schema") != 1:
        findings.append(Finding("AVA-MANIFEST-SCHEMA", "error", path, "unsupported manifest_schema", category="deterministic"))


def validate_semantic_state(manifest: dict[str, Any], findings: list[Finding]) -> bool:
    path = ".ava/state/manifest.json"
    semantic = manifest.get("semantic_compatibility")
    version = manifest.get("ava_version")
    if not isinstance(semantic, dict):
        findings.append(Finding("AVA-SEMANTIC-STATE", "error", path, "semantic_compatibility must be an object", category="semantic"))
        return False
    status = semantic.get("status")
    compatible = semantic.get("compatible_through")
    target = semantic.get("target_version")
    decisions = semantic.get("unresolved_decisions")
    if status not in {"complete", "pending", "partial", "blocked"}:
        findings.append(Finding("AVA-SEMANTIC-STATE", "error", path, "semantic status is unsupported", category="semantic"))
        return False
    if not isinstance(compatible, str) or not SEMVER_RE.fullmatch(compatible):
        findings.append(Finding("AVA-SEMANTIC-STATE", "error", path, "compatible_through is invalid", category="semantic"))
    if not isinstance(decisions, list) or any(not isinstance(item, str) or not item for item in decisions):
        findings.append(Finding("AVA-SEMANTIC-STATE", "error", path, "unresolved_decisions must be a list of non-empty strings", category="semantic"))
        decisions = []
    if status == "complete":
        if target is not None or decisions or compatible != version:
            findings.append(
                Finding(
                    "AVA-SEMANTIC-COMPLETE",
                    "error",
                    path,
                    "complete semantic state requires target_version null, no decisions, and compatible_through equal to ava_version",
                    category="semantic",
                )
            )
        return True
    if target != version:
        findings.append(
            Finding(
                "AVA-SEMANTIC-TARGET",
                "error",
                path,
                "incomplete semantic state must target the installed ava_version",
                category="semantic",
            )
        )
    if status == "pending" and decisions:
        findings.append(Finding("AVA-SEMANTIC-STATE", "error", path, "pending state cannot contain unresolved decisions", category="semantic"))
    if status == "blocked" and not decisions:
        findings.append(Finding("AVA-SEMANTIC-STATE", "error", path, "blocked state requires an unresolved decision", category="semantic"))
    findings.append(
        Finding(
            "AVA-SEMANTIC-INCOMPLETE",
            "warning" if status in {"partial", "blocked"} else "recommendation",
            path,
            f"project-owned context is semantically {status}; ordinary routing must remain blocked",
            decision_required=status in {"partial", "blocked"},
            category="semantic",
            related={"role": "Upgrade Role", "target_version": str(target)},
        )
    )
    return False


def validate_upgrade_state(upgrade: Any, semantic_complete: bool, findings: list[Finding]) -> bool:
    path = ".ava/state/upgrade.json"
    if not isinstance(upgrade, dict):
        findings.append(Finding("AVA-UPGRADE-SHAPE", "error", path, "upgrade journal must be a JSON object", category="deterministic"))
        return False
    status = upgrade.get("status")
    stage = upgrade.get("stage")
    operations = upgrade.get("allowed_operations")
    if upgrade.get("upgrade_schema") != 1:
        findings.append(Finding("AVA-UPGRADE-SCHEMA", "error", path, "unsupported upgrade_schema", category="deterministic"))
    if status not in {"idle", "active", "blocked", "complete", "aborted", "rolled-back"}:
        findings.append(Finding("AVA-UPGRADE-STATE", "error", path, "unsupported journal status", category="deterministic"))
        return False
    if not isinstance(operations, list) or not operations:
        findings.append(Finding("AVA-UPGRADE-STATE", "error", path, "allowed_operations must be a non-empty list", category="deterministic"))
        operations = []
    terminal_stage = {"idle": "idle", "complete": "complete", "aborted": "aborted", "rolled-back": "rolled-back"}
    if status in terminal_stage:
        if stage != terminal_stage[status] or operations != ["normal"]:
            findings.append(
                Finding(
                    "AVA-UPGRADE-TERMINAL",
                    "error",
                    path,
                    f"{status} journal requires stage {terminal_stage[status]} and allowed_operations ['normal']",
                    category="deterministic",
                )
            )
    else:
        if "normal" in operations:
            findings.append(Finding("AVA-UPGRADE-ACTIVE", "error", path, "active or blocked journals cannot allow normal routing", category="deterministic"))
        if stage in {"idle", "complete", "aborted", "rolled-back", None}:
            findings.append(Finding("AVA-UPGRADE-ACTIVE", "error", path, "active or blocked journal has a terminal or missing stage", category="deterministic"))
        findings.append(
            Finding(
                "AVA-DETERMINISTIC-INCOMPLETE",
                "warning",
                path,
                f"deterministic work is {status}/{stage}; ordinary routing must remain blocked",
                category="deterministic",
                related={"role": "Ava Maintenance", "stage": str(stage)},
            )
        )
    normal = status in {"idle", "complete", "aborted", "rolled-back"} and operations == ["normal"] and semantic_complete
    if not normal and status in {"idle", "complete", "aborted", "rolled-back"} and not semantic_complete:
        findings.append(
            Finding(
                "AVA-ROUTING-BLOCKED",
                "recommendation",
                path,
                "journal is terminal but semantic compatibility is incomplete, so ordinary routing remains blocked",
                category="routing",
                related={"role": "Upgrade Role"},
            )
        )
    return normal


def validate_opencode(root: Path, findings: list[Finding]) -> None:
    for name in ("opencode.json", "opencode.jsonc"):
        path = root / name
        if not path.is_file():
            continue
        text = path.read_text(errors="replace")
        if ".ava/**" not in text or not re.search(r'"read"\s*:\s*\{[^}]*"\.ava/\*\*"\s*:\s*"allow"', text, re.DOTALL):
            findings.append(
                Finding(
                    "AVA-HOST-OPENCODE-READ",
                    "warning",
                    name,
                    "OpenCode configuration does not grant read access to .ava/**",
                    decision_required=True,
                    category="host",
                    related={"host": "OpenCode", "role": "Ava Maintenance"},
                )
            )
        if not re.search(r'"edit"\s*:\s*\{[^}]*"\.ava/\*\*"\s*:\s*"ask"', text, re.DOTALL):
            findings.append(
                Finding(
                    "AVA-HOST-OPENCODE-EDIT",
                    "recommendation",
                    name,
                    "OpenCode configuration should require confirmation before editing .ava/**",
                    decision_required=True,
                    category="host",
                    related={"host": "OpenCode", "role": "Ava Maintenance"},
                )
            )


def validate_installed(root: Path) -> ValidationResult:
    findings: list[Finding] = []
    manifest_path = root / ".ava/state/manifest.json"
    upgrade_path = root / ".ava/state/upgrade.json"
    if not (root / "AGENTS.md").is_file():
        findings.append(Finding("AVA-INSTALL-ROUTER", "error", "AGENTS.md", "managed root router is missing", category="deterministic"))

    manifest, manifest_error = read_json(manifest_path)
    if manifest_error:
        findings.append(
            Finding(
                "AVA-MANIFEST-READ",
                "error",
                ".ava/state/manifest.json",
                f"manifest is {manifest_error}",
                category="deterministic",
                related={"role": "Ava Maintenance"},
            )
        )
        manifest = None
    upgrade, upgrade_error = read_json(upgrade_path)
    if upgrade_error:
        findings.append(
            Finding(
                "AVA-UPGRADE-READ",
                "error",
                ".ava/state/upgrade.json",
                f"upgrade journal is {upgrade_error}",
                category="deterministic",
                related={"role": "Ava Maintenance"},
            )
        )
        upgrade = None

    if isinstance(manifest, dict):
        validate_manifest_shape(root, manifest, findings)
        entries = manifest.get("managed_files")
        if not isinstance(entries, list):
            findings.append(Finding("AVA-MANIFEST-FIELD", "error", ".ava/state/manifest.json", "managed_files must be a list", category="deterministic"))
            entries = []
        seen: set[str] = set()
        expected_payload: set[str] = set()
        for entry in entries:
            if not isinstance(entry, dict):
                findings.append(Finding("AVA-MANAGED-ENTRY", "error", ".ava/state/manifest.json", "managed_files entries must be objects", category="deterministic"))
                continue
            value = entry.get("path")
            kind = entry.get("kind")
            if not isinstance(value, str) or safe_managed_path(root, value) is None:
                findings.append(Finding("AVA-MANAGED-PATH", "error", ".ava/state/manifest.json", f"unsafe or invalid managed path: {value!r}", category="deterministic"))
                continue
            if value in seen:
                findings.append(Finding("AVA-MANAGED-DUPLICATE", "error", ".ava/state/manifest.json", f"duplicate managed path: {value}", category="deterministic"))
                continue
            seen.add(value)
            live = safe_managed_path(root, value)
            assert live is not None
            if kind == "payload":
                expected_payload.add(value)
                digest = entry.get("sha256")
                if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                    findings.append(Finding("AVA-MANAGED-CHECKSUM-SHAPE", "error", ".ava/state/manifest.json", f"payload checksum is invalid for {value}", category="deterministic"))
                elif not live.is_file() or live.is_symlink():
                    findings.append(Finding("AVA-MANAGED-MISSING", "error", value.removeprefix("/"), "managed payload is missing or not a regular file", category="deterministic", related={"role": "Ava Maintenance"}))
                elif hashlib.sha256(live.read_bytes()).hexdigest() != digest:
                    findings.append(Finding("AVA-MANAGED-CHECKSUM", "error", value.removeprefix("/"), "managed payload checksum does not match the manifest", decision_required=True, category="deterministic", related={"role": "Ava Maintenance"}))
            elif kind == "state":
                if value not in {"/.ava/state/manifest.json", "/.ava/state/upgrade.json"}:
                    findings.append(Finding("AVA-MANAGED-STATE-PATH", "error", ".ava/state/manifest.json", f"unexpected mutable managed state path: {value}", category="deterministic"))
            else:
                findings.append(Finding("AVA-MANAGED-KIND", "error", ".ava/state/manifest.json", f"unsupported managed kind for {value}", category="deterministic"))

        for required in {"/AGENTS.md", "/.ava/state/manifest.json", "/.ava/state/upgrade.json"}:
            if required not in seen:
                findings.append(Finding("AVA-MANAGED-REQUIRED", "error", ".ava/state/manifest.json", f"required managed path is not recorded: {required}", category="deterministic"))

        for directory in (root / ".ava/base", root / ".ava/guidance", root / ".ava/migrations"):
            if not directory.is_dir():
                continue
            for path in directory.rglob("*"):
                if path.is_file():
                    logical = "/" + path.relative_to(root).as_posix()
                    if logical not in expected_payload:
                        findings.append(
                            Finding(
                                "AVA-MANAGED-UNEXPECTED",
                                "error",
                                path.relative_to(root).as_posix(),
                                "unexpected file exists inside an Ava-managed payload root",
                                decision_required=True,
                                category="deterministic",
                                related={"role": "Ava Maintenance"},
                            )
                        )

        host = manifest.get("host_integration")
        if host is not None:
            if not isinstance(host, dict) or host.get("ownership") != "project-owned" or host.get("discovery") != "project-provided":
                findings.append(Finding("AVA-HOST-INTEGRATION", "error", ".ava/state/manifest.json", "host_integration has unsupported ownership or discovery metadata", category="host"))
            else:
                entrypoint = host.get("entrypoint")
                if not isinstance(entrypoint, str) or not PROJECT_PATH_RE.fullmatch(entrypoint) or entrypoint.startswith(("./AGENTS.md", "./.ava/")) or "/../" in entrypoint:
                    findings.append(Finding("AVA-HOST-ENTRYPOINT", "error", ".ava/state/manifest.json", "host entrypoint is not a safe canonical project-owned path", category="host"))
                elif not (root / entrypoint.removeprefix("./")).is_file():
                    findings.append(Finding("AVA-HOST-ENTRYPOINT", "warning", entrypoint, "recorded project-owned host entrypoint is missing", decision_required=True, category="host", related={"role": "Ava Maintenance"}))

        semantic_complete = validate_semantic_state(manifest, findings)
    else:
        semantic_complete = False

    normal = validate_upgrade_state(upgrade, semantic_complete, findings) if upgrade is not None else False
    validate_opencode(root, findings)
    blocking_categories = {"deterministic", "semantic", "routing"}
    if any(finding.severity == "error" and finding.category in blocking_categories for finding in findings):
        normal = False
    return ValidationResult("installed", findings, normal_routing_permitted=normal)
