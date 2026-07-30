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
  at: 2026-07-30T22:59:00+02:00
---

# Define Release Guidance and Upgrade Role

## Goal

A user should be able to issue one explicit request that activates a dedicated Upgrade Role and reconciles every affected project-owned Ava file after a deterministic base upgrade.

The one-prompt requirement applies only to project-owned changes required by an active Ava version upgrade. Ordinary project maintenance remains governed by the normal role and workflow authority model and must not require Upgrade Role activation or release-specific guidance.

The managed upgrade path must remain reachable even when the newly installed base is not yet compatible with project-owned routing, roles, workflows, or registries.

## Define the release guidance

- how scoped `log.md` entries contribute to release change information
- which upgrade-relevant facts must be recorded more explicitly than ordinary conceptual history
- the release manifest or `UPGRADE.md` structure for source version, target version, changed contracts, affected project concepts, required decisions, and completion criteria
- how guidance references deterministic migration IDs and changed managed paths
- how an agent discovers all applicable guidance across a multi-version upgrade
- how the Upgrade Role reads installed `ava_version` and separate semantic-compatibility state
- how the Upgrade Role records complete, partial, blocked, or pending semantic migration without hiding unresolved decisions
- the canonical one-prompt upgrade procedure and expected report
- an Ava-managed guidance location that can be discovered before reading any project-owned registry or routing file

## Define the Upgrade Role

- create an explicit Upgrade Role whose sole purpose is to perform semantic project-context migration for an active Ava upgrade
- make the Upgrade Role definition, index, required instructions, constraints, release guidance entry point, and activation contract entirely Ava-managed
- define its activation, authority, required reading, capabilities, constraints, completion checks, and deactivation
- define direct activation from the Ava-managed router after the pre-routing manifest check, without resolving through project-owned role or workflow registries
- permit it to cross the normal maintenance boundaries between roles, workflows, shared instructions, and project knowledge only for the bounded source-to-target upgrade
- make it the sole agent role permitted to update the Ava-managed manifest and semantic migration state
- prevent it from performing unrelated project maintenance or silently inventing project-specific semantics
- require it to stop and report unresolved decisions whenever release guidance and existing project intent are insufficient
- define how it returns the project to normal routing only after migration completion or another protocol-defined terminal state

## Managed activation boundary

- the root Ava-managed `AGENTS.md` checks upgrade state before ordinary workflow or role resolution
- active or incomplete upgrade state selects the Ava-managed Upgrade Role directly
- activation and required reading do not depend on project-owned indexes, role registries, workflow registries, or routing instructions
- project-owned registries become migration inputs only after the Upgrade Role and bounded authority are active
- missing, incompatible, or corrupt project-owned routing cannot make upgrade inspection, resume, abort, rollback, or semantic reconciliation unreachable

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

Upgrade-specific authority must not replace or narrow the ordinary authority of roles such as Project Steward, Role Manager, Inbox Ingester, or Change Reviewer when no upgrade is active.

## Completion criteria

- define a structured, agent-readable release guidance contract
- define any required structure or metadata additions for upgrade-relevant `log.md` entries
- add the Upgrade Role to the public role catalog and define its complete bounded authority
- define the Upgrade Role and all bootstrap guidance needed to activate it as Ava-managed content
- define direct managed activation before any project-owned routing or registry lookup
- demonstrate that the Upgrade Role remains reachable with incompatible, missing, or corrupt project-owned routing structures
- define the one-prompt semantic migration procedure
- define exhaustive discovery and migration of affected project-owned files, registries, indexes, logs, metadata, links, and structural conventions
- define completion, partial completion, conflict, and user-decision states
- ensure reports show installed base version and semantic compatibility separately
- ensure the role cannot resume normal routing while the upgrade remains incomplete
- ensure public roadmap and architecture wording restricts the one-prompt requirement to upgrade-required project-owned changes without limiting ordinary project maintenance
- align the guidance and role with manifests, instruction resolution, workflows, validation, and release assets
