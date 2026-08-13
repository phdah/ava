---
type: Internal Development Task
title: Preserve Existing Scoped History During Ingestion
description: Prevent Inbox Ingester operations from deleting or rewriting pre-existing scoped history while still allowing a required new history entry to be appended.
tags: [internal, roadmap, dogfood, inbox, history, roles, trust]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 16
classification: required-v1
blocks: release-candidate
affected_version: 1.0.0-alpha.14
generated:
  by: agent:opencode
  at: 2026-08-13T12:18:45+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-13T14:46:00+02:00
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

The previous Inbox Ingester constraints prohibited general cleanup, unrelated trusted-content mutation, and takeover of broad Project Steward maintenance, but did not state the permitted mutation shape for an existing scoped log.

## Classification

This is `required-v1` and blocks the release candidate until its repository implementation is complete. Inbox ingestion is a core v1 behavior, and its mutation authority must not permit source processing to erase durable history.

## Root cause

The contracts distinguished required scoped-history updates from general cleanup but did not define additive-only authority over an existing `log.md`. An agent could therefore interpret authority to update the nearest conceptual log as authority to replace, prune, or rewrite prior entries while ingesting a source.

## Scope

- define that Inbox Ingester may append one qualifying scoped-history entry required by the ingested semantic change
- prohibit Inbox Ingester from deleting, rewriting, consolidating, correcting, or retiring pre-existing scoped-history entries
- require a Project Steward handoff when existing history is stale, inaccurate, superseded, or needs retirement context
- require clean-slate test-project preparation to complete history cleanup before Inbox Ingester activation rather than during ingestion
- preserve the existing scoped-history threshold so routine ingestion does not create log entries
- add installed-payload regression coverage using a pre-existing knowledge log and an ingestion change that both does and does not meet the scoped-history threshold

## Completion criteria

- [x] Inbox Ingester instructions, capabilities, constraints, and completion checks agree on additive-only authority over pre-existing scoped history.
- [x] Ingestion leaves every pre-existing log entry unchanged and in its original order.
- [x] A qualifying ingested conceptual or structural change may add the single nearest required entry without duplicating history at ancestor or sibling scopes.
- [x] Stale, disputed, obsolete, or clean-slate history cleanup is reported as a Project Steward or fixture-preparation prerequisite rather than performed by Inbox Ingester.
- [x] A source remains pending when required cleanup or retirement decisions materially affect safe ingestion.
- [x] Regression coverage rejects deletion or rewriting of an existing log entry.
- [x] Regression coverage confirms that non-qualifying routine ingestion does not alter a scoped log.
- [x] Regression coverage confirms that a qualifying change adds only the required entry and preserves prior history.
- [x] Affected role, shared-history, review, fixture, and validation contracts remain aligned.
- [x] The resolving change records repository tests, validation, and concrete resolution evidence.

## Resolution evidence

- Inbox Ingester now loads the shared scoped-history contract as required reading and records its authority change in a role-scoped history log.
- Inbox Ingester instructions define additive-only scoped-history authority: the ingestion itself must cross the existing shared threshold, at most one nearest-scope entry may be added, and every pre-existing entry must remain verbatim and in its existing relative order.
- Capabilities and constraints explicitly separate the permitted new history entry from cleanup, correction, consolidation, supersession, retirement, and clean-slate preparation. Material cleanup decisions keep the source pending and are handed to Project Steward; fixture cleanup occurs before role activation.
- Change Reviewer now conditionally loads the shared scoped-history contract for ingestion reviews and treats destructive ingestion-time history mutation as a semantic review failure.
- `internal/release/fixtures/inbox-scoped-history.json` covers routine non-qualifying ingestion, qualifying single-entry history, and cleanup handoff against a pre-existing knowledge log.
- `internal/release/tests/test_inbox_scoped_history.py` validates assembled installed-role and reviewer contracts, preserves the existing shared threshold, checks exact prior-entry preservation, and explicitly rejects deleted or rewritten history entries.
- The new regression module is registered in `internal/release/test.sh`, so it runs with the maintained repository release suite.
- Dogfood and Phase 5 indexes are synchronized with finding 16 implementation-complete and synthetic-vault qualification restored as the official next work.

## Release qualification follow-up

Exercise the corrected Inbox Ingester through a published prerelease against a realistic project containing pre-existing scoped history. Confirm that ordinary ingestion preserves the log, qualifying history is added without rewriting prior entries, and required cleanup causes a Project Steward handoff. This published evidence remains a release gate and does not keep the implementation task pending after repository completion.
