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
- optional release-declared managed host bootstrap mapping and selection
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
- explicit-only or host-bootstrap discovery reporting without unsupported native claims

## Implementation locations

- [Release assembler](../../../internal/release/assemble.py)
- [Distributed installer source](../../../internal/release/ava-install.sh)
- [Implementation guide](../../../internal/release/installer.md)
- [Focused tests](../../../internal/release/tests/test_installer.py)
- [Project scaffold sources](../../../templates/project-scaffolds/)
- [Optional host bootstrap sources](../../../templates/host-bootstraps/)

## Validation

`sh internal/release/test.sh` passes 11 integration tests covering:

- clean installation and project-owned preservation
- explicit root-router adoption
- managed-file conflict refusal
- checksum failure before mutation
- archive traversal rejection
- symlink escape rejection
- optional host bootstrap installation
- declarative migration execution
- direct and chained upgrades
- semantic pending state and rollback
- rollback conflict detection after a managed edit

The implementation also passes shell syntax checks, Python compilation, and the expanded repository-boundary validator.

## Following task

[Implement validation, conformance, and upgrade fixtures](08-implement-validation-and-upgrade-fixtures.md).
