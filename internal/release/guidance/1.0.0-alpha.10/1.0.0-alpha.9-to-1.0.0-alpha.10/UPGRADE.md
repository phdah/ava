---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.0.0-alpha.9 to 1.0.0-alpha.10
description: Reconciles project-owned knowledge organization and inbox-ingestion outcomes with Ava 1.0.0-alpha.10.
guidance_schema: 1
guidance_id: 1.0.0-alpha.9-to-1.0.0-alpha.10
from_version: "1.0.0-alpha.9"
to_version: "1.0.0-alpha.10"
semantic_review_required: true
migration_ids: []
supersedes: []
generated:
  by: agent:openai-chatgpt
  at: 2026-08-07T11:45:00+02:00
---

# Upgrade Ava project context from 1.0.0-alpha.9 to 1.0.0-alpha.10

## Summary

Ava 1.0.0-alpha.10 adds explicit managed contracts for semantic knowledge-hierarchy promotion and faithful inbox ingestion. Project-owned knowledge branches, processed source results, and pending inbox state may follow the alpha.9 behavior, so semantic review is required. The updater replaces managed files only and must not infer or apply project-owned decisions.

## Changed managed contracts

- `/.ava/base/shared/instructions/knowledge-organization.md` now separates durable concepts from collections and requires promotion before mixed flat branches grow further.
- `/.ava/base/shared/instructions/inbox-ingestion-fidelity.md` is new and requires complete source-section disposition, epistemic and attribution fidelity, renderable claim provenance, movement gates, and final-state reconciliation.
- `/.ava/base/roles/inbox-ingester/instructions.md`, `/.ava/base/roles/project-steward/instructions.md`, and `/.ava/base/roles/change-reviewer/instructions.md` assign the ingestion, reorganization, and independent-review responsibilities for those contracts.
- `/.ava/base/workflows/ingest-inbox.md` now requires complete inventory, fidelity-preserving integration, semantic review, and final reconciliation.
- Managed index changes expose the new fidelity contract but do not independently require project-owned edits.

No deterministic migration is declared for this edge.

## Affected project-owned concepts

Inspect only these bounded scopes:

- `knowledge/**/index.md` branches whose stable headings or repeated labels represent reusable semantic classes while independently maintained subjects remain direct siblings
- mixed flat knowledge branches where another ingestion would add a sibling, or documents that combine multiple independently maintained durable subjects
- knowledge documents whose `sources[].resource` references inbox material processed before 1.0.0-alpha.10, especially when source-attributed claims lack renderable footnote definitions
- direct pending children under `/inbox/`, excluding reserved indexes and processed containers, when prior completion reporting lacks a retained section inventory or final-state reconciliation

The required outcomes are one canonical path per durable subject, justified child collections with direct-child indexes, preserved metadata and provenance, explicit `mapped`, `non-durable`, or `pending` dispositions for every substantive section, faithful uncertainty and attribution, source-matching Markdown footnotes, and final counts reconciled with final paths.

## Required decisions

### `knowledge-hierarchy-classification`

A user decision is required when project context does not establish which durable hierarchy should own a repeated semantic group. The affected moves remain blocked until the canonical collection and concept identities are chosen or the current structure is explicitly retained.

### `unresolved-source-disposition`

A user decision is required when a substantive section cannot be safely mapped, classified as non-durable, or retained as a sufficiently described pending item without deciding new project meaning. The source and semantic completion remain blocked.

## Semantic migration procedure

1. Do not edit managed files. Record the exact affected project-owned paths before mutation.
2. Review only branches matching the discovery conditions. Promote stable semantic groups into child collections, move affected concepts, update direct-child indexes, repair links, and preserve unknown metadata, provenance, and scoped history.
3. For each affected source result, reconstruct or verify a substantive-section inventory. Give every section an explicit `mapped`, `non-durable`, or `pending` disposition.
4. Compare destination claims with source passages. Restore uncertainty, causal strength, attribution, approval state, and disagreement where needed.
5. Ensure every claim-level footnote label matches `sources[].id`, its definition links to the corresponding `sources[].resource`, and the source supports the claim.
6. Keep sources pending while hierarchy, ownership, fidelity, provenance, or user decisions remain unresolved. A source with no substantive sections remains unchanged and pending unless explicitly decided otherwise.
7. Recompute completion reporting from final paths and indexes, recording all inspected or changed files and all processed, blocked, unchanged, failed, and pending outcomes.
8. Run independent semantic review. Structural validation supports the review but does not prove semantic fidelity.

## Validation and completion criteria

- affected durable subjects have one canonical path and justified collections use direct-child indexes
- moved concepts preserve unknown metadata, provenance, history, and valid links
- no collection promotion relies on a numeric file threshold
- every selected source has a complete section inventory and every section has an explicit disposition
- uncertainty, attribution, approval state, and disagreement match source evidence or recorded decisions
- every claim footnote resolves through matching `sources[].id` and `sources[].resource` to supporting content
- unresolved sources remain pending and final counts reconcile with final filesystem state and indexes
- the migration record names every inspected or changed project-owned file
- blocking decisions are resolved, or semantic status remains blocked
- independent semantic review reports no unresolved hierarchy, fidelity, attribution, provenance, or reconciliation finding

Only then may compatibility advance to `1.0.0-alpha.10`.

## Rollback implications

Fidelity corrections and semantically justified collections can normally remain when rolling back to 1.0.0-alpha.9. Before rollback completes, verify indexes and links, preserve the migration record, and ensure no source is considered processed solely because the newer procedure moved it. Do not remove accurate provenance or restore weaker claims merely to reproduce prior behavior.
