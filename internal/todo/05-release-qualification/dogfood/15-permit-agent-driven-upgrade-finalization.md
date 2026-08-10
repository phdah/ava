---
type: Internal Development Task
title: Permit Agent-Driven Upgrade Finalization
description: Remove the instruction ambiguity that causes Ava Maintenance to look for a non-existent installer binary when finalizing an upgrade, and make explicit that the agent performs the finalization state transition directly.
tags: [internal, roadmap, dogfood, upgrades, finalization, maintenance]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 15
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.14
generated:
  by: agent:opencode
  at: 2026-08-10T11:53:37+02:00
---

# Permit Agent-Driven Upgrade Finalization

## Observed behavior

After semantic reconciliation completed successfully on an alpha.13 to alpha.14 upgrade, Ava Maintenance could not finalize the journal. The instructions say to "use the exact existing installer or updater operation" and "do not reproduce its state transitions manually," and the permitted-operation contract describes finalization as something the installer reports the journal as finalizable for.

With no installer binary on PATH and no `ava` command available, the role blocked and asked the user for an installer path rather than performing the state transition itself.

The user had to invoke a separate agent session to write the three terminal fields to `upgrade.json` (`status: complete`, `stage: complete`, `allowed_operations: ["normal"]`) and remove the transaction directory manually.

## Reproduction and evidence

Run a complete alpha.13 to alpha.14 upgrade through an agent session, completing both the managed commit and semantic reconciliation. When Ava Maintenance then attempts finalization, it searches for a binary called `ava` or for an updater executable path in the transaction. Finding neither, it blocks and presents a question about the installer rather than completing the upgrade.

Affected instructions:
- `distribution/upgrades.md` - Completion section and finalization description in "Abort, rollback, resume, and finalization"
- `templates/base/roles/ava-maintenance/instructions.md` - "Invoke finalization only when semantic compatibility is complete and the existing installer reports the journal as finalizable. Use the exact existing installer or updater operation."
- `templates/base/shared/instructions/upgrade-state-and-routing.md` - "Use existing installer or updater operations for deterministic mutation."

## Classification

This is a `blocker` for the next prerelease. Every upgrade finalization is blocked because Ava has no installer binary and will not have one. The agent is the mechanism for all state transitions, including finalization. Until this is corrected, no upgrade can complete without manual intervention.

## Root cause

The finalization instructions were written to protect against agents fabricating state transitions around a real installer that enforces checksums and preconditions. Since Ava has no installer binary and will not have one, the constraint has nothing to defer to and blocks the only available mechanism.

## Scope

The resolving PR must:

- update `distribution/upgrades.md` to remove the installer-invocation framing from finalization and state that Ava Maintenance writes the terminal state directly once semantic compatibility is confirmed complete
- update `templates/base/roles/ava-maintenance/instructions.md` to replace "invoke the existing installer finalization" with explicit authorization to write `status: complete`, `stage: complete`, `allowed_operations: ["normal"]` to `upgrade.json` and remove the transaction directory when the preconditions are met
- update `templates/base/shared/instructions/upgrade-state-and-routing.md` to replace "use existing installer or updater operations for deterministic mutation" with language that permits direct state writes for finalization and makes clear that the agent is the finalization mechanism
- ensure the preconditions Ava Maintenance must verify before writing the terminal state remain explicit: semantic compatibility is `complete`, no unresolved decisions remain, all managed changes are classified, and the journal is in `active/semantic` or an equivalent finalizable state
- leave all other deterministic mutation constraints intact; this change is scoped to finalization only

## Completion criteria

- [ ] An agent completing a successful upgrade can finalize the journal without searching for a binary or asking the user for an installer path.
- [ ] The three terminal fields (`status`, `stage`, `allowed_operations`) and transaction directory removal are explicitly authorized in the Ava Maintenance instructions.
- [ ] The preconditions for finalization are stated and must pass before the agent writes any terminal field.
- [ ] `distribution/upgrades.md`, `templates/base/roles/ava-maintenance/instructions.md`, and `templates/base/shared/instructions/upgrade-state-and-routing.md` are updated consistently.
- [ ] Affected indexes remain aligned.
- [ ] Concrete resolution and repository-validation evidence are recorded below.

## Resolution evidence

_To be completed in the resolving PR._

## Release qualification follow-up

Exercise a complete upgrade through a fresh agent session and confirm that Ava Maintenance writes the terminal state and removes the transaction directory without user intervention or binary lookup.
