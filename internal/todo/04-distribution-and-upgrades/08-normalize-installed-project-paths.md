---
type: Internal Development Task
title: Normalize Installed Project Paths
description: Replace filesystem-root-looking references with an explicit project-root-relative path convention throughout installed Ava content and release tooling.
tags: [internal, roadmap, paths, portability, routing, installer]
status: completed
phase: 4
order: 8
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T16:35:00+02:00
---

# Normalize Installed Project Paths

The first local installation test showed that managed instructions such as `/.ava/base/shared/instructions/...` are interpreted by some hosts as absolute filesystem paths. The files exist at `.ava/...` below the selected project root, so the host first attempts to read the wrong location and only recovers after inspecting the project.

This task establishes one unambiguous path convention before the first release.

## Decision

- Agent-facing installed prose and metadata use an explicit `./` project-root prefix.
- A leading slash is invalid for a project-local reference in distributed prose or metadata.
- Document-relative Markdown links remain relative to the containing document.
- Typed release manifest, installed manifest, and upgrade journal path fields retain leading-slash root-anchored logical identifiers for deterministic tooling only.
- Host entrypoint metadata uses canonical `./...` paths.

The authoritative contract is [Ava Project-Root Path Conventions](../../../distribution/paths.md).

## Implementation

- normalized the managed router, role catalog, workflow catalog, shared instructions, workflows, roles, and project-owned scaffolds
- documented the distinction between agent-facing paths and machine-only path identifiers
- canonicalized installer host entrypoints as `./...` and rejected operating-system absolute paths
- added a release-source validator that rejects ambiguous leading-slash project references
- made release assembly and boundary validation run the path validator
- added root-router resolution, installer, manifest-stability, and regression fixtures

## Validation

The focused suite validates:

- the observed `/.ava/base/shared/instructions/upgrade-state-and-routing.md` regression
- resolution of every static project-root link in the managed root router
- rejection of ambiguous leading-slash references in fresh release sources
- acceptance of ordinary document-relative links
- preservation of machine manifest path identifiers
- canonical `./...` host entrypoint storage and absolute-path rejection

## Completion criteria

- [x] installed instructions never direct a conforming host to an operating-system root path
- [x] one documented `./...` convention is used across distributed agent-facing content
- [x] manifest path semantics are explicit and distinct from prose and host-tool paths
- [x] required root-router references resolve from the selected project root
- [x] fresh-install and upgrade sources reject reintroduction of ambiguous references
- [x] the release pipeline blocks assembly when the convention is violated
