---
type: Distribution Contract
title: Ava Project-Root Path Conventions
description: Defines project-root-relative prose references, machine manifest path identifiers, host entrypoint paths, and release validation requirements.
tags: [ava, distribution, paths, portability, manifests, hosts]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T20:30:00+02:00
---

# Ava Project-Root Path Conventions

This contract defines how Ava represents paths beneath an installed project's selected root.

Ava distinguishes paths intended for an agent or human to resolve from logical identifiers consumed only by deterministic release tooling. The forms are deliberately different so a host cannot mistake a project file for an operating-system absolute path.

# Agent-facing project paths

Installed Markdown, YAML metadata, role required reading, workflow references, provenance references, guidance prose, and host instructions use an explicit `./` prefix for paths rooted at the selected project:

```text
./AGENTS.md
./.ava/base/shared/instructions/upgrade-state-and-routing.md
./roles/index.md
./knowledge/domain/index.md
```

`./` always means the installed project root, not the directory containing the current document.

A leading slash is never valid for a project-local reference in distributed prose or metadata. `/AGENTS.md` and `/.ava/...` mean operating-system absolute paths and must not appear as instructions to a host file tool.

Normal Markdown links that are intentionally relative to the document containing them may continue to use forms such as `role.md`, `../index.md`, or `../../shared/example.md`. They are document-relative links, not canonical project paths.

# Manifest path identifiers

Release manifests, installed manifests, and upgrade journals use root-anchored logical path identifiers for deterministic filesystem operations:

```json
{
  "destination": "/.ava/base/roles/index.md"
}
```

These values:

- are identifiers inside a typed machine-readable field
- are always interpreted relative to the selected project root
- are never operating-system absolute paths
- must never be passed directly to an agent or host filesystem tool
- are normalized and joined to the selected target root by the installer
- reject empty segments, `.` segments, `..` segments, backslashes, NUL bytes, and root escapes

The leading slash is retained in these machine fields to distinguish root-anchored installed destinations from archive-relative paths. It does not define the prose convention.

Archive member paths, guidance archive paths, migration source paths, and similar asset-internal values remain normalized relative identifiers without either `/` or `./`.

# Host entrypoint metadata

`host_integration.entrypoint` is agent-facing project metadata and therefore uses the explicit project-root form:

```json
{
  "entrypoint": "./CODEX.md",
  "ownership": "project-owned",
  "discovery": "project-provided"
}
```

The installer accepts `CODEX.md` or `./CODEX.md` as input, records only the canonical `./CODEX.md` form, and rejects operating-system absolute paths. The entrypoint must remain outside `./AGENTS.md` and `./.ava/`.

# Release-source validation

Release assembly must reject distributed source content that contains an ambiguous leading-slash reference to a project path. Validation covers:

- the root router
- managed role and workflow sources
- managed shared instructions and indexes
- project-owned create-if-absent scaffolds

At minimum, validation rejects leading-slash references to `AGENTS.md`, `.ava`, `roles`, `workflows`, `shared`, `knowledge`, `inbox`, `index.md`, and `log.md`.

Fixtures must prove that:

- the root router uses `./.ava/base/shared/instructions/upgrade-state-and-routing.md`
- every static root-router reference resolves from the selected project root
- an ambiguous `/.ava/...` reference blocks release assembly
- fresh-install and upgrade payload sources cannot reintroduce the ambiguous form

# Reporting

User-facing installer plans and errors should print `./...` when describing a project path. Machine-readable manifest and journal output retains the field-specific identifier form defined above.
