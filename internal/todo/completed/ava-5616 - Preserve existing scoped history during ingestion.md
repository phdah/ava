---
id: ava-5616
title: "Preserve existing scoped history during ingestion"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5616
---

## Description

Prevent Inbox Ingester operations from deleting or rewriting pre-existing scoped history while still allowing a required new history entry to be appended.

## Migrated task record

Historical metadata: phase 5 finding 16, `required-v1`, blocking release candidate, affected version `1.0.0-alpha.14`, completed after implementation.

### Observed behavior and root cause

During synthetic ingestion, commit `81b0ec4` in the dogfood project reduced `knowledge/log.md` from 59 lines to five and removed prior trusted-history entries. The user intended a clean synthetic project, but cleanup occurred inside an Inbox Ingester batch instead of Project Steward maintenance or fixture preparation. Existing contracts distinguished history updates from cleanup but did not state the permitted mutation shape for an existing log, so “update the nearest conceptual log” could be interpreted as replace/prune/rewrite authority.

### Approved scope and completion criteria

Inbox Ingester may append at most one nearest-scope history entry when the ingested semantic/structural change crosses the established shared threshold. It may not delete, rewrite, consolidate, correct, supersede or retire prior entries. Stale/disputed/obsolete/clean-slate history requires Project Steward handoff or pre-activation fixture preparation; material cleanup dependencies keep the source pending. Routine ingestion that does not meet the history threshold must not touch the log. Regression had to prove exact prior-entry preservation/order, single qualifying append, non-qualifying no-op, cleanup handoff, and aligned shared/reviewer/installed contracts.

### Resolution evidence

Inbox Ingester now loads the shared scoped-history contract as required reading, and its role history records the authority change. Instructions define additive-only authority, one nearest entry maximum, and verbatim/order-preserved prior history. Capabilities/constraints separate append authority from cleanup/correction/consolidation/supersession/retirement and clean-slate preparation. Change Reviewer conditionally loads the history contract for ingestion review and treats destructive history mutation as a semantic failure.

`internal/release/fixtures/inbox-scoped-history.json` covers routine no-op, qualifying single-entry append and cleanup handoff on a pre-existing log. `test_inbox_scoped_history.py` validates installed role/reviewer contracts, threshold preservation, exact prior-entry preservation and rejection of deletion/rewriting, and runs in `internal/release/test.sh`.

Published follow-up required ordinary, qualifying and cleanup-required ingestion against realistic pre-existing history. That remains release evidence rather than reopening the completed implementation task.