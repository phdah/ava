# Ava Internal Roadmap

`internal/todo/` is Ava's repository-internal Backlog.md project. The live lifecycle state is stored only in native Backlog.md task files under `tasks/` and `completed/`.

The integration is evaluated against Backlog.md `1.50.1`. The repository root `backlog.config.yml` selects this directory and disables Backlog.md remote operations and automatic commits.

## Status model

- `To Do`: executable work in the active ordered queue.
- `In Progress`: currently being implemented.
- `Parked`: valid work intentionally excluded from the active queue.
- `Done`: implementation is complete. Done cards may remain in `tasks/` until cleanup moves them to `completed/`.

The legacy phase directories `01-*` through `07-*` retain the full pre-Backlog task specifications, rationale, and completion evidence. Their frontmatter statuses and status tables are frozen historical snapshots. They must not be updated as lifecycle state and are not current status sources.

## Current queue

1. `AVA-602` - Evaluate and add a default Backlog.md project task role.
2. `AVA-701` - Investigate and design durable interaction evidence for manual semantic changes.

Phase 5 release progression and alpha dogfooding remain `Parked` until the user explicitly resumes them. The dogfood umbrella remains open in its retained specification, but that does not make it active board work.

## Use

```sh
backlog task list --json
backlog board
backlog browser
```

`backlog browser` serves the local UI on `127.0.0.1:6420` by default. Backlog.md `1.50.1` is the validated version for this repository.

Prefer Backlog.md CLI, TUI, or web operations for lifecycle changes. Direct Markdown edits are also valid when they preserve the native frontmatter shape and pass:

```sh
python3 internal/todo/validate.py
```

Run `backlog cleanup` when Done cards should move from `tasks/` into `completed/`. A recently completed card may remain in `tasks/`, which keeps it directly reopenable through the normal Backlog status edit flow before cleanup. Archived historical cards remain durable completion evidence.

## Ordering and dependencies

Task IDs preserve the former phase and task grouping. The active cross-phase queue is also encoded as native dependencies:

```text
AVA-601 -> AVA-602 -> AVA-701
```

Do not infer active work from a retained phase index. Ask Backlog.md or read the native task files.

## Retained specifications

The pre-Backlog hierarchy remains available for detailed scope and history:

1. [Format contract and base structure](01-format-contract/)
2. [Core roles for initialized projects](02-core-roles/)
3. [Workflow system](03-workflows/)
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/)
5. [V1 release qualification](05-release-qualification/)
6. [Backlog.md integration](06-backlog-md/)
7. [Durable interaction evidence](07-interaction-evidence/)

These indexes are navigation and historical evidence only. Backlog.md owns current status, ordering, dependencies, labels, and completed-task handling.

## Adding work

New internal work must be a native Backlog.md task. Put detailed scope directly in the Backlog task for new work. The retained phase files exist only for the one-time migration of pre-Backlog history and must not become a second mutable status system.

Keep all of this repository-internal. Nothing under `internal/` belongs in distributed Ava templates or installed projects.
