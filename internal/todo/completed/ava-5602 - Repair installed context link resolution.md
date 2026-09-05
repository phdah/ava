---
id: ava-5602
title: "Repair installed context link resolution"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5602
---

## Description

Ensure every managed role and base link resolves against the installed project layout rather than the repository source layout. This native Backlog.md task preserves the finding, implementation, and qualification evidence.

## Migrated task record

---
type: Internal Development Task
title: Repair Installed Context Link Resolution
description: Ensure every managed role and base link resolves against the installed project layout rather than the repository source layout.
tags: [internal, roadmap, dogfood, release, links, validation, blocker]
status: completed
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
  at: 2026-08-06T10:49:13+02:00
---

# Repair Installed Context Link Resolution

## Observed behavior

The Inbox Ingester completed a real ingestion run even though its required-reading manifest contained a link that could not resolve in an installed alpha.5 project. Strict role activation should have stopped before ingestion rather than guessing, substituting, or skipping mandatory context.

## Reproduction and evidence

In the alpha.5 installation at `~/stuff/project-vault/`, `/.ava/base/roles/inbox-ingester/index.md` linked the required inbox convention as `../../inbox/index.md`. From the installed role directory this resolved to nonexistent `/.ava/base/inbox/index.md`; the actual project-owned convention was `/inbox/index.md`.

The source link resolved inside `templates/base/` only because that repository source tree contained `templates/base/inbox/`. Release assembly mapped the managed base and project-owned inbox scaffold to different installed roots without rewriting or rejecting the source-layout-relative link.

Related contextual links targeting `../../AGENTS.md` from managed role directories also resolved beneath `/.ava/base/` rather than to the installed root router. The work therefore had to inspect the complete assembled base rather than fix only the first observed link.

## Classification

This was a `blocker`. Broken required-reading links invalidate deterministic role activation and permit agents to act without the complete mandatory instruction set. The next prerelease and later release gates were blocked until assembled installed-project links were valid and covered by release qualification.

## Root cause

Managed documents retained links authored for the repository source layout even when release assembly placed their targets at different installed destinations. Qualification did not resolve every required and contextual managed link against the assembled installed tree.

## Scope

- define installed-project-relative targets for links crossing managed and project-owned roots
- correct every affected managed document
- validate required-reading and applicable contextual links against the assembled release tree
- keep project-owned scaffold links and managed payload ownership separate
- make release qualification fail before publication when an assembled managed link is unresolved

## Completion criteria

- every required-reading link in an assembled release resolves to its intended installed path
- managed contextual links to the root router, registries, inbox convention, and other cross-root targets resolve correctly
- release validation rejects the alpha.5 broken-link shape
- regression fixtures cover source paths whose installed destinations differ from repository locations
- a corrected published prerelease can load the complete Inbox Ingester required-reading chain without substitution
- implementing PR, published version, and real installed-project validation are recorded

## Resolution evidence

Repository implementation and local qualification were completed in PR #53. All 15 links that failed against the assembled alpha.5 layout were corrected or decoupled from repository-only contracts. `assemble.py` resolves distributed local inline Markdown links through the complete payload destination map before writing assets, root/path escapes are rejected, repository conformance reports `AVA-INSTALLED-LINK-MISSING`, regression fixtures reproduce the alpha.5 shape and path traversal cases, `internal/release/test.sh` passed all 129 tests, boundary validation passed, and a local assembled install passed conformance with the complete Inbox Ingester required-reading set.

Immutable published validation completed on 2026-08-06 against `1.0.0-alpha.7`, released from revision `8a23c44233572585b93ee56ac408fdc5c7227d0c` through PR #57. A real project was installed from alpha.6 and upgraded to alpha.7, retained all 54 managed payload files, advanced installed and semantic compatibility state, preserved project-owned OpenCode configuration, and allowed normal routing. The agent activated Inbox Ingester normally and all seven required-reading links resolved and loaded in order. The inbox convention resolved to `./inbox/index.md`, root router to `./AGENTS.md`, managed role registry to `./.ava/base/roles/index.md`, and shared contracts under `./.ava/base/shared/instructions/`, with no repository-source substitution, guessing, inbox processing, or mutation.

The separate empty transaction-container cleanup defect discovered during accompanying Ava Maintenance inspection is preserved as AVA-5606 and does not invalidate this finding.