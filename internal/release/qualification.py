#!/usr/bin/env python3
"""Canonical session-neutral deterministic Ava release qualification driver.

The release gate has no LLM runtime dependency. The active maintainer session may
be an ordinary ChatGPT chat, ChatGPT Work, or another repository-capable agent.
Deterministic execution is normally delegated to GitHub Actions; direct shell
execution remains supported when the current environment provides it.
"""

from __future__ import annotations

import json
import os
import sys

from internal.release import qualification_automation as automation
from internal.release import qualification_runner
from internal.release import qualification_work as implementation


def execution_label() -> str:
    value = os.environ.get("AVA_QUALIFICATION_EXECUTOR", "direct-shell").strip()
    if not value:
        raise ValueError("AVA_QUALIFICATION_EXECUTOR must be non-empty when set")
    return value


def validate_config(args) -> int:
    repository_root = implementation.resolve(args.repository_root)
    config, _, _ = automation.load_configuration(repository_root)
    print(f"qualification configuration valid: active pair {config['active_pair']}")
    print(f"release qualification mode: {implementation.QUALIFICATION_MODE}")
    print(f"qualification executor: {execution_label()}")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = implementation.parse_args(argv)
    try:
        # The underlying deterministic implementation historically called this
        # value WORK_HOST. It now records the actual executor label and imposes
        # no ChatGPT mode requirement.
        implementation.WORK_HOST = execution_label()
        if args.command == "validate-config":
            return validate_config(args)
        return implementation.execute(args)
    except (
        implementation.WorkQualificationError,
        automation.AutomationError,
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
