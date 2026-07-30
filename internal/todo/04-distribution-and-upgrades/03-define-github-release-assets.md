---
type: Internal Development Task
title: Define GitHub Release Assets
description: Define immutable, version-consistent release assets, distribution channels, and bootstrap trust modes.
tags: [internal, roadmap, releases, distribution, security]
status: pending
phase: 4
order: 3
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Define GitHub Release Assets

## Define

- canonical release tag naming such as `v1.2.3`
- the stable latest-release URL and version-pinned URLs
- required assets, including installer, base bundle, integrity checksums, release manifest, change notes, upgrade guidance, and migrations
- asset filenames and content types
- how every asset declares or proves that it belongs to the same Ava version and source revision
- stable, prerelease, and development distribution channels
- the repository or organization configuration required to enable GitHub immutable releases for all published Ava releases
- how release automation verifies that a published release, its tag, and its assets are immutable rather than merely assuming immutability
- retention behavior and the relationship between immutable release settings, attestations, and the selected provenance model

## Bootstrap trust model

Define two distinct paths:

1. A convenience path that executes an immutable release installer directly and relies on GitHub repository, account, TLS, and release trust.
2. A verified path that downloads a pinned installer, verifies signed provenance or an attestation through a separately trusted mechanism, and only then executes it.

Checksums downloaded from the same release provide integrity checking but do not independently authenticate the bootstrap script or publisher. Do not describe checksums alone as solving the `curl | sh` trust problem.

Evaluate signed release manifests, GitHub artifact attestations, Sigstore, or another explicit authenticity mechanism. Keep the final mechanism minimal and document its trust assumptions.

## Convenience command shape

```sh
curl -fsSL https://github.com/phdah/ava/releases/latest/download/ava-install.sh | sh
```

```sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.2.3/ava-install.sh | sh
```

## Completion criteria

- define the complete release artifact contract
- define latest and pinned-version installation behavior
- reject mutable `main` assets as the recommended installation path
- define convenience and verified bootstrap flows separately
- document integrity, authenticity, trust assumptions, and failure behavior
- require GitHub immutable releases to be enabled before the first publication
- define an automated or repeatable verification that every published release is immutable
- define how release automation builds and attests all assets from one source revision