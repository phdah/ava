---
type: Shared Instruction
title: Workflow Triggers
description: Portable workflow trigger intent, external executor discovery, validation, and scheduler ownership boundaries.
tags: [ava, workflows, triggers, portability, validation]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T12:15:00+02:00
---

# Purpose

A workflow may declare portable trigger intent so external systems can discover workflows that are suitable for manual, scheduled, or event-driven invocation.

Trigger metadata describes when a workflow is intended to be considered. It does not configure, authorize, or operate an executor.

Ava validates the portable declaration. Cron expressions, time zones, event filters, credentials, retries, concurrency, delivery guarantees, and other environment-specific execution settings remain outside the workflow document.

# Metadata

A workflow may declare an optional `triggers` list:

```yaml
triggers:
  - kind: manual
    description: Run when a maintainer explicitly requests the workflow.
  - kind: schedule
    description: Run periodically to review accumulated project context.
  - kind: event
    description: Run after a pull request is opened or updated.
```

Each trigger entry must contain exactly these recognized fields:

- `kind`: one of `manual`, `schedule`, or `event`
- `description`: a non-empty human-readable description of the intended trigger

Trigger entries must be unique by `kind`. A workflow may therefore declare at most one trigger of each kind.

Unknown trigger fields are preserved for forward compatibility but have no Ava semantics and produce a warning. A portable workflow must not depend on an unknown field for correct interpretation.

# Trigger kinds

## `manual`

The workflow is suitable for explicit invocation by a user, agent client, or another system that has already received an authorized request.

A manual trigger does not bypass normal workflow resolution, input validation, role activation, approval requirements, or capability constraints.

## `schedule`

The workflow is suitable for periodic or time-based invocation by an external scheduler.

The workflow document must not embed executable scheduler configuration, including:

- cron expressions
- concrete dates or times
- time zones
- jitter or delay settings
- missed-run behavior
- retry or backoff policy
- concurrency or overlap policy

Those values belong to the external executor binding.

## `event`

The workflow is suitable for invocation after an externally observed event.

The workflow document may describe the event semantically, but must not embed environment-specific event configuration, including:

- webhook URLs or secrets
- repository, branch, path, or actor filters
- CI provider event syntax
- message-bus topics or subscriptions
- payload schemas tied to one provider
- acknowledgement, retry, or delivery semantics

Those values belong to the external executor binding.

# Discovery

External systems discover executable workflows through the managed and project-owned workflow registries defined by [Workflow registry and routing](workflow-routing.md).

A discovery client must:

1. traverse only registered workflows
2. validate each workflow against [Workflow format](workflow-format.md)
3. inspect its optional `triggers` metadata
4. select only workflows whose declared trigger kind matches the executor's intended binding
5. retain the canonical workflow path as the invocation identity
6. supply required workflow inputs when invoking it

A trigger declaration does not make an unregistered, deprecated, invalid, or otherwise blocked workflow executable.

A client may expose workflows without trigger metadata for manual browsing. It must not infer schedule or event suitability from titles, descriptions, procedure text, or filename conventions.

# Executor bindings

An executor binding is environment-owned configuration that connects one registered workflow path to one concrete trigger implementation.

Examples include:

- a cron entry invoking a workflow through an agent client
- a GitHub Actions workflow reacting to a pull request event
- a ChatGPT task configured with a schedule
- a CI job invoked after a deployment stage
- a custom client reacting to a message-bus event

Bindings must live outside portable workflow prompts. They may be stored in project-owned infrastructure, CI, scheduler, client, or host configuration.

A binding is responsible for:

- concrete timing or event matching
- environment and target selection
- authentication and secrets
- required workflow input values
- retries, concurrency, idempotency, and delivery guarantees
- invoking the canonical workflow path
- retaining execution history when required

Ava does not define a portable binding-file format because these responsibilities differ materially between executors.

# Runtime boundary

Trigger metadata is validated but advisory for execution.

Ava does not:

- start or monitor schedules
- subscribe to events
- expose webhooks
- maintain trigger state or execution history
- guarantee that an external binding exists
- verify that a binding matches its trigger description
- grant permission to invoke or mutate project content

When a workflow is invoked by an external executor, normal upgrade-state checks, workflow routing, role activation, input resolution, operating mode, authority, constraints, and approval requirements still apply.

# Validation

Treat these as errors:

- `triggers` is present but is not a list
- a trigger entry is not a mapping
- a trigger entry omits `kind` or `description`
- `kind` is not `manual`, `schedule`, or `event`
- `description` is empty or not a string
- more than one trigger entry uses the same `kind`
- schedule metadata contains executable timing or scheduler configuration
- event metadata contains provider-specific filters, secrets, endpoints, subscriptions, or payload configuration
- a trigger declaration claims to bypass routing, input, role, approval, authority, or capability checks

Treat these as warnings or semantic findings:

- unknown fields within a trigger entry
- a trigger description that is too vague to guide executor binding
- a workflow that appears intended for recurring execution but declares no trigger metadata
- an external binding that invokes a shorthand name instead of retaining the canonical workflow path
- documentation that implies Ava operates the scheduler or event source

A validator may validate workflow metadata and descriptions. It cannot prove that an external executor binding exists or behaves as described.

# Examples

Valid portable metadata:

```yaml
triggers:
  - kind: manual
    description: Run when a maintainer requests a bounded review.
  - kind: schedule
    description: Run periodically to audit the selected project-context scope.
```

Invalid schedule configuration:

```yaml
triggers:
  - kind: schedule
    description: Run every weekday morning.
    cron: "0 8 * * 1-5"
    timezone: Europe/Stockholm
```

Invalid event configuration:

```yaml
triggers:
  - kind: event
    description: Run for pull request changes.
    github_event: pull_request
    branches: [main]
    webhook_secret: AVA_SECRET
```

The invalid examples belong in executor-owned configuration, not portable workflow metadata.
