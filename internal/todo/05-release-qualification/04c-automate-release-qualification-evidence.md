---
type: Internal Development Task
title: Automate Release Qualification and Evidence State
description: Add one repository-only maintainer operation that acquires exact release inputs, prepares the synthetic fixture, runs qualification, audits every spawned OpenCode session, and records durable release-state evidence.
tags: [internal, roadmap, release, qualification, automation, evidence, opencode]
status: complete
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 4.3
classification: required-v1
blocks: next-qualification-run
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T15:39:53+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-14T16:27:00+02:00
---

# Automate Release Qualification and Evidence State

## Purpose

Replace the current multi-step maintainer interaction with one repository-only, non-interactive operation that prepares and executes release qualification, independently audits the OpenCode sessions created by that run, and writes a compact durable release-state record for review.

The operation must be hands-off during execution. It must stop with machine-readable evidence rather than ask the user to resolve an interactive question. Successful execution does not grant publication authority or replace explicit user signoff.

This is internal release tooling. It must not create a distributed Ava CLI, persistent runtime, service, or user-project command surface.

## Approved decisions

- This task is required before the next synthetic qualification run and preempts the current V1 operator path until implementation is complete.
- Exact source and target release selection comes from a reviewed checked-in catalog with one explicit active pair. Do not resolve a mutable `latest` release.
- Begin the historical pair ledger with `1.0.0-alpha.13 -> 1.0.0-alpha.14` without treating that historical result as qualification of a later corrective release.
- Support exact published GitHub Releases and exact caller-supplied local release asset directories.
- Published assets require GitHub immutable-release attestation verification followed by verification of the exact seven-asset `SHA256SUMS` inventory.
- Reuse one immutable five-image qualification set instead of generating new image bytes for every run.
- Store the five visually accepted PNG files and their exact manifest under the repository-only synthetic fixture scope. Generated corpus copies remain repository-external.
- Use `internal/release/generate-synthetic-qualification-vault.sh` as the maintained one-command fixture entry point instead of reconstructing its generation, pinned-image installation, finalization, verification, and variant-materialization sequence in the orchestrator.
- Record `qualification_model` and `audit_model` as separate checked-in fixed fields. Initialize both to `openai/gpt-5.6-sol` while allowing a reviewed future state change to update either field independently.
- Run the audit in a fresh OpenCode session after qualification. The audit must inspect the exact child and nested sessions bound to that run.
- A blocking or major audit finding makes the operation nonzero and records the release pair as `needs-review`.
- Persist compact manifests and audit reports in the repository. Keep downloaded assets, generated corpus copies, isolated workspaces, detailed command output, and full transcripts outside Git. The five canonical pinned fixture images are the explicit image exception.
- Write evidence files but do not create a Git commit.
- A mechanically and semantically successful run records `awaiting-user-signoff`, not automatic acceptance.
- Record audit issues in the run evidence. Do not automatically create, classify, or resolve dogfood finding files.

## State model

The repository-owned internal qualification state scope separates configuration, release-pair history, and immutable run records.

The checked-in state represents:

- schema version
- active source and target pair
- exact release tags, source revisions, release-manifest digests, and asset digests
- whether each side is a published immutable release or an exact local asset set
- qualification and audit model identifiers
- OpenCode version
- pinned qualification-image manifest and per-image digests
- fixture generator revision and deterministic inventory digest
- qualification matrix digest
- runner, automation, and repository revision
- latest run identifier for each release pair
- pair status: `not-run`, `running`, `failed`, `needs-review`, `awaiting-user-signoff`, `accepted`, or `rejected`
- explicit user signoff identity and time only after a later user-owned acceptance step

Every retained scenario outcome is bound to the complete execution identity. Passing work may be reused only when source assets, target assets, image set, fixture inventory, matrix, repository revision, OpenCode version, runner and automation bytes, and both model identifiers still match.

Changing the active pair or any bound execution identity cannot relabel or reuse evidence from an earlier pair.

## Hands-off procedure

The implementation provides one thin POSIX shell entry point backed by repository-only Python orchestration.

The operation:

1. Requires a clean Ava checkout before starting and loads the checked-in active pair and model state.
2. Creates an isolated run root outside the repository with separate asset, fixture, execution, transcript, audit, and temporary-test-project paths.
3. For a published side, downloads the exact tag's seven assets with `gh`, verifies immutable-release attestations, rejects mutable aliases, and verifies every checksum and manifest identity.
4. For a local side, resolves the exact supplied directory and applies the same normal-file, checksum, identity, and edge validation without claiming publication or attestation evidence.
5. Verifies the committed pinned qualification-image manifest and every image digest, size, media type, dimension, and destination.
6. Invokes `internal/release/generate-synthetic-qualification-vault.sh` with `TMPDIR` set to the isolated run's fixture parent and retains the exact output path it reports.
7. Requires the wrapper to complete clean deterministic generation, exact committed-image placement, image finalization, complete fixture verification, and variant materialization before continuing.
8. Creates a deterministic repository-external test-project boundary instead of depending on a user-owned project path.
9. Runs mutation-free qualification preflight and then the complete maintained qualification matrix with the checked-in qualification model.
10. Preserves complete runner evidence long enough for audit and user signoff and never deletes failed or `needs-review` evidence automatically.
11. Emits a machine-readable session inventory that binds every top-level OpenCode session and nested task session to its scenario, prompt digest, model, project root, transcript digest, parent, and terminal state.
12. Starts a fresh OpenCode audit session with the checked-in audit model and maintained audit prompt.
13. Validates the audit against the maintained output schema with admitted severity, evidence, consequence, correction, remediation owner, limitations, and terminal conclusion.
14. Returns nonzero for mechanical failure, incomplete scenarios, unresolved required decisions, invalid audit output, or any admitted blocking or major audit finding.
15. Writes the compact run manifest, audit report, issue inventory, raw-evidence digest, and updated pair state into the repository only after external execution and audit are complete.
16. Leaves repository evidence changes uncommitted for maintainer and user review.

## Audit contract

The automated audit is not the same conversational session that performed qualification work. It receives only the run identity, maintained audit instructions, session inventory, runner evidence paths, applicable release contracts, and fixture oracle needed for the declared audit scope.

At minimum, the audit determines:

- whether every required role was announced only after complete required reading
- whether a missing or invalid required path was guessed around rather than treated according to the active contract
- whether each mutation remained inside the active role and scenario boundary
- whether ambiguous requests remained unmodified and visibly requested clarification
- whether calendar persistence used deterministic verification and retained the correct reference context
- whether inbox completion was independently reconciled against every selected source and the maintained oracle rather than inferred from file movement or link validity
- whether semantic reconciliation recorded every inspected and changed project-owned path before completion
- whether finalization followed the target release's intended agent-driven or installer-backed contract without an unqualified fallback
- whether removal and reinstall preserved project-owned bytes
- whether command errors, retries, missing tools, nested sessions, or superseded attempts weaken the claimed evidence
- whether runner pass criteria are strong enough to support each terminal claim

The audit report is advisory evidence. The orchestrator uses its validated severity to select `needs-review`, but it does not apply remediation or create roadmap findings automatically.

## Repository evidence

Compact run records contain or link to:

- source and target identity
- all bound execution inputs and digests
- fixture and image identities
- model and OpenCode versions
- scenario outcomes through the bound runner summary
- session inventory
- independent audit report
- structured issues
- external raw-evidence location and digest
- final automated state
- later user signoff state

Generated raw corpus files, copied corpus images, release asset archives, isolated projects, complete JSONL transcripts, provider credentials, and unrelated OpenCode session data remain outside the repository. The five canonical pinned image inputs under the internal fixture are the only image-file exception.

## Failure and rerun policy

- Preserve a failed or `needs-review` external workspace for diagnosis.
- A corrected rerun receives a new run identifier and does not overwrite prior compact evidence.
- Reuse passing scenarios only under the complete bound execution identity.
- A changed pair, release digest, fixture digest, matrix digest, model, OpenCode version, repository revision, runner, automation, audit contract, or pinned-image identity starts a new execution identity.
- Interactive approval, clarification, or semantic judgment that cannot be resolved from checked-in approved state becomes a recorded nonzero result.
- Never convert a failed or audited `needs-review` run into `awaiting-user-signoff` by editing only the summary state.

## Implementation

The completed implementation is centered on:

- `internal/release/qualify-release.sh`
- `internal/release/qualification_automation.py`
- `internal/release/qualification-automation.md`
- `internal/release/qualification/`
- `internal/release/tests/test_qualification_automation.py`

The checked-in pair catalog begins with historical `v1.0.0-alpha.13 -> v1.0.0-alpha.14` and keeps it distinct from the active corrective pair. The active pair is immutable published `v1.0.0-alpha.14 -> exact local v1.0.0-alpha.15`, so a caller must supply the exact local target asset directory until that corrective release is published.

`qualification_model` and `audit_model` are separate checked-in fields and both currently resolve to `openai/gpt-5.6-sol`.

## Test coverage

The bounded repository test suite covers without network or model credentials:

- checked-in pair/config/state consistency
- mutable-release alias refusal
- local asset checksum and identity validation
- published release immutable-attestation failure handling through fakes
- exact five-image pinned manifest verification
- use of the maintained fixture-generation wrapper as one operation
- complete execution-identity namespacing
- top-level and nested OpenCode session inventory
- audit-output schema validation and severity gating
- compact evidence writing with user signoff left unset
- absence of automatic Git commits or dogfood finding creation
- syntax and compile coverage from `internal/release/test.sh`
- repository boundary validation keeping the entire automation and evidence scope internal

## Completion

Implementation is complete. The required supporting task no longer preempts Step 1.

The normal next operator action is now:

```sh
internal/release/qualify-release.sh \
  --target-assets /absolute/path/to/v1.0.0-alpha.15/assets
```

That execution is release qualification evidence, not unfinished implementation work. A clean automated run must end at `awaiting-user-signoff`; explicit evidence acceptance remains a separate Step 1 gate before the release path advances.
