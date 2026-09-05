---
id: ava-403
title: "Define GitHub release assets, trust modes, and channels"
status: "Done"
labels: ["internal", "roadmap", "phase-04"]
ordinal: 403
---

## Description

Define immutable, version-consistent release assets, distribution channels, and bootstrap trust modes. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Define GitHub Release Assets
description: Define immutable, version-consistent release assets, distribution channels, and bootstrap trust modes.
tags: [internal, roadmap, releases, distribution, security]
status: complete
phase: 4
order: 3
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T13:27:00+02:00
---

# Define GitHub Release Assets

The accepted public contract is documented in [Ava GitHub Release Assets](/distribution/releases.md). Its machine-readable release manifest is defined by [release.schema.json](/distribution/schemas/release.schema.json).

## Accepted decisions

- Canonical release tags are `v` followed by canonical Ava SemVer without build metadata.
- Stable releases use `/releases/latest/download/` and exact version-pinned URLs. Prereleases require exact tag selection.
- Development builds are revision-named GitHub Actions artifacts and are not supported release installation sources.
- Every stable and prerelease release publishes `ava-install.sh`, `ava-base.tar.gz`, `ava-guidance.tar.gz`, `ava-migrations.tar.gz`, `ava-release.json`, `ava-release-notes.md`, and `SHA256SUMS`.
- Guidance and migration archives remain present with explicit empty inventories when no entries apply.
- The tag, release manifest, installer, archive metadata, release notes, and GitHub release target must identify one Ava version and one full source revision.
- `ava-release.json` contains the asset inventory, source-to-installed mapping, compatibility declarations, and upgrade metadata. It does not contain its own checksum.
- `SHA256SUMS` covers every other uploaded Ava asset and avoids a self-checksum cycle.
- SHA-256 provides byte integrity after the expected digest is authenticated. Checksums from the same unverified release do not independently authenticate the publisher.
- Ava initially uses GitHub immutable release attestations as its authenticity mechanism rather than maintaining a second Sigstore key or project signing hierarchy.
- Convenience bootstrap trusts GitHub account, repository, TLS, and immutable release delivery before executing the installer.
- Verified bootstrap requires a pinned tag and verifies the GitHub release attestation and local installer asset before execution.
- Release assets are built twice from one clean source revision and must be reproducible before publication.
- Release automation assembles a draft, uploads and validates the complete asset set, then publishes once. Published assets and tags are never edited or reused.
- Repository release immutability must be enabled before the first publication and automation must verify the setting before release creation.
- Post-publication automation verifies immutable state, the release attestation, the tag target, the exact asset set, and every retained local asset.
- Stable and prerelease assets are retained indefinitely. Development artifacts follow Actions retention policy.

## Repository impact

- Added the public GitHub release asset and trust contract.
- Added a Draft 2020-12 JSON Schema for `ava-release.json`.
- Indexed the release contract and release schema.
- Recorded the conceptual release identity, integrity, authenticity, publication, and retention decisions.
- Advanced the active roadmap to the upgrade and migration protocol.

## Validation

The release schema was parsed with `python -m json.tool` and checked with `jsonschema` Draft 2020-12 validation.

Validation covered a valid release-candidate manifest, exact required asset names/order/media types, rejection of a prerelease declared stable, rejection of a wrong media type, and managed replacement/project-owned create-if-absent mapping rules.

The implementation and fixture tasks must automate the full publication and post-publication checks defined by the public contract.