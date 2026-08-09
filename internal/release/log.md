# Ava Release Implementation Log

This log records major conceptual and structural changes to Ava's internal release implementation. It does not replace Git history.

## 2026-08-09

- **Strict recursive adjacent release authoring**: Normalized retained alpha.5 through alpha.12 history into immutable release-local records, with exactly one previous-to-target edge per file. Removed active `upgrade-impact.json` authoring, made cumulative guidance non-selectable archival evidence, and changed release validation to reject historical record changes. Upgrade qualification and release assembly now follow predecessor records recursively and derive installer-compatible source projections in memory.
- **Adjacent upgrade edge catalogs**: Added separate managed and semantic path resolution, supported-source retention, exact-once guidance composition with explicit supersession, catalog composition and validation tools, a multi-edge fixture, and regression coverage for invalid graphs and semantically lagging projects.

## 2026-08-07

- **Synthetic v1 qualification fixture**: Added a repository-only standard-library generator for a reproducible 300-file fictional corpus, external image slots, semantic oracle, run-evidence contract, and isolated qualification variants.

## 2026-08-05

- **Isolated release PR policy gate**: Added a required-check workflow for release-please proposals while ordinary pull requests remain unaffected.

## 2026-08-04

- **Executable alpha qualification**: Added frozen readiness gates, defect classes, source policy, reproducible assembly proof, and transition fixtures.
- **Release preparation automation**: Added release-please coordination, Conventional Commit validation, immutable draft releases, exact-SHA qualification, attestation, and non-clobbering publication.

## 2026-08-03

- **Deterministic release assembly**: Added reproducible release assets, explicit installed mappings, checksums, identity, guidance, migrations, and project scaffolds.
- **Thin installer and updater**: Added the distributed POSIX shell entry point with embedded Python.
- **Managed transaction protocol**: Added installation, upgrades, reconciliation, recovery, rollback, and semantic blocking.
- **Restricted migrations**: Added declarative apply and verify operations.
- **Explicit source ownership**: Separated managed base and project scaffold sources.
- **Unified conformance validation**: Added repository, installed-project, and release validation.
