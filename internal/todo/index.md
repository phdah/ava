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
- Every request enters managed state gating and explicit workflow or role routing before substantive handling. A generic host persona cannot bypass the Ava router based on apparent subject matter.
- OpenCode is Ava's first installer-supported host configuration. Ava keeps `./.ava/` hidden, creates project-owned OpenCode permissions by default when possible, preserves existing configuration, and validates maintained host behavior through the conformance suite.
- Document creation provenance and latest meaningful-update provenance are separate. `generated` remains immutable creation provenance, while canonical `updated` records only the latest meaningful mutation.
- No pre-`1.0.0` Ava installation is a supported user state. Historical unversioned Ava migration is therefore outside the v1 roadmap; unknown historical layouts must be refused safely.
- `1.0.0-alpha.1` has no supported earlier release source. Later prerelease transitions are supported only through explicit release-manifest upgrade edges.
- Alpha publication is gated by reproducible assembly, the maintained conformance evidence, stable defect classes, protected-state blocker impacts, and explicit approval for the exact version and source revision.
- Release-please prepares versions, changelog state, immutable tags, draft releases, qualified assets, and attestations. Merging the reviewed release pull request authorizes publication of the resulting tagged revision, and the workflow publishes only after all maintained gates pass.
- Stable support guarantees begin with `1.0.0`, not with alpha, beta, or RC publication.
- Public distribution contracts, release payload sources, and internal publication procedures are separate repository concerns.
- Internal Ava development roles remain separate from every distributed project bundle.

## Active roadmap

1. [Format contract and base structure](01-format-contract/) - 4 of 4 complete
2. [Core roles for initialized projects](02-core-roles/) - 5 of 5 complete
3. [Workflow system](03-workflows/) - 6 of 6 complete
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/) - 10 of 10 complete
5. [V1 release qualification](05-release-qualification/) - 3 of 6 core gates complete; dogfood active with 2 pending findings, 3 pending supporting qualification tasks, and 7 completed findings
6. [Backlog.md integration](06-backlog-md/) - 0 of 2 complete; queued after release qualification

The release assembler and thin installer/updater implement deterministic source mapping, integrity verification, installation, direct and chained upgrades, managed reconciliation, restricted migrations, durable recovery state, semantic blocking, project-owned host entrypoint metadata, and create-if-absent OpenCode host configuration.

The managed Ava Maintenance role provides the agent-facing interface for installed identity, integrity, deterministic recovery coordination, host accessibility, explicit upgrades, finalization, and safe removal. Upgrade Role remains isolated to semantic reconciliation of project-owned context.

The unified conformance suite validates repository structure, installed managed state, semantic routing gates, unconditional root-router sequencing, filesystem safety, transaction rollback, host support, release integrity, trust evidence, and immutable publication requirements through stable machine-readable findings and indexed fixtures.

The alpha qualification policy composes that conformance evidence with roadmap completion, reproducible release assembly, defect classification, prerelease upgrade declarations, and exact publication approval.

Release-please enforces release classification at the merge boundary, maintains version and changelog state, keeps one release pull request current, creates immutable tags and draft releases, and hands the exact prepared SHA to qualification, reproducible assembly, release conformance, attestation, non-clobbering asset upload, and automatic publication.

Alpha publication is complete through immutable `1.0.0-alpha.10`. The remaining ordered path to the first stable release is:

1. build the reproducible [synthetic v1 qualification vault](05-release-qualification/04a-build-synthetic-qualification-vault.md)
2. [qualify and publish the corrective alpha](05-release-qualification/04b-qualify-and-publish-corrective-alpha.md), collecting immutable evidence for completed findings 03 through 07
3. complete [review sufficiency and termination criteria](05-release-qualification/dogfood/08-define-review-sufficiency-and-termination.md)
4. [compose semantic upgrades from adjacent release edges](05-release-qualification/dogfood/09-compose-semantic-upgrades-from-adjacent-edges.md)
5. continue working the [dogfood findings backlog](05-release-qualification/dogfood/) during realistic prerelease use and keep the dogfood umbrella active until the user explicitly declares it complete
6. publish the release candidate only after dogfood blockers and required RC work are resolved
7. [stabilize the published release candidate](05-release-qualification/05a-stabilize-release-candidate.md) through the complete generated-vault matrix
8. qualify and publish `1.0.0`

Dogfood findings are numbered independently from the six core Phase 5 gates. New findings may be added and resolved continuously without renumbering release stages. Completed findings remain as durable evidence, and an empty backlog does not automatically advance the roadmap.

Additional `alpha.N`, beta, or RC releases may be inserted when findings require them. The first alpha is a testable distribution, not a promise that the v1 feature set is defect-free.

Phase 6 is queued after release qualification and does not block the v1 release unless the user explicitly reprioritizes it.

## Task status

- `pending`: active repository work that has not met its implementation completion criteria
- `completed`: repository work that has been implemented, indexed, repository-validated, and committed with resolution evidence

Update a task's frontmatter and its active phase index together when its status changes. Published-asset or realistic-project qualification that can only happen after merge is tracked as a release gate and does not keep or return an implementation task to `pending`. Individual finding completion never completes the dogfood umbrella unless the user explicitly makes that decision.

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
