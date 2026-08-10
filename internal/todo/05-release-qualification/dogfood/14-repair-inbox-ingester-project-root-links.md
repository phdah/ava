---
type: Internal Development Task
title: Repair Inbox Ingester project-root links
description: Fix Inbox Ingester references that incorrectly resolve the project-owned inbox beneath the managed role directory instead of the project root.
tags: [internal, roadmap, dogfood, inbox, roles, links, routing]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 14
classification: blocker
blocks: next-prerelease
affected_version: general managed Inbox Ingester role, exposed during alpha dogfooding
generated:
  by: agent:openai-chatgpt
  at: 2026-08-10T13:21:00+02:00
---

# Repair Inbox Ingester Project-Root Links

## Finding

During realistic recipe ingestion, the Inbox Ingester failed while loading its required context. The role attempted to read:

`/.ava/base/roles/inbox-ingester/inbox/index.md`

and stopped because that file does not exist.

The failure comes from `templates/base/roles/inbox-ingester/index.md`, which currently describes the project inbox through role-relative links such as `./inbox/` and requires `[Inbox convention](./inbox/index.md)`. Once assembled under `/.ava/base/roles/inbox-ingester/`, those references resolve beneath the managed role directory rather than to the project-owned root `inbox/` directory.

This makes a valid Inbox Ingester activation fail before ingestion can begin. The dogfood session confirmed that manually clarifying that the intended target is the project-root `inbox/` directory allows the interaction to continue.

## Expected fix

Make the Inbox Ingester reference the project-owned inbox through the canonical project-root path rather than a path relative to the managed role directory.

At minimum, review:

- `templates/base/roles/inbox-ingester/index.md`
- the assembled `/.ava/base/roles/inbox-ingester/index.md` representation
- link or conformance validation that should catch managed-role references resolving into nonexistent managed subdirectories

The fix should remain bounded to path resolution. Do not change Inbox Ingester ownership, ingestion semantics, or the project-owned status of `/inbox/` merely to repair the links.

## Completion criteria

- [ ] the Inbox Ingester overview resolves `inbox/` to the project-owned project-root directory
- [ ] required reading resolves the Inbox convention to the project-root `/inbox/index.md`, not `/.ava/base/roles/inbox-ingester/inbox/index.md`
- [ ] no managed Inbox Ingester instruction treats the project inbox as a child of the role directory
- [ ] assembled or installed-path validation covers the corrected references
- [ ] regression coverage fails if the role again tries to load `/.ava/base/roles/inbox-ingester/inbox/index.md`
- [ ] the Inbox Ingester can complete required reading in a conforming installed project with the standard project-owned inbox scaffold
- [ ] affected indexes, fixtures, and tests are aligned

## Release gate

This finding blocks the next prerelease because the published managed Inbox Ingester cannot reliably activate for its primary workflow while its required-reading path points to a nonexistent managed location.
