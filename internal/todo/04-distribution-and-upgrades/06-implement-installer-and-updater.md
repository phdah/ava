---
type: Internal Development Task
title: Implement Installer and Updater
description: Implement the thin POSIX shell entry point for fresh installation and explicit versioned upgrades.
tags: [internal, roadmap, shell, installer, updater]
status: proposed
phase: 4
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Implement Installer and Updater

This task becomes active only after explicit user approval of the distribution-first architecture and completion of the preceding design tasks.

## Implement

- one POSIX shell entry point that handles fresh installation and existing-project upgrades
- latest stable and explicit version selection
- target-directory selection with the current directory as the default
- convenience and verified bootstrap flows defined by the release contract
- release asset download, integrity checks, and authenticity verification where requested
- manifest creation and installed `ava_version` detection
- managed-file comparison and safe replacement
- deterministic migration execution
- dry-run, conflict reporting, and non-interactive failure behavior
- installation of pending semantic upgrade guidance and separate semantic-compatibility state

## Keep it thin

The script should orchestrate standard filesystem, archive, and verification operations. It must not become a general Ava CLI, role navigator, semantic editor, or persistent runtime.

## Completion criteria

- support a clean install into an eligible existing project
- support an explicit upgrade to a chosen version
- support latest stable through the documented convenience path
- support a separately verified pinned-version path
- fail safely on conflicts, incomplete assets, checksum errors, authenticity failures, and unsupported transitions
- clearly distinguish installed `ava_version` from semantic compatibility
- remain readable, auditable, and usable through standard shell tooling
- document required system commands, portability assumptions, and trust assumptions