# Inbox Ingester Update Log

This log records major conceptual and structural changes to the Inbox Ingester. It does not replace Git history.

## 2026-08-13

- **Scoped-history preservation boundary**: Limited ingestion-time history authority to one independently required entry at the nearest owning scope. Existing entries must remain verbatim and in their existing relative order; cleanup, correction, consolidation, supersession, retirement, and clean-slate preparation belong to Project Steward maintenance or prior fixture preparation.
