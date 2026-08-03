---
type: Shared Instruction
title: Ownership and Mutation Authority
description: Defines how active Ava roles distinguish release ownership from authority to modify project context.
tags: [ava, instructions, ownership, mutation, authority, upgrades]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T11:56:00+02:00
---

# Purpose

This instruction defines how an active Ava role or workflow interprets file ownership while working in an installed project.

Ownership controls release lifecycle, manifest membership, canonical baselines, and automatic replacement. Mutation authority controls whether the active role may change a file for the current task. These are separate concepts.

All paths beginning with `./` are resolved from the project root.

# Installed ownership classes

Ava has exactly two ownership classes.

## Ava-managed

Ava-managed content belongs to the installed Ava release. It includes:

- `./AGENTS.md`
- all files under `./.ava/base/`
- `./.ava/state/manifest.json`
- `./.ava/state/upgrade.json`
- all files under `./.ava/guidance/`
- deterministic migration support installed by the release

Ava-managed files provide the canonical router, default roles, default workflows, shared contracts, state, and release guidance. Ordinary semantic roles must not customize them.

Managed files change only through deterministic release tooling or another narrowly defined managed mechanism. A role may update a managed state field only when an active protocol explicitly grants that authority, such as the bounded semantic-migration state transitions assigned to the Upgrade Role.

## Project-owned

Project-owned content contains project-specific context outside declared managed paths. Standard project-owned locations include:

- `./index.md` and `./log.md` when present
- `./roles/`
- `./workflows/`
- `./shared/`
- `./knowledge/`
- `./inbox/`
- host-specific instruction files such as `./CODEX.md`, `./CLAUDE.md`, or `./.github/copilot-instructions.md`

A host-specific instruction file remains project-owned even when its path is recorded in `host_integration` metadata. It is not part of the managed-file inventory and deterministic Ava tooling must not create, replace, checksum, back up, restore, migrate, or roll it back.

Project-owned content may predate Ava installation, be created as create-if-absent scaffolding, or be added later. Creation time does not change ownership.

`Project-owned` does not mean human-only, externally maintained, or read-only to Ava. Active Ava roles and workflows are expected to maintain project-owned context when the current task and their resolved authority require it.

# Mutation authority

An active role or explicitly invoked workflow may create, update, reorganize, move, or remove project-owned files when all of the following permit the change:

1. the active role and workflow scope
2. the role's capabilities and constraints
3. the current user-approved task
4. applicable project instructions
5. conflict, provenance, validation, and unresolved-decision rules

This applies generally to normal project stewardship, role and workflow maintenance, inbox ingestion, knowledge organization, review follow-up, and bounded semantic upgrade work. It is not limited to a particular role.

A mutation does not change ownership. A project-owned file remains project-owned after an Ava role edits it. An Ava-managed file remains Ava-managed after a permitted managed operation or state transition.

# Required behavior before mutation

Before changing a project file:

1. classify the target as Ava-managed or project-owned
2. resolve the active role's authority for the intended operation
3. refuse ordinary semantic customization of Ava-managed files
4. apply project-owned changes only within the current task scope
5. preserve required metadata, provenance, indexes, links, and scoped history
6. stop and ask the user when ownership, destination, authority, or intended semantics remain materially ambiguous

Do not infer permission from the file being writable or from its location alone when the manifest or active instructions indicate otherwise.

# Managed-file conflicts

A local edit, deletion, or corruption does not convert an Ava-managed file into project-owned content.

When an active task discovers an unexpected managed-file change:

- do not silently normalize, overwrite, merge, or reclassify it
- preserve evidence of the current state
- report the path and the conflict
- follow the applicable recovery or upgrade protocol
- require an explicit decision before discarding project-specific meaning found in a managed path

The updater remains responsible for checksum comparison and deterministic replacement behavior.

# Release boundary

Installers, updaters, and deterministic migrations may replace or transform managed content according to the release protocol. They must not rewrite project-owned semantics as an incidental consequence of replacing the Ava base.

Semantic changes to project-owned context happen through an active Ava role under an explicit user request. During an Ava upgrade, the Upgrade Role may cross ordinary project-maintenance boundaries only for the bounded source-to-target migration defined by installed release guidance.

# Registries and extensions

Managed and project-owned registries are separate extension points.

- managed default roles and workflows live under `./.ava/base/`
- project-specific roles and workflows live under `./roles/` and `./workflows/`
- adding a project concept must not require editing a managed registry
- ownership does not provide name precedence when a role or workflow identifier is ambiguous

Report ambiguous resolution rather than choosing a concept because it is managed or project-owned.

# Completion checks

After changing project-owned context, verify that:

- every changed path remained in its correct ownership class
- the active role had authority for every mutation
- no managed file was customized outside a defined managed mechanism
- required metadata, provenance, indexes, links, and logs remain valid
- unresolved ownership or semantic decisions are reported rather than hidden
