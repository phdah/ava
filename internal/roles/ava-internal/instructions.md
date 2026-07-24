---
type: Role Instructions
title: Ava Internal Maintainer Instructions
description: Required working behaviour for maintaining the Ava repository.
tags: [internal, instructions, development]
timestamp: 2026-07-23T00:00:00Z
---

# Working model

Treat the user's prompts and approved decisions as the source material for repository changes.

Translate informal requirements into small, structured, linked documents that can later serve as the basis for Ava-generated roles and agent context.

Apply approved decisions consistently across documentation and implementation.

# Ambiguity and conflict

Challenge unclear requirements before implementation.

When instructions are ambiguous, contradictory, or incomplete in a way that changes the result:

1. identify the exact ambiguity or conflict
2. explain which files, behaviours, or contracts it affects
3. ask the user for a decision
4. do not silently choose between conflicting instructions

All future Ava-generated roles should follow the same principle: agents need a clear instruction path and must surface unresolved conflicts to the user.

# Decision handling

The role may make suggestions and formulate alternatives.

It may implement decisions already made through the current prompt, existing repository instructions, or explicit user approval.

It must request approval before applying a large architectural decision as defined in [role.md](role.md).

It does not need to produce ADR files or explain trade-offs unless requested.

# File discovery

Always begin with the required reading listed in [index.md](index.md).

Use `index.md` files for progressive discovery. Do not read the complete repository by default.

Recent commits and `log.md` files are not mandatory reading before routine work. Read logs when conceptual history is relevant to the task.

# Structured documents

Follow OKF-compatible conventions:

- use Markdown for knowledge and instruction documents
- add YAML frontmatter to every non-reserved Markdown document
- include a non-empty `type` field in frontmatter
- use descriptive Ava-specific type values rather than Google's data-oriented taxonomy
- use `index.md` for directory discovery
- use `log.md` only for major conceptual or structural changes
- use Markdown links to connect related documents
- keep documents focused and avoid combining unrelated responsibilities

Reserved `index.md` and `log.md` files do not require normal concept frontmatter.

# Index and log maintenance

Update the relevant `index.md` whenever files or directories are added, removed, renamed, or conceptually reorganized.

Update the nearest relevant `log.md` for major changes such as:

- a new role or major role redesign
- a change to the platform hierarchy
- a new format rule
- a changed architectural boundary
- a deprecation or migration decision

Do not use `log.md` for routine edits, formatting, minor refactoring, or implementation details already captured by Git.

# Implementation defaults

Default to Go for application code and Bash for shell automation when appropriate.

No MCP protocol implementation is required until the repository design reaches that phase.

Testing requirements should be defined when MCP or CLI implementation begins. Until then, validate documentation structure and links where practical.

# Git workflow

Modify files directly on the current default branch.

Complete all repository changes requested in the current session. Do not leave requested work unfinished merely to preserve a single atomic commit.

Create one or more commits as needed. Each commit must contain a coherent completed change. A single user request may produce multiple commits when it contains multiple coherent changes or the active repository tooling writes changes separately.

Do not create or manage:

- branches
- pull requests
- GitHub issues
- review workflows

Do not inspect Git history unless the task requires it.

# Completion

When the requested work is complete:

1. verify that internal and generated-platform concerns remain separated
2. verify that indexes reflect the current structure
3. update conceptual logs when required
4. commit every completed change produced by the request
5. report what changed and identify any unresolved decision
