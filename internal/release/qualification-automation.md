---
type: Internal Release Qualification Procedure
title: Hands-Off Release Qualification and Evidence State
description: One non-interactive maintainer operation for exact release acquisition, clean synthetic qualification, complete OpenCode session audit, and compact reviewable evidence state.
tags: [internal, release, qualification, automation, evidence, opencode]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
---

# Purpose

`qualify-release.sh` is the maintainer entry point for a complete release qualification run. It resolves the one reviewed active release pair, creates a fresh isolated synthetic vault and test boundary, runs the maintained qualification matrix, inventories every OpenCode session created by that run including nested sessions, performs an independent read-only audit in a fresh session, and writes compact evidence for review.

This is repository-only release tooling. It does not create a distributed Ava command, commit generated evidence, authorize publication, or change dogfood findings automatically.

# Checked-in control state

`internal/release/qualification/` contains:

- one explicit active pair in `config.json`
- fixed `qualification_model` and `audit_model` fields
- exact reviewed release selectors and the historical pair ledger in `pair-catalog.json`
- current automated and later user-owned signoff state in `current-state.json`
- schemas, the independent audit contract, and compact run evidence

The historical `1.0.0-alpha.13 -> 1.0.0-alpha.14` pair is retained separately. Its evidence can never qualify the active corrective pair.

# Current command

The active pair uses immutable published `v1.0.0-alpha.14` as the source and an exact caller-supplied local `v1.0.0-alpha.15` asset directory as the corrective target:

```sh
internal/release/qualify-release.sh \
  --target-assets /absolute/path/to/v1.0.0-alpha.15/assets
```

Use `--run-root-parent /absolute/external/path` to choose the parent for raw execution evidence. Otherwise the system temporary directory is used. The run root must remain outside the Ava repository.

`--source-assets` is accepted only when the checked-in source selector is `local`. Supplying it for the current published source is an error.

Validate only the checked-in control state, schemas, and pinned image bytes with:

```sh
internal/release/qualify-release.sh --validate-config-only
```

# Exact release acquisition

A published selector:

1. rejects mutable `latest` selection
2. requires the exact tag to be published, non-draft, and immutable
3. downloads exactly the seven Ava release assets with `gh`
4. verifies the release attestation and each downloaded asset with `gh release verify` and `gh release verify-asset`
5. verifies the seven-file `SHA256SUMS` inventory and release manifest identity
6. requires the downloaded manifest and asset digests to equal the checked-in catalog

A local selector requires an exact normal directory supplied by the caller. It receives the same normal-file, seven-asset, checksum, manifest, version, tag, revision, and upgrade-edge validation, but records `attested: false` and never claims publication evidence.

# Isolated execution identity

Each run receives a new external root with separate release assets, fixture, execution, transcript, audit, and test-project scopes.

The operation invokes `generate-synthetic-qualification-vault.sh` as the single fixture lifecycle entry point. Before that, it validates all five committed PNGs against the pinned image manifest, including bytes, SHA-256, PNG dimensions, media type, and corpus destination.

The execution identity binds:

- complete source and target release identities and asset digests
- pinned-image manifest and per-image digests
- fixture generator digest and generated fixture inventory digest
- qualification matrix digest
- Ava repository revision
- runner and automation digests
- OpenCode version
- qualification and audit model identifiers

Runner state is namespaced by that execution-identity digest. A changed release asset, fixture, image set, matrix, repository revision, runner, automation, OpenCode version, or model therefore cannot reuse a retained passing scenario from an earlier identity.

# Qualification and audit

The operation runs the existing synthetic runner preflight, then the complete maintained matrix. It snapshots OpenCode sessions before and after execution, reconciles direct session IDs from runner command evidence, follows parent relationships to nested sessions, exports every relevant session, and records scenario, prompt digest, model, project root, transcript digest, parent, and terminal state.

When session evidence exists, a fresh OpenCode session runs the maintained independent audit. The audit is read-only and checks routing, required-reading order, authority, mutation boundaries, source fidelity, calendar behavior, inbox reconciliation, semantic reconciliation, finalization, lifecycle preservation, errors and retries, nested sessions, superseded attempts, and whether runner assertions support the terminal claims.

A `blocker` or `major` audit finding produces nonzero status and `needs-review`. Any mechanical failure, incomplete runner outcome, invalid session inventory, or invalid audit also produces nonzero status. A mechanically successful all-pass run with a valid audit records `awaiting-user-signoff`, never automatic acceptance.

# Evidence and review

Raw release assets, generated corpus copies, isolated workspaces, command output, and full transcripts remain in the external run root. Compact records are written under `internal/release/qualification/runs/` and `current-state.json` is updated only after execution and audit are complete.

The operation never runs `git commit`. Review the uncommitted evidence, investigate any `failed` or `needs-review` result, and obtain explicit user signoff before a successful pair may become `accepted` or advance a release gate.
