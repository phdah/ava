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
8. [x] [Normalize installed project paths](08-normalize-installed-project-paths.md)
9. [x] [Implement OpenCode support and decide managed directory discoverability](09-implement-opencode-host-support.md)
10. [x] [Implement validation, conformance, and upgrade fixtures](10-implement-validation-and-upgrade-fixtures.md)

Task 7 implements deterministic release assembly and one thin POSIX installer/updater with embedded structured-data handling. It supports fresh installation, explicit adoption, direct and chained upgrades, three-way managed reconciliation, restricted deterministic migrations, durable recovery, semantic upgrade blocking, and project-owned host entrypoint metadata.

Task 8 establishes `./...` as the canonical agent-facing project-root path form, preserves typed machine path identifiers for deterministic tooling, canonicalizes host entrypoint metadata, and blocks ambiguous leading-slash references during release validation.

Task 9 keeps `./.ava/` as the hidden managed directory and adds a minimal project-owned OpenCode configuration by default. The installer supports `--host none`, never overwrites existing OpenCode configuration, continues installation when configuration already exists, and prints the required manual merge block.

Task 10 adds the unified repository, installed-project, and release-asset conformance validator, stable machine-readable findings, explicit normal-routing gates, immutable-publication checks, installer failure fixtures, and the complete v1 conformance matrix.

## Status

Phase 4 is complete. Release tooling, installed-state maintenance, OpenCode support, semantic upgrade separation, and conformance qualification are ready for prerelease policy and alpha publication.

## Next phase

[V1 release qualification](../05-release-qualification/).
