---
type: Distribution Contract
title: Ava Upgrade and Migration Protocol
description: Defines deterministic base upgrades, durable transaction state, maintenance and semantic routing, rollback, finalization, and semantic completion.
tags: [ava, distribution, upgrades, migrations, transactions, compatibility, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-opencode
  at: 2026-08-20T11:51:12Z
---

# Ava Upgrade and Migration Protocol

This contract defines supported release transitions without silently overwriting managed conflicts or treating a new managed base as completed migration of project-owned context.

It implements [Ava Distribution and Ownership Boundary](ownership.md), [Ava Versioning and Compatibility](versioning.md), and [Ava GitHub Release Assets](releases.md). The updater owns deterministic mutation through managed commit and recovery operations. Ava Maintenance interprets and invokes those operations and owns the bounded terminal finalization transition after semantic completion. Upgrade Role owns project-owned semantic reconciliation.

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
11. Ava Maintenance may invoke deterministic operations but must not reproduce or bypass their protected state transitions, except for the exact protocol-defined terminal finalization transition after every finalization precondition is proven.
12. Upgrade Role may update semantic state but must not perform deterministic installation administration.

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
- project-owned paths later changed by Upgrade Role
- current failure and permitted operations

The updater writes and validates the journal before live mutation and through deterministic recovery. Each transition uses temporary-file write, flush, and atomic rename. The only agent-owned journal mutation is the terminal finalization transition defined below, which uses the same atomic-write requirement.

`transaction_id` names the exact transaction directory at `/.ava/state/transactions/<transaction_id>/`. Every recorded staging, backup, candidate-manifest, and transaction-plan path must resolve beneath that directory without symlink escape. Terminal cleanup removes this exact transaction directory, not only the nested path recorded in `staging.workspace`.

Terminal states may remain for reporting. Normal routing requires a safe terminal journal state, `semantic_compatibility.status: complete`, and no `/.ava/state/transactions/` container.

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

Release entries marked `project-owned` and `create-if-absent` apply only to fresh installation or explicit adoption. During upgrade, new recommended project-owned files are described by guidance and created only by Upgrade Role through the explicit semantic migration request.

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

Ava Maintenance owns agent-facing inspection and may invoke abort through the updater.

## Preflight

Actions: validate manifest and journal, current managed files, three-way plan, release assets, migration graph, guidance inventory, filesystem requirements, and unresolved semantic carry rules.

Permitted: inspect, resolve, resume, abort.

Conflict: `blocked/preflight`.

Exit: deterministic conflict-free plan.

Ava Maintenance explains the conflict and invokes only the deterministic operation permitted by the journal. It does not resolve semantic ambiguity or reconstruct managed state manually.

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

Only Upgrade Role performs project-owned semantic reconciliation. It may inspect and modify project-owned files only after managed activation establishes source-to-target authority.

Permitted: inspect, reconcile semantic context, record changed paths, capture decisions, update semantic state, and prepare project-owned rollback resolution.

Ava Maintenance remains responsible for deterministic status explanation, finalization, and invocation of managed rollback. Normal operations remain blocked until semantic state is complete and finalization reaches a safe terminal state, or rollback reaches a safe source terminal state.

## Completion

After full validation and semantic completion, Ava Maintenance performs the protocol-defined terminal finalization transition directly. Before any journal write it validates that semantic compatibility is complete, no unresolved decisions remain, the managed commit and selected edges are complete, every managed change has a terminal classification, the journal is in a finalizable post-commit state, and the exact transaction directory derived from `transaction_id` resolves safely beneath `/.ava/state/transactions/` with every recorded transaction-local path contained beneath it.

The atomic terminal journal write records:

```json
{
  "status": "complete",
  "stage": "complete",
  "current_edge": null,
  "staging": null,
  "failure": null,
  "allowed_operations": ["normal"]
}
```

It also refreshes `updated_at` and preserves unrelated journal fields. Only after that atomic write succeeds does Ava Maintenance recursively remove the exact `/.ava/state/transactions/<transaction_id>/` directory, including its workspace, backup, plan, and other transaction-local state. It then attempts to remove `/.ava/state/transactions/` only with a non-recursive empty-directory operation. A sibling transaction or any other entry prevents container removal and remains untouched. Finalization verifies the terminal journal, complete semantic compatibility, and absence of both the exact transaction directory and the empty transaction container.

Interrupted terminal cleanup occurs when transaction storage remains after a safe terminal write. Managed pre-routing activates Ava Maintenance despite the journal's `normal` operation. A valid `complete`, `aborted`, or `rolled-back` journal identifies its exact cleanup directory through `transaction_id`; Ava Maintenance revalidates semantic completion for that state and replays only exact directory cleanup plus guarded empty-container removal. An `idle` journal has no transaction ID and permits direct removal only of an empty container, or of its sole direct entry when that directory's valid plan identity, source manifest backup, source journal backup, and live managed checksums prove the fully restored source. Ambiguous or additional entries are managed-state conflicts and keep normal routing blocked.

Finalization is agent-driven and does not require an `ava` binary, updater executable, or transaction-local installer path. This is the only direct journal-mutation exception for Ava Maintenance.

# Managed pre-routing mode

Before ordinary workflow, role, instruction, or project-registry discovery, root `/AGENTS.md` must:

1. minimally validate `/.ava/state/upgrade.json`
2. validate the supported envelope of `manifest.json`
3. inspect whether `/.ava/state/transactions/` exists and which direct entries it contains
4. activate Ava Maintenance when state is malformed, contradictory, in a deterministic stage, retains terminal cleanup residue, contains another transaction entry, or the request is installation inspection or deterministic recovery
5. activate Upgrade Role only when semantic reconciliation is required and the requested outcome changes or validates project-owned context
6. keep unrelated ordinary requests blocked while deterministic, semantic, or finalization-cleanup work remains incomplete
7. load exact installed guidance paths only after Upgrade Role activation
8. enforce the operation allowlist and role authority boundary
9. read project-owned registries only after normal routing is permitted, or as bounded migration inputs after Upgrade Role activation

Both managed roles must be reachable entirely from managed files.

Malformed managed state enters read-only Ava Maintenance recovery rather than normal routing. Missing, corrupt, or incompatible project-owned routing cannot prevent installation inspection, deterministic recovery coordination, or semantic reconciliation.

# Role ownership by state and request

| Managed condition | Requested outcome | Active role |
|---|---|---|
| missing, malformed, unsupported, or contradictory state | inspect or explain recovery | Ava Maintenance |
| active or blocked deterministic stage | inspect, resume, abort, rollback, finalize, or explain | Ava Maintenance |
| semantic status incomplete | reconcile project-owned context | Upgrade Role |
| semantic status incomplete | inspect status, explain blockage, finalize, or invoke rollback | Ava Maintenance |
| safe terminal journal with transaction residue | replay evidence-bound terminal cleanup or report conflict | Ava Maintenance |
| safe terminal state and semantic complete | ordinary project work | ordinary routing |
| safe terminal state and semantic complete | installation health, host access, explicit upgrade, or removal | Ava Maintenance through ordinary routing |

The role selected for an explanation does not gain mutation authority owned by the other role or deterministic tooling. Ava Maintenance's terminal-finalization authority is the explicit bounded exception defined by this protocol.

# Permitted operations

| State | Operations | Owning interface | Normal routing |
|---|---|---|---|
| `idle` | normal | ordinary routing or Ava Maintenance request | only with semantic complete |
| `active/planning` | inspect, abort | Ava Maintenance invoking updater | blocked |
| `active/preflight` | inspect, resolve, resume, abort | Ava Maintenance and deterministic resolver | blocked |
| `blocked/preflight` | inspect, resolve, resume, abort | Ava Maintenance and deterministic resolver | blocked |
| `active/staged` | inspect, resume, abort | Ava Maintenance invoking updater | blocked |
| `active/migrating` | inspect, resume, abort or rollback by commit boundary | Ava Maintenance invoking updater | blocked |
| `blocked/migrating` | inspect, resolve, resume, rollback | Ava Maintenance and deterministic resolver | blocked |
| `active/validating` | inspect, resume, abort or rollback by commit boundary | Ava Maintenance invoking updater | blocked |
| `blocked/validating` | inspect, resolve, resume, rollback | Ava Maintenance and deterministic resolver | blocked |
| `active/base-installed` | inspect, semantic handoff, rollback | Ava Maintenance, then Upgrade Role for reconciliation | blocked unless semantic complete and finalized |
| `active/semantic` | inspect, reconcile, resolve, rollback preparation | Upgrade Role for project context, Ava Maintenance for deterministic actions | blocked |
| `blocked/semantic` | inspect, capture decisions, resolve, rollback preparation | Upgrade Role for project context, Ava Maintenance for deterministic actions | blocked |
| `active/rollback` | inspect, resolve, resume rollback | Ava Maintenance invoking updater | blocked |
| `blocked/rollback` | inspect, prepare project resolution, resume rollback | Upgrade Role for project resolution, Ava Maintenance for updater invocation | blocked |
| `complete` | normal, or bounded cleanup replay when transaction residue remains | ordinary routing or Ava Maintenance | allowed only when the transaction container is absent |
| `aborted` | normal | ordinary routing | only with unchanged source state and semantic complete |
| `rolled-back` | normal | ordinary routing | only after source compatibility validation |

The journal may narrow this operation set for a failure but never broaden it. Finalization remains a protocol-derived Ava Maintenance terminal transition rather than a new journal permission value.

# Abort, rollback, resume, and finalization

Before live managed mutation, abort removes staging, leaves the source manifest authoritative, records `aborted`, and permits normal routing when source semantics are complete.

After live mutation begins, abort becomes rollback. It is not terminal until source managed state is restored and validated.

Rollback restores only the source release recorded by the transaction; it is not a general downgrade. It restores prior managed payload, managed state, manifest, identity, and checksums.

Before project-owned semantic edits, validated restoration may become terminal `rolled-back`.

After project-owned edits, automatic rollback still restores managed state but never edits project files. The transaction remains `blocked/rollback` and reports every changed project path. The user must explicitly retain and prove compatibility, revert through version control or editing, or reconcile for the source release through Upgrade Role. Only then may Ava Maintenance invoke managed rollback to reach a terminal state.

A fresh invocation resumes by validating the source manifest, journal, workspace, planned paths, recorded migration checksums, and completed postconditions. It continues from the earliest unverified operation. If safe continuation cannot be proven, it blocks and offers rollback.

After Upgrade Role marks semantic compatibility complete, Ava Maintenance validates the finalization preconditions and atomically writes the exact terminal journal transition itself. It then removes only the exact transaction directory derived from `transaction_id`, attempts guarded removal of its empty parent, and verifies that both the directory and empty container are absent before normal routing is enabled. Interrupted cleanup is replayed idempotently from a terminal transaction ID or the bounded restored-source evidence required for `idle`. Ava Maintenance must not search for or require an installer binary to finalize.

Resume, abort, rollback, repair, and non-terminal journal mutation remain installer or updater responsibilities. Direct finalization does not broaden Ava Maintenance authority beyond the terminal transition above.

# Role-led removal

Removal is not an upgrade transaction and does not add an uninstall command mode.

Ava Maintenance may remove an installation only after explicit user intent and proof that:

- the manifest identifies a supported Ava installation
- no deterministic transaction is active or blocked
- semantic compatibility is complete with no unresolved work
- every deleted path is recorded as Ava-managed
- the root router still matches its recorded checksum
- no modified, missing, corrupt, non-regular, or unexpected managed content would be discarded ambiguously

A successful removal deletes `/.ava/` and the unchanged managed `/AGENTS.md`. It preserves every project-owned role, workflow, shared instruction, knowledge item, inbox item, index, log, OpenCode configuration, and host entrypoint.

A modified router or unexpected content beneath `/.ava/` blocks automatic removal until the user resolves the conflict explicitly. Project-owned host entrypoints are never modified; Ava Maintenance reports any reference that becomes stale after removal.

# Examples

## PATCH: 1.2.3 to 1.2.4

A direct edge, no migrations, and no semantic review. Ava Maintenance may initiate the updater, which validates, commits the target manifest last, advances both installed and compatible-through versions, and completes without semantic mode.

## MINOR: 1.2.4 to 1.3.0

An opt-in managed capability is proven unreachable by existing projects. The transition follows the PATCH path. Compatibility proof is release evidence, not runtime semantic work.

A recommended project scaffold is not created by the updater. Guidance may offer it through Upgrade Role and must declare semantic review when action is required.

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

A status request reaches Ava Maintenance. A request to reconcile project-owned context reaches Upgrade Role. After semantic completion, Ava Maintenance performs the direct terminal finalization transition before normal routing resumes.

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
- deterministic pre-routing to Ava Maintenance
- semantic pre-routing to Upgrade Role
- agent-driven terminal finalization without binary discovery, including exact terminal journal fields and recorded transaction-workspace cleanup
- finalization precondition failure leaving the journal unchanged and normal routing blocked
- preservation of installer-backed resume, abort, rollback, and non-terminal mutation boundaries
- managed recovery with missing or incompatible project registries
- separate installed-base and semantic-compatibility reporting
- host capability and OpenCode managed-context accessibility reporting
- role-led removal that preserves project-owned content and refuses uncertain ownership
