from __future__ import annotations

import re
import unittest
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[3]
INSTRUCTIONS_PATH = ROOT / "internal/roles/ava-internal/instructions.md"
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


class InstructionNavigationTests(unittest.TestCase):
    def test_maintainer_instructions_link_only_to_indexes(self) -> None:
        text = INSTRUCTIONS_PATH.read_text()
        targets = MARKDOWN_LINK_RE.findall(text)
        self.assertTrue(targets, "maintainer instructions should expose index entry points")

        invalid: list[str] = []
        for target in targets:
            path = target.split("#", 1)[0].split("?", 1)[0]
            if PurePosixPath(path).name != "index.md":
                invalid.append(target)

        self.assertEqual(
            invalid,
            [],
            "instruction links must point only to index.md files; "
            f"found direct content links: {invalid}",
        )


if __name__ == "__main__":
    unittest.main()
