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
  at: 2026-07-30T15:26:00Z
---

# Define Distribution and Ownership Boundary

## Architecture constraints

- Ava uses exactly two ownership classes: Ava-managed and project-owned.
- The root `AGENTS.md`, manifests, release guidance, and every installed bootstrap file are Ava-managed.
- Project-specific customization must live in project-owned paths referenced by managed instructions.
- There is no third generated-integration-shim ownership class.

## Decide

- the exact installed ownership boundary for Ava as a versioned context distribution
- the installed path layout for base instructions, default roles, default workflows, manifests, and project context
- which managed files may be customized, or whether managed-file customization is prohibited
- how local modifications to managed files are detected and reported
- how the managed root `AGENTS.md` discovers Ava-managed and project-owned instructions
- whether existing `templates/base/` paths can become the installed layout or require migration
- which previous MCP, CLI, provider, and application-service concepts are removed from the public architecture

## Constraints

- project-owned content must never be overwritten merely because a new base release exists
- managed bootstrap files must not mix project-specific content into their ownership boundary
- the ownership model must remain understandable through normal files and Git diffs
- internal repository instructions must never enter the distributed bundle
- incompatible public path changes require separate user approval

## Completion criteria

- document the two accepted ownership classes and exact path boundaries
- define the stable bootstrap and manifest locations
- define the root `AGENTS.md` as Ava-managed and the supported project-customization path
- identify any required migration from the current template layout
- align the README, template index, metadata contract, and upgrade roadmap
- obtain user approval before applying incompatible public path changes