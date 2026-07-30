# Phase 04: Proposed Versioned Distribution and Upgrades

This phase proposes Ava as an immutable, versioned context distribution installed and upgraded through thin release tooling.

The phase is not accepted architecture and its tasks must not be executed until the user explicitly approves the pivot.

## Proposed tasks

1. [ ] [Define the distribution and ownership boundary](01-define-distribution-and-ownership-boundary.md)
2. [ ] [Define the Ava SemVer and compatibility contract](02-define-semver-and-compatibility.md)
3. [ ] [Define GitHub release assets, trust modes, and channels](03-define-github-release-assets.md)
4. [ ] [Define the upgrade and migration protocol](04-define-upgrade-and-migration-protocol.md)
5. [ ] [Define release logs and agent upgrade guidance](05-define-release-logs-and-agent-guidance.md)
6. [ ] [Implement the installer and updater](06-implement-installer-and-updater.md)
7. [ ] [Implement validation, rollback, trust, and upgrade fixtures](07-implement-validation-and-upgrade-fixtures.md)
8. [ ] [Publish the first versioned Ava release](08-publish-first-versioned-release.md)

Every task currently has `status: proposed`. After architecture approval, activate tasks in order by changing only the next task to `pending` and updating the root roadmap.

## Previous phase

[Workflow system](../03-workflows/). Its remaining tasks would be deferred until the ownership and migration boundaries in this proposed phase are settled.