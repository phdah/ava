---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.0.0-alpha.5 to 1.0.0-alpha.10
description: Reconciles project-owned knowledge organization and inbox-ingestion outcomes with Ava 1.0.0-alpha.10.
guidance_schema: 1
guidance_id: 1.0.0-alpha.5-to-1.0.0-alpha.10
from_version: "1.0.0-alpha.5"
to_version: "1.0.0-alpha.10"
semantic_review_required: true
migration_ids: []
supersedes: []
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T11:45:00+02:00
---

# Upgrade Ava project context from 1.0.0-alpha.5 to 1.0.0-alpha.10

## Summary

Ava 1.0.0-alpha.10 changes the managed contracts for knowledge hierarchy promotion and faithful inbox ingestion. Project-owned knowledge branches, pending inbox sources, and previously completed ingestion results may rely on the earlier, less explicit behavior. Semantic review is required before the project can be marked compatible through 1.0.0-alpha.10.

The deterministic updater replaces managed files only. It does not reorganize project-owned knowledge, reinterpret source material, repair attribution, or decide unresolved taxonomy and source dispositions.

## Changed managed contracts

- `/.ava/base/roles/change-reviewer/instructions.md` now requires independent review of durable subject identity, hierarchy promotion, source-section coverage, epistemic fidelity, attribution, renderable claim provenance, and final-state reconciliation.
- `/.ava/base/roles/inbox-ingester/instructions.md` now requires a substantive-section inventory before destination mutation, explicit dispositions for every substantive section, preservation of uncertainty and attribution, renderable claim-level provenance, and final-state reconciliation before a source is processed.
- `/.ava/base/roles/project-steward/instructions.md` now owns project-wide promotion of reusable semantic groups into child collections and preservation of metadata, provenance, links, indexes, and scoped history during reorganization.
- `/.ava/base/shared/instructions/inbox-ingestion-fidelity.md` is a new managed contract defining complete source coverage, epistemic and attribution fidelity, Markdown footnote provenance, source movement gates, and completion reporting.
- `/.ava/base/shared/instructions/knowledge-organization.md` now distinguishes durable concepts from collections and requires semantic hierarchy promotion before mixed flat branches grow further.
- `/.ava/base/workflows/ingest-inbox.md` now requires complete section inventory, fidelity-preserving integration, independent semantic review, and read-only final-state reconciliation.
- Changes to managed indexes and repaired managed links make the revised contracts discoverable but do not themselves require project-owned edits.
- The managed upgrade-role and upgrade-state changes only enforce this reviewed guidance and do not authorize edits outside the affected project-owned scopes below.

No deterministic migration is declared for this edge.

## Affected project-owned concepts

### Knowledge branches and indexes

Inspect a project-owned `knowledge/**/index.md` and its direct children only when at least one of these conditions holds:

- the index uses stable headings or repeated labels to separate reusable classes while all concepts remain direct siblings
- the branch mixes independently maintained durable subjects such as projects, systems, integrations, people, events, or recurring records
- another ingestion would add a sibling to an already mixed flat branch
- an existing concept combines multiple independently maintained durable subjects rather than one durable identity

The required outcome is one canonical path per durable subject, child collections for stable semantic routing classes, direct-child-only indexes, and Markdown links for cross-cutting relationships. Do not create speculative or empty collections, and do not use a numeric file threshold as the promotion rule.

Completion is validated by checking the final parent and child indexes, canonical paths, preserved metadata and source provenance, and all links affected by moves.

### Knowledge documents produced from inbox sources

Inspect a project-owned knowledge document only when its `sources[].resource` references a project-owned inbox source that was processed under an Ava version before 1.0.0-alpha.10, or when the document contains source-attributed claims without renderable Markdown footnote definitions.

The required outcome is:

- every substantive source section has an explicit `mapped`, `non-durable`, or `pending` disposition
- uncertainty, causality, attribution, approval state, and disagreement remain faithful to the source
- every claim-level footnote label matches a `sources[].id`
- every footnote definition links to the source identified by the matching `sources[].resource`
- the cited source actually supports the attributed claim

Completion is validated against the preserved source content, destination metadata, rendered footnotes, and the final section inventory. File-level provenance alone is not evidence that every source topic was integrated.

### Pending inbox sources and completion reports

Inspect direct project-owned children under `/inbox/`, excluding reserved index files and processed containers, when they were previously reported as processed or blocked without a retained section inventory and final-state reconciliation.

A source may move to a processed location only when every substantive section is accounted for and no fidelity, attribution, provenance, taxonomy, or ownership blocker remains. A source with zero substantive sections remains unchanged and pending unless the user explicitly chooses another disposition.

Completion reports must be recomputed from the final filesystem state. Selected-source totals, processed, blocked, unchanged, failed, pending, destination, and concept counts must reconcile with final paths and indexes.

## Required decisions

### `knowledge-hierarchy-classification`

A user decision is required when a repeated group could reasonably be modeled in more than one durable hierarchy and the trusted project context does not establish the intended taxonomy. The decision must select the canonical collection and concept identity, or explicitly retain the current structure. Affected branch moves and their completion checks remain blocked until this is resolved.

### `unresolved-source-disposition`

A user decision is required when a substantive source section cannot be mapped to trusted knowledge, classified as non-durable under existing project intent, or safely left as a clearly described pending item without deciding new project meaning. The affected source must remain pending. Source movement and semantic completion remain blocked until the decision is recorded.

## Semantic migration procedure

1. Do not edit Ava-managed files. Use the installed contracts as the authority for reviewing project-owned content.
2. Identify only knowledge branches and documents matching the discovery conditions above. Record their exact project-owned paths before editing.
3. For each affected knowledge branch, classify durable subjects and reusable semantic groups. When a group is a stable routing decision, create or select the child collection, move the affected concepts, update direct-child indexes, and repair links. Preserve unknown metadata, source provenance, and scoped history.
4. For each affected processed source, reconstruct or verify the substantive-section inventory from the preserved source. Record every section as `mapped`, `non-durable`, or `pending`; there is no implicit ignored state.
5. Compare destination claims with their supporting passages. Restore qualifiers, attribution, approval state, and disagreement where the earlier result overstated certainty or authorship.
6. Ensure claim-level provenance uses renderable Markdown footnotes whose labels match `sources[].id`, whose definitions link to the corresponding `sources[].resource`, and whose sources support the claims.
7. Leave any source pending when section coverage, provenance, hierarchy, ownership, or required user decisions remain unresolved. Do not move a source merely to empty the inbox.
8. Recompute the completion report from final project-owned paths and indexes. Record processed, blocked, unchanged, failed, and pending outcomes and the exact files inspected or changed.
9. Run independent semantic review using the managed Change Reviewer criteria. Deterministic link and metadata validation is supporting evidence only and does not prove semantic fidelity.
10. Copy unresolved blocking decisions into semantic compatibility state. Advance compatibility only after every criterion below passes.

## Validation and completion criteria

All of the following must pass:

- every affected durable subject has one canonical project-owned path
- every promoted collection represents a reusable semantic routing choice rather than a presentation-only heading
- parent and child indexes list direct children only
- moved concepts preserve unknown metadata, source provenance, scoped history, and valid links
- no promotion decision relies on a numeric file-count threshold
- every selected source has a complete substantive-section inventory
- every substantive section is explicitly `mapped`, `non-durable`, or `pending`
- uncertainty, causal strength, attribution, approval state, and disagreement match the supporting sources or explicit project decisions
- every used claim-level footnote has a definition, matches a `sources[].id`, links to its `sources[].resource`, and is supported by that source
- sources with unresolved semantic blockers remain pending and are not reported as processed
- sources with zero substantive sections remain unchanged and pending unless an explicit user decision authorizes another disposition
- final completion counts exclude reserved entries and reconcile with the selected source inventory, final inbox state, destination paths, and final indexes
- the migration record names every inspected or changed project-owned file
- `knowledge-hierarchy-classification` and `unresolved-source-disposition` are absent from unresolved decisions, or semantic status remains blocked
- independent semantic review reports no unresolved hierarchy, fidelity, attribution, provenance, or reconciliation finding

Only after all applicable criteria pass may `compatible_through` advance to `1.0.0-alpha.10` and the semantic transaction be finalized.

## Rollback implications

Project-owned edits that improve source fidelity, preserve uncertainty, add accurate provenance, or create semantically justified collections can usually remain when rolling back to 1.0.0-alpha.5. The older managed roles may not enforce these guarantees, but the project-owned structure remains valid when its indexes and links are internally consistent.

Before rollback is considered complete, explicitly reconcile any hierarchy or reporting convention that depends on 1.0.0-alpha.10 behavior, preserve the migration record, and verify that no source is marked processed solely because the newer completion procedure moved it. Do not undo fidelity corrections or collapse justified collections merely to reproduce earlier behavior.
