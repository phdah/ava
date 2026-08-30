---
id: ava-5633
title: "Decide whether to keep, shrink, or remove the complete-pending-inbox qualification scenario"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5633
---

## Description

Evaluate whether the 305-source complete-pending-inbox scenario should remain, shrink, or be removed given its outsized multi-hour cost. The selected implementation shrinks the live scenario to the deterministic seven-source minimum while preserving the immutable 305-file corpus.

## Migrated task record

Historical metadata: phase 5 finding 33, `blocker`, blocking next prerelease, affected version `1.0.0-alpha.15`, completed 2026-08-25.

### Observed behavior and evidence

Run `20260825T063751637610Z-alpha14-to-alpha15-corrective-local` showed `complete-pending-inbox` at roughly 2+ hours after tightened fidelity constraints, versus under 20 minutes before them. It was the only matrix scenario performing full Inbox Ingester work over all 305 direct sources; the other 16 were deterministic checks or small routing prompts. The finalized corpus has seven maintained text/document formats (`md`, `txt`, `csv`, `docx`, `pdf`, `pptx`, `ics`). Available evidence lacked fine per-phase instrumentation, so the coarse 2-hour floor implied >23.6 seconds/source end to end versus <3.9 previously, with provider/fixed overhead included.

### Decision and tradeoffs

All three options were evaluated. Keeping 305 preserved maximum volume/repetition/chronology/PNG coverage but imposed disproportionate multi-hour reliability/quota cost. Removing the scenario eliminated cost but would discard the only maintained end-to-end Inbox Ingester qualification for an area that had exposed numerous findings. The selected option was to shrink to exactly seven sources, the strict lower bound for one source per maintained format, while mechanically requiring the selected union to retain `mapped`, `non-durable`, and `pending` dispositions.

The immutable finalized 305-file corpus and oracle remain unchanged. Only the materialized live `complete-pending-inbox` variant is minimized. `selection.json` records selected source names, formats, dispositions and SHA-256. A naive source-proportional estimate suggested roughly three minutes plus fixed/provider overhead, explicitly not a measured runtime; the next real run remains responsible for actual timing.

The shrink intentionally loses repeated volume, broad chronology and PNG live ingestion in this single every-release scenario while retaining those in corpus/oracle evidence. It reduces the rationale for previously proposed resume/status mitigations, which were later explicitly removed from the backlog after reassessment.

### Resolution evidence

`minimize_inbox.py` deterministically selects the seven-source lower bound from `oracle/baseline.json`, verifies seven formats plus all three dispositions, checks digests, prunes only the materialized variant inbox, writes `selection.json`, and refreshes `variants/index.json`. `generate-synthetic-qualification-vault.sh` applies the minimizer after normal variant materialization. `test_minimize_qualification_inbox.py` covers lower bound, disposition preservation, pruning, evidence and refreshed inventory. The synthetic-vault blueprint/index document the seven-source contract and individual lifecycle command.

The next live qualification remained responsible for measuring post-shrink runtime and proving the reduced end-to-end scenario.