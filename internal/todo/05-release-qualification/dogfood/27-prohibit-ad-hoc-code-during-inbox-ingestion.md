---
type: Internal Development Task
title: Prohibit Ad Hoc Code Execution During Inbox Ingestion
description: Stop Inbox Ingester from creating and executing scripts to bulk-transform inbox content, since doing so bypasses per-section disposition curation and exceeds the role's declared project mutation scope.
tags: [internal, roadmap, dogfood, inbox, scope, qualification]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 27
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.15
generated:
  by: agent:opencode
  at: 2026-08-24T00:00:00Z
updated:
  by: agent:openai-chatgpt
  at: 2026-08-24T15:58:00+02:00
---

# Prohibit Ad Hoc Code Execution During Inbox Ingestion

## Observed behavior

Mandatory release qualification for candidate `77977f8` ran the `complete-pending-inbox` scenario. The independent audit found (`AUD-SCOPE-001`, minor) that the Inbox Ingester session created `.tmp_ingest.py` at the project root, executed it, and later deleted it, to bulk-process the entire 305-file inbox batch programmatically.

`templates/base/roles/inbox-ingester/role.md:50-58` and `capabilities.md:20-38` authorize destination documents, required directories, indexes, provenance, and source movement, but not arbitrary root-level implementation files or code execution as an ingestion mechanism.

This is independently evidenced as the mechanism that produced `AUD-INBOX-001` (see finding 28): the script performed whole-source, filename-keyword routing instead of the required per-section disposition process, so this scope violation and the fidelity violation share one root cause.

## Reproduction and evidence

Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local`, active pair `alpha14-to-alpha15-corrective-local`, candidate revision `77977f8`. Session `ses_fcc3d6a7dffeqdNojknUD9NOdq`, transcript `complete-pending-inbox.jsonl`, the `apply_patch` call adding `.tmp_ingest.py`.

Result: `automated_state: needs-review`. All 17 runner scenarios and all 286 repository tests passed; the independent audit found two major issues and this minor issue.

## Classification

`blocker` for the next prerelease: it currently blocks acceptance of this qualification run and therefore blocks merge of the release PR.

## Root cause

Neither `templates/base/roles/inbox-ingester/capabilities.md` nor `constraints.md` addresses whether the role may create or execute code as part of ingestion. Faced with a large batch, the session wrote a Python script to mechanize routing instead of producing each destination document directly, which both exceeded the role's declared mutation scope and (per finding 28) bypassed the required per-section fidelity process.

## Scope

- add an explicit constraint to `templates/base/roles/inbox-ingester/constraints.md` (and align `capabilities.md` if needed) prohibiting creation or execution of scripts, generated code, or other programmatic bulk-content-transformation mechanisms as part of ingestion
- require every destination document to be produced through direct, per-source (or per-section) reasoning and editing rather than generated automation
- add or extend fixture/regression coverage that would catch a project-root script or other out-of-scope implementation file appearing during ingestion
- keep this fix bounded to the scope boundary; do not fold in finding 28's disposition-fidelity wording here

## Completion criteria

- [x] `inbox-ingester` role documents explicitly prohibit ad hoc script creation or code execution as an ingestion mechanism
- [x] regression coverage exercises this boundary
- [x] affected documentation and indexes remain aligned
- [x] repository test suite passes

## Resolution evidence

Inbox Ingester `instructions.md` and `constraints.md` now require direct source or section reasoning and editing and explicitly prohibit ad hoc scripts, generated code, temporary implementation files, and programmatic bulk transformation during ingestion. The role-scoped log records the authority boundary.

The synthetic `complete-pending-inbox` runner now observes direct project-root entries for the full OpenCode prompt and fails when a new entry appears, including a helper that is deleted before final conformance. `test_qualification_runner.py` reproduces the observed create-delete pattern with `.tmp_ingest.py`, while the qualification procedure and release implementation log document the guard.

The repository test suite remains the PR validation gate for this completed implementation.

## Release qualification follow-up

This changes distributed role content (`templates/base/roles/inbox-ingester/`), so the resolving change is a releasable `fix` and requires a brand-new full 17-scenario qualification run and independent audit against a freshly assembled candidate before the release PR may proceed.
