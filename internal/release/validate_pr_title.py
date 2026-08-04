#!/usr/bin/env python3
"""Validate and classify Ava pull-request titles."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass

ALLOWED_TYPES = frozenset(
    {
        "build",
        "chore",
        "ci",
        "docs",
        "feat",
        "fix",
        "perf",
        "refactor",
        "revert",
        "style",
        "test",
    }
)
RELEASE_LEVELS = {
    "feat": "minor",
    "fix": "patch",
    "perf": "patch",
    "revert": "patch",
}
TITLE_PATTERN = re.compile(
    r"^(?P<type>[a-z][a-z0-9-]*)"
    r"(?:\((?P<scope>[a-z0-9][a-z0-9._/-]*)\))?"
    r"(?P<breaking>!)?: (?P<subject>\S.*)$"
)


class TitleError(ValueError):
    """Raised when a pull-request title violates Ava's merge contract."""


@dataclass(frozen=True)
class Classification:
    type: str
    scope: str | None
    subject: str
    breaking: bool
    release_level: str | None


def classify(title: str) -> Classification:
    match = TITLE_PATTERN.fullmatch(title.strip())
    if not match:
        raise TitleError("expected '<type>(<scope>)!: <subject>' Conventional Commit syntax")

    change_type = match.group("type")
    if change_type not in ALLOWED_TYPES:
        allowed = ", ".join(sorted(ALLOWED_TYPES))
        raise TitleError(f"unsupported type '{change_type}'; expected one of: {allowed}")

    breaking = bool(match.group("breaking"))
    return Classification(
        type=change_type,
        scope=match.group("scope"),
        subject=match.group("subject"),
        breaking=breaking,
        release_level="major" if breaking else RELEASE_LEVELS.get(change_type),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("title")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = classify(args.title)
    except TitleError as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.as_json:
        print(json.dumps(asdict(result), sort_keys=True))
    else:
        release = result.release_level or "none"
        print(f"Valid Conventional Commit title: type={result.type} release={release}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
