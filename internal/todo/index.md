# Ava Internal Roadmap

This directory contains the ordered development roadmap for Ava. Each executable task has its own file so a future Ava Internal Maintainer session can complete one bounded change at a time.

## Accepted architecture direction

```text
GitHub Release
    -> thin shell installer or updater
    -> versioned Ava-managed base content
       plus project-owned roles, workflows, instructions, and knowledge
    -> root AGENTS.md
    -> exactly one active role for each request
```

- The files are Ava's product and public interface.
- Ava does not initially require an MCP server, workspace-provider layer, shared Go application service, or feature-rich CLI.
- GitHub Releases provide immutable, version-addressable installer, bundle, checksum, manifest, change-note, and migration assets.
- The installer performs deterministic installation, managed-file reconciliation, checksum verification, and mechanical migrations.
- The host agent performs semantic work against project-owned context through existing Ava roles and instructions.
- Ava-managed content and project-owned content must have an explicit ownership boundary.
- Installed projects record their Ava version, managed-file checksums, completed migrations, and pending semantic upgrade state.
- Semantic Versioning describes compatibility across Ava distributions.
- Project-owned context is changed only through an explicit agent request that loads release-specific upgrade guidance.
- Scoped `log.md` files remain conceptual history and may feed release notes, but release upgrade guidance must clearly state compatibility impact and required actions.
- Internal Ava development roles remain separate from every distributed project bundle.

## Active roadmap

1. [Format contract and base structure](01-format-contract/) - 3 of 3 complete
2. [Core roles for initialized projects](02-core-roles/) - 4 of 4 complete
3. [Workflow system](03-workflows/) - 3 of 6 complete; remaining work is deferred until the distribution ownership contract is settled
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/) - 0 of 8 complete

The distribution pivot is now the active priority. Resume the remaining workflow-system tasks after the ownership, release, and migration boundaries are explicit enough to evaluate how workflows participate in upgrades.

## Superseded pre-pivot phases

The following directories preserve the previous application-centric roadmap for historical context. Their pending tasks are not executable roadmap work and must not be selected as the next task:

- [Workspace access and provider abstraction](04-workspace-provider/)
- [Semantic MCP tool catalog](05-semantic-tools/)
- [Deterministic validation for the application architecture](06-validation/)
- [Shared Go application services](07-application-services/)
- [MCP implementation](08-mcp/)
- [Companion CLI](09-cli/)
- [Testing, compatibility, and migrations for the application architecture](10-compatibility/)

These directories may be removed or converted into historical notes after the replacement roadmap has been implemented and reviewed. Until then, this root roadmap determines which tasks are active.

## Task status

- `pending`: active roadmap work that has not met its completion criteria
- `complete`: active roadmap work that has been implemented, indexed, validated, and committed
- `superseded`: historical planning that must not be executed under the accepted architecture

A phase explicitly listed under **Superseded pre-pivot phases** is superseded regardless of legacy `pending` metadata in its child task files.

Update a task's frontmatter and its active phase index together when its status changes.

## Shared completion work

Complete these concerns as part of the relevant individual tasks:

- preserve the existing generated-project instruction contracts unless the task explicitly changes them
- keep `templates/base/roles/index.md` accurate
- keep the workflow registry accurate
- verify every role has deterministic required reading
- keep role and workflow routing conditions distinct
- validate required files, metadata, links, version state, ownership, and migration references
- update affected template and repository indexes
- update conceptual logs only when a task introduces a major conceptual or structural change
- ensure no files or instructions under `/internal/` are copied into distributed projects
- keep public Ava behavior independent of the internal development role
- ensure every release asset set is internally version-consistent and checksum-verifiable
- test both fresh installation and supported upgrade transitions
