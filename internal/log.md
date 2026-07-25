# Internal Update Log

This log records major conceptual and structural changes to Ava's internal development instructions. It does not replace Git history.

## 2026-07-25

* **Roadmap hierarchy**: Replaced the monolithic task definitions in `internal/todo.md` with a stable bootstrap, an ordered roadmap index, numbered phase indexes, and one file per task.
* **Task execution**: Added explicit phase and task ordering, a current next-task link, and per-task status while preserving the original roadmap scope and completion state.
* **Git workflow delegation**: Removed Git and GitHub operation rules from the Ava Internal Maintainer role so active repository tooling controls commits, branches, pull requests, issues, reviews, merges, and history inspection.

## 2026-07-24

* **Roadmap structure**: Expanded `internal/todo.md` from a role list into the detailed Ava implementation roadmap.
* **Core roles**: Replaced overlapping proposed roles with a four-role direction while preserving distinct procedures as workflows.
* **Workflow planning**: Added tasks for workflow format, routing, registry, trigger portability, and built-in workflow prompts.
* **Provider planning**: Added workspace-provider and GitHub integration tasks so repository access remains backend-independent.
* **Implementation planning**: Added semantic MCP tools, change planning, validation, Go services, CLI, testing, compatibility, and migration work.

## 2026-07-23

* **Conformance**: Established the repository root as an Open Knowledge Format version 0.1 bundle with root navigation and concept metadata.
* **Initialization**: Established the internal development hierarchy.
* **Creation**: Added the Ava Internal Maintainer role for repository-specific development work.
* **Boundary**: Defined internal role instructions as separate from all user-generated Ava platforms.
