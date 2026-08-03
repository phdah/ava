---
type: Internal Development Task
title: Implement OpenCode Support and Decide Managed Directory Discoverability
description: Keep Ava-managed context hidden while installing a minimal project-owned OpenCode permission configuration by default.
tags: [internal, roadmap, discoverability, hosts, permissions, opencode]
status: completed
phase: 4
order: 9
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
---

# Implement OpenCode Support and Decide Managed Directory Discoverability

The first local installation test showed that a host may require explicit permission before reading files under `.ava/`, even when the root `AGENTS.md` correctly routes the agent there. Ava instructions cannot themselves grant host filesystem permissions.

## Decision

- `./.ava/` remains Ava's canonical hidden managed directory.
- A normal installation creates a minimal project-owned `./opencode.json` when neither `opencode.json` nor `opencode.jsonc` already exists.
- The generated configuration allows reads under `.ava/**` without repeated confirmation and keeps edits under `.ava/**` guarded with `ask`.
- `--host none` skips host configuration.
- The host selector is intentionally extensible so future host-specific configuration can be added without changing Ava's host-neutral context layout.
- Existing project OpenCode configuration is never overwritten or merged automatically. Installation continues and prints the exact configuration block that can be merged manually.
- The generated OpenCode configuration is project-owned, is not included in Ava's managed-file manifest, and is never replaced during upgrade.
- Broader runtime and model-backed host conformance remains part of task 10 rather than this bounded installer integration task.

## Implementation

Implemented in #30:

- added a default `--host opencode` selection and a `--host none` override
- added create-if-absent installation of the minimal OpenCode permission configuration
- preserved existing `opencode.json` and `opencode.jsonc` files while emitting manual merge guidance
- kept the root router, `.ava/` layout, manifest schema, and host-neutral context format unchanged
- added focused installer fixtures for host configuration behavior

## Validation

The focused suite verifies:

- default installation creates the expected project-owned `opencode.json`
- `--host none` creates no OpenCode configuration
- an existing OpenCode configuration is preserved and Ava installation still completes
- the manual merge guidance includes the required `.ava/**` read permission
- an upgrade never replaces a project-owned OpenCode configuration

## Completion criteria

- [x] `.ava/` remains the hidden canonical managed directory
- [x] the default installer path provides OpenCode read access to `.ava/**`
- [x] managed edits remain guarded by OpenCode permission configuration
- [x] users can explicitly select no host configuration
- [x] existing project OpenCode configuration is preserved without blocking installation
- [x] manual merge guidance is emitted when automatic creation is not possible
- [x] generated host configuration is project-owned and excluded from deterministic Ava upgrades
- [x] focused fresh-install and upgrade behavior is covered by maintained tests
