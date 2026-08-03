# Ava

Ava is a versioned, file-based context distribution for AI agents. It provides a structured bundle of roles, workflows, instructions, constraints, and knowledge conventions that an agent can discover directly from a project repository.

Ava does not require an agent runtime, MCP server, or general-purpose CLI application. The files are the product. The host agent supplies filesystem access, search, editing, and version-control operations.

> **Status:** Design phase. The public format, distribution ownership, versioning, release, upgrade, and semantic-guidance contracts are defined. Versioned release assembly, installation, and upgrade tooling have not yet been implemented.

## Name

The name Ava is inspired by the AI robot Ava in [*Ex Machina*](https://www.imdb.com/title/tt0470752/). Ava is exceptionally good at playing different roles to achieve her goals. This mirrors the project's role-based structure, where distinct roles support different workflows and make relevant context easy to collect, organize, and retrieve.

## Purpose

Ava should make it easy to add a coherent agent context system to an existing project with one command, while keeping the resulting files understandable and editable without proprietary tooling.

The system should make it clear:

- which agent roles exist
- what each role is responsible for
- what each role may, must, and must not do
- which instructions and context files a role must read
- which predefined workflows exist and which role each workflow activates
- how an agent discovers task-specific context progressively
- which files are managed by Ava and which are owned by the project
- which Ava base version is installed
- whether project-owned context is semantically compatible with that installed version
- how a project is upgraded safely to a later Ava version

The goal is not to hide agent behavior in an application or one large prompt. The goal is to represent it as a navigable, version-controlled hierarchy of small, explicit documents.

## Core idea

An Ava release contains a versioned managed base bundle and the metadata needed to install or upgrade it. A project retains its own roles, workflows, instructions, knowledge, and source material through explicit project-owned extension paths.

```text
GitHub Release
    -> thin shell installer or updater
    -> Ava-managed router, base bundle, state, and guidance
       plus preserved project-owned context
    -> exactly one active role for each request
```

The installer and updater perform deterministic distribution work. The host agent interprets and maintains semantic project context. Ava does not need an MCP protocol layer or persistent command application between them.

## Repository source versus installed projects

This repository does not mirror the filesystem of an installed project.

```text
Ava repository
├── README.md
├── distribution/      # public distribution contracts and schemas
├── templates/         # authored release payload and scaffold sources
└── internal/          # repository-only development and release procedures
```

Release assembly maps repository sources to explicit installed destinations and ownership classes. The repository's `templates/base/` directory is not copied verbatim to a project, and its source paths do not determine installed ownership. Public files under `distribution/` are contracts, not automatically installed payloads. Internal files are never distributed.

The complete mapping, adoption rules, and collision behavior are defined by the [distribution and ownership contract](distribution/ownership.md). Ava versions, installed manifest state, semantic compatibility, and support guarantees are defined by the [versioning and compatibility contract](distribution/versioning.md).

## Installed-project layout

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

Project-owned paths may predate Ava installation, be created by create-if-absent scaffolding, or be added later. Creation time never defines ownership.

## Core model

Ava distinguishes four public concepts:

1. **Roles** define durable responsibilities, authority, constraints, required instructions, and context.
2. **Workflows** define reusable, bounded procedures that activate exactly one primary role.
3. **Shared instructions** define routing, metadata, history, ownership, and other common contracts.
4. **Knowledge** provides trusted project context that roles and workflows load when relevant.

Workflows are optional explicit procedural scopes, not command aliases for ordinary role work. A free-form request selects a role directly. A workflow is justified only when it adds repeatable scope, meaningful inputs, an operating mode, procedure-specific constraints, or a standardized expected output.

The intended relationship is:

```text
request -> managed root router -> exactly one active role
explicit workflow -> exactly one primary role
role or workflow -> managed contracts plus relevant project context
```

Roles and workflows remain ordinary Markdown. Deterministic installation, integrity verification, managed-file replacement, mechanical migrations, and structural validation belong to release tooling rather than workflows or agent roles.

## Distribution through GitHub Releases

GitHub Releases are the canonical Ava distribution channel. Each release contains a mutually compatible set of immutable assets, including:

- a thin POSIX shell installer and updater
- the versioned Ava-managed base bundle
- integrity checksums for every release asset
- a machine-readable release manifest
- human-readable change notes
- agent-readable upgrade guidance
- deterministic migration scripts when required
- GitHub immutable release attestations

The convenience installation path resolves the latest stable release:

```sh
curl -fsSL https://github.com/phdah/ava/releases/latest/download/ava-install.sh | sh
```

A version can be selected directly through the release URL:

```sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.2.3/ava-install.sh | sh
```

These one-line commands execute the bootstrap installer before its checksum can be verified. Checksums downloaded from the same release protect payload integrity after the installer starts, but do not independently authenticate the bootstrap script or publisher.

The [release contract](distribution/releases.md) therefore defines two trust modes:

1. **Convenience mode:** execute the immutable release installer directly and rely on GitHub account, repository, TLS, and release trust.
2. **Verified mode:** download a pinned installer first, verify the GitHub immutable release attestation and installer asset, then execute it.

A mutable script fetched from `main` is not the recommended installation path.

## Installed-project ownership

Ava uses exactly two ownership classes.

### Ava-managed content

Ava-managed content is installed from a specific release and recorded in `/.ava/state/manifest.json`.

It includes:

- `/AGENTS.md`
- all files under `/.ava/base/`
- `/.ava/state/manifest.json`
- `/.ava/state/upgrade.json`
- all files under `/.ava/guidance/`
- any selected host-specific bootstrap file
- deterministic migration support installed by the release

The root `AGENTS.md` remains a stable, project-independent router. Managed default roles, workflows, and shared contracts live under `/.ava/base/`.

Managed-file customization is prohibited. A local edit does not convert a managed file into project-owned content. The updater checks immutable payloads against recorded SHA-256 values, validates mutable managed state through schema and allowed transitions, reports conflicts, and refuses silent overwrite or merge.

### Project-owned content

Project-owned content includes project-specific roles, workflows, instructions, knowledge, source material, indexes, logs, and other context outside declared managed paths.

The standard extension roots are:

- `/roles/`
- `/workflows/`
- `/shared/`
- `/knowledge/`
- `/inbox/`
- `/index.md` and `/log.md` when present

Existing content under those paths remains project-owned during installation. Ava may create minimal scaffold files only when a path is absent. Such scaffolds are project-owned immediately and are never added to the managed manifest.

There is no third ownership class for generated integration shims. Any installed bootstrap or integration file is Ava-managed. Any project customization is project-owned.

Ownership is established by the accepted path contract, manifest record, authority, and explicit adoption decision. It is never inferred from timestamps, creation order, Git history, or similarity to a default file.

## Router and project extensions

The managed root router discovers:

- managed instruction contracts under `/.ava/base/shared/`
- managed default roles under `/.ava/base/roles/`
- managed default workflows under `/.ava/base/workflows/`
- project-owned roles through `/roles/index.md` when present
- project-owned workflows through `/workflows/index.md` when present
- project-owned shared instructions, knowledge, and inbox material only when relevant

Managed and project-owned registries remain separate. A project must not edit managed registries to add project-specific entries.

Canonical paths identify roles and workflows. A name that matches more than one registered concept is ambiguous and must be reported rather than resolved through ownership precedence.

## Host discovery

The canonical entry point is always `/AGENTS.md`.

A host may discover it in one of three supported ways:

1. **Native discovery:** the host automatically loads root `AGENTS.md` with validated compatible semantics.
2. **Host bootstrap:** an optional Ava-managed host-specific file contains only a thin instruction to load `/AGENTS.md`.
3. **Explicit activation:** the user instructs the host to read and follow `./AGENTS.md` as the project root instructions.

Ava must not claim native compatibility for a named host until the behavior is documented or covered by a maintained conformance fixture. Installation and validation report discovery as native, host-bootstrap, explicit-only, or unsupported.

Host-specific bootstrap files must never duplicate routing or ownership rules, contain project customization, or become a second canonical router.

## Installation and adoption

A fresh installation may proceed when the target root is safe and writable, `/.ava/` is absent, and planned managed paths do not collide with unclassified content.

Existing `/index.md`, `/log.md`, `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, and `/inbox/` paths remain untouched and project-owned. Missing minimal scaffolds may be created using create-if-absent behavior.

A pre-existing `/AGENTS.md`, unrecognized `/.ava/`, conflicting host bootstrap, or locally modified managed file aborts automatically until an explicit adoption, recovery, or migration decision resolves the exact path.

Installation into a non-empty project first produces a dry-run classification. It must never silently claim, replace, relocate, merge, or reclassify existing files.

Existing unversioned Ava projects require an explicit migration because their current root layout may mix historical defaults and project-specific content. The migration inventories the files, preserves project-specific behavior in project-owned paths, installs release defaults under `/.ava/base/`, and replaces the root router only after its project-specific meaning has been resolved.

## Versioning

Ava releases follow Semantic Versioning based on supported behavior, not only whether old files remain readable:

- **PATCH** releases preserve supported structure and intended behavior.
- **MINOR** releases add backward-compatible capability that is explicitly opt-in or proven not to change existing routing, resolution, authority, validation, or behavior.
- **MAJOR** releases introduce incompatible format, routing, ownership, authority, resolution, validation, or behavioral changes.

Every installed project records its Ava state in `/.ava/state/manifest.json`.

`ava_version` has one meaning only: it identifies the installed Ava-managed base distribution. It advances after the deterministic base upgrade succeeds, even when project-owned semantic migration remains pending.

Semantic compatibility is tracked separately through:

- `compatible_through`: highest Ava version completed by project-owned context
- `target_version`: installed version currently requiring reconciliation, or `null`
- `status`: `complete`, `pending`, `partial`, or `blocked`
- `unresolved_decisions`: decisions or prerequisites preventing completion

The manifest records immutable managed files as checksum-protected `payload` and mutable files such as `manifest.json` and `upgrade.json` as schema-validated `state`. Managed state files do not contain impossible self-checksums.

The OKF version and Ava version are separate. `okf_version` identifies the underlying knowledge-format compatibility level. `ava_version` identifies only the installed Ava base distribution.

The complete policy, manifest fields, compatibility test, prerelease rules, upgrade paths, deprecation lifecycle, and support windows are defined by [Ava Versioning and Compatibility](distribution/versioning.md).

## Upgrade model

Running the release installer in an existing Ava project performs an explicit deterministic upgrade:

1. Read the installed Ava base version and managed-file manifest.
2. Resolve or receive the target release version.
3. Download and verify the target release assets according to the selected trust mode.
4. Compare the previously installed base, current local managed files, and target base.
5. Abort and report any modified, missing, corrupt, or invalid managed content or state.
6. Replace unchanged Ava-managed payload files.
7. Run deterministic migrations in version order.
8. Install the target release's semantic upgrade guidance.
9. Advance `ava_version` only when deterministic work succeeds.
10. Record any required project-owned context migration in separate semantic compatibility state.

Project-owned context changes happen through one explicit agent request, for example:

```text
Reconcile this project's project-owned Ava context with the installed Ava version. Apply the installed upgrade guidance, explain material semantic changes, and report unresolved decisions before marking semantic migration complete.
```

The active Ava agent inspects the installed version transition, release guidance, affected project context, and migration completion criteria. This keeps project-specific interpretation inside the agent while making the trigger a single clear prompt.

## Logs and release guidance

Scoped `log.md` files remain useful as conceptual history and as source material for release notes. They are not by themselves the migration protocol because they may contain unrelated history and do not necessarily state compatibility impact or required actions.

A release therefore provides structured upgrade guidance that identifies:

- the source and target versions
- changed base contracts and managed paths
- deterministic migrations and their order
- project-owned concepts that require semantic review
- required user decisions or conflict conditions
- validation and completion criteria

The complete representation and composition rules are defined by [Ava Release Guidance](distribution/guidance.md).

## OKF v0.2 structure

Ava follows Google's Open Knowledge Format version 0.2, especially its use of:

- hierarchical Markdown documents
- YAML frontmatter for machine-readable metadata
- `index.md` files for progressive disclosure
- `log.md` files for scoped conceptual history
- Markdown links for relationships between concepts
- provenance, generation, verification, lifecycle, and staleness metadata
- Git for portability, history, attribution, and review

Ava adapts these ideas for agent instructions rather than data-catalog metadata. It does not use BigQuery-specific concepts, resource identifiers, or a fixed data-oriented taxonomy.

The authored document metadata and workflow instructions under `templates/base/shared/instructions/` define the current installed format contracts. Release assembly maps them into the installed managed base.

## Agent traversal model

An installed project provides deterministic guidance for how an agent reads it:

1. Automatically or explicitly load the root `/AGENTS.md` file.
2. Read the managed instruction-resolution and upgrade-state contracts.
3. Determine whether the request explicitly invokes a registered managed or project-owned workflow or is a free-form request.
4. Resolve exactly one active role from the managed and project-owned registries.
5. Read the active role's `index.md` and every document it marks as required.
6. Read the workflow prompt, inputs, and workflow-specific context when a workflow is active.
7. Follow explicit links to task-specific instructions and project context only when relevant.
8. Resolve instruction overlap by explicit activation scope rather than directory depth.
9. Keep capabilities and constraints cumulative and non-expandable at narrower scopes.
10. Ask the user when routing, ownership, or instruction conflicts remain unresolved.

The current user request supplies the immediate objective and narrowest procedural scope, bounded by the active role, project constraints, and capabilities provided by the host agent and its available tools.

## Design goals

- **Simple:** Installation and upgrade require one command in convenience mode, while ordinary use requires no Ava process or service.
- **Human-readable:** The complete system remains understandable with normal filesystem and Markdown tools.
- **Agent-readable:** Agents can discover and parse instructions without an Ava SDK or protocol server.
- **Progressive:** Agents load the minimum relevant context rather than scanning the complete project.
- **Explicit:** Responsibilities, authority, constraints, ownership, workflows, and migrations are written down.
- **Versioned:** Releases and installed projects use a clear SemVer compatibility contract.
- **Upgradeable:** Managed base content can be replaced deterministically and project context can be migrated explicitly.
- **Diffable:** Changes remain reviewable in Git.
- **Portable:** The generated structure does not depend on a specific model provider, agent runtime, editor, or storage backend.
- **Validatable:** Ava can detect structural, metadata, routing, ownership, version, and migration errors.
- **Obsidian-compatible:** Projects remain readable and editable as normal Markdown vaults.

## Initial non-goals

Ava is not initially intended to provide:

- an MCP server
- a persistent or feature-rich CLI application
- an agent execution runtime
- model inference or provider integrations
- a scheduler
- multi-agent orchestration
- workspace-provider abstractions
- repository or storage integrations
- secrets or credential management
- a fixed universal taxonomy
- domain-specific integrations such as databases, APIs, or cloud platforms

The release installer may use standard tools such as `sh`, `curl`, `tar`, and checksum or signature utilities. That does not make Ava a general command platform.

## Internal development roles

Repository-specific development roles live under [`internal/`](internal/). They exist only to help develop Ava and must never be copied into distributed projects, templates, examples, or default role catalogs.

The first internal role is the [Ava Internal Maintainer](internal/roles/ava-internal/). Maintainer-only publication procedures live under [`internal/release/`](internal/release/).

## Roadmap direction

The implementation roadmap is tracked in [`internal/todo.md`](internal/todo.md). Its direction is:

1. retain and refine the existing file format, roles, workflows, and routing contracts
2. define the boundary between Ava-managed base content and project-owned context
3. define Ava SemVer, installed-base versioning, and separate semantic compatibility state
4. define immutable GitHub Release assets and bootstrap trust modes
5. define deterministic upgrade, migration, and agent-guidance protocols
6. implement a thin installer and updater with explicit version selection
7. implement validation and fixtures for installation, adoption, and upgrades
8. publish the first versioned Ava distribution
