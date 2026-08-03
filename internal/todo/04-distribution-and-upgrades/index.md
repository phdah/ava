# Phase 04: Versioned Distribution and Upgrades

Define and implement Ava as an immutable, versioned context distribution installed and upgraded through thin release tooling.

## Tasks

1. [x] [Define the distribution and ownership boundary](01-define-distribution-and-ownership-boundary.md)
2. [x] [Define the Ava SemVer and compatibility contract](02-define-semver-and-compatibility.md)
3. [x] [Define GitHub release assets, trust modes, and channels](03-define-github-release-assets.md)
4. [x] [Define the upgrade and migration protocol](04-define-upgrade-and-migration-protocol.md)
5. [x] [Define release guidance and the Upgrade Role](05-define-release-logs-and-agent-guidance.md)
6. [x] [Separate distribution contracts and release procedures](06-separate-distribution-contracts-and-release-procedures.md)
7. [x] [Implement the installer and updater](07-implement-installer-and-updater.md)
8. [ ] [Implement validation, conformance, and upgrade fixtures](08-implement-validation-and-upgrade-fixtures.md)
9. [ ] [Publish the first versioned Ava release](09-publish-first-versioned-release.md)

Task 7 implemented deterministic release assembly and a thin manifest-driven installer and updater. It provides explicit source mapping, checksum and archive validation, safe project adoption, direct declared upgrades, transactional managed-file replacement, migration execution, semantic upgrade state, and smoke coverage.

The accepted distribution boundary places managed content under `/AGENTS.md` and `/.ava/`, while project-owned extension and context paths remain at the project root. Installed `ava_version` remains separate from project-owned semantic compatibility.

## Current active task

[Implement validation, conformance, and upgrade fixtures](08-implement-validation-and-upgrade-fixtures.md).
