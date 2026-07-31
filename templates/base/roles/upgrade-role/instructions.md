---
type: Role Instructions
title: Upgrade Role Instructions
description: Procedure for applying installed release guidance and completing or blocking semantic compatibility.
tags: [ava, role, upgrades, migration, instructions]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T15:35:00+02:00
---

# Entry procedure

Before changing project-owned context:

1. Read the managed manifest and upgrade journal.
2. Confirm the installed base, compatible-through version, target version, journal status, stage, and allowed operations.
3. Confirm that `reconcile-semantic` or the narrower requested recovery operation is permitted.
4. Resolve the exact relative guidance paths recorded by the transaction beneath `/.ava/guidance/`, in order.
5. Validate each guidance document against the release-guidance contract and its transaction edge.
6. Stop without mutation when managed state or guidance cannot establish safe authority.

# Impact analysis

For every loaded guidance document:

1. Identify changed managed contracts and their project-facing semantic impact.
2. Resolve cumulative obligations and explicit supersession across the guidance chain.
3. Build a bounded inventory from the affected concept conditions in the guidance.
4. Inspect affected registries, indexes, canonical paths, references, metadata, and scoped history.
5. Separate deterministic work already completed from semantic project-owned work.
6. Identify required decisions that project intent cannot resolve.

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
5. append or update the path in `upgrade.json.project_changes`
6. validate the changed document and its relationships

A migration is not complete while any required role, workflow, registry, index, log, metadata field, link, filename, or structural convention remains inconsistent with the target contract.

# Semantic state transitions

The role may transition semantic compatibility only as allowed by the versioning contract:

- `pending` to `partial`, `blocked`, or `complete`
- `partial` to `blocked` or `complete`
- `blocked` to `partial` or `complete` after blocking conditions are resolved

Use `partial` only when safe required work has been applied but completion criteria remain unmet without a current blocking decision. Use `blocked` when a decision, prerequisite, host limitation, or invalid managed input prevents safe continuation.

Mark `complete` only when:

- every loaded guidance completion criterion passes
- every affected project relationship is consistent
- `unresolved_decisions` is empty
- `compatible_through` can advance exactly to installed `ava_version`
- `target_version` can be cleared
- the journal can reach `complete/complete` with `allowed_operations: [normal]`

# Rollback support

The Upgrade Role does not perform managed rollback.

When rollback is requested after project-owned edits:

1. report every recorded project path
2. determine whether each edit remains compatible with the source release
3. mark each journal resolution as retained, reverted, or reconciled only with evidence
4. update project-owned context only when the user explicitly chooses a safe source-compatible resolution
5. keep rollback blocked until source semantic compatibility is validated

Never automatically reverse project-owned edits.

# Completion report

Report:

- installed Ava base
- source compatible-through version
- semantic target
- final semantic status
- guidance documents applied
- changed project-owned paths
- validations performed
- unresolved decisions
- whether normal routing is available
