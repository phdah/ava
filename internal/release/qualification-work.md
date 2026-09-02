---
type: Internal Release Qualification Host Procedure
title: ChatGPT Work Cloud Deterministic Qualification
description: Minimal deterministic Ava release qualification procedure for ChatGPT Work Cloud.
tags: [internal, release, qualification, chatgpt, work, cloud, deterministic]
generated:
  by: agent:openai-chatgpt
  at: 2026-09-02T17:30:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T20:30:00+02:00
---

# Purpose

The normal Ava release gate is deterministic. It deliberately uses **zero delegated qualification agents**.

The ChatGPT Work session is the release orchestrator: it resolves the release PR, reviews the managed delta, makes the maintainer semantic-impact judgment, authors the adjacent edge and any required guidance, runs deterministic qualification commands, inspects GitHub Actions, presents the final evidence, and waits for explicit user acceptance.

Consumer-behavior simulations such as routing, calendar interpretation, ambiguous clarification, inbox ingestion, semantic reconciliation, role-led finalization, and role-led uninstall are **optional behavioral QA**. They are not required to publish a normal release.

# Why the release gate is deterministic

The mandatory release gate answers questions that can be checked without stochastic agent behavior:

- are source and target assets exact and intact?
- does the candidate assemble from the exact repository revision?
- can Ava install into an empty project?
- can Ava install into a mature project without altering existing project-owned bytes?
- are modified, missing, corrupt, and unexpected managed states rejected correctly?
- does the reviewed final candidate contain exactly one source-to-target edge?
- can the previous release upgrade deterministically to the target while preserving project-owned bytes?
- do interrupted upgrade resume, abort, and rollback mechanics behave safely?
- do the normal repository and release tests pass in GitHub Actions?

These checks are stable release-safety evidence. General LLM behavior remains useful QA, but it must not make every alpha release expensive or brittle.

# Work Cloud setup

Run the release process in ChatGPT Work Cloud. Do not use the user's computer for non-CI release qualification.

Create repository-external Work Cloud paths for downloaded assets, the finalized fixture, a read-only test boundary, and execution workspaces. The exact target assets must be assembled from the clean release PR revision being qualified.

The normal GitHub Actions suite remains CI-owned; see **GitHub Actions boundary** below.

# Pre-edge deterministic preflight

Before semantic-impact review or adjacent-edge authoring, assemble the provisional candidate:

```sh
target_assets="$(internal/release/assemble-candidate.sh --phase edge-independent)"
```

Then run:

```sh
internal/release/qualify-release.sh pre-edge \
  --qualification-root "$qualification_root" \
  --execution-root "$run_root/pre-edge" \
  --source-assets "$run_root/assets/source" \
  --target-assets "$target_assets" \
  --test-project "$run_root/test-project"
```

The pre-edge preflight runs only:

- fresh empty install
- mature-project install and project-owned preservation
- modified managed-content rejection
- missing managed-content rejection
- corrupt managed-state rejection
- unexpected managed-content rejection
- finalized corpus and external test-boundary integrity checks

It writes no repository qualification evidence. Its purpose is only to fail fast before spending maintainer effort on the release edge.

If it fails, stop and fix the release candidate before edge authoring.

# Maintainer semantic review and edge authoring

After the pre-edge preflight passes, the same Work session performs the maintained semantic-impact assessment over the exact previous-to-target managed delta and records the decision and rationale.

Then author exactly one adjacent release record for the source-to-target transition, plus only required transition-local guidance, deterministic migrations, and retirement decisions.

No delegated agent is required for this step. This is maintainer judgment over the release itself, not a synthetic consumer scenario.

# Final deterministic qualification

After edge authoring, assemble the reviewed candidate from the new exact release PR revision:

```sh
target_assets="$(internal/release/assemble-candidate.sh --phase edge-dependent)"
```

Use a new repository-external execution root and run:

```sh
internal/release/qualify-release.sh final \
  --qualification-root "$qualification_root" \
  --execution-root "$run_root/final" \
  --source-assets "$run_root/assets/source" \
  --target-assets "$target_assets" \
  --test-project "$run_root/test-project"
```

The final qualification reruns every pre-edge deterministic check and additionally verifies:

- exactly one authentic previous-to-target edge in the final release assets
- one complete deterministic previous-to-target upgrade preserving project-owned bytes
- interrupted upgrade resume
- interrupted upgrade abort
- rollback to the previous release
- the resulting deterministic semantic state, whether mechanically complete or authentically pending maintainer/user reconciliation

A passing final run writes the compact final run record and summary under `internal/release/qualification/runs/`, updates `current-state.json`, and enters `awaiting-user-signoff`.

There is no mandatory independent LLM audit and no mandatory scenario interaction transcript.

# GitHub Actions boundary

The normal pull-request checks remain GitHub Actions work. In particular, `.github/workflows/python-tests.yml` executes the internal Backlog validation, installed-project task-board checks, and `internal/release/test.sh`, which runs the repository Python/unit test suite.

The Work release task must require those checks to pass but **does not duplicate** them in its own cloud shell. It may inspect their results through GitHub. Rerunning the repository test suite inside Work is optional diagnostic work only when investigating a failure, not part of the qualification evidence contract.

# Optional behavioral QA

The synthetic vault still contains behavioral scenarios for routing, calendar interpretation, clarification, inbox ingestion, semantic reconciliation/finalization, and lifecycle behavior.

Those scenarios are optional behavioral QA. Run them deliberately when a release materially changes those contracts, before a larger milestone, or while evaluating an agent host. They are not release acceptance evidence and a failure in an optional behavioral run does not by itself block publication.

A later task may expose these behavioral scenarios through a generic host protocol with adapters for ChatGPT Work, OpenCode, or another capable agent runtime. PR #122 retains the implementation history needed to recover earlier OpenCode-oriented execution if that work is pursued.

# Evidence and acceptance

Only the authoritative final deterministic run is committed as release qualification evidence. It binds:

- exact repository revision
- exact source and target release identities and asset hashes
- qualification matrix digest
- deterministic qualification driver digest
- deterministic scenario summary
- `awaiting-user-signoff` state

The pre-edge preflight is intentionally ephemeral and does not form a revision-ancestry evidence chain.

After the final deterministic run passes and required GitHub Actions checks are green, present the evidence to the user. Only explicit user approval may run `accept-release-qualification.sh` and permit the release PR to merge.

# No local fallback for the Work release procedure

The release procedure currently validates ChatGPT Work Cloud as its non-CI execution environment. Do not silently move qualification to the user's computer if Work execution fails. Report the missing capability.

The deterministic qualification entry point itself contains no OpenCode or LLM runtime dependency, which leaves room for a later generic execution-host design without changing the release-safety checks.
