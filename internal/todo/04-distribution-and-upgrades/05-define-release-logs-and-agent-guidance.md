---
type: Internal Development Task
title: Define Release Guidance and Upgrade Role
description: Define structured release information and an explicit Upgrade Role for one-prompt semantic reconciliation of all affected project-owned Ava context.
tags: [internal, roadmap, releases, logs, migration, agents, roles]
status: complete
phase: 4
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
---

# Define Release Guidance and Upgrade Role

The accepted public guidance contract is documented in [Ava Release Guidance](/distribution/guidance.md). Parsed guidance metadata is validated by [guidance.schema.json](/distribution/schemas/guidance.schema.json).

The managed pre-routing behavior is defined by [Upgrade State and Routing](/templates/base/shared/instructions/upgrade-state-and-routing.md), and the complete managed role is defined under [`templates/base/roles/upgrade-role/`](/templates/base/roles/upgrade-role/).

## Accepted decisions

- Every supported semantic transition installs one canonical `/.ava/guidance/<from>-to-<to>/UPGRADE.md` document.
- Release manifests inventory every guidance file and each upgrade edge records the exact applicable guidance paths.
- Guidance metadata records source, target, semantic-review requirement, deterministic migration IDs, and explicit supersession.
- Guidance bodies explicitly state changed contracts, affected project-owned concepts, required decisions, semantic procedure, validation and completion criteria, and rollback implications.
- Scoped `log.md` files and release notes may inform release authors but never define migration obligations. No new log metadata is required.
- Multi-version obligations are cumulative unless later guidance explicitly supersedes an earlier guidance ID and restates its replacement obligations.
- The root managed router checks upgrade and semantic state before ordinary instruction, workflow, role, or project-registry discovery.
- Active or blocked upgrade state activates the managed Upgrade Role directly. Semantic upgrade reconciliation is not a workflow.
- Project-owned registries become migration inputs only after the Upgrade Role and bounded source-to-target authority are active.
- The Upgrade Role may cross ordinary project maintenance boundaries only for installed guidance obligations.
- The Upgrade Role is the only agent role permitted to update semantic compatibility and semantic-stage journal fields.
- Deterministic tooling retains exclusive authority over release identity, managed inventory, checksums, migration execution records, staging, backups, and managed rollback.
- Normal routing remains blocked until semantic compatibility is complete and the journal reaches a safe terminal state.
- The canonical one-prompt request authorizes required semantic migration but not unrelated project maintenance.

## Repository impact

- Added the release-guidance public contract and metadata schema.
- Added the managed Upgrade Role with deterministic required reading, bounded authority, complete procedure, capabilities, and constraints.
- Added managed pre-routing state and recovery instructions.
- Updated the root router, managed role catalog, managed workflow registry, and shared instruction index.
- Explicitly excluded semantic upgrades from workflow invocation and ordinary role selection.
- Marked the deferred workflow phase active again and made its catalog-purpose audit the next task.

## Validation

Validation covered:

- JSON parsing and Draft 2020-12 shape for `guidance.schema.json`
- all five mandatory Upgrade Role files and deterministic required-reading links
- direct managed activation without project-owned registry dependency
- explicit normal-routing blocks for active, blocked, pending, partial, and malformed state
- managed versus project-owned mutation boundaries
- one-prompt scope restriction to upgrade-required project-owned changes
- explicit guidance metadata, required sections, composition, decisions, completion, and rollback rules
- workflow registry wording that excludes semantic upgrade activation
- roadmap status, counts, and next-task handoff

Installer and fixture tasks must implement executable validation of state transitions, path inventories, Markdown section order, cross-schema version agreement, and recovery reachability.
