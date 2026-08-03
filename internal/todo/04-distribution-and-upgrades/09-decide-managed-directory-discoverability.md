---
type: Internal Development Task
title: Decide Managed Directory Discoverability
description: Decide whether Ava-managed context should remain under the hidden `.ava` directory and define any host configuration required for reliable access.
tags: [internal, roadmap, discoverability, hosts, permissions, opencode]
status: pending
phase: 4
order: 9
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T16:35:00+02:00
---

# Decide Managed Directory Discoverability

The first local installation test showed that a host may require explicit confirmation before reading files under `.ava/`, even when the root `AGENTS.md` correctly routes the agent there. Ava instructions cannot themselves grant host filesystem permissions.

Before the first release, Ava must decide whether the managed base remains hidden and how adopting projects make it reliably accessible.

## Evaluate

- keeping the managed base at `.ava/` and documenting required host permission configuration
- keeping `.ava/` while generating or recommending optional host-specific configuration, such as an OpenCode project permission rule
- moving managed content to a visible project directory while preserving the ownership and upgrade boundary
- whether a project-provided host entrypoint is sufficient for discovery but not permission granting
- whether host configuration should be project-owned, Ava-managed, create-if-absent, explicitly installed, or never modified by Ava
- the portability cost of host-specific files such as `opencode.json`
- hidden-file behavior in common agents, editors, search tools, glob implementations, and filesystem permission prompts
- security implications of automatically allowing reads from all managed content while continuing to prevent ordinary edits

## Define the contract

- state whether `.ava/` remains the canonical managed directory
- state what Ava guarantees about discovery and what remains the responsibility of the host or adopting project
- explicitly document that `AGENTS.md` can request reads but cannot change host permission policy
- define whether the installer may offer an explicit host-integration option without silently changing project-owned configuration
- define ownership, upgrade, conflict, and rollback behavior for any generated or recommended host configuration
- avoid claiming native support for a host unless a tested configuration works without repeated approval prompts

## Implement and validate the decision

- update distribution, ownership, installation, and host-integration documentation
- update templates and installer behavior if the managed directory or optional host integration changes
- add an OpenCode fixture covering clean project startup, required managed reads, read permission, and write protection
- add at least one host-neutral fixture proving that managed content remains discoverable through the root router
- verify that a project with an existing global or project host configuration is not silently overwritten
- verify that declining host-specific integration leaves a clear, functional manual path
- include any required pre-release documentation in the generated release assets

## Completion criteria

- the managed-directory strategy is an explicit documented decision, not an accidental consequence of naming
- a fresh installation can load all required managed context without repeated unexplained prompts under every host claimed as supported
- Ava never implies that instruction text can grant filesystem permissions
- host-specific configuration has a clear ownership and mutation policy
- existing project and global host configuration is preserved unless the user explicitly authorizes a compatible change
- read access and write protection for managed content are both tested
- the first release remains blocked until the selected strategy is implemented and validated
