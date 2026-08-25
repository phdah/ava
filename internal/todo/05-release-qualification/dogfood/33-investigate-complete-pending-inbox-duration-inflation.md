---
type: Internal Development Task
title: Investigate and Document Complete-Pending-Inbox Duration Inflation
description: Determine whether complete-pending-inbox's multi-hour duration is an inherent cost of findings 27/28's fidelity requirements or contains a fixable inefficiency, and set realistic operator expectations either way.
tags: [internal, roadmap, dogfood, release, qualification, reliability, inbox, performance]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 33
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-25T00:00:00Z
---

# Investigate and Document Complete-Pending-Inbox Duration Inflation

## Observed behavior

`complete-pending-inbox` alone can now take well over an hour (observed roughly 2+ hours on 2026-08-25, run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local`), compared to under 20 minutes before the inbox-fidelity constraints were tightened by findings 27 and 28. This inflates total qualification run time past the monitoring timeout described in finding 32 as routine behavior rather than an edge case, and multiplies the operational cost of finding 31's missing resume support.

## Reproduction and evidence

Run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local`. The same fixture batch findings 27 and 28 exercised bundles 305 direct inbox sources, including 7 `.docx` and 2 `.pptx` sources (`internal/release/fixtures/synthetic-qualification-vault/blueprint.json:24`).

## Classification

`required-v1` for the release candidate: the duration itself does not make a run impossible, unlike findings 30, 31, 32, and 34, but it is the primary driver that turns the multi-hour monitoring and resume gap from a rare edge case into routine, expected behavior. It must be understood and either bounded or explicitly accepted before the release candidate gate.

## Root cause

Findings 27 and 28 intentionally removed the previous fast path (an ad hoc bulk-processing script) and added mandatory per-section rendered-destination reconciliation for the same 305-source batch. That is the correct fix for the scope and fidelity defects those findings addressed, and this finding does not propose weakening it. The resulting cost is that Inbox Ingester must now reason and edit through each of roughly 305 sources directly, one section-ledger and reconciliation pass at a time, inside a single long-lived OpenCode session with no internal checkpointing of its own. No instrumentation currently records where the observed ~2 hours actually goes (per-source timing, reconciliation-pass timing, provider latency versus reasoning time), so it is not yet possible to tell whether the full duration is inherent to correct behavior or partly caused by an incidental inefficiency, such as redundant re-reads or repeated whole-destination re-verification.

## Scope

- add lightweight phase or per-source timing visibility to the `complete-pending-inbox` qualification path (for example requiring the session's completion report to include per-phase elapsed time, or timestamping `runner-commands.jsonl` entries so wall-clock phase duration can be reconstructed after the fact) sufficient to tell whether time is dominated by reasoning and editing volume or by an avoidable repeated pass
- using that evidence, either (a) confirm the duration is an accepted, inherent cost of correct per-section fidelity and document it explicitly in `qualification-automation.md`/`procedure.md` so operators plan for multi-hour single-scenario runs, or (b) identify and fix a concrete, bounded inefficiency if the timing evidence reveals one
- do not reduce the per-section reconciliation or scope-boundary requirements introduced by findings 27 and 28 to chase a shorter duration
- cross-reference findings 30, 31, and 32 as the actual operational mitigation for the resulting duration: detachment, resume, and pollable status are what make a multi-hour scenario tolerable, independent of whether it can be shortened

## Completion criteria

- [ ] timing evidence exists for at least one `complete-pending-inbox` run sufficient to attribute duration to reasoning/editing volume versus an identifiable inefficiency
- [ ] the duration is either explicitly documented as an accepted cost or a concrete bounded inefficiency is fixed, with the outcome recorded in this finding's resolution evidence
- [ ] `qualification-automation.md`/`procedure.md` sets realistic multi-hour duration expectations for this scenario if the cost is accepted
- [ ] repository test suite passes if any code changed

## Resolution evidence

_Complete in the resolving implementation PR._
