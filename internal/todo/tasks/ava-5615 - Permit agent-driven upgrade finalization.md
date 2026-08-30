---
id: ava-5615
title: "Permit agent-driven upgrade finalization"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5615
---

## Description

Remove instruction ambiguity that caused Ava Maintenance to look for a nonexistent installer binary when finalizing an upgrade, and make the bounded terminal transition agent-driven.

## Migrated task record

Historical metadata: phase 5 finding 15, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.14`, completed after implementation.

### Observed behavior and root cause

After successful alpha.13-to-alpha.14 semantic reconciliation, Ava Maintenance could not finalize because its instructions said to use the exact existing installer/updater operation and not reproduce state transitions manually. No `ava` binary or installer path existed, so the role blocked and the user had to use another agent session to write terminal journal fields and remove the transaction directory. The protective installer framing had no mechanism to defer to and blocked the only available successful-finalization mechanism.

### Approved scope

Finalization alone was changed. Ava Maintenance may directly record `status: complete`, `stage: complete`, `allowed_operations: ["normal"]` and remove the exact recorded transaction workspace only after proving semantic compatibility is complete, unresolved decisions are absent, managed changes are classified, and the journal is in a finalizable active semantic/post-commit state. Explicit upgrade, resume, abort, rollback, repair, semantic-state changes and other non-terminal deterministic mutation remain installer-backed or outside this exception.

### Resolution evidence

`distribution/upgrades.md` now defines successful finalization as a bounded Ava Maintenance terminal transition after journal and semantic validation. Ava Maintenance role/instructions/capabilities/constraints/history consistently describe this as the only direct journal-write exception. `upgrade-state-and-routing.md` names Ava Maintenance as the finalization mechanism and forbids searching for an `ava` binary or updater solely to finalize.

`internal/release/fixtures/ava-maintenance.json` records required preconditions, exact terminal state, cleanup and `requires_installer_binary: false`; recovery fixtures still require installer mechanisms for abort/resume/rollback. `test_ava_maintenance.py` enforces the split, exact state, bounded cleanup and preconditions inside `internal/release/test.sh`. Related role/fixture/dogfood/phase/roadmap state was synchronized.

Release follow-up required a fresh-agent complete upgrade proving Ava Maintenance performs terminal state and cleanup without user intervention or binary lookup.