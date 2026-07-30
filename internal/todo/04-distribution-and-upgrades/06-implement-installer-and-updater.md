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
  at: 2026-07-30T11:26:00Z
---

# Implement Installer and Updater

## Implement

- one POSIX shell entry point that handles fresh installation and existing-project upgrades
- latest stable and explicit version selection
- target-directory selection with the current directory as the default
- release asset download and checksum verification
- manifest creation and installed-version detection
- managed-file comparison and safe replacement
- deterministic migration execution
- dry-run, conflict reporting, and non-interactive failure behavior
- installation of pending semantic upgrade guidance

## Keep it thin

The script should orchestrate standard filesystem and archive operations. It must not become a general Ava CLI, role navigator, semantic editor, or persistent runtime.

## Completion criteria

- support a clean install into an eligible existing project
- support an explicit upgrade to a chosen version
- support latest stable as the recommended path
- fail safely on conflicts, incomplete assets, checksum errors, and unsupported transitions
- remain readable, auditable, and usable through `curl | sh`
- document required system commands and portability assumptions
