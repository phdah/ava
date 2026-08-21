---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.0.0-alpha.14 to 1.0.0-alpha.15
description: Reconciles project-owned inbox, ingestion, and calendar assumptions with Ava 1.0.0-alpha.15.
guidance_schema: 1
guidance_id: 1.0.0-alpha.14-to-1.0.0-alpha.15
from_version: "1.0.0-alpha.14"
to_version: "1.0.0-alpha.15"
semantic_review_required: true
migration_ids: []
supersedes: []
generated:
  by: agent:openai-opencode
  at: 2026-08-21T00:00:00Z
---

# Upgrade Ava project context from 1.0.0-alpha.14 to 1.0.0-alpha.15

## Summary

Ava 1.0.0-alpha.15 repairs project-root context loading for Inbox Ingester, strengthens ingestion history, provenance, delegated-batch, and completion rules, and conditionally requires deterministic calendar verification before relative language becomes a durable fact. Active project-owned inbox conventions, ingestion workflows, or related instructions may remain structurally valid while encoding assumptions that conflict with these managed rules. Semantic review is therefore required. The updater replaces managed files only and must not infer or rewrite project-owned intent.

The release also records every guidance-driven project-owned path inspected during semantic reconciliation and moves bounded successful-upgrade finalization to Ava Maintenance. Those managed evidence and lifecycle changes do not independently require project-owned content edits.

## Changed managed contracts

- `/.ava/base/roles/inbox-ingester/index.md` now loads the project-root `/inbox/index.md` convention correctly and treats it as active project-owned context during ingestion.
- `/.ava/base/roles/inbox-ingester/` and `/.ava/base/workflows/ingest-inbox.md` preserve all pre-existing scoped history verbatim, permit at most one independently required nearest-scope entry, and hand cleanup or retirement decisions to Project Steward.
- `/.ava/base/shared/instructions/inbox-ingestion-fidelity.md` requires one exact selected-source ledger, disjoint delegated source ownership, complete per-source evidence, coordinator reconciliation, and precise claim-level attribution when source claims could otherwise be confused.
- `/.ava/base/shared/instructions/calendar-verification.md` conditionally requires a source-established reference context and deterministic verification before relative calendar language is persisted as an absolute fact.
- `/.ava/base/roles/upgrade-role/` and the public upgrade journal schema record each inspected project-owned path exactly once, using `inspected` and `retained` when no mutation is required.
- `/.ava/base/roles/ava-maintenance/` and the managed state router make Ava Maintenance responsible for protocol-bounded terminal finalization and keep ordinary routing blocked while transaction storage remains.

No deterministic project-owned migration is declared for this edge.

## Affected project-owned concepts

Inspect only active project-owned context that can participate in the changed behavior:

- `/inbox/index.md` when present. Confirm that its pending and processed conventions do not weaken source preservation, scoped-history, provenance, exact-once reconciliation, or completion rules. If absent, inspect only whether the project actively uses Inbox Ingester or the managed `ingest-inbox` workflow and requires a project convention.
- `/workflows/index.md` and only reachable project-owned workflows that resolve to Inbox Ingester or explicitly govern inbox ingestion, delegation, batch completion, provenance, source movement, or scoped logs. Confirm that child success or aggregate counts are not treated as complete without exact per-source evidence and coordinator reconciliation.
- Active project-owned role or shared instructions referenced by an affected workflow, affected registered role, or `/inbox/index.md`. Inspect only statements about ingestion completion, delegated summaries, source attribution, relative-date conversion, or ingestion-time history mutation.
- Pending or incomplete inbox batches that cross the upgrade boundary, or active completion claims based only on child execution, source movement, or aggregate counts. Reconcile every originally selected source and substantive section exactly once before retaining a complete claim.
- Inbox-derived destinations and nearest owning logs only when linked from an active or disputed batch, when differing source-specific claims could be confused, or when history cleanup is a stated prerequisite. Do not scan unrelated project knowledge.
- Durable active calendar facts only when provenance or an explicit weekday/date relationship shows that an absolute value was derived from relative language. Establish the source reference context and verify the relationship deterministically.

The upgrade evidence must record every project-owned path actually inspected or changed. Inspection alone does not authorize unrelated edits.

## Required decisions

### `project-ingestion-intent`

A user decision is required only when active project-owned context intentionally permits weaker ingestion completion, attribution, history mutation, or relative-calendar behavior and project intent does not establish whether the rule is a narrower compatible policy or a stale assumption. Keep the affected context and semantic compatibility unresolved until its intended authority and outcome are decided.

## Semantic migration procedure

1. Do not edit managed files. Record every project-owned path inspected or changed exactly once in the upgrade journal.
2. Follow the bounded discovery conditions above from active registries, conventions, workflows, and instruction links. Do not perform a blanket project scan.
3. Reconcile stale project-owned ingestion rules with exact selected-source inventory, disjoint delegated ownership, complete per-source evidence, coordinator final-state reconciliation, precise attribution, and additive-only nearest-scope history behavior.
4. For active or disputed cross-version batches, verify each selected source and substantive section against final pending, processed, destination, and index state. Keep incomplete or unreconciled sources pending.
5. For affected calendar facts, establish the source-relative reference context and verify material calendar relationships deterministically. Preserve relative wording or record an unresolved decision when the reference context is ambiguous.
6. Preserve intentional narrower project safeguards when they do not weaken managed authority or completion requirements.
7. If `project-ingestion-intent` is triggered, record the unresolved decision and stop compatibility completion until the user resolves it.
8. Run independent semantic review of affected project-owned context. Structural validation supports the review but does not prove semantic compatibility.

## Validation and completion criteria

- active project-owned inbox conventions and ingestion workflows do not weaken managed source lifecycle, provenance, history, delegation, or completion rules
- every selected source and substantive section in an affected cross-version batch is reconciled exactly once, with no missing or overlapping delegated evidence
- differing source authorship, dates, chronology, certainty, status, proposals, decisions, and outcomes retain precise attribution where confusion is possible
- scoped logs touched by affected ingestion preserve every pre-existing entry verbatim and in relative order, contain at most one independently required nearest-scope addition, and leave cleanup to Project Steward
- affected durable calendar facts have established reference context and deterministic verification, or remain relative or unresolved
- every inspected or changed project-owned path has exactly one journal record; inspection-only paths use `change_type: inspected` and `resolution: retained`
- `project-ingestion-intent` is resolved when triggered
- independent semantic review reports no blocking or major ingestion, provenance, history, workflow, calendar, or instruction-scope finding

Only then may semantic compatibility advance to `1.0.0-alpha.15`.

## Rollback implications

Project-owned edits made for alpha.15 ingestion or calendar rules may be stricter than alpha.14 but are not automatically incompatible with it. Before rollback completes, re-evaluate changed project-owned instructions against alpha.14 managed behavior and preserve inspection-only journal records as evidence rather than rollback work. Do not automatically reverse project-owned edits or discard unresolved source and history decisions.
