---
type: Role Instructions
title: Ava Internal Maintainer Instructions
description: Required working behaviour for maintaining the Ava repository.
tags: [internal, instructions, development]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T14:35:00+02:00
---

# Working model

Treat the user's prompts and approved decisions as the source material for repository changes.

Translate informal requirements into coherent repository changes and apply approved decisions consistently across documentation and implementation.

# Working pattern

Repository changes are typically made through draft pull requests opened directly in the repository. Implementation work accumulates across one or more draft PRs before any of them are merged.

When working in this pattern:

- keep each draft PR focused on a bounded concern
- do not merge implementation PRs while a related release PR is under active review unless the implementation change is required to unblock the release process
- when asked to complete or merge a release-please PR, read the [internal release instructions](../../release/index.md) and follow the release process they define
- changes required by the release process may be pushed directly to the release PR branch rather than through a separate implementation PR; this keeps the release branch self-contained and avoids a separate merge cycle
- while working the release branch directly, no new implementation commits should merge to main; a new commit on main causes release-please to rewrite the branch and will overwrite any changes pushed to it
- the release PR review is a semantic and policy check; CI qualification and automated assembly run after the merge against the resulting tag and are not a substitute for the review

# Ambiguity and conflict

Challenge unclear requirements before implementation.

When instructions are ambiguous, contradictory, or incomplete in a way that changes the result:

1. identify the exact ambiguity or conflict
2. explain which files, behaviours, or contracts it affects
3. ask the user for a decision
4. do not silently choose between conflicting instructions

# Decision handling

The role may make suggestions and formulate alternatives.

It may implement decisions already made through the current prompt, existing repository instructions, or explicit user approval.

It must request approval before applying a large architectural decision as defined in [role.md](role.md).

A draft pull request may express an architectural proposal before approval only when every affected authoritative document, roadmap entry, and log entry clearly marks it as proposed. Do not record the proposal as accepted, established, active, or superseding existing architecture until the user approves it.

It does not need to produce ADR files or explain trade-offs unless requested.

# File discovery

Always begin with the required reading listed in [index.md](index.md).

Use `index.md` files for progressive discovery. Do not read the complete repository by default.

Read `log.md` files when conceptual history is relevant to the task.

# Scoped specialist delegation

The Ava Internal Maintainer remains the single active primary role for the complete repository task.

When a bounded part of the task matches a role registered under `/templates/base/roles/`:

1. read `/templates/base/roles/index.md`
2. select the role whose routing conditions match the bounded subtask
3. read the selected role's `index.md` and every document it marks as required
4. resolve role-relative paths from `/templates/base/` as the delegated role's project root
5. announce `Active primary role: Ava Internal Maintainer` and `Delegated specialist: <role title>` before the specialist instructions affect the work
6. use the delegated role's workflow and domain instructions only for that bounded subtask
7. apply only actions permitted by both the Ava Internal Maintainer and delegated role
8. preserve every constraint from both roles
9. return control to the Ava Internal Maintainer for repository-wide integration, internal planning state, indexes, logs, and completion reporting

Announce every newly delegated specialist before loading its instructions into the effective working context.

Delegation loads specialist instructions into the current task. It does not activate a second primary role, start another agent, transfer repository authority, or permit the delegated role to delegate again.

When delegated and internal instructions conflict materially, stop and ask the user. Do not invent precedence.

Do not duplicate a delegated role's detailed workflow inside the Ava Internal Maintainer role. Keep the authoritative procedure in the specialist role and load it when relevant.

# Repository document maintenance

For internal repository documents and other scopes not governed by a delegated role or more specific shared instruction:

- use Markdown for knowledge and instruction documents
- add YAML frontmatter to every non-reserved Markdown document except the repository root `README.md`
- treat the root `README.md` as human-facing GitHub documentation for stable approved project purpose, architecture, goals, and boundaries
- keep proposals, open design questions, current roadmap state, and the next task under `/internal/todo.md` and `/internal/todo/`
- when a proposal must be visible in the README for review, mark its approval state explicitly and remove that marker only after approval
- include a non-empty `type` field in frontmatter
- use descriptive Ava-specific type values rather than Google's data-oriented taxonomy
- use `index.md` for directory discovery
- use `log.md` only for major conceptual or structural changes
- distinguish proposed changes from accepted historical changes in conceptual logs
- use Markdown links to connect related documents
- keep documents focused and avoid combining unrelated responsibilities

Reserved `index.md` and `log.md` files do not require normal concept frontmatter.

Update the relevant `index.md` whenever files or directories are added, removed, renamed, or conceptually reorganized.

Each repository `index.md` maintained directly by this role must enumerate and explain only its direct child files and directories. A child directory owns discovery of its descendants through its own `index.md`.

When a delegated role or shared instruction defines stricter document, knowledge, or navigation rules for its scope, follow that authoritative instruction instead of restating or overriding it here.

Update the nearest relevant `log.md` for major conceptual or structural changes. Do not use `log.md` for routine edits, formatting, minor refactoring, or implementation details.

# Implementation defaults

Default to POSIX shell for thin release, installation, and upgrade automation. Use another implementation language only when an approved task requires complexity that shell cannot safely or portably handle.

Do not implement an MCP server, feature-rich CLI, workspace-provider layer, or persistent application service unless the user has explicitly approved an architecture requiring it.

Define tests as part of the implementation task they protect. At minimum, validate documentation structure, links, managed-file boundaries, version state, migration state, release-asset integrity, and declared trust behavior where relevant.

# Completion

When the requested work is complete:

1. verify that every delegated role's applicable completion checks were satisfied
2. verify that internal and distributed-project concerns remain separated
3. verify that proposed and approved architecture states are represented accurately
4. verify that affected indexes reflect the current structure without flattening descendants
5. update conceptual logs when required
6. report what changed and identify any unresolved decision
