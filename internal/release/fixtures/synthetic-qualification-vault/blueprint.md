---
type: Internal Qualification Fixture Blueprint
title: Synthetic V1 Qualification Vault Blueprint
description: Reviewed narrative, inventory, reproducibility, and safety contract for the generated Adam qualification corpus.
tags: [internal, release, qualification, fixtures, synthetic-data]
generated:
  by: agent:opencode
  at: 2026-08-07T16:53:38+02:00
updated:
  by: agent:opencode
  at: 2026-08-09T10:57:56+02:00
---

# Synthetic V1 Qualification Vault Blueprint

## Boundary

The fixture is wholly fictional. It does not derive from a private vault, employer material, production data, credentials, or another non-public source. All contact values use reserved or visibly non-functional values.

Generation requires a new or empty explicit output directory outside the Ava repository. The generator resolves symlinks and rejects the repository root and every descendant. Only `<output>/corpus/` is raw ingestion input. Never ingest `image-prompts/`, `oracle/`, or `variants/`.

The corpus is staged in four chronological batch directories. Each batch contains only direct source files so it can be copied into the inbox for one bounded ingestion run:

```text
corpus/
|-- 01-pre-move/          # before 2025-02-15
|-- 02-move-transition/   # 2025-02-15 through 2025-03-02
|-- 03-renovation/        # 2025-03-03 through 2025-03-31
`-- 04-settled/           # 2025-04-01 onward
```

The managed `ingest-inbox` workflow processes direct inbox children, so copy the files from one batch directory rather than the `corpus/` tree itself. Dates and oracle metadata retain the six-month organization without relying on links, tags, aliases, or frontmatter. The complete-pending-inbox variant intentionally flattens all four batches into one direct inbox for its full-corpus scenario.

## Narrative

The sole canonical fact sheet is [blueprint.json](blueprint.json). It fixes Adam Lind's fictional identity, his dog Uno, Northstar Transit Labs AB, two fictional Stockholm addresses, recurring work and personal subjects, and all temporal state transitions.

The interval is 2025-01-01 through 2025-06-30. Adam moves from the old apartment to the new apartment on 2025-02-22. The old address remains historically true in earlier dated sources. The new address becomes current after the move. A kitchen renovation runs from 2025-03-03 through 2025-03-28, during Adam's first full month in the new apartment.

## Fixed Inventory

The deterministic baseline contains exactly 300 raw files. Finalization adds exactly five externally generated images for a complete 305-file corpus.

| Structural class | Count |
|---|---:|
| Diary | 150 |
| Personal todo | 12 |
| Work todo | 12 |
| Running | 24 |
| Reading | 12 |
| Cooking | 18 |
| Dog care | 12 |
| Housing and move | 18 |
| Kitchen renovation | 12 |
| Work artifacts | 18 |
| Household finance | 6 |
| Appointments and travel | 6 |

| Format | Deterministic count |
|---|---:|
| Markdown | 254 |
| Plain text | 15 |
| CSV | 10 |
| DOCX | 7 |
| PDF | 9 |
| PPTX | 2 |
| ICS | 3 |

The five image slots add five structurally decoded PNG files. They cover Uno, the February move, a kitchen receipt, the settled apartment, and a work artifact.

## Reproducibility

The implementation uses the repository's Python 3.11-or-newer runtime contract and no third-party packages. The baseline does not embed the executing interpreter's patch version, and date selection uses SHA-256 ranking rather than runtime-dependent pseudorandom sampling. OOXML archives use stored entries, fixed timestamps, sorted paths, fixed document properties, and no library-generated identifiers. PDF object order, metadata, line wrapping, and timestamps are fixed. Text uses UTF-8, LF endings, and deterministic ordering.

Generate a clean baseline:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py generate /absolute/path/outside/ava/qualification-vault
```

Verify its structure, consistency, formats, inventory, and hashes:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py verify /absolute/path/outside/ava/qualification-vault
```

After an image-capable agent creates the five files at the exact destinations declared in `image-prompts/`, finalize their per-run inventory:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py finalize-images /absolute/path/outside/ava/qualification-vault
```

Materialize all eight isolated qualification variant families after image finalization:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py materialize-variants /absolute/path/outside/ava/qualification-vault
```

Validate a populated scenario run manifest before accepting its pass or fail result:

```sh
python3 internal/release/fixtures/synthetic-qualification-vault/fixture.py verify-run-manifest /absolute/path/outside/ava/run-manifest.json
```

The baseline oracle and prompt bytes are reproducible. Externally generated PNG bytes are not claimed to be reproducible; finalization structurally decodes them and records their actual SHA-256 values and file types.

## Oracle

`oracle/baseline.json` records the fixture revision, seed, Python runtime contract, canonical fact sheet digest, exact source inventory, routing domains, durable subjects, non-durable material, source-section dispositions, qualified claims, duplicates, chronological transitions, and pending image slots.

`oracle/run-manifest.template.json` supplies the schema-shaped starting point for real assembled or published qualification. Actual run evidence must bind release identity, asset URLs and hashes, host and model identity, loaded paths and role announcement order, project-owned before and after hashes, installer and conformance output, transcript, reviewer, and linked finding.

## Variants

Variant construction never edits `corpus/`. It first verifies the finalized baseline, records the corpus inventory, and creates isolated project workspaces plus explicit execution plans for:

1. an empty project
2. a mature mixed private-and-work project with project-owned OpenCode configuration
3. registered private and work roles
4. the complete pending inbox corpus
5. modified, missing, corrupt, and unexpected managed-content scenarios
6. resume, abort, rollback, and finalize interrupted-upgrade checkpoints
7. pending project-owned semantic reconciliation
8. uninstall and reinstallation checkpoints

The first four families contain their deterministic project-owned baseline. Managed damage, interrupted upgrades, semantic reconciliation, uninstall, and reinstall require real installed assembled or published assets, so those families remain execution plans until qualification creates and hashes the actual checkpoints. The fixture does not fabricate Ava-managed state or claim that a plan is a materialized managed state or execution evidence.
