---
type: Internal Development Task
title: Implement OpenCode Support and Decide Managed Directory Discoverability
description: Make OpenCode Ava's first explicitly supported host and settle how Ava-managed context is exposed and permitted under the selected managed-directory strategy.
tags: [internal, roadmap, discoverability, hosts, permissions, opencode]
status: completed
phase: 4
order: 9
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
---

# Implement OpenCode Support and Decide Managed Directory Discoverability

The first local installation test showed that a host may require explicit confirmation before reading files under `.ava/`, even when the root `AGENTS.md` correctly routes the agent there. Ava instructions cannot themselves grant host filesystem permissions.

OpenCode is now Ava's first explicitly supported host.

## Decision

- Keep `./.ava/` as the canonical Ava-managed directory.
- Use OpenCode's native project-root `AGENTS.md` discovery.
- Load mandatory managed context through explicit direct `./.ava/...` paths rather than hidden-file scanning.
- Treat `./.ava/` as project-local workspace content, not an external directory.
- Require no OpenCode project configuration for default discovery or reads.
- Never create or modify project `opencode.json`, project `opencode.jsonc`, global OpenCode configuration, or `.opencode/` content.
- Offer no installer-managed OpenCode integration option because native discovery is sufficient.
- Keep optional host-level managed write protection project-owned.
- Keep deterministic managed writes inside the installer and updater transaction.

The authoritative public contract is [OpenCode host support](../../../distribution/opencode.md).

## Implementation

- added the public OpenCode discovery, permission, ownership, installation, and troubleshooting contract
- documented maintainer release validation and the pinned compatibility policy
- added installation and upgrade fixtures that preserve absent, project, and global OpenCode configuration
- added installed-router resolution and host-neutral portability fixtures
- added a live OpenCode startup fixture using an isolated home and the installed project root
- added a dedicated CI job for the pinned supported OpenCode version

## Validation boundary

The deterministic conformance boundary covers native router discovery, project-local managed paths, default workspace-read behavior, configuration preservation, and real OpenCode startup against an installed fixture.

A model-backed end-to-end response depends on the user's selected provider and model. Ava does not treat provider credentials or model behavior as part of the file-distribution compatibility contract.

## Completion criteria

- [x] OpenCode is Ava's first explicitly documented supported host.
- [x] root `AGENTS.md` discovery is classified as native.
- [x] `./.ava/` remains the explicit canonical managed directory.
- [x] mandatory managed reads use direct project-local paths and do not depend on hidden scanning.
- [x] Ava does not imply that instruction text grants filesystem permissions.
- [x] OpenCode-specific configuration has a project-owned and user-owned mutation policy.
- [x] existing project and global OpenCode configuration is preserved.
- [x] fresh installation and upgrade fixtures cover the selected strategy.
- [x] a host-neutral fixture proves router portability.
- [x] the pinned OpenCode CLI starts from an installed fixture in CI.
