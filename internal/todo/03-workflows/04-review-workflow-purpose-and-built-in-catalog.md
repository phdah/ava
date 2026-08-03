---
type: Internal Development Task
title: Review Workflow Purpose and Built-in Catalog
description: Defines when a reusable workflow is justified and aligns the built-in catalog with free-form role work and deterministic release tooling.
tags: [internal, roadmap, workflows, catalog, routing]
status: complete
phase: 3
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Review Workflow Purpose and Built-in Catalog

The workflow format, routing contracts, managed catalog, and affected role guidance now distinguish optional reusable procedures from ordinary role work and deterministic tooling.

## Accepted purpose boundary

- A free-form request selects the role whose durable responsibilities own the requested outcome.
- An explicitly invoked workflow adds a bounded reusable procedure with meaningful inputs, mode, ordering, context, or expected output.
- A workflow must not exist only as a command-like alias for ordinary role work.
- Installation, managed-file replacement, integrity checks, deterministic migrations, state transitions, and structural validation belong to deterministic tooling.
- Semantic Ava version reconciliation is not a workflow. Active upgrade state directly selects the managed Upgrade Role.

## Workflow admission criteria

A workflow must be repeatable, bounded, owned by exactly one ordinary role, and provide procedural value beyond the role's durable instructions. It must define meaningful inputs or fixed batch scope, an effective operating mode, a distinct procedure, and a standardized expected output.

Warnings include duplicated role procedures, generic mutation outputs, one-off work, aliases that only select a role, and wrappers around deterministic mechanics.

## Catalog audit

### Retained and revised

- `ingest-inbox`: retained as a batch procedure across every pending direct inbox source.
- `review-change`: retained as a standardized semantic review with independence disclosure, evidence, severity, and remediation ownership.

### Replaced

- `daily-project-maintenance` was replaced by `audit-project-context`, which defines a bounded suggestion-only audit without assuming a scheduler or previous-run state.
- `review-role-change` was replaced by `review-role-catalog`, which reviews the complete registered role system rather than duplicating the general bounded change-review procedure.

### Removed

The following workflows duplicated durable role responsibilities and were removed before Ava's first supported release:

- `create-role`
- `update-role`
- `repair-role`
- `configure-project`
- `curate-project-knowledge`
- `tighten-instructions`

The underlying work remains available through free-form Role Manager or Project Steward routing.

## Versioning and migration

Managed workflows are versioned release payloads. Project-owned workflows remain project-owned. Workflow changes that affect identity, invocation ambiguity, primary role, required inputs, mode, or intended behavior follow Ava's compatibility classification and release-guidance requirements.

The current repository is pre-`1.0.0` and has no published supported workflow references, so rejected initial workflows were removed directly rather than retained as deprecation stubs.

## Repository impact

- Added workflow admission, warning, free-form, deterministic-tooling, and versioning boundaries.
- Corrected workflow and role resolution across managed `/.ava/base/` registries and project-owned extension registries.
- Reduced the built-in catalog from ten workflows to four outcome-oriented procedures.
- Updated retained workflow primary-role paths to their installed managed locations.
- Removed stale workflow aliases from role routing and instructions.
- Updated public architecture, versioning guidance, roadmap state, and conceptual history.

## Validation

Validation covered:

- each registered workflow's metadata, required section order, input declarations, mode, and expected output
- exactly one registered ordinary primary role for every workflow
- managed and project-owned registry path consistency with the root router
- exclusion of the managed Upgrade Role from workflow primary-role resolution
- direct-child workflow index coverage and absence of removed entries
- role routing without removed command aliases
- roadmap status and next-task handoff
- pre-`1.0.0` direct-removal compatibility rationale
