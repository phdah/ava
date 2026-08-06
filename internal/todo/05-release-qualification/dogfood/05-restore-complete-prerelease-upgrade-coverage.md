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
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T11:30:00+02:00
---

# Restore Complete Prerelease Upgrade Coverage

## Observed behavior

The published `1.0.0-alpha.6` release does not declare an upgrade edge from `1.0.0-alpha.5`, even though alpha.5 was the immediately preceding published prerelease and had been validated as a realistic installed project state.

The subsequent `1.0.0-alpha.7` release declares only `1.0.0-alpha.6 -> 1.0.0-alpha.7`. An alpha.5 installation therefore cannot upgrade to alpha.6 and cannot reach alpha.7 through a valid chain. The release PR repair for alpha.7 satisfied the immediate previous-version guard but did not audit the complete published support graph.

The alpha.7 release preparation also treated the source declaration as sufficient without recording an explicit assessment of the accumulated source-to-target delta. Ava-managed files may be replaced by normal transactional reconciliation, but every supported edge must still state whether deterministic migrations, semantic guidance, and source-relevant release notes are required. Empty migration and guidance inventories must be a reviewed conclusion rather than an unexamined default.

## Reproduction and evidence

The immutable alpha.6 release source declaration contains alpha.3 and alpha.4 but omits alpha.5. Running the alpha.6 installer in an alpha.5 project therefore resolves no matching edge and reports an unsupported transition.

The immutable alpha.7 declaration contains only alpha.6. Published releases are immutable, so the corrective release must declare direct edges from all currently relevant installed prereleases:

```text
1.0.0-alpha.5 -> 1.0.0-alpha.8
1.0.0-alpha.6 -> 1.0.0-alpha.8
1.0.0-alpha.7 -> 1.0.0-alpha.8
```

For each source, release preparation must compare the source release with the target managed payload and contracts, then explicitly determine:

- which Ava-managed files are retained, replaced, created, or deleted by normal reconciliation
- whether any managed-state transformation requires deterministic migration IDs
- whether any project-owned concept requires semantic review and installed guidance
- which cumulative changes must appear in release notes for a user upgrading from that source

## Classification

This is a `blocker` for the next prerelease. Ava advertises explicit prerelease upgrade support, but a realistic installation on alpha.5 is stranded by immutable release metadata. Publishing another prerelease without repairing that path would repeat the same support failure.

## Root cause

`internal/release/upgrade-sources.txt` is reviewed state for the next release, but alpha.6 retained the earlier alpha.3 and alpha.4 sources and omitted the newly published alpha.5 source.

The release PR validator introduced for alpha.7 requires the exact current `main` version and agreement between the source file and two transition fixtures. It does not identify previously supported or realistically installed prereleases that would become stranded. Consistently incomplete declarations can therefore pass.

Release preparation also lacked a mandatory source-to-target impact review binding each edge to actual managed replacements, migration IDs, guidance paths, semantic-review decisions, and cumulative release-note obligations.

## Scope

- declare alpha.8 as a direct upgrade target from alpha.5, alpha.6, and alpha.7
- update `upgrade-sources.txt`, alpha qualification transitions, conformance transitions, and frozen expectations together
- preserve alpha.5, alpha.6, and alpha.7 as explicit protected direct sources until a reviewed support decision removes them
- require release preparation to inspect the managed and semantic delta for every declared source edge
- include exactly the reviewed deterministic migration IDs and guidance paths in the generated release manifest
- permit empty migration or guidance lists only when the review records why normal reconciliation is sufficient and no project-owned semantic work is required
- ensure release notes describe cumulative changes relevant to each supported source
- preserve published release immutability; do not edit or republish alpha.6 or alpha.7 assets
- keep real version-pinned validation pending until immutable alpha.8 assets exist

## Completion criteria

- alpha.8 declares direct manifest edges from alpha.5, alpha.6, and alpha.7
- release qualification fails when a protected installed prerelease is omitted
- every declared edge has a reviewed managed-change, migration, guidance, semantic-review, and cumulative release-note assessment
- generated `migration_ids` and `guidance_paths` exactly match that assessment
- release notes identify cumulative changes relevant to alpha.5, alpha.6, and alpha.7 installations
- real version-pinned alpha.5, alpha.6, and alpha.7 projects upgrade successfully to immutable alpha.8
- the updater replaces all changed unmodified Ava-managed files, advances installed state correctly, and preserves project-owned files byte-for-byte
- regression tests cover the stranded alpha.5 shape, protected-source preservation, managed delta verification, explicit empty decisions, cumulative notes, and reviewed manifest edge assembly
- the implementing PR, corrective published version, and three real upgrade results are recorded as resolution evidence
- the dogfood, phase, and roadmap indexes remain aligned

## Resolution evidence

Repository implementation is complete in this change:

- `upgrade-sources.txt`, alpha qualification, and conformance fixtures prepare direct alpha.5, alpha.6, and alpha.7 edges to alpha.8
- `protected_direct_sources` prevents a release proposal from silently dropping one of those installed prereleases
- `upgrade-impact.json` records exact per-source managed changes and explicit migration, guidance, semantic, and cumulative-note decisions
- `validate_upgrade_impact.py` verifies the protected set, actual tagged managed payload deltas, explicit review fields, and changelog coverage
- `assemble_reviewed.py` writes each manifest edge from the reviewed migration and guidance lists and refreshes release checksums
- focused regression coverage passes locally

The finding remains pending until alpha.8 is published immutably and all three real source installations upgrade successfully with project-owned files preserved. Finding 06 is now the next actionable blocker and should be included before that publication.
