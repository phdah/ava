# Ava

Ava is a versioned, file-based context distribution for AI agents. It installs a structured system of roles, workflows, instructions, constraints, routing rules, and knowledge conventions directly into a project repository.

The files are the product. Ava does not require a persistent agent runtime, MCP server, or proprietary application. A compatible host agent supplies filesystem access, search, editing, and version-control operations while Ava supplies the project-local context system and its deterministic release tooling.

> **Status:** Ava is entering its stable `1.0.0` release line. Installation, upgrades, release assembly, conformance validation, qualification, attestations, and immutable GitHub Release publication are implemented and maintained in this repository.

## Why Ava

Agent context tends to become difficult to navigate when responsibilities, instructions, workflows, and project knowledge accumulate in one large prompt or in loosely related files. Ava instead gives the agent a predictable hierarchy that can be discovered progressively.

Ava makes it explicit:

- which roles exist and when each role should be active
- what each role may, must, and must not do
- which instructions a role must read
- which reusable workflows exist and which role owns each workflow
- how conversational follow-ups differ from new scoped work
- which files are Ava-managed and which remain project-owned
- which Ava version is installed
- whether the installed managed base is healthy
- how later stable releases are upgraded safely

## Install

The convenience installation path resolves the latest stable GitHub Release:

```sh
curl -fsSL https://github.com/phdah/ava/releases/latest/download/ava-install.sh | sh
```

A specific stable version can be selected through its immutable release URL:

```sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.0.0/ava-install.sh | sh
```

For a stronger trust boundary, download the installer and release assets first, verify the GitHub release attestation and checksums, and then execute the pinned installer. The exact trust and asset contract is documented in [Ava GitHub Release Assets](distribution/releases.md).

## Core model

Ava distinguishes four public concepts:

1. **Roles** define durable responsibilities, authority, constraints, required instructions, and context.
2. **Workflows** define reusable bounded procedures that activate exactly one primary role.
3. **Shared instructions** define routing, metadata, history, ownership, and other common contracts.
4. **Knowledge** provides trusted project context that roles and workflows load when relevant.

The routing model is intentionally explicit:

```text
request
  -> managed-state gate
  -> roleless conversational follow-up
     OR same-role continuation
     OR fresh role/workflow resolution
  -> relevant managed contracts and project context
```

A workflow is not required for ordinary role work. It is useful when the task benefits from a repeatable procedure, defined inputs, a specific operating mode, or a standardized output.

## Installed project layout

A standard installed project looks like this:

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
├── roles/                            # project-owned extensions
├── workflows/                        # project-owned extensions
├── shared/                           # project-owned shared context
├── knowledge/                        # project-owned trusted knowledge
└── inbox/                            # project-owned source intake
```

The repository itself is not copied verbatim into an installed project. Release assembly maps authored repository sources to explicit installed destinations.

```text
Ava repository
├── README.md
├── distribution/      # public contracts and schemas
├── templates/         # authored managed payload and scaffold sources
└── internal/          # repository-only development and release machinery
```

## Ownership boundary

Ava uses two ownership classes.

### Ava-managed

Managed content is installed from one immutable Ava release and recorded in `/.ava/state/manifest.json`. It includes the canonical router, the managed base, managed state, release guidance, and deterministic migration support.

Managed payload files are checksum-protected. Local modification, deletion, corruption, or unexpected managed content is detected rather than silently overwritten.

### Project-owned

Project roles, workflows, instructions, knowledge, inbox material, logs, indexes, and other context remain project-owned. Installation and upgrades preserve them byte-for-byte unless an explicit project-context reconciliation asks an agent to change them.

Creation time does not determine ownership. The path contract, installed manifest, and explicit adoption decisions do.

See [Ava Distribution and Ownership Boundary](distribution/ownership.md) for the complete rules.

## Managed-state gate

Every request first checks the installed Ava state. Normal routing is permitted only when managed state is structurally valid and no active maintenance transaction requires attention.

This means the same installed files that drive routing also provide deterministic signals for damaged managed content, incomplete upgrades, pending finalization, and other maintenance conditions.

## Installation and adoption

Fresh installation is deterministic and supports both empty and mature repositories.

Existing project-owned content under the standard extension roots is preserved. Missing scaffolds may be created only with create-if-absent semantics. A conflicting root router, unrecognized `.ava/` state, or locally modified managed payload causes the installer to stop rather than guess.

A dry-run mode reports the intended classification and mutations before installation into a non-empty project.

## Stable versioning

Ava follows Semantic Versioning for the stable release line:

- **PATCH** preserves supported structure and intended behavior.
- **MINOR** adds backward-compatible capability that is opt-in or proven behavior-preserving for existing projects.
- **MAJOR** introduces an incompatible format, routing, ownership, authority, resolution, validation, or behavioral change.

Each installed project records its Ava version and managed release identity in `/.ava/state/manifest.json`. Semantic compatibility of project-owned context is tracked separately from the installed managed-base version.

The complete policy is defined in [Ava Versioning and Compatibility](distribution/versioning.md).

## Upgrade model

Stable `1.0.0` is the root of Ava's supported release lineage. It has no previous supported release and no upgrade edge.

Every later release records exactly one adjacent edge from the immediately previous stable release. The updater composes those immutable edge records when a supported project upgrades across more than one release.

A normal deterministic upgrade:

1. reads the installed release identity and managed manifest
2. resolves and verifies the target immutable release assets
3. checks local managed content against the installed baseline
4. refuses unresolved managed-file conflicts
5. replaces unchanged managed payloads
6. runs declared deterministic migrations
7. installs transition-local semantic guidance when required
8. advances the installed managed-base version only after deterministic work succeeds
9. leaves project-owned semantic reconciliation as an explicit agent task when the release requires it

This keeps mechanical distribution work deterministic while leaving project-specific interpretation with the agent.

## Release integrity

GitHub Releases are Ava's canonical distribution channel. A stable release contains a mutually compatible immutable asset set including:

- `ava-install.sh`
- `ava-base.tar.gz`
- `ava-guidance.tar.gz`
- `ava-migrations.tar.gz`
- `ava-release.json`
- `ava-release-notes.md`
- `SHA256SUMS`

A release is published only after maintained qualification, reproducible assembly, conformance validation, asset attestation, checksum verification, and immutable-release verification succeed.

Release Please coordinates version and changelog changes. Ordinary implementation PRs are squash merged. Release Please release PRs are merge-committed so the accepted qualification revision remains in commit ancestry.

## Repository development

Repository-only release and qualification machinery lives under `internal/release/`. Public contracts live under `distribution/`. Authored managed payloads and project scaffolds live under `templates/`.

The internal roadmap is maintained under `internal/todo/` using Backlog.md-compatible task records.

## Public contracts

The main public contracts are:

- [Distribution and ownership](distribution/ownership.md)
- [Paths and installed layout](distribution/paths.md)
- [Versioning and compatibility](distribution/versioning.md)
- [GitHub release assets](distribution/releases.md)
- [Upgrades and migrations](distribution/upgrades.md)
- [Release guidance](distribution/guidance.md)
- [Adjacent upgrade edges](distribution/adjacent-upgrade-edges.md)

These contracts define the supported behavior of an installed Ava release. Internal implementation details must conform to them rather than silently redefining them.
