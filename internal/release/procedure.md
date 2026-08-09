---
type: Internal Release Procedure
title: Ava Release Publication Procedure
description: Defines adjacent-edge release preparation, qualification, assembly, approval, publication, and verification.
tags: [internal, releases, publication, verification, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T17:30:00+02:00
---

# Ava Release Publication Procedure

Ava has one release flow for alpha, beta, release candidate, stable, patch, minor, and major releases. The version and channel come from the release-please pull request. The release PR owns only the new adjacent transition.

## Authoritative release state

The active upgrade history is `internal/release/catalogs/<target>.json`.

Every normal release must:

1. load `internal/release/catalogs/<previous>.json`
2. copy every inherited edge, digest, guidance record, and supported source unchanged
3. add exactly one edge, `<previous> -> <target>`
4. assess only that managed delta for project-owned semantic impact
5. set `semantic_review_required` explicitly
6. add guidance only when that new edge requires semantic reconciliation
7. update `internal/release/catalog-retirements.json`, normally with an empty list

A no-impact release still authors the edge with `semantic_review_required: false`. It must not omit the edge or repeat historical impact prose.

Legacy `upgrade-impact.json`, published direct edges, and target-specific cumulative guidance are read-only compatibility evidence. They are never valid inputs for a new release.

## Release PR completion

Before merging a release PR, the Ava Internal Maintainer must:

1. verify version, manifest, base version, and release channel identity
2. create the target catalog from the previous catalog with `compose_adjacent_catalog.py`
3. review the exact previous-to-target managed delta
4. add only transition-local migrations and guidance
5. retain every inherited supported source or record an explicit retirement reason
6. run `validate_release_pr.py`
7. run the complete `internal/release/test.sh` suite
8. confirm all required checks pass
9. merge only after the catalog delta is accepted

The release policy compares inherited and proposed catalogs. It rejects zero or multiple new edges, skipped or non-adjacent edges, cumulative shortcuts, inherited edge or guidance mutation, guidance artifact digest changes, silent source retirement, and cumulative guidance copied onto the new target.

## Assembly

`assemble_reviewed.py` reads the target catalog and stages only guidance referenced by that catalog. It mechanically composes one installer-compatible source-to-target projection for each retained source.

Those projections are generated output, not authored release state. Their migration and guidance lists come from the unique adjacent path and apply effective guidance exactly once. The active repository never stores a parallel cumulative assessment.

## Immutable compatibility boundary

Published tags, manifests, assets, checksums, and attestations are immutable. Historical installers may continue to read the representation published with their release. Repository-local cumulative alpha.10 through alpha.12 guidance remains archival and cannot be selected unless referenced by the canonical catalog.

## Publication

After the release PR is merged, automation:

1. binds the immutable tag, version, source revision, and channel
2. reruns release identity and catalog-delta validation
3. runs the complete qualification suite
4. assembles twice from the canonical target catalog and requires identical digests
5. validates release conformance
6. attests and uploads assets without replacement
7. publishes the existing draft release

Any failure leaves publication blocked. Existing tags and assets are never moved, overwritten, or reused.

## Post-publication qualification

The first release after a catalog change must prove:

- inherited edge and guidance identities are unchanged
- only the previous-to-target edge was authored
- at least three retained historical sources resolve uniquely
- semantic compatibility lag receives outstanding guidance exactly once
- project-owned files remain unchanged until the Upgrade Role applies required guidance
- the installed journal preserves the composed semantic decision and exact guidance paths
