from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LEGACY_WORD = "al" + "pha"
LEGACY_VERSION = "1.0.0-" + LEGACY_WORD
LEGACY_PATTERNS = (
    re.compile(re.escape(LEGACY_VERSION), re.IGNORECASE),
    re.compile(re.escape("final-" + LEGACY_WORD), re.IGNORECASE),
    re.compile(re.escape(LEGACY_WORD + "-reset"), re.IGNORECASE),
    re.compile(re.escape("stable-" + "bootstrap"), re.IGNORECASE),
    re.compile(r"\b" + re.escape(LEGACY_WORD) + r"\d+(?:-to-" + re.escape(LEGACY_WORD) + r"\d+)?\b", re.IGNORECASE),
)
ALLOWED_HISTORY_ROOTS = (
    Path("internal/todo/tasks"),
    Path("internal/todo/archive/tasks"),
)


def allowed_history(path: Path) -> bool:
    return any(path == root or path.is_relative_to(root) for root in ALLOWED_HISTORY_ROOTS)


def contains_legacy(value: str) -> bool:
    return any(pattern.search(value) for pattern in LEGACY_PATTERNS)


class StableLineageCleanTests(unittest.TestCase):
    def test_legacy_release_lineage_exists_only_in_task_history(self) -> None:
        violations: list[str] = []
        for path in sorted(ROOT.rglob("*")):
            relative = path.relative_to(ROOT)
            if relative.parts and relative.parts[0] == ".git":
                continue
            if allowed_history(relative):
                continue
            if contains_legacy(relative.as_posix()):
                violations.append(f"path:{relative.as_posix()}")
                continue
            if not path.is_file():
                continue
            data = path.read_bytes()
            if b"\x00" in data:
                continue
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
            if contains_legacy(text):
                violations.append(f"content:{relative.as_posix()}")
        self.assertEqual([], violations, "legacy release lineage remains outside task history:\n" + "\n".join(violations))

    def test_stable_root_has_no_release_record(self) -> None:
        self.assertFalse((ROOT / "internal/release/catalogs/1.0.0.json").exists())


if __name__ == "__main__":
    unittest.main()
