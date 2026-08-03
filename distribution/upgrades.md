---
type: Distribution Contract
title: Ava Upgrade and Migration Protocol
description: Defines deterministic base upgrades, durable transaction state, migration ordering, managed upgrade routing, rollback, and semantic completion.
tags: [ava, distribution, upgrades, migrations, transactions, compatibility]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Ava Upgrade and Migration Protocol

This contract defines supported release transitions without silently overwriting managed conflicts or treating a new managed base as completed migration of project-owned context.

It implements [Ava Distribution and Ownership Boundary](ownership.md), [Ava Versioning and Compatibility](versioning.md), and [Ava GitHub Release Assets](releases.md). The updater owns deterministic stages. The managed Upgrade Role owns the project-owned semantic stage.

# Invariants

1. `/.ava/state/manifest.json` describes the last completed managed installation.
2. `/.ava/state/upgrade.json` is the durable journal for a planned, active, blocked, completed, aborted, or rolled-back transaction.
3. `ava_version` advances only after target managed content and deterministic migrations are staged, applied, validated, and committed.
4. Advancing `ava_version` does not imply semantic compatibility of project-owned context.
5. Normal routing is blocked while the transaction is active or semantic compatibility is not `complete`.
6. Deterministic work never modifies project-owned content.
7. Modified, missing, corrupt, invalid, or colliding managed paths block the transaction.
8. Immutable release metadata must declare every supported source-to-target transition.
9. Resume and rollback use durable recorded state, never filesystem guesses.
10. Automatic rollback never reverses project-owned edits.

# Managed state

## Installed manifest

Before the managed commit point, the existing manifest remains authoritative. Candidate manifest content belongs in the transaction workspace.

The updater replaces the live manifest last. The new manifest records the target release, managed inventory, `okf_version`, and only the mechanical semantic transition permitted by the versioning contract. Manifest-last replacement is the commit boundary even though POSIX filesystems cannot atomically replace every managed path together.

## Upgrade journal

`upgrade.json` conforms to [upgrade.schema.json](schemas/upgrade.schema.json). It records:

- transaction ID, status, and stage
- source and target release identities
- resolved direct or chained path and current edge
- staging, backup, and candidate-manifest locations
- managed-file classifications and operations
- resolved migrations and verified completion records
- project-owned paths later changed by the Upgrade Role
- current failure and permitted operations

The updater writes and validates the journal before live mutation. Each transition uses temporary-file write, flush, and atomic rename.

Terminal states may remain for reporting. Normal routing requires both a terminal journal state and `semantic_compatibility.status: complete`.

# Explicit release graph

Each release manifest declares exact upgrade edges containing:

- `from` and `to` versions
- `direct` or `chained` mode
- mandatory intermediate versions
- unresolved-semantic-state carry permission
- migration IDs
- installed guidance paths

The edge `to` value must equal the containing release's `ava_version`; validators enforce this semantic rule.

A direct A to B upgrade is supported only when B declares a direct edge from A, lists every required migration and guidance item, declares no intermediate, and uses compatible installer and state protocols.

A chained A to D edge lists mandatory intermediate versions, for example:

```text
A -> B -> C -> D
```

The updater verifies every intermediate release and every adjacent edge before changing the project. Deterministic work for all edges runs inside one outer transaction. Skipped intermediate semantic work is allowed only when final guidance composes all obligations.

An upgrade may carry `pending`, `partial`, or `blocked` semantic state only when every traversed edge explicitly permits it and final guidance covers the original `compatible_through` version through the final target. Otherwise preflight blocks.

# Three-way managed reconciliation

For each immutable managed payload, compare:

1. the installed manifest checksum
2. current local checksum or absence
3. target checksum or absence

| Previous | Current | Target | Result |
|---|---|---|---|
| present | equals previous | same | retain |
| present | equals previous | changed | replace |
| present | equals previous | absent | delete |
| present | missing or differs | any | conflict |
| absent | absent | present | create |
| absent | present | present | collision |
| absent | present | absent | unrelated, untouched |

A local difference remains a managed conflict even when the target equals the previous release. Local edits never transfer ownership.

Mutable managed state is validated through schema, consistency, authority, and allowed transitions instead of byte checksums.

Conflict reports include path, expected state, actual state, target operation, and explicit recovery choices. Recovery may restore the installed version, discard a local edit, preserve project meaning in a project-owned path, or abort.

# Project-owned paths

Deterministic upgrades never create, replace, delete, move, or merge project-owned content.

Release entries marked `project-owned` and `create-if-absent` apply only to fresh installation or explicit adoption. During upgrade, new recommended project-owned files are described by guidance and created only by the managed Upgrade Role through the explicit semantic migration request.

# Deterministic migrations

Migrations operate only on managed payload or managed state. Each step declares:

- stable ID
- exact source and target versions
- numeric order and dependency IDs
- apply and verification entry points
- descriptor and file checksums
- `idempotent: true`

For every traversed edge, the updater selects only its declared IDs, verifies each descriptor and file, rejects missing or duplicate IDs, cycles, invalid dependencies, transition mismatches, and ambiguous ordering, then records a stable topological order by dependency, edge, numeric order, and ID.

For each migration:

1. verify preconditions
2. execute against staged managed content or state
3. execute verification
4. record ID, descriptor checksum, edge index, completion time, and verified postcondition

On resume, a recorded step with the same checksum is reverified and skipped. A checksum change blocks. An unrecorded step may be rerun only because the step is idempotent. Failed verification remains unrecorded and blocks.

# Transaction state machine

## Planning

Entry: valid installed manifest, no active owner, resolved target.

Actions: verify target release, resolve path, create active journal.

Permitted: inspect, abort.

Exit: complete release path and assets recorded.

## Preflight

Actions: validate manifest and journal, current managed files, three-way plan, release assets, migration graph, guidance inventory, filesystem requirements, and unresolved semantic carry rules.

Permitted: inspect, resolve, resume, abort.

Conflict: `blocked/preflight`.

Exit: deterministic conflict-free plan.

## Staging

Actions: create transaction workspace, durable rollback backup, unpack and verify target assets, construct target managed tree and candidate manifest, record operations.

Permitted: inspect, resume, abort.

Exit: durable candidate and rollback material.

## Migrating

Actions: execute and record migrations in resolved order.

Permitted: inspect, resolve, resume, abort before live mutation, rollback after live mutation.

Failure: `blocked/migrating`.

Exit: all required migrations reverified.

## Validating

Actions: validate candidate managed tree, state transitions, ownership, release identity, router and recovery reachability, and absence of project-owned changes.

Permitted: inspect, resolve, resume, abort before commit, rollback after commit.

Failure: `blocked/validating`.

Exit: complete deterministic validity.

## Managed commit

While the journal remains active, replace live managed payloads from staging and replace `manifest.json` last.

The new manifest transitions semantics mechanically:

- no semantic review and prior `complete`: advance `compatible_through` and remain complete
- semantic review required: preserve `compatible_through`, set target, set `pending`, clear unresolved decisions
- explicitly carried unresolved state: preserve last completed compatibility and initialize the composed target state

After manifest replacement, the journal becomes `base-installed`, then `complete` when semantic compatibility is complete or `semantic` otherwise.

## Semantic migration

Only the Ava-managed Upgrade Role performs this stage. It may inspect and modify project-owned files only after managed activation establishes source-to-target authority.

Permitted: inspect, reconcile semantic context, record changed paths, capture decisions, update semantic state, resume, request rollback.

Normal operations remain blocked until semantic state is complete or rollback reaches a safe source terminal state.

## Completion

After full validation and semantic completion:

```json
{
  "status": "complete",
  "stage": "complete",
  "allowed_operations": ["normal"]
}
```

# Managed pre-routing mode

Before ordinary workflow, role, instruction, or project-registry discovery, root `/AGENTS.md` must:

1. minimally validate `/.ava/state/upgrade.json`
2. validate the supported envelope of `manifest.json`
3. enter upgrade mode when journal status is `active` or `blocked`, or semantic status is not `complete`
4. load the managed Upgrade Role directly, without project-owned or combined registry resolution
5. load exact installed guidance paths recorded by the transaction
6. enforce the operation allowlist
7. read project-owned registries only afterward, as migration inputs

The [release guidance contract](guidance.md) defines the canonical managed Upgrade Role path and guidance entry point. Both must be reachable entirely from managed files.

Malformed managed upgrade state enters minimal recovery mode rather than normal routing. Missing, corrupt, or incompatible project-owned routing cannot prevent inspect, resume, abort, rollback, or semantic reconciliation.

# Permitted operations

| State | Operations | Normal routing |
|---|---|---|
| `idle` | normal | only with semantic complete |
| `active/planning` | inspect, abort | blocked |
| `active/preflight` | inspect, resolve, resume, abort | blocked |
| `blocked/preflight` | inspect, resolve, resume, abort | blocked |
| `active/staged` | inspect, resume, abort | blocked |
| `active/migrating` | inspect, resume, abort or rollback by commit boundary | blocked |
| `blocked/migrating` | inspect, resolve, resume, rollback | blocked |
| `active/validating` | inspect, resume, abort or rollback by commit boundary | blocked |
| `blocked/validating` | inspect, resolve, resume, rollback | blocked |
| `active/base-installed` | inspect, resume semantic migration, rollback | blocked unless semantic complete |
| `active/semantic` | inspect, reconcile, resolve, resume, rollback | blocked |
| `blocked/semantic` | inspect, capture decisions, resolve, resume, rollback | blocked |
| `active/rollback` | inspect, resolve, resume rollback | blocked |
| `blocked/rollback` | inspect, capture decisions, resolve, resume rollback | blocked |
| `complete` | normal | allowed |
| `aborted` | normal | only with unchanged source state |
| `rolled-back` | normal | only after source compatibility validation |

The journal may narrow this operation set for a failure but never broaden it.

# Abort, rollback, and resume

Before live managed mutation, abort removes staging, leaves the source manifest authoritative, records `aborted`, and permits normal routing when source semantics are complete.

After live mutation begins, abort becomes rollback. It is not terminal until source managed state is restored and validated.

Rollback restores only the source release recorded by the transaction; it is not a general downgrade. It restores prior managed payload, managed state, manifest, identity, and checksums.

Before project-owned semantic edits, validated restoration may become terminal `rolled-back`.

After project-owned edits, automatic rollback still restores managed state but never edits project files. The transaction remains `blocked/rollback` and reports every changed project path. The user must explicitly retain and prove compatibility, revert through version control or editing, or reconcile for the source release. Only then may rollback become terminal and normal routing resume.

A fresh invocation resumes by validating the source manifest, journal, workspace, planned paths, recorded migration checksums, and completed postconditions. It continues from the earliest unverified operation. If safe continuation cannot be proven, it blocks and offers rollback.

# Examples

## PATCH: 1.2.3 to 1.2.4

A direct edge, no migrations, and no semantic review. The updater validates, commits the target manifest last, advances both installed and compatible-through versions, and completes without semantic mode.

## MINOR: 1.2.4 to 1.3.0

An opt-in managed capability is proven unreachable by existing projects. The transition follows the PATCH path. Compatibility proof is release evidence, not runtime semantic work.

A recommended project scaffold is not created by the updater. Guidance may offer it through the Upgrade Role and must declare semantic review when action is required.

## MAJOR: 1.3.0 to 2.0.0

The release declares a direct edge, migration `manifest-v1-to-v2`, guidance, and semantic review.

After deterministic success:

```text
Installed Ava base: 2.0.0
Project context compatible through: 1.3.0
Semantic target: 2.0.0
Semantic status: pending
Upgrade journal: active/semantic
Normal operations: blocked
```

A fresh agent reads managed state first and reaches the managed Upgrade Role even when `/roles/index.md` or `/workflows/index.md` is incompatible. Completion requires every affected project file, registry, index, link, and decision to be reconciled.

## Chained: 1.0.0 to 2.0.0 through 1.5.0

The updater verifies and executes `1.0.0 -> 1.5.0 -> 2.0.0` inside one outer transaction. If final guidance cannot compose skipped semantic obligations, the path is unsupported and preflight aborts.

# Validation requirements

Implementations and fixtures must cover:

- edge target equality and direct/chained invariants
- migration and guidance existence, checksums, uniqueness, ordering, dependency cycles, and idempotency
- three-way conflicts and ownership boundaries
- manifest-last commit
- interruption and resume at every stage
- abort before live mutation
- rollback before and after commit
- rollback after project edits remaining blocked until explicit resolution
- normal-routing blocks for pending, partial, and blocked semantics
- managed recovery with missing or incompatible project registries
- separate installed-base and semantic-compatibility reporting
