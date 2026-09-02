---
type: Internal Release Qualification Execution
title: Session-Neutral Deterministic Qualification
description: Deterministic Ava release qualification executed independently of the active maintainer chat mode.
tags: [internal, release, qualification, deterministic, github-actions, session-neutral]
generated:
  by: agent:openai-chatgpt
  at: 2026-09-02T20:45:00+02:00
---

# Purpose

Ava's normal release qualification is deterministic and does not require an LLM runtime, a delegated agent, or a particular ChatGPT mode.

The active maintainer may work from an ordinary ChatGPT chat, ChatGPT Work, or another repository-capable session. Mandatory release qualification is executed by GitHub Actions against the release PR, so the maintainer session does not need a shell, mutable cloud workspace, OpenCode, Work Local, Codex Local, or a user-hosted process.

The canonical low-level entry point remains:

```sh
internal/release/qualify-release.sh
```

The canonical end-to-end deterministic shell helper is:

```sh
internal/release/run-release-qualification.sh pre-edge|final
```

These commands are executor-neutral. GitHub Actions is the normal executor, while direct shell execution is useful for diagnostics when available.

# Automatic release-PR execution

`.github/workflows/release-qualification.yml` runs on the repository's release-please PR.

It determines the stage from release state:

- if `internal/release/catalogs/<target>.json` does not yet exist, run `pre-edge`
- once that exact adjacent edge exists, run `final`

The workflow sets `AVA_QUALIFICATION_EXECUTOR=github-actions`. The run record stores the executor label only as provenance; acceptance does not depend on a ChatGPT product mode.

# Pre-edge

`pre-edge` is an ephemeral fail-fast check. It:

1. reads the configured exact source -> target qualification pair
2. downloads the exact immutable source release from GitHub
3. verifies the release and each release asset
4. generates and verifies the finalized synthetic qualification vault
5. creates an external byte-integrity test boundary
6. assembles the provisional no-edge target
7. runs deterministic empty-install, mature-install/preservation, and managed-damage checks

It writes no committed qualification evidence.

# Maintainer semantic review

After pre-edge passes, the active maintainer session reviews the exact previous-to-target managed delta, records the project-owned semantic-impact decision and rationale, and authors exactly one adjacent edge plus any required transition-local guidance, migrations, or retirement decisions.

This is the only semantic reasoning required by the normal release procedure. It is maintainer review of the release itself, not synthetic consumer-agent simulation.

# Final qualification

Once the edge exists, the workflow runs `final` from the exact release PR revision.

The final run repeats the pre-edge checks and adds:

- exact previous-to-target edge validation
- real deterministic previous-to-target upgrade
- interrupted upgrade resume
- interrupted upgrade abort
- rollback
- project-owned byte preservation
- mechanically correct target semantic state
- exact source/target/repository identity binding

A passing final run creates the authoritative compact run record and summary under `internal/release/qualification/runs/` and sets the active pair to `awaiting-user-signoff`.

The workflow commits only those qualification files back to the release PR. On the resulting evidence commit, the workflow reuses the existing run when the qualified revision is an ancestor of `HEAD` and every intervening path is under `internal/release/qualification/`.

# User acceptance without shell access

Explicit user approval is still required.

When the active session has shell execution, it may use `accept-release-qualification.sh` directly.

When it does not, the session may use its connected GitHub write capability to add this transient release-PR file:

`internal/release/qualification/acceptance-request.json`

with exactly:

```json
{
  "identity": "user:<stable-identity>",
  "run_id": "<exact-final-run-id>",
  "schema_version": 1
}
```

The request must be created only after explicit user approval. The release-qualification workflow validates it, invokes the maintained acceptance implementation, deletes the request, and commits the accepted state. The request must never survive into the released revision.

# GitHub Actions versus the maintainer session

GitHub Actions owns deterministic execution. The active maintainer session owns orchestration and judgment.

The maintainer session therefore only needs connected repository capabilities sufficient to:

- inspect the release PR and diffs
- edit the qualification pair and release edge/guidance
- inspect workflow results and compact evidence
- create the transient acceptance request after explicit approval
- merge the PR after all gates pass

There is no requirement to switch from normal Chat to Work merely to perform a release.

# Optional behavioral QA

Routing, calendar interpretation, clarification, inbox ingestion, agent-led semantic reconciliation/finalization, and role-led lifecycle scenarios remain optional QA fixtures.

They are intentionally outside the normal publication gate. A future generic behavioral protocol may run them with ChatGPT Work, OpenCode, or another capable host without changing the deterministic release-safety contract.
