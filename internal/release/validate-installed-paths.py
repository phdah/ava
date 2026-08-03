#!/usr/bin/env python3
"""Validate project-root path references in distributed Ava source content."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

AMBIGUOUS_PROJECT_PATH_RE = re.compile(
    r"(?<![.A-Za-z0-9_:/-])"
    r"(/(?:AGENTS\.md|\.ava(?=/|\b)|roles/|workflows/|shared/|knowledge/|inbox/|index\.md|log\.md))"
)
PROJECT_PATH_RE = re.compile(r"\./[A-Za-z0-9._/-]+")
GENERATED_ROOTS = (
    "./.ava/state/",
    "./.ava/guidance/",
)
PROJECT_EXTENSION_ROOTS = (
    "./roles/",
    "./workflows/",
    "./shared/",
    "./knowledge/",
    "./inbox/",
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    token: str

    def format(self, root: Path) -> str:
        return f"{self.path.relative_to(root)}:{self.line}: ambiguous project path {self.token!r}; use './...'"


def distributed_sources(root: Path) -> list[Path]:
    base = root / "templates" / "base"
    scaffolds = root / "templates" / "project-scaffolds"
    paths: list[Path] = []

    for path in base.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(base)
        if relative.parts and relative.parts[0] in {"knowledge", "inbox"}:
            continue
        paths.append(path)

    paths.extend(path for path in scaffolds.rglob("*") if path.is_file())
    return sorted(set(paths), key=lambda path: path.relative_to(root).as_posix().encode())


def ambiguous_findings(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in distributed_sources(root):
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            for match in AMBIGUOUS_PROJECT_PATH_RE.finditer(line):
                findings.append(Finding(path, line_number, match.group(1)))
    return findings


def source_for_installed_path(root: Path, value: str) -> Path | None:
    if value == "./AGENTS.md":
        return root / "templates/base/AGENTS.md"
    if value.startswith("./.ava/base/"):
        return root / "templates/base" / value.removeprefix("./.ava/base/")
    if value.startswith(GENERATED_ROOTS):
        return None
    if value in {"./index.md", "./log.md"}:
        return root / "templates/project-scaffolds" / value.removeprefix("./")
    if value.startswith(PROJECT_EXTENSION_ROOTS):
        return root / "templates/project-scaffolds" / value.removeprefix("./")
    raise ValueError(f"unclassified project-root path: {value}")


def router_project_paths(root: Path) -> list[str]:
    router = root / "templates/base/AGENTS.md"
    return sorted(set(PROJECT_PATH_RE.findall(router.read_text())))


def unresolved_router_paths(root: Path) -> list[str]:
    unresolved: list[str] = []
    for value in router_project_paths(root):
        try:
            source = source_for_installed_path(root, value)
        except ValueError:
            unresolved.append(value)
            continue
        if source is not None and not source.is_file():
            unresolved.append(value)
    return unresolved


def validate(root: Path) -> list[str]:
    errors = [finding.format(root) for finding in ambiguous_findings(root)]
    errors.extend(
        f"templates/base/AGENTS.md: unresolved project-root path {value!r}"
        for value in unresolved_router_paths(root)
    )

    router = (root / "templates/base/AGENTS.md").read_text()
    regression = "./.ava/base/shared/instructions/upgrade-state-and-routing.md"
    if regression not in router:
        errors.append(f"templates/base/AGENTS.md: missing regression reference {regression!r}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Installed project paths valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
