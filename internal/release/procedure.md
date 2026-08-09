---
type: Internal Release Procedure
title: Ava Release Publication Procedure
description: Defines release-local adjacent-edge preparation, recursive qualification, assembly, approval, publication, and verification.
tags: [internal, releases, publication, verification, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T17:50:00+02:00
---

# Ava Release Publication Procedure

Ava has one release flow for alpha, beta, release candidate, stable, patch, minor, and major releases. The version and channel come from the release-please pull request. Each release PR owns only its new adjacent transition.

## Authoritative release state

The authored upgrade history is an immutable ledger under `internal/release/catalogs/`.

Each `internal/release/catalogs/<target>.json` file contains:

- exactly one edge, `<previous> -> <target>`
- only migrations introduced by that edge
- only semantic guidance introduced by that edge
- only source-retirement decisions made by that release

A release record never copies earlier edges, guidance records, supported-source lists, or cumulative assessments. To resolve an upgrade, tooling starts at the target record, follows `edge.from` recursively through earlier release records until it reaches the source, and then composes those records chronologically in memory.

Every normal release must:

1. leave every existing catalog record unchanged
2. create only `internal/release/catalogs/<target>.json`
3. author exactly one edge, `<previous> -> <target>`
4. assess only that managed delta for project-owned semantic impact
5. set `semantic_review_required` explicitly
6. add guidance only when that edge requires semantic reconciliation
7. record any source retirement and its reason inside the target release record

A no-impact release still authors the edge with `semantic_review_required: false`. It must not omit the edge or repeat historical impact prose.

Legacy `upgrade-impact.json`, published direct edges, and target-specific cumulative guidance are read-only compatibility evidence. They are never valid inputs for a new release.

## Release PR completion

Before merging a release PR, the Ava Internal Maintainer must:

1. verify version, manifest, base version, and release channel identity
2. create one target record with `compose_adjacent_catalog.py`
3. review the exact previous-to-target managed delta
4. add only transition-local migrations, guidance, and retirement decisions
5. run `validate_release_pr.py` against the release PR base revision
6. run the complete `internal/release/test.sh` suite
7. confirm all required checks pass
8. merge only after the release-local edge is accepted

The release policy rejects a missing target record, a record whose edge does not start at the immediately previous release, extra or cumulative guidance, invalid retirement decisions, guidance artifact digest changes, legacy `upgrade-impact.json` authoring, and any release PR that changes historical catalog JSON files.

## Recursive composition

For an upgrade from source `S` to target `T`:

1. load `internal/release/catalogs/T.json`
2. follow its edge to the immediately previous version
3. continue loading predecessor records until the edge whose `from` version is `S`
4. reverse the selected records into chronological order
5. compose migrations, semantic decisions, guidance, and retirements exactly once

Missing intermediate records, cycles, skipped predecessors, duplicate guidance, and unsupported sources block the upgrade.

## Assembly

`assemble_reviewed.py` reads the target release record and recursively loads its predecessors. It stages guidance referenced by the composed path and mechanically produces one installer-compatible source-to-target projection for each retained source.

Those projections are generated output, not authored release state. Their migration and guidance lists come from the unique adjacent path and apply effective guidance exactly once. The repository never stores a parallel cumulative catalog snapshot.

## Immutable compatibility boundary

Published tags, manifests, assets, checksums, and attestations are immutable. Historical installers may continue to read the representation published with their release. Repository-local cumulative alpha.10 through alpha.12 guidance remains archival and cannot be selected unless referenced by its owning release edge.

## Publication

After the release PR is merged, automation:

1. binds the immutable tag, version, source revision, and channel
2. verifies that the tagged change adds only the target release record
3. recursively validates the complete source-to-target edge chain
4. runs the complete qualification suite
5. assembles twice from the recursive records and requires identical digests
6. validates release conformance
7. attests and uploads assets without replacement
8. publishes the existing draft release

Any failure leaves publication blocked. Existing tags and assets are never moved, overwritten, or reused.

## Post-publication qualification

The first release after this change must prove:

- every historical release record remains unchanged
- only the new previous-to-target record was authored
- at least three retained historical sources resolve through the recursive chain
- semantic compatibility lag receives outstanding guidance exactly once
- project-owned files remain unchanged until the Upgrade Role applies required guidance
- the installed journal preserves the composed semantic decision and exact guidance paths
