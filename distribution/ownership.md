---
type: Distribution Contract
title: Ava Distribution and Ownership Boundary
description: Defines repository source mapping, installed paths, release ownership, adoption, managed-file conflicts, and native or project-provided host integration.
tags: [ava, distribution, ownership, installation, adoption, host-integration]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Ava Distribution and Ownership Boundary

This document defines the repository, release, installation, and upgrade boundary between Ava-managed distribution content and project-owned context.

It is a release and assembly contract, not the complete instruction loaded by agents during ordinary project work. Installed agent behavior is defined separately by [Ownership and mutation authority](../templates/base/shared/instructions/ownership-and-mutation.md), which release assembly installs under `/.ava/base/shared/instructions/`. Manifest fields, payload checksums, mutable state, and compatibility are defined by [Ava Versioning and Compatibility](versioning.md).

# Repository source model

The Ava repository separates public contracts, release payload sources, project scaffold sources, and internal release procedures:

```text
/
├── README.md
├── index.md
├── log.md
├── distribution/             # public distribution contracts and schemas
├── templates/
│   ├── index.md
│   ├── base/                 # authored managed-base and format-reference material
│   └── project-scaffolds/    # project-owned create-if-absent material
└── internal/
    └── release/              # repository-only publication and installer implementation
```

`distribution/` defines public repository-level contracts. Its files are not automatically installed into projects.

`internal/` is never distributed.

`templates/base/` and `templates/project-scaffolds/` are source material, not directories copied verbatim into a project. Release assembly maps each distributed source file to an explicit installed destination and ownership class. Repository location, source age, and Git history do not determine installed ownership.

Host-specific instruction and configuration files are not Ava template sources. They are supplied and owned by adopting projects or users.

# Installed-project layout

The accepted installed layout is:

```text
/
├── AGENTS.md                         # Ava-managed canonical router
├── .ava/                             # Ava-managed namespace
│   ├── base/
│   │   ├── index.md
│   │   ├── roles/
│   │   ├── workflows/
│   │   └── shared/
│   ├── state/
│   │   ├── manifest.json
│   │   └── upgrade.json
│   └── guidance/
├── index.md                          # project-owned when present
├── roles/                            # project-owned role extensions
├── workflows/                        # project-owned workflow extensions
├── shared/                           # project-owned shared context
├── knowledge/                        # project-owned trusted knowledge
├── inbox/                            # project-owned source intake
└── CODEX.md                          # optional project-owned host entrypoint example
```

The final host entrypoint name and location are chosen by the project owner. Other examples include `CLAUDE.md` and `/.github/copilot-instructions.md`.

Project-owned paths may exist before installation, be created by create-if-absent scaffolding, or be added later. Creation time never changes their ownership.

# Release ownership classes

Ava has exactly two ownership classes.

## Ava-managed

Ava-managed content is installed from a specific Ava release and recorded in `/.ava/state/manifest.json`.

It includes:

- `/AGENTS.md`
- all files under `/.ava/base/`
- `/.ava/state/manifest.json`
- `/.ava/state/upgrade.json`
- all files under `/.ava/guidance/`
- deterministic migration support installed by the release

Ava-managed files must not contain project-specific customization. A local edit does not convert a managed file into project-owned content.

## Project-owned

Project-owned content includes project-specific roles, workflows, instructions, knowledge, source material, indexes, logs, host-specific instruction files, host-specific project configuration, and other project context outside declared managed paths.

The standard extension roots are:

- `/roles/`
- `/workflows/`
- `/shared/`
- `/knowledge/`
- `/inbox/`
- `/index.md` and `/log.md` when present

Project-owned host entrypoints may exist elsewhere outside `/AGENTS.md` and `/.ava/`. Their exact paths may be recorded as host integration metadata, but that metadata does not transfer ownership to Ava.

Pre-existing content accepted during installation remains project-owned unless an explicit adoption decision assigns an exact path to the managed release set. The installer must never infer ownership from timestamps, creation order, filenames alone, or similarity to an Ava default.

# Manifest authority

`/.ava/state/manifest.json` is the installed ownership record for Ava-managed files. It records at least the installed Ava version, release identity, installed managed paths, managed-file roles, and whether each path is immutable payload or mutable managed state. Payload entries record expected checksums. State entries are validated through their schema and allowed transitions and do not contain self-checksums.

A path is Ava-managed only when all of these agree:

1. the path is allowed by this contract
2. the installed manifest declares it in `managed_files`
3. the file was installed or explicitly adopted under an approved release transaction
4. the owning authority remains Ava rather than the project

The manifest must never claim project-owned extension roots or arbitrary pre-existing files as managed.

The manifest may separately record bounded host integration metadata:

```json
{
  "entrypoint": "./CODEX.md",
  "ownership": "project-owned",
  "discovery": "project-provided"
}
```

This record is descriptive. The entrypoint does not appear in `managed_files`, has no Ava checksum, and is never mutated by deterministic Ava tooling. Native host discovery requires no host integration record.

# Managed-file conflicts

Before replacing, deleting, or moving an immutable managed payload, the updater compares its current checksum with the checksum recorded for the installed version.

Before changing mutable managed state, the updater validates its schema, internal consistency, and allowed transition from the previously completed state.

- An unchanged managed payload may be replaced by the target release.
- A modified, missing, or corrupt managed payload is a conflict.
- Missing, malformed, inconsistent, or unauthorized managed state is a conflict.
- Conflicts abort the affected upgrade transaction before project files are changed.
- The updater reports the path, expected payload checksum or state invariant, actual state, intended operation, and available recovery choices.
- The updater never silently overwrites, merges, or reclassifies the file.

Restoring the installed version, explicitly discarding the local modification, or moving project-specific content into a project-owned extension path are separate user-approved recovery actions.

# Router and extension discovery

`/AGENTS.md` is the canonical managed entry point. It must remain stable, project-independent, and replaceable by upgrades.

The router discovers:

- managed routing and ownership contracts under `/.ava/base/shared/`
- managed default roles under `/.ava/base/roles/`
- managed default workflows under `/.ava/base/workflows/`
- project-owned roles through `/roles/index.md` when present
- project-owned workflows through `/workflows/index.md` when present
- project-owned shared instructions and context through explicit links under `/shared/`
- project-owned knowledge and inbox content only when required by the selected role, workflow, or task

Managed and project-owned registries are separate extension points. A project must not edit managed registries to add project-specific entries.

Canonical paths remain the identity for roles and workflows. An explicit name that resolves to more than one registered workflow or role must be reported as ambiguous rather than resolved by ownership precedence.

# Host integration and discovery

Ava supports three relevant discovery outcomes.

## Native `AGENTS.md` discovery

A host is natively supported when its documented and validated behavior loads the project-root `AGENTS.md` automatically with compatible instruction semantics.

Ava must not claim native support for a named host until that behavior has a maintained conformance fixture or documented verification.

OpenCode is Ava's first natively supported host. It loads root `AGENTS.md` and treats direct `./.ava/...` reads as project-local workspace access. OpenCode support does not require or authorize Ava to create or modify `opencode.json`, `opencode.jsonc`, global configuration, or `.opencode/` content. The complete contract is [OpenCode host support](opencode.md).

## Project-provided host entrypoint

A project may contain an instruction file recognized by its chosen host. The project owner may identify that existing file to the installer with `--host-entrypoint PATH`.

The installer must:

- validate that the path resolves to an existing regular file inside the selected project root
- reject `./AGENTS.md`, `./.ava/`, and paths below `./.ava/`
- preserve the file byte-for-byte
- record only its normalized project-owned integration metadata
- preserve that metadata across upgrades unless explicitly changed

The installer must not:

- create the host file
- inspect or validate its prose
- add it to release assets or `managed_files`
- replace, delete, back up, restore, migrate, or roll it back

The project owner is responsible for instructing the host file to load and follow `./AGENTS.md`. The host file may contain additional project-specific instructions.

## Explicit activation

When automatic discovery is unavailable or unverified, Ava remains usable through an explicit activation instruction:

```text
Read ./AGENTS.md and follow it as the root instructions for this project.
```

Validation classifies supported discovery as `native`, `project-provided`, `explicit-only`, or `unsupported`. The installer records only project-provided integration metadata. Native OpenCode installations normally retain `host_integration: null` because discovery does not depend on a project-owned entrypoint.

Instruction text cannot grant host filesystem permissions. A host or project configuration remains responsible for allowing, asking for, or denying file operations.

# Fresh installation

A project is eligible for fresh installation when:

- the target root resolves safely and is writable
- planned managed paths do not collide with unclassified content
- `/.ava/` is absent
- `/AGENTS.md` is absent, or an explicit adoption plan has been approved
- every create-if-absent project scaffold can be created or skipped without modifying existing content
- any supplied host entrypoint already exists as a normal project-owned file outside managed paths

The installer creates managed content and may create minimal project-owned scaffolding only when the target path is absent. Scaffold files are project-owned immediately and are never added to the managed manifest.

Existing `/index.md`, `/log.md`, `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, `/inbox/`, host-specific instruction files, and host-specific project configuration remain untouched and project-owned.

# Adoption of existing projects

Installation into a non-empty project is an adoption transaction, not a merge heuristic.

The installer first produces a dry-run classification of every relevant path:

- proposed Ava-managed path
- existing project-owned path
- recognized prior Ava-managed path
- optional project-provided host entrypoint
- unresolved collision
- explicit adoption or migration decision required

No existing path is claimed, replaced, moved, or merged without a decision that names the exact path and resulting ownership.

## Collision behavior

| Existing path or state | Default behavior | Explicit resolution |
|---|---|---|
| `/AGENTS.md` | Abort | Preserve its project-specific meaning in a project-owned path, then explicitly authorize installation of the managed router |
| `/.ava/` without a supported manifest | Abort | Run an approved unversioned-adoption or recovery procedure |
| `/.ava/` with a supported manifest | Treat as installed Ava | Continue only through the defined upgrade protocol |
| Requested host entrypoint does not exist or is unsafe | Abort | Supply an existing normal project-owned file inside the target root |
| `/index.md` or `/log.md` | Preserve as project-owned | No ownership transfer required |
| `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, or `/inbox/` | Preserve as project-owned and skip colliding scaffolds | Resolve only structural incompatibilities explicitly |
| Locally modified managed file | Abort upgrade | Restore, discard, or migrate customization explicitly |

# Adoption of unversioned Ava projects

The current unversioned template layout is not the final installed layout. Existing projects may contain a root `AGENTS.md` plus default and project-specific content mixed under `/roles/`, `/workflows/`, and `/shared/`.

Adopting such a project requires an explicit migration that:

1. inventories existing files without assuming which are defaults
2. identifies project-specific behavior and preserves it in project-owned paths
3. installs the selected release's defaults under `/.ava/base/`
4. replaces the root router only after project-specific router content has been preserved or deliberately discarded
5. creates the managed manifest and records every adopted managed path
6. records any selected host entrypoint as project-owned metadata only
7. reports unresolved files whose ownership or semantic intent cannot be determined safely

Similarity to a historical template may be evidence for a suggested classification, but it is never sufficient for silent ownership transfer.

# Source-to-installed mapping

The release assembler and installer implement an explicit mapping rather than copying `templates/base/` as a project root.

| Repository source | Installed destination | Ownership |
|---|---|---|
| `templates/base/AGENTS.md` | `/AGENTS.md` | Ava-managed |
| managed base index and contracts | `/.ava/base/` | Ava-managed |
| default roles | `/.ava/base/roles/` | Ava-managed |
| default workflows | `/.ava/base/workflows/` | Ava-managed |
| managed shared instructions | `/.ava/base/shared/` | Ava-managed |
| release-generated manifest and state | `/.ava/state/` | Ava-managed |
| release upgrade guidance | `/.ava/guidance/` | Ava-managed |
| `templates/project-scaffolds/` | project root extension paths | Project-owned, create-if-absent only |
| project-supplied host entrypoint | unchanged project path | Project-owned metadata reference only |

Release assembly must provide a complete, mechanically verifiable manifest for distributed mappings. No release may treat repository source location alone as ownership metadata, and no release may package a project-specific host entrypoint or host configuration file.

# Removed architecture concepts

This boundary does not require or reserve responsibility for:

- an MCP server
- a persistent Ava runtime
- a feature-rich CLI
- a workspace-provider abstraction
- repository or storage provider layers
- application-service ownership of project context

The installer performs deterministic filesystem and release operations. Installed shared instructions govern how active Ava roles work directly with project-owned context. Release tooling applies only deterministic managed changes and must not perform semantic project maintenance as an incidental side effect.
