---
type: Internal Development Task
title: Define Distribution and Ownership Boundary
description: Define Ava as a file distribution and separate Ava-managed base content from project-owned context.
tags: [internal, roadmap, distribution, ownership]
status: pending
phase: 4
order: 1
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T11:26:00Z
---

# Define Distribution and Ownership Boundary

## Decide

- the exact public product boundary for Ava as a versioned context distribution
- which files are Ava-managed, project-owned, or generated integration shims
- the installed path layout for base instructions, default roles, default workflows, manifests, and project context
- which managed files may be customized and how local modifications are detected
- how the root `AGENTS.md` loads Ava-managed and project-owned instructions
- whether existing `templates/base/` paths can become the installed layout or require migration
- which previous MCP, CLI, provider, and application-service concepts are removed from the public architecture

## Constraints

- preserve the current generated-project instruction behavior unless an explicit follow-up task changes it
- project-owned content must never be overwritten merely because a new base release exists
- the ownership model must remain understandable through normal files and Git diffs
- internal repository instructions must never enter the distributed bundle

## Completion criteria

- document the accepted ownership classes and exact path boundaries
- define the stable bootstrap and manifest locations
- identify any required migration from the current template layout
- align the README, template index, metadata contract, and upgrade roadmap
- obtain user approval before applying incompatible public path changes
