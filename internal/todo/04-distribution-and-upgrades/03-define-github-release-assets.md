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
- Every stable and prerelease release publishes `ava-install.sh`, `ava-base.tar.gz`, `ava-guidance.tar.gz`, `ava-migrations.tar.gz`, `ava-release.json`, `ava-release-notes.md`, and `SHA256SUMS`.
- The tag, release manifest, installer, archive metadata, release notes, and GitHub release target identify one version and source revision.
- `ava-release.json` contains asset inventory, source-to-installed mapping, compatibility declarations, and upgrade metadata.
- SHA-256 provides byte integrity after the expected digest is authenticated.
- Ava initially uses GitHub immutable release attestations as its authenticity mechanism.
- Convenience bootstrap trusts GitHub delivery before execution. Verified bootstrap validates a pinned immutable release and installer asset first.
- Release assets are built twice from one clean source revision and must be reproducible.
- Release automation publishes a validated draft once. Published assets and tags are never edited or reused.
- Stable and prerelease assets are retained indefinitely.

## Repository impact

The public release contract and schema are indexed under `/distribution/`. Maintainer coordination is documented separately under `/internal/release/`.

## Validation

The release schema was parsed and checked as Draft 2020-12, including asset identity, channel consistency, media types, and installed ownership mapping.
