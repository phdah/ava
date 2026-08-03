# Ava Internal Roadmap

This directory contains the ordered development roadmap for Ava. Each executable task has its own file so a future Ava Internal Maintainer session can complete one bounded change at a time.

## Accepted architecture direction

```text
GitHub Release
    -> thin shell installer or updater
    -> versioned Ava-managed base content
       plus project-owned roles, workflows, instructions, and knowledge
    -> Ava-managed root AGENTS.md
    -> exactly one active role for each request
```

- The files are Ava's product and public interface.
- Ava does not initially require an MCP server, workspace-provider layer, shared Go application service, or feature-rich CLI.
- GitHub Releases provide immutable, version-addressable installer, bundle, checksum, manifest, change-note, and migration assets.
- The installer performs deterministic installation, managed-file reconciliation, integrity verification, and mechanical migrations.
- The host agent performs semantic work against project-owned context through existing Ava roles and instructions.
- Ava uses exactly two ownership classes: Ava-managed and project-owned.
- The root `AGENTS.md` and every installed bootstrap file are Ava-managed. Project customization lives only in project-owned paths.
- `ava_version` identifies only the installed Ava-managed base distribution.
- Semantic compatibility of project-owned content is tracked separately from `ava_version`.
- Project-owned upgrade changes happen through one explicit request that loads installed release guidance.
- Active upgrade state directly selects the managed Upgrade Role before ordinary workflow or role routing.
- Public distribution contracts, release payload sources, and internal publication procedures are separate repository concerns.
- Internal Ava development roles remain separate from every distributed project bundle.

## Active roadmap

1. [Format contract and base structure](01-format-contract/) - 3 of 4 complete; document update metadata remains as a follow-up
2. [Core roles for initialized projects](02-core-roles/) - 4 of 4 complete
3. [Workflow system](03-workflows/) - 6 of 6 complete
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/) - 7 of 9 complete; active with validation and conformance next

The release assembler and thin installer/updater now implement deterministic source mapping, integrity verification, installation, direct and chained upgrades, managed reconciliation, restricted migrations, durable recovery state, semantic blocking, and optional host bootstraps.

Continue Phase 4 with validation, conformance, and upgrade fixtures before publishing the first immutable release.

The format metadata follow-up remains pending without replacing the current Phase 4 sequence.

## Task status

- `pending`: active roadmap work that has not met its completion criteria
- `complete`: active roadmap work that has been implemented, indexed, validated, and committed

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
