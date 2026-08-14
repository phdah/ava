---
type: Internal Development Task
title: Add Deterministic Resume and Abort Qualification Checkpoints
description: Provide a qualification-only harness that creates authentic interrupted upgrade states for repeatable end-to-end resume and abort testing.
tags: [internal, roadmap, dogfood, qualification, installer, recovery, transactions]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 17
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T11:21:21+02:00
---

# Add Deterministic Resume and Abort Qualification Checkpoints

## Observed behavior

During synthetic-vault qualification, the user finalized the 305-file corpus, materialized all eight qualification families, and successfully exercised managed-content damage, semantic reconciliation, finalization, rollback, uninstall, and reinstall behavior against published alpha assets.

The generated interrupted-upgrade plans require a maintained checkpoint harness for `--resume` and `--abort`, but no such harness exists. A normal installer invocation runs through transaction creation, staging, validation, managed mutation, commit, and cleanup without an operator-controlled pause. The required authentic intermediate states therefore cannot be produced repeatably through the maintained fixture.

## Reproduction and evidence

`internal/release/fixtures/synthetic-qualification-vault/fixture.py` materializes `resume` and `abort` scenarios whose operations require the operator to:

1. install the declared source release
2. start the target upgrade with the maintained checkpoint harness
3. capture a checkpoint valid for the selected operation
4. invoke `--resume` or `--abort` and verify the terminal state

The `--resume` and `--abort` lifecycle operations are implemented by the distributed installer, but the referenced checkpoint harness is absent. Existing Ava Maintenance fixtures define the expected routing and operation, while the conformance matrix cites those declarative cases rather than an end-to-end installer interruption for resume and abort.

Rollback remains independently executable because a semantic-review-required upgrade naturally leaves a real active transaction after managed commit. Abort requires a durable pre-live-mutation transaction, and resume requires a durable incomplete managed commit with its genuine plan, backup, candidate, and staging state intact.

## Classification

This is `required-v1` and blocks the release candidate until deterministic resume and abort qualification can be executed. It is a qualification-fixture gap, not evidence that the implemented installer operations are defective.

## Root cause

The synthetic qualification design specified authentic interrupted-upgrade coverage and correctly prohibited fabricated managed state, but fixture implementation stopped at generating execution plans. It did not provide the deterministic mechanism needed to pause a real transaction at the two required durable boundaries.

## Scope

- add an internal, qualification-only checkpoint harness for authentic abortable and resumable upgrade states
- build checkpoints through real transaction machinery rather than hand-authored manifest, journal, plan, backup, candidate, or staging data
- keep checkpoint controls out of the distributed user-facing installer interface and release payload
- exercise the real assembled installer `--abort` and `--resume` operations against the resulting states
- verify source and target managed checksums, transaction cleanup, semantic state, routing state, and project-owned preservation
- connect the synthetic-vault execution plans and maintained conformance evidence to the executable scenarios

## Completion criteria

- [ ] One documented qualification command creates a real pre-live-mutation transaction that permits `abort`.
- [ ] Invoking the assembled installer with `--abort` restores the source installation, removes only the owned transaction workspace, preserves project-owned content, and returns to normal routing.
- [ ] One documented qualification command creates a real interrupted transaction with an incomplete managed commit that permits `resume`.
- [ ] Invoking the assembled installer with `--resume` completes the deterministic target transition or reaches the target's authentic semantic stage, as declared by the selected upgrade edge.
- [ ] Resume rejects unrelated managed edits and accepts only source, current, or target checksums recorded by the transaction.
- [ ] Neither checkpoint relies on timing-sensitive process termination or manually fabricated managed state.
- [ ] Qualification-only checkpoint controls cannot enter assembled release assets or add a public installer mode.
- [ ] The synthetic execution plans identify the maintained commands and expected terminal states without claiming planned state as execution evidence.
- [ ] Automated regression coverage executes both operations and validates transaction cleanup and project-owned preservation.
- [ ] The complete release suite and repository boundary validation pass.

## Qualification follow-up

After implementation, re-materialize or prepare only the affected interrupted-upgrade workspaces as the fixture contract permits, execute both scenarios against the selected qualification assets, and record user signoff for the resulting terminal states.
