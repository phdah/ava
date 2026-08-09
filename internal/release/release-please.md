---
type: Internal Release Procedure
title: Ava Release Automation
description: Defines release-please version proposals, release-local edge completion, recursive qualification, and immutable publication.
tags: [internal, releases, automation, release-please, conventional-commits]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-09T17:50:00+02:00
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

A newly created release PR is intentionally incomplete. Its policy check remains red until one target release record exists and passes recursive chain validation.

The maintainer completes it by creating only:

```text
internal/release/catalogs/<target>.json
```

That file contains exactly one `<previous> -> <target>` edge, only guidance and migrations introduced by that edge, and any source-retirement decisions made by the target release. Earlier release records remain untouched.

The gate validates:

- target and channel identity
- exactly one target release record changed relative to the release PR base
- the edge starts at the immediately previous release
- the record contains only transition-local guidance and migration references
- guidance metadata, digest, and artifact integrity
- explicit, valid source-retirement decisions
- recursive continuity through every intermediate release record
- unique composed paths for every retained source

`upgrade-impact.json`, `upgrade-sources.txt`, cumulative catalog snapshots, and published direct edges are not current authoring inputs.

## Assembly and publication

The release workflow sets:

```text
AVA_UPGRADE_CATALOG=internal/release/catalogs/<target>.json
```

The reviewed assembler follows `edge.from` recursively through earlier release records, stages the guidance referenced by those edges, and derives installer-compatible projections for each retained source. The cumulative graph exists only during validation and assembly.

After merge, automation verifies the exact tag and source SHA, proves that only the target record was added, reruns recursive chain validation and the complete repository suite, assembles twice, compares digests, validates conformance, attests assets, uploads without clobbering, and publishes the existing draft.

The same release-local record rule applies to alpha, beta, release candidate, stable, patch, minor, and major releases.
