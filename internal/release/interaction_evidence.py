"""Deterministic structural validation for processed interaction evidence."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any

from internal.release.conformance_common import ACTOR_RE, Finding, relative

INTERACTION_ID_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{15,127}$")
EVIDENCE_KINDS = {
    "fact",
    "authorization",
    "correction",
    "conflict-resolution",
    "retirement",
    "task-state",
    "mixed",
}


def _strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _parse_inline_list(value: str) -> list[str] | None:
    value = value.strip()
    if not (value.startswith("[") and value.endswith("]")):
        return None
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [_strip_scalar(item) for item in inner.split(",") if item.strip()]


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, "missing frontmatter"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "unterminated frontmatter"

    result: dict[str, Any] = {}
    current: str | None = None
    for number, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()
        if indent == 0:
            if ":" not in stripped:
                return None, f"invalid frontmatter at line {number}"
            key, raw = stripped.split(":", 1)
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]*", key):
                return None, f"invalid key at line {number}"
            value = raw.strip()
            inline = _parse_inline_list(value)
            if inline is not None:
                result[key] = inline
            elif value:
                result[key] = _strip_scalar(value)
            else:
                result[key] = None
            current = key
            continue
        if indent != 2 or current is None:
            return None, f"unsupported frontmatter nesting at line {number}"
        if stripped.startswith("- "):
            container = result.get(current)
            if container is None:
                container = []
                result[current] = container
            if not isinstance(container, list):
                return None, f"mixed mapping and list at line {number}"
            container.append(_strip_scalar(stripped[2:]))
            continue
        if ":" not in stripped:
            return None, f"invalid nested frontmatter at line {number}"
        key, raw = stripped.split(":", 1)
        container = result.get(current)
        if container is None:
            container = {}
            result[current] = container
        if not isinstance(container, dict):
            return None, f"mixed list and mapping at line {number}"
        container[key] = _strip_scalar(raw)
    return result, None


def _safe_project_path(value: Any) -> str | None:
    if not isinstance(value, str) or not value.startswith("./"):
        return None
    path = PurePosixPath(value[2:])
    if not path.parts or any(part in {"", ".", ".."} for part in path.parts):
        return None
    if path.parts[0] == ".ava" or path.as_posix() == "AGENTS.md":
        return None
    return path.as_posix()


def _timestamp(value: Any) -> bool:
    if not isinstance(value, str) or not value:
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def _is_interaction_metadata(metadata: dict[str, Any] | None, path: Path) -> bool:
    if metadata and metadata.get("type") == "Interaction Evidence":
        return True
    name = path.name
    if not name.startswith("interaction-") or not name.endswith(".md"):
        return False
    return bool(INTERACTION_ID_RE.fullmatch(name[len("interaction-") : -len(".md")]))


def validate_interaction_evidence(root: Path, findings: list[Finding]) -> None:
    processed = root / "inbox/processed"
    if not processed.is_dir():
        return

    records: list[tuple[Path, dict[str, Any], str]] = []
    seen_ids: dict[str, Path] = {}

    for path in sorted(processed.rglob("*.md")):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        metadata, error = parse_frontmatter(text)
        if not _is_interaction_metadata(metadata, path):
            continue
        logical = relative(root, path)
        if error or metadata is None:
            findings.append(Finding("AVA-INTERACTION-SHAPE", "error", logical, error or "invalid interaction evidence frontmatter", category="provenance"))
            continue
        if path.parent != processed:
            findings.append(Finding("AVA-INTERACTION-PATH", "error", logical, "interaction evidence must be stored directly under inbox/processed", category="provenance"))
        if metadata.get("type") != "Interaction Evidence" or not isinstance(metadata.get("title"), str) or not metadata.get("title"):
            findings.append(Finding("AVA-INTERACTION-SHAPE", "error", logical, "interaction evidence requires type and non-empty title", category="provenance"))

        interaction_id = metadata.get("interaction_id")
        if not isinstance(interaction_id, str) or not INTERACTION_ID_RE.fullmatch(interaction_id) or path.name != f"interaction-{interaction_id}.md":
            findings.append(Finding("AVA-INTERACTION-ID", "error", logical, "interaction_id must be opaque, safe, at least 16 characters, and match the filename", category="provenance"))
        else:
            previous = seen_ids.get(interaction_id)
            if previous is not None:
                findings.append(Finding("AVA-INTERACTION-DUPLICATE-ID", "error", logical, f"interaction_id duplicates {relative(root, previous)}", category="provenance"))
            else:
                seen_ids[interaction_id] = path

        if metadata.get("evidence_kind") not in EVIDENCE_KINDS:
            findings.append(Finding("AVA-INTERACTION-KIND", "error", logical, "unsupported or missing evidence_kind", category="provenance"))

        generated = metadata.get("generated")
        if not isinstance(generated, dict) or set(generated) != {"by", "at"} or not ACTOR_RE.fullmatch(str(generated.get("by", ""))) or not str(generated.get("by", "")).startswith(("agent:", "tool:")) or not _timestamp(generated.get("at")):
            findings.append(Finding("AVA-INTERACTION-SHAPE", "error", logical, "generated must contain a valid agent/tool actor and ISO 8601 timestamp", category="provenance"))

        supplier = metadata.get("supplier")
        supplier_valid = isinstance(supplier, dict) and supplier.get("kind") == "human" and supplier.get("identity") == "unverified"
        if supplier_valid and "actor" in supplier:
            actor = supplier.get("actor")
            supplier_valid = isinstance(actor, str) and actor.startswith("human:") and bool(ACTOR_RE.fullmatch(actor))
        if not supplier_valid:
            findings.append(Finding("AVA-INTERACTION-SUPPLIER", "error", logical, "supplier must be human/unverified with only an optional established human: actor", category="provenance"))

        targets = metadata.get("targets")
        if not isinstance(targets, list) or not targets:
            findings.append(Finding("AVA-INTERACTION-TARGET", "error", logical, "interaction evidence requires at least one project-owned target", category="provenance"))
            targets = []
        evidence_resource = "./" + logical
        for target in targets:
            safe = _safe_project_path(target)
            if safe is None:
                findings.append(Finding("AVA-INTERACTION-TARGET", "error", logical, f"unsafe or managed target: {target!r}", category="provenance"))
                continue
            target_path = root / safe
            if not target_path.is_file():
                findings.append(Finding("AVA-INTERACTION-TARGET", "error", logical, f"missing target: {target}", category="provenance"))
                continue
            target_text = target_path.read_text(encoding="utf-8", errors="replace")
            if evidence_resource not in target_text:
                findings.append(Finding("AVA-INTERACTION-REVERSE-REF", "error", logical, f"target does not reference {evidence_resource}: {target}", category="provenance"))

        supersedes = metadata.get("supersedes", [])
        if not isinstance(supersedes, list):
            findings.append(Finding("AVA-INTERACTION-SUPERSEDES", "error", logical, "supersedes must be a list", category="provenance"))
            supersedes = []
        for item in supersedes:
            safe = _safe_project_path(item)
            if safe is None or not safe.startswith("inbox/processed/interaction-"):
                findings.append(Finding("AVA-INTERACTION-SUPERSEDES", "error", logical, f"invalid superseded evidence path: {item!r}", category="provenance"))
                continue
            old_path = root / safe
            if not old_path.is_file():
                findings.append(Finding("AVA-INTERACTION-SUPERSEDES", "error", logical, f"missing superseded evidence: {item}", category="provenance"))
                continue
            old_metadata, old_error = parse_frontmatter(old_path.read_text(encoding="utf-8", errors="replace"))
            if old_error or not old_metadata or old_metadata.get("type") != "Interaction Evidence":
                findings.append(Finding("AVA-INTERACTION-SUPERSEDES", "error", logical, f"superseded path is not interaction evidence: {item}", category="provenance"))

        redactions = metadata.get("redactions", [])
        if not isinstance(redactions, list) or any(not isinstance(item, str) or not item for item in redactions):
            findings.append(Finding("AVA-INTERACTION-SHAPE", "error", logical, "redactions must be a list of non-empty non-sensitive reason strings", category="provenance"))

        statement = re.search(r"(?ms)^# Statement\s*$.*?(?=^# |\Z)", text)
        if statement is None or re.search(r"(?m)^>\s+\S", statement.group(0)) is None:
            findings.append(Finding("AVA-INTERACTION-STATEMENT", "error", logical, "interaction evidence requires an exact quoted statement under # Statement", category="provenance"))

        records.append((path, metadata, text))
