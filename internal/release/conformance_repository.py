"""Repository-source conformance checks."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from typing import Any

from internal.release.assemble import (
    AssemblyError,
    markdown_inline_link_targets,
    markdown_without_code,
    read_payloads,
    unresolved_installed_markdown_links,
)
from internal.release.conformance_common import (
    ACTOR_RE,
    OBSOLETE_PATHS,
    REPOSITORY_REQUIRED,
    RESERVED_MARKDOWN,
    ROLE_REQUIRED_FILES,
    Finding,
    ValidationResult,
    relative,
)


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[dict[str, Any] | None, str | None]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return None, "missing"
    try:
        end = lines.index("---", 1)
    except ValueError:
        return None, "unterminated"

    result: dict[str, Any] = {}
    current: str | None = None
    for number, line in enumerate(lines[1:end], 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and current:
            match = re.match(r"^\s{2}([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
            if not match:
                return None, f"unsupported nested frontmatter at line {number}"
            nested = result.setdefault(current, {})
            if not isinstance(nested, dict):
                return None, f"mixed scalar and mapping at line {number}"
            nested[match.group(1)] = strip_scalar(match.group(2))
            continue
        match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
        if not match:
            return None, f"unsupported frontmatter at line {number}"
        key, value = match.groups()
        current = key
        result[key] = strip_scalar(value) if value else {}
    return result, None


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def validate_provenance(
    root: Path,
    path: Path,
    metadata: dict[str, Any],
    findings: list[Finding],
) -> None:
    generated = metadata.get("generated")
    if generated is not None:
        if not isinstance(generated, dict) or set(generated) != {"by", "at"}:
            findings.append(
                Finding(
                    "AVA-META-GENERATED-SHAPE",
                    "error",
                    relative(root, path),
                    "generated must contain exactly by and at",
                    category="metadata",
                )
            )
        else:
            if not ACTOR_RE.fullmatch(str(generated.get("by", ""))):
                findings.append(
                    Finding(
                        "AVA-META-ACTOR",
                        "error",
                        relative(root, path),
                        "generated.by must use a stable agent:, human:, or tool: actor identifier",
                        category="metadata",
                    )
                )
            if parse_timestamp(generated.get("at")) is None:
                findings.append(
                    Finding(
                        "AVA-META-TIMESTAMP",
                        "error",
                        relative(root, path),
                        "generated.at must be an ISO 8601 timestamp",
                        category="metadata",
                    )
                )

    updated = metadata.get("updated")
    if updated is None:
        return
    if not isinstance(updated, dict) or set(updated) != {"by", "at"}:
        findings.append(
            Finding(
                "AVA-META-UPDATE-SHAPE",
                "error",
                relative(root, path),
                "updated must contain exactly by and at",
                category="metadata",
            )
        )
        return
    if not ACTOR_RE.fullmatch(str(updated.get("by", ""))):
        findings.append(
            Finding(
                "AVA-META-ACTOR",
                "error",
                relative(root, path),
                "updated.by must use a stable agent:, human:, or tool: actor identifier",
                category="metadata",
            )
        )
    updated_at = parse_timestamp(updated.get("at"))
    if updated_at is None:
        findings.append(
            Finding(
                "AVA-META-TIMESTAMP",
                "error",
                relative(root, path),
                "updated.at must be an ISO 8601 timestamp",
                category="metadata",
            )
        )
    generated_at = parse_timestamp(generated.get("at")) if isinstance(generated, dict) else None
    if updated_at and generated_at and updated_at < generated_at:
        findings.append(
            Finding(
                "AVA-META-UPDATE-REGRESSION",
                "error",
                relative(root, path),
                "updated.at cannot precede generated.at",
                category="metadata",
            )
        )


def public_markdown(root: Path) -> list[Path]:
    paths: list[Path] = []
    for directory in (root / "distribution", root / "templates/base", root / "templates/project-scaffolds"):
        if directory.is_dir():
            paths.extend(path for path in directory.rglob("*.md") if path.is_file())
    return sorted(set(paths), key=lambda path: relative(root, path).encode())


def local_link_target(path: Path, raw: str, *, project_root_paths: bool = False) -> Path | None:
    value = raw.strip()
    if not value or value.startswith(("#", "http://", "https://", "mailto:", "resource:")):
        return None
    value = value.split("#", 1)[0]
    if not value or value.startswith("/") or (project_root_paths and value.startswith("./")):
        return None
    return (path.parent / value).resolve()


def linked_names(index: Path) -> set[str]:
    if not index.is_file():
        return set()
    names: set[str] = set()
    text = markdown_without_code(index.read_text())
    for raw in markdown_inline_link_targets(text):
        value = raw.split("#", 1)[0].rstrip("/")
        if value and not value.startswith(("http://", "https://", "/")):
            names.add(Path(value).name)
    return names


def validate_repository(root: Path) -> ValidationResult:
    findings: list[Finding] = []

    for item in REPOSITORY_REQUIRED:
        if not (root / item).is_file():
            findings.append(
                Finding(
                    "AVA-REPOSITORY-REQUIRED",
                    "error",
                    item,
                    "required repository contract or implementation file is missing",
                    category="boundary",
                )
            )
    for item in OBSOLETE_PATHS:
        if (root / item).exists():
            findings.append(
                Finding(
                    "AVA-BOUNDARY-OBSOLETE",
                    "error",
                    item,
                    "obsolete distribution source location remains",
                    fix_available=True,
                    category="boundary",
                )
            )

    identifiers: dict[str, Path] = {}
    distributed_roots = (root / "templates/base", root / "templates/project-scaffolds")
    for path in public_markdown(root):
        text = path.read_text(errors="replace")
        if path.name not in RESERVED_MARKDOWN:
            metadata, error = parse_frontmatter(text)
            if error:
                findings.append(
                    Finding(
                        "AVA-DOC-FRONTMATTER",
                        "error",
                        relative(root, path),
                        f"invalid frontmatter: {error}",
                        category="metadata",
                    )
                )
            elif metadata is not None:
                if not isinstance(metadata.get("type"), str) or not metadata["type"].strip():
                    findings.append(
                        Finding(
                            "AVA-DOC-TYPE",
                            "error",
                            relative(root, path),
                            "non-reserved Markdown documents require a non-empty type",
                            category="metadata",
                        )
                    )
                validate_provenance(root, path, metadata, findings)
                identifier = metadata.get("id") or metadata.get("identifier")
                if isinstance(identifier, str) and identifier:
                    previous = identifiers.get(identifier)
                    if previous:
                        findings.append(
                            Finding(
                                "AVA-ID-DUPLICATE",
                                "error",
                                relative(root, path),
                                f"identifier {identifier!r} is also declared by {relative(root, previous)}",
                                decision_required=True,
                                category="discovery",
                            )
                        )
                    else:
                        identifiers[identifier] = path

        for raw in markdown_inline_link_targets(markdown_without_code(text)):
            target = local_link_target(
                path,
                raw,
                project_root_paths=any(path.is_relative_to(source_root) for source_root in distributed_roots),
            )
            if target is not None and not target.exists():
                findings.append(
                    Finding(
                        "AVA-LINK-MISSING",
                        "error",
                        relative(root, path),
                        f"local link target does not exist: {raw}",
                        category="discovery",
                    )
                )

    try:
        installed_link_issues = unresolved_installed_markdown_links(read_payloads(root))
    except (AssemblyError, UnicodeDecodeError) as exc:
        findings.append(
            Finding(
                "AVA-ASSEMBLY-MAPPING",
                "error",
                "templates",
                f"distributed source mapping cannot be validated: {exc}",
                category="boundary",
            )
        )
    else:
        for issue in installed_link_issues:
            if issue.archive_path.startswith("base/"):
                source_path = f"templates/base/{issue.archive_path.removeprefix('base/')}"
            else:
                source_path = f"templates/project-scaffolds/{issue.archive_path.removeprefix('scaffolds/')}"
            findings.append(
                Finding(
                    "AVA-INSTALLED-LINK-MISSING",
                    "error",
                    source_path,
                    f"link {issue.raw_target} from {issue.source_destination} resolves to missing installed path {issue.resolved_target}",
                    category="discovery",
                )
            )

    base = root / "templates/base"
    roles = base / "roles"
    registry = roles / "index.md"
    registry_text = registry.read_text(errors="replace") if registry.is_file() else ""
    if roles.is_dir():
        for directory in sorted((path for path in roles.iterdir() if path.is_dir()), key=lambda path: path.name.encode()):
            present = {path.name for path in directory.iterdir() if path.is_file()}
            missing = sorted(ROLE_REQUIRED_FILES - present)
            for name in missing:
                findings.append(
                    Finding(
                        "AVA-ROLE-STRUCTURE",
                        "error",
                        relative(root, directory / name),
                        "registered role is missing a required file",
                        category="discovery",
                        related={"role": directory.name},
                    )
                )
            if f"({directory.name}/)" not in registry_text:
                findings.append(
                    Finding(
                        "AVA-REGISTRY-MISSING",
                        "error",
                        relative(root, directory),
                        "role directory is not registered in templates/base/roles/index.md",
                        decision_required=True,
                        category="discovery",
                        related={"role": directory.name},
                    )
                )
            index = directory / "index.md"
            links = linked_names(index)
            for name in sorted((ROLE_REQUIRED_FILES - {"index.md"}) & present):
                if name not in links:
                    findings.append(
                        Finding(
                            "AVA-REQUIRED-READING-MISSING",
                            "error",
                            relative(root, index),
                            f"role index does not link required file {name}",
                            category="discovery",
                            related={"role": directory.name},
                        )
                    )

    workflow_registry = base / "workflows/index.md"
    workflow_registry_text = workflow_registry.read_text(errors="replace") if workflow_registry.is_file() else ""
    workflows = base / "workflows"
    if workflows.is_dir():
        for path in sorted(workflows.glob("*.md"), key=lambda item: item.name.encode()):
            if path.name in {"index.md", "log.md"}:
                continue
            if f"({path.name})" not in workflow_registry_text:
                findings.append(
                    Finding(
                        "AVA-REGISTRY-MISSING",
                        "error",
                        relative(root, path),
                        "workflow is not registered in templates/base/workflows/index.md",
                        decision_required=True,
                        category="discovery",
                        related={"workflow": path.stem},
                    )
                )
            metadata, error = parse_frontmatter(path.read_text(errors="replace"))
            if not error and metadata is not None:
                primary_role = metadata.get("primary_role")
                if not isinstance(primary_role, str) or not primary_role.startswith("./.ava/base/roles/"):
                    findings.append(
                        Finding(
                            "AVA-WORKFLOW-ROLE",
                            "error",
                            relative(root, path),
                            "workflow primary_role must be a canonical managed role path",
                            category="routing",
                            related={"workflow": path.stem},
                        )
                    )
                else:
                    source = base / primary_role.removeprefix("./.ava/base/")
                    if not source.is_file():
                        findings.append(
                            Finding(
                                "AVA-WORKFLOW-ROLE",
                                "error",
                                relative(root, path),
                                f"workflow primary_role does not resolve: {primary_role}",
                                category="routing",
                                related={"workflow": path.stem},
                            )
                        )

    indexed_scopes = (
        base / "shared/instructions",
        base / "workflows",
    )
    if roles.is_dir():
        indexed_scopes += tuple(path for path in roles.iterdir() if path.is_dir())
    for scope in indexed_scopes:
        index = scope / "index.md"
        links = linked_names(index)
        if not scope.is_dir() or not index.is_file():
            continue
        for path in scope.glob("*.md"):
            if path.name in RESERVED_MARKDOWN:
                continue
            if path.name not in links:
                findings.append(
                    Finding(
                        "AVA-INDEX-ORPHAN",
                        "recommendation",
                        relative(root, path),
                        "document is not discoverable from its direct index",
                        fix_available=True,
                        category="discovery",
                    )
                )

    for source_root in (base, root / "templates/project-scaffolds"):
        if not source_root.is_dir():
            continue
        for path in source_root.rglob("*"):
            if not path.is_file():
                continue
            text = path.read_text(errors="ignore")
            if re.search(r"\]\([^)]*internal/|resource:\s*/?internal/", text):
                findings.append(
                    Finding(
                        "AVA-INTERNAL-LEAKAGE",
                        "error",
                        relative(root, path),
                        "distributed source references repository-internal content",
                        decision_required=True,
                        category="boundary",
                    )
                )
            for obsolete in OBSOLETE_PATHS:
                if obsolete in text:
                    findings.append(
                        Finding(
                            "AVA-DEPRECATED-REFERENCE",
                            "error",
                            relative(root, path),
                            f"distributed source references obsolete path {obsolete}",
                            fix_available=True,
                            category="boundary",
                        )
                    )

    return ValidationResult("repository", findings)
