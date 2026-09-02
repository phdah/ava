---
type: Internal Release Qualification Procedure
title: Hands-Off Release Qualification and Evidence State
description: Mandatory two-phase pre-merge qualification executed in ChatGPT Work Cloud with deterministic validation, fresh subagents, independent audit, and explicit user acceptance.
tags: [internal, release, qualification, automation, evidence, chatgpt, work]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T17:30:00+02:00
---

# Purpose

Every Ava release completes two qualification phases before its release-please PR may merge.

The qualification workload that is not already executed by GitHub Actions runs entirely in **ChatGPT Work Cloud**. The supported flow does not require OpenCode, Work Local, Codex Local, a developer workstation, or another user-hosted process.

Work Cloud supplies the mutable cloud filesystem and shell. Deterministic Ava scripts prepare and validate each scenario. Fresh Work subagents execute only the semantic interactions emitted by the deterministic protocol. A separate fresh Work subagent performs the independent audit.

The execution procedure is defined in [ChatGPT Work Cloud qualification execution](qualification-work.md).

# Two phases

The first phase qualifies target behavior that does not depend on an adjacent release edge. It runs immediately after release-please identifies the target version and before semantic-impact review, catalog authoring, guidance, or migrations.

The second phase runs only after the adjacent edge exists and exercises the source-to-target upgrade contract.

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

# Work execution model

`internal/release/qualify-release.sh` is a deterministic protocol driver. It never starts an LLM process.

The protocol has four operations:

- `init`: bind exact source/target assets, fixture, repository revision, phase prerequisite, and external Work cloud paths
- `advance`: execute deterministic scenario work until either the phase completes or one fresh semantic subagent is required
- `audit-request`: produce the exact read-only independent-audit request after all phase scenarios pass mechanically
- `finalize`: validate audit immutability and evidence, then write compact qualification state into the repository

When `advance` returns `SUBAGENT_REQUIRED`, the parent Work task delegates the generated request to one fresh Work subagent. The subagent works in the isolated project, follows installed Ava routing and roles, writes the declared structured response, and returns control. Calling `advance` again performs deterministic postcondition checks before any later scenario starts.

No shell subprocess is used as an agent runtime. OpenCode session enumeration, exports, permissions, provider databases, and local transcripts are not part of this protocol.

# Work subagent boundary

Each generated interaction request binds:

- one scenario and stage
- exact prompt bytes and SHA-256
- configured qualification model
- exact isolated workspace root
- complete pre-interaction workspace file digests
- expected role when the scenario requires one
- a response path in the shared Work cloud filesystem
- a strict tool boundary

The fresh scenario subagent may use only the cloud filesystem and shell needed for that isolated project. It must not use web search, cloud browser, plugins, apps, MCPs, other repositories, memory, or user-local files.

The response records ordered required-reading evidence bound to the pre-interaction file hashes, the final role/user-facing response, and `external_tools_used: []`. Deterministic validation then checks the scenario's filesystem and managed-state postconditions.

# Deterministic versus semantic work

Deterministic-only scenarios remain code. They run directly through the shared qualification scenario engine inside the Work cloud shell.

Semantic scenarios are split into deterministic preparation, one or more fresh Work subagent interactions, and deterministic verification. This preserves the existing mechanical assertions instead of converting them into LLM judgment.

The complete pending-inbox scenario may finish as `structural-pass` with semantic status pending audit. `structural-pass` is mechanically successful but not semantic acceptance.

# Independent audit

Every phase receives one fresh independent Work subagent after all mechanical scenario outcomes pass.

The audit subagent did not execute any scenario. It receives only the exact current phase evidence and is read-only over repository, fixture, assets, interaction evidence, deterministic logs, and scenario workspaces. The fixture oracle remains evaluator-only.

Before delegating the audit, the deterministic protocol records repository, scenario, fixture, and release-asset digests. `finalize` verifies those digests again and refuses evidence if the audit changed anything outside its declared response file.

The maintained audit contract is [audit-prompt.md](qualification/audit-prompt.md).

# Evidence model

Qualification evidence is independent of ChatGPT thread IDs and product-internal session identifiers.

Compact interaction evidence contains:

- scenario/stage identity
- prompt digest
- model identifier
- workspace identity
- ordered required-reading evidence
- final response
- empty external-tool inventory
- response digest

The run execution identity binds:

- `qualification_host: chatgpt-work-cloud`
- Work protocol version
- exact repository revision
- exact source and target release identities and asset digests
- phase
- qualification matrix digest
- finalized fixture digest
- qualification driver digest
- qualification and audit models
- linked early-phase prerequisite for the final phase

Raw Work cloud workspaces are transient and remain outside Git. The compact summary, interactions, audit, issues, and run record are committed under `internal/release/qualification/`.

# Edge-independent phase

The previous side is the exact immutable published release. The target side is a provisional local candidate assembled from the clean release PR revision without an adjacent catalog.

A clean early result writes compact evidence under `phase-runs/` and records `passed` in `phase-state.json`. Commit those files to the release PR before adjacent edge authoring.

A `failed` or `needs-review` result stops the release before managed-delta review and edge authoring.

# Early-result invalidation

The early result remains reusable only when the final qualified revision descends from the early qualified revision and every intervening path is limited to:

- `internal/release/qualification/phase-state.json`
- compact files for the exact prerequisite run under `internal/release/qualification/phase-runs/`
- `internal/release/catalogs/<target-version>.json`
- `internal/release/guidance/<target-version>/...`
- `internal/release/migrations/...`

Any other intervening change invalidates the early result and requires a new edge-independent Work run.

The phase gate also proves that the target adjacent catalog and target guidance were absent at the early revision.

# Edge-dependent phase

After the adjacent edge is complete, the reviewed candidate is assembled from the new exact release PR revision and the final Work phase is initialized in a new external Work cloud run root.

Before any final scenario runs, `qualification_work.py` applies the existing phase gate to prove:

- one committed clean edge-independent prerequisite exists
- both phases use the same exact source release
- both phases target the same version
- early and final assets are bound to their respective repository revisions
- the final target declares the authentic adjacent upgrade edge
- the early revision is an ancestor of the final revision
- only allowed edge-authoring changes occurred between them

A clean final result stops at `awaiting-user-signoff`.

# User acceptance

Qualification does not accept itself.

After the user reviews the complete two-phase evidence and explicitly approves it, record acceptance with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

The acceptance entry point validates the linked two-phase chain before recording signoff and `release_acceptance` state.

# Release PR blocker

The release PR policy rejects merge unless the accepted final run:

1. is a clean edge-dependent run
2. names one clean edge-independent prerequisite
3. uses the same source and target version as the early run
4. binds both candidate asset sets to their qualified revisions
5. proves early-before-edge ordering
6. proves allowed revision ancestry and intervening changes
7. has a clean independent audit
8. has explicit user signoff
9. has no non-qualification content changes after final qualification

The release gate does not care about OpenCode or ChatGPT session identifiers. It consumes the durable Work evidence and exact repository/release identities.

# No local fallback

The supported qualification flow is Work Cloud only. If the active ChatGPT account or workspace cannot provide cloud shell/filesystem execution, GitHub access, fresh subagent delegation, shared cloud files, or release-PR write access, report that missing capability and stop.

Do not move qualification to OpenCode or a local computer to work around missing Work capabilities.
