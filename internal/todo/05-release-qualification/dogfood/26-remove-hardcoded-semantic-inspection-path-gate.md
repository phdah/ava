---
type: Internal Development Task
title: Remove Hardcoded Semantic-Inspection-Path Qualification Gate
description: Remove the deterministic qualification postcondition that required a fixed, hardcoded set of project-owned paths to be recorded as inspected, because the set does not generalize across release edges.
tags: [internal, roadmap, dogfood, release, upgrades, qualification]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 26
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-24T11:05:00Z
---

# Remove Hardcoded Semantic-Inspection-Path Qualification Gate

## Observed behavior

Qualification run `20260821T100350003229Z-alpha14-to-alpha15-corrective-local` failed the `interrupted-finalize` and `pending-semantic-reconciliation` scenarios. Each failure reported one "missing inspected path" (`/shared/index.md` and `/index.md` respectively) relative to a fixed four-path list (`/index.md`, `/roles/index.md`, `/shared/index.md`, `/workflows/index.md`) declared in `qualification-matrix.json`.

Both underlying agent sessions had already inspected and recorded every project-owned path actually relevant to this release edge, including `/inbox/index.md`, `/inbox/processed/index.md`, and `/knowledge/index.md`, none of which the fixed list required. The only "missing" paths were generic, content-free project scaffold files unrelated to this edge's guidance.

## Reproduction and evidence

Qualification run `20260821T100350003229Z-alpha14-to-alpha15-corrective-local`, `internal/release/qualification/runs/20260821T100350003229Z-alpha14-to-alpha15-corrective-local.json` and companion `.issues.json`. Both failing scenarios' recorded `upgrade.json.project_changes` are preserved under `/tmp/ava-qualification-20260821T100350003229Z-alpha14-to-alpha15-corrective-local/execution/.../scenarios/`.

## Classification

`blocker` for the next prerelease: the current qualification gate produces false failures against a correctly behaving candidate, which blocks every future release edge whose guidance-relevant paths differ from the alpha.13-to-alpha.14 edge that originated the hardcoded list.

## Root cause

Finding 21 introduced a deterministic postcondition (`qualification_postconditions.py`) that compares each semantic scenario's recorded `project_changes` against a fixed path list declared once in `qualification-matrix.json`. That list was copied directly from what one specific agent session inspected during the alpha.13-to-alpha.14 qualification. It was never re-derived per release edge.

The Upgrade Role contract (`templates/base/roles/upgrade-role/instructions.md`) and this release's own guidance (`internal/release/guidance/1.0.0-alpha.15/1.0.0-alpha.14-to-1.0.0-alpha.15/UPGRADE.md`) both require bounded, guidance-driven inspection and explicitly prohibit a blanket project scan. A fixed, edge-agnostic path list is structurally incompatible with that bounded-discovery contract: it cannot represent "the guidance-relevant paths for this edge," so it will keep producing false failures or false passes for any edge whose affected concepts differ from the one it was copied from.

Whether the actually-inspected path set is *adequate* for a given edge's guidance is a semantic judgment, not a fixed structural fact. The independent audit already performs this judgment independently (it raised the equivalent finding `AVA-AUD-SEMANTIC-ACCOUNTING-004` in this same run by reading the guidance and the transcripts) and remains the correct owner of it, consistent with the release procedure's separation between deterministic tooling and semantic review.

## Scope

- remove `internal/release/qualification_postconditions.py` and its test suite
- remove the postcondition invocation from `internal/release/qualify-synthetic.sh`, `internal/release/test.sh`, and `internal/release/index.md`
- remove the hardcoded `expected_project_changes` and `expected_reported_project_owned_paths` fields from the `interrupted-finalize` and `pending-semantic-reconciliation` scenarios in `qualification-matrix.json`
- preserve the unrelated schema and Upgrade Role instruction coverage (the `inspected`/`retained` journal representation and completion-report wording) that finding 21 and finding 23 also introduced; only the fixed-list deterministic gate is removed
- record this reversal in `internal/release/log.md`

## Completion criteria

- [x] no repository script or test references a hardcoded per-scenario expected-inspected-path list
- [x] `qualify-synthetic.sh` runs the scenario runner directly and exits with its status
- [x] the schema and Upgrade Role reporting-contract regression coverage from findings 21 and 23 is preserved under `internal/release/tests/test_semantic_upgrade.py`
- [x] `internal/release/log.md` records the reversal and its rationale
- [x] this repository's own test suite (`internal/release/test.sh`) passes after the change

## Resolution evidence

`internal/release/qualification_postconditions.py` and `internal/release/tests/test_qualification_postconditions.py` are removed. `qualify-synthetic.sh` now execs the scenario runner directly. `test.sh` no longer compiles or runs the removed module or test. `qualification-matrix.json` no longer declares expected inspected-path lists for `interrupted-finalize` or `pending-semantic-reconciliation`. The schema/instruction invariant from the removed test is preserved as `InspectionOnlyProjectChangeContractTests` in `test_semantic_upgrade.py`. `internal/release/log.md` records this reversal under today's date.

Semantic adequacy of guidance-driven path inspection for a given release edge remains an independent-audit concern, not a deterministic qualification-matrix gate.

## Release qualification follow-up

The corrective alpha.15 release PR needs a brand-new full qualification run against a freshly assembled candidate once all outstanding findings from run `20260821T100350003229Z-alpha14-to-alpha15-corrective-local` are resolved or explicitly deferred. `interrupted-finalize` and `pending-semantic-reconciliation` are expected to pass without this removed gate; the independent audit remains responsible for judging semantic-inspection adequacy.
