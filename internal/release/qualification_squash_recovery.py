#!/usr/bin/env python3
"""One-time recovery validation for the accidentally squash-merged alpha.19 release."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from internal.release import qualification_acceptance as acceptance

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
TARGET_VERSION = "1.0.0-alpha.19"
PREVIOUS_VERSION = "1.0.0-alpha.18"
TAGGED_REVISION = "4aeb06b4292b9c768ea745ca5989e94c24d4be7c"
BASE_REVISION = "3d45f49ade63604cadeff89d376f3fa36b8f007d"
ACCEPTED_TREE = "4a881af3836573a6557615e68b9f895c4fd0ef08"
REVISION_RE = re.compile(r"^[0-9a-f]{40}$")


def validate_alpha19_squash_recovery(
    root: Path,
    *,
    previous_version: str,
    base_revision: str,
) -> str:
    root = root.resolve()
    target_version = (root / "version.txt").read_text(encoding="utf-8").strip()
    if target_version != TARGET_VERSION or previous_version != PREVIOUS_VERSION:
        raise acceptance.QualificationAcceptanceError(
            "squash recovery is limited to 1.0.0-alpha.18 -> 1.0.0-alpha.19"
        )
    if base_revision != BASE_REVISION:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 squash recovery base revision does not match the recorded release PR base"
        )

    head = acceptance.git(root, "rev-parse", "HEAD").stdout.strip()
    if head != TAGGED_REVISION:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 squash recovery is limited to the recorded tagged revision"
        )
    tree = acceptance.git(root, "rev-parse", "HEAD^{tree}").stdout.strip()
    if tree != ACCEPTED_TREE:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 tagged tree does not match the recorded accepted release PR tree"
        )

    parents = acceptance.git(root, "rev-list", "--parents", "-n", "1", "HEAD").stdout.split()
    if parents != [TAGGED_REVISION, BASE_REVISION]:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 tagged revision is not the expected one-parent squash of the release PR base"
        )

    acceptance.validate_acceptance_ledger(root, through_version=previous_version)
    entry, run = acceptance._qualified_run(root, target_version)
    if entry.get("previous_version") != previous_version:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 accepted qualification does not match the expected previous release"
        )
    if run.get("automated_state") != "awaiting-user-signoff" or run.get("mechanical_error") is not None:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 accepted run was not a clean automated qualification"
        )
    signoff = run.get("user_signoff")
    if not isinstance(signoff, dict):
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 accepted run is missing explicit user signoff"
        )
    if signoff.get("identity") != entry.get("accepted_by") or signoff.get("time") != entry.get("accepted_at"):
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 release acceptance and run signoff disagree"
        )

    source = run.get("source")
    target = run.get("target")
    identity = run.get("execution_identity")
    qualified_revision = entry.get("qualified_revision")
    if not isinstance(source, dict) or source.get("version") != previous_version:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 accepted run source does not match the previous release"
        )
    if not isinstance(target, dict) or target.get("version") != target_version or target.get("kind") != "local":
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 accepted run target does not match the local release candidate"
        )
    if not isinstance(identity, dict) or identity.get("repository_revision") != qualified_revision:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 accepted run repository revision does not match release state"
        )
    if not isinstance(qualified_revision, str) or REVISION_RE.fullmatch(qualified_revision) is None:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 accepted qualification revision is invalid"
        )
    if target.get("source_revision") != qualified_revision:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 qualified assets were not assembled from the qualified revision"
        )

    base_ok = acceptance.git(
        root,
        "merge-base",
        "--is-ancestor",
        base_revision,
        qualified_revision,
        check=False,
    )
    if base_ok.returncode != 0:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 qualified revision is not descended from the recorded release PR base"
        )

    changed = {
        line.strip()
        for line in acceptance.git(
            root,
            "diff",
            "--name-only",
            qualified_revision,
            "HEAD",
        ).stdout.splitlines()
        if line.strip()
    }
    invalid = sorted(
        path for path in changed if not path.startswith("internal/release/qualification/")
    )
    if invalid:
        raise acceptance.QualificationAcceptanceError(
            "alpha.19 tagged release content differs from the qualified revision outside qualification bookkeeping: "
            + ", ".join(invalid)
        )

    return (
        "validated one-time alpha.19 squash recovery; "
        f"qualified revision: {qualified_revision}; tagged revision: {TAGGED_REVISION}"
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--previous-version", required=True)
    parser.add_argument("--base-revision", required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        message = validate_alpha19_squash_recovery(
            args.root,
            previous_version=args.previous_version,
            base_revision=args.base_revision,
        )
    except (acceptance.QualificationAcceptanceError, OSError) as exc:
        print(f"release qualification recovery invalid: {exc}", file=sys.stderr)
        return 1
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
