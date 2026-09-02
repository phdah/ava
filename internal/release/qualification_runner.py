"""Shared qualification scenario helpers.

Release qualification is executed through internal/release/qualify-release.sh.
"""

from __future__ import annotations

import json
from pathlib import Path

from internal.release import _qualification_runner_core as _core
from internal.release._qualification_runner_core import *  # noqa: F401,F403

for _entrypoint in ("parse_args", "preflight", "planned_summary", "main"):
    globals().pop(_entrypoint, None)


def initialize_execution_root(execution_root: Path, qualification_root: Path) -> None:
    """Initialize phase execution state owned by the qualification entrypoint."""
    _core.initialize_execution_root(execution_root, qualification_root)
    sentinel = execution_root / SENTINEL
    payload = json.loads(sentinel.read_text(encoding="utf-8"))
    payload["owner"] = "internal/release/qualify-release.sh"
    sentinel.write_text(canonical_json(payload), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit("use internal/release/qualify-release.sh")
