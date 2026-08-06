---
type: Internal Development Task
title: Restore Complete Prerelease Upgrade Coverage
description: Prevent release preparation from stranding supported installations and require reviewed per-source managed, migration, guidance, semantic, and cumulative-note assessments.
tags: [internal, roadmap, dogfood, releases, upgrades, migrations, guidance, blocker]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 5
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.6 through 1.0.0-alpha.7
generated:
  by: agent:openai-chatgpt
  at: 2026-08-06T09:25:50+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T13:45:00+02:00
---

# Restore Complete Prerelease Upgrade Coverage

## Observed behavior

The published `1.0.0-alpha.6` release omitted the immediately preceding `1.0.0-alpha.5` source. The subsequent `1.0.0-alpha.7` release declared only `1.0.0-alpha.6`, so an alpha.5 installation cannot reach a valid newer release through the published graph.

The release process also treated a source list as sufficient without requiring an explicit source-to-target assessment of managed changes, deterministic migrations, semantic guidance, and cumulative release notes.

## Root cause

Release preparation validated only release-specific declarations copied into several prerelease fixtures. It did not inherit the direct source commitments of the previous immutable release, did not protect known stranded sources, and did not bind assembled edges to one reviewed source assessment.

The implementation also mixed generic release machinery with data for a presumed next version. That made the flow specific to the next alpha instead of reusable for release candidates and stable releases.

## Corrective design

The repository provides one generic release flow:

1. A releasable implementation pull request merges to `main`.
2. Release-please creates or updates its release pull request.
3. The release pull request initially fails because no reviewed impact exists for its proposed target.
4. An agent inspects all included changes and completes `internal/release/upgrade-impact.json` directly on the release-please branch.
5. Qualification derives required direct sources from the previous version, the previous release's direct sources, and channel-neutral protected-source policy.
6. The agent validates actual tagged deltas, cumulative changelog coverage, migrations, guidance, and semantic decisions.
7. The release pull request is merged only after all checks pass.
8. The exact tagged revision is requalified, assembled, attested, and published.

Current release edges come only from `upgrade-impact.json`. Historical tags that predate that file are read through their immutable legacy `upgrade-sources.txt` declarations.

## Scope

- keep release tooling independent of any presumed next version
- support alpha, beta, release candidate, and stable SemVer targets
- require release-please configuration to match the proposed channel
- inherit direct sources from immutable previous release state
- protect explicitly retained installed sources through channel-neutral policy
- allow inherited sources to be retired only with a reviewed reason
- require exact per-source managed payload deltas
- require explicit migration, guidance, and semantic-review assessments
- require exact cumulative changelog coverage from each source through the target
- derive assembled manifest edges directly from the reviewed impact
- keep release-specific edges and assessments off ordinary implementation branches
- preserve published release immutability

## Completion criteria

- an incomplete release-please pull request fails qualification
- the same validator and reviewed assembler accept representative alpha, release candidate, stable, and stable patch releases
- the immediately previous version and inherited direct sources cannot be silently omitted
- protected sources require a separate policy change before retirement
- every declared source has reviewed managed-change, migration, guidance, semantic, and cumulative-note data
- generated `migration_ids`, `guidance_paths`, and source edges exactly match the reviewed impact
- no production release logic hardcodes the next Ava release version
- the eventual corrective release declares and validates the required real source edges
- real version-pinned source installations upgrade successfully and preserve project-owned files byte-for-byte

## Resolution evidence

Draft PR [#60](https://github.com/phdah/ava/pull/60) implements the generic release-PR completion machinery:

- release identity and channel validation is target-derived
- direct source requirements are inherited from immutable release history
- `upgrade-impact.json` is the sole current edge declaration
- reviewed assembly derives edge sources from that impact
- tests cover alpha, release candidate, stable, stable patch, inheritance, retirement, exact cumulative notes, managed deltas, and edge assembly
- future-version transition fixtures and release-specific impact data were removed from the implementation branch

The finding remains pending until a corrective immutable release uses this flow and real affected installations upgrade successfully.
