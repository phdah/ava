---
type: Internal Development Task
title: Define Release Guidance and Upgrade Role
description: Define structured release information and an explicit Upgrade Role for one-prompt semantic reconciliation of all affected project-owned Ava context.
tags: [internal, roadmap, releases, logs, migration, agents, roles]
status: pending
phase: 4
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T22:27:00+02:00
---

# Define Release Guidance and Upgrade Role

## Goal

A user should be able to issue one explicit request that activates a dedicated Upgrade Role and reconciles every affected project-owned Ava file after a deterministic base upgrade. The role must remain reachable through an entirely Ava-managed path even when project-owned routing is incompatible with the installed base.

## Define the release guidance

- how scoped `log.md` entries contribute to release change information
- which upgrade-relevant facts must be recorded more explicitly than ordinary conceptual history
- the release manifest or `UPGRADE.md` structure for source version, target version, changed contracts, affected project concepts, required decisions, and completion criteria
- how guidance references deterministic migration IDs and changed managed paths
- how an agent discovers all applicable guidance across a multi-version upgrade
- how the Upgrade Role reads installed `ava_version` and separate semantic-compatibility state
- how the Upgrade Role records complete, partial, blocked, or pending semantic migration without hiding unresolved decisions
- the canonical one-prompt upgrade procedure and expected report
- the Ava-managed locations and indexes through which upgrade guidance is discovered without first reading project-owned registries

## Define the Upgrade Role

- create an explicit Upgrade Role whose sole purpose is to perform semantic project-context migration for an active Ava upgrade
- make the Upgrade Role, its `index.md`, required instructions, constraints, guidance entry point, and activation contract Ava-managed
- define a pre-routing activation path from the Ava-managed root `AGENTS.md` and manifest state directly to the Upgrade Role
- ensure Upgrade Role discovery and activation do not depend on project-owned role registries, workflow registries, shared instructions, or routing indexes
- define its activation, authority, required reading, capabilities, constraints, completion checks, and deactivation
- permit it to cross the normal maintenance boundaries between roles, workflows, shared instructions, and project knowledge only for the bounded source-to-target upgrade
- make it the sole agent role permitted to update the Ava-managed manifest and semantic migration state
- prevent it from performing unrelated project maintenance or silently inventing project-specific semantics
- require it to stop and report unresolved decisions whenever release guidance and existing project intent are insufficient
- define how it returns the project to normal routing only after migration completion or another protocol-defined terminal state

## Required semantic migration scope

The Upgrade Role must inspect and update every affected project-owned Ava file and relationship, not only high-level role or workflow documents. Its scope includes:

- project-specific roles and role registries
- project-specific workflows and workflow registries
- shared project instructions and constraints
- project knowledge and context documents
- all affected `index.md` and `log.md` files
- metadata, frontmatter, links, references, and catalog entries
- project-owned bootstrap extensions and routing references
- directory layouts, filenames, and structural conventions when the target release changes how project context is organized
- semantic compatibility state and unresolved-decision records in the Ava-managed manifest

A migration is not complete while any required project-owned index, log, registry, metadata field, reference, or structural change remains inconsistent with the target release.

## Required distinction

Scoped logs remain human-readable conceptual history. They may be an input to release guidance, but the Upgrade Role must not infer migration obligations from arbitrary log prose alone. Release-specific guidance must state compatibility impact and required action directly.

The one-prompt semantic migration must not change the meaning of `ava_version`, which identifies the installed base. Any manifest update must follow the field ownership and state transitions defined by the versioning and upgrade protocol tasks.

Project-owned registries and routing files are migration inputs, not authorities for locating or activating the Upgrade Role. They must not be read until the managed router has established upgrade mode and the role's bounded authority.

## Completion criteria

- define a structured, agent-readable release guidance contract
- define any required structure or metadata additions for upgrade-relevant `log.md` entries
- add the Upgrade Role to the public role catalog while preserving an independent Ava-managed activation path for incomplete upgrades
- define the one-prompt semantic migration procedure
- define the pre-routing manifest check and direct managed activation path from root `AGENTS.md` to the Upgrade Role
- prove that the Upgrade Role, guidance, and permitted-operation instructions remain reachable without any project-owned registry or routing dependency
- define exhaustive discovery and migration of affected project-owned files, registries, indexes, logs, metadata, links, and structural conventions
- define completion, partial completion, conflict, and user-decision states
- ensure reports show installed base version and semantic compatibility separately
- ensure the role cannot resume normal routing while the upgrade remains incomplete
- align the guidance and role with manifests, instruction resolution, workflows, validation, and release assets