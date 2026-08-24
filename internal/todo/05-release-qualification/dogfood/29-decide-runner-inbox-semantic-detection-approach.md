---
type: Internal Development Task
title: Decide How Qualification Should Detect Inbox Semantic-Disposition Failures
description: The deterministic scenario runner can mark inbox ingestion as passed even when it violates the semantic fidelity contract; decide the approach before implementing a fix.
tags: [internal, roadmap, dogfood, inbox, qualification, runner, decision-needed]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 29
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-24T00:00:00Z
---

# Decide How Qualification Should Detect Inbox Semantic-Disposition Failures

## Observed behavior

Mandatory release qualification for candidate `77977f8` found (`AUD-RUNNER-001`, major, independent audit) that `internal/release/qualification_runner.py:595-605` marks the `complete-pending-inbox` scenario as `pass` after only checking that the OpenCode process exited successfully, no direct pending files remain, and installed conformance passes. None of those checks compare destination meaning or section dispositions against the selected sources or the evaluator-only oracle.

This run, the runner recorded `complete-pending-inbox` as `pass` even though finding 28 (`AUD-INBOX-001`) demonstrates the session promoted `non-durable` passages and reported unreconciled disposition totals. The equivalent gap was previously observed as `AVA-AUD-RUNNER-INBOX-006` in the prior qualification attempt and was deliberately deferred at that time as "situational."  It has now recurred and materially contributed to a `needs-review` result.

## Reproduction and evidence

Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local`, candidate revision `77977f8`. Runner summary records `complete-pending-inbox: pass`; independent audit finding `AUD-RUNNER-001` and companion finding `AUD-INBOX-001` (finding 28) contradict that pass.

## Classification

`blocker` for the next prerelease: it currently contributes to the blocked qualification result for the release PR.

## Root cause

The deterministic runner intentionally does not have access to the evaluator-only oracle (`internal/release/fixtures/synthetic-qualification-vault/oracle/baseline.json`) during a scenario, so it cannot itself judge semantic fidelity without leaking the answer key into the environment the qualification session operates in. Judging semantic fidelity has therefore always been the independent audit's job, not the runner's. But currently the runner's own `pass`/`fail` label is treated as authoritative for that scenario's terminal outcome, so a structurally clean run can report `pass` while the semantic content is wrong, and the *only* thing that later contradicts it is the independent audit, which runs after and outside the runner's own summary.

## Decision needed

This needs an explicit approach decision before implementation, not a unilateral engineering choice:

1. **Audit-gates-runner-summary**: after the audit runs, if it finds a blocking/major finding tied to a specific scenario, retroactively flip that scenario's runner-summary outcome to `fail` (mirrors the now-removed semantic-path-accounting postcondition's shape, but driven by the audit instead of a fixed deterministic list). Keeps the oracle hidden from the qualification session itself.
2. **Rename/soften the runner's claim**: stop calling `complete-pending-inbox` (and similarly evidence-only scenarios) `pass`/`fail` outright; label the runner's own check something like `structural-pass` versus a separate `semantic` status that stays open until the independent audit reports on it, and require both to be clean before `awaiting-user-signoff`.
3. **Give the runner bounded, non-oracle deterministic checks**: add structural fidelity checks the runner *can* perform without the oracle (e.g., every `inbox/processed/` source must still resolve from at least one destination's `sources:` metadata, every used footnote marker must have a definition) to catch a subset of failures earlier, while still relying on the audit for full semantic judgment.
4. **Some combination of the above.**

Each option has different implications for qualification architecture, the meaning of "pass," and how much trust the runner's own summary can carry independent of the audit. This is why the finding records the problem without prescribing the fix.

## Scope

To be defined once the approach is chosen. Likely touches `internal/release/qualification_runner.py`, its test suite, and possibly `internal/release/procedure.md`'s description of what a scenario `pass` means.

## Completion criteria

_To be defined once the approach above is chosen._

## Resolution evidence

_Complete in the resolving implementation PR, once an approach is selected._

## Release qualification follow-up

Any resolving change here is repository-only qualification tooling unless it also changes distributed behavior; classify its commit type accordingly per `internal/release/release-please.md`. A brand-new full qualification run is required regardless once this and findings 27-28 are resolved.
