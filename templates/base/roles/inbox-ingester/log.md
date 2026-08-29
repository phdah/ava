# Inbox Ingester Update Log

This log records major conceptual and structural changes to the Inbox Ingester. It does not replace Git history.

## 2026-08-29

- **Agent tool freedom**: Restored freedom to use host-agent tools, scripts, code execution, document readers, temporary helpers, and other execution mechanisms during ingestion. Tool choice does not expand mutation authority or weaken trust, provenance, source-preservation, per-section disposition, rendered reconciliation, or final-state requirements. This reverses only the mechanism-level restriction recorded on 2026-08-24; rendered disposition reconciliation remains required.

## 2026-08-24

- **Rendered disposition reconciliation**: Required per-section `mapped` and `non-durable` decisions to be verified against final rendered trusted destinations before completion totals are accepted. Whole-source promotion fails when it carries non-durable meaning into trusted knowledge, and ambiguous sections remain pending instead of being promoted to complete a source.
- **Ingestion execution boundary**: Prohibited creating or executing ad hoc scripts, generated code, temporary implementation files, or programmatic bulk-content transformers as an ingestion mechanism. Destination content remains direct source or section reasoning and editing; existing deterministic Ava validation tools remain allowed only within their existing scope.

## 2026-08-15

- **Delegated batch evidence**: Kept child sessions as a permitted execution strategy while making the coordinating Inbox Ingester responsible for one exact selected-source ledger, disjoint child ownership, complete per-source section evidence, and final reconciliation before any complete batch claim.
- **Cross-source provenance**: Required precise claim-level attribution when differing authors, dates, chronology, certainty, status, proposals, decisions, or outcomes could otherwise be confused across sources or child-session boundaries.

## 2026-08-13

- **Scoped-history preservation boundary**: Limited ingestion-time history authority to one independently required entry at the nearest owning scope. Existing entries must remain verbatim and in their existing relative order; cleanup, correction, consolidation, supersession, retirement, and clean-slate preparation belong to Project Steward maintenance or prior fixture preparation.
