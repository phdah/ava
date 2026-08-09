---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.0.0-alpha.8 to 1.0.0-alpha.12
description: Reconciles project-owned knowledge organization and inbox-ingestion outcomes with Ava 1.0.0-alpha.12.
guidance_schema: 1
guidance_id: 1.0.0-alpha.8-to-1.0.0-alpha.12
from_version: "1.0.0-alpha.8"
to_version: "1.0.0-alpha.12"
semantic_review_required: true
migration_ids: []
supersedes: []
generated:
  by: agent:openai-chatgpt
  at: 2026-08-09T14:15:00+02:00
---

# Upgrade Ava project context from 1.0.0-alpha.8 to 1.0.0-alpha.12

## Summary

This edge carries forward the reviewed project-owned reconciliation introduced before Ava 1.0.0-alpha.10 for knowledge hierarchy promotion and faithful inbox ingestion. Ava 1.0.0-alpha.11 strengthened the managed root router so every request completes Ava routing before substantive handling. Ava 1.0.0-alpha.12 adds bounded acceptance review, explicit audit scope, evidence-based finding admission, and terminating re-review behavior to the managed Change Reviewer role and review workflows.

The router and review-contract changes are managed-only and require no additional project-owned edits.

The deterministic updater replaces managed files only. It must not reorganize project-owned knowledge, reinterpret source material, repair attribution, or decide unresolved taxonomy and source dispositions.

## Changed managed contracts

- `/.ava/base/shared/instructions/knowledge-organization.md` requires durable subjects to have canonical paths and stable semantic groups to become justified child collections.
- `/.ava/base/shared/instructions/inbox-ingestion-fidelity.md` requires complete section disposition, faithful uncertainty and attribution, renderable claim provenance, movement gates, and final-state reconciliation.
- The managed Inbox Ingester, Project Steward, Change Reviewer, and ingest workflow assign and verify those responsibilities.
- `/AGENTS.md` requires Ava routing before every substantive answer, refusal, task execution, or project action. This changes managed routing behavior only.
- The managed Change Reviewer role and review workflows define bounded acceptance, explicit audit scope, finding admission, and re-review termination. These changes do not alter project-owned role, workflow, metadata, registry, or knowledge formats.

No deterministic migration is declared for this edge.

## Affected project-owned concepts

Inspect only:

- mixed or repeatedly grouped `knowledge/**` branches where stable semantic classes or independently maintained durable subjects remain flat
- knowledge documents produced from inbox sources before 1.0.0-alpha.10 when section coverage, uncertainty, attribution, or renderable claim provenance may be incomplete
- direct pending children under `/inbox/` when prior completion reporting lacks a retained section inventory or final-state reconciliation

Do not edit project-owned roles, workflows, registries, metadata, or knowledge solely because `/AGENTS.md` or the managed review contracts changed.

## Required decisions

### `knowledge-hierarchy-classification`

A user decision is required when trusted project context does not establish the canonical collection or durable concept identity.

### `unresolved-source-disposition`

A user decision is required when a substantive source section cannot be safely mapped, classified as non-durable, or retained as a clearly described pending item without deciding new project meaning.

## Semantic migration procedure

1. Do not edit Ava-managed files. Record every affected project-owned path before mutation.
2. Promote only stable semantic groups, preserve canonical subject identity, update direct-child indexes, repair links, and preserve unknown metadata, provenance, and scoped history.
3. For each affected source result, account for every substantive section as `mapped`, `non-durable`, or `pending`.
4. Restore source-faithful uncertainty, causal strength, attribution, approval state, and disagreement where needed.
5. Ensure claim footnotes match `sources[].id`, link to the matching `sources[].resource`, and are supported by that source.
6. Keep sources pending while hierarchy, ownership, fidelity, provenance, or user decisions remain unresolved.
7. Recompute completion reporting from final paths and indexes, recording every inspected or changed file.
8. Run independent semantic review. Structural validation supports but does not replace semantic review.

## Validation and completion criteria

- affected durable subjects have one canonical path
- promoted collections are justified semantic routing choices and their indexes list direct children only
- moved concepts preserve unknown metadata, provenance, history, and valid links
- every selected source section has an explicit disposition
- uncertainty, attribution, approval state, and disagreement match source evidence or recorded decisions
- every claim footnote resolves through matching source metadata to supporting content
- unresolved sources remain pending and completion counts reconcile with final filesystem state
- the migration record names every inspected or changed project-owned file
- blocking decisions are resolved, or semantic status remains blocked
- independent semantic review reports no unresolved hierarchy, fidelity, attribution, provenance, or reconciliation finding

Only then may compatibility advance to `1.0.0-alpha.12`.

## Rollback implications

Fidelity corrections and semantically justified collections can normally remain when rolling back. Preserve the migration record, verify indexes and links, and do not weaken accurate provenance or claims merely to reproduce older managed behavior.
