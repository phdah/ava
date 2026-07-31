# Internal Update Log

This log records major conceptual and structural changes to Ava's internal development instructions. It does not replace Git history.

## 2026-07-31

* **Deprecated roadmap removal**: Removed the superseded workspace-provider, semantic-tool, application-service, MCP, CLI, and application-specific compatibility task directories from the executable roadmap hierarchy.
* **Requirement preservation**: Moved the remaining valid requirements into the active installer and validation tasks, including safe path resolution, traversal and symlink protection, atomic grouped changes, dry-run and pre/post validation, stable machine-readable findings, structural conformance rules, deterministic repair boundaries, and compatibility fixtures.
* **Historical boundary**: Kept the architecture pivot and removed planning available through this log and Git history rather than as misleading unchecked tasks.

## 2026-07-30

* **Distribution-first roadmap**: Replaced the active application-centric implementation direction with a versioned distribution and upgrade phase covering ownership, SemVer, GitHub Release assets, deterministic migrations, agent-readable upgrade guidance, a thin installer and updater, validation, and the first published release.
* **Superseded phases**: Marked workspace providers, semantic MCP tools, shared Go services, MCP implementation, companion CLI, and their application-specific compatibility plan as superseded historical planning rather than executable tasks.
* **Version and ownership model**: Limited the architecture to two ownership classes, made the root `AGENTS.md` Ava-managed, defined `ava_version` as installed-base state only, and required separate semantic compatibility state.
* **Bootstrap trust boundary**: Required the release roadmap to distinguish convenient bootstrap execution from a separately verified download-first flow. Checksums alone are not treated as independent bootstrap authentication.
* **Authoritative terminology alignment**: Updated internal maintainer scope and generated project instructions to depend on host-agent tools and repository access rather than a required workspace-provider or MCP layer.
* **Workflow dependency update**: Deferred the remaining workflow catalog and lifecycle tasks until the distribution ownership and migration contracts are settled, and removed their dependency on planned semantic MCP tools.
* **Next task**: Set the managed versus project-owned distribution boundary as the next architectural task.

## 2026-07-26

* **Index maintenance**: Required Ava Internal Maintainers to keep each `index.md` limited to direct children and delegate descendant discovery to child indexes.

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