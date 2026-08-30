---
type: Ava Upgrade Guidance
title: Upgrade Ava project context from 1.0.0-alpha.14 to 1.0.0-alpha.15
description: Reconciles project-owned ingestion, upgrade-lifecycle, and calendar assumptions with Ava 1.0.0-alpha.15.
guidance_schema: 1
guidance_id: 1.0.0-alpha.14-to-1.0.0-alpha.15
from_version: "1.0.0-alpha.14"
to_version: "1.0.0-alpha.15"
semantic_review_required: true
migration_ids: []
supersedes: []
generated:
  by: agent:openai-opencode
  at: 2026-08-29T12:06:33+00:00
---

# Upgrade Ava project context from 1.0.0-alpha.14 to 1.0.0-alpha.15

## Summary

Ava 1.0.0-alpha.15 strengthens inbox-ingestion fidelity and provenance, adds deterministic verification for calendar facts derived from relative language, transfers narrowly bounded successful upgrade finalization to Ava Maintenance, and records semantic inspection-only paths in upgrade state. Existing project-owned trusted knowledge, scoped history, active instructions, or tools may remain structurally valid while encoding alpha.14 assumptions that conflict with these contracts. Semantic review is therefore required. The updater replaces managed files only and must not infer or rewrite project-owned meaning.

## Changed managed contracts

- `/.ava/base/roles/inbox-ingester/` and `/.ava/base/workflows/ingest-inbox.md` now resolve project-root paths explicitly, preserve all existing scoped-history entries verbatim and in order, and require exact selected-source inventories and complete per-source evidence for delegated batches.
- `/.ava/base/shared/instructions/inbox-ingestion-fidelity.md` now requires section-specific dispositions, rendered-output reconciliation, non-durable-content exclusion, explicit handling of ambiguity, and claim-level provenance where source identity, chronology, certainty, status, decision state, or outcome could otherwise be confused.
- `/.ava/base/shared/instructions/calendar-verification.md` now requires deterministic verification before persisting calendar values derived from relative or relational source language. Ambiguous source context must be preserved or clarified rather than guessed.
- `/.ava/base/roles/ava-maintenance/` and `/.ava/base/shared/instructions/upgrade-state-and-routing.md` now grant Ava Maintenance only the defined successful terminal journal transition and transaction cleanup. Normal routing remains blocked while `/.ava/state/transactions/` exists, and interrupted cleanup requires exact journal identity or strictly proven restored-source evidence.
- `/.ava/base/roles/upgrade-role/instructions.md` and the upgrade-state schema now require every guidance-driven inspected project-owned path to be recorded. An unchanged inspection uses `change_type: inspected` and `resolution: retained`; later mutation replaces that inspection-only classification, and inspection-only records do not create rollback work.

No deterministic migration is declared for this edge.

## Affected project-owned concepts

### Inbox ingestion products and instructions

Inspect only:

- active project-owned roles, workflows, and shared instructions that define Inbox Ingester behavior, section dispositions, processed-source completion, delegated batches, provenance, or ingestion-time log mutation
- direct children of `/inbox/processed/`, trusted documents whose provenance references those sources, and scoped logs that reliable provenance or version-control evidence identifies as changed by those ingestions
- multi-source destinations where source author, date, chronology, certainty, status, proposal or decision state, or outcome differs and file-level provenance cannot disambiguate the claims

Completion requires defensible section-by-section dispositions; every mapped claim present in its named destination with qualifiers preserved; non-durable meaning absent from trusted destinations; ambiguous or unsupported completion reconciled or restored to an explicit pending state; required claim-level provenance aligned with source passages; and pre-existing scoped history preserved. When reliable evidence cannot establish lost history or source disposition, record a blocking user decision rather than reconstructing meaning by guesswork.

### Upgrade lifecycle dependencies

Inspect active project-owned roles, workflows, shared instructions, operational knowledge, host entrypoints, and project tools only when they reference finalization or installer commands, an `ava` executable, `upgrade.json`, `project_changes`, rollback reporting, `/.ava/state/transactions/`, terminal journal states, `allowed_operations`, normal-routing availability, or manual managed-state recovery.

Completion requires that project-owned context does not require installer-backed successful finalization, claim broader journal or cleanup authority, permit normal routing while the transaction container exists, reject `change_type: inspected`, or treat inspection-only records as mutations or rollback obligations. Reconcile each incompatible dependency or record a blocking user decision.

### Derived calendar facts

Inspect only active project-owned documents whose source provenance points to relative or relational calendar language and whose persisted text derives a weekday, absolute date, week number, month or year relationship, or equivalent calendar value. Also inspect internally contradictory weekday and date relationships. Already-absolute source-stated dates require no review solely because of this edge.

Completion requires recomputing derived values through a deterministic calendar operation using the source-established reference context, then correcting an inconsistency, restoring source-relative wording, or recording a blocking ambiguity. Do not use the upgrade session's current date unless it is genuinely the source reference.

## Required decisions

### `ingestion-evidence-gap`

A user decision is required when a processed source or trusted destination appears affected but reliable project evidence cannot establish section dispositions, claim provenance, or prior scoped-history content. Do not invent the missing evidence or silently preserve an unsupported completion claim.

### `project-upgrade-authority`

A user decision is required when project-owned instructions or tools intentionally claim finalization, recovery, routing, schema, or rollback behavior incompatible with the target and their narrower intended authority cannot be established from project context.

### `calendar-reference-context`

A user decision is required when a persisted derived calendar fact cannot be verified because the source's reference date or time zone is absent or ambiguous and source-relative wording cannot preserve the intended meaning adequately.

## Semantic migration procedure

1. Do not edit managed files. Record every project-owned path inspected or changed in `upgrade.json.project_changes`; unchanged inspections use `inspected` and `retained`, while a later mutation replaces that classification.
2. Apply the bounded discovery conditions above. Do not expand them into a blanket scan of unrelated project content.
3. Reconcile ingestion instructions and products against the target's section-disposition, provenance, rendered-output, delegated-batch, and additive-history rules.
4. Reconcile project-owned upgrade lifecycle dependencies against the target's finalization authority, transaction-container routing block, inspection metadata, and rollback semantics.
5. Verify only source-derived calendar relationships covered by the bounded conditions, preserving ambiguity rather than deriving from an unrelated current date.
6. Record each triggered unresolved decision and stop compatibility completion until the user resolves it.
7. Run independent semantic review of every changed project-owned instruction or knowledge artifact. Structural validation supports this review but does not prove semantic compatibility.

## Validation and completion criteria

- every relevant processed source has defensible section dispositions and rendered-destination evidence, and non-durable or ambiguous material is not silently represented as trusted mapped meaning
- multi-source claims that could be confused carry sufficient claim-level provenance, and reliable pre-existing scoped history remains verbatim and in relative order
- no active project-owned instruction or tool requires obsolete installer-backed finalization, grants broader managed-state mutation authority, permits normal routing with a transaction container present, or misinterprets inspection-only upgrade records
- every covered derived calendar fact is deterministically verified, restored to source-relative wording, or represented by a blocking ambiguity
- every inspected or changed project-owned path is recorded exactly once with the final applicable classification
- all triggered required decisions are resolved
- independent semantic review reports no unresolved ingestion-fidelity, provenance, calendar, upgrade-authority, routing, state, or rollback finding

Only then may semantic compatibility advance to `1.0.0-alpha.15`.

## Rollback implications

Project-owned edits made for alpha.15 ingestion fidelity, lifecycle authority, inspection metadata, or calendar verification may not remain semantically compatible with alpha.14. Before rollback completes, re-evaluate those edits against alpha.14's managed contracts. Do not retain alpha.15-only project assumptions where they would conflict with the restored managed base, and do not discard provenance or verification improvements that remain valid project knowledge merely because the managed version is older.
