#!/usr/bin/env python3
"""Canonical deterministic Ava release qualification CLI."""

from __future__ import annotations

import json
import os
import sys

from internal.release import qualification_engine
from internal.release import qualification_runner
from internal.release import qualification_state as state


def execution_label() -> str:
    value = os.environ.get("AVA_QUALIFICATION_EXECUTOR", "direct-shell").strip()
    if not value:
        raise ValueError("AVA_QUALIFICATION_EXECUTOR must be non-empty when set")
    return value


def validate_config(args) -> int:
    repository_root = qualification_engine.resolve(args.repository_root)
    config, _, _ = state.load_configuration(repository_root)
    print(f"qualification configuration valid: active pair {config['active_pair']}")
    print(f"release qualification mode: {qualification_engine.QUALIFICATION_MODE}")
    print(f"qualification executor: {execution_label()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = qualification_engine.parse_args(argv)
    try:
        qualification_engine.QUALIFICATION_EXECUTOR = execution_label()
        if args.command == "validate-config":
            return validate_config(args)
        return qualification_engine.execute(args)
    except (
        qualification_engine.QualificationExecutionError,
        state.QualificationStateError,
        qualification_runner.QualificationError,
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        StopIteration,
    ) as exc:
        print(f"deterministic qualification error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
