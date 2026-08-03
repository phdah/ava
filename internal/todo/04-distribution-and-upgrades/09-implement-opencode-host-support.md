---
type: Internal Development Task
title: Implement OpenCode Support and Decide Managed Directory Discoverability
description: Make OpenCode Ava's first explicitly supported host and settle how Ava-managed context is exposed and permitted under the selected managed-directory strategy.
tags: [internal, roadmap, discoverability, hosts, permissions, opencode]
status: pending
phase: 4
order: 9
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
---

# Implement OpenCode Support and Decide Managed Directory Discoverability

The first local installation test showed that a host may require explicit confirmation before reading files under `.ava/`, even when the root `AGENTS.md` correctly routes the agent there. Ava instructions cannot themselves grant host filesystem permissions.

OpenCode is the first host Ava must explicitly support. This task must produce a tested configuration and a clear managed-directory decision rather than only documenting generic host uncertainty.

## Evaluate

- keeping the managed base at `.ava/` and documenting the required OpenCode permission configuration
- keeping `.ava/` while offering an explicit OpenCode integration option that does not silently mutate project-owned configuration
- moving managed content to a visible project directory while preserving the ownership and upgrade boundary
- whether OpenCode discovers root `AGENTS.md` natively or requires a project-owned host entrypoint
- whether a project-provided host entrypoint is sufficient for discovery but not permission granting
- whether OpenCode configuration should be project-owned, Ava-managed, create-if-absent, explicitly installed, or only documented
- the portability and ownership cost of `opencode.json` or another OpenCode-specific project file
- hidden-file behavior in OpenCode file reads, search, globbing, and permission prompts
- security implications of allowing managed reads while continuing to guard managed writes

## Define the host contract

- state whether `.ava/` remains the canonical managed directory
- define exactly how a clean OpenCode project discovers and loads root `AGENTS.md`
- define the OpenCode configuration required to read every managed required-reading path without repeated unexplained prompts
- state what Ava guarantees and what remains the responsibility of OpenCode or the adopting project
- explicitly document that instruction text cannot grant host filesystem permissions
- define whether the installer may offer an explicit OpenCode integration option without silently changing project-owned configuration
- define ownership, upgrade, conflict, and rollback behavior for any generated or recommended OpenCode configuration
- classify OpenCode discovery accurately as native or project-provided based on the tested result

## Implement

- update distribution, ownership, installation, and host-integration documentation
- update templates and installer behavior when required by the selected managed-directory or explicit OpenCode integration strategy
- provide the minimal documented OpenCode setup needed for a user to begin working with Ava after installation
- preserve existing global and project OpenCode configuration unless the user explicitly authorizes a compatible change
- ensure declining installer-managed integration leaves a clear manual configuration path
- include required OpenCode setup and limitations in generated prerelease documentation

## Validate

Add maintained OpenCode fixtures covering:

- clean project startup after Ava installation
- discovery and loading of root `AGENTS.md`
- direct resolution of every managed required-reading path
- reading hidden managed content without repeated unexplained prompts
- ordinary protection against accidental managed-file editing
- intentional deterministic installer or updater writes
- project-owned roles, workflows, shared instructions, and knowledge
- an existing global OpenCode configuration
- an existing project `opencode.json` or equivalent configuration
- explicit acceptance and rejection of any offered integration change
- a project-provided host entrypoint when that mode is supported

Add at least one host-neutral fixture proving that root-router discovery remains portable without claiming support for another named host.

## Completion criteria

- OpenCode is Ava's first explicitly documented and tested supported host
- a fresh OpenCode session can load every required managed context file without failed absolute-path attempts or repeated unexplained permission prompts
- the managed-directory strategy is an explicit documented decision
- Ava never implies that instruction text grants filesystem permissions
- OpenCode-specific configuration has a clear ownership and mutation policy
- existing project and global OpenCode configuration is preserved unless the user explicitly authorizes a compatible change
- managed reads, guarded managed writes, and deterministic updater writes are all tested
- the first alpha remains blocked until OpenCode support and the selected managed-directory strategy are implemented and validated
