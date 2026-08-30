# Project Task Manager Update Log

This log records major conceptual and structural changes to the Project Task Manager. It does not replace Git history.

## 2026-08-30

- **First-class task lifecycle role**: Added Project Task Manager as a distinct managed role because cross-cutting task lifecycle, priority, dependency, and history ownership is durable but does not confer ownership of the work described by tasks.
- **Native Backlog.md boundary**: Defined Backlog.md as the default project task interface while keeping task files and configuration project-owned, Git-reviewable, and directly editable in valid native Markdown.
- **Composition and approval**: Separated backlog ownership from execution roles and required explicit approval for destructive cleanup, ambiguous reprioritization, material scope changes, and new architectural or product decisions.
