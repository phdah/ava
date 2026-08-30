---
id: ava-302
title: "Define the workflow registry and routing contract"
status: "Done"
labels: ["internal", "roadmap", "phase-03"]
ordinal: 302
---

## Description

Define deterministic workflow discovery, role resolution, precedence, and deprecation behavior. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Define the Workflow Registry and Routing Contract
description: Define deterministic workflow discovery, role resolution, precedence, and deprecation behavior.
tags: [internal, roadmap, workflows, routing]
status: completed
phase: 3
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-07-28T10:32:00Z
---

# Define the Workflow Registry and Routing Contract

## Completed outcome

The public [workflow registry and routing contract](/templates/base/shared/instructions/workflow-routing.md) now defines:

- `/workflows/index.md` as the canonical registry root
- registry membership through progressive direct-child index discovery
- workflow path as the stable identity without a separate identifier or registry format
- explicit invocation by canonical path or unambiguous lowercase kebab-case filename stem
- workflow titles as descriptive metadata rather than stable invocation identifiers
- explicit workflow invocation taking precedence over free-form semantic role selection
- no semantic inference of workflows from ordinary requests
- blocking behavior for unresolved, ambiguous, unregistered, invalid, or deprecated workflows
- no fallback to free-form role selection after a failed workflow invocation
- exact resolution of one registered, non-deprecated `primary_role`
- required input and required-context resolution before execution
- advisory `replaced_by` metadata without automatic workflow or role redirection
- migration behavior for moved, renamed, deprecated, and removed workflows
- deterministic errors, warnings, and semantic blocking findings

The generated router, workflow registry, workflow format, metadata contract, and instruction-resolution contract now reference the same authoritative routing behavior.

## Core routing decisions

- Workflows remain Markdown-native and path-identified.
- A workflow must be explicitly invoked; Ava does not guess one from semantic similarity.
- Explicit workflow routing activates the workflow's declared role and bypasses free-form role selection.
- Routing failures stop execution rather than silently selecting another route.
- Deprecated workflows and roles are never followed automatically through `replaced_by`.

## Completion criteria

- [x] choose the registry format and location
- [x] define router behavior for interactive and workflow-driven requests
- [x] update generated `AGENTS.md`
- [x] validate workflow links and role references
- [x] define deprecation and migration behavior