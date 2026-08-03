---
type: Internal Development Task
title: Define Distribution and Ownership Boundary
description: Define Ava as a file distribution and separate Ava-managed base content from project-owned context.
tags: [internal, roadmap, distribution, ownership]
status: complete
phase: 4
order: 1
generated:
  by: agent:openai-chatgpt
  at: 2026-07-31T11:16:00+02:00
---

# Define Distribution and Ownership Boundary

The accepted public contract is documented in [Ava Distribution and Ownership Boundary](/distribution/ownership.md).

## Accepted decisions

- Ava uses exactly two ownership classes: Ava-managed and project-owned.
- Distribution ownership controls release lifecycle, manifest membership, and automatic replacement. It does not define exclusive edit rights.
- Active Ava roles and workflows are expected to maintain project-owned context within their capabilities, constraints, current instructions, and user-approved task scope.
- Editing a file does not change its ownership class.
- The repository source layout and installed-project layout are intentionally different.
- Repository source paths do not determine installed ownership.
- `/AGENTS.md` is the Ava-managed canonical router.
- `/.ava/base/` contains managed default roles, workflows, shared instructions, and base navigation.
- `/.ava/state/manifest.json` is the stable managed-file ownership and installed-version record.
- `/.ava/state/upgrade.json` is the stable active-upgrade state location.
- `/.ava/guidance/` contains release-specific managed upgrade guidance.
- `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, `/inbox/`, `/index.md`, and `/log.md` are project-owned extension and context paths when present.
- Project-owned files may predate installation, be created by create-if-absent scaffolding, or be added later.
- Managed-file customization is prohibited. Checksum mismatches are reported as conflicts and are never silently overwritten or reclassified.
- Project-specific behavior must be expressed in project-owned extension paths rather than by editing managed files.
- Host-specific bootstrap files are optional thin Ava-managed pointers to `/AGENTS.md`, never independent routers or a third ownership class.
- Hosts without validated automatic discovery use an explicit instruction to load `/AGENTS.md`; unsupported discovery behavior is reported rather than guessed.
- Existing projects are adopted through explicit path classification and collision resolution. Installation never silently claims, replaces, relocates, or merges pre-existing files.
- Pre-existing root files and standard extension directories remain project-owned by default.
- A pre-existing `/AGENTS.md`, an unrecognized `/.ava/`, a conflicting host bootstrap, or a modified managed file aborts automatically unless an explicit adoption, recovery, or migration decision resolves the exact path.
- Existing unversioned Ava projects require an explicit migration from mixed root defaults into the managed `/.ava/base/` namespace while preserving project-specific content.
- MCP servers, persistent runtimes, feature-rich CLIs, workspace-provider layers, and application services are not part of the ownership or installation boundary.

## Repository impact

The public contract now lives under `/distribution/`, release payload and scaffold sources remain under `/templates/base/`, and maintainer-only release procedures live under `/internal/release/`. The repository still does not resemble an installed project, and release assembly must map every source explicitly.

## Validation

The contract covers exact installed ownership paths, routing and extension discovery, manifest authority, managed-file conflicts, installation and adoption, unversioned migration, host discovery, and source-to-installed mapping.

The incompatible public path decision was approved by the user before implementation.
