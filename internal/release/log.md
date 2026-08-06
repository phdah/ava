# Ava Release Implementation Log

This log records major conceptual and structural changes to Ava's internal release implementation. It does not replace Git history.

## 2026-08-06

- **Protected prerelease source coverage**: Added an explicit protected direct-source set so a corrective release cannot retain only the immediately previous prerelease while stranding another supported installed state.
- **Reviewed per-edge impact assembly**: Added a source-specific review artifact and validator for managed replacements, deterministic migrations, guidance, semantic review, and cumulative release-note coverage. Release assembly now writes each manifest edge from that reviewed assessment.

## 2026-08-05

- **Isolated release PR policy gate**: Added a dedicated required-check workflow that no-ops ordinary pull requests but validates release-please proposals against the current `main` version, upgrade-source declarations, and matching prerelease transition fixtures before merge.

## 2026-08-04

- **Executable alpha qualification**: Added a frozen readiness gate for `1.0.0-alpha.1`, stable defect classes, protected-state blocker impacts, exact version-and-revision publication approval, reproducible assembly proof, explicit first-alpha no-source policy, and tested prerelease upgrade-edge declarations through RC and stable.
- **Release preparation automation**: Added release-please version and changelog management, Conventional Commit pull-request title enforcement, bounded first-alpha bootstrap, immutable tag and draft-release preparation, exact-SHA qualification, reproducible assembly, release conformance, artifact attestation, and non-clobbering draft asset upload while retaining explicit publication approval.

## 2026-08-03

- **Deterministic release assembly**: Added reproducible construction of the exact seven GitHub Release assets, explicit source-to-installed mapping, checksums, embedded identity, guidance and migration inventories, and create-if-absent project scaffolds.
- **Thin installer and updater**: Added one distributed POSIX shell entry point with embedded Python for strict release-state, archive, path, transaction, and checksum handling.
- **Managed transaction protocol**: Implemented fresh installation, direct and chained upgrades, three-way managed reconciliation, manifest-last commit, durable backup, resume, abort, rollback, finalization, and semantic upgrade blocking.
- **Restricted migrations**: Selected declarative JSON apply and verify operations for the initial migration protocol so migrations cannot obtain arbitrary filesystem execution authority.
- **Explicit source ownership**: Added a separate project-scaffold source root while retaining `templates/base/` as authored managed-base and format-reference source material. Host instruction files remain project-owned and are referenced only through optional installed metadata.
- **Implementation validation**: Added focused integration coverage for installation, adoption, conflicts, unsafe archives, symlink escapes, project-provided host entrypoints, migrations, chained upgrades, semantic state, and rollback.
- **Unified conformance validation**: Added one machine-readable validator for repository sources, installed projects, and release assets with stable findings, explicit routing gates, non-destructive host diagnostics, immutable-publication evidence, and an indexed v1 conformance matrix.
