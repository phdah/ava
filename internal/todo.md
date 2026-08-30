---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's ordered internal development roadmap and individual task files.
tags: [internal, planning, roadmap, todo]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-30T16:00:00+02:00
---

# Ava Internal To-Do List

This file is the authoritative entry point for answering what Ava development work comes next. It is internal repository context and must never be copied into distributed projects.

Use the [ordered roadmap](todo/index.md) for broad phase navigation. Use the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md) only when the user explicitly resumes work toward `1.0.0`.

## Current roadmap mode

V1 release progression and further alpha dogfooding are intentionally parked by user decision. The dogfood umbrella remains open as historical roadmap state, but it is not the active work queue and must not preempt ordinary implementation work.

The two concrete qualification-infrastructure defects exposed by the `v1.0.0-alpha.15` release are complete: OpenCode temporary-root permission hardening and exact-run qualification session inventory isolation. The reprioritized roadmap now continues with Backlog.md integration.

## Official next action

**Implement [Evaluate and implement Backlog.md for internal todos](todo/06-backlog-md/01-evaluate-and-implement-backlog-md-for-internal-todos.md).**

Then continue in this order:

1. [Evaluate and add a default Backlog.md project task role](todo/06-backlog-md/02-evaluate-and-add-default-project-task-role.md)
2. [Investigate and design durable interaction evidence for manual semantic changes](todo/07-interaction-evidence/01-investigate-and-design-durable-interaction-evidence.md)

After that queue is complete, reassess the roadmap with the user. Do not automatically resume alpha dogfooding, release-candidate preparation, or stable `1.0.0` qualification.

## Qualification hardening status

The alpha.15 release process exposed two root causes, both now resolved:

- qualification and independent-audit OpenCode sessions needed sufficient permission to read Ava-created temporary roots without relying on hidden user-global configuration; this is complete through tracked repository policy plus qualification-owned per-run permission propagation
- qualification session inventory needed exact-run isolation; this is complete through an authoritative before/after new-session boundary, current-run descendant closure, and execution-root validation

No exceptional qualification-state override mechanism was added. The infrastructure failures were removed at their normal execution boundaries.

## V1 release status

Phase 5 remains structurally open. The alpha dogfood umbrella remains pending because the user has not declared dogfooding complete, and the existing V1 release path must be reassessed before it is resumed.

The V1 operator path remains the canonical release procedure when stable-release work resumes, but it is not the source of the current next action.

## Answering "what is next?"

For a status-only question:

1. read this file
2. report the **Official next action**
3. follow the ordered implementation queue above
4. consult the V1 release operator path only if the user explicitly asks to resume release progression
