# Phase 04: Versioned Distribution and Upgrades

Define and implement Ava as an immutable, versioned context distribution installed and upgraded through thin release tooling.

## Tasks

1. [x] [Define the distribution and ownership boundary](01-define-distribution-and-ownership-boundary.md)
2. [ ] [Define the Ava SemVer and compatibility contract](02-define-semver-and-compatibility.md)
3. [ ] [Define GitHub release assets, trust modes, and channels](03-define-github-release-assets.md)
4. [ ] [Define the upgrade and migration protocol](04-define-upgrade-and-migration-protocol.md)
5. [ ] [Define release guidance and the Upgrade Role](05-define-release-logs-and-agent-guidance.md)
6. [ ] [Implement the installer and updater](06-implement-installer-and-updater.md)
7. [ ] [Implement validation, conformance, and upgrade fixtures](07-implement-validation-and-upgrade-fixtures.md)
8. [ ] [Publish the first versioned Ava release](08-publish-first-versioned-release.md)

All tasks are active roadmap work and should be completed in order unless a later task is required to unblock an earlier design decision.

The accepted distribution boundary places managed content under `/AGENTS.md` and `/.ava/`, while project-owned extension and context paths remain at the project root. See the completed first task and the public distribution contract for the exact mapping.

## Previous phase

[Workflow system](../03-workflows/). Its remaining tasks are deferred until the ownership and migration boundaries in this phase are settled.
