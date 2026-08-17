---
type: Internal Development Task
title: Record Semantic Inspection Paths Before Completion
description: Require Upgrade Role to record every guidance-driven project-owned inspection as durable journal evidence before semantic compatibility can become complete.
tags: [internal, roadmap, dogfood, upgrades, semantic, journal, qualification]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 21
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

# Record Semantic Inspection Paths Before Completion

## Observed behavior

The full `alpha.13 -> alpha.14` synthetic qualification reached an all-pass runner summary, but the independent audit found that the `interrupted-finalize` semantic migration inspected four project-owned paths and then marked semantic compatibility complete with `upgrade.json.project_changes: []`.

The audit recorded this as `QUA-SEMANTIC-PATHS-003` with major severity. The companion `pending-semantic-reconciliation` scenario recorded the same four inspected paths, demonstrating that the missing accounting was not inherent to the fixture.

## Classification

This is `required-v1` and blocks release-candidate acceptance. Semantic compatibility must be auditable before normal routing is restored. A migration cannot claim completion while guidance-driven inspection evidence is missing from the durable journal.

## Root cause

The Upgrade Role contract required every *changed* path to be recorded but did not provide a valid journal representation for a path that was inspected as a semantic input and retained unchanged.

The upgrade schema allowed only `created`, `modified`, `deleted`, and `moved` change types. Recording an unchanged inspection would therefore either be omitted or falsely classified as a mutation.

The synthetic runner also checked final semantic state but did not independently assert the known project-path accounting required by the semantic qualification scenarios.

## Scope

The resolving change must:

- add an explicit inspection-only project-change representation without weakening existing mutation records
- require Upgrade Role to record every guidance-driven project-owned path it actually inspects before semantic completion
- use one record per path and replace an inspection-only classification with the actual change type if that path is later mutated
- prevent semantic completion while an inspected or changed path is missing or unresolved
- keep inspection-only records from creating rollback work by themselves
- make the synthetic semantic scenarios declare their expected inspected-path accounting
- add a deterministic postcondition that converts an otherwise passing scenario to failure when required accounting is missing, duplicated, or unresolved
- preserve the independent audit as the semantic reviewer rather than moving semantic judgment into deterministic code

## Completion criteria

- [x] `upgrade.schema.json` accepts `change_type: inspected` for project-owned paths retained without mutation.
- [x] Upgrade Role records every guidance-driven inspected or changed project-owned path exactly once before semantic completion.
- [x] Inspection-only records use `resolution: retained` and are replaced with the actual change type when the same path is later mutated.
- [x] Rollback preparation distinguishes actual project edits from inspection-only evidence.
- [x] The interrupted-finalize and pending-semantic-reconciliation qualification scenarios declare the four expected project paths.
- [x] The qualification shell gate runs deterministic semantic project-change postconditions after a successful scenario runner.
- [x] Missing, duplicate, or unresolved expected paths change the final qualification summary to failure and return nonzero.
- [x] Repository tests cover the schema representation, role contract, expected scenario paths, and postcondition behavior.

## Resolution evidence

`distribution/schemas/upgrade.schema.json` now admits `inspected` as an explicit project change type for guidance-driven reads that require no content mutation.

`templates/base/roles/upgrade-role/instructions.md` requires inspection accounting during impact analysis, defines `inspected/retained`, requires exactly one record for every inspected or changed path before semantic completion, and excludes inspection-only records from rollback edit work.

The synthetic qualification matrix names `/index.md`, `/roles/index.md`, `/shared/index.md`, and `/workflows/index.md` as required project-change evidence for both semantic scenarios. `internal/release/qualification_postconditions.py` checks those records after a successful runner execution and rewrites the summary to fail when accounting is missing, duplicated, or unresolved.

`internal/release/qualify-synthetic.sh` now runs the semantic postcondition gate after the scenario runner, and `internal/release/tests/test_qualification_postconditions.py` covers the accepted and rejected states.

## Release qualification follow-up

Rerun the semantic reconciliation and finalization scenarios through the corrective release. Both must retain complete project-path accounting, and the independent audit must report no blocking or major semantic-accounting finding.
