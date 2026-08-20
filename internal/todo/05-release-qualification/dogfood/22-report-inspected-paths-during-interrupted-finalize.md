---
type: Internal Development Task
title: Report Inspected Project-Owned Paths During Interrupted-Finalize
description: Make Ava Maintenance's interrupted-terminal-cleanup replay report confirm inspection of every required project-owned path.
tags: [internal, roadmap, dogfood, release, upgrades, maintenance]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 22
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:openai-opencode
  at: 2026-08-20T00:00:00Z
---

# Report Inspected Project-Owned Paths During Interrupted-Finalize

## Observed behavior

Mandatory release qualification for candidate `8927a3c` (recoverable terminal cleanup) ran the `interrupted-finalize` scenario, which exercises the new interrupted-terminal-cleanup replay procedure. The scenario failed: the resulting report did not confirm inspection of `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md`.

## Reproduction and evidence

Qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local`, active pair `alpha14-to-alpha15-corrective-local` (published `v1.0.0-alpha.14` to local `v1.0.0-alpha.15`), candidate revision `8927a3c`.

Result: 15 of 17 scenarios passed. `interrupted-finalize` failed with the missing inspected paths listed above.

## Classification

This is a `blocker` for the next prerelease. It blocks acceptance of the current release qualification run and therefore blocks merge of the release PR.

## Root cause

Unknown. The interrupted-terminal-cleanup replay instructions added in `8927a3c` describe the cleanup-replay procedure itself but do not clearly require the report to enumerate inspection of the standard project-owned paths (`/index.md`, `/roles/index.md`, `/shared/index.md`, `/workflows/index.md`) the way other Ava Maintenance report paths already do. Investigate whether this is a reporting-instruction gap or a deeper behavioral gap in the replay path.

## Scope

- identify why the interrupted-terminal-cleanup replay path omits these inspected paths from its report
- update `templates/base/roles/ava-maintenance/instructions.md` (and any related capabilities/constraints/routing text) so the replay procedure's report explicitly confirms inspection of these paths
- add or extend fixture coverage in `internal/release/fixtures/ava-maintenance.json` and `internal/release/tests/test_ava_maintenance.py` for the reporting requirement
- keep the bounded, evidence-gated nature of the replay authority introduced in `8927a3c` unchanged

## Completion criteria

- the interrupted-terminal-cleanup replay report explicitly confirms inspection of `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md`
- regression coverage coversthis reporting requirement
- a fresh full qualification run against a new candidate passes the `interrupted-finalize` scenario
- affected documentation and indexes remain aligned

## Resolution evidence

_Complete in the resolving implementation PR._

## Release qualification follow-up

The corrective alpha release PR must run a complete fresh 17-scenario qualification against the new candidate revision produced by this fix before it may be accepted. Append that evidence here after the run.
