---
type: Internal Development Task
title: Preserve Large-Batch Inbox Fidelity and Claim Provenance
description: Make delegated and large-batch inbox ingestion retain complete per-source section evidence, cross-source claim provenance, and coordinator-owned final reconciliation.
tags: [internal, roadmap, dogfood, inbox, provenance, delegation, qualification]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 20
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:openai-chatgpt
  at: 2026-08-15T00:19:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-15T00:19:00+02:00
---

# Preserve Large-Batch Inbox Fidelity and Claim Provenance

## Observed behavior

The full synthetic `alpha.13 -> alpha.14` qualification processed all 305 inbox sources and the deterministic runner reached an all-pass result, but the independent audit found that the completed knowledge could not prove faithful coverage and claim provenance across the delegated ingestion batch.

The audit reported two related major findings:

- `QUA-INBOX-ORACLE-001`: the final result could not be independently reconciled to all expected source meaning
- `QUA-INBOX-PROVENANCE-002`: source-specific and conflicting reports were not consistently traceable with the required claim-level attribution

The qualification sessions under test were correct not to read the hidden fixture oracle. The defect is not oracle access. The oracle is evaluator-only expected-outcome evidence. The defect is that large-batch execution did not retain enough coordinator-owned, per-source evidence to prove that every selected source and substantive section was handled faithfully, especially after work was split across child sessions.

## Reproduction and evidence

Run the complete pending-inbox synthetic scenario with the finalized 305-source corpus and allow the host to split the work across child sessions.

The historical qualification audit found that:

- the parent and child sessions reported successful completion and all pending source files were moved
- source-section counts were reported by the execution, but batch success could not be reconciled source-by-source from the retained child evidence
- many mapped source-specific claims that required precise attribution were not traceable from the final canonical knowledge to their supporting source passages
- the deterministic runner accepted the scenario because the direct inbox was empty and installed conformance passed, while the later semantic audit found major fidelity gaps

This demonstrates a scale and delegation gap in the implementation of the existing faithful-ingestion contract rather than a reason to expose qualification oracle data to the Inbox Ingester.

## Classification

This is `required-v1` and blocks release-candidate acceptance. Faithful ingestion and provenance are core v1 behavior, and the realistic qualification corpus exposed a failure mode that smaller regression cases did not cover.

The finding does not make child sessions invalid. Parallelism remains permitted as an execution strategy, but it must not weaken the parent Inbox Ingester's completion responsibility.

## Root cause

The existing fidelity contract defines strong per-source requirements but did not make the evidence boundary explicit when a large batch is split across child sessions.

A parent session could therefore accept child success summaries and aggregate counts without retaining one exact selected-source ledger that proves:

- each selected source was owned exactly once
- every substantive section had a defensible disposition
- every mapped section reached its stated destination
- source-specific claims retained required claim-level provenance
- cross-child contributions to the same destination preserved differences in author, date, chronology, certainty, status, proposal, decision, and outcome
- final counts reconciled to the original selected-source inventory and final filesystem state

## Scope

The resolving change must:

- keep the substantive-section inventory derived from the actual selected sources rather than from qualification expected-answer data
- define coordinator ownership of one exact selected-source ledger for every batch
- require child work, when used, to operate on explicit disjoint source subsets and return complete per-source section, destination, provenance, blocker, validation, and final-state evidence
- make child success provisional until the coordinator reconciles all selected sources exactly once
- prevent batch completion when child evidence is missing, overlapping, or cannot be reconciled to the final pending and processed inventories
- make precise claim attribution mandatory where differing source reports could otherwise be confused with each other or with canonical project state
- require cross-child destination reconciliation before a complete batch claim
- extend realistic regression fixtures and tests for delegated evidence loss
- preserve the separation between deterministic validation and independent semantic review

## Completion criteria

- [x] The shared fidelity contract defines delegated and large-batch completion responsibility.
- [x] The `ingest-inbox` workflow retains the exact selected-source inventory and requires reconciled child evidence when execution is split.
- [x] Precise attribution criteria cover source-specific differences in author, date, chronology, certainty, status, proposals, decisions, and outcomes.
- [x] Missing or overlapping child evidence prevents a complete batch claim.
- [x] Regression fixtures include a delegated batch whose missing per-source evidence must fail completion.
- [x] Regression tests enforce coordinator-owned reconciliation and cross-source provenance requirements.
- [x] Qualification oracle data remains evaluator-only and is not made an Inbox Ingester dependency.

## Resolution evidence

The implementation strengthens `templates/base/shared/instructions/inbox-ingestion-fidelity.md` with explicit delegated and large-batch semantics. The coordinating Inbox Ingester owns one selected-source ledger, child sessions return complete per-source evidence for disjoint subsets, child success is provisional, and final batch counts are accepted only after exact reconciliation.

`templates/base/workflows/ingest-inbox.md` now carries those requirements into the workflow procedure and expected output. It also requires precise claim-level provenance whenever source-specific reports could otherwise be confused across child boundaries.

`internal/release/fixtures/inbox-ingestion-fidelity.json` adds a delegated-batch failure case, and `internal/release/tests/test_inbox_ingestion_fidelity.py` enforces the coordinator ledger, disjoint child ownership, provisional child success, missing-evidence failure, and strengthened attribution rules.

## Release qualification follow-up

Rerun the complete synthetic pending-inbox scenario through the corrective release. The independent audit, using the hidden oracle as evaluator evidence, must be able to reconcile every selected source and substantive expected outcome without a blocking or major inbox-fidelity or provenance finding.
