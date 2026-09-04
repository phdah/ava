---
id: ava-5640
title: Remove obsolete release paths and align maintained release documentation
status: In Progress
assignee: []
created_date: '2026-09-03 08:10'
updated_date: '2026-09-04 15:30'
labels:
  - internal
  - roadmap
  - release
  - cleanup
  - documentation
  - maintenance
milestone: m-0
dependencies:
  - ava-5639
references:
  - ava-5639
type: enhancement
ordinal: 6639
---

## Description

Reduce Ava's maintained release surface to the single release process that is actually supported today. Remove deprecated release scripts, modules, workflows, helpers, configuration, fixtures, compatibility branches, and documentation that are no longer used by the current release flow rather than retaining them "just in case".

The same rule applies to wording. Live instructions, README content, comments, examples, and release documentation must describe the current process directly and consistently. They should not explain the current process through references to superseded OpenCode, ChatGPT Work, multi-host, older qualification, or other historical implementations unless that history is genuinely required to operate the current system.

Historical logs, changelog/history records, completed task resolution evidence, committed release evidence, and similar immutable records are allowed to describe what happened previously. They must remain clearly historical and must not function as alternative instructions or dormant executable paths.

This cleanup should follow AVA-5639 so the resilient publication/recovery design is first established as part of the definitive current release process.

## Required behavior

1. Starting from the authoritative release procedure and active GitHub Actions workflows, inventory the complete maintained release execution surface and identify every file, script, Python module, workflow, helper, configuration entry, fixture, test, and instruction that participates in the current process.
2. Classify remaining release-related artifacts as current runtime/support surface, required immutable historical evidence, or obsolete material. Do not keep a fourth category of dormant or potentially-useful legacy implementation.
3. Delete obsolete executable and declarative release artifacts completely when they are not required by the current process. This includes superseded host-specific runners, old orchestration approaches, compatibility/fallback paths, duplicate entry points, and abandoned helpers where they are no longer live.
4. Remove dead branches and compatibility logic inside retained scripts/modules when those branches only support deprecated release processes.
5. Rewrite retained release instructions, comments, docstrings, examples, names, and terminology so they describe only the current supported state and current operator flow. Avoid wording such as "previously", "old path", "legacy alternative", or historical comparisons in maintained operational instructions when the historical context is not needed to execute the process.
6. Keep historical logs/evidence intact where they are records of past releases or decisions, but clearly separate them from live operational documentation and never treat them as executable guidance.
7. Remove stale references to deleted files, commands, phases, hosts, scripts, environment variables, or workflows across the repository.
8. Consolidate duplicated release logic where multiple retained entry points perform the same current responsibility without a justified separation.
9. Add or strengthen regression checks so deleted/deprecated release entry points and stale documentation references cannot silently reappear.
10. Validate the cleaned repository against the complete current release test suite and ensure AVA-5639's publication/recovery path remains fully supported.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 The implementation records an inventory of the maintained release surface and classifies every release-related executable/documentation artifact as current, required historical evidence, or obsolete
- [x] #2 Every artifact classified as obsolete is removed rather than retained as a dormant fallback or possible future option
- [x] #3 Retained scripts, Python modules, workflows, helpers, fixtures, and configuration contain no branches whose only purpose is supporting a superseded release process
- [x] #4 The authoritative release procedure and all maintained release instructions/examples use current terminology and describe one current supported flow without references to obsolete host-specific or superseded qualification/publication mechanisms
- [x] #5 Repository-wide references to removed release files, commands, environment variables, workflows, and terminology are eliminated or intentionally confined to immutable historical logs/evidence
- [x] #6 Historical logs, changelog/history, completed task resolution evidence, and required release evidence remain preserved but are clearly non-operational records
- [x] #7 Duplicate current release entry points or helpers are consolidated unless their separation has an explicit maintained purpose
- [x] #8 Regression coverage detects dangling release references and prevents known deprecated entry points or compatibility paths from being reintroduced accidentally
- [ ] #9 The complete current release test suite passes after cleanup, including AVA-5639's resilient publication and manual recovery behavior
- [x] #10 A maintainer reading only the live release procedure and retained operational files can understand and execute the current release process without needing historical context
<!-- AC:END -->

## Implementation inventory

### Current runtime and support surface

- `.github/workflows/release-qualification.yml` and `qualification_ci.py` own mandatory release-PR qualification execution and evidence handoff.
- `run-release-qualification.sh` owns immutable source acquisition and repository-external fixture/test-boundary setup.
- `qualify-release.sh` and `qualification.py` are the stable shell and Python qualification entry points.
- `qualification_engine.py` owns deterministic pre-edge/final execution; `qualification_runner.py` owns reusable scenario mechanics and targeted behavioral QA; `qualification_state.py` owns current config/schema/digest/repository-state helpers.
- `qualification_acceptance.py` and `accept-release-qualification.sh` own explicit acceptance.
- `assemble*.{sh,py}`, adjacent catalog modules, immutable `catalogs/`, and reviewed `guidance/` own candidate assembly and supported upgrade composition.
- `.github/workflows/release-please.yml`, `publication.py`, and `publication-recovery.md` own durable publication and AVA-5639 recovery.
- `conformance*.py`, `validate-boundaries.sh`, `test.sh`, and maintained release tests own validation.
- `procedure.md`, `release-please.md`, `qualification-automation.md`, `qualification-execution.md`, `conformance.md`, and release indexes are live operator documentation.

### Required historical evidence

- `internal/release/log.md`, `CHANGELOG.md`, completed/archive roadmap task evidence, committed records under `internal/release/qualification/runs/`, immutable published release metadata, catalogs, and reviewed guidance remain preserved as records or compatibility evidence. Historical terminology in those records is non-operational.

### Removed obsolete surface

- The Work-named qualification implementation, old two-phase runner/automation/gate stack, phase state, independent audit prompt and schemas, old run/session schemas, and their tests.
- The old model/session-oriented `qualification_automation.py` helper plus model configuration and execution-identity/session-inventory tests; current state helpers are now bounded in `qualification_state.py`.
- The superseded alpha qualification policy/fixture/test stack.
- The compatibility-only `validate_upgrade_impact.py` validator and its test. The current adjacent-catalog and release-PR policy remain unchanged.

## Validation

`test_release_surface.py` and `validate-boundaries.sh` fail if the known obsolete paths return. The maintained release suite now compiles and executes only current release modules while retaining publication/recovery regression coverage. Final task completion is gated on the PR CI result.
