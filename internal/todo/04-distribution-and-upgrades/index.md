# Phase 04: Versioned Distribution and Upgrades

Define and implement Ava as an immutable, versioned context distribution installed and upgraded through thin release tooling.

## Tasks

1. [x] [Define the distribution and ownership boundary](01-define-distribution-and-ownership-boundary.md)
2. [x] [Define the Ava SemVer and compatibility contract](02-define-semver-and-compatibility.md)
3. [x] [Define GitHub release assets, trust modes, and channels](03-define-github-release-assets.md)
4. [x] [Define the upgrade and migration protocol](04-define-upgrade-and-migration-protocol.md)
5. [x] [Define release guidance and the Upgrade Role](05-define-release-logs-and-agent-guidance.md)
6. [ ] [Separate distribution contracts and release procedures](06-separate-distribution-contracts-and-release-procedures.md)
7. [ ] [Implement the installer and updater](07-implement-installer-and-updater.md)
8. [ ] [Implement validation, conformance, and upgrade fixtures](08-implement-validation-and-upgrade-fixtures.md)
9. [ ] [Publish the first versioned Ava release](09-publish-first-versioned-release.md)

The workflow catalog audit is complete. Task 6 is the current next task and must separate public distribution contracts, release payload sources, and maintainer-only publication procedures before installer implementation.

The accepted distribution boundary places managed content under `/AGENTS.md` and `/.ava/`, while project-owned extension and context paths remain at the project root. The accepted versioning contract separates installed `ava_version` from project-owned semantic compatibility and distinguishes immutable payload checksums from mutable managed state validation. The accepted release contract defines one immutable GitHub Release asset set, stable and prerelease selection, SHA-256 integrity, GitHub release attestations, and separate convenience and verified bootstrap paths.

The accepted upgrade protocol defines explicit release edges, three-way managed reconciliation, a durable `upgrade.json` transaction journal, ordered idempotent migrations, manifest-last commit semantics, managed pre-routing upgrade mode, and rollback that never silently reverses project-owned edits.

The accepted release-guidance contract defines versioned installed `UPGRADE.md` documents with validated metadata, explicit affected project concepts, decisions, procedures, completion criteria, rollback implications, and ordered multi-version composition. Active upgrade state directly selects the managed Upgrade Role before any project-owned registry or workflow discovery.

The workflow audit defines workflows as optional explicitly invoked procedures rather than command aliases for ordinary role work. The managed catalog contains batch inbox ingestion, bounded change review, complete role-catalog review, and bounded project-context audit. Workflow changes follow the versioning and semantic migration boundaries defined by the compatibility contract.

Before implementation, the repository structure will separate public distribution contracts and schemas under `/distribution/`, release payload sources under `/templates/`, and maintainer-only publication procedures under `/internal/release/`.

## Previous active phase

[Workflow system](../03-workflows/). Its built-in catalog audit is complete; trigger portability and lifecycle ownership remain pending and do not replace the current distribution task.
