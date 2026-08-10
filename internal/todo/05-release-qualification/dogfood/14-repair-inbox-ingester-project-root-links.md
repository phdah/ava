---
type: Internal Development Task
title: Repair Inbox Ingester project-root links
description: Fix Inbox Ingester references that incorrectly resolve the project-owned inbox beneath the managed role directory instead of the project root.
tags: [internal, roadmap, dogfood, inbox, roles, links, routing]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 14
classification: blocker
blocks: next-prerelease
affected_version: general managed Inbox Ingester role, exposed during alpha dogfooding
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T13:21:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-10T14:12:32+02:00
---

# Repair Inbox Ingester Project-Root Links

## Finding

During realistic recipe ingestion, the Inbox Ingester failed while loading its required context. The role attempted to read:

`/.ava/base/roles/inbox-ingester/inbox/index.md`

and stopped because that file does not exist.

The failure came from `templates/base/roles/inbox-ingester/index.md`, which described the project inbox through Markdown links such as `./inbox/` and required `[Inbox convention](./inbox/index.md)`. Ava's path contract defines `./...` as project-root-relative for agent-facing project paths, but ordinary Markdown link resolution from the nested managed role directory made the host treat those targets as role-relative.

This made a valid Inbox Ingester activation fail before ingestion could begin. The dogfood session confirmed that manually clarifying that the intended target was the project-root `./inbox/` directory allowed the interaction to continue.

## Implemented fix

The Inbox Ingester now states the project-owned inbox and required inbox convention as explicit project-root paths in prose rather than encoding them as nested Markdown link targets. Required reading names `./inbox/index.md` directly and explicitly says not to resolve it relative to the Inbox Ingester role directory.

The change remains bounded to path resolution. Inbox ownership, ingestion semantics, and the project-owned status of `./inbox/` are unchanged.

## Completion criteria

- [x] the Inbox Ingester overview resolves `inbox/` to the project-owned project-root directory
- [x] required reading resolves the Inbox convention to project-root `./inbox/index.md`, not `/.ava/base/roles/inbox-ingester/inbox/index.md`
- [x] no managed Inbox Ingester instruction treats the project inbox as a child of the role directory
- [x] assembled or installed-path validation covers the corrected references
- [x] regression coverage fails if the role again expresses the project inbox through the broken nested Markdown-link shape
- [x] the Inbox Ingester can complete required reading in a conforming installed project with the standard project-owned inbox scaffold
- [x] affected indexes, fixtures, and tests are aligned

## Resolution evidence

The resolving change:

- replaces the Inbox Ingester's `./inbox/` and `./inbox/index.md` Markdown links with explicit project-root path instructions in `templates/base/roles/inbox-ingester/index.md`
- keeps ordinary document-relative links for managed role files and the managed role registry
- extends `internal/release/tests/test_installed_paths.py` to inspect the assembled payload mapping for `/.ava/base/roles/inbox-ingester/index.md`
- asserts that the assembled role names project-root `./inbox/index.md`, does not contain the broken `](./inbox/` link shape, includes the standard project-owned `/inbox/index.md` scaffold destination, and never creates `/.ava/base/roles/inbox-ingester/inbox/index.md`
- uses the existing `internal.release.tests.test_installed_paths` suite entry, so the regression runs as part of `internal/release/test.sh`

Published installed-project confirmation remains a release qualification gate and does not keep this repository implementation task pending.

## Release gate

The repository blocker is resolved. The next prerelease still remains blocked by any other pending blocker in the dogfood backlog, currently finding 15.
