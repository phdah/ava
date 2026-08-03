---
type: Internal Development Task
title: Define Workflow Trigger Portability
description: Define portable trigger metadata while keeping scheduler configuration outside Ava.
tags: [internal, roadmap, workflows, triggers]
status: complete
phase: 3
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T14:15:00+02:00
---

# Define Workflow Trigger Portability

This task is complete.

## Implemented decision

Ava recognizes optional portable workflow trigger metadata for:

- `manual`
- `schedule`
- `event`

Each trigger declaration contains a required trigger kind and non-empty human-readable description.

Trigger metadata is structurally validated but advisory for execution. It describes portable trigger intent without configuring or operating an executor.

Environment-specific configuration remains outside Ava workflow prompts, including cron expressions, time zones, event filters, webhook configuration, credentials, retries, concurrency, delivery guarantees, and execution history.

## Authoritative contracts

The implementation is defined by:

- [Workflow triggers](../../../templates/base/shared/instructions/workflow-triggers.md)
- [Workflow format](../../../templates/base/shared/instructions/workflow-format.md)
- [Workflow registry and routing](../../../templates/base/shared/instructions/workflow-routing.md)

External systems discover trigger-capable workflows through the managed and project-owned workflow registries. They retain the canonical workflow path and perform an explicit invocation through normal upgrade-state, validation, routing, role, input, authority, approval, and capability checks.

Ava does not define a portable executor-binding format or provide a scheduler, event source, webhook service, or workflow runtime.

## Validation coverage

The contracts define valid and invalid trigger examples and classify malformed metadata, embedded executor configuration, duplicate trigger kinds, bypass claims, vague descriptions, and unverifiable bindings.

Executable validator fixtures will be added with the validator implementation rather than creating fixtures for tooling that does not yet exist.

## Next task

[Define Workflow Lifecycle Ownership](06-define-workflow-lifecycle-ownership.md).
