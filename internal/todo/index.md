# Ava Internal Roadmap

`internal/todo/` is Ava's repository-internal Backlog.md project. Native Backlog.md files are the only roadmap/task lifecycle source.

The integration is pinned and validated against Backlog.md `1.50.1`. The repository-root `backlog.config.yml` points Backlog.md at this directory, uses task prefix `ava`, disables remote operations, and disables automatic commits.

## Native layout

- `tasks/` contains current, parked, won't-fix, and reopenable task records.
- `completed/` contains completed historical task records after cleanup/archive.
- `validate.py` enforces Ava-specific migration, dependency, queue, and release-parking invariants.

The former numbered phase directories and `/internal/todo.md` were removed after their task specifications, roadmap context, and completion evidence were migrated into the native task records. Do not recreate a second phase/status hierarchy.

## Status model

- `To Do`: executable work in the active ordered queue.
- `In Progress`: currently being implemented.
- `Parked`: valid work intentionally excluded from the active queue.
- `Won't Fix`: intentionally closed work that should not be implemented.
- `Done`: implementation is complete.

## Current queue

1. `AVA-701` - Investigate and design durable interaction evidence for manual semantic changes.

`AVA-601` and `AVA-602` are complete and cleaned into `completed/`.

Phase 5 release progression, alpha dogfooding, the synthetic qualification completion gate, corrective-alpha work, RC work, stable-release work, and post-v1 Finding 25 remain `Parked` until the user explicitly resumes them.

## Maintainer workflow

When selecting, planning, executing, or completing an internal roadmap task, use Backlog.md's native workflow rather than reconstructing state from prose.

If Backlog.md is installed:

```sh
backlog instructions overview
backlog task list --json
backlog task <id> --json
backlog board
backlog browser
```

Without a global install, use the pinned package:

```sh
npx -y backlog.md@1.50.1 instructions overview
npx -y backlog.md@1.50.1 task list --json
npx -y backlog.md@1.50.1 task <id> --json
npx -y backlog.md@1.50.1 board
npx -y backlog.md@1.50.1 browser --no-open
```

`backlog browser` serves only on the local machine (`127.0.0.1`, default port `6420`).

Prefer Backlog.md commands for task creation and lifecycle changes so native field handling remains canonical. Direct Markdown edits are allowed when required by repository work, but they must preserve Backlog.md's native task shape and pass:

```sh
python3 internal/todo/validate.py
```

Use `backlog cleanup` when completed tasks should move from `tasks/` to `completed/`.

## Task execution rules

- One bounded task is the normal unit of implementation and PR scope.
- Read the selected native task itself before planning implementation.
- Respect native `dependencies` before starting dependent work.
- Treat `Parked` as intentionally excluded from the active queue, not merely lower priority.
- Treat `Won't Fix` as closed by decision and do not execute it unless its status is explicitly changed.
- Put new scope, acceptance criteria, implementation notes, and completion evidence directly in the native task rather than creating a parallel planning document.
- Complete/reopen/reprioritize through Backlog.md state, then commit the resulting Markdown changes normally.
- Historical completion evidence belongs in completed task records and must remain durable.

The active cross-phase ordering at migration is:

```text
AVA-601 -> AVA-602 -> AVA-701
```

Do not infer a different current task from historical narrative embedded in completed or parked cards.

## Adding work

New internal roadmap work must be a native Backlog.md task under this project. Use Backlog.md's task creation/editing workflow and preserve dependencies, labels, acceptance criteria, and task history in the card itself.

Keep this project repository-internal. Nothing under `internal/` belongs in distributed Ava templates or installed user projects.
