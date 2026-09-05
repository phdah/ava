from __future__ import annotations

import unittest
from pathlib import Path

from internal.release.assemble import read_payloads

SOURCE_ROOT = Path(__file__).resolve().parents[3]


class ProjectTaskBoardTests(unittest.TestCase):
    def test_release_maps_backlog_scaffold_as_project_owned_create_if_absent(self) -> None:
        payloads = {item.destination: item for item in read_payloads(SOURCE_ROOT)}
        expected = {
            "/backlog.config.yml",
            "/backlog/index.md",
            "/backlog/tasks/index.md",
        }

        self.assertTrue(expected.issubset(payloads))
        self.assertNotIn("/backlog/completed/index.md", payloads)
        self.assertNotIn("/backlog/tasks/.gitkeep", payloads)
        for destination in expected:
            payload = payloads[destination]
            self.assertEqual(payload.ownership, "project-owned")
            self.assertEqual(payload.operation, "create-if-absent")
            self.assertEqual(payload.role, "scaffold")

    def test_project_task_manager_is_managed_base_content(self) -> None:
        payloads = {item.destination: item for item in read_payloads(SOURCE_ROOT)}
        for name in ("index.md", "role.md", "instructions.md", "capabilities.md", "constraints.md", "log.md"):
            destination = f"/.ava/base/roles/project-task-manager/{name}"
            self.assertIn(destination, payloads)
            self.assertEqual(payloads[destination].ownership, "ava-managed")
            self.assertEqual(payloads[destination].operation, "replace-managed")

    def test_default_config_is_local_non_committing_and_has_terminal_statuses(self) -> None:
        config = (SOURCE_ROOT / "templates/project-scaffolds/backlog.config.yml").read_text()
        self.assertIn("backlog_directory: backlog", config)
        self.assertIn('statuses: ["To Do", "In Progress", "Won\'t Fix", "Done"]', config)
        self.assertIn("remote_operations: false", config)
        self.assertIn("auto_commit: false", config)
        self.assertIn('task_prefix: "task"', config)

    def test_role_uses_backlog_for_next_task_and_preserves_direct_edits(self) -> None:
        instructions = (SOURCE_ROOT / "templates/base/roles/project-task-manager/instructions.md").read_text()
        contract = (SOURCE_ROOT / "templates/base/shared/instructions/project-task-board.md").read_text()
        registry = (SOURCE_ROOT / "templates/base/roles/index.md").read_text()
        self.assertIn("backlog instructions overview", instructions)
        self.assertIn('task list --status "To Do" --ready --sort ordinal --limit 1 --json', instructions)
        self.assertIn("project-defined actionable status", instructions)
        self.assertIn("follow that configuration rather than imposing the defaults", contract)
        self.assertIn("Direct Markdown editing remains valid and authoritative", instructions)
        self.assertIn("Project Task Manager", registry)

    def test_internal_maintainer_uses_same_canonical_next_task_query(self) -> None:
        instructions = (SOURCE_ROOT / "internal/roles/ava-internal/instructions.md").read_text()
        roadmap = (SOURCE_ROOT / "internal/todo/index.md").read_text()
        task_index = (SOURCE_ROOT / "internal/todo/tasks/index.md").read_text()
        query = 'backlog task list --status "To Do" --ready --sort ordinal --limit 1 --json'
        self.assertIn(query, instructions)
        self.assertIn(query, roadmap)
        self.assertIn("/internal/todo/completed/", instructions)
        self.assertIn("`completed/` is the canonical location", roadmap)
        self.assertIn("canonical finished-task location", task_index)
        self.assertNotIn("leave the task in `/internal/todo/tasks/`", instructions)


if __name__ == "__main__":
    unittest.main()
