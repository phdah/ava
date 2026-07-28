# Role Manager Update Log

This log records major conceptual and structural changes to the Role Manager. It does not replace Git history.

## 2026-07-27

- **Role lifecycle identity**: Renamed the Role Generator to the Role Manager and made the role responsible for creation, updates, repair, reorganization, approved identity changes, deprecation, and removal. The generated catalog now routes role lifecycle work through `roles/role-manager/`.
- **Role structure and context rules**: Finalized the five mandatory role files, deterministic required-reading manifests, optional `context/` discovery, and role-scoped log behavior. Added explicit overlap decisions and boundaries against project stewardship, inbox ingestion, independent review, and deterministic validation.
