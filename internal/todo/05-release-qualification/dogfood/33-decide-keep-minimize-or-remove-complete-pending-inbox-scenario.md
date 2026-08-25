---
type: Internal Development Task
title: Decide Whether to Keep, Shrink, or Remove the Complete-Pending-Inbox Qualification Scenario
description: Evaluate whether the 305-source complete-pending-inbox scenario should remain as-is, be shrunk to a smaller representative batch, or be removed from the maintained qualification matrix, given its outsized multi-hour cost relative to the rest of the matrix.
tags: [internal, roadmap, dogfood, release, qualification, reliability, inbox, performance]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 33
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-25T17:13:00+02:00
---

# Decide Whether to Keep, Shrink, or Remove the Complete-Pending-Inbox Qualification Scenario

## Observed behavior

`complete-pending-inbox` alone can now take well over an hour (observed roughly 2+ hours on 2026-08-25, run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local`), compared to under 20 minutes before the inbox-fidelity constraints were tightened by findings 27 and 28. This inflates total qualification run time past the monitoring timeout described in finding 32 as routine behavior rather than an edge case, and multiplies the operational cost of finding 31's missing resume support. The operator asked to evaluate outright removing or shrinking this scenario rather than only explaining or bounding its duration.

## Reproduction and evidence

Run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local`. The fixture batch findings 27 and 28 exercised, and that scenario 7 still used, bundled 305 direct inbox sources from the finalized corpus. The deterministic baseline contains seven maintained text/document formats (`md`, `txt`, `csv`, `docx`, `pdf`, `pptx`, `ics`), including 7 `.docx` and 2 `.pptx` sources that also motivate finding 34. `internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json` order 7 (`complete-pending-inbox`) is the only scenario of the 17 that invokes a full inbox-ingestion OpenCode session; all other 16 scenarios are either pure installer/conformance checks or a single small routing prompt.

The available run evidence does not contain per-phase instrumentation, so the timing breakdown is necessarily coarse. Using the observed 2-hour floor, the 305-source run averaged more than 23.6 wall-clock seconds per source end to end. The pre-findings-27/28 under-20-minute behavior was under 3.9 seconds per source. That roughly 6x-or-greater increase is consistent with the new direct source reasoning and rendered reconciliation work, although the wall-clock average also includes provider and fixed session overhead and therefore must not be read as pure per-source reasoning time.

## Decision

**Shrink the maintained live qualification variant to exactly seven direct inbox sources.**

Seven is the strict lower bound because each source has one format and all seven maintained text/document formats must remain represented. The deterministic minimizer selects exactly one source per format and prefers records carrying more section dispositions. In the current oracle this selects a household-finance source for one of the eligible formats, which carries `mapped`, `non-durable`, and `pending` sections together; the final selection is mechanically rejected unless the union still contains all three dispositions.

The complete 305-file finalized corpus remains unchanged as source-fixture and oracle evidence. Only the `complete-pending-inbox` live qualification variant is minimized. The selection is recorded in `variants/04-complete-pending-inbox/selection.json`, including source names, formats, dispositions, and SHA-256 values.

A naive linear projection from the observed current wall-clock average puts seven sources at roughly 3 minutes of source-proportional work, before fixed installation, OpenCode session, reconciliation, conformance, and provider overhead. That is an estimate, not a measured duration; the next real qualification run must establish the actual runtime.

## Options evaluated

### Keep all 305 sources

This provides the strongest batch-volume and broad corpus coverage, including repeated chronology, multiple files per format, and the five finalized PNG sources. It also preserves the exact workload that exposed findings 20, 27, and 28. The cost is now disproportionate: one scenario consumes roughly 2+ hours, magnifying session-lifecycle, resume, monitoring, and provider-quota failures without adding a new format or disposition class for most additional files. Rejected.

### Shrink to the representative minimum

This preserves the maintained scenario's essential contract: a real Inbox Ingester run, every maintained text/document format, all three section dispositions, structural fidelity checks, semantic independent audit, source preservation, and rendered destination reconciliation. Seven sources is minimal rather than arbitrary, so there is no smaller set that preserves the required format contract. The tradeoff is intentional loss of volume, repetition, broad six-month chronology, and PNG ingestion coverage in this specific live scenario. Those remain represented in the immutable 305-file corpus and oracle, but no longer all receive live ingestion during every release qualification. Selected.

### Remove the scenario

This would remove the dominant runtime entirely, but it would also remove the only maintained end-to-end inbox-ingestion scenario. That would give up direct qualification coverage for the feature area that produced findings 04, 14, 16, 20, 27, 28, and 29, leaving correctness primarily to ad hoc dogfooding and lower-level deterministic checks. Rejected.

## Implications for follow-up findings

- Finding 30 remains pending. Detaching long-running qualification from the operator session is still a valid reliability improvement, but the seven-source shrink removes this scenario's multi-hour runtime as its largest amplifier. Its classification and exact scope should be reassessed while resolving that finding rather than changed implicitly here.
- Finding 31 remains pending. Cross-invocation resume still avoids repeating already-passed scenarios after a crash, but the amount of lost work from this scenario should fall substantially.
- Finding 32 remains pending. A pollable status artifact still provides materially better observability than a bounded `kill -0` loop, although the expected normal run duration should be remeasured after this shrink.
- Finding 34 remains necessary and unchanged in principle. The minimum set intentionally retains one `.docx` and one `.pptx`, so Inbox Ingester still needs a sanctioned deterministic Office-document reader before `complete-pending-inbox` can pass.

## Scope

The completed implementation keeps the matrix scenario and its semantic audit requirement, preserves the immutable 305-file corpus, and changes the maintained one-command fixture path so the materialized `complete-pending-inbox` family is deterministically reduced to the exact seven-source minimum before qualification begins. The minimizer updates the variant inventory and writes selection evidence. The individual fixture lifecycle documents the same explicit minimization step.

## Completion criteria

- [x] a per-phase or per-source timing breakdown exists for at least one `complete-pending-inbox` run
- [x] all three options (keep, shrink, remove) are evaluated with concrete tradeoffs, not just asserted
- [x] a decision is recorded among keep/shrink/remove with explicit rationale
- [x] if shrink: the minimum fixture composition preserving disposition-class and format coverage is specified
- [x] if remove: the exact required changes to `procedure.md`, `qualification-automation.md`, and `qualification_runner.py`'s matrix validation are identified, along with the explicit coverage-loss tradeoff
- [x] the decision's implications for findings 30, 31, 32, and 34 are noted so their scope can be adjusted if needed

The remove-only completion item is satisfied by the recorded option analysis: because remove was rejected, no repository change to the 17-scenario matrix contract is required.

## Resolution evidence

Resolved by shrinking, not removing, `complete-pending-inbox`.

- `internal/release/fixtures/synthetic-qualification-vault/minimize_inbox.py` computes the deterministic seven-source lower-bound selection from `oracle/baseline.json`, verifies all seven maintained formats and all three dispositions remain covered, checks source digests, prunes only the materialized variant inbox, records `selection.json`, and refreshes `variants/index.json`.
- `internal/release/generate-synthetic-qualification-vault.sh` applies the minimizer after ordinary variant materialization, so the repository-owned qualification automation receives the reduced variant without changing the immutable corpus.
- `internal/release/tests/test_minimize_qualification_inbox.py` covers the seven-format lower bound, disposition preservation, pruning, selection evidence, and refreshed variant inventory.
- `internal/release/fixtures/synthetic-qualification-vault/blueprint.md` and the fixture index document the maintained seven-source contract and the explicit individual-lifecycle command.
- The next live full qualification run remains responsible for measuring actual post-shrink runtime and proving the scenario with the eventual finding-34 Office reader.
