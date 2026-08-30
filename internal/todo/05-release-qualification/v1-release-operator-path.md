---
type: Internal Release Qualification Procedure
title: V1 Release Operator Path
description: Canonical ordered path from the current alpha state to Ava 1.0.0.
tags: [internal, roadmap, release, qualification, operator]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T15:58:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-30T15:32:00+02:00
---

# V1 Release Operator Path

## Current status

This release path is currently parked by explicit user decision. Further alpha dogfooding and immediate progression toward `1.0.0` are not the active roadmap queue.

The current implementation queue is defined by `/internal/todo.md`: qualification OpenCode permission hardening is complete, and the remaining infrastructure task is to isolate qualification session inventory before continuing with the reprioritized post-qualification roadmap work. Resume this operator path only when the user explicitly asks to continue V1 release progression.

The `v1.0.0-alpha.15` release exposed qualification-infrastructure defects that are tracked separately as supporting tasks. Their implementation does not itself close alpha dogfooding or authorize release-candidate work.

## Ordered path to `1.0.0`

When resumed, the conceptual order remains:

1. Finish the [synthetic v1 qualification system](04a-build-synthetic-qualification-vault.md) and any open qualification-infrastructure obligations needed for a trustworthy full run.
2. Complete any remaining evidence obligations in [Qualify and Publish the Corrective Alpha](04b-qualify-and-publish-corrective-alpha.md).
3. Obtain explicit user closure of [alpha dogfooding](04-dogfood-alpha-and-track-findings.md).
4. [Prepare, qualify, accept, and publish the `1.0.0` release candidate](05-publish-release-candidate.md).
5. [Stabilize the published release candidate](05a-stabilize-release-candidate.md).
6. [Prepare, qualify, accept, and publish `1.0.0`](06-qualify-and-publish-v1.md).

A new blocker preempts the next prerelease. A `required-v1` dogfood finding preempts the release gate named by its `blocks` field.

## Qualification infrastructure before resumption

The alpha.15 release exposed two concrete hardening tasks outside the dogfood finding stream:

1. [Harden Qualification OpenCode Permissions](04d-harden-qualification-opencode-permissions.md) - complete
2. [Isolate Qualification Session Inventory](04e-isolate-qualification-session-inventory.md) - pending

The completed permission task removes the hidden dependency on user-global temporary-root permission state. The remaining task addresses cross-run session inventory contamination. Neither task adds a failed-state override or exceptional acceptance mechanism.

## Release procedure when resumed

For every future release edge, follow [Ava Release Publication Procedure](../../release/procedure.md):

1. let release-please create or determine the release PR and version
2. complete the semantic-impact assessment and adjacent release record
3. run deterministic validation and tests
4. assemble the local candidate from the clean release PR revision
5. configure the exact published-source to local-target qualification pair
6. run `qualify-release.sh`
7. fix and rerun any genuine `failed` or `needs-review` result
8. obtain explicit user approval when the result is `awaiting-user-signoff`
9. record acceptance with `accept-release-qualification.sh` and commit the qualification state
10. require the Release PR policy check to pass
11. merge and let publication automation publish and verify the immutable release

Qualification infrastructure must be reliable enough that the normal procedure can run without hidden host permission state, historical-session contamination, or manual qualification-state rewriting.

## Dogfood closure

Do not infer alpha dogfood closure from published releases, passing tests, an empty blocker list, or completion of the hardening tasks. Closure remains an explicit user decision.

## Release candidate and stable release

After explicit dogfood closure, prepare the RC through the same mandatory release procedure, stabilize the published RC through the maintained matrix, and only then prepare `1.0.0`.

## Historical acceptance

Existing historical acceptance entries remain governed by the release-quality ledger and release procedure. Do not reinterpret or rewrite them when resuming this path.

## Answering "what is next?"

Read `/internal/todo.md` first. Use this file only when the user explicitly asks to resume or inspect the V1 release path.
