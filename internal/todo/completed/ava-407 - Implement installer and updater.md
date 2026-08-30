---
id: ava-407
title: "Implement the installer and updater"
status: "Done"
labels: ["internal", "roadmap", "phase-04"]
ordinal: 407
---

## Description

Implement the thin POSIX shell entry point for fresh installation and explicit versioned upgrades. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Implement Installer and Updater
description: Implement the thin POSIX shell entry point for fresh installation and explicit versioned upgrades.
tags: [internal, roadmap, shell, installer, updater]
status: complete
phase: 4
order: 7
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
---

# Implement Installer and Updater

This task is complete.

## Implemented

- deterministic release assembly for the exact seven required GitHub Release assets
- reproducible tar and gzip output with embedded release identity
- explicit source-to-installed mapping with checksums, ownership, role, and operation
- managed base installation under `/AGENTS.md` and `/.ava/base/`
- explicit project-owned create-if-absent scaffolds under `templates/project-scaffolds/`
- optional project-provided host entrypoint validation and project-owned manifest metadata
- latest-stable behavior through the embedded installer fetched from the canonical latest URL
- explicit version selection and target-directory selection
- convenience integrity verification and pinned `gh` immutable-release verification mode
- strict manifest, checksum, asset identity, archive inventory, and release graph validation
- safe archive extraction without links, devices, absolute paths, traversal, or duplicates
- canonical installed-path normalization and symlink escape rejection
- fresh installation, explicit `/AGENTS.md` adoption, and safe refusal of unrecognized `/.ava/`
- three-way managed reconciliation and local managed-modification conflicts
- direct and chained upgrades with adjacent-edge verification
- declarative deterministic migrations restricted to staged managed content
- durable transaction planning, staging, backup, resume, abort, rollback, and finalization
- manifest-last managed commit semantics and handled-failure restoration
- separate installed `ava_version` and semantic compatibility state
- installed release guidance and active semantic upgrade routing block
- human plan output and normalized JSON Lines output
- explicit-only or project-provided host discovery reporting without unsupported native claims

## Implementation locations

- [Release assembler](/internal/release/assemble.py)
- [Distributed installer source](/internal/release/ava-install.sh)
- [Implementation guide](/internal/release/installer.md)
- [Focused tests](/internal/release/tests/test_installer.py)
- [Project scaffold sources](/templates/project-scaffolds/)

## Validation

`sh internal/release/test.sh` covers 13 integration cases including clean installation and project-owned preservation, explicit root-router adoption, managed-file conflict refusal, checksum failure before mutation, archive traversal rejection, symlink escape rejection, project-owned host entrypoint recording/preservation, invalid or reserved host entrypoint refusal, declarative migration execution, direct/chained upgrades, semantic pending state/rollback, and rollback conflict detection.

The implementation also passes shell syntax checks, Python compilation, and the expanded repository-boundary validator.

## Following task

Implement validation, conformance, and upgrade fixtures.