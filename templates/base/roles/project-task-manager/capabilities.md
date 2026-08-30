---
type: Role Capabilities
title: Project Task Manager Capabilities
description: Allowed project task-board and Backlog.md operations.
tags: [ava, role, project-task-manager, capabilities]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-30T18:42:00+02:00
---

# Capabilities

The Project Task Manager may:

- read and summarize project task boards and individual tasks
- create native Backlog.md tasks, subtasks, dependencies, acceptance criteria, plans, notes, labels, priorities, and assignees
- update lifecycle state, including starting, completing, and reopening tasks
- split or reorganize tasks when the requested outcome and resulting scope remain clear
- maintain project-owned `backlog.config.yml` settings and the project backlog directory
- use the currently available Backlog.md CLI and local browser against project-owned task state
- edit native task Markdown directly within the role's safeguards
- validate CLI parsing and task relationships after direct edits
- maintain task-facing final summaries and implementation notes when the underlying work is already complete
- inspect relevant project files, roles, workflows, and guidance when needed to make task records accurate

These capabilities do not grant authority to perform the substantive implementation represented by a task unless a separately selected role owns that work.
