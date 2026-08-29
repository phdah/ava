---
type: Internal Development Task
title: Remove Inbox Ingestion Execution-Mechanism Restriction
description: Revert Finding 27's mechanism-level restriction while preserving Inbox Ingester authority, trust boundaries, semantic fidelity, provenance, source handling, and qualification safeguards.
tags: [internal, roadmap, dogfood, inbox, agents, qualification]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 34
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:openai-chatgpt
  at: 2026-08-29T11:50:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-29T13:20:00+02:00
---

# Remove Inbox Ingestion Execution-Mechanism Restriction

## Decision

Finding 27 introduced an explicit mechanism-level restriction during inbox ingestion. That restriction is not aligned with Ava's intended responsibility.

Ava should define the role's authority, trust boundaries, required outcomes, and semantic correctness rather than prescribe execution strategy. Removing Finding 27's restriction returns the role contract to those existing responsibilities without adding replacement execution guidance.

The resulting ingestion must still satisfy all applicable role constraints and output requirements, including trust, disposition, provenance, source preservation, validation, and bounded mutation authority.

## Motivation

Finding 27 addressed a real semantic-fidelity defect by constraining how ingestion could be performed. Findings 28 and 29 subsequently established the appropriate safeguards: correct per-passage disposition, rendered-output reconciliation, bounded structural evidence, and independent semantic audit.

Those requirements judge the result directly. The additional mechanism-level restriction is therefore unnecessary and belongs outside the role contract.

## Scope

- remove the Inbox Ingester instruction and constraint language added by Finding 27 that prescribes ingestion execution strategy
- add no replacement execution-mechanism guidance to the role
- remove qualification checks and regression coverage whose only purpose is to enforce Finding 27's execution restriction
- preserve the semantic fidelity, disposition, provenance, source-preservation, trust, validation, and final-state requirements established independently of Finding 27, especially Findings 28 and 29
- keep permanent project mutations bounded to the role's declared destination and maintenance authority
- record that this finding supersedes only Finding 27's execution-mechanism restriction, not the semantic defects that originally motivated Findings 28 and 29

## Completion criteria

- [x] Finding 27's execution-mechanism restriction is absent from Inbox Ingester instructions and constraints
- [x] no replacement execution-mechanism guidance is added to the role contract
- [x] role instructions continue to constrain authority, trust, fidelity, provenance, source handling, validation, and final project state
- [x] qualification no longer enforces Finding 27's mechanism-level restriction
- [x] Findings 28 and 29 semantic protections remain intact
- [x] affected role documentation, qualification coverage, and indexes are aligned
- [x] repository test suite passes

## Resolution evidence

- `templates/base/roles/inbox-ingester/instructions.md` and `constraints.md` remove the execution boundary introduced by Finding 27 without adding a replacement policy; `capabilities.md` remains unchanged.
- `templates/base/roles/inbox-ingester/log.md` records that this reverses only Finding 27's mechanism restriction. The rendered disposition-reconciliation requirement introduced by Finding 28 remains unchanged.
- `internal/release/qualification_runner.py` removes the transient direct-project-root watcher and the inbox-specific guard path. Complete inbox qualification still requires processed-source preservation, provenance, structural fidelity, installed conformance, and audit-gated `structural-pass` semantics.
- `internal/release/tests/test_qualification_runner.py` removes the former execution-restriction regression and pins the complete-inbox scenario's independent semantic-audit requirement.
- `internal/release/qualification-runner.md` and the release implementation log describe only the remaining outcome-based qualification requirements.
- The dogfood backlog and V1 release roadmap advance to assembling a new exact corrective-alpha candidate and rerunning the complete qualification flow. Finding 25 remains post-v1 and non-blocking.
- The repository test suite passes with these changes before the implementation PR is considered complete.
