# Distribution Sources

Files under this directory are repository source material for Ava releases. They are not copied verbatim into an installed project, and their repository paths do not determine installed ownership.

## Contents

- [Distribution and ownership contract](distribution-and-ownership.md) - Installed path layout, ownership classes, source-to-installed mapping, adoption, collision, and bootstrap rules.
- [Versioning and compatibility contract](versioning-and-compatibility.md) - Ava SemVer, installed manifest state, semantic compatibility, upgrade-path compatibility, deprecation, and support guarantees.
- [GitHub release assets contract](github-release-assets.md) - Immutable release identity, required assets, channels, checksums, attestations, bootstrap trust modes, publication, verification, and retention.
- [Upgrade and migration protocol](upgrade-and-migration.md) - Explicit upgrade edges, three-way managed reconciliation, durable transaction state, deterministic migration ordering, rollback, and managed upgrade routing.
- [Release guidance contract](release-guidance.md) - Installed `UPGRADE.md` metadata, semantic obligations, decisions, composition, completion, and Upgrade Role discovery.
- [Distribution schemas](schemas/) - Machine-readable schemas for installed state, release metadata, upgrade transactions, and release guidance metadata.
- [Current base format source](base/) - Authored roles, workflows, shared instructions, and project-format examples used while release assembly is being implemented.

The release assembler must map source files to explicit installed destinations and ownership classes. In particular, the installed project uses a managed `/.ava/` namespace plus project-owned extension paths; it does not reproduce this repository's `/templates/` hierarchy.

Repository-development instructions under `/internal/` are never part of generated or installed project content.
