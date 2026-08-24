# Ava Release Implementation Log

This log records major conceptual and structural changes to Ava's internal release implementation. It does not replace Git history.

## 2026-08-24

- **Transient inbox root guard**: The complete pending-inbox qualification scenario now observes direct project-root entries throughout the OpenCode process and fails on any new entry, including one deleted before final conformance. This closes the evidence gap that allowed a temporary ingestion helper script to escape deterministic qualification checks.
- **Removed the hardcoded semantic-inspection-path qualification gate**: The deterministic postcondition added on 2026-08-15 compared each semantic scenario's recorded inspected paths against one fixed, edge-agnostic list. The list was copied from a single prior release edge and did not generalize: it produced false failures against correctly behaving candidates whose guidance named different affected paths. `qualification_postconditions.py` and its dedicated test suite are removed; `qualify-synthetic.sh` runs the scenario runner directly. Judging whether an edge's actual inspected-path set satisfies its own guidance remains an independent-audit responsibility rather than a fixed structural check.

## 2026-08-17

- **Mandatory pre-merge release qualification**: Every release-please PR must qualify its exact locally assembled candidate through the full hands-off OpenCode matrix and independent audit before merge.
- **Explicit qualification acceptance**: A clean automated result stops at `awaiting-user-signoff`; explicit user approval records `qualified-run` acceptance and enables the release PR policy gate.
- **Revision-bound merge safety**: Release acceptance is bound to the qualified repository revision and local asset identity. Any non-qualification content change after qualification requires a fresh run and signoff.
- **Historical release-quality backfill**: Releases `v1.0.0-alpha.1` through `v1.0.0-alpha.14` are explicitly grandfathered as accepted with `basis: historical-backfill`, without claiming they ran the current qualification system.

## 2026-08-15

- **Semantic inspection postconditions**: Added fixture-declared project-path accounting for semantic reconciliation and a deterministic post-run gate that changes otherwise passing scenarios to failure when required inspected or changed paths are missing, duplicated, or unresolved.

## 2026-08-14

- **Hands-off qualification evidence state**: Added one repository-only qualification operation that resolves the reviewed exact release pair, verifies immutable published assets or exact local assets, regenerates the pinned synthetic fixture, runs the maintained matrix, captures top-level and nested OpenCode sessions, runs a fresh read-only audit, and writes compact uncommitted evidence bound to the complete execution identity. Successful automation stops at `awaiting-user-signoff`; blocking or major audit findings stop at `needs-review`.
- **Pinned synthetic image inputs**: Imported the five visually accepted fictional qualification PNGs into the repository-only fixture with an exact manifest and maintained copy command. Clean generated vaults no longer depend on user-local image bytes, while assembly regression coverage keeps every pinned image out of Ava release assets and installed projects.
- **One-command synthetic qualification**: Added one repository-only manual shell entry point for the complete pinned-input synthetic qualification matrix, with safe external workspaces, exact managed-damage interpretation, authentic resume and abort checkpoints, calendar regression coverage, bounded OpenCode execution, interrupted reruns, and deterministic terminal summaries. The complete matrix remains a local maintainer operation; CI exercises only bounded runner tests.

## 2026-08-10

- **Release-impact-based change types**: Conventional Commit types now describe impact on the supported Ava distribution rather than implementation novelty or repository location. Repository-only qualification, tests, CI, documentation, and maintenance remain non-releasable when they do not change produced assets or supported behavior, while internal release tooling remains releasable when its output or guarantees change. Maintained examples and release tests freeze the boundary, including the synthetic qualification vault case.

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
