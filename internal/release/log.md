# Ava Release Implementation Log

This log records major conceptual and structural changes to Ava's internal release implementation. It does not replace Git history.

## 2026-08-03

- **Deterministic release assembly**: Added reproducible construction of the exact seven GitHub Release assets, explicit source-to-installed mapping, checksums, embedded identity, guidance and migration inventories, and create-if-absent project scaffolds.
- **Thin installer and updater**: Added one distributed POSIX shell entry point with embedded Python for strict release-state, archive, path, transaction, and checksum handling.
- **Managed transaction protocol**: Implemented fresh installation, direct and chained upgrades, three-way managed reconciliation, manifest-last commit, durable backup, resume, abort, rollback, finalization, and semantic upgrade blocking.
- **Restricted migrations**: Selected declarative JSON apply and verify operations for the initial migration protocol so migrations cannot obtain arbitrary filesystem execution authority.
- **Explicit source ownership**: Added a separate project-scaffold source root while retaining `templates/base/` as authored managed-base and format-reference source material. Host instruction files remain project-owned and are referenced only through optional installed metadata.
- **Implementation validation**: Added focused integration coverage for installation, adoption, conflicts, unsafe archives, symlink escapes, project-provided host entrypoints, migrations, chained upgrades, semantic state, and rollback.
