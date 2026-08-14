---
type: Role Instructions
title: Upgrade Role Instructions
description: Procedure for applying installed release guidance and completing or blocking semantic compatibility.
tags: [ava, role, upgrades, migration, instructions]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-15T00:19:00+02:00
---

# Entry procedure

Before changing project-owned context:

1. Read the managed manifest and upgrade journal.
2. Confirm the installed base, compatible-through version, target version, journal status, semantic stage, and allowed operations.
3. Confirm that `reconcile-semantic` or the semantic resolution requested by the user is permitted.
4. Confirm that each applicable selected edge explicitly requires semantic review, or that unresolved semantic state is being carried under the upgrade protocol.
5. Resolve the exact relative guidance paths recorded by the transaction beneath `./.ava/guidance/`, in order.
6. Validate each guidance document against the release-guidance contract and its transaction edge.
7. Stop without mutation when an explicit edge decision and its guidance list disagree, when required guidance is absent, or when managed state cannot establish semantic authority.
8. Hand deterministic inspection, resume, abort, rollback, finalization, host accessibility, and removal requests to Ava Maintenance.

The release-wide semantic-review field is only an inventory summary. Use the selected installed edge decisions and exact journal guidance paths. Do not infer project-owned migrations from arbitrary managed-file differences, release history, logs, or unrecorded guidance.

# Impact analysis

For every loaded guidance document:

1. Identify changed managed contracts and their project-facing semantic impact.
2. Resolve cumulative obligations and explicit supersession across the guidance chain.
3. Build a bounded inventory from the affected concept conditions in the guidance.
4. Inspect affected registries, indexes, canonical paths, references, metadata, and scoped history.
5. Record every project-owned path actually inspected for the semantic decision in `upgrade.json.project_changes`, even when inspection proves that no content mutation is required.
6. Separate deterministic work already completed from semantic project-owned work.
7. Identify required decisions that project intent cannot resolve.

An inspection-only record uses `change_type: inspected` and `resolution: retained`. If the same path is later created, modified, deleted, or moved during this semantic reconciliation, update its record to that actual change type and the current resolution rather than keeping a duplicate inspection-only entry.

Explain the material changes and planned project-owned mutations before applying them. The canonical one-prompt request authorizes the required migration, but it does not authorize unrelated cleanup.

# Decision handling

When a blocking decision is required:

1. use the guidance decision identifier
2. state the affected files and criteria
3. preserve completed safe work
4. add or update the decision in `semantic_compatibility.unresolved_decisions`
5. set semantic status and journal state to `blocked` according to the protocol
6. report the exact decision required

Do not invent project-specific policy, authority, naming, ownership, or destructive behavior.

# Applying project-owned changes

Apply the smallest coherent set of changes that satisfies all non-superseded guidance obligations.

For every changed project path:

1. verify that it is project-owned
2. preserve unknown valid metadata and unrelated project intent
3. update all affected canonical references and discovery indexes
4. update the nearest scoped log when meaning, authority, routing, ownership, compatibility, or stable structure changes
5. update its existing inspection record or append the path in `upgrade.json.project_changes` with the actual change type
6. validate the changed document and its relationships

The project change record must identify the exact path, change type, recorded time, and current resolution. `inspected` means the path was read as a guidance-driven semantic input and retained without content mutation. Do not mark semantic compatibility complete while an inspected or changed project-owned path is missing from the journal or remains unresolved.

A migration is not complete while any required role, workflow, registry, index, log, metadata field, link, filename, or structural convention remains inconsistent with the target contract.

# Semantic state transitions

The role may transition semantic compatibility only as allowed by the versioning contract:

- `pending` to `partial`, `blocked`, or `complete`
- `partial` to `blocked` or `complete`
- `blocked` to `partial` or `complete` after blocking conditions are resolved

Use `partial` only when safe required work has been applied but completion criteria remain unmet without a current blocking decision. Use `blocked` when a decision, prerequisite, host limitation, or invalid managed input prevents safe continuation.

Mark `complete` only when:

- every exact installed guidance document has been applied in transaction order
- every loaded guidance completion criterion passes
- every affected project relationship is consistent
- every project-owned path inspected or changed while applying the guidance is recorded exactly once in `upgrade.json.project_changes`
- every inspection-only path is recorded as `change_type: inspected` with `resolution: retained`
- every changed project-owned path records its actual change type and current resolution
- `unresolved_decisions` is empty
- `compatible_through` can advance exactly to installed `ava_version`
- `target_version` can be cleared
- the journal remains non-normal until deterministic finalization reaches `complete/complete` with `allowed_operations: [normal]`

The Upgrade Role updates semantic compatibility but does not manually grant normal routing. Ava Maintenance invokes deterministic finalization after semantic completion.

# Rollback preparation

The Upgrade Role does not perform managed rollback.

When rollback is requested after project-owned edits:

1. report every recorded project path whose change type is not `inspected`
2. determine whether each edit remains compatible with the source release
3. mark each changed-path journal resolution as retained, reverted, or reconciled only with evidence
4. leave inspection-only records as historical semantic evidence; they do not create rollback work by themselves
5. update project-owned context only when the user explicitly chooses a safe source-compatible resolution
6. keep rollback blocked until source semantic compatibility is validated
7. hand the deterministic rollback invocation to Ava Maintenance

Never automatically reverse project-owned edits.

# Completion report

Report:

- installed Ava base
- source compatible-through version
- semantic target
- final semantic status
- selected edge semantic-review decisions
- exact guidance documents applied
- every project-owned path inspected or changed and its recorded journal classification
- validations performed
- unresolved decisions
- whether finalization or another deterministic action remains for Ava Maintenance
- whether normal routing is available
