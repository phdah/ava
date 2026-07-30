# Ava Internal Roadmap

This directory contains the ordered development roadmap for Ava. Each executable task has its own file so a future Ava Internal Maintainer session can complete one bounded change at a time.

## Proposed architecture direction

This replacement direction is under review in draft PR #11. It must not be treated as accepted architecture until the user explicitly approves it.

```text
GitHub Release
    -> thin shell installer or updater
    -> versioned Ava-managed base content
       plus project-owned roles, workflows, instructions, and knowledge
    -> Ava-managed root AGENTS.md
    -> exactly one active role for each request
```

- The files are proposed as Ava's product and public interface.
- Ava would not initially require an MCP server, workspace-provider layer, shared Go application service, or feature-rich CLI.
- GitHub Releases would provide immutable, version-addressable installer, bundle, checksum, manifest, change-note, and migration assets.
- The installer would perform deterministic installation, managed-file reconciliation, integrity verification, and mechanical migrations.
- The host agent would perform semantic work against project-owned context through existing Ava roles and instructions.
- Ava would use exactly two ownership classes: Ava-managed and project-owned.
- The root `AGENTS.md` and every installed bootstrap file would be Ava-managed. Project customization would live only in project-owned paths.
- `ava_version` would identify only the installed Ava-managed base distribution.
- Semantic compatibility of project-owned content would be tracked separately from `ava_version`.
- Project-owned context would change only through an explicit agent request that loads release-specific upgrade guidance.
- Scoped `log.md` files would remain conceptual history and may feed release notes, but release guidance must state compatibility impact and required actions directly.
- Release checksums would protect integrity but would not independently authenticate a `curl | sh` bootstrap. A separate signing or attestation decision is required.
- Internal Ava development roles would remain separate from every distributed project bundle.

## Proposed replacement roadmap

1. [Format contract and base structure](01-format-contract/) - 3 of 3 complete
2. [Core roles for initialized projects](02-core-roles/) - 4 of 4 complete
3. [Workflow system](03-workflows/) - 3 of 6 complete; remaining work would be deferred until the distribution ownership contract is settled
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/) - 0 of 8 complete

No implementation task in the replacement phase should be treated as approved until the user approves the architecture. After approval, the distribution and ownership boundary becomes the next active task.

## Proposed superseded phases

The following directories preserve the previous application-centric roadmap for historical context. Within this draft branch they are proposed as superseded and must not be selected while the replacement direction is under review:

- [Workspace access and provider abstraction](04-workspace-provider/)
- [Semantic MCP tool catalog](05-semantic-tools/)
- [Deterministic validation for the application architecture](06-validation/)
- [Shared Go application services](07-application-services/)
- [MCP implementation](08-mcp/)
- [Companion CLI](09-cli/)
- [Testing, compatibility, and migrations for the application architecture](10-compatibility/)

If the pivot is rejected, these phases remain the existing roadmap. If the pivot is approved, they may be marked formally superseded or converted into historical notes.

## Task status

- `pending`: roadmap work that has not met its completion criteria
- `complete`: roadmap work that has been implemented, indexed, validated, and committed
- `proposed`: replacement roadmap work awaiting architecture approval
- `superseded`: historical planning that must not be executed under approved replacement architecture

Tasks under `04-distribution-and-upgrades/` remain proposed until the user approves this architectural pivot.

Update a task's frontmatter and its active phase index together when its status changes.

## Shared completion work

Complete these concerns as part of the relevant individual tasks:

- keep `templates/base/roles/index.md` accurate
- keep the workflow registry accurate
- verify every role has deterministic required reading
- keep role and workflow routing conditions distinct
- describe operational capabilities through the host agent and available tools, not a required workspace-provider abstraction
- validate required files, metadata, links, version state, ownership, and migration references
- update affected template and repository indexes
- update conceptual logs only when a task introduces a major conceptual or structural change
- ensure no files or instructions under `/internal/` are copied into distributed projects
- keep public Ava behavior independent of the internal development role
- ensure every release asset set is internally version-consistent and integrity-verifiable
- document that bootstrap authenticity requires signed provenance or a separately trusted verification path
- test both fresh installation and supported upgrade transitions