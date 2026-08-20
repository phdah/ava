---
type: Internal Development Task
title: Report Inspected Project-Owned Paths During Interrupted-Finalize
description: Make Ava Maintenance's interrupted-terminal-cleanup replay report confirm inspection of every required project-owned path.
tags: [internal, roadmap, dogfood, release, upgrades, maintenance]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 22
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:openai-opencode
  at: 2026-08-20T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-20T18:11:00+02:00
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

The interrupted-terminal-cleanup replay procedure preserved the bounded cleanup authority correctly, but its reporting contract only required generic removed, preserved, or conflicted paths. It did not require Ava Maintenance to carry the durable semantic inspection evidence already present in terminal `upgrade.json.project_changes` into the cleanup completion report.

The correct fix is reporting-only. Ava Maintenance must not reread project-owned semantic inputs during terminal cleanup because semantic inspection authority belongs to Upgrade Role. It should instead report the exact project-owned paths and outcomes already recorded in the validated terminal journal.

## Scope

- identify why the interrupted-terminal-cleanup replay path omits these inspected paths from its report
- update `templates/base/roles/ava-maintenance/instructions.md` (and any related capabilities/constraints/routing text) so the replay procedure's report explicitly confirms inspection of these paths
- add or extend fixture coverage in `internal/release/fixtures/ava-maintenance.json` and `internal/release/tests/test_ava_maintenance.py` for the reporting requirement
- keep the bounded, evidence-gated nature of the replay authority introduced in `8927a3c` unchanged

## Completion criteria

- [x] the interrupted-terminal-cleanup replay report explicitly confirms inspection of `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md` when those paths are present in durable journal evidence
- [x] regression coverage covers this reporting requirement
- [x] the reporting fix does not broaden Ava Maintenance authority to reread or modify project-owned semantic inputs
- [x] affected documentation and indexes remain aligned

## Resolution evidence

`templates/base/roles/ava-maintenance/instructions.md` now requires interrupted terminal cleanup to carry every project-owned path recorded in validated terminal `project_changes` evidence into the completion report, including inspection-only retained records for `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md`. It explicitly prohibits rereading those project-owned semantic inputs under maintenance authority.

`internal/release/fixtures/ava-maintenance.json` models the four inspection-only retained journal records for `terminal-cleanup-replay`, requires those exact paths in the report, identifies `journal.project_changes` as the evidence source, and asserts that project-owned files are not reread.

`internal/release/tests/test_ava_maintenance.py` verifies the recorded-path set, inspection-only classification, durable evidence source, no-reread boundary, and the corresponding maintenance instruction contract.

## Release qualification follow-up

The corrective alpha release PR must run a complete fresh 17-scenario qualification against the new candidate revision produced by this fix before it may be accepted. The `interrupted-finalize` scenario must pass and confirm all four project-owned paths in the resulting report. Append that immutable qualification evidence here after the run; this release gate does not return the implemented finding to pending.