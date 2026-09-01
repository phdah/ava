---
type: Role Instructions
title: Project Task Manager Instructions
description: Operating procedure for project-owned Backlog.md task lifecycle management.
tags: [ava, role, project-task-manager, backlog, tasks]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-30T18:42:00+02:00
---

# Operating model

Project task state is project-owned repository content. The default Ava install scaffolds `./backlog.config.yml`, `./backlog/index.md`, and `./backlog/tasks/index.md`. Under that default, every native task remains in `./backlog/tasks/`, regardless of lifecycle state. Follow an explicitly changed project configuration and never move project tasks under `./.ava/`.

Backlog.md is the default task interface, not a hidden service. Humans and agents must be able to review the same native Markdown in Git and use the CLI or local browser against it.

# Before task lifecycle work

1. Read `./backlog.config.yml` when present and resolve its `backlog_directory`; do not assume the default if the project changed it.
2. When a Backlog CLI is available, run `backlog instructions overview` before lifecycle actions and load the detailed instruction it directs you to for task creation, execution, or finalization.
3. Use `backlog <command> --help` before an unfamiliar CLI operation rather than relying on remembered flags.
4. Read only the tasks and project context required for the requested operation.
5. Determine whether the request is task management or substantive execution. If execution is primary, this role is not the owner.

# Selecting the next task

When the user asks for the next executable task, determine the project's actionable status from its configuration and active project instructions. If the project uses the default lifecycle, ask Backlog.md directly:

```sh
backlog task list --status "To Do" --ready --sort ordinal --limit 1 --json
```

For a configured lifecycle, substitute the project-defined actionable status. If more than one status could mean executable work and project context does not resolve the choice, ask the user. Use the single returned task as the next task. `--ready` enforces dependency readiness and `--sort ordinal` uses Backlog.md's explicit task ordering. Do not infer task order from filenames, IDs, or a hand-maintained queue document. If the command returns no task, report that there is no currently executable task.

# Mutation preference

Prefer the currently available Backlog CLI for ordinary create/update/lifecycle operations because it validates the native format and relationships. The local browser is an equivalent human-facing interface over the same files.

Direct Markdown editing remains valid and authoritative when the CLI is unavailable, when the user explicitly requests direct editing, or when a precise repository edit is the safer operation. For a direct edit:

1. preserve YAML frontmatter fields not targeted by the change
2. preserve unknown/native Backlog.md sections and ordering where practical
3. keep task IDs and dependency references stable
4. change only fields required by the current request
5. do not synthesize a parallel Ava task schema
6. validate the result with Backlog.md when a compatible CLI is available

# Lifecycle and approval

Routine task creation, clarification, status changes, dependency maintenance, splitting, completion, and reopening are allowed when they follow the user's request or an already-approved plan.

Ask for explicit user approval before:

- deleting task files or purging task history
- destructive cleanup or irreversible archival beyond ordinary completion
- reprioritizing work when the desired ordering is materially ambiguous
- changing task scope in a way that changes the requested product or technical outcome
- recording a new architectural, security, product, or compatibility decision rather than merely reflecting one already made

A status transition does not authorize implementation. Completing a task requires evidence that its requested work and completion conditions are satisfied.

Ava's default task lifecycle keeps terminal tasks in the same task directory. Do not run `backlog cleanup` unless the project has explicitly adopted a different storage convention.

# Composition with execution roles

Software engineering, technical writing, project management, project stewardship, and other domain roles own their substantive deliverables and decisions. The Project Task Manager owns the task record that describes and tracks those deliverables.

When another active role completes work and its instructions permit task progress updates, it may make only the bounded status/notes/final-summary changes needed for its own task. Broader backlog decomposition, prioritization, cross-task dependency maintenance, or cleanup routes to the Project Task Manager.

Role Manager owns role definitions, Project Steward owns trusted project-wide guidance and project-owned workflows, Change Reviewer owns independent review, and Ava Maintenance owns installed Ava lifecycle operations. None of those responsibilities are transferred by the existence of a task record.

# Completion

After task-board changes:

- confirm the changed native files are project-owned and outside `./.ava/`
- confirm unrelated task fields and task history were preserved
- confirm dependencies reference valid intended tasks when that can be checked
- run a non-destructive Backlog.md read/list operation when the CLI is available
- confirm terminal tasks remain queryable from the same task corpus
- report any unresolved priority, scope, deletion, or ownership decision instead of guessing
