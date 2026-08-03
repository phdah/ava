---
type: Internal Development Task
title: Define Upgrade and Migration Protocol
description: Define safe base reconciliation, deterministic migrations, conflicts, rollback, and separate semantic completion state.
tags: [internal, roadmap, upgrades, migrations]
status: complete
phase: 4
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T14:43:00+02:00
---

# Define Upgrade and Migration Protocol

The accepted public protocol is documented in [Ava Upgrade and Migration Protocol](/distribution/upgrades.md). Its durable transaction journal is defined by [upgrade.schema.json](/distribution/schemas/upgrade.schema.json), and release edges and migration descriptors are defined by [release.schema.json](/distribution/schemas/release.schema.json).

## Accepted decisions

- `manifest.json` remains authoritative for the last completed managed installation and advances only after deterministic staging, migration, and validation succeed.
- `upgrade.json` is a durable transaction journal with explicit status, stages, release identities, path, staging state, migrations, managed changes, project changes, failures, and permitted operations.
- Release manifests declare exact direct or chained source-to-target edges.
- Managed payloads use three-way comparison between the installed baseline checksum, current local content, and target release content.
- Modified, missing, corrupt, invalid, or colliding managed paths block the transaction.
- Deterministic upgrades never modify project-owned content.
- Migrations have stable identifiers, exact transitions, dependencies, order, checksums, apply and verification entry points, and required idempotency.
- The target manifest is replaced last.
- Installed base completion and project-owned semantic completion remain separate.
- Active upgrade state activates the managed Upgrade Role before project-owned registry discovery.
- Rollback restores only managed state and never automatically reverses project-owned semantic edits.

## Repository impact

The public protocol and schemas are indexed under `/distribution/`. Installer and fixture tasks remain responsible for executable behavior.

## Validation

The upgrade and release schemas were parsed and exercised with valid and invalid idle, active, direct, chained, migration, and semantic-review fixtures.
