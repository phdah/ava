"""Shared helpers for release qualification automation.

Release qualification is executed through internal/release/qualify-release.sh.
"""

from internal.release._qualification_automation_core import *  # noqa: F401,F403

for _entrypoint in ("parse_args", "main"):
    globals().pop(_entrypoint, None)


if __name__ == "__main__":
    raise SystemExit("use internal/release/qualify-release.sh")
