---
id: ava-701
title: >-
  Investigate and design durable interaction evidence for manual semantic
  changes
status: To Do
assignee: []
created_date: ''
updated_date: '2026-08-30 18:26'
labels:
  - internal
  - roadmap
  - phase-07
  - provenance
  - interaction-evidence
  - metadata
milestone: m-0
dependencies:
  - ava-602
ordinal: 701
---

## Description

Define a privacy-aware provenance mechanism for semantic mutations supported or authorized directly by a user's conversational prompt. This is a proposal/design task and must not record or implement a new public format or role-authority architecture without explicit user approval.

## Purpose

A mutation role may change trusted context from facts, corrections, approvals, conflict resolutions, task-state changes, or retirement decisions supplied directly in conversation. Existing `updated` metadata identifies the recording agent and Git records the mutation, but neither necessarily preserves the human statement that supplied the fact or authority. Commit messages are not canonical evidence, and scoped `log.md` must remain reserved for meaningful conceptual/structural history rather than routine prompt provenance.

Investigate a durable, minimal evidence model, potentially using narrowly scoped project-owned processed evidence referenced from canonical destinations through `sources` metadata and precise Markdown attribution where useful. The exact path, representation, and authority model remain undecided until user approval.

## Required design decisions

### Capture boundary

Define deterministic inclusion/exclusion rules. Capture only material user-supplied facts, task-state changes, corrections, conflict resolutions, approvals, retirement decisions, or other authority necessary to understand a semantic mutation. Exclude formatting, mechanical repairs, already-authorized deterministic operations, and changes fully supported by an existing durable source.

Do not create a transcript archive. Preserve the smallest complete exact user statement needed for the mutation, with only enough surrounding context to avoid misleading evidence.

### Evidence and authority semantics

Distinguish the human supplier/approver from the role or tool that records the evidence. Separate factual evidence from approval evidence. Approval may authorize mutation while a proposal or existing source remains factual evidence. Storage location must not itself make content authoritative.

Define correction, conflict-resolution, retirement, and later supersession semantics without rewriting original evidence.

### Record/reference model

Evaluate canonical path, filename, Markdown structure, metadata, lifecycle, ownership, indexing, provenance fields, `sources` references, precise footnotes, attachment handling, and whether mutation roles may create evidence directly or must invoke a bounded deterministic capture mechanism.

Do not infer verified human identity from display names or host metadata.

### Privacy and safety

Define minimization, secret/token handling, personal or regulated data behavior, user-visible disclosure/confirmation, redaction boundaries, attachment/repository-size handling, unsafe-capture fallback, deletion/correction/retention, and Git-history limitations.

### Mutation integrity

Define atomic evidence creation plus semantic mutation, rollback/interruption recovery, concurrent edits, validation, and completion checks. A successful operation must not leave a semantic mutation without required evidence, an orphan evidence record, a broken link, or inconsistent provenance.

Interaction evidence does not replace scoped conceptual history when the same mutation independently crosses the `log.md` threshold.

### Contract integration

If approved, identify required changes to project-owned path/ownership rules, inbox/processed lifecycle, document metadata and `sources`, mutation-role capabilities/constraints, mutation completion, change review, installation/upgrade/validation, and compatibility contracts.

Reviewers should inspect available linked interaction evidence before concluding a manual semantic mutation lacks authority, while still recognizing that not every manual change requires captured prompt evidence.

### Backlog.md compatibility

Use the accepted Backlog.md model from AVA-601/602. Interaction evidence may support a task-state mutation but must not duplicate task history, become a second backlog, or introduce competing task lifecycle/approval semantics.

## Evaluation scenarios

Cover at least: direct new fact, correction of sourced context, approval of a proposal, conflict resolution, trusted-context retirement, conversational completion of a Backlog task, already-authorized deterministic operation, formatting-only repair, mixed relevant/secret prompt, attachment or multi-turn evidence, either-side atomic failure, and a mutation that also meets the scoped-history threshold.

## Constraints

- Git commit messages are not canonical interaction evidence
- do not persist full transcripts by default
- preserve exact relevant wording when safely possible rather than paraphrasing
- do not infer verified human identity
- do not require interaction evidence when an existing durable source fully supports the mutation
- do not weaken scoped-history thresholds
- do not grant new mutation-role write authority before the ownership/safety model is approved
- do not adopt a mandatory public path/format/authority change without explicit user approval

## Completion criteria

- deterministic capture/exclusion thresholds
- distinct factual versus approval evidence models
- minimal exact-statement representation and separate human/agent provenance
- complete privacy, secrets, attachment, minimization, retention, and unsafe-capture rules
- explicit path, ownership, metadata, lifecycle, links, supersession, and authority semantics
- atomic mutation/evidence behavior and recovery/validation model
- evaluated direct-role versus deterministic-capture alternatives with recommendation
- independent scoped-history and review semantics
- Backlog.md remains the sole task-state model
- affected public contracts/roles/fixtures/upgrade impacts are identified
- design is presented for explicit user approval before architecture is recorded or implemented

This follows AVA-602 and is tracked toward the `v1.0.0` milestone rather than resuming the former parked V1 release-task path.
