#!/usr/bin/env python3
"""Deterministic inbox-fidelity checks for synthetic release qualification."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Iterable


class InboxStructuralError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---\n", 4)
    if end < 0:
        return ""
    return text[4:end]


def _source_rows(text: str, *, document: Path) -> list[dict[str, str]]:
    frontmatter = _frontmatter(text)
    if not frontmatter:
        return []

    rows: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    in_sources = False
    for line in frontmatter.splitlines():
        if re.fullmatch(r"sources:\s*", line):
            in_sources = True
            continue
        if in_sources and re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s*", line):
            break
        if not in_sources:
            continue

        item = re.match(r"^\s*-\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if item:
            if current is not None:
                rows.append(current)
            current = {item.group(1): _yaml_scalar(item.group(2))}
            continue
        field = re.match(r"^\s+([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$", line)
        if field and current is not None:
            current[field.group(1)] = _yaml_scalar(field.group(2))

    if current is not None:
        rows.append(current)

    for row in rows:
        if not row.get("id") or not row.get("resource"):
            raise InboxStructuralError(
                f"{document}: each sources entry must contain non-empty id and resource fields"
            )
    return rows


def _trusted_markdown(project: Path) -> Iterable[Path]:
    for path in sorted(project.rglob("*.md"), key=lambda item: item.relative_to(project).as_posix()):
        relative = path.relative_to(project)
        if relative.as_posix() == "AGENTS.md":
            continue
        if relative.parts and relative.parts[0] in {".ava", "inbox"}:
            continue
        yield path


def _local_target(value: str, *, document: Path) -> str:
    target = value.split("#", 1)[0]
    if not target:
        raise InboxStructuralError(f"{document}: empty local source path")
    if "://" in target or target.startswith("/"):
        raise InboxStructuralError(f"{document}: source path must be project-local: {value}")
    return target


def _metadata_resource_path(project: Path, document: Path, resource: str) -> Path:
    resource_path = _local_target(resource, document=document)
    if resource_path.startswith("./"):
        return (project / resource_path[2:]).resolve()
    return (document.parent / resource_path).resolve()


def _validate_footnote_label(label: str, *, document: Path) -> None:
    if not re.fullmatch(r"[1-9][0-9]*", label):
        raise InboxStructuralError(
            f"{document}: claim-provenance footnote label {label!r} must be a positive decimal integer"
        )


def _group_source_ids(value: str, *, document: Path, label: str) -> list[str]:
    prefix = "Sources:"
    if not value.startswith(prefix):
        raise InboxStructuralError(
            f"{document}: footnote definition {label!r} must begin with {prefix!r}"
        )

    payload = value[len(prefix) :].strip()
    if payload.endswith("."):
        payload = payload[:-1].rstrip()
    if not payload:
        raise InboxStructuralError(
            f"{document}: footnote definition {label!r} must reference at least one sources id"
        )
    if re.search(r"\[[^\]]*\]\([^)]+\)", payload):
        raise InboxStructuralError(
            f"{document}: footnote definition {label!r} must not repeat source links from metadata"
        )

    source_ids: list[str] = []
    for member in payload.split(";"):
        member = member.strip()
        match = re.fullmatch(r"`source:([^`\s]+)`\s+-\s+(.+)", member)
        if not match:
            raise InboxStructuralError(
                f"{document}: footnote definition {label!r} has malformed grouped source attribution"
            )
        source_id = match.group(1)
        if source_id in source_ids:
            raise InboxStructuralError(
                f"{document}: footnote definition {label!r} repeats sources id {source_id!r}"
            )
        source_ids.append(source_id)

    return source_ids


def validate_inbox_structural_fidelity(
    project: Path,
    selected_sources: list[dict[str, str]],
) -> None:
    """Check source preservation, metadata traceability, and renderable footnotes.

    This intentionally does not judge whether destination meaning is correct. That remains
    evaluator-only independent-audit work.
    """

    project = project.resolve()
    processed_root = (project / "inbox/processed").resolve()
    if not processed_root.is_dir():
        raise InboxStructuralError("inbox/processed is missing after ingestion")

    processed_files = [
        path.resolve()
        for path in processed_root.rglob("*")
        if path.is_file() and path.name not in {"index.md", "log.md"}
    ]
    processed_by_digest: dict[str, list[Path]] = {}
    for path in processed_files:
        processed_by_digest.setdefault(sha256_file(path), []).append(path)

    referenced_processed: set[Path] = set()
    for document in _trusted_markdown(project):
        text = document.read_text(encoding="utf-8", errors="replace")
        rows = _source_rows(text, document=document)
        if not rows:
            continue

        sources_by_id: dict[str, Path] = {}
        for row in rows:
            source_id = row["id"]
            if source_id in sources_by_id:
                raise InboxStructuralError(f"{document}: duplicate sources id {source_id!r}")
            resource = _metadata_resource_path(project, document, row["resource"])
            if not resource.is_file():
                raise InboxStructuralError(
                    f"{document}: sources resource does not resolve to a file: {row['resource']}"
                )
            if not resource.is_relative_to(processed_root):
                raise InboxStructuralError(
                    f"{document}: sources resource is outside inbox/processed: {row['resource']}"
                )
            sources_by_id[source_id] = resource
            referenced_processed.add(resource)

        definitions: dict[str, list[str]] = {}
        used_markers: set[str] = set()
        for line in text.splitlines():
            definition = re.match(r"^\[\^([^\]\s]+)\]:\s*(.*)$", line)
            if definition:
                definitions.setdefault(definition.group(1), []).append(definition.group(2))
                continue
            used_markers.update(re.findall(r"\[\^([^\]\s]+)\]", line))

        for label, values in definitions.items():
            _validate_footnote_label(label, document=document)
            if len(values) != 1:
                raise InboxStructuralError(
                    f"{document}: footnote definition {label!r} must appear exactly once"
                )
            source_ids = _group_source_ids(values[0], document=document, label=label)
            for source_id in source_ids:
                if source_id not in sources_by_id:
                    raise InboxStructuralError(
                        f"{document}: footnote definition {label!r} references unknown sources id {source_id!r}"
                    )

        for label in sorted(used_markers):
            _validate_footnote_label(label, document=document)
            values = definitions.get(label, [])
            if len(values) != 1:
                raise InboxStructuralError(
                    f"{document}: used footnote marker {label!r} requires exactly one definition"
                )

    for selected in selected_sources:
        source_path = selected.get("path", "<unknown>")
        digest = selected.get("sha256", "")
        matches = processed_by_digest.get(digest, [])
        if len(matches) != 1:
            raise InboxStructuralError(
                f"selected source {source_path} must be preserved exactly once under inbox/processed; found {len(matches)} matches"
            )
        if matches[0] not in referenced_processed:
            raise InboxStructuralError(
                f"selected source {source_path} is not referenced by trusted sources metadata"
            )
