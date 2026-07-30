# Ava

Ava is a proposed versioned, file-based context distribution for AI agents. It provides a structured bundle of roles, workflows, instructions, constraints, and knowledge conventions that an agent can discover directly from a project repository.

Ava is not intended to require an agent runtime, MCP server, or general-purpose CLI application. The files are the product. The host agent supplies filesystem access, search, editing, and version-control operations.

> **Status:** Design phase. The distribution-first direction described here is proposed in draft PR #11 and is not accepted architecture until explicitly approved. The repository contains the current format and project templates. Versioned release artifacts, installation, and upgrade support have not yet been implemented.

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

## Proposed core idea

An Ava release would contain a versioned base context bundle and the metadata needed to install or upgrade it. A project would receive that bundle, add its own roles, workflows, instructions, and knowledge, and expose a root `AGENTS.md` entry point that an agent loads automatically.

```text
GitHub Release
    -> thin shell installer or updater
    -> Ava-managed base context plus project-owned context
    -> Ava-managed root AGENTS.md
    -> automatic role and instruction discovery
```

The installer and updater perform deterministic distribution work. The agent interprets and maintains semantic project context. Ava does not need an MCP protocol layer or persistent command application between them.

## Core model

Ava distinguishes four public concepts:

1. **Roles** define durable responsibilities, authority, constraints, required instructions, and context.
2. **Workflows** define reusable, bounded procedures that activate exactly one primary role.
3. **Shared instructions** define project-wide contracts for routing, metadata, history, and other common behavior.
4. **Knowledge** provides trusted project context that roles and workflows load when relevant.

The intended relationship is:

```text
request -> root router -> exactly one active role
explicit workflow -> exactly one primary role
role or workflow -> shared instructions and relevant project context
```

Roles and workflows remain ordinary Markdown. Deterministic installation, integrity verification, managed-file replacement, and mechanical migrations belong to release tooling rather than agent roles.

## Proposed distribution through GitHub Releases

GitHub Releases are the proposed canonical Ava distribution channel. Each release should contain a mutually compatible set of immutable assets, including:

- a thin POSIX shell installer and updater
- the versioned Ava base bundle
- integrity checksums for every release asset
- a machine-readable release manifest
- human-readable change notes
- agent-readable upgrade guidance
- deterministic migration scripts when required
- signed release provenance or attestations when the trust model is finalized

A convenient latest-stable installation could use:

```sh
curl -fsSL https://github.com/phdah/ava/releases/latest/download/ava-install.sh | sh
```

A version could be selected directly through the release URL:

```sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.2.3/ava-install.sh | sh
```

These one-line commands are convenient but execute the bootstrap installer before its checksum can be verified. Checksums downloaded from the same release protect payload integrity after the installer starts, but do not independently authenticate the bootstrap script or publisher.

The release contract must therefore define two explicit trust modes:

1. **Convenience mode:** execute the immutable release installer directly and rely on GitHub account, repository, and TLS trust.
2. **Verified mode:** download a pinned installer first, verify signed provenance or an attestation through a separately trusted mechanism, then execute it.

The exact signing or attestation mechanism remains an open roadmap decision. Ava must not claim that release checksums alone make `curl | sh` independently verifiable.

A mutable script fetched from `main` should not be the recommended installation path.

## Proposed installed-project ownership

Ava should use exactly two ownership classes.

### Ava-managed content

Versioned base instructions, routing contracts, default roles, default workflows, manifests, migration guidance, and bootstrap files distributed by Ava. The root `AGENTS.md` is Ava-managed and should remain a stable router. Project customization must live in project-owned paths referenced by the managed router rather than modifying the router itself.

The local manifest records the installed version and checksums of Ava-managed files. An updater may replace unchanged managed files and must detect local modifications before overwriting them.

### Project-owned content

Project-specific roles, workflows, instructions, and knowledge created after installation. Ava must not rewrite this content as an incidental side effect of replacing the base bundle.

There is no third ownership class for generated integration shims. Any installed bootstrap or integration file is Ava-managed. Any project customization is project-owned.

The exact path layout and boundary rules remain an open roadmap task. The current files under `templates/base/` remain the format reference until that ownership contract is finalized.

## Proposed versioning

Ava releases should follow Semantic Versioning:

- **PATCH** releases correct defects or clarify text without changing supported structure or intended behavior.
- **MINOR** releases add backward-compatible instructions, roles, workflows, metadata, or optional capabilities.
- **MAJOR** releases introduce incompatible format, routing, ownership, or behavioral contract changes.

Every installed project should record its Ava state in a project-level manifest.

`ava_version` has one meaning only: it identifies the installed Ava-managed base distribution. It advances after the deterministic base upgrade succeeds, even when project-owned semantic migration remains pending.

Semantic compatibility must be tracked separately. The manifest should record at least:

- which Ava version the project-owned context is semantically compatible through
- which installed target version still requires semantic migration
- whether that migration is complete, partial, blocked, or pending
- unresolved user decisions that prevent completion

The exact metadata shape remains part of the versioning task. It must not overload `ava_version` with both installed-base and project-behavior semantics.

The OKF version and Ava version are also separate. `okf_version` identifies the underlying knowledge-format compatibility level. `ava_version` identifies only the installed Ava base distribution.

## Proposed upgrade model

Running the release installer in an existing Ava project should perform an explicit deterministic upgrade:

1. Read the installed Ava base version and managed-file manifest.
2. Resolve or receive the target release version.
3. Download and verify the target release assets according to the selected trust mode.
4. Compare the previously installed base, current local managed files, and target base.
5. Replace unchanged Ava-managed files and report conflicts for locally modified managed files.
6. Run deterministic migrations in version order.
7. Install the target release's semantic upgrade guidance.
8. Advance `ava_version` only when deterministic work succeeds.
9. Record any required project-owned context migration in the separate semantic compatibility state.

Project-owned context changes should happen through one explicit agent request, for example:

```text
Reconcile this project's project-owned Ava context with the installed Ava version. Apply the installed upgrade guidance, explain material semantic changes, and report unresolved decisions before marking semantic migration complete.
```

The active Ava agent should inspect the installed version transition, release guidance, affected project context, and migration completion criteria. This keeps project-specific interpretation inside the agent while making the trigger a single clear prompt.

## Logs and release guidance

Scoped `log.md` files remain useful as conceptual history and as source material for release notes. They should not by themselves be the migration protocol because they may contain unrelated history and do not necessarily state compatibility impact or required actions.

A release should therefore provide structured upgrade guidance derived from relevant logs and explicit migration decisions. It should identify:

- the source and target versions
- changed base contracts and managed paths
- deterministic migrations and their order
- project-owned concepts that require semantic review
- required user decisions or conflict conditions
- validation and completion criteria

The roadmap will decide whether this is represented by a release manifest, an `UPGRADE.md` document, structured upgrade metadata associated with `log.md`, or a combination of them.

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

The generated document metadata and workflow instructions under `templates/base/shared/instructions/` define the current public format contracts.

## Agent traversal model

An initialized project should provide deterministic guidance for how an agent reads it:

1. Automatically load the root `AGENTS.md` file.
2. Read the shared instruction-resolution contract required by the router.
3. Determine whether the request explicitly invokes a registered workflow or is a free-form request.
4. Resolve exactly one active role.
5. Read the active role's `index.md` and every document it marks as required.
6. Read the workflow prompt and workflow-specific context when a workflow is active.
7. Follow explicit links to task-specific instructions and context only when relevant.
8. Resolve instruction overlap by explicit activation scope rather than directory depth.
9. Keep capabilities and constraints cumulative and non-expandable at narrower scopes.
10. Ask the user when routing or instruction conflicts remain unresolved.

The current user request supplies the immediate objective and narrowest procedural scope, bounded by the active role, project constraints, and capabilities provided by the host agent and its available tools.

## Design goals

- **Simple:** Installation and upgrade should require one command in convenience mode, while ordinary use requires no Ava process or service.
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

The first internal role is the [Ava Internal Maintainer](internal/roles/ava-internal/).

## Proposed roadmap direction

The proposed replacement roadmap is tracked in [`internal/todo.md`](internal/todo.md). Its direction is:

1. obtain explicit approval for the distribution-first architecture
2. retain and refine the existing file format, roles, workflows, and routing contracts
3. define the boundary between Ava-managed base content and project-owned context
4. define Ava SemVer, installed-base versioning, and separate semantic compatibility state
5. define immutable GitHub Release assets and bootstrap trust modes
6. implement a thin installer and updater with explicit version selection
7. implement deterministic migrations, conflict detection, rollback, and validation
8. define structured, agent-readable semantic upgrade guidance
9. support a one-prompt project-context migration procedure
10. test fresh installs and upgrades across supported release transitions
11. publish the first versioned Ava distribution

Until the architecture is explicitly approved, this roadmap remains a proposal and application-centric implementation tasks remain superseded only within this draft branch.