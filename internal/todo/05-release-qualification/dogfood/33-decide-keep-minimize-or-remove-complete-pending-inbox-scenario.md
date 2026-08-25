---
type: Internal Development Task
title: Decide Whether to Keep, Shrink, or Remove the Complete-Pending-Inbox Qualification Scenario
description: Evaluate whether the 305-source complete-pending-inbox scenario should remain as-is, be shrunk to a smaller representative batch, or be removed from the maintained qualification matrix, given its outsized multi-hour cost relative to the rest of the matrix.
tags: [internal, roadmap, dogfood, release, qualification, reliability, inbox, performance]
status: pending
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
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
---

# Decide Whether to Keep, Shrink, or Remove the Complete-Pending-Inbox Qualification Scenario

## Observed behavior

`complete-pending-inbox` alone can now take well over an hour (observed roughly 2+ hours on 2026-08-25, run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local`), compared to under 20 minutes before the inbox-fidelity constraints were tightened by findings 27 and 28. This inflates total qualification run time past the monitoring timeout described in finding 32 as routine behavior rather than an edge case, and multiplies the operational cost of finding 31's missing resume support. The operator has asked to evaluate outright removing or shrinking this scenario rather than only explaining or bounding its duration.

## Reproduction and evidence

Run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local`. The fixture batch findings 27 and 28 exercised, and that scenario 7 still uses, bundles 305 direct inbox sources across 7 formats (`md`, `txt`, `csv`, `docx`, `pdf`, `pptx`, `ics`; `internal/release/fixtures/synthetic-qualification-vault/blueprint.json:24`), including 7 `.docx` and 2 `.pptx` sources that also motivate finding 34. `internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json` order 7 (`complete-pending-inbox`) is the only scenario of the 17 that invokes a full inbox-ingestion OpenCode session; all other 16 scenarios are either pure installer/conformance checks or a single small routing prompt (see the timing breakdown already discussed for this backlog).

## Classification

`blocker` for the next prerelease, and the first item to resolve before any of findings 30, 31, 32, or 34: this scenario's shape is upstream of those findings' urgency and scope. If the decision is to shrink or remove it, finding 34 (Office-document reader tool) may become unnecessary or smaller, and the volume of duration/resume/monitoring pain from findings 30-32 shrinks proportionally. Re-running full qualification, or continuing to invest in findings 30-32/34 exactly as scoped, before this is decided risks solving the wrong-sized problem.

## Root cause

Findings 27 and 28 intentionally removed the previous fast path (an ad hoc bulk-processing script) and added mandatory per-section rendered-destination reconciliation for the same 305-source batch. That is the correct fix for the scope and fidelity defects those findings addressed, and this finding does not propose weakening the fidelity contract itself. What was never revisited is whether the fixture's batch **size** (305 sources) is the right size for a qualification scenario now that each source requires direct, unautomated per-section reasoning. No instrumentation currently records where the observed ~2 hours actually goes (per-source timing, reconciliation-pass timing, provider latency versus reasoning time), and no one has evaluated whether a much smaller batch would still exercise every disposition class (`mapped`/`non-durable`/`pending`) and every source format this scenario is meant to cover.

## Scope

This finding is a decision-and-investigation task, not a predetermined fix. It must produce a recorded decision among exactly three options, with evidence:

1. **Keep as-is.** Accept the ~2 hour cost as the correct price of per-section fidelity over a realistic-sized batch, relying on findings 30-32 to make that duration operationally tolerable. Document the expected duration explicitly in `qualification-automation.md`/`procedure.md`.
2. **Shrink the fixture.** Reduce `variants/04-complete-pending-inbox`'s inbox batch from 305 sources to the smallest set that still exercises every disposition class and every one of the 7 source formats at least once (including at least one `.docx` and one `.pptx` so finding 34 remains exercised). Estimate or measure the resulting duration.
3. **Remove the scenario.** Drop `complete-pending-inbox` from the maintained matrix entirely. This requires updating the "17-scenario matrix" mandate in `procedure.md` and `qualification-automation.md`, updating `qualification_runner.py`'s `load_matrix()` family/scenario validation, and explicitly recording the resulting loss of automated release-qualification coverage for inbox ingestion — the feature area that produced findings 04, 14, 16, 20, 27, 28, and 29. Inbox-ingestion correctness would then rely entirely on ad hoc dogfooding rather than the mandated matrix.

To choose between these, gather at least:

- a rough per-phase or per-source timing breakdown of one `complete-pending-inbox` run (reasoning/editing time versus reconciliation-verification time versus provider latency)
- the minimum source count needed to cover every disposition class and format, if option 2 is considered
- the exact coverage lost (by finding number) if option 3 is chosen

Record the decision, its rationale, and the resulting concrete scope for whichever option is chosen. If the decision is "shrink" or "remove," this finding's resolution evidence hands off the exact fixture/matrix/documentation change as the bounded follow-up work; it does not need to implement that change itself unless the user asks for both in one pass.

## Completion criteria

- [ ] a per-phase or per-source timing breakdown exists for at least one `complete-pending-inbox` run
- [ ] all three options (keep, shrink, remove) are evaluated with concrete tradeoffs, not just asserted
- [ ] a decision is recorded among keep/shrink/remove with explicit rationale
- [ ] if shrink: the minimum fixture composition preserving disposition-class and format coverage is specified
- [ ] if remove: the exact required changes to `procedure.md`, `qualification-automation.md`, and `qualification_runner.py`'s matrix validation are identified, along with the explicit coverage-loss tradeoff
- [ ] the decision's implications for findings 30, 31, 32, and 34 are noted so their scope can be adjusted if needed

## Resolution evidence

_Complete in the resolving implementation PR._
