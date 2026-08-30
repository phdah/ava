---
id: ava-5620
title: "Preserve large-batch inbox fidelity and claim provenance"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5620
---

## Description

Make delegated and large-batch inbox ingestion retain complete per-source section evidence, cross-source claim provenance, and coordinator-owned final reconciliation.

## Migrated task record

Historical metadata: phase 5 finding 20, `required-v1`, blocking release candidate, affected version `1.0.0-alpha.14`, completed after implementation.

### Observed behavior and root cause

A 305-source synthetic ingestion reached deterministic all-pass, but independent audit reported major `QUA-INBOX-ORACLE-001` and `QUA-INBOX-PROVENANCE-002` findings: final knowledge could not prove faithful source-by-source coverage and claim provenance across delegated child sessions. The sessions correctly had no hidden oracle access. The defect was insufficient coordinator-owned evidence after batch splitting.

The fidelity contract had strong per-source requirements but did not explicitly define delegated evidence boundaries. Parent sessions could accept child summaries/counts without proving exact-once source ownership, complete section dispositions, destination realization, source-specific claim attribution, cross-child differences in author/date/chronology/certainty/status/proposal/decision/outcome, and final inventory reconciliation.

### Approved scope and completion criteria

The source-derived substantive inventory remains independent of evaluator oracle data. One coordinator owns an exact selected-source ledger; child work, when used, receives disjoint source subsets and returns complete per-source section/destination/provenance/blocker/validation/final-state evidence; child success is provisional until exact reconciliation; missing/overlapping evidence blocks completion; precise claim attribution is required where reports could be confused; cross-child destination contributions are reconciled; realistic regression covers delegated evidence loss; deterministic validation remains separate from semantic audit; evaluator oracle remains evaluator-only.

### Resolution evidence

`inbox-ingestion-fidelity.md` now defines delegated/large-batch responsibility, a coordinator-owned selected-source ledger, disjoint child evidence, provisional child success and exact final reconciliation. `ingest-inbox.md` carries these requirements into procedure/output and requires precise claim provenance across child boundaries. `inbox-ingestion-fidelity.json` adds a delegated-batch failure case, and `test_inbox_ingestion_fidelity.py` enforces coordinator ledger, disjoint ownership, provisional success, missing-evidence failure and attribution rules.

Release follow-up required rerunning complete pending-inbox qualification so the independent evaluator, using hidden oracle evidence, could reconcile every selected source and substantive expected outcome without blocking/major fidelity or provenance findings.