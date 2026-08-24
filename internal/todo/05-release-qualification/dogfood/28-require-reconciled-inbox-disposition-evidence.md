---
type: Internal Development Task
title: Require Reconciled Per-Passage Disposition Evidence Before Inbox Completion
description: Stop Inbox Ingester from promoting non-durable source passages into trusted knowledge and from claiming disposition totals that were never reconciled against rendered destination content.
tags: [internal, roadmap, dogfood, inbox, fidelity, provenance, qualification]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 28
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-24T00:00:00Z
---

# Require Reconciled Per-Passage Disposition Evidence Before Inbox Completion

## Observed behavior

Mandatory release qualification for candidate `77977f8` ran the `complete-pending-inbox` scenario. The independent audit found (`AUD-INBOX-001`, major) that trusted knowledge destinations contain source passages the fixture oracle explicitly classifies `non-durable` (intentionally not promoted), and that the session's reported disposition totals were not backed by any actual reconciliation.

Evidence cited by the audit:

- the fixture oracle at `oracle/baseline.json:400-406` classifies the January 2 cooking "Next time" passage as `non-durable`; `knowledge/personal/cooking/neapolitan-pizza-practice.md:529-547` promotes it anyway, and the same pattern repeats across all 18 cooking records
- the oracle at `oracle/baseline.json:443-464` classifies a recurring dog-care "window spot" passage as `non-durable`; `knowledge/personal/pets/uno.md:1283-1292` promotes it, repeating across all 12 dog-care records
- the session reported `1,895 mapped passages, 349 non-durable passages, 0 pending`, but no executed reconciliation computed the 349 non-durable dispositions, and the rendered destinations contradict the claim

This is the same defect class as `AVA-AUD-INBOX-FIDELITY-005` from the prior qualification attempt (run `20260821T100350003229Z-alpha14-to-alpha15-corrective-local`), now confirmed to recur on a fresh, independent attempt rather than being a one-off coincidence.

## Reproduction and evidence

Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local`, candidate revision `77977f8`, session `ses_fcc3d6a7dffeqdNojknUD9NOdq`. See also finding 27: the mechanism this run was a generated script performing whole-source, filename-keyword routing instead of the fixture's required per-section child ledgers.

## Classification

`blocker` for the next prerelease: it currently blocks acceptance of this qualification run and therefore blocks merge of the release PR. It has now recurred across two independent qualification attempts.

## Root cause

`templates/base/shared/instructions/inbox-ingestion-fidelity.md` already states the disposition contract (every substantive section ends in exactly one of `mapped`/`non-durable`/`pending`, non-durable sections are "intentionally not promoted"), but nothing requires the *completion claim itself* to be reconciled against what was actually rendered into destinations. A session can therefore assert disposition totals without having performed the reconciliation, and nothing catches a whole-source promotion that silently ignores per-passage dispositions.

## Scope

- strengthen `templates/base/shared/instructions/inbox-ingestion-fidelity.md` (and/or the Inbox Ingester completion-report contract) to require that claimed disposition totals be derived by reconciling actual rendered destination content against the per-source section ledger, not asserted from a running tally
- explicitly forbid promoting a passage into a destination when its section disposition is `non-durable`, regardless of the mechanism used to produce the destination
- add or extend fixture/regression coverage that would catch a whole-source promotion or an unreconciled completion claim
- coordinate with finding 27 without merging the two findings' completion criteria: 27 removes the ad hoc code mechanism, this finding closes the fidelity gap independent of mechanism

## Completion criteria

- [ ] the fidelity contract requires disposition totals to be reconciled against rendered destination content before completion
- [ ] the fidelity contract explicitly forbids promoting `non-durable`-classified content into any destination
- [ ] regression coverage exercises this requirement
- [ ] affected documentation and indexes remain aligned
- [ ] repository test suite passes

## Resolution evidence

_Complete in the resolving implementation PR._

## Release qualification follow-up

This changes distributed role/instruction content, so the resolving change is a releasable `fix` and requires a brand-new full 17-scenario qualification run and independent audit against a freshly assembled candidate before the release PR may proceed. The `complete-pending-inbox` scenario and its independent-audit review must both be clean.
