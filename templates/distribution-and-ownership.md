---
type: Distribution Contract
title: Ava Distribution and Ownership Boundary
description: Defines repository source mapping, installed paths, release ownership, adoption, managed-file conflicts, and bootstrap discovery.
tags: [ava, distribution, ownership, installation, adoption, bootstrap]
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T12:08:00+02:00
---

# Ava Distribution and Ownership Boundary

This document defines the repository, release, installation, and upgrade boundary between Ava-managed distribution content and project-owned context.

It is a release and assembly contract, not the complete instruction loaded by agents during ordinary project work. Installed agent behavior is defined separately by [Ownership and mutation authority](base/shared/instructions/ownership-and-mutation.md), which release assembly installs under `/.ava/base/shared/instructions/`. Manifest fields, payload checksums, mutable state, and compatibility are defined by [Ava Versioning and Compatibility](versioning-and-compatibility.md).

# Repository source model

The Ava repository remains a development repository:

```text
/
├── README.md
├── index.md
├── log.md
├── internal/                 # repository-only development context
└── templates/
    ├── index.md
    ├── distribution-and-ownership.md
    ├── versioning-and-compatibility.md
    ├── schemas/
    └── base/                 # authored managed-base and scaffold source material
```

`internal/` is never distributed.

`templates/base/` is source material, not a directory copied verbatim into a project. Release assembly must map each source file to an explicit installed destination and ownership class. Repository location, source age, and Git history do not determine installed ownership.

Before the first release, release assembly may reorganize `templates/base/` into clearer managed-payload and create-if-absent scaffold sources. Such repository-only reorganization does not itself change the installed path contract.

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
├── shared/                           # project-owned shared instructions and context
├── knowledge/                        # project-owned trusted knowledge
└── inbox/                            # project-owned source intake
```

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
- any selected host-specific bootstrap file
- deterministic migration support installed by the release

Ava-managed files must not contain project-specific customization. A local edit does not convert a managed file into project-owned content.

## Project-owned

Project-owned content includes project-specific roles, workflows, instructions, knowledge, source material, indexes, logs, and other project context outside declared managed paths.

The standard extension roots are:

- `/roles/`
- `/workflows/`
- `/shared/`
- `/knowledge/`
- `/inbox/`
- `/index.md` and `/log.md` when present

Pre-existing content accepted during installation remains project-owned unless an explicit adoption decision assigns an exact path to the managed release set. The installer must never infer ownership from timestamps, creation order, filenames alone, or similarity to an Ava default.

The operational meaning of these classes, including the distinction between ownership and role mutation authority, belongs to the installed [Ownership and mutation authority](base/shared/instructions/ownership-and-mutation.md) contract.

# Manifest authority

`/.ava/state/manifest.json` is the installed ownership record for Ava-managed files. It records at least the installed Ava version, release identity, installed path, managed-file role, and whether the path is immutable payload or mutable managed state. Payload entries record an expected checksum. State entries are validated through their schema and allowed transitions and do not contain self-checksums.

A path is Ava-managed only when all of these agree:

1. the path is allowed by this contract
2. the installed manifest declares it
3. the file was installed or explicitly adopted under an approved release transaction
4. the owning authority remains Ava rather than the project

The manifest must never claim project-owned extension roots or arbitrary pre-existing files.

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

Managed and project-owned registries are separate extension points. A project must not edit the managed registries to add project-specific entries.

Canonical paths remain the identity for roles and workflows. An explicit name that resolves to more than one registered workflow or role must be reported as ambiguous rather than resolved by ownership precedence.

# Bootstrap discovery

Ava supports three discovery outcomes.

## Native `AGENTS.md` discovery

A host is natively supported when its documented and validated behavior loads the project-root `AGENTS.md` automatically with compatible instruction semantics.

Ava must not claim native support for a named host until that behavior has a maintained conformance fixture or documented verification.

## Host-specific bootstrap

A release may provide an optional host-specific bootstrap file when a host uses another recognized instruction filename.

Such a file:

- is selected explicitly by installer option or validated host detection
- is Ava-managed and recorded in the manifest
- contains only a thin instruction to load and follow `/AGENTS.md`
- must not duplicate routing, role, workflow, ownership, or upgrade semantics
- must not contain project-specific customization

A host-specific file does not create a third ownership class or a second canonical router.

## Explicit activation

When automatic discovery is unavailable or unverified, Ava remains usable through an explicit activation instruction:

```text
Read ./AGENTS.md and follow it as the root instructions for this project.
```

Installation and validation must report whether discovery is native, provided through a selected bootstrap, explicit-only, or unsupported because the host cannot reliably load repository instructions.

# Fresh installation

A project is eligible for fresh installation when:

- the target root resolves safely and is writable
- planned managed paths do not collide with unclassified content
- `/.ava/` is absent
- `/AGENTS.md` is absent, or an explicit adoption plan has been approved
- every create-if-absent project scaffold can be created or skipped without modifying existing content

The installer creates managed content and may create minimal project-owned scaffolding only when the target path is absent. Scaffold files are project-owned immediately and are never added to the managed manifest.

Existing `/index.md`, `/log.md`, `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, and `/inbox/` content remains untouched and project-owned.

# Adoption of existing projects

Installation into a non-empty project is an adoption transaction, not a merge heuristic.

The installer first produces a dry-run classification of every relevant path:

- proposed Ava-managed path
- existing project-owned path
- recognized prior Ava-managed path
- unresolved collision
- explicit adoption or migration decision required

No existing path is claimed, replaced, moved, or merged without a decision that names the exact path and resulting ownership.

## Collision behavior

| Existing path or state | Default behavior | Explicit resolution |
|---|---|---|
| `/AGENTS.md` | Abort | Preserve its project-specific meaning in a project-owned path, then explicitly authorize installation of the managed router |
| `/.ava/` without a supported manifest | Abort | Run an approved unversioned-adoption or recovery procedure |
| `/.ava/` with a supported manifest | Treat as installed Ava | Continue only through the defined upgrade protocol |
| Selected host bootstrap path | Abort unless it exactly matches the expected managed file | Explicitly preserve or replace it |
| `/index.md` or `/log.md` | Preserve as project-owned | No ownership transfer required |
| `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, or `/inbox/` | Preserve as project-owned and skip colliding scaffolds | Resolve only structural incompatibilities explicitly |
| Locally modified managed file | Abort upgrade | Restore, discard, or migrate customization explicitly |

# Adoption of unversioned Ava projects

The current unversioned template layout is not the final installed layout. Existing projects may contain a root `AGENTS.md` plus default and project-specific content mixed under `/roles/`, `/workflows/`, and `/shared/`.

Adopting such a project requires an explicit migration that:

1. inventories the existing files without assuming which are defaults
2. identifies project-specific behavior and preserves it in project-owned paths
3. installs the selected release's defaults under `/.ava/base/`
4. replaces the root router only after project-specific router content has been preserved or deliberately discarded
5. creates the managed manifest and records every adopted managed path
6. reports unresolved files whose ownership or semantic intent cannot be determined safely

Similarity to a historical template may be evidence for a suggested classification, but it is never sufficient for silent ownership transfer.

# Source-to-installed mapping

The first release assembler and installer must implement an explicit mapping rather than copying `templates/base/` as a project root.

The intended mapping is:

| Repository source | Installed destination | Ownership |
|---|---|---|
| `templates/base/AGENTS.md` | `/AGENTS.md` | Ava-managed |
| managed base index and contracts | `/.ava/base/` | Ava-managed |
| default roles | `/.ava/base/roles/` | Ava-managed |
| default workflows | `/.ava/base/workflows/` | Ava-managed |
| `templates/base/shared/instructions/ownership-and-mutation.md` | `/.ava/base/shared/instructions/ownership-and-mutation.md` | Ava-managed |
| other managed shared instructions | `/.ava/base/shared/` | Ava-managed |
| release-generated manifest and state | `/.ava/state/` | Ava-managed |
| release upgrade guidance | `/.ava/guidance/` | Ava-managed |
| minimal project scaffold sources | project root extension paths | Project-owned, create-if-absent only |
| selected host bootstrap source | host-specific project-root path | Ava-managed |

Task 06 must either reorganize repository template sources before packaging or provide a release manifest that makes this mapping complete and mechanically verifiable. No release may treat repository source location alone as ownership metadata.

# Removed architecture concepts

This boundary does not require or reserve responsibility for:

- an MCP server
- a persistent Ava runtime
- a feature-rich CLI
- a workspace-provider abstraction
- repository or storage provider layers
- application-service ownership of project context

The installer performs deterministic filesystem and release operations. Installed shared instructions govern how active Ava roles work directly with project-owned context. Release tooling applies only deterministic managed changes and must not perform semantic project maintenance as an incidental side effect.
