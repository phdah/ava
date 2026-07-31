---
type: Internal Development Task
title: Define Distribution and Ownership Boundary
description: Define Ava as a file distribution and separate Ava-managed base content from project-owned context.
tags: [internal, roadmap, distribution, ownership]
status: pending
phase: 4
order: 1
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T22:59:00+02:00
---

# Define Distribution and Ownership Boundary

## Architecture constraints

- Ava uses exactly two ownership classes: Ava-managed and project-owned.
- The root `AGENTS.md`, manifests, release guidance, and every installed bootstrap file are Ava-managed.
- Project-specific customization must live in project-owned paths referenced by managed instructions.
- There is no third generated-integration-shim ownership class.
- The root `AGENTS.md` remains the canonical bundle entry point. Compatibility bootstrap files may direct host agents to it but must not duplicate or redefine its routing semantics.
- Ownership is determined by the accepted path, manifest, authority, and adoption contract, never by when a file was created.
- Project-owned content may predate Ava installation or be created afterward. Creation time never defines or limits the project-owned class.

## Decide

- the exact installed ownership boundary for Ava as a versioned context distribution
- the installed path layout for base instructions, default roles, default workflows, manifests, and project context
- the stable Ava-managed path for the installed manifest and upgrade state
- which managed files may be customized, or whether managed-file customization is prohibited
- how local modifications to managed files are detected and reported
- how the managed root `AGENTS.md` discovers Ava-managed and project-owned instructions, registries, and extension points
- which supported host agents discover `AGENTS.md` natively and what portable fallback entry point or explicit activation contract applies when they do not
- whether host-specific bootstrap files are distributed, how the installer selects them, and how they remain thin Ava-managed pointers rather than a third ownership class
- how installation and validation report unsupported host bootstrap behavior or missing automatic instruction loading
- whether existing `templates/base/` paths can become the installed layout or require migration
- what makes an existing project eligible for Ava installation or adoption
- how installation handles pre-existing `AGENTS.md`, `index.md`, `log.md`, role registries, workflow registries, instructions, knowledge, and directory layouts
- how explicit adoption decisions classify each accepted pre-existing path as Ava-managed or project-owned without relying on creation time, timestamps, or repository history
- how public documentation defines project-owned content without implying that it must be created after installation
- which path and content collisions must abort automatically and which may be resolved through an explicit adoption or migration decision
- how an existing unversioned or partially Ava-structured project is classified and adopted without silently changing project ownership
- which previous MCP, CLI, provider, and application-service concepts are removed from the public architecture

## Constraints

- project-owned content must never be overwritten merely because a new base release exists
- managed bootstrap files must not mix project-specific content into their ownership boundary
- host compatibility must not require an MCP server, persistent Ava runtime, or feature-rich CLI
- host-specific bootstrap files must not fork, duplicate, or weaken the canonical routing and instruction contracts
- installation into an existing project must not silently claim, replace, relocate, or merge pre-existing project files
- file age, creation order, commit date, and filesystem timestamps must never determine ownership
- the ownership model must remain understandable through normal files and Git diffs
- internal repository instructions must never enter the distributed bundle
- incompatible public path changes require separate user approval

## Completion criteria

- document the two accepted ownership classes and exact path boundaries
- define the stable bootstrap and manifest locations
- define the root `AGENTS.md` as Ava-managed and the supported project-customization path
- define native and fallback bootstrap discovery across supported host agents, including explicit activation and unsupported-host reporting
- define any host-specific bootstrap files as thin Ava-managed integration points without creating another ownership or authority model
- define ownership classification through paths, manifest records, authority, and explicit adoption rather than creation time
- remove creation-time qualifiers from public ownership definitions and explicitly include adopted pre-existing project content in the project-owned class
- define existing-project eligibility, adoption, collision, abort, and explicit-resolution behavior
- demonstrate how pre-existing roles, workflows, instructions, knowledge, registries, and root files retain or receive unambiguous ownership during adoption
- identify any required migration from the current template layout or existing unversioned Ava projects
- align the README, template index, metadata contract, installer task, and upgrade roadmap
- obtain user approval before applying incompatible public path changes
