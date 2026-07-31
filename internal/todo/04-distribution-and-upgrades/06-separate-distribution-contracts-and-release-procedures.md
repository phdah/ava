---
type: Internal Development Task
title: Separate Distribution Contracts and Release Procedures
description: Separate public distribution contracts, release payload sources, and internal maintainer release procedures into explicit repository boundaries.
tags: [internal, roadmap, distribution, structure, releases, maintainers]
status: pending
phase: 4
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T14:09:00+02:00
---

# Separate Distribution Contracts and Release Procedures

## Goal

Make the repository structure express three distinct responsibilities:

1. public contracts that define what a valid Ava distribution is
2. authored source material that is assembled into release payloads
3. internal procedures used by the Ava Internal Maintainer and release automation to build and publish releases

This is a repository-source reorganization. It must not change the accepted installed-project path, ownership, versioning, compatibility, trust, or upgrade contracts.

## Target structure

Use this structure unless implementation reveals a material conflict:

```text
/
├── distribution/
│   ├── index.md
│   ├── ownership.md
│   ├── versioning.md
│   ├── releases.md
│   └── schemas/
│       ├── index.md
│       ├── manifest.schema.json
│       └── release.schema.json
├── templates/
│   ├── index.md
│   └── base/
└── internal/
    ├── index.md
    ├── release/
    │   ├── index.md
    │   └── procedure.md
    └── roles/ava-internal/
```

The exact internal release-procedure filenames may be refined when the publication workflow is implemented, but their authority boundary must remain explicit.

## Responsibility boundaries

### Public distribution contracts

`/distribution/` contains authoritative repository-level contracts and machine-readable schemas that define:

- installed ownership and source-to-installed mapping
- Ava SemVer and compatibility state
- GitHub Release identity, assets, channels, integrity, authenticity, and retention
- release and installed-state schemas

These files are public Ava contracts but are not automatically installed into projects. Release assembly includes only files explicitly declared by the release manifest.

### Release payload sources

`/templates/` contains only authored source material intended for release assembly, including:

- Ava-managed router and base context
- default roles, workflows, and shared instructions
- create-if-absent project scaffolds
- selected host bootstrap source files when introduced

Repository location alone must still never imply installed destination or ownership.

### Internal release procedures

`/internal/release/` contains repository-only operating instructions for:

- the Ava Internal Maintainer's release responsibilities
- preparation and approval boundaries
- invoking and supervising release automation
- required pre-publication and post-publication verification
- failure, correction, and recovery procedures
- repository settings and permissions required for publication

The Ava Internal Maintainer coordinates release work and maintains the contracts. GitHub Actions or equivalent deterministic automation builds, validates, attests, and publishes assets. Internal procedures are never distributed to installed Ava projects.

## Implement

- create the top-level `/distribution/` index and schema index
- move the distribution ownership, versioning, and GitHub release asset contracts from `/templates/` into `/distribution/`
- move release and installed-state schemas from `/templates/schemas/` into `/distribution/schemas/`
- reduce `/templates/` to release payload and scaffold source material
- add `/internal/release/` navigation and a bounded maintainer-facing publication procedure
- update root, template, internal, roadmap, README, contract, schema `$id`, and cross-document links
- update release assembly and validation references to use the new authoritative paths
- verify no internal procedure is included in release payloads
- verify public contracts are not installed merely because they live outside `/internal/`
- preserve Git history through file moves where practical

## Completion criteria

- `/distribution/` is the clear authoritative home for public distribution contracts and schemas
- `/templates/` contains only release payload or create-if-absent scaffold sources
- `/internal/release/` contains maintainer and automation publication procedures only
- the Ava Internal Maintainer remains responsible for coordinating release creation without making the public release format an internal implementation detail
- all indexes enumerate only direct children and all links resolve
- schema identifiers and documentation reference the new canonical paths
- release assembly includes content only through explicit manifest mapping
- installed-project paths and ownership semantics remain unchanged
- no `/internal/` content can enter a release bundle
- validation covers the repository boundary between contracts, payload sources, and internal procedures
