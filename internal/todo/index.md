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
- Agent-facing installation inspection, explanation, deterministic recovery coordination, explicit upgrade initiation, host access reporting, and removal belong to Ava Maintenance rather than new status, repair, or uninstall command surfaces.
- Ava Maintenance may invoke deterministic installer operations such as resume, abort, rollback, and finalize, but must not manually reconstruct managed payloads or rewrite protected state.
- Upgrade Role remains the sole managed role for project-owned semantic reconciliation and compatibility transitions.
- Ava uses exactly two ownership classes: Ava-managed and project-owned.
- The root `AGENTS.md` and installed Ava base are Ava-managed. Project customization and host-specific configuration remain project-owned.
- `ava_version` identifies only the installed Ava-managed base distribution.
- Semantic compatibility of project-owned content is tracked separately from `ava_version`.
- Project-owned upgrade changes happen through one explicit request that loads installed release guidance.
- Managed pre-routing selects Ava Maintenance for deterministic or malformed state and Upgrade Role for semantic reconciliation.
- OpenCode is Ava's first installer-supported host configuration. Ava keeps `./.ava/` hidden, creates project-owned OpenCode permissions by default when possible, preserves existing configuration, and defers broader runtime conformance to the final conformance task.
- Document creation provenance and latest meaningful-update provenance are separate. `generated` remains immutable creation provenance, while canonical `updated` records only the latest meaningful mutation.
- No pre-`1.0.0` Ava installation is a supported user state. Historical unversioned Ava migration is therefore outside the v1 roadmap; unknown historical layouts must be refused safely.
- Public distribution contracts, release payload sources, and internal publication procedures are separate repository concerns.
- Internal Ava development roles remain separate from every distributed project bundle.

## Active roadmap

1. [Format contract and base structure](01-format-contract/) - 4 of 4 complete
2. [Core roles for initialized projects](02-core-roles/) - 5 of 5 complete
3. [Workflow system](03-workflows/) - 6 of 6 complete
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/) - 9 of 10 complete; active with final conformance next
5. [V1 release qualification](05-release-qualification/) - 0 of 5 complete; begins after conformance readiness

The release assembler and thin installer/updater implement deterministic source mapping, integrity verification, installation, direct and chained upgrades, managed reconciliation, restricted migrations, durable recovery state, semantic blocking, project-owned host entrypoint metadata, and create-if-absent OpenCode host configuration.

The managed Ava Maintenance role now provides the agent-facing interface for installed identity, integrity, deterministic recovery coordination, host accessibility, explicit upgrades, finalization, and safe removal. Upgrade Role remains isolated to semantic reconciliation of project-owned context.

The ordered path to the first stable release is:

1. implement the full validation, conformance, and upgrade matrix
2. define alpha acceptance and prerelease upgrade policy
3. publish `1.0.0-alpha.1`
4. dogfood the alpha and add bounded fix tasks for discovered defects
5. publish a release candidate only after alpha blockers are resolved
6. qualify and publish `1.0.0`

Additional `alpha.N`, beta, or RC releases may be inserted when findings require them. The first alpha is a testable distribution, not a promise that the v1 feature set is defect-free.

## Task status

- `pending`: active roadmap work that has not met its completion criteria
- `completed`: active roadmap work that has been implemented, indexed, validated, and committed

Update a task's frontmatter and its active phase index together when its status changes.

## Shared completion work

Complete these concerns as part of the relevant individual tasks:

- keep `templates/base/roles/index.md` accurate
- keep the workflow registry accurate
- verify every role has deterministic required reading
- keep role and workflow routing conditions distinct
- preserve the separation between Ava Maintenance and the internal Ava Internal Maintainer
- preserve the separation between deterministic Ava Maintenance and semantic Upgrade Role authority
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
