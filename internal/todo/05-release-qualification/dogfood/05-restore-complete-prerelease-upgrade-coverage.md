---
type: Internal Development Task
title: Restore Complete Prerelease Upgrade Coverage
description: Repair the stranded alpha.5 upgrade path and require each corrective prerelease edge to account explicitly for managed changes, deterministic migrations, semantic guidance, and cumulative release notes.
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
---

# Restore Complete Prerelease Upgrade Coverage

## Observed behavior

The published `1.0.0-alpha.6` release does not declare an upgrade edge from `1.0.0-alpha.5`, even though alpha.5 was the immediately preceding published prerelease and had been validated as a realistic installed project state.

The subsequent `1.0.0-alpha.7` release declares only `1.0.0-alpha.6 -> 1.0.0-alpha.7`. An alpha.5 installation therefore cannot upgrade to alpha.6 and cannot reach alpha.7 through a valid chain. The release PR repair for alpha.7 satisfied the immediate previous-version guard but did not audit the complete published support graph.

The alpha.7 release preparation also treated the source declaration as sufficient without recording an explicit assessment of the accumulated source-to-target delta. Ava-managed files may be replaced by the normal transactional reconciliation mechanism, but every supported edge must still state whether deterministic migrations, semantic guidance, and source-relevant release notes are required. Empty migration and guidance inventories must be an explicit reviewed conclusion rather than an unexamined default.

## Reproduction and evidence

The immutable alpha.6 release source declaration contains:

```text
1.0.0-alpha.3
1.0.0-alpha.4
```

It omits `1.0.0-alpha.5`. Running the alpha.6 installer in an alpha.5 project therefore resolves no matching edge and must report an unsupported transition.

The immutable alpha.7 declaration contains only:

```text
1.0.0-alpha.6
```

The alpha.7 release cannot repair alpha.5 through a chained path because the required adjacent `alpha.5 -> alpha.6` edge does not exist. Published releases are immutable, so the next corrective prerelease must declare a direct edge from alpha.5 rather than altering alpha.6 or alpha.7.

The expected corrective target must support direct upgrades from every currently relevant installed prerelease:

```text
1.0.0-alpha.5 -> next corrective prerelease
1.0.0-alpha.6 -> next corrective prerelease
1.0.0-alpha.7 -> next corrective prerelease
```

For each source, release preparation must compare the source release with the target managed payload and contracts, then explicitly determine:

- which Ava-managed files are retained, replaced, created, or deleted by normal reconciliation
- whether any managed-state transformation requires deterministic migration IDs
- whether any project-owned concept requires semantic review and installed guidance
- which cumulative changes must appear in release notes for a user upgrading from that source

## Classification

This is a `blocker` for the next prerelease. Ava advertises explicit prerelease upgrade support, but a realistic installation on alpha.5 is stranded by immutable release metadata. Publishing another prerelease without repairing that path would repeat the same support failure and make release qualification pass a declaration that does not represent the complete intended support graph.

## Root cause

`internal/release/upgrade-sources.txt` is reviewed state for the next release, but alpha.6 retained the earlier alpha.3 and alpha.4 sources and omitted the newly published alpha.5 source.

The release PR validator introduced for alpha.7 requires the exact current `main` version to be present and requires agreement between the source file and two transition fixtures. It does not identify previously supported or realistically installed prereleases that would become stranded. Consistently incomplete declarations can therefore pass.

Release preparation also lacks a mandatory source-to-target impact review that binds the edge to its actual managed replacements, migration IDs, guidance paths, semantic-review decision, and cumulative release-note obligations.

## Scope

- make this the next actionable dogfood implementation task while finding 02 remains pending only for published alpha.7 validation
- declare the next corrective prerelease as a direct upgrade target from alpha.5, alpha.6, and alpha.7
- update `upgrade-sources.txt`, alpha qualification transitions, conformance transitions, and frozen expectations together for the exact corrective version
- strengthen release qualification so reviewed source coverage cannot be reduced to only the immediate previous version when that would strand an intended supported prerelease
- require release preparation to inspect the managed and semantic delta for every declared source edge
- include all required deterministic migration IDs and guidance paths in the generated release manifest
- permit empty migration or guidance lists only when the release review records why normal managed reconciliation is sufficient and why no project-owned semantic work is required
- ensure release notes describe the cumulative user-visible and managed-contract changes relevant to every supported source, including changes first introduced in alpha.6 and alpha.7
- preserve published release immutability; do not edit or republish alpha.6 or alpha.7 assets
- keep the alpha.7 installed-link validation in finding 02 rather than merging it into this task

## Completion criteria

- the next corrective prerelease declares direct manifest edges from alpha.5, alpha.6, and alpha.7
- release qualification fails when an intended supported installed prerelease is omitted from the reviewed corrective source set
- every declared edge has an explicit reviewed managed-change, migration, guidance, semantic-review, and cumulative release-note assessment
- generated `migration_ids` and `guidance_paths` exactly match that assessment, including an explicit justified empty result when no special instructions are needed
- release notes identify the cumulative changes relevant to alpha.5, alpha.6, and alpha.7 installations
- real version-pinned alpha.5, alpha.6, and alpha.7 projects upgrade successfully to the corrective immutable prerelease
- the updater replaces all changed unmodified Ava-managed files, advances installed state correctly, and preserves project-owned files byte-for-byte
- regression tests cover the stranded alpha.5 shape, preservation of intended supported sources, and edge impact assessment during release preparation
- the implementing PR, corrective published version, and three real upgrade results are recorded as resolution evidence
- the dogfood, phase, and roadmap indexes remain aligned

## Resolution evidence

Pending implementation.
