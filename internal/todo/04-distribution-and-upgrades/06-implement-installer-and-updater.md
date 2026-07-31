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
  at: 2026-07-31T10:51:00+02:00
---

# Implement Installer and Updater

This task begins after completion of the preceding design tasks.

Implement the accepted [distribution and ownership contract](/templates/distribution-and-ownership.md). The repository source tree must not be copied verbatim into a project.

## Release assembly

Before installation, produce a complete release manifest that maps every source file to:

- exact installed destination
- ownership class
- checksum
- file role
- create, replace, create-if-absent, or migration behavior

The release assembly must map at least:

- `templates/base/AGENTS.md` to `/AGENTS.md`
- managed default roles, workflows, shared instructions, and base navigation to `/.ava/base/`
- release state to `/.ava/state/`
- release guidance to `/.ava/guidance/`
- minimal project scaffolds to project-root extension paths as create-if-absent, immediately project-owned content
- explicitly selected host bootstrap files to their host-specific root paths as Ava-managed thin pointers

Either reorganize repository sources into explicit managed and project-scaffold roots or generate a mechanically complete mapping from the current source tree. Source location alone must never imply installed ownership.

## Implement

- one POSIX shell entry point that handles fresh installation and existing-project upgrades
- latest stable and explicit version selection
- target-directory selection with the current directory as the default
- convenience and verified bootstrap flows defined by the release contract
- release asset download, integrity checks, and authenticity verification where requested
- manifest creation and installed `ava_version` detection at `/.ava/state/manifest.json`
- active upgrade state at `/.ava/state/upgrade.json`
- managed base installation under `/.ava/base/`
- release guidance installation under `/.ava/guidance/`
- root `/AGENTS.md` installation as the canonical Ava-managed router
- optional host bootstrap selection and reporting without duplicating router semantics
- create-if-absent project scaffolding that is never added to the managed manifest
- managed-file comparison and safe replacement
- deterministic migration execution
- existing-project eligibility checks and the approved adoption, collision, abort, and explicit-resolution behavior
- canonical path normalization for every managed operation
- rejection of absolute paths, parent traversal, symlink escapes, and archive entries that resolve outside the selected target root
- staged grouped changes with atomic apply or rollback behavior where the platform permits it
- expected checksum or version checks before replacing, moving, or deleting existing managed files
- dry-run output that reports every planned create, replace, move, and delete operation, its reason, resulting ownership, detected conflicts, and expected validation effects
- validation before apply and after staged changes, before committing the transaction
- clear, normalized failure reporting suitable for both humans and automation
- installation of pending semantic upgrade guidance and separate semantic-compatibility state
- recording of the active upgrade transaction so normal Ava routing remains blocked until semantic completion, rollback, or another defined terminal state
- clear handoff instructions for activating the dedicated Upgrade Role after deterministic work succeeds

## Adoption behavior

The installer must:

- preserve pre-existing `/index.md`, `/log.md`, `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, and `/inbox/` as project-owned
- skip create-if-absent scaffolds when their paths already exist
- abort on a pre-existing `/AGENTS.md` until an explicit adoption decision preserves or discards its project-specific meaning
- abort on an unrecognized `/.ava/` until an approved adoption or recovery procedure applies
- treat a supported manifest as an installed Ava project and enter the upgrade protocol
- abort on conflicting host bootstrap files unless they exactly match the expected managed file or are explicitly resolved
- migrate unversioned Ava projects only through an explicit plan that separates mixed root defaults from project-owned context
- never classify ownership from timestamps, creation order, Git history, or similarity alone

## Keep it thin

The script should orchestrate standard filesystem, archive, state-recording, and verification operations. It must not become a general Ava CLI, role navigator, semantic editor, or persistent runtime. Semantic project-owned changes remain the responsibility of the explicit Upgrade Role.

## Completion criteria

- support a clean install into an eligible empty or compatible existing project
- support explicit adoption or safe refusal for pre-existing Ava-like or conflicting project structures
- support an explicit upgrade to a chosen version
- support latest stable through the documented convenience path
- support a separately verified pinned-version path
- install only paths declared by the release manifest
- prove that managed and project-owned paths are never conflated by source location
- fail safely on path collisions, managed-file conflicts, incomplete assets, checksum errors, authenticity failures, unsupported transitions, unsafe archive paths, and out-of-root filesystem resolution
- prove that no installer, updater, migration, rollback, or cleanup operation can modify a path outside the selected target root
- preserve grouped logical changes and avoid partial application when staging, validation, or final apply fails
- clearly distinguish installed `ava_version` from semantic compatibility
- preserve the active-upgrade state and prevent normal operation until the Upgrade Role completes or the protocol exits through another defined terminal state
- report bootstrap discovery as native, host-bootstrap, explicit-only, or unsupported
- remain readable, auditable, and usable through standard shell tooling
- document required system commands, portability assumptions, and trust assumptions
