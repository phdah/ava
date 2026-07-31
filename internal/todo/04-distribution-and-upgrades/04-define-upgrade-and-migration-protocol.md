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

The accepted public protocol is documented in [Ava Upgrade and Migration Protocol](/templates/upgrade-and-migration.md). Its durable transaction journal is defined by [upgrade.schema.json](/templates/schemas/upgrade.schema.json), and explicit release edges and migration descriptors are defined by the updated [release.schema.json](/templates/schemas/release.schema.json).

## Accepted decisions

- `manifest.json` remains authoritative for the last completed managed installation and advances only after deterministic staging, migration, and validation succeed.
- `upgrade.json` is a durable transaction journal with explicit status, stage, source and target release identities, path, staging state, completed migrations, managed changes, project changes, failures, and permitted operations.
- Release manifests declare exact direct or chained source-to-target edges. SemVer ordering alone does not establish upgrade support.
- Chained upgrades verify every mandatory intermediate release and execute deterministic edges inside one outer durable transaction.
- Managed payloads use three-way comparison between the installed baseline checksum, current local content, and target release content.
- A modified, missing, corrupt, invalid, or colliding managed path blocks the transaction. It is never overwritten or reclassified silently.
- Deterministic upgrades do not create or modify project-owned scaffolds. New project-owned content is handled through installed guidance and the explicit Upgrade Role.
- Deterministic migrations have stable identifiers, exact source and target versions, dependency and order metadata, verified file checksums, apply and verification entry points, and required idempotency.
- Migration completion is recorded only after postcondition verification. Resume revalidates recorded work and reruns only safe unrecorded work.
- The target manifest is replaced last. This is the managed commit boundary for advancing `ava_version`.
- Installed base completion and project-owned semantic completion remain separate. Pending, partial, or blocked semantic state keeps the overall upgrade active and normal routing blocked.
- The managed root router must check upgrade and semantic state before ordinary routing and activate the managed Upgrade Role without consulting project-owned registries.
- Project-owned registries become migration inputs only after managed upgrade authority is active.
- Abort is terminal only before live managed mutation. After mutation begins, abort becomes rollback.
- Rollback restores the recorded source managed state. It never automatically reverses project-owned semantic edits.
- After project-owned edits, rollback remains blocked until those paths are explicitly reconciled and source compatibility is revalidated.

## Repository impact

- Added the public upgrade and migration protocol.
- Added a Draft 2020-12 schema for `/.ava/state/upgrade.json`.
- Replaced unrestricted release source strings with explicit direct and chained upgrade edges.
- Added structured migration file inventories and step descriptors to the release schema.
- Defined state entry, permitted operations, exit conditions, abort, rollback, and resume behavior.
- Defined PATCH, MINOR, MAJOR, and chained transition examples.
- Defined the managed pre-routing check and authority boundary required by the next Upgrade Role task.
- Advanced the roadmap to release guidance and the Upgrade Role.

## Validation

The upgrade and release schemas were parsed with `python -m json.tool`, checked as Draft 2020-12 schemas, and exercised with valid and invalid fixtures.

Validation covered:

- idle and active upgrade journal states
- rejection of normal routing in active upgrade state
- direct edges with no intermediates
- rejection of direct edges containing intermediates
- chained edges requiring at least one intermediate
- migration descriptors with stable IDs, dependencies, apply and verify paths, checksums, and required idempotency
- a release manifest with an explicit MAJOR transition and semantic review
- rejection of a non-idempotent migration descriptor

The installer, Upgrade Role, and fixture tasks must implement the filesystem, interruption, routing, and rollback behaviors defined by the protocol.
