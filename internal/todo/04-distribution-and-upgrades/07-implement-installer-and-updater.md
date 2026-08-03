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
  at: 2026-08-03T16:30:00+02:00
---

# Implement Installer and Updater

This task is complete.

## Implemented

- deterministic release assembly through [`internal/release/build-assets.sh`](../../../release/build-assets.sh)
- one generated POSIX shell entry point from [`templates/installer/ava-install.sh`](../../../../templates/installer/ava-install.sh)
- an auditable manifest-driven engine packaged inside the verified base archive
- explicit source-to-installed mapping for the managed router, base roles, workflows, shared instructions, state, optional bootstraps, and create-if-absent project scaffolds
- latest-stable and pinned-version URL behavior through immutable release identity embedded during assembly
- convenience and GitHub immutable-release verified bootstrap modes
- target selection, dry-run planning, explicit `/AGENTS.md` adoption, and optional host bootstrap selection
- archive, checksum, identity, path, symlink, collision, managed-file, transition, and semantic-state validation
- direct declared upgrades, explicit intermediate-release refusal for chained paths, deterministic migration execution, and post-apply validation
- target-root transaction staging, managed-file backup, rollback on failure, and manifest-last commit
- separate installed `ava_version`, semantic compatibility, durable `upgrade.json`, and Upgrade Role handoff
- normalized `AVA_PLAN`, `AVA_RESULT`, `AVA_HANDOFF`, and `AVA_ERROR` output

## Validation

[`internal/release/test-installer.sh`](../../../release/test-installer.sh) builds two prerelease fixture distributions and verifies:

- dry-run without target mutation
- clean installation
- explicit direct upgrade
- project-owned scaffold preservation
- locally modified managed-file refusal
- existing router refusal and explicit adoption
- unrecognized `/.ava/` refusal
- unsafe destination rejection without out-of-root writes

[`internal/release/validate-boundaries.sh`](../../../release/validate-boundaries.sh) validates shell syntax, compiled installer-engine source, release-source boundaries, required files, and canonical schema locations.

## Portability and trust

The implementation requires a POSIX shell and Python 3.10 or later. `curl` is required for downloads, a SHA-256 utility is required for integrity checks, and GitHub CLI is required only for verified immutable-release mode.

The complete implementation contract and usage are documented in [Ava Installer and Updater](../../../../distribution/installer.md).

## Next task

[Implement validation, conformance, and upgrade fixtures](08-implement-validation-and-upgrade-fixtures.md).
