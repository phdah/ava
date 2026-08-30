# Ava Internal Roadmap

This directory contains the ordered development roadmap for Ava. Each executable task has its own file so a future Ava Internal Maintainer session can complete one bounded change at a time.

## Accepted architecture direction

```text
GitHub Release
    -> thin shell installer or updater
    -> versioned Ava-managed base content
       plus project-owned roles, workflows, instructions, and knowledge
    -> Ava-managed root AGENTS.md
    -> managed-state gate on every request
    -> roleless follow-up, retained active role, or fresh role/workflow routing
```

- The files are Ava's product and public interface.
- Ava does not initially require an MCP server, workspace-provider layer, shared Go application service, or feature-rich CLI.
- GitHub Releases provide immutable, version-addressable installer, bundle, checksum, manifest, change-note, and migration assets.
- The installer performs deterministic installation, managed-file reconciliation, integrity verification, recovery operations, and mechanical migrations.
- The host agent performs semantic work against project-owned context through existing Ava roles and instructions.
- Agent-facing installation inspection, explanation, deterministic recovery coordination, explicit upgrade initiation, host access reporting, terminal finalization, and removal belong to Ava Maintenance rather than new status, repair, finalization, or uninstall command surfaces.
- Ava Maintenance invokes deterministic installer operations such as resume, abort, and rollback, but successful post-semantic finalization is a bounded direct terminal journal transition performed by the role after all protocol preconditions pass.
- Upgrade Role remains the sole managed role for project-owned semantic reconciliation and compatibility transitions.
- Ava uses exactly two ownership classes: Ava-managed and project-owned.
- The root `AGENTS.md` and installed Ava base are Ava-managed. Project customization and host-specific configuration remain project-owned.
- `ava_version` identifies only the installed Ava-managed base distribution.
- Semantic compatibility of project-owned content is tracked separately from `ava_version`.
- Project-owned upgrade changes happen through one explicit request that loads installed release guidance.
- Managed pre-routing selects Ava Maintenance for deterministic or malformed state and Upgrade Role for semantic reconciliation.
- Every request enters the managed-state gate and Ava's routing decision before substantive handling.
- Role continuity is conversation-scoped only and does not add persistent runtime, manifest, or project state.
- OpenCode is Ava's first installer-supported host configuration.
- Document creation provenance and latest meaningful-update provenance are separate.
- No pre-`1.0.0` Ava installation is a supported user state.
- Stable support guarantees begin with `1.0.0`, not with alpha, beta, or RC publication.
- Public distribution contracts, release payload sources, and internal publication procedures are separate repository concerns.
- Internal Ava development roles remain separate from every distributed project bundle.

## Active roadmap

1. [Format contract and base structure](01-format-contract/) - complete
2. [Core roles for initialized projects](02-core-roles/) - complete
3. [Workflow system](03-workflows/) - complete
4. [Versioned distribution and upgrades](04-distribution-and-upgrades/) - complete
5. [V1 release qualification](05-release-qualification/) - open but release progression is currently parked; qualification hardening is complete
6. [Backlog.md integration](06-backlog-md/) - current implementation phase
7. [Durable interaction evidence](07-interaction-evidence/) - queued after Backlog.md integration

## Current implementation queue

The user has explicitly reprioritized away from continued alpha dogfooding and immediate `1.0.0` progression. The current ordered queue is:

1. [Evaluate and implement Backlog.md for internal todos](06-backlog-md/01-evaluate-and-implement-backlog-md-for-internal-todos.md)
2. [Evaluate and add a default Backlog.md project task role](06-backlog-md/02-evaluate-and-add-default-project-task-role.md)
3. complete the [Durable interaction evidence](07-interaction-evidence/) investigation
4. reassess the roadmap with the user before resuming V1 release work

The two qualification-hardening tasks derived from concrete alpha.15 release-process failures are complete. They remain ordinary implementation history rather than additional dogfood findings and did not create a new exceptional qualification-override architecture.

## Parked V1 release path

Phase 5 remains open because alpha dogfooding has not been explicitly closed and stable release work is not complete. The [V1 Release Operator Path](05-release-qualification/v1-release-operator-path.md) remains authoritative when the user explicitly resumes progression toward `1.0.0`, but it must not preempt the implementation queue above.

Do not infer dogfood closure from the published alpha, passing tests, or an empty blocker list. Do not automatically begin release-candidate work after the current implementation queue.

## Task status

- `pending`: active repository work that has not met its implementation completion criteria
- `completed` or `complete`: repository work that has met its implementation completion criteria according to the task's existing convention

Update a task's frontmatter and its active phase index together when its status changes. Published-asset or realistic-project qualification that can only happen after merge is tracked as a release gate and does not keep or return an implementation task to `pending` unless the task explicitly says so.

## Shared completion work

Complete these concerns as part of the relevant individual tasks:

- keep `templates/base/roles/index.md` accurate
- keep the workflow registry accurate
- verify every role has deterministic required reading
- keep role and workflow routing conditions distinct
- preserve the separation between Ava Maintenance and the internal Ava Internal Maintainer
- preserve the separation between deterministic Ava Maintenance and semantic Upgrade Role authority
- describe operational capabilities through the host agent and available tools, not a required workspace-provider abstraction
- keep deterministic managed-state mutations inside the installer or updater except for Ava Maintenance's protocol-defined successful terminal finalization transition
- validate required files, metadata, links, version state, ownership, and migration references
- update affected template and repository indexes
- update conceptual logs only when a task introduces a major conceptual or structural change
- ensure no files or instructions under `/internal/` are copied into distributed projects
- keep public Ava behavior independent of the internal development role
- ensure every release asset set is internally version-consistent and integrity-verifiable
- document that bootstrap authenticity requires signed provenance or a separately trusted verification path
- test OpenCode against the same installed paths and release assets used by users
- test both fresh installation and explicitly supported prerelease or stable upgrade transitions
