---
id: ava-701
title: >-
  Investigate and design durable interaction evidence for manual semantic
  changes
status: Done
assignee: []
created_date: ''
updated_date: '2026-08-31 08:19'
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

Define a privacy-aware provenance mechanism for semantic mutations supported or authorized directly by a user's conversational prompt. Design the mechanism first and require explicit user approval before recording a new public format or role-authority architecture. After approval, implement the accepted design as part of this task.

## Purpose

A mutation role may change trusted context from facts, corrections, approvals, conflict resolutions, task-state changes, or retirement decisions supplied directly in conversation. Existing `updated` metadata identifies the recording agent and Git records the mutation, but neither necessarily preserves the human statement that supplied the fact or authority. Commit messages are not canonical evidence, and scoped `log.md` must remain reserved for meaningful conceptual or structural history rather than routine prompt provenance.

Interaction evidence must preserve only the minimum safe source statement required to understand a semantic mutation and must remain ordinary project-owned source provenance rather than a parallel authority, history, or task system.

## Required design decisions

### Capture boundary

Define deterministic inclusion and exclusion rules. Capture only material user-supplied facts, task-state changes, corrections, conflict resolutions, approvals, retirement decisions, or other authority necessary to understand a semantic mutation. Exclude formatting, mechanical repairs, already-authorized deterministic operations, and changes fully supported by an existing durable source.

Do not create a transcript archive. Preserve the smallest complete exact user statement needed for the mutation, with only enough surrounding context to avoid misleading evidence.

### Evidence and authority semantics

Distinguish the human supplier or approver from the role or tool that records the evidence. Separate factual evidence from approval evidence. Approval may authorize mutation while a proposal or existing source remains factual evidence. Storage location must not itself make content authoritative.

Define correction, conflict-resolution, retirement, and later supersession semantics without rewriting original evidence.

### Record and reference model

Define path, filename, Markdown structure, metadata, lifecycle, ownership, indexing, provenance fields, `sources` references, precise footnotes, attachment handling, and whether mutation roles may create evidence directly or require deterministic tooling.

Do not infer verified human identity from display names or host metadata.

### Privacy and safety

Define minimization, secret and token handling, personal or regulated data behavior, disclosure and confirmation, redaction boundaries, attachment and repository-size handling, unsafe-capture fallback, deletion, correction, retention, and Git-history limitations.

### Mutation integrity

Define atomic evidence creation plus semantic mutation, rollback and interruption recovery, concurrent edits, validation, and completion checks. A successful operation must not leave a semantic mutation without required evidence, an orphan evidence record, a broken link, or inconsistent provenance.

Interaction evidence does not replace scoped conceptual history when the same mutation independently crosses the `log.md` threshold.

### Contract integration

Integrate the approved design into project-owned source handling, document provenance, mutation-role capability and required reading, task-state handling, independent change review, validation, installation behavior, upgrade behavior, and compatibility expectations without creating a new runtime service or managed state.

### Backlog.md compatibility

Backlog.md remains the sole task-state model. Interaction evidence may support a task-state mutation but must not duplicate task history or introduce competing task lifecycle semantics.

## Evaluation scenarios

Cover at least: direct new fact, correction of sourced context, approval of a proposal, conflict resolution, trusted-context retirement, conversational completion of a Backlog task, already-authorized deterministic operation, formatting-only repair, mixed relevant and secret prompt, attachment or multi-turn evidence, either-side atomic failure, and a mutation that also meets the scoped-history threshold.

## Constraints

- Git commit messages are not canonical interaction evidence.
- Do not persist full transcripts by default.
- Preserve exact relevant wording when safely possible rather than paraphrasing.
- Do not infer verified human identity.
- Do not require interaction evidence when an existing durable source fully supports the mutation.
- Do not weaken scoped-history thresholds.
- Do not grant a role new semantic target authority through evidence capture.
- Backlog.md remains the sole task-state model.
- Do not introduce a runtime service, transcript database, identity system, or new managed state.

## Completion criteria

- deterministic capture and exclusion thresholds
- distinct factual versus approval evidence models
- minimal exact-statement representation and separate human and agent provenance
- complete privacy, secrets, attachment, minimization, retention, and unsafe-capture rules
- explicit path, ownership, metadata, lifecycle, links, supersession, and authority semantics
- atomic mutation and evidence behavior with recovery and validation
- direct role capture versus deterministic helper evaluated and resolved
- independent scoped-history and review semantics
- Backlog.md remains the sole task-state model
- affected managed roles and public behavior are updated after explicit user approval
- deterministic validation and regression coverage are implemented
- installation does not create an interaction-specific source hierarchy
- upgrade behavior is prospective and does not fabricate historical evidence

## Approval and implementation result

The user explicitly rejected stopping at the design stage and authorized implementation. During implementation the user also made a material storage decision: conversational evidence must be handled like other successfully ingested source material and stored directly under `./inbox/processed/`, not under a dedicated `interactions/` hierarchy.

The accepted model is therefore:

```text
./inbox/processed/interaction-<opaque-id>.md
```

The filename and `type: Interaction Evidence` metadata identify the source form. The processed-source tree remains generic and does not gain an interaction-specific collection or index.

### Implemented contract

`templates/base/shared/instructions/interaction-evidence.md` now defines:

- the mandatory capture and exclusion threshold;
- minimal exact-statement preservation;
- factual versus authorization semantics;
- direct processed-source storage and no pending duplicate;
- narrow ancillary evidence authority for already-authorized mutation roles;
- actor and supplier separation without inferred identity verification;
- safe redaction, secret handling, sensitive-data minimization, attachments, retention, and Git-history limitations;
- append-only correction, retirement, conflict-resolution, and supersession semantics;
- target `sources` provenance for ordinary Markdown and normal Markdown evidence links for Backlog.md tasks;
- one logical transaction across evidence, target mutation, and reverse reference;
- recovery rules for either-side partial failure and collision-safe concurrent IDs;
- independent scoped-history semantics;
- prospective upgrade behavior without historical evidence synthesis;
- Change Reviewer interpretation of factual versus authorization evidence.

### Role integration

The shared contract is mandatory required reading for Project Steward, Role Manager, Inbox Ingester, Project Task Manager, and Upgrade Role because each can perform semantic project-owned mutations that may depend on conversational authority.

Project Steward, Role Manager, Inbox Ingester, Project Task Manager, and Upgrade Role now have explicit narrow capabilities to create the required processed interaction source for their own already-authorized mutations. This does not grant general inbox authority or broaden semantic target authority.

Change Reviewer remains read-only and loads the interaction-evidence contract only when the reviewed change contains linked interaction evidence, depends materially on conversational authority, or requires provenance assessment.

### Deterministic validation

`internal/release/interaction_evidence.py` validates processed interaction evidence without interpreting conversational meaning. It checks:

- direct `inbox/processed/` placement and rejects an interaction-specific subdirectory;
- metadata shape, generated actor, evidence kind, supplier boundary, ID shape, and filename binding;
- duplicate interaction IDs;
- project-owned target safety and existence;
- reverse references from every target to the evidence source;
- supersession paths and source type;
- required exact quoted statement content.

The unified installed-project conformance path runs this validation. Regression coverage includes valid evidence, forbidden interaction-specific hierarchy, missing targets, missing reverse references, duplicate IDs, invalid supersession, supplier violations, and missing exact statements.

### Compatibility and release behavior

The new capture obligation changes managed mutation and review behavior and is compatibility-sensitive. It applies prospectively once a release containing the new managed base becomes active. Existing projects must not receive fabricated historical prompt evidence during upgrade.

Release guidance for the release edge introducing this behavior must explain the new prospective obligation and any project-owned semantic review required by the release process. No new managed state, ownership class, runtime component, or installer-created interaction directory is required.

## Completion evidence

AVA-701 is complete as both a design and implementation task. The implementation uses the existing processed inbox source boundary rather than a source-type hierarchy, preserves Backlog.md as the sole task-state model, keeps scoped history independent, grants only bounded ancillary evidence-write authority, and includes deterministic conformance validation plus regression coverage.
