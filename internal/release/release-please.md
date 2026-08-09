---
type: Internal Release Procedure
title: Ava Release Automation
description: Defines release-please version proposals, one-edge catalog completion, qualification, and immutable publication.
tags: [internal, releases, automation, release-please, conventional-commits]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T17:30:00+02:00
---

# Ava Release Automation

Ava uses release-please as a single-package coordinator. It proposes versions, updates `CHANGELOG.md`, `version.txt`, and the release manifest, creates immutable tags and draft releases, and publishes only after every maintained gate succeeds.

## Merge-boundary contract

Ordinary pull request titles use:

```text
<type>(<optional-scope>)!: <subject>
```

Releasable types are `feat`, `fix`, `perf`, and `revert`. Other supported types are internal-only unless marked breaking.

Ordinary implementation PRs do not predeclare a release version or upgrade edge.

## Release PR contract

A newly created release PR is intentionally incomplete. Its policy check remains red until the target catalog exists and passes strict delta validation.

The maintainer completes it by inheriting `internal/release/catalogs/<previous>.json` and adding exactly one `<previous> -> <target>` edge. `internal/release/catalog-retirements.json` records any explicit supported-source retirement.

The gate validates:

- target and channel identity
- immutable inheritance of all prior edges and guidance
- exactly one new adjacent edge
- no skipped, shortcut, cumulative, or non-adjacent edge
- no inherited edge, migration reference, guidance metadata, digest, or artifact mutation
- no cumulative guidance copied from an older transition
- retained supported sources and explicit retirements
- unique composed paths for every retained source

`upgrade-impact.json` and `upgrade-sources.txt` are not current authoring inputs.

## Assembly and publication

The release workflow sets:

```text
AVA_UPGRADE_CATALOG=internal/release/catalogs/<target>.json
```

The reviewed assembler stages only catalog-referenced guidance and derives installer-compatible projections from each retained source through the canonical adjacent graph.

After merge, automation verifies the exact tag and source SHA, reruns catalog validation and the complete repository suite, assembles twice, compares digests, validates conformance, attests assets, uploads without clobbering, and publishes the existing draft.

The same catalog rule applies to alpha, beta, release candidate, stable, patch, minor, and major releases.
