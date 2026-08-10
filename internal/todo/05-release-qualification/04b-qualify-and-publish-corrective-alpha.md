---
type: Internal Development Task
title: Qualify and Publish the Corrective Alpha
description: Publish the completed dogfood corrections as one immutable alpha, then collect the required published-release evidence before release-candidate preparation.
tags: [internal, roadmap, alpha, qualification, publishing, dogfood]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 4.2
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T15:45:02+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T16:23:00+02:00
---

# Qualify and Publish the Corrective Alpha

## Purpose

Publish the completed dogfood corrections through one new immutable alpha and use its pinned public assets to collect the real-release evidence required before Ava can close alpha dogfooding and prepare the release candidate.

Do not hard-code a planned alpha number in this task. Release-please determines the actual next prerelease version and channel from the repository state at execution time. Never move, replace, or reuse an immutable published tag.

Use [Step 2 of the V1 Release Operator Path](v1-release-operator-path.md#step-2-qualify-and-publish-the-corrective-alpha) as the practical operator sequence. Use the maintained [release publication procedure](../../release/procedure.md) as the authoritative release-authoring contract.

## Dependencies

Do not complete or publish the corrective alpha until:

- all currently recorded blocker and `required-v1` dogfood findings are implementation-complete
- the [synthetic v1 qualification vault](04a-build-synthetic-qualification-vault.md) has met its Step 1 qualification gate; its corpus and images are already user-confirmed as generated, but ingestion, review, lifecycle, and execution-evidence qualification still remain
- no newly discovered blocker prevents prerelease publication
- the exact target version and source revision receive approval through the maintained release pull-request process

## Release preparation

- let release-please derive the canonical target and channel
- review only the exact previous-to-target managed delta
- complete the project-owned semantic-impact assessment and preserve reviewed rationale for the resulting `semantic_review_required` decision
- author exactly one immutable previous-to-target record under `internal/release/catalogs/<target>.json`
- add only transition-local guidance, migrations, and retirement decisions introduced by that edge
- do not author or update `internal/release/upgrade-impact.json`; it is archival compatibility evidence only
- do not author cumulative target-specific guidance or copy earlier edge records into the new release record
- preserve every historical catalog record unchanged
- validate the release PR against its base revision with `internal/release/validate_release_pr.py`
- run the complete `internal/release/test.sh` suite
- require the maintained release automation to qualify and reproducibly assemble the exact tagged revision before publication

## Published-asset qualification

After publication, use version-pinned immutable assets to:

- install into the empty and mature qualification-vault variants
- upgrade every source declared by the published release path while preserving baseline project-owned files until explicit semantic reconciliation
- verify managed-state gating, deterministic recovery, semantic reconciliation, and terminal finalization through the actual installed contracts
- verify no successful terminal operation leaves the transaction workspace behind
- verify Ava Maintenance reaches healthy normal state without requiring an installed `ava` binary for successful terminal finalization
- exercise finding 12's realistic multi-turn routing transitions in a fresh installed-project session
- exercise finding 15's fresh-agent semantic reconciliation and agent-driven finalization path
- repeat representative inbox ingestion and obtain isolated Change Reviewer results for hierarchy and fidelity
- exercise no-clear-match and ambiguous requests and verify explicit unresolved routing without host-persona fallback
- repeat a clean OpenCode session to prove canonical router discovery is not accidental session residue
- bind the release identity, pinned asset URLs and digests, transcripts, conformance results, project-owned before-and-after hashes, and pass/fail outcomes into the qualification evidence manifests

## Completion criteria

- one immutable corrective alpha is published from the approved source revision
- every declared upgrade source reaches a recorded terminal state through the published assets
- every completed dogfood finding that names a published-version or realistic-project evidence gate has that evidence recorded
- finding 12 has realistic multi-turn installed-project evidence
- finding 15 has fresh-agent terminal-finalization evidence with no binary lookup dependency
- the generated qualification vault passes the required routing, ingestion, review, hierarchy, upgrade, recovery, finalization, and maintenance checks
- the release URL, revision, asset digests, per-source outcomes, transcripts, and conformance results are bound in valid qualification evidence manifests
- no blocker or `required-v1` finding remains pending and every newly discovered release-relevant failure has a numbered dogfood finding and disposition

Completing this task does not itself complete dogfooding. After this task passes, the next step is the explicit user-owned dogfood closure gate defined in the [V1 Release Operator Path](v1-release-operator-path.md#step-3-close-alpha-dogfooding).
