---
type: Internal Development Task
title: Add Deterministic Resume and Abort Qualification Checkpoints
description: Provide a qualification-only harness that creates authentic interrupted upgrade states for repeatable end-to-end resume and abort testing.
tags: [internal, roadmap, dogfood, qualification, installer, recovery, transactions]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 17
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T11:21:21+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-14T11:40:00+02:00
---

# Add Deterministic Resume and Abort Qualification Checkpoints

## Observed behavior

During synthetic-vault qualification, the user finalized the 305-file corpus, materialized all eight qualification families, and successfully exercised managed-content damage, semantic reconciliation, finalization, rollback, uninstall, and reinstall behavior against published alpha assets.

The generated interrupted-upgrade plans require a maintained checkpoint harness for `--resume` and `--abort`, but no such harness existed. A normal installer invocation runs through transaction creation, staging, validation, managed mutation, commit, and cleanup without an operator-controlled pause. The required authentic intermediate states therefore could not be produced repeatably through the maintained fixture.

## Reproduction and evidence

`internal/release/fixtures/synthetic-qualification-vault/fixture.py` materializes `resume` and `abort` scenarios whose operations require the operator to install the source release, create an authentic interrupted target transaction, invoke the corresponding public recovery operation, and verify the terminal state.

The `--resume` and `--abort` lifecycle operations were already implemented by the distributed installer. The missing component was only a deterministic qualification mechanism for reaching the two durable transaction boundaries without fabricated state or timing-sensitive process termination.

## Classification

This was `required-v1` because deterministic resume and abort qualification is required before the release candidate. It was a qualification-fixture gap, not evidence that the implemented installer operations were defective.

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

- [x] One documented qualification command creates a real pre-live-mutation transaction that permits `abort`.
- [x] Invoking the assembled installer with `--abort` restores the source installation, removes only the owned transaction workspace, preserves project-owned content, and returns to normal routing.
- [x] One documented qualification command creates a real interrupted transaction with an incomplete managed commit that permits `resume`.
- [x] Invoking the assembled installer with `--resume` completes the deterministic target transition or reaches the target's authentic semantic stage, as declared by the selected upgrade edge.
- [x] Resume rejects unrelated managed edits and accepts only source, current, or target checksums recorded by the transaction.
- [x] Neither checkpoint relies on timing-sensitive process termination or manually fabricated managed state.
- [x] Qualification-only checkpoint controls cannot enter assembled release assets or add a public installer mode.
- [x] The synthetic execution plans identify the maintained commands and expected terminal states without claiming planned state as execution evidence.
- [x] Automated regression coverage executes both operations and validates transaction cleanup and project-owned preservation.
- [x] The complete release suite includes repository boundary validation and the new checkpoint regression module.

## Resolution evidence

- `internal/release/fixtures/synthetic-qualification-vault/checkpoint.py` executes the Python payload from the exact assembled target `ava-install.sh`, removes only its top-level command dispatcher in memory, and interrupts existing atomic transaction boundaries with a `BaseException` so installer rollback does not erase the deliberately captured state.
- The abort checkpoint is captured only after the real installer has durably created its plan, backup, candidate workspace, and `active/staged` journal with `live_mutation_started: false` and `managed_commit_complete: false`.
- The resume checkpoint is captured only after the real installer has entered `active/validating`, performed managed writes, and immediately before the live target manifest commit, leaving the source manifest live and the authentic candidate, plan, backup, and staging state intact.
- The harness verifies candidate target identity, transaction structure, source/current/target checksum admissibility, and unchanged project-owned inventory before returning checkpoint JSON.
- `checkpoints.md` defines the exact qualification commands, expected checkpoint states, real assembled `--abort` and `--resume` invocations, terminal acceptance states, and the rule that checkpoint JSON is setup evidence rather than accepted execution evidence.
- `test_qualification_checkpoints.py` executes both real recovery operations, validates source restoration and target completion, checks transaction cleanup and project-owned preservation, proves unrelated managed edits produce `RESUME_CONFLICT`, proves a recorded source checksum remains resumable, and verifies the harness does not enter assembled release assets.
- `internal/release/test.sh` registers the new regression module and invokes `validate-boundaries.sh`; the boundary validator requires and compiles the qualification-only harness while keeping it outside distributed sources.

## Qualification follow-up

The repository finding is complete. Re-prepare only the affected interrupted-upgrade workspaces as the fixture contract permits, execute both checkpoint commands and the real `--resume` and `--abort` operations against the selected qualification assets, then record their terminal states and user signoff in the synthetic-vault run evidence. This published-asset exercise remains a release qualification gate and does not return this implementation finding to pending.
