---
type: Internal Development Task
title: Qualify and Publish the Corrective Alpha
description: Publish the routing correction and completed dogfood fixes as one immutable alpha, then collect their required real-release evidence.
tags: [internal, roadmap, alpha, qualification, publishing, dogfood]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 4.2
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T15:45:02+02:00
---

# Qualify and Publish the Corrective Alpha

## Purpose

Turn the completed alpha.10 semantic fixes and the pending mandatory-routing correction into immutable evidence before release-candidate preparation. The current release-please proposal is `1.0.0-alpha.11`; if that version becomes unusable, select a new canonical alpha identifier and never move or reuse an immutable tag.

## Dependencies

Do not complete or publish the corrective alpha until:

- [mandatory role routing](dogfood/07-enforce-role-routing-before-every-response.md) is implemented with regression coverage
- the [synthetic v1 qualification vault](04a-build-synthetic-qualification-vault.md) can be generated reproducibly
- no pending blocker prevents prerelease publication
- the exact target and source revision receive approval through the maintained release pull-request process

## Release preparation

- let release-please derive the canonical target and channel
- complete the reviewed `internal/release/upgrade-impact.json` on the release branch
- include every required inherited and protected source or record an independently approved retirement
- update the maintained transition matrix to the actual published prerelease graph and replace obsolete planned latest-alpha-to-RC assumptions
- provide exact per-source managed deltas, semantic-impact decisions, guidance, migrations, and cumulative changelog coverage
- assemble twice from the exact source revision and require identical asset digests
- run repository, installed, release, boundary, OpenCode, and publication qualification against the assembled assets

## Published-asset qualification

After publication, use version-pinned immutable assets to:

- install into the empty and mature qualification-vault variants
- upgrade every declared direct source while preserving baseline project-owned files until explicit semantic reconciliation
- verify no terminal operation leaves an empty transaction container and Ava Maintenance reports healthy deterministic state
- reconcile every edge that requires semantic review through the exact installed Upgrade Role guidance
- repeat representative ingestion and obtain isolated Change Reviewer results for hierarchy and fidelity
- ask the exact glasses-warranty question in a fresh session and prove state gating and role routing occur before handling
- ask a no-clear-match and an ambiguous request and verify explicit unresolved routing without host-persona fallback
- repeat a clean OpenCode session to prove canonical router discovery is not accidental session residue

## Completion criteria

- one immutable corrective alpha is published from the approved source revision
- every declared direct source upgrades through public assets and has recorded terminal state
- findings 03 through 07 contain their applicable published-version and realistic-project evidence
- the generated qualification vault passes the required routing, ingestion, review, hierarchy, upgrade, and maintenance checks
- the release URL, revision, asset digests, per-source outcomes, transcripts, and conformance results are bound in the qualification evidence manifest
- no blocker remains pending and any newly discovered failure has a numbered dogfood finding

Completing this task does not complete dogfooding. The umbrella remains active until the user explicitly closes it.
