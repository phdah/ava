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
8. [ ] [Normalize installed project paths](08-normalize-installed-project-paths.md)
9. [ ] [Decide managed directory discoverability](09-decide-managed-directory-discoverability.md)
10. [ ] [Implement validation, conformance, and upgrade fixtures](10-implement-validation-and-upgrade-fixtures.md)
11. [ ] [Publish the first versioned Ava release](11-publish-first-versioned-release.md)

Task 7 implements deterministic release assembly and one thin POSIX installer/updater with embedded structured-data handling. It supports fresh installation, explicit adoption, direct and chained upgrades, three-way managed reconciliation, restricted deterministic migrations, durable recovery, semantic upgrade blocking, and project-owned host entrypoint metadata.

The focused implementation suite covers clean installation, create-if-absent preservation, managed conflicts, checksum failures, unsafe archives, symlink escapes, project-provided host entrypoints, migration execution, chained upgrades, semantic state, and rollback.

Local installation testing exposed two pre-release portability questions: installed instructions use leading-slash paths that some hosts interpret as filesystem-root paths, and hidden `.ava/` reads may require host-specific permission confirmation. Tasks 8 and 9 resolve those issues before the broader conformance matrix in task 10 and publication in task 11.

## Current active task

[Normalize installed project paths](08-normalize-installed-project-paths.md).
