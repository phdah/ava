---
type: Internal Development Task
title: Define Workflow Trigger Portability
description: Define portable trigger metadata while keeping scheduler configuration outside Ava.
tags: [internal, roadmap, workflows, triggers]
status: pending
phase: 3
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Define Workflow Trigger Portability

This is the current next task. Complete it before workflow lifecycle ownership and before returning to Phase 4 installer implementation.

## Proposal for approval

Ava should recognize and structurally validate portable trigger intent, but it should not define executable scheduler or event bindings.

A workflow may declare an optional top-level `triggers` list. Each entry describes one supported way an external executor may choose to invoke the workflow:

```yaml
triggers:
  - kind: manual
    description: Run when a user explicitly requests the workflow.
  - kind: schedule
    description: Run every weekday morning in the project operating timezone.
  - kind: event
    description: Run when a pull request is opened or updated.
```

The declaration is portable because it states intent without embedding executor-specific configuration. Cron expressions, GitHub Actions event syntax, ChatGPT task schedules, CI pipeline configuration, webhook endpoints, credentials, retry policy, concurrency, and environment-specific input binding remain outside Ava workflow files.

Merging an implementation of this proposal would approve the public workflow-format change. Until approval, no authoritative distributed contract should describe these fields as active.

## Recognized trigger metadata

`triggers` is an optional non-empty list of trigger declarations.

Each declaration contains:

- `kind`: required; one of `manual`, `schedule`, or `event`
- `description`: required non-empty string describing the portable invocation intent

No other trigger fields have Ava semantics in the initial contract. Unknown fields must be preserved for forward compatibility but produce a warning because an executor must not assume that Ava validates them.

Duplicate `kind` values are allowed when a workflow has materially different trigger intents of the same category, such as two distinct events. Exact duplicate entries should produce a warning.

## Trigger kinds

### `manual`

Describes explicit invocation by a user, agent client, or external system.

It does not replace the workflow-routing requirement that the invocation resolve through a canonical workflow path or unambiguous filename stem.

### `schedule`

Describes recurring or delayed invocation intent in human-readable terms.

Ava does not define a cron dialect, recurrence rule, timezone field, daylight-saving behavior, missed-run policy, or scheduler ownership. The external executor translates the description into its native configuration.

### `event`

Describes invocation in response to an external event.

Ava does not define a shared event taxonomy, webhook schema, payload contract, filtering expression, authentication mechanism, or delivery guarantee. The external executor owns those details and supplies workflow inputs through the normal invocation contract.

## Discovery by external executors

External executors discover workflows through the existing managed and project-owned workflow registries.

An executor may:

1. traverse the workflow registries using the existing direct-child index rules
2. parse registered workflow metadata
3. select workflows whose `triggers` declarations match capabilities configured outside Ava
4. create or maintain executor-native bindings that invoke the canonical workflow path
5. validate required workflow inputs before invocation

Trigger metadata must not create a second workflow registry, invocation identifier, routing priority, or automatic activation path.

## External binding boundary

Executable trigger bindings belong to the host project or executor configuration, not to the portable Ava workflow prompt.

Examples include:

- crontab entries or systemd timers
- GitHub Actions workflow files and event filters
- ChatGPT task definitions
- CI pipeline schedules and rules
- custom agent-client configuration
- webhook infrastructure and secret management

A binding may reference a canonical workflow path and provide input values. It must not modify the workflow's declared primary role, mode, authority, or constraints.

Ava installation and upgrade tooling must treat external bindings as project-owned or environment-owned content. It must never generate, replace, or silently migrate those bindings unless a future separately approved contract defines a bounded integration mechanism.

## Validation level

Trigger metadata is advisory for execution but normative for document structure.

Validation errors:

- `triggers` is present but is not a non-empty list
- an entry is not a mapping
- `kind` is absent or unsupported
- `description` is absent or empty

Validation warnings:

- an exact duplicate trigger declaration
- unknown trigger fields
- descriptions that embed secrets, executor configuration, or environment-specific file paths
- schedule descriptions too vague for a human to configure reliably
- event descriptions that do not identify the relevant external event in understandable terms

A valid trigger declaration does not prove that any executor binding exists, is enabled, or can supply the required inputs. Execution readiness remains an external concern.

## Consequences

This proposal intentionally prefers honest portability over machine-executable scheduling metadata.

Benefits:

- one workflow document remains usable across cron, GitHub Actions, ChatGPT tasks, CI systems, and custom clients
- Ava avoids owning scheduler semantics or a persistent runtime
- executor-specific bindings can evolve without mutating managed workflow prompts
- validation can still detect malformed or misleading trigger intent

Trade-off:

- an executor cannot create a complete schedule or event binding from Ava metadata alone
- users or integration tooling must translate the portable description into executor-native configuration

That trade-off is acceptable because executable cross-platform scheduling is not actually portable without defining a runtime, event model, and environment configuration layer that Ava explicitly does not own.

## Intended implementation after approval

1. Add the optional `triggers` metadata contract to `templates/base/shared/instructions/workflow-format.md`.
2. Update `templates/base/shared/instructions/workflow-routing.md` to state that trigger discovery never bypasses explicit workflow identity resolution.
3. Update examples and validation fixtures to cover valid, malformed, duplicate, and unknown-field declarations.
4. Mark this task complete and update the Phase 3 index only after the authoritative contract and validation coverage are implemented.

## Next task

[Define Workflow Lifecycle Ownership](06-define-workflow-lifecycle-ownership.md).
