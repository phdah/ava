# Ava Internal Roadmap

`internal/todo/` is Ava's repository-internal Backlog.md project. Native Backlog.md files are the only roadmap and task lifecycle source.

The integration is pinned and validated against Backlog.md `1.50.1`. The repository-root `backlog.config.yml` points Backlog.md at this directory, uses task prefix `ava`, disables remote operations, and disables automatic commits.

## Native layout

- `tasks/` contains every task record, regardless of lifecycle state.
- `tasks/index.md` explains the directory but is not a task record.
- `milestones/` contains native Backlog.md milestone records. Update next-up roadmap tasks toward the active milestone by assigning the milestone through Backlog.md commands.
- `validate.py` enforces Ava-specific inventory, dependency, status, milestone, and release-tracking invariants.

Ava intentionally does not use Backlog.md's optional `completed/` cleanup directory. `Done` tasks remain in `tasks/` with their history and completion evidence intact.

The former numbered phase directories and `/internal/todo.md` were removed after their task specifications, roadmap context, and completion evidence were migrated into the native task records. Do not recreate a second phase, queue, or status hierarchy.

## Status model

- `To Do`: executable work when its dependencies are satisfied.
- `In Progress`: currently being implemented.
- `Parked`: valid work intentionally excluded from execution until explicitly resumed.
- `Won't Fix`: intentionally closed work that should not be implemented.
- `Done`: implementation is complete.

## Selecting work

Do not maintain or infer a current queue in this index. Ask Backlog.md for the next executable task whenever work must be selected.

If Backlog.md is installed:

```sh
backlog instructions overview
backlog task list --status "To Do" --ready --sort ordinal --limit 1 --json
```

Without a global install, use the pinned package:

```sh
npx -y backlog.md@1.50.1 instructions overview
npx -y backlog.md@1.50.1 task list --status "To Do" --ready --sort ordinal --limit 1 --json
```

The task returned by that query is the next internal roadmap task. `--ready` excludes tasks with unsatisfied dependencies, `--sort ordinal` uses the task's explicit Backlog.md order, and `--limit 1` returns only the next candidate. Task IDs and filenames are not roadmap ordering mechanisms.

If the query returns no task, there is no currently executable internal roadmap task. Do not substitute a `Parked`, `Won't Fix`, `Done`, or already `In Progress` task based on historical prose or task numbering.

Read the complete returned task before planning or modifying the repository. For interactive inspection, `backlog board` and `backlog browser` remain available. `backlog browser` serves only on the local machine (`127.0.0.1`, default port `6420`).

## Maintainer workflow

When selecting, planning, executing, or completing an internal roadmap task, use Backlog.md's native workflow rather than reconstructing state from prose.

- One bounded task is the normal unit of implementation and PR scope.
- Read the complete selected task before planning implementation.
- Treat `Parked` as intentionally excluded until the user explicitly resumes it.
- Treat `Won't Fix` as closed by decision and do not execute it unless its status is explicitly changed.
- Put new scope, acceptance criteria, implementation notes, and completion evidence directly in the native task rather than creating a parallel planning document.
- Prefer Backlog.md commands for lifecycle and task metadata changes. Direct Markdown edits are allowed when required by repository work but must preserve Backlog.md's native task shape.
- Complete, reopen, or reprioritize through native task state and commit the resulting Markdown normally.
- Leave `Done` tasks in `tasks/`. Do not run `backlog cleanup` for the Ava internal roadmap.

After roadmap changes, run:

```sh
python3 internal/todo/validate.py
```

## Adding work

New internal roadmap work must be a native Backlog.md task under `internal/todo/tasks/`. Use Backlog.md's task creation and editing workflow and preserve dependencies, labels, acceptance criteria, and task history in the card itself.

Keep this project repository-internal. Nothing under `internal/` belongs in distributed Ava templates or installed user projects.
