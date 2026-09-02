"""Shared qualification scenario API.

Release qualification execution must enter through internal/release/qualify-release.sh.
The implementation lives in the private core module so this public import surface cannot
execute the former complete 17-scenario qualification flow.
"""

from __future__ import annotations

import json
from pathlib import Path

from internal.release import _qualification_runner_core as _core
from internal.release._qualification_runner_core import *  # noqa: F401,F403

# Do not expose the former standalone complete-matrix command API.
for _legacy_name in ("parse_args", "preflight", "planned_summary", "main"):
    globals().pop(_legacy_name, None)


def initialize_execution_root(execution_root: Path, qualification_root: Path) -> None:
    """Initialize phase execution state with the canonical shell entrypoint as owner."""
    _core.initialize_execution_root(execution_root, qualification_root)
    sentinel = execution_root / SENTINEL
    payload = json.loads(sentinel.read_text(encoding="utf-8"))
    payload["owner"] = "internal/release/qualify-release.sh"
    sentinel.write_text(canonical_json(payload), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(
        "qualification_runner.py is shared implementation support; "
        "use internal/release/qualify-release.sh"
    )
