#!/usr/bin/env python3
"""Validate Ava repository sources, installed projects, and release assets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

from internal.release.conformance_common import (
    REPOSITORY_REQUIRED,
    SEVERITIES,
    SEVERITY_RANK,
    Finding,
    ValidationResult,
    sorted_findings,
)
from internal.release.conformance_installed import validate_installed
from internal.release.conformance_release import validate_release
from internal.release.conformance_repository import validate_repository
from internal.release.interaction_evidence import validate_interaction_evidence


def detect_mode(root: Path) -> str:
    if (root / ".ava/state/manifest.json").exists() or (root / ".ava").exists():
        return "installed"
    if (root / "ava-release.json").exists() or (root / "SHA256SUMS").exists():
        return "release"
    return "repository"


def validate(root: Path, mode: str = "auto", *, require_publication_evidence: bool = False) -> ValidationResult:
    resolved = root.resolve()
    selected = detect_mode(resolved) if mode == "auto" else mode
    if selected == "repository":
        return validate_repository(resolved)
    if selected == "installed":
        result = validate_installed(resolved)
        validate_interaction_evidence(resolved, result.findings)
        return result
    if selected == "release":
        return validate_release(resolved, require_publication_evidence=require_publication_evidence)
    raise ValueError(f"unsupported validation mode: {selected}")


def should_fail(findings: Iterable[Finding], threshold: str) -> bool:
    if threshold == "never":
        return False
    rank = SEVERITY_RANK[threshold]
    return any(SEVERITY_RANK[item.severity] <= rank for item in findings)


def format_text(result: ValidationResult) -> str:
    lines = [
        f"{item.severity.upper()} [{item.rule_id}] {item.path}: {item.message}"
        for item in sorted_findings(result.findings)
    ]
    if not lines:
        lines.append(f"Ava {result.mode} conformance valid.")
    if result.normal_routing_permitted is not None:
        lines.append(f"Normal routing permitted: {'yes' if result.normal_routing_permitted else 'no'}")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--mode", choices=("auto", "repository", "installed", "release"), default="auto")
    parser.add_argument("--format", choices=("text", "json", "jsonl"), default="text")
    parser.add_argument("--fail-on", choices=SEVERITIES + ("never",), default="error")
    parser.add_argument("--require-publication-evidence", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = validate(args.root, args.mode, require_publication_evidence=args.require_publication_evidence)
    if args.format == "json":
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    elif args.format == "jsonl":
        for item in sorted_findings(result.findings):
            print(json.dumps(item.to_dict(), sort_keys=True))
    else:
        print(format_text(result))
    return 1 if should_fail(result.findings, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
