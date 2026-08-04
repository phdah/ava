"""Shared finding schema and primitives for Ava conformance validation."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable

SEVERITIES = ("error", "warning", "recommendation")
SEVERITY_RANK = {name: rank for rank, name in enumerate(SEVERITIES)}
ACTOR_RE = re.compile(r"^(?:agent|human|tool):[a-z0-9][a-z0-9._-]*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SEMVER_RE = re.compile(
    r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-(?:alpha|beta|rc)\.(?:0|[1-9][0-9]*))?$"
)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PROJECT_PATH_RE = re.compile(r"^\./(?:[^/]+/)*[^/]+$")
MANAGED_PATH_RE = re.compile(r"^/(?:[^/]+/)*[^/]+$")

RESERVED_MARKDOWN = {"index.md", "log.md"}
ROLE_REQUIRED_FILES = {"index.md", "role.md", "instructions.md", "capabilities.md", "constraints.md"}
REPOSITORY_REQUIRED = (
    "distribution/index.md",
    "distribution/paths.md",
    "distribution/ownership.md",
    "distribution/versioning.md",
    "distribution/releases.md",
    "distribution/upgrades.md",
    "distribution/guidance.md",
    "distribution/schemas/manifest.schema.json",
    "distribution/schemas/release.schema.json",
    "distribution/schemas/upgrade.schema.json",
    "distribution/schemas/guidance.schema.json",
    "templates/base/AGENTS.md",
    "templates/base/index.md",
    "templates/base/roles/index.md",
    "templates/base/workflows/index.md",
    "templates/base/shared/index.md",
    "templates/base/shared/instructions/index.md",
    "templates/project-scaffolds/index.md",
    "internal/release/assemble.py",
    "internal/release/ava-install.sh",
)
OBSOLETE_PATHS = (
    "templates/distribution-and-ownership.md",
    "templates/versioning-and-compatibility.md",
    "templates/github-release-assets.md",
    "templates/upgrade-and-migration.md",
    "templates/release-guidance.md",
    "templates/schemas",
    "templates/host-bootstraps",
)
RELEASE_ASSETS = (
    "ava-install.sh",
    "ava-base.tar.gz",
    "ava-guidance.tar.gz",
    "ava-migrations.tar.gz",
    "ava-release.json",
    "ava-release-notes.md",
    "SHA256SUMS",
)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    path: str
    message: str
    fix_available: bool = False
    decision_required: bool = False
    category: str = "structural"
    related: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.severity not in SEVERITY_RANK:
            raise ValueError(f"unsupported severity: {self.severity}")
        if not self.rule_id.startswith("AVA-"):
            raise ValueError(f"unstable rule identifier: {self.rule_id}")

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationResult:
    mode: str
    findings: list[Finding]
    normal_routing_permitted: bool | None = None

    @property
    def valid(self) -> bool:
        return not any(item.severity == "error" for item in self.findings)

    def to_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "schema_version": 1,
            "mode": self.mode,
            "valid": self.valid,
            "findings": [item.to_dict() for item in sorted_findings(self.findings)],
        }
        if self.normal_routing_permitted is not None:
            value["normal_routing_permitted"] = self.normal_routing_permitted
        return value


def sorted_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda item: (
            SEVERITY_RANK[item.severity],
            item.category.encode(),
            item.path.encode(),
            item.rule_id.encode(),
            item.message.encode(),
        ),
    )


def relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def read_json(path: Path) -> tuple[Any | None, str | None]:
    try:
        return json.loads(path.read_text()), None
    except FileNotFoundError:
        return None, "missing"
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, str(exc)
