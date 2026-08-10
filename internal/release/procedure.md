---
type: Internal Release Procedure
title: Ava Release Publication Procedure
description: Defines release-local adjacent-edge preparation, semantic-impact assessment, recursive qualification, assembly, approval, publication, and verification.
tags: [internal, releases, publication, verification, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T13:34:00+02:00
---

# Ava Release Publication Procedure

Ava has one release flow for alpha, beta, release candidate, stable, patch, minor, and major releases. The version and channel come from the release-please pull request. Each release PR owns only its new adjacent transition.

## Authoritative release state

The authored upgrade history is an immutable ledger under `internal/release/catalogs/`.

Every published release has a record. The first record is `1.0.0-alpha.1.json`, which owns the bootstrap transition `0.0.0 -> 1.0.0-alpha.1`. The `0.0.0` sentinel is retired by that record because it is not an installed Ava release. There is no exception that permits a release without an edge.

Each `internal/release/catalogs/<target>.json` file contains:

- exactly one edge, `<previous> -> <target>`
- only migrations introduced by that edge
- only semantic guidance introduced by that edge
- only source-retirement decisions made by that release

A release record never copies earlier edges, guidance records, supported-source lists, or cumulative assessments. To resolve an upgrade, tooling starts at the target record, follows `edge.from` recursively through earlier release records until it reaches the source, and then composes those records chronologically in memory.

Every release must:

1. leave every existing catalog record unchanged
2. create only `internal/release/catalogs/<target>.json`
3. author exactly one edge, `<previous> -> <target>`
4. assess only that managed delta for project-owned semantic impact
5. set `semantic_review_required` explicitly
6. add guidance only when that edge requires semantic reconciliation
7. record any source retirement and its reason inside the target release record

A no-impact release still authors the edge with `semantic_review_required: false`. It must not omit the edge or repeat historical impact prose.

Legacy `upgrade-impact.json`, published direct edges, and target-specific cumulative guidance are read-only compatibility evidence. They are never valid inputs for a new release.

## Project-owned semantic-impact assessment

The semantic decision is a maintainer judgment about the compatibility of project-owned context, not a proxy for whether managed behavior changed and not a proxy for whether a deterministic project-file migration exists.

For the exact previous-to-target managed delta, the release author must answer:

1. **Managed delta:** Which managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed?
2. **Project-owned compatibility:** Could valid active project-owned context from the previous release remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible under the target managed contracts?
3. **Required reconciliation:** If yes, which bounded project-owned concepts must be inspected or reconciled before semantic compatibility may advance?

The author must consider plausible active project-owned instruction relationships exposed to the changed managed contract, including roles, workflows, shared instructions, indexes, host entrypoints, metadata, and links. Start from the changed contract and follow bounded dependencies. Do not default to scanning all project-owned content.

Set `semantic_review_required: true` when project-owned context may require semantic inspection or reconciliation because of the managed delta. This remains true even when there is no deterministic project-file edit to perform. Structurally valid project-owned instructions can still encode assumptions that conflict with the target behavior.

When `true`, the adjacent edge must reference transition-local guidance that defines all of the following:

- affected project-owned concepts
- bounded discovery conditions that identify potentially incompatible active context
- completion criteria for proving reconciliation complete

Set `semantic_review_required: false` when the reviewed managed delta cannot make supported project-owned context require semantic reconciliation. A managed behavior change alone is insufficient evidence for `true`. For `false`, the release author must explain why valid project-owned context remains compatible and why a previously complete semantic state may advance mechanically.

The release PR body or review record must preserve the rationale for either decision. The release author owns the initial classification and evidence. The reviewer or approver independently confirms that the rationale applies the project-owned compatibility test and that any `true` guidance is bounded enough to execute.

Deterministic release validation checks representation and consistency only. In particular, `true` requires guidance references and `false` forbids them. Tooling must not guess semantic migration need from changed file paths, managed behavior categories, or the presence or absence of deterministic migrations.

## Release PR completion

Before merging a release PR, the Ava Internal Maintainer must:

1. verify version, manifest, base version, and release channel identity
2. review the exact previous-to-target managed delta
3. complete the project-owned semantic-impact assessment above and record the reviewed rationale
4. create one target record with `compose_adjacent_catalog.py`
5. add only transition-local migrations, guidance, and retirement decisions
6. confirm any `true` semantic guidance names affected concepts, bounded discovery conditions, and completion criteria
7. run `validate_release_pr.py` against the release PR base revision
8. run the complete `internal/release/test.sh` suite
9. confirm all required checks pass
10. merge only after the release-local edge and semantic-impact rationale are accepted

The release policy rejects a missing target record, a record whose edge does not start at the immediately previous release, a missing historical record, extra or cumulative guidance, invalid retirement decisions, guidance artifact digest changes, legacy `upgrade-impact.json` authoring, and any release PR that changes historical catalog JSON files.

## Recursive composition

For an upgrade from source `S` to target `T`:

1. load `internal/release/catalogs/T.json`
2. follow its edge to the immediately previous version
3. continue loading predecessor records until the edge whose `from` version is `S`
4. reverse the selected records into chronological order
5. compose migrations, semantic decisions, guidance, and retirements exactly once

Repository qualification additionally walks the complete ledger from `0.0.0` through the current target. Missing intermediate records, cycles, skipped predecessors, duplicate guidance, and unsupported sources block the release.

## Assembly

`assemble_reviewed.py` reads the target release record and recursively loads its predecessors. It stages guidance referenced by the composed path and mechanically produces one installer-compatible source-to-target projection for each retained source.

Those projections are generated output, not authored release state. Their migration and guidance lists come from the unique adjacent path and apply effective guidance exactly once. The repository never stores a parallel cumulative catalog snapshot.

## Immutable compatibility boundary

Published tags, manifests, assets, checksums, and attestations are immutable. Historical installers may continue to read the representation published with their release. Repository-local cumulative alpha.10 through alpha.12 guidance remains archival and cannot be selected unless referenced by its owning release edge.

## Publication

After the release PR is merged, automation:

1. binds the immutable tag, version, source revision, and channel
2. verifies that the tagged change adds only the target release record
3. recursively validates the complete bootstrap-to-target edge chain
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
- every release from alpha.1 onward has exactly one edge record
- at least three retained historical sources resolve through the recursive chain
- semantic compatibility lag receives outstanding guidance exactly once
- project-owned files remain unchanged until the Upgrade Role applies required guidance
- the installed journal preserves the composed semantic decision and exact guidance paths
