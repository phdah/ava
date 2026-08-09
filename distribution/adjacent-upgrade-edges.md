---
type: Ava Distribution Contract Proposal
title: Adjacent Upgrade Edge Catalog
description: Proposed self-contained release graph for deterministic managed upgrades and separately resolved project-owned semantic reconciliation.
tags: [distribution, releases, upgrades, guidance, proposal]
status: proposed
generated:
  by: agent:openai-chatgpt
  at: 2026-08-09T12:30:00+02:00
---

# Adjacent Upgrade Edge Catalog

> **Proposal:** This contract becomes authoritative only when its implementation pull request is approved and merged. Until then, the existing direct source-to-target release contract remains active.

## Purpose

A release should add and review only the new edge from the previous release to the proposed target. It must not re-author cumulative source-to-target assessments or duplicate semantic guidance already reviewed for earlier edges.

The target release remains self-contained. Its release manifest and archives carry every immutable edge, migration, and guidance document needed for the supported source range.

## Catalog

A catalog has:

- one target version
- the source versions accepted as upgrade entry points
- immutable adjacent edge records
- immutable guidance metadata referenced by those edges

Each edge records:

- `from` and `to`
- whether unresolved semantic state may cross the edge
- deterministic migration IDs
- semantic guidance paths
- an explicit semantic-review decision
- `edge_sha256`, calculated from the canonical edge content

An inherited edge must retain its exact content and digest. A release may append one new edge, explicitly retire supported entry points, or add guidance for its new edge. It must not rewrite inherited edges.

## Path resolution

Preflight resolves exactly one path from the installed `ava_version` to the target. A missing path, multiple possible paths, a cycle, an unsupported source, an altered edge digest, or a missing referenced artifact blocks before managed mutation.

The release manifest may contain branches for explicitly supported release channels, but a source-to-target resolution must still be unique.

The updater must not download intermediate release assets. It uses only the selected target release's self-contained edge catalog and archives.

## Separate managed and semantic paths

The updater resolves two paths:

1. the managed path from installed `ava_version` to the target
2. the semantic path from `semantic_compatibility.compatible_through` to the target

Only the managed path contributes deterministic migrations. The semantic path contributes project-owned guidance and the decision to advance or block semantic compatibility.

A project whose managed base is newer than `compatible_through` therefore receives every outstanding semantic obligation exactly once. An edge with no project-owned impact advances compatibility mechanically only when earlier semantic obligations are already complete.

Pending, partial, or blocked semantic state may cross a path only when every traversed edge explicitly permits it.

## Guidance composition

Guidance is evaluated in semantic-edge order. Every guidance ID is loaded at most once.

Guidance remains cumulative unless a later guidance document explicitly lists earlier active guidance IDs in `supersedes`. Supersession is valid only when every named ID is already active. Missing IDs, duplicate application, conflicting identity, or transition mismatch blocks preflight.

## Release authoring and review

For a normal release, maintainers review only:

- the new adjacent managed delta
- the new edge's path-by-path project-owned impact assessment
- the new edge's migrations and guidance
- explicit supported-source retirement, when any
- unchanged identity and checksums for inherited edges and referenced artifacts

Qualification must still exercise every retained supported source. This proves composition without forcing maintainers to rewrite cumulative prose.

## Compatibility transition

The current source-to-target release metadata remains valid during the proposal review. After approval, release tooling may emit the adjacent catalog while retaining read compatibility for already published releases.

The first catalog-based release must import the previously reviewed edge history without changing its meaning. Historical cumulative guidance files may remain repository history, but only immutable adjacent guidance is referenced by the new catalog.
