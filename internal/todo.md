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
  at: 2026-08-30T14:00:00+02:00
---

# Ava Internal To-Do List

This file is the authoritative entry point for answering what Ava development work comes next. It is internal repository context and must never be copied into distributed projects.

Use the [ordered roadmap](todo/index.md) for broad phase navigation. Use the [V1 release operator path](todo/05-release-qualification/v1-release-operator-path.md) only when the user explicitly resumes work toward `1.0.0`.

## Current roadmap mode

V1 release progression and further alpha dogfooding are intentionally parked by user decision. The dogfood umbrella remains open as historical roadmap state, but it is not the active work queue and must not preempt ordinary implementation work.

The `v1.0.0-alpha.15` release exposed two concrete qualification-infrastructure defects. Those defects are now ordinary bounded implementation tasks rather than additional dogfood findings.

## Official next action

**Implement [Harden Qualification OpenCode Permissions](todo/05-release-qualification/04d-harden-qualification-opencode-permissions.md).**

Then continue in this order:

1. [Isolate Qualification Session Inventory](todo/05-release-qualification/04e-isolate-qualification-session-inventory.md)
2. [Evaluate and implement Backlog.md for internal todos](todo/06-backlog-md/01-evaluate-and-implement-backlog-md-for-internal-todos.md)
3. [Evaluate and add a default Backlog.md project task role](todo/06-backlog-md/02-evaluate-and-add-default-project-task-role.md)
4. [Investigate and design durable interaction evidence for manual semantic changes](todo/07-interaction-evidence/01-investigate-and-design-durable-interaction-evidence.md)

After that queue is complete, reassess the roadmap with the user. Do not automatically resume alpha dogfooding, release-candidate preparation, or stable `1.0.0` qualification.

## Qualification hardening scope

The next two tasks address root causes observed during the alpha.15 release process:

- qualification and independent-audit OpenCode sessions must receive sufficient permission to read Ava-created temporary roots without relying on hidden user-global configuration
- qualification session inventory must be exact-run isolated and must not absorb historical OpenCode sessions from earlier qualification runs

Do not add an exceptional qualification-state override mechanism as part of these tasks. The current direction is to remove the infrastructure failures rather than design recovery around them.

## V1 release status

Phase 5 remains structurally open. The alpha dogfood umbrella remains pending because the user has not declared dogfooding complete, and the existing V1 release path must be reassessed before it is resumed.

The V1 operator path remains the canonical release procedure when stable-release work resumes, but it is not the source of the current next action.

## Answering "what is next?"

For a status-only question:

1. read this file
2. report the **Official next action**
3. follow the ordered implementation queue above
4. consult the V1 release operator path only if the user explicitly asks to resume release progression
