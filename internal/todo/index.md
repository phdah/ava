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
- The installer performs deterministic installation, managed-file reconciliation, integrity verification, recovery operations, and mechanical migrations.
- The host agent performs semantic work against project-owned context through existing Ava roles and instructions.
- Agent-facing installation inspection, explanation, recovery coordination, and removal belong to a dedicated Ava Maintenance role rather than new status, repair, or uninstall command surfaces.
- The Maintenance role may invoke deterministic installer operations such as resume, abort, rollback, and finalize, but must not manually reconstruct managed payloads or rewrite protected state.
- Ava uses exactly two ownership classes: Ava-managed and project-owned.
- The root `AGENTS.md` and installed Ava base are Ava-managed. Project customization and host-specific entrypoints remain project-owned.
- `ava_version` identifies only the installed Ava-managed base distribution.
- Semantic compatibility of project-owned content is tracked separately from `ava_version`.
- Project-owned upgrade changes happen through one explicit request that loads installed release guidance.
- Active upgrade state directly selects the managed Upgrade Role before ordinary workflow or role routing.
- OpenCode is the first supported host through native root `AGENTS.md` discovery, project-local managed reads, preserved host configuration, and maintained fixtures.
- No pre-`1.0.0` Ava installation is a supported user state. Historical unversioned Ava migration is therefore outside the v1 roadmap; unknown historical layouts must be refused safely.
- Public distribution contracts, release payload sources, and internal publication procedures are separate repository concerns.
- Internal Ava development roles remain separate from every distributed project bundle.

## Active roadmap

1. [Format contract and base structure](01-format-contract/) - 3 of 4 complete; document update metadata is active
2. [Core roles for initialized projects](02-core-roles/) - 4 of 5 complete; Ava Maintenance remains
3. [Workflow system](03-workflows/) - 6 of 6 complete
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/) - 9 of 10 complete; conformance waits on the two cross-phase blockers
5. [V1 release qualification](05-release-qualification/) - 0 of 5 complete; begins after conformance readiness

The release assembler and thin installer/updater implement deterministic source mapping, integrity verification, installation, direct and chained upgrades, managed reconciliation, restricted migrations, durable recovery state, semantic blocking, and project-owned host entrypoint metadata.

The ordered path to the first stable release is:

1. complete document update metadata
2. create the Ava Maintenance role
3. implement the full validation, conformance, and upgrade matrix
4. define alpha acceptance and prerelease upgrade policy
5. publish `1.0.0-alpha.1`
6. dogfood the alpha and add bounded fix tasks for discovered defects
7. publish a release candidate only after alpha blockers are resolved
8. qualify and publish `1.0.0`

Additional `alpha.N`, beta, or RC releases may be inserted when findings require them. The first alpha is a testable distribution, not a promise that the v1 feature set is defect-free.

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
- preserve the separation between the Ava Maintenance role and the internal Ava Internal Maintainer role
- describe operational capabilities through the host agent and available tools, not a required workspace-provider abstraction
- keep deterministic managed-state mutations inside the installer or updater even when a role initiates them
- validate required files, metadata, links, version state, ownership, and migration references
- update affected template and repository indexes
- update conceptual logs only when a task introduces a major conceptual or structural change
- ensure no files or instructions under `/internal/` are copied into distributed projects
- keep public Ava behavior independent of the internal development role
- ensure every release asset set is internally version-consistent and integrity-verifiable
- document that bootstrap authenticity requires signed provenance or a separately trusted verification path
- test OpenCode against the same installed paths and release assets used by users
- test both fresh installation and explicitly supported prerelease or stable upgrade transitions
- add alpha findings as explicit roadmap tasks before RC or stable qualification
