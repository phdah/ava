---
type: Internal Development Task
title: Preserve Existing Scoped History During Ingestion
description: Prevent Inbox Ingester operations from deleting or rewriting pre-existing scoped history while still allowing a required new history entry to be appended.
tags: [internal, roadmap, dogfood, inbox, history, roles, trust]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 16
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:opencode
  at: 2026-08-13T12:18:45+02:00
---

# Preserve Existing Scoped History During Ingestion

## Observed behavior

During alpha dogfooding in `~/stuff/project-vault`, commit `81b0ec4` ingested the first synthetic source batch and replaced the existing `knowledge/log.md`. The removed entries described the prior trusted context. The user had intentionally deprecated that context while preparing a clean ingestion project, but its remaining history cleanup occurred inside the Inbox Ingester operation rather than through separate Project Steward maintenance or deterministic fixture reset.

The resulting project state was user-authorized, but the execution boundary was unsafe. Ingestion should not use source processing as an opportunity to delete or rewrite pre-existing scoped history.

## Reproduction and evidence

The reviewed dogfood range was `81b0ec4^..daebe0a` in `~/stuff/project-vault` under OpenCode session `ses_013a8f7dcffefRLIh6m6uEAgvX`.

In commit `81b0ec4`:

- `knowledge/log.md` was reduced from 59 lines to five lines
- prior personal and work history was removed while the synthetic inbox batch was ingested
- the commit was an Inbox Ingester batch rather than a separately bounded Project Steward cleanup

The current Inbox Ingester constraints already prohibit general cleanup, unrelated trusted-content mutation, and takeover of broad Project Steward maintenance. Its capabilities nevertheless allow updating a required scoped log, and the contracts and fixtures do not state or enforce that pre-existing history entries must remain unchanged during ingestion.

## Classification

This is `required-v1` and blocks the release candidate. Inbox ingestion is a core v1 behavior, and its mutation authority must not permit source processing to erase durable history. The issue does not invalidate the already ingested synthetic knowledge because the user confirmed the clean-slate intent, but the role boundary needs an explicit contract and regression coverage before stable support begins.

## Root cause

The current contracts distinguish required scoped-history updates from general cleanup but do not define the permitted mutation shape for an existing `log.md`. As a result, an agent can interpret authority to "update the nearest conceptual log" as authority to replace, prune, or rewrite prior entries while ingesting a source.

## Scope

- define that Inbox Ingester may append one qualifying scoped-history entry required by the ingested semantic change
- prohibit Inbox Ingester from deleting, rewriting, consolidating, correcting, or retiring pre-existing scoped-history entries
- require a Project Steward handoff when existing history is stale, inaccurate, superseded, or needs retirement context
- require clean-slate test-project preparation to complete history cleanup before Inbox Ingester activation rather than during ingestion
- preserve the existing scoped-history threshold so routine ingestion does not create log entries
- add installed-payload regression coverage using a pre-existing knowledge log and an ingestion change that both does and does not meet the scoped-history threshold

## Completion criteria

- Inbox Ingester instructions, capabilities, constraints, and completion checks agree on append-only authority over pre-existing scoped history
- ingestion leaves every pre-existing log entry unchanged and in its original order
- a qualifying ingested conceptual or structural change may append the single nearest required entry without duplicating history at ancestor or sibling scopes
- stale, disputed, obsolete, or clean-slate history cleanup is reported as a Project Steward or fixture-preparation prerequisite rather than performed by Inbox Ingester
- a source remains pending when required cleanup or retirement decisions materially affect safe ingestion
- regression coverage fails if Inbox Ingester deletes or rewrites an existing log entry
- regression coverage confirms that non-qualifying routine ingestion does not alter a scoped log
- regression coverage confirms that a qualifying change appends only the required entry and preserves prior history
- affected role, shared-history, review, fixture, and validation contracts remain aligned
- the resolving change records repository tests, validation, and concrete resolution evidence

## Resolution evidence

Pending.

## Release qualification follow-up

After the repository fix is merged, exercise the corrected Inbox Ingester through a published prerelease against a realistic project containing pre-existing scoped history. Confirm that ordinary ingestion preserves the log, qualifying history is appended without rewriting prior entries, and required cleanup causes a Project Steward handoff. This published evidence remains a release gate and does not keep the implementation task pending after its repository completion criteria pass.
