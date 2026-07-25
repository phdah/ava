---
type: Internal Development Task
title: Define Coherent Change Planning
description: Define provider-independent grouped change sets for dry-run and safe client execution.
tags: [internal, roadmap, changes, planning]
status: pending
phase: 5
order: 5
timestamp: 2026-07-25T00:00:00Z
---

# Define Coherent Change Planning

Ava should be able to return a provider-independent change set when it cannot apply changes directly.

## Candidate change operations

```text
create
replace
move
delete
append
```

Each operation should include:

- target path
- expected version when applicable
- complete or patch content
- rationale
- validation effects
- whether user approval is required

## Completion criteria

- define the change-set schema
- support dry-run output
- preserve grouped logical changes
- allow a client with GitHub MCP tools to execute the plan safely
- define post-application validation
