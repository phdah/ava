---
type: Internal Development Task
title: Implement Installer and Updater
description: Implement the thin POSIX shell entry point for fresh installation and explicit versioned upgrades.
tags: [internal, roadmap, shell, installer, updater]
status: pending
phase: 4
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Implement Installer and Updater

This task begins after completion of the preceding design tasks.

## Implement

- one POSIX shell entry point that handles fresh installation and existing-project upgrades
- latest stable and explicit version selection
- target-directory selection with the current directory as the default
- convenience and verified bootstrap flows defined by the release contract
- release asset download, integrity checks, and authenticity verification where requested
- manifest creation and installed `ava_version` detection under the defined Ava-managed path
- managed-file comparison and safe replacement
- deterministic migration execution
- existing-project eligibility checks and the approved adoption, collision, abort, and explicit-resolution behavior
- canonical path normalization for every managed operation
- rejection of absolute paths, parent traversal, symlink escapes, and archive entries that resolve outside the selected target root
- staged grouped changes with atomic apply or rollback behavior where the platform permits it
- expected checksum or version checks before replacing, moving, or deleting existing managed files
- dry-run output that reports every planned create, replace, move, and delete operation, its reason, detected conflicts, and expected validation effects
- validation before apply and after staged changes, before committing the transaction
- clear, normalized failure reporting suitable for both humans and automation
- installation of pending semantic upgrade guidance and separate semantic-compatibility state
- recording of the active upgrade transaction so normal Ava routing remains blocked until semantic completion, rollback, or another defined terminal state
- clear handoff instructions for activating the dedicated Upgrade Role after deterministic work succeeds

## Keep it thin

The script should orchestrate standard filesystem, archive, state-recording, and verification operations. It must not become a general Ava CLI, role navigator, semantic editor, or persistent runtime. Semantic project-owned changes remain the responsibility of the explicit Upgrade Role.

## Completion criteria

- support a clean install into an eligible empty or compatible existing project
- support explicit adoption or safe refusal for pre-existing Ava-like or conflicting project structures
- support an explicit upgrade to a chosen version
- support latest stable through the documented convenience path
- support a separately verified pinned-version path
- fail safely on path collisions, managed-file conflicts, incomplete assets, checksum errors, authenticity failures, unsupported transitions, unsafe archive paths, and out-of-root filesystem resolution
- prove that no installer, updater, migration, rollback, or cleanup operation can modify a path outside the selected target root
- preserve grouped logical changes and avoid partial application when staging, validation, or final apply fails
- clearly distinguish installed `ava_version` from semantic compatibility
- preserve the active-upgrade state and prevent normal operation until the Upgrade Role completes or the protocol exits through another defined terminal state
- remain readable, auditable, and usable through standard shell tooling
- document required system commands, portability assumptions, and trust assumptions
