---
type: Internal Development Task
title: Remove Empty Upgrade Transaction Containers
description: Ensure terminal installer cleanup removes the empty managed transaction container after its final upgrade transaction is deleted.
tags: [internal, roadmap, dogfood, release, installer, transactions, cleanup, blocker]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 6
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.7
generated:
  by: agent:openai-chatgpt
  at: 2026-08-06T10:49:13+02:00
---

# Remove Empty Upgrade Transaction Containers

## Observed behavior

A real project was installed with immutable `1.0.0-alpha.6` assets and then upgraded successfully to immutable `1.0.0-alpha.7` assets. The upgrade retained all 54 managed payload files, produced a terminal `complete` journal, advanced semantic compatibility through alpha.7, and permitted normal routing.

A subsequent Ava Maintenance integrity inspection nevertheless reported a final `FAIL` because the updater left an empty `./.ava/state/transactions/` directory. The directory was not an active transaction workspace and was not represented as a managed file in the manifest. Every recorded payload checksum, state envelope, semantic field, routing condition, and OpenCode permission check passed.

The installed conformance validator currently rejects unexpected files in managed payload roots but does not classify this empty structural directory as a conformance error. The remaining directory still creates an ambiguous managed-state artifact and causes a correctly cautious maintenance inspection to report a healthy installation as unhealthy.

## Reproduction and evidence

From a project without Ava installed:

```sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.0.0-alpha.6/ava-install.sh | sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.0.0-alpha.7/ava-install.sh | sh
```

The upgrade completes successfully and reports:

```text
SEMANTIC complete compatible_through=1.0.0-alpha.7 target=None
Installed Ava 1.0.0-alpha.7
```

After completion, `./.ava/state/transactions/` still exists as an empty directory.

An Ava Maintenance inspection then reports all recorded installation checks as passing but marks the unrecorded empty transaction container as unexpected content and returns `FAIL`.

## Classification

This is a `blocker` for the next prerelease. A terminal successful upgrade must leave a canonical, unambiguous managed state that Ava Maintenance can report as healthy. Installer-owned transaction storage must not remain after the last transaction has been removed.

The defect should be included in the same corrective prerelease cycle as the upgrade-coverage work in finding 05, but it remains a separate bounded implementation task.

## Root cause

For upgrades, the installer creates transaction workspaces beneath:

```text
./.ava/state/transactions/<transaction-id>/
```

After a semantic-complete upgrade, it removes the transaction-specific directory. The cleanup attempts to remove the now-empty parent only for fresh-install transaction storage under `.ava-install/`, not for upgrade transaction storage under `.ava/state/transactions/`. The parent therefore remains after its final child is deleted.

## Scope

- centralize terminal transaction cleanup so it removes the transaction-specific workspace first and then removes its parent only when the parent is empty
- apply the cleanup to successful upgrade completion and every terminal recovery path that deletes the final transaction workspace
- preserve the transaction container whenever another transaction entry or required recovery artifact remains
- keep active and blocked transaction state durable and inspectable
- avoid weakening manifest, journal, rollback, or filesystem-safety guarantees
- add regression coverage for successful upgrade cleanup and guarded parent removal

## Completion criteria

- a successful semantic-complete upgrade removes `./.ava/state/transactions/` when its final transaction workspace is deleted
- rollback, abort, and other terminal cleanup paths remove the container when they delete the final workspace
- active or blocked transactions retain their complete durable workspace
- a non-empty transaction container is never removed
- cleanup remains safe and idempotent when the parent is already absent
- regression tests cover successful cleanup, active-state preservation, and guarded removal of a non-empty parent
- a real upgrade using the corrective immutable prerelease leaves no empty transaction container and passes Ava Maintenance integrity inspection
- the finding index records the implementing PR, published version, and dogfood verification before this task is completed

## Resolution evidence

Pending implementation.
