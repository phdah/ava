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
  at: 2026-08-17T12:26:00+02:00
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

For the current corrective alpha:

```sh
internal/release/qualify-release.sh \
  --target-assets /absolute/path/to/v1.0.0-alpha.15/assets
```

The run identity binds the release assets, fixture, images, matrix, repository revision, runner, automation, OpenCode version, and qualification/audit models.

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

The fixture oracle is evaluator-only. Qualification agents must not rely on it; the independent audit uses it to judge the resulting behavior.
