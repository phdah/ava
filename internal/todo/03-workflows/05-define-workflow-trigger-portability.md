---
type: Internal Development Task
title: Define Workflow Trigger Portability
description: Define portable trigger metadata while keeping scheduler configuration outside Ava.
tags: [internal, roadmap, workflows, triggers]
status: in-progress
phase: 3
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Define Workflow Trigger Portability

This is the current next task. Complete it before workflow lifecycle ownership and before returning to Phase 4 installer implementation.

## Implemented proposal

The draft implementation adds [Workflow triggers](../../../templates/base/shared/instructions/workflow-triggers.md) as an authoritative distributed shared instruction.

It defines:

- optional `triggers` workflow metadata
- `manual`, `schedule`, and `event` trigger kinds
- a required human-readable description for each trigger
- registry-based discovery by external executors
- structural validation of portable trigger intent
- executor ownership of concrete schedules, event filters, secrets, retries, concurrency, and execution history
- normal workflow routing, role, input, approval, authority, and capability checks for externally triggered invocations

## Design decision proposed for approval

Trigger metadata is validated but advisory for execution.

Ava describes portable trigger intent but does not define a portable executor-binding format or operate a scheduler, event source, webhook service, or workflow runtime.

This avoids treating cron, GitHub Actions, ChatGPT tasks, CI systems, and custom agent clients as though they share one executable configuration model.

## Remaining integration before completion

- replace the temporary trigger boundary in `workflow-format.md` with the new contract
- ensure workflow routing links to external trigger discovery where relevant
- add or update validation fixtures when the validator implementation exists
- mark this task and Phase 3 task 5 complete only after the authoritative contracts are internally consistent

## Next task

[Define Workflow Lifecycle Ownership](06-define-workflow-lifecycle-ownership.md).
