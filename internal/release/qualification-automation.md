---
type: Internal Release Qualification Procedure
title: Hands-Off Release Qualification and Evidence State
description: Mandatory two-phase pre-merge release qualification, independent audit, explicit user acceptance, and release-quality state.
tags: [internal, release, qualification, automation, evidence, opencode]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T12:45:00+02:00
---

# Purpose

Every Ava release must complete both explicit phases of `qualify-release.sh` before its release-please PR may merge.

The first phase qualifies target behavior that does not depend on an adjacent release edge. It runs immediately after release-please has identified the target version and before semantic-impact review, catalog authoring, guidance, or migrations. The second phase runs only after the adjacent edge exists and exercises the source-to-target upgrade contract.

Each phase inventories its own OpenCode sessions and receives its own independent audit. A clean edge-independent run is reusable evidence, not release acceptance. A clean edge-dependent run stops at `awaiting-user-signoff`, and publication remains blocked until the user explicitly accepts the linked two-phase chain.

# Control state

`internal/release/qualification/` contains:

- `config.json`: the active qualification pair and models
- `pair-catalog.json`: exact source/target selectors used to execute qualification
- `phase-state.json`: latest edge-independent result per release pair
- `phase-runs/`: compact edge-independent run, session, issue, and audit evidence
- `current-state.json`: edge-dependent execution state plus the durable release-acceptance ledger
- `runs/`: compact edge-dependent run, session, issue, and audit evidence
- `schemas/`: state and evidence schemas
- `audit-prompt.md`: the prompt/contract used by each independent audit session

Historical releases through `v1.0.0-alpha.14` are explicitly accepted with `basis: historical-backfill`. This does not claim they were run through the current qualification system. New releases must use `basis: qualified-run`.

# Phase classification

Every maintained scenario in `fixtures/synthetic-qualification-vault/qualification-matrix.json` declares exactly one `qualification_phase`.

Edge-independent scenarios are:

1. fresh empty installation
2. mature project installation and preservation
3. private routing
4. work routing
5. calendar regression
6. ambiguous routing clarification
7. complete pending-inbox ingestion plus independent semantic audit
8. modified managed-content detection
9. missing managed-content detection
10. corrupt upgrade-journal detection
11. unexpected managed-content detection
12. role-led uninstall and pinned reinstall

Edge-dependent scenarios are:

1. interrupted upgrade resume
2. interrupted upgrade abort
3. rollback
4. semantic reconciliation plus finalization
5. pending semantic reconciliation

The independent audit is phase-scoped. It audits every session and terminal claim present in the current phase and does not treat scenarios assigned to the other phase as missing evidence.

# Edge-independent phase

The previous side remains the exact immutable published release. The target side is a provisional local candidate assembled from the clean release PR revision without an adjacent catalog:

```sh
early_assets="$(internal/release/assemble-candidate.sh --phase edge-independent)"
internal/release/qualify-release.sh \
  --phase edge-independent \
  --target-assets "$early_assets"
```

The provisional candidate intentionally contains no source-to-target adjacent edge. `qualification_phase_runner.py` therefore validates only distinct pinned source and target identities before running the edge-independent scenario set.

The edge-independent operation produces one of:

- `failed`: mechanical, evidence, or incomplete-run failure
- `needs-review`: independent audit found a blocker/major issue or cannot support the terminal claim
- `passed`: all early mechanical and semantic claims passed

A `failed` or `needs-review` result stops the release before managed-delta review and edge authoring. Do not create the target catalog, guidance, migrations, or related release-specific state after a non-passing early result.

A clean early result writes compact evidence under `phase-runs/` and records it in `phase-state.json`. Commit that compact evidence to the release PR before beginning edge authoring. The automation itself does not commit it.

# Edge authoring and invalidation

After the edge-independent phase passes, review the managed delta, determine semantic impact, and author only the target release's adjacent catalog, guidance, and migrations as required.

The early result remains reusable only when the repository revision used by the later phase descends from the early qualified revision and every intervening path is one of:

- `internal/release/qualification/phase-state.json`
- compact files for the exact prerequisite run under `internal/release/qualification/phase-runs/`
- `internal/release/catalogs/<target-version>.json`
- `internal/release/guidance/<target-version>/...`
- `internal/release/migrations/...`

Any other intervening change invalidates the early result and requires a new edge-independent run from the changed revision before continuing. This includes template, distribution, installer, fixture, matrix, qualification-tooling, or release-note changes.

The final gate also proves that the target adjacent catalog and target guidance did not already exist at the early qualified revision. This makes the fail-fast ordering mechanically checkable rather than procedural convention.

# Edge-dependent phase

After the adjacent edge is complete, assemble the reviewed candidate and run only the edge-dependent scenarios:

```sh
final_assets="$(internal/release/assemble-candidate.sh --phase edge-dependent)"
internal/release/qualify-release.sh \
  --phase edge-dependent \
  --target-assets "$final_assets"
```

Before executing any scenario, `qualification_phase_automation.py` requires a committed clean early result for the same active pair, validates the allowed intervening change set, validates that both phases use the same immutable source and target version, and requires the final target to declare the authentic reviewed upgrade edge.

The final execution identity records both the prerequisite edge-independent run id and its repository revision. The edge-dependent result remains one of the existing release states:

- `failed`
- `needs-review`
- `awaiting-user-signoff`

Only `awaiting-user-signoff` may proceed to explicit user acceptance.

# OpenCode JSON capture

`qualify-release.sh` uses the maintained `qualification-opencode.sh` adapter. For session inventory, the adapter translates `session list --format json` to the required OpenCode database query. The adapter also handles session `export` capture.

OpenCode environments affected by the 65,536-byte stdout-pipe truncation must not require an external wrapper. For both the session-list database query and `opencode export`, the maintained adapter first lets the real OpenCode process write JSON to a temporary regular file and then re-emits those bytes to qualification automation. Python-side parsing remains the JSON validation boundary.

Session inventory is exact-run isolated. Qualification snapshots OpenCode sessions immediately before and after the runner, and only IDs newly created across that boundary can become current-run evidence. Runner stdout/stderr session IDs are binding hints only. A top-level session must belong to the current execution, nested sessions are admitted only through descendants of already-owned current-run sessions, and every inventoried project root must resolve inside the exact current execution root and bind to a maintained scenario. Historical host sessions may remain indefinitely without cleanup and cannot enter a later run merely because their IDs appear in preserved output.

# Runner and audit boundary

The synthetic runner owns deterministic and structural evidence. A scenario whose complete terminal claim can be proven mechanically returns `pass`. A scenario that deliberately requires evaluator-only semantic judgment may return `structural-pass` with `semantic_status: pending-audit` after every deterministic check succeeds.

`structural-pass` is a mechanically successful runner outcome and does not stop the remaining scenarios in that phase. It is not semantic acceptance. The independent audit remains the authority for meaning preservation, including inbox section dispositions that require the evaluator-only oracle.

# Operator handling of non-passing results

When either phase produces `failed` or `needs-review`, the release operator must present the exact terminal result and individual findings to the user before taking corrective action.

After reporting them, ask whether the user wants those findings recorded as bounded native Backlog.md tasks on `main`. This is opt-in for each failed qualification. Recording tasks is tracking only and does not accept qualification, satisfy the release merge gate, or authorize repository changes.

Any user-directed correction is ordinary repository work. If it changes an input covered by the early phase, the early phase must run again. If it occurs after final qualification, both applicable evidence and final acceptance must be regenerated according to the revision rules.

# User acceptance

After reviewing a clean edge-dependent run, explicit user approval is recorded with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

The acceptance entry point first validates the linked edge-independent prerequisite and its non-invalidation relationship, then applies the existing qualification acceptance update. If `--run-id` is omitted, the latest edge-dependent run for the active pair is used.

Acceptance updates the final run signoff, pair state, and `release_acceptance` entry in `current-state.json` to `accepted` with `basis: qualified-run`. Commit the resulting qualification-state changes to the release PR branch.

# Release PR blocker

The Release PR policy check rejects merge unless the existing qualification acceptance checks pass and the two-phase gate additionally proves:

1. the accepted run is an edge-dependent run
2. it names one clean edge-independent prerequisite run
3. both runs use the same exact source release and target version
4. early target assets were assembled from the early qualified revision
5. final target assets were assembled from the final qualified revision
6. the early revision is an ancestor of the final revision
7. the target adjacent catalog and guidance were absent at the early revision
8. only early compact evidence and edge-specific authoring files changed between the two qualified revisions
9. explicit user signoff applies to the clean final edge-dependent run
10. after final qualification, only files under `internal/release/qualification/` changed

This preserves the original final revision/signoff binding while allowing expensive early checks to be reused only when their validated inputs remained unchanged.

# Evidence boundary

Raw workspaces, release assets, transcripts, and command evidence remain outside the repository. Compact early evidence lives under `phase-runs/`; compact final evidence and release-quality state live under `runs/` and `current-state.json`.

The fixture oracle is evaluator-only. Qualification agents and deterministic runner checks must not rely on it; each independent audit uses it only for applicable phase claims.
