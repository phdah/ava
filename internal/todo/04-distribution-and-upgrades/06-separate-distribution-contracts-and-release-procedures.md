---
type: Internal Development Task
title: Separate Distribution Contracts and Release Procedures
description: Separate public distribution contracts, release payload sources, and maintainer-only publication procedures.
tags: [internal, roadmap, distribution, releases, repository-structure]
status: complete
phase: 4
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Separate Distribution Contracts and Release Procedures

This task establishes a repository boundary without changing installed paths, ownership classes, versioning, trust, upgrade behavior, or semantic guidance.

## Implemented structure

```text
/
├── distribution/        # public contracts and schemas
├── templates/           # release payload and scaffold sources only
└── internal/release/    # maintainer-only publication procedures
```

Public contracts now use concise canonical paths:

- `/distribution/ownership.md`
- `/distribution/versioning.md`
- `/distribution/releases.md`
- `/distribution/upgrades.md`
- `/distribution/guidance.md`
- `/distribution/schemas/`

## Accepted boundaries

- Public distribution contracts are repository-level authority but are not automatically installed into projects.
- Release assembly includes only paths explicitly declared by the release manifest.
- `/templates/` contains authored managed payload and create-if-absent scaffold sources, not public release policy or internal procedures.
- `/internal/release/` coordinates maintainers around approval and publication while deterministic automation owns assembly, validation, integrity, attestation, and immutable publication mechanics.
- No file under `/internal/` may be included in a release payload or required by installed Ava behavior.
- Existing installed path, ownership, compatibility, trust, and upgrade contracts remain unchanged.

## Repository changes

- Moved and renamed public distribution contracts from `/templates/` into `/distribution/`.
- Moved public JSON Schemas into `/distribution/schemas/` and updated their canonical `$id` values.
- Reduced `/templates/` navigation to release payload and scaffold sources under `/templates/base/`.
- Added maintainer publication guidance and a POSIX repository-boundary validator under `/internal/release/`.
- Updated repository, template, task, and public-contract links to canonical paths.
- Updated root and internal conceptual logs and advanced the roadmap.

## Validation

`internal/release/validate-boundaries.sh` checks:

- required public contracts and schemas exist
- obsolete template contract locations are absent
- `/templates/` has no unexpected direct children
- schema identifiers use canonical `/distribution/schemas/` paths
- current repository files contain no stale template-contract references
- release source files do not depend on internal repository content

The next task is [Implement Installer and Updater](07-implement-installer-and-updater.md).
