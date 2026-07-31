# Phase 04: Versioned Distribution and Upgrades

Define and implement Ava as an immutable, versioned context distribution installed and upgraded through thin release tooling.

## Tasks

1. [x] [Define the distribution and ownership boundary](01-define-distribution-and-ownership-boundary.md)
2. [x] [Define the Ava SemVer and compatibility contract](02-define-semver-and-compatibility.md)
3. [x] [Define GitHub release assets, trust modes, and channels](03-define-github-release-assets.md)
4. [ ] [Define the upgrade and migration protocol](04-define-upgrade-and-migration-protocol.md)
5. [ ] [Define release guidance and the Upgrade Role](05-define-release-logs-and-agent-guidance.md)
6. [ ] [Separate distribution contracts and release procedures](06-separate-distribution-contracts-and-release-procedures.md)
7. [ ] [Implement the installer and updater](07-implement-installer-and-updater.md)
8. [ ] [Implement validation, conformance, and upgrade fixtures](08-implement-validation-and-upgrade-fixtures.md)
9. [ ] [Publish the first versioned Ava release](09-publish-first-versioned-release.md)

All tasks are active roadmap work and should be completed in order unless a later task is required to unblock an earlier design decision.

The accepted distribution boundary places managed content under `/AGENTS.md` and `/.ava/`, while project-owned extension and context paths remain at the project root. The accepted versioning contract separates installed `ava_version` from project-owned semantic compatibility and distinguishes immutable payload checksums from mutable managed state validation. The accepted release contract defines one immutable GitHub Release asset set, stable and prerelease selection, SHA-256 integrity, GitHub release attestations, and separate convenience and verified bootstrap paths.

Before implementation, the repository structure will separate public distribution contracts and schemas under `/distribution/`, release payload sources under `/templates/`, and maintainer-only publication procedures under `/internal/release/`.

## Previous phase

[Workflow system](../03-workflows/). Its remaining tasks are deferred until the ownership and migration boundaries in this phase are settled.
