---
type: Internal Development Task
title: Repair Installed Context Link Resolution
description: Ensure every managed role and base link resolves against the installed project layout rather than the repository source layout.
tags: [internal, roadmap, dogfood, release, links, validation, blocker]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 2
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-05T13:07:09+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-05T15:07:14+02:00
---

# Repair Installed Context Link Resolution

## Observed behavior

The Inbox Ingester completed a real ingestion run even though its required-reading manifest contains a link that cannot resolve in an installed alpha.5 project. Strict role activation should have stopped before ingestion rather than guessing, substituting, or skipping mandatory context.

## Reproduction and evidence

In the alpha.5 installation at `~/stuff/project-vault/`, `/.ava/base/roles/inbox-ingester/index.md` links the required inbox convention as `../../inbox/index.md`. From the installed role directory this resolves to the nonexistent managed path `/.ava/base/inbox/index.md`; the actual project-owned convention is `/inbox/index.md`.

The source link resolves inside `templates/base/` only because that repository source tree contains `templates/base/inbox/`. Release assembly maps the managed base and project-owned inbox scaffold to different installed roots without rewriting or rejecting the source-layout-relative link.

Related contextual links that target `../../AGENTS.md` from managed role directories also resolve beneath `/.ava/base/` rather than to the installed root router. The resolving work must inspect the complete assembled base rather than fixing only the first observed link.

## Classification

This is a `blocker`. Broken required-reading links invalidate deterministic role activation and permit agents to act without the complete mandatory instruction set. The next prerelease and every later release gate are blocked until assembled installed-project links are valid and covered by release qualification.

## Root cause

Managed documents retain links authored for the repository source layout even when release assembly places their targets at different installed destinations. Current qualification does not resolve every required and contextual managed link against the assembled installed tree.

## Scope

- define installed-project-relative targets for links that cross managed and project-owned roots
- correct every affected managed document, not only the observed Inbox Ingester link
- validate required-reading and applicable contextual links against the assembled release tree
- keep project-owned scaffold links and managed payload ownership separate
- make release qualification fail before publication when an assembled managed link is unresolved

## Completion criteria

- every required-reading link in an assembled release resolves to its intended installed path
- managed contextual links to the root router, registries, inbox convention, and other cross-root targets resolve correctly
- release validation rejects the alpha.5 broken-link shape
- regression fixtures cover source paths whose installed destinations differ from their repository locations
- a project installed from the corrected published prerelease can load the complete Inbox Ingester required-reading chain without path substitution
- the finding index records the implementing PR, published version, and real installed-project validation before this task is completed

## Resolution evidence

Repository implementation and local qualification are complete in the current worktree:

- all 15 links that failed against the assembled alpha.5 layout now use installed-project targets or no longer link to repository-only contracts
- `assemble.py` resolves every distributed local inline Markdown link through the complete payload destination map before writing release assets
- both project-root and document-relative traversal beyond the selected project are rejected
- repository conformance reports unresolved installed targets as `AVA-INSTALLED-LINK-MISSING`
- the `installed-link-missing` fixture reproduces the source-resolving alpha.5 Inbox Ingester defect and proves that `./inbox/index.md` resolves through the project-owned scaffold mapping
- the `installed-link-root-escape` fixture rejects excess document-relative traversal and `./../` project-root traversal while accepting an exact document-relative path to the root router
- `internal/release/test.sh` passes all 129 tests
- `internal/release/validate-boundaries.sh` reports `Repository boundaries valid.`
- a local `1.0.0-alpha.1` assembly completed, installed into a clean temporary project, passed installed conformance with normal routing permitted, and contained the complete Inbox Ingester required-reading file set

The finding remains pending until an implementing PR is recorded, a corrected prerelease is published, and the Inbox Ingester required-reading chain is validated in a real project installed from that immutable release. The implementing PR and published version are not yet available.
