---
type: Internal Release Qualification Procedure
title: Hands-Off Release Qualification and Evidence State
description: Mandatory pre-merge release qualification, independent audit, explicit user acceptance, and release-quality state.
tags: [internal, release, qualification, automation, evidence, opencode]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-24T17:23:00+02:00
---

# Purpose

Every Ava release must pass `qualify-release.sh` before its release-please PR may merge.

The operation qualifies the exact previous published release against one exact locally assembled target from the release PR branch. It runs the maintained matrix, inventories every top-level and nested OpenCode session, performs an independent audit, and writes compact evidence.

A clean automated run stops at `awaiting-user-signoff`. Publication remains blocked until the user explicitly accepts that run.

# Control state

`internal/release/qualification/` contains:

- `config.json`: the active qualification pair and models
- `pair-catalog.json`: exact source/target selectors used to execute qualification
- `current-state.json`: pair execution state plus the durable release-acceptance ledger
- `runs/`: compact run, session, issue, and audit evidence
- `schemas/`: state and evidence schemas
- `audit-prompt.md`: the prompt/contract used by the independent audit session

Historical releases through `v1.0.0-alpha.14` are explicitly accepted with `basis: historical-backfill`. This does not claim they were run through the current qualification system. New releases must use `basis: qualified-run`.

# Pre-merge candidate

Release qualification runs after the release PR has its target version, adjacent edge, semantic-impact decision, and candidate assets prepared, but before merge.

The previous side is the exact immutable published release. The target side is local and must be assembled from the clean release PR revision being qualified.

From that clean release PR checkout, run:

```sh
internal/release/assemble-candidate.sh
```

The candidate assembler derives the target version and channel from `version.txt`, binds the current `HEAD`, derives deterministic publication metadata, selects `internal/release/catalogs/<version>.json`, and creates a repository-external candidate directory. It refuses dirty source state, missing catalog state, repository-local output, and reuse of an existing candidate directory. Set `AVA_CANDIDATE_ROOT` only when a specific external output parent is desired.

Because assembly diagnostics go to stderr and only the absolute asset path is written to stdout, assembly and qualification can be composed directly:

```sh
internal/release/qualify-release.sh \
  --target-assets "$(internal/release/assemble-candidate.sh)"
```

The run identity binds the release assets, fixture, images, matrix, repository revision, runner, automation, OpenCode version, and qualification/audit models.

# OpenCode JSON capture

`qualify-release.sh` uses the maintained `qualification-opencode.sh` adapter. For session inventory, the adapter translates `session list --format json` to the required OpenCode database query. The adapter also handles session `export` capture.

OpenCode environments affected by the 65,536-byte stdout-pipe truncation must not require an external wrapper. For both the session-list database query and `opencode export`, the maintained adapter first lets the real OpenCode process write JSON to a temporary regular file and then re-emits those bytes to qualification automation. Python-side parsing remains the JSON validation boundary.

`AVA_QUALIFICATION_OPENCODE` may still select the real OpenCode executable when needed, but normal qualification does not require a large-JSON shim.

# Runner and audit boundary

The synthetic runner owns deterministic and structural evidence. A scenario whose complete terminal claim can be proven mechanically returns `pass`. A scenario that deliberately requires evaluator-only semantic judgment may return `structural-pass` with `semantic_status: pending-audit` after every deterministic check succeeds.

`structural-pass` is a mechanically successful runner outcome, so it does not stop the remaining matrix and does not prevent the independent audit from running. It is not interpreted as semantic acceptance. The independent audit remains the authority for meaning preservation, including inbox section dispositions that require the evaluator-only oracle.

The hands-off operation reaches `awaiting-user-signoff` only after all runner outcomes are mechanically successful and the independent audit concludes cleanly. A semantic defect discovered by the audit therefore produces `needs-review` without rewriting the runner's original structural evidence.

# Automated result

The operation produces one of:

- `failed`: mechanical, evidence, or incomplete-run failure
- `needs-review`: independent audit found a blocker/major issue or cannot support the terminal claim
- `awaiting-user-signoff`: complete mechanical and semantic pass

The automation never accepts a release itself and never commits evidence.

# User acceptance

After reviewing a clean run, explicit user approval is recorded with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

If `--run-id` is omitted, the latest run for the active pair is used.

Acceptance updates the run signoff, pair state, and `release_acceptance` entry in `current-state.json` to `accepted` with `basis: qualified-run`. The resulting qualification-state changes are then committed to the release PR branch.

# Release PR blocker

The Release PR policy check rejects merge unless:

1. every historical release through the previous version has accepted release-quality state
2. the target release has `basis: qualified-run` and status `accepted`
3. its run ended cleanly at `awaiting-user-signoff`
4. the run source and target match the release PR edge
5. the local target assets identify the exact repository revision that was qualified
6. explicit user signoff matches the acceptance ledger
7. the qualified revision belongs to the release PR
8. after that revision, only files under `internal/release/qualification/` changed

Any release-content change after qualification invalidates acceptance and requires a new run.

# Evidence boundary

Raw workspaces, release assets, transcripts, and command evidence remain outside the repository. Compact evidence and release-quality state remain under `internal/release/qualification/`.

The fixture oracle is evaluator-only. Qualification agents and deterministic runner checks must not rely on it; the independent audit uses it to judge the resulting behavior.
