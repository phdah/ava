# Inbox Ingester Update Log

This log records major conceptual and structural changes to the Inbox Ingester. It does not replace Git history.

## 2026-08-15

- **Delegated batch evidence**: Kept child sessions as a permitted execution strategy while making the coordinating Inbox Ingester responsible for one exact selected-source ledger, disjoint child ownership, complete per-source section evidence, and final reconciliation before any complete batch claim.
- **Cross-source provenance**: Required precise claim-level attribution when differing authors, dates, chronology, certainty, status, proposals, decisions, or outcomes could otherwise be confused across sources or child-session boundaries.

## 2026-08-13

- **Scoped-history preservation boundary**: Limited ingestion-time history authority to one independently required entry at the nearest owning scope. Existing entries must remain verbatim and in their existing relative order; cleanup, correction, consolidation, supersession, retirement, and clean-slate preparation belong to Project Steward maintenance or prior fixture preparation.
