---
type: Internal Development Task
title: Normalize Installed Project Paths
description: Replace filesystem-root-looking references with an explicit project-root-relative path convention throughout installed Ava content and release tooling.
tags: [internal, roadmap, paths, portability, routing, installer]
status: pending
phase: 4
order: 8
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T16:35:00+02:00
---

# Normalize Installed Project Paths

The first local installation test showed that managed instructions such as `/.ava/base/shared/instructions/...` are interpreted by some hosts as absolute filesystem paths. The files exist at `.ava/...` below the selected project root, so the host first attempts to read the wrong location and only recovers after inspecting the project.

This task must establish one unambiguous path convention before the first release.

## Decide and document

- define how Ava represents paths rooted at the installed project
- distinguish project-root-relative references from operating-system absolute paths
- decide whether canonical prose should use `.ava/...`, `./.ava/...`, or another explicit project-root notation
- distinguish human-facing instruction paths from manifest destinations and installer-internal normalized paths
- define whether a leading slash is ever valid in installed prose, metadata, indexes, role required reading, workflow references, provenance links, or guidance
- preserve portability across hosts whose file tools interpret leading slashes differently

## Implement

- audit all release payload sources for project paths beginning with `/`
- update the root `AGENTS.md`, managed role files, workflow files, shared instructions, indexes, and project-owned scaffolds to use the chosen convention
- update distribution contracts and examples so the convention is explicit
- review release manifest and installed manifest schemas separately from prose references, changing them only when their path semantics would otherwise be ambiguous
- update the installer, assembler, validators, and tests where they compare, emit, or consume installed paths
- ensure host-entrypoint metadata remains clearly project-root-relative without being mistaken for an operating-system path
- add fixtures proving that a newly installed project can resolve every required-reading path directly from the project root without a failed absolute-path attempt
- add a regression fixture based on the observed `/.ava/base/shared/instructions/upgrade-state-and-routing.md` failure

## Completion criteria

- installed instructions never cause a conforming host to interpret project files as filesystem-root files
- one documented project-root path convention is used consistently across all distributed content
- manifest path semantics are explicit and cannot be confused with prose or host-tool paths
- every required role, workflow, instruction, state, and provenance reference resolves from the selected project root
- fresh-install and upgrade fixtures reject reintroduction of ambiguous leading-slash references
- the first release remains blocked until the convention is implemented and validated
