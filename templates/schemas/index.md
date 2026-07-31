# Distribution Schemas

Machine-readable schemas used by Ava release assembly, installation, upgrades, and validation.

- [Installed manifest schema](manifest.schema.json) - JSON Schema for the Ava-managed `/.ava/state/manifest.json` file.
- [Upgrade transaction schema](upgrade.schema.json) - JSON Schema for the Ava-managed `/.ava/state/upgrade.json` durable transaction journal.
- [Release manifest schema](release.schema.json) - JSON Schema for the immutable `ava-release.json` GitHub Release asset, including explicit upgrade edges and migration descriptors.
- [Upgrade guidance metadata schema](guidance.schema.json) - JSON Schema for parsed `UPGRADE.md` frontmatter in the Ava-managed guidance archive.
