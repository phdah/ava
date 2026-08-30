---
id: ava-541
title: Build the synthetic v1 qualification vault
status: Done
assignee: []
created_date: ''
updated_date: '2026-08-30 18:14'
labels:
  - internal
  - roadmap
  - phase-05
  - release
  - qualification
dependencies: []
ordinal: 541
---

## Description

Generate and qualify Ava's reproducible six-month synthetic corpus for V1 release qualification. This supporting release task is intentionally parked with the rest of release progression.

## Qualification fixture contract

The fixture models fictional Adam in Stockholm from 2025-01-01 through 2025-06-30, including a February apartment move, March kitchen renovation, work projects, dog care, running, reading, Neapolitan pizza, household administration, purchases, appointments, travel, and changing time-bound facts. Canonical facts and chronology come from one machine-readable fact sheet.

Generated output must remain outside the Ava repository. The maintained baseline is 300 deterministic generated sources plus exactly five pinned fictional PNG inputs, yielding a finalized 305-source corpus. The generator uses fixed inputs/seed and normalized document metadata so clean runs reproduce the same inventories and digests. Supported source formats include Markdown, text, DOCX, PDF, PPTX, CSV, ICS, and the five pinned images.

The oracle records canonical facts, source inventory, expected durable/non-durable outcomes, section dispositions, uncertainty/attribution requirements, chronology, duplicates, routing expectations, and image states. Qualification agents do not receive the evaluator-only oracle.

## Qualification families

The fixture materializes isolated variants for:

1. empty project before installation
2. mature mixed private/work project
3. project with registered private/work roles
4. pending inbox corpus, now minimized to the maintained representative seven-source live ingestion set while preserving the immutable 305-file baseline
5. modified, missing, corrupt, and unexpected managed content
6. interrupted deterministic upgrade states
7. pending project-owned semantic reconciliation
8. uninstall followed by reinstallation

The maintained qualification machinery covers installation, routing, ingestion, hierarchy/fidelity, damaged state, semantic reconciliation, finalization, rollback, resume, abort, uninstall, reinstall, project-owned preservation, and independent semantic audit.

## Repository implementation evidence

The fixture implementation lives under `internal/release/fixtures/synthetic-qualification-vault/` and remains excluded from assembled user-facing release assets. It includes generation, verification, pinned-image installation/finalization, deterministic variant materialization, qualification-only interrupted-upgrade checkpoints, schemas, tests, and boundary validation.

Recorded deterministic baseline evidence:

- baseline oracle SHA-256: `fe65371084f6bdb2ae38da0fe31e4be3fda9be8ebe93f6fbc80b168e86d5ca46`
- generated corpus: 300 files
- batch counts: 77 pre-move, 37 move-transition, 46 renovation, 140 settled
- pinned images: 5
- finalized corpus: 305 files
- clean retained generations were byte-identical across CPython 3.11.14 and 3.13.12

## State at Backlog.md migration

Corpus generation, five-image acceptance/pinning, image finalization, finalized-corpus verification, all eight variant families, routing/hierarchy/fidelity/damaged-state/semantic/finalization/rollback/uninstall/reinstall coverage, authentic resume/abort checkpoints, calendar regression coverage, and the maintained 17-scenario runner are implementation-complete.

The representative live `complete-pending-inbox` variant was intentionally reduced to exactly seven sources, one for each maintained text/document format while preserving mapped, non-durable, and pending disposition coverage. The full 305-file corpus remains immutable evaluator/source evidence.

The remaining release-specific obligation before this task can complete is a fresh exact-candidate qualification run with complete evidence/signoff when release progression is explicitly resumed. Do not regenerate or refinalize the corpus or images unless qualification exposes an actual fixture defect or invalid evidence.

This task is historical parked release state, not the active queue.
