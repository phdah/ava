---
type: Internal Release Qualification Procedure
title: Deterministic Release Qualification and Evidence State
description: Minimal session-neutral release qualification using deterministic pre-edge and final checks plus explicit user acceptance.
tags: [internal, release, qualification, automation, evidence, deterministic, session-neutral]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T20:45:00+02:00
---

# Purpose

Ava's normal release qualification is deterministic and intentionally cheap in agent usage.

The release procedure is session-neutral. The active maintainer session does not need to supply a shell or a particular ChatGPT execution mode. GitHub Actions is the canonical executor for mandatory qualification on the release PR.

`internal/release/qualify-release.sh` contains no agent runtime dependency. The end-to-end deterministic execution contract is defined in [Session-neutral deterministic qualification](qualification-execution.md).

# Release stages

There are two execution stages with different purposes:

1. **pre-edge**: an ephemeral fail-fast preflight before semantic-impact review and adjacent-edge authoring
2. **final**: the single authoritative release qualification after the reviewed edge exists

The pre-edge result is not committed as qualification evidence. The final result is the only run used for user acceptance and release-PR gating.

# Pre-edge checks

The pre-edge stage runs:

1. fresh empty installation
2. mature-project installation and preservation of existing project-owned bytes
3. modified managed-content rejection
4. missing managed-content rejection
5. corrupt managed-state rejection
6. unexpected managed-content rejection
7. synthetic corpus and external test-boundary integrity

This stage exists to fail fast before spending maintainer effort on release semantics.

# Maintainer semantic-impact assessment

After pre-edge passes, the maintainer reviews the exact previous-to-target release delta.

The assessment must explicitly cover:

1. **Managed delta:** which managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed
2. **Project-owned compatibility:** whether valid active project-owned context could remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible
3. **Required reconciliation:** which bounded project-owned concepts require review when compatibility may be affected

The decision and its rationale are reviewed release evidence. A managed behavior change alone does not decide semantic impact. The presence or absence of a deterministic project-file migration does not decide it either.

# Final checks

The final stage reruns all pre-edge checks and additionally validates:

1. exactly one authentic previous-to-target edge in the target release assets
2. a complete deterministic source-to-target upgrade preserving project-owned bytes
3. interrupted upgrade resume
4. interrupted upgrade abort
5. rollback to the previous release
6. the mechanically correct semantic state after upgrade, whether complete or authentically pending project-owned reconciliation

A clean final result writes one run record and one deterministic summary under `internal/release/qualification/runs/`, updates `current-state.json`, and enters `awaiting-user-signoff`.

The release-qualification workflow commits only those compact qualification changes back to the release PR. The next workflow run reuses the exact run when every post-qualification change is confined to `internal/release/qualification/`.

# Executor model

The authoritative run records an executor label for provenance, for example `github-actions` or `direct-shell`. The executor label is not a compatibility claim and does not select or require a ChatGPT mode.

GitHub Actions is the normal release executor because it makes the workflow available from any repository-connected maintainer session. Direct shell execution is optional diagnostic capability, not a prerequisite for using the release procedure.

# Agent-behavior scenarios

Routing, calendar reasoning, ambiguous clarification, inbox ingestion, semantic reconciliation/finalization, and role-led uninstall/reinstall are not normal release-gating checks.

They remain **optional behavioral QA** in the synthetic qualification corpus. Run them deliberately when the changed release contract makes them useful, or when evaluating a host. They do not consume release acceptance state and do not require every alpha release to spend fresh agent turns.

A later task may define a generic host protocol for optional behavioral QA, with ChatGPT Work, OpenCode, or another runtime as adapters. PR #122 preserves the implementation history for recovering earlier OpenCode-oriented pieces if needed.

# Evidence model

The authoritative final run binds:

- exact repository revision
- exact source and target release identities and asset hashes
- non-empty qualification executor provenance
- `qualification_mode: deterministic`
- qualification matrix digest
- deterministic qualification driver digest
- deterministic summary file
- automated state `awaiting-user-signoff`
- explicit user signoff only after acceptance

The release gate does not require:

- an LLM audit model
- synthetic consumer-agent transcript evidence
- OpenCode sessions
- ChatGPT thread IDs
- provider session IDs
- a committed pre-edge prerequisite run
- ChatGPT Work

# User acceptance

A clean final run does not accept itself.

After the user explicitly approves the final evidence, a shell-capable environment may run `accept-release-qualification.sh` directly. A repository-connected session without shell access may create the transient `internal/release/qualification/acceptance-request.json` described in `procedure.md` and `qualification-execution.md`.

The release-qualification workflow validates that request, invokes the maintained acceptance implementation, removes the request, and commits the accepted state.

# Release PR blocker

The release PR policy requires:

- valid release identity and adjacent catalog
- all prior accepted release-state history
- one clean current final qualification run
- exact local target/repository revision binding
- explicit user signoff
- no release-content changes after final qualification
- required GitHub Actions checks to pass

The former committed edge-independent prerequisite chain is no longer part of release acceptance. The final run repeats the applicable deterministic checks against the exact reviewed revision instead.

# Semantic judgment boundary

Tooling validates release mechanics. It does not decide project-owned semantic meaning.

Tooling must not guess semantic migration need. The maintained semantic-impact assessment is the reviewed maintainer judgment over the Managed delta, Project-owned compatibility, and Required reconciliation questions. The deterministic final run verifies that the target reaches the correct mechanical state and stops at pending semantic reconciliation when that is the correct release behavior.
