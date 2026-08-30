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
            "/backlog/tasks/.gitkeep",
            "/backlog/completed/.gitkeep",
        }

        self.assertTrue(expected.issubset(payloads))
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

    def test_default_config_is_local_and_non_committing(self) -> None:
        config = (SOURCE_ROOT / "templates/project-scaffolds/backlog.config.yml").read_text()
        self.assertIn("backlog_directory: backlog", config)
        self.assertIn('statuses: ["To Do", "In Progress", "Done"]', config)
        self.assertIn("remote_operations: false", config)
        self.assertIn("auto_commit: false", config)
        self.assertIn('task_prefix: "task"', config)

    def test_role_loads_current_backlog_guidance_and_preserves_direct_edits(self) -> None:
        instructions = (SOURCE_ROOT / "templates/base/roles/project-task-manager/instructions.md").read_text()
        registry = (SOURCE_ROOT / "templates/base/roles/index.md").read_text()
        self.assertIn("backlog instructions overview", instructions)
        self.assertIn("Direct Markdown editing remains valid and authoritative", instructions)
        self.assertIn("Project Task Manager", registry)


if __name__ == "__main__":
    unittest.main()
