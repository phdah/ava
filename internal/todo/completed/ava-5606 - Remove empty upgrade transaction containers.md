---
id: ava-5606
title: "Remove empty upgrade transaction containers"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5606
---

## Description

Ensure terminal installer cleanup removes the empty managed transaction container after its final upgrade transaction is deleted. This task preserves the finding and resolution evidence.

## Migrated task record

Historical metadata: phase 5 finding 6, `blocker`, blocking the next prerelease, affected version `1.0.0-alpha.7`, completed after implementation.

### Observed behavior

A real alpha.6-to-alpha.7 upgrade retained all 54 payload files, reached a terminal complete journal, advanced semantic compatibility, and permitted normal routing, but left an empty `./.ava/state/transactions/` directory. Ava Maintenance therefore reported an otherwise healthy installation as unhealthy because the unrecorded empty structural artifact remained. Installed conformance did not classify the empty directory as a payload error, but it still made managed state ambiguous.

### Root cause

Upgrade workspaces lived beneath `./.ava/state/transactions/<transaction-id>/`. Terminal cleanup removed the transaction-specific directory but attempted parent removal only for fresh-install storage under `.ava-install/`, leaving the empty upgrade parent behind.

### Scope and completion criteria

The approved fix centralized terminal cleanup: remove the specific workspace first, then its immediate parent only when empty; apply this to successful completion and terminal recovery paths; preserve the container when other transaction/recovery artifacts remain; keep active/blocked state durable; retain filesystem-safety guarantees; and cover success, active-state preservation, non-empty parent guarding, idempotency, rollback and abort behavior. A semantic-complete final transaction had to remove the parent, while active/non-empty states had to preserve it.

### Resolution evidence

Merged PR #62 implemented one terminal cleanup helper across successful upgrade completion, resumed completion, rollback, abort, finalization, and failed recovery. It removes the transaction workspace and then uses guarded empty-parent removal, so unrelated entries prevent deletion. Regression coverage verified semantic-complete cleanup, active semantic preservation until rollback, rollback cleanup, and preservation of unrelated transaction/recovery artifacts. Python tests, Release PR policy, and conventional-title checks passed, and repository docs/roadmap evidence were aligned.

The following corrective immutable release still had a release-gate follow-up to perform real supported-source upgrades, confirm no empty transaction container remains, and pass Ava Maintenance integrity inspection. That evidence does not reopen this completed implementation task.