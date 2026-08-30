---
id: ava-5608
title: "Define review sufficiency and termination criteria"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "required-v1"]
ordinal: 5608
---

## Description

Make Ava reviews capable of reaching a stable acceptable conclusion instead of continually discovering progressively smaller improvements. This task preserves the review-sufficiency finding and resolution evidence.

## Migrated task record

Historical metadata: phase 5 finding 8, `required-v1`, blocking release candidate, observed against repository source on 2026-08-08, completed after implementation.

### Observed behavior

Repeated semantic review could become an open-ended review/remediation loop: each corrected review was followed by progressively smaller new concerns instead of a determination that the bounded change was sufficiently correct. The prior Change Reviewer allowed zero findings but did not clearly distinguish acceptance review from improvement discovery, establish finding thresholds, or define successful re-review termination.

### Root cause and scope

The contract lacked explicit acceptance-vs-audit semantics, evidence/consequence/confidence/impact admission thresholds, optional observation handling, incremental re-review behavior, stable termination, and threshold-based conclusions. The fix was intentionally owned by Change Reviewer rather than generalized into unrelated root instructions.

The approved contract used established review patterns: ordinary bounded review defaults to an acceptance decision; findings exclude preferences, speculative improvements and alternative valid designs; optional observations cannot affect acceptance; re-review starts from prior findings/remediation and broadens only on concrete new evidence; resolved concerns are not reopened without changed evidence/scope/authority/regression; audit behavior requires explicit scope; and conclusions state whether the active threshold was met without claiming user approval or deterministic validity.

### Completion criteria

The task required clean acceptance, distinction among findings/observations/preferences, monotonic prior-finding re-review, independent admission of any new finding, no reopening without changed evidence, explicit audit mode, threshold conclusions under advisory authority, fixtures for clean review/satisfied re-review/regression/audit, aligned role/workflow/docs/indexes, and concrete repository-validation evidence.

### Resolution evidence

Change Reviewer now defines `acceptance` as the default standard and `audit` only when explicitly requested. Every candidate finding passes evidence, consequence, confidence, and threshold admission. Preferences/speculative/stylistic/alternative-valid-design concerns are not findings. Minor findings are non-blocking and optional observations are normally omitted in acceptance review.

Re-review continues prior state by classifying earlier findings resolved/unresolved/superseded before reviewing remediation. New or reopened findings require changed evidence, scope, authority, or regression and must independently pass admission. Review terminates successfully once prior blocking/major findings are closed, no new admitted blocking/major issue exists, and no user-owned decision prevents conclusion.

`review-change` defaults to acceptance and accepts prior review state; `review-role-catalog` explicitly defaults to audit. `internal/release/fixtures/review-sufficiency.json` covers clean review, satisfied re-review, remediation regression and exhaustive audit. `internal/release/tests/test_review_sufficiency.py` protects standards, admission, observations, monotonic termination, workflow defaults and advisory authority and is included in the release test suite. No separate shared evaluative-role rule was added.

Release qualification still required an installed corrective-prerelease review/remediate/re-review cycle demonstrating a successful terminal conclusion when earlier findings were resolved and no new concern exceeded the threshold.