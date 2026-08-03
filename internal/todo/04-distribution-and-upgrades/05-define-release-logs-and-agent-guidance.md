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
- Release manifests inventory every guidance file and each upgrade edge records the exact applicable paths.
- Guidance metadata records source, target, semantic-review requirement, deterministic migration IDs, and explicit supersession.
- Guidance bodies explicitly state changed contracts, affected project-owned concepts, required decisions, semantic procedure, completion criteria, and rollback implications.
- Scoped logs and release notes may inform release authors but never define migration obligations.
- Active or blocked upgrade state activates the managed Upgrade Role directly. Semantic reconciliation is not a workflow.
- The Upgrade Role may cross ordinary project maintenance boundaries only for installed guidance obligations.
- Deterministic tooling retains exclusive authority over managed release state and rollback.
- Normal routing remains blocked until semantic compatibility and transaction state are safe.

## Repository impact

The public guidance contract and schema are indexed under `/distribution/`; managed role and routing sources remain under `/templates/base/`.

## Validation

Validation covered schema shape, managed role files and reading links, pre-routing activation, state blocks, mutation boundaries, guidance composition, decisions, completion, and rollback rules.
