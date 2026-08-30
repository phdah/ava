---
type: Internal Development Plan
title: Ava Internal To-Do List
description: Stable entry point for Ava's Backlog.md-managed internal development roadmap.
tags: [internal, planning, roadmap, todo, backlog-md]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-30T16:17:00+02:00
---

# Ava Internal To-Do List

This file is the stable entry point for Ava's internal roadmap. Current task state is authoritative in the native Backlog.md project at [`internal/todo/`](todo/index.md), not in the retained legacy phase status fields.

## Official next action

**Implement `AVA-602`, Evaluate and add a default Backlog.md project task role.**

Then implement `AVA-701`, Investigate and design durable interaction evidence for manual semantic changes.

V1 release progression and further alpha dogfooding remain parked. Do not resume them without explicit user direction.

## Board

```sh
backlog task list --json
backlog board
backlog browser
```

The integration is validated against Backlog.md `1.50.1`. `backlog.config.yml` keeps the Backlog root under `internal/todo`, disables remote operations, and leaves automatic commits off.

For a status-only question, read this file and the native Backlog task state. Consult the retained Phase 5 operator path only when the user explicitly asks to resume release progression.
