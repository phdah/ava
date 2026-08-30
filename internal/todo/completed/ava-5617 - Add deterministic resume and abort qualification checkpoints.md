---
id: ava-5617
title: "Add deterministic resume and abort qualification checkpoints"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5617
---

## Description

Provide a qualification-only harness that creates authentic interrupted upgrade states for repeatable end-to-end resume and abort testing.

## Migrated task record

Historical metadata: phase 5 finding 17, `required-v1`, blocking release candidate, affected version `1.0.0-alpha.14`, completed after implementation.

### Problem and scope

The synthetic vault could exercise most lifecycle states but had no deterministic way to reach authentic intermediate states for public `--resume` and `--abort`. Normal installer runs do not pause at operator-controlled durable boundaries, and fabricated journal/manifest/staging data was intentionally prohibited. The missing component was a qualification harness, not a defect in the already implemented recovery operations.

The task required an internal-only checkpoint mechanism using real transaction machinery, no public installer mode, real assembled recovery operations, checksum/state/routing/project-owned preservation checks, maintained execution-plan integration, and regression coverage for cleanup and preservation.

### Resolution evidence

`internal/release/fixtures/synthetic-qualification-vault/checkpoint.py` executes the exact assembled target installer payload, removes only its top-level dispatcher in memory, and uses controlled `BaseException` interruption at existing atomic boundaries so normal rollback does not erase the deliberately captured state. Abort state is captured after authentic plan/backup/candidate/staging and an `active/staged` journal before live mutation. Resume state is captured during `active/validating` immediately before live target-manifest commit, leaving the source manifest live and authentic transaction artifacts intact.

The harness verifies target identity, transaction structure, admissible source/current/target checksums, and unchanged project-owned inventory. `checkpoints.md` documents setup commands, expected states, real recovery operations, terminal acceptance and the rule that checkpoint JSON is setup rather than execution evidence. `test_qualification_checkpoints.py` executes both recovery operations, validates restoration/target completion/cleanup/preservation, proves unrelated managed edits cause `RESUME_CONFLICT`, accepts recorded source checksums, and proves the harness is excluded from release assets. `internal/release/test.sh` and boundary validation compile/test it while keeping it internal.

Repository implementation is complete. Published qualification still had to recreate only the affected workspaces, execute checkpoint plus real recovery commands against selected assets, and record terminal evidence/signoff without reopening this task.