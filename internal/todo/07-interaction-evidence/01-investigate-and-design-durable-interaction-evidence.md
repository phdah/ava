---
type: Internal Development Task
title: Investigate and Design Durable Interaction Evidence for Manual Semantic Changes
description: Define a privacy-aware provenance mechanism for semantic mutations supported or authorized directly by a user's conversational prompt.
tags: [internal, roadmap, provenance, interaction-evidence, metadata, inbox]
status: pending
phase: 7
order: 1
depends_on: 06-backlog-md
generated:
  by: agent:opencode
  at: 2026-08-13T11:49:53+02:00
---

# Investigate and Design Durable Interaction Evidence for Manual Semantic Changes

## Origin

This need was identified while carrying out the local alpha-verification work prompted as "on the next todo, which is to verify the alpha version."

A mutation role such as Project Steward may change existing trusted context based on information, confirmation, approval, correction, or a decision supplied directly by the user in a conversational prompt. The resulting knowledge document and its `updated` metadata identify the recording agent, and Git records the mutation, but neither necessarily preserves the human statement that supplied the facts or authority for the new state. Commit messages are not reliable canonical evidence.

Scoped `log.md` files remain reserved for meaningful conceptual, structural, ownership, classification, and compatibility history. Routine factual and task-state changes must not be added to those logs merely to preserve prompt evidence.

## Purpose

Investigate and design an explicit, durable, reviewable mechanism that can preserve the smallest complete part of a manual user prompt needed to understand a semantic mutation. Evaluate direct creation of a Markdown evidence document under a dedicated project-owned path such as project-root `inbox/processed/`, with the canonical destination referencing it through `sources` metadata and, when precision is useful, a Markdown footnote.

This task does not approve that path, representation, or authority model. Because adoption would change Ava's public format, ownership, and role-capability contracts, present the design and material alternatives for explicit user approval before recording or implementing an accepted architecture.

## Required design decisions

### Capture boundary

Define a deterministic threshold that captures interaction evidence only when the prompt itself supplies material facts, task-state changes, corrections, conflict resolutions, approvals, trusted-context retirement decisions, or other authority needed to understand a semantic mutation.

Explicitly exclude formatting, mechanical repairs, deterministic maintenance, invocation of an already-authorized operation, and changes fully supported by an existing durable source.

The mechanism must not become a transcript archive. Preserve the exact relevant user statement where possible and only the smallest complete statement needed to support the mutation. Define when limited surrounding context is necessary to prevent a quotation from becoming misleading or incomplete.

### Evidence and authority semantics

- distinguish the person who supplied or approved information from the role, agent, or tool that recorded it
- define how factual evidence differs from approval evidence
- specify that approval to apply a proposal establishes authority to mutate, while the proposal or another source may remain the evidence for factual claims
- ensure storage under `inbox/processed/` or another accepted path does not make content authoritative by location alone; the active role still interprets and validates the evidence
- define how corrections, conflict resolutions, retirement decisions, and later supersession affect an evidence record without rewriting the original human statement

### Record and reference model

- evaluate the canonical path, filename, Markdown structure, metadata, lifecycle, ownership, and indexing rules for interaction evidence
- define the minimum provenance needed for the human supplier or approver, recording role or tool, capture time, source interaction, and affected mutation without claiming identity guarantees the host cannot provide
- define when a canonical document uses `sources` metadata, a precise Markdown footnote, or both
- define stable link behavior for creation, movement, review, upgrade, and validation
- decide how attachments or non-text prompt inputs are referenced, minimized, copied, rejected, or redacted
- determine whether selected mutation roles may create processed evidence directly or must invoke a dedicated deterministic capture mechanism

### Privacy and safety

Define safeguards before any conversational content is persisted in Git, including:

- data minimization and relevance checks
- secret, credential, token, personal-data, and regulated-data handling
- user-visible disclosure or confirmation requirements
- redaction rules that do not silently alter the evidentiary meaning
- attachment handling and repository-size concerns
- behavior when safe durable capture is impossible
- deletion, correction, retention, and Git-history limitations

### Mutation integrity

Define how evidence creation and canonical mutation are completed atomically so a successful operation cannot leave a semantic change without its required evidence, an orphan evidence record, a broken link, or inconsistent provenance.

Specify validation, rollback, interruption recovery, concurrent-edit handling, and mutation-completion checks. Do not use interaction evidence as a replacement for scoped history when the same change independently meets the `log.md` threshold.

### Contract integration

If the direction is approved, identify and update the authoritative contracts governing:

- project-owned path and ownership classification
- inbox ingestion and processed-source lifecycle
- document metadata and `sources`
- role capabilities and constraints for semantic mutation
- mutation completion and atomicity
- change review and attribution checks
- installation, upgrade, validation, and compatibility behavior

Require reviewers to inspect available linked interaction evidence before concluding that a manual semantic mutation lacked authority or attribution. Also define how a reviewer reports missing required evidence without assuming that every manual change needs a captured prompt.

### Backlog.md compatibility

Complete the [Backlog.md integration](../06-backlog-md/) first and use its accepted task structure in this design. Interaction evidence may support a task-state mutation, but it must not duplicate task history, become a second backlog, or introduce a competing model for task status, approval, or completion.

## Evaluation scenarios

Test the proposed threshold and representation against at least:

1. a user supplies a new project fact directly
2. a user corrects trusted context that cites an older durable source
3. a user approves a proposal whose factual claims remain sourced elsewhere
4. a user resolves a conflict between durable sources
5. a user authorizes retirement of trusted context
6. a user marks a Backlog.md task complete through conversation
7. a user invokes an already-authorized deterministic operation
8. an agent performs a formatting-only or mechanical metadata repair
9. a prompt contains both relevant evidence and secrets or unrelated personal information
10. an attachment, image, or multi-turn exchange contains the material statement
11. evidence capture succeeds but the canonical mutation fails, and the inverse failure order
12. a mutation both needs interaction evidence and independently meets the scoped `log.md` threshold

## Constraints

- Do not treat Git commit messages as canonical interaction evidence.
- Do not persist complete transcripts by default.
- Do not paraphrase when the exact relevant user statement can be preserved safely and completely.
- Do not infer verified human identity from a conversational display name or agent-host metadata.
- Do not make all semantic mutations require interaction evidence when an existing durable source fully supports the change.
- Do not weaken current `log.md` thresholds or use evidence files as conceptual history substitutes.
- Do not grant new direct-write capability to mutation roles before the ownership and safety model is approved.
- Do not adopt a public format, mandatory path, or role-authority change without explicit user approval.

## Completion criteria

- the capture and exclusion thresholds are deterministic enough to apply consistently
- the factual-evidence and approval-evidence models are distinct and demonstrated through scenarios
- the proposed record preserves exact minimal statements and separates human supply or approval from agent recording provenance
- privacy, secrets, attachments, minimization, retention, and unsafe-capture behavior are defined
- path, ownership, metadata, links, lifecycle, supersession, and authority semantics are explicit
- atomic creation and mutation behavior, failure recovery, concurrency, and validation are defined
- the direct-role capability and deterministic-capture alternatives are evaluated with a recommendation
- scoped history remains independent and the reviewer contract accounts for available interaction evidence
- the accepted Backlog.md model remains the sole task-state and task-history representation
- all affected public contracts, roles, fixtures, upgrade impacts, and compatibility implications are identified
- the design is presented for explicit user approval before any accepted architecture or implementation is recorded
- after approval, adopted contract changes and regression coverage are completed directly or represented by bounded follow-up tasks
