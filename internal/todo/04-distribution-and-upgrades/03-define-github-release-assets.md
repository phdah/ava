---
type: Internal Development Task
title: Define GitHub Release Assets
description: Define immutable, version-consistent GitHub Release assets and stable or prerelease channels.
tags: [internal, roadmap, releases, distribution]
status: pending
phase: 4
order: 3
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T11:26:00Z
---

# Define GitHub Release Assets

## Define

- canonical release tag naming such as `v1.2.3`
- the stable latest-release URL and version-pinned URLs
- required assets, including installer, base bundle, checksums, release manifest, change notes, upgrade guidance, and migrations
- asset filenames and content types
- how every asset declares or proves that it belongs to the same Ava version
- stable, prerelease, and development distribution channels
- signing or checksum requirements
- retention and immutability expectations

## Proposed command shape

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
- document verification and failure behavior
- define how release automation builds all assets from one source revision
