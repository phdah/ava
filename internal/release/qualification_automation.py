"""Shared release-qualification automation API.

Release qualification execution must enter through internal/release/qualify-release.sh.
The implementation lives in the private core module; this import surface intentionally
exposes helpers but not the former standalone full-qualification command.
"""

from internal.release._qualification_automation_core import *  # noqa: F401,F403

# Do not expose the former standalone complete-matrix automation command API.
for _legacy_name in ("parse_args", "main"):
    globals().pop(_legacy_name, None)


if __name__ == "__main__":
    raise SystemExit(
        "qualification_automation.py is shared implementation support; "
        "use internal/release/qualify-release.sh"
    )
