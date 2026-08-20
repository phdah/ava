---
type: Internal Development Task
title: Report Inspected Root Index During Pending-Semantic-Reconciliation
description: Make the pending-semantic-reconciliation report confirm inspection of the project root index.
tags: [internal, roadmap, dogfood, release, upgrades, maintenance]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 23
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:openai-opencode
  at: 2026-08-20T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-20T18:28:44+02:00
---

# Report Inspected Root Index During Pending-Semantic-Reconciliation

## Observed behavior

Mandatory release qualification for candidate `8927a3c` ran the `pending-semantic-reconciliation` scenario. It failed: the resulting report did not confirm inspection of `/index.md`.

## Reproduction and evidence

Qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local`, active pair `alpha14-to-alpha15-corrective-local` (published `v1.0.0-alpha.14` to local `v1.0.0-alpha.15`), candidate revision `8927a3c`.

Result: 15 of 17 scenarios passed. `pending-semantic-reconciliation` failed with the missing inspected path listed above.

## Classification

This is a `blocker` for the next prerelease. It blocks acceptance of the failed release qualification run and therefore blocks merge of that release candidate revision.

## Root cause

The durable semantic accounting introduced by finding 21 was correct: Upgrade Role already records every guidance-driven inspected project-owned path, including `/index.md`, in `upgrade.json.project_changes`.

The gap was in the human-readable completion-report contract. It required Upgrade Role to report every inspected or changed path and its journal classification, but did not explicitly require an inspection-only record to be described as an inspection. A report could therefore list `/index.md` or `change_type: inspected` without clearly confirming that the path had actually been inspected during semantic reconciliation.

This is independent of finding 22's ownership boundary. Finding 22 repaired Ava Maintenance reporting during terminal cleanup from durable journal evidence; finding 23 repairs Upgrade Role's own semantic-reconciliation completion report.

## Scope

- identify why the pending-semantic-reconciliation report omits confirmation of `/index.md` inspection
- update the relevant role instructions so the report explicitly confirms inspection of `/index.md`
- add or extend fixture coverage for the reporting requirement
- coordinate with finding 22 if investigation shows a shared root cause, without merging the two findings' completion criteria

## Completion criteria

- [x] the pending-semantic-reconciliation report contract explicitly requires every inspection-only journal path, including `/index.md`, to be named and confirmed as inspected during semantic reconciliation
- [x] regression coverage pins the four expected reported project-owned paths and the explicit inspection wording
- [x] affected documentation and indexes remain aligned

## Resolution evidence

`templates/base/roles/upgrade-role/instructions.md` now requires the completion report to state explicitly, for every `change_type: inspected` journal record, that the exact recorded path was inspected during semantic reconciliation and retained without mutation. Merely listing the path or its journal classification is explicitly insufficient.

`internal/release/fixtures/synthetic-qualification-vault/qualification-matrix.json` now declares `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md` as the expected reported project-owned paths for `pending-semantic-reconciliation`, separate from the existing deterministic journal-accounting expectation.

`internal/release/tests/test_qualification_postconditions.py` verifies both the Upgrade Role reporting contract and the scenario's expected reported path set.

## Release qualification follow-up

The corrective alpha release PR must run a complete fresh 17-scenario qualification against a new candidate revision containing the finding 22 and 23 fixes before it may be accepted. The `pending-semantic-reconciliation` scenario must pass and explicitly confirm inspection of `/index.md` in its resulting report.

Append immutable qualification evidence here after that run. This release gate does not return the implemented finding to `pending`.
