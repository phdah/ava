---
type: Internal Development Task
title: Automate Release Qualification and Evidence State
description: Add one repository-only maintainer operation that acquires exact release inputs, prepares the synthetic fixture, runs qualification, audits every spawned OpenCode session, and records durable release-state evidence.
tags: [internal, roadmap, release, qualification, automation, evidence, opencode]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 4.3
classification: required-v1
blocks: next-qualification-run
generated:
  by: agent:openai-chatgpt
  at: 2026-08-14T15:39:53+02:00
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
- Record `qualification_model` and `audit_model` as separate checked-in fixed fields. Initialize both to `openai/gpt-5.6-sol` while allowing a reviewed future state change to update either field independently.
- Run the audit in a fresh OpenCode session after qualification. The audit must inspect the exact child and nested sessions bound to that run.
- A blocking or major audit finding makes the operation nonzero and records the release pair as `needs-review`.
- Persist compact manifests and audit reports in the repository. Keep downloaded assets, generated corpus copies, isolated workspaces, detailed command output, and full transcripts outside Git. The five canonical pinned fixture images are the explicit image exception.
- Write evidence files but do not create a Git commit.
- A mechanically and semantically successful run records `awaiting-user-signoff`, not automatic acceptance.
- Record audit issues in the run evidence. Do not automatically create, classify, or resolve dogfood finding files.

## State model

Add a repository-owned internal qualification state scope that separates configuration, release-pair history, and immutable run records.

The checked-in state must represent at least:

- schema version
- active source and target pair
- exact release tags, source revisions, release-manifest digests, and asset digests
- whether each side is a published immutable release or an exact local asset set
- qualification and audit model identifiers
- OpenCode version
- pinned qualification-image manifest and per-image digests
- fixture generator revision and deterministic inventory digest
- qualification matrix digest
- runner and repository revision
- latest run identifier for each release pair
- pair status: `not-run`, `running`, `failed`, `needs-review`, `awaiting-user-signoff`, `accepted`, or `rejected`
- explicit user signoff identity and time only after a later user-owned acceptance step

Every retained scenario outcome must be bound to the complete execution identity. Passing work may be reused only when source assets, target assets, image set, fixture inventory, matrix, repository revision, OpenCode version, and both model identifiers still match.

Changing the active pair or any bound execution identity must not relabel or reuse evidence from an earlier pair.

## Hands-off procedure

Implement one thin POSIX shell entry point backed by repository-only Python orchestration where structured state or process control requires it.

The operation must:

1. Require a clean Ava checkout before starting and load the checked-in active pair and model state.
2. Create an isolated run root outside the repository with separate asset, fixture, execution, transcript, audit, and temporary-test-project paths.
3. For a published side, download the exact tag's seven assets with `gh`, verify immutable-release attestations, reject mutable aliases, and verify every checksum and manifest identity.
4. For a local side, resolve the exact supplied directory and apply the same normal-file, checksum, identity, and edge validation without claiming publication or attestation evidence.
5. Verify the committed pinned qualification-image manifest and every image digest, size, media type, and destination.
6. Generate a clean deterministic synthetic baseline with the maintained fixture implementation.
7. Copy only the five verified committed images to their declared corpus destinations through the maintained fixture command, then run image finalization, complete fixture verification, and variant materialization.
8. Create a deterministic repository-external test-project boundary instead of depending on a user-owned project path.
9. Run mutation-free qualification preflight and then the complete maintained qualification matrix with the checked-in qualification model.
10. Preserve complete runner evidence long enough for audit and user signoff. Never delete failed or `needs-review` evidence automatically.
11. Emit a machine-readable session inventory that binds every top-level OpenCode session and nested task session to its scenario, prompt digest, model, project root, transcript digest, and terminal state.
12. Start a fresh OpenCode audit session with the checked-in audit model and a maintained audit prompt. Require read-only review of routing, required-reading order, authority, mutations, source fidelity, lifecycle behavior, errors, final claims, and runner acceptance gaps.
13. Validate the audit against a maintained output schema with admitted finding severity, evidence, consequence, correction, remediation owner, limitations, and terminal conclusion.
14. Return nonzero for mechanical failure, incomplete scenarios, unresolved required decisions, invalid audit output, or any admitted blocking or major audit finding.
15. Write the compact run manifest, audit report, issue inventory, raw-evidence digests, and updated pair state into the repository only after external execution and audit are complete.
16. Leave the repository changes uncommitted for maintainer and user review.

## Audit contract

The automated audit must not be the same conversational session that performed qualification work. It must receive only the run identity, maintained audit instructions, session inventory, runner evidence paths, applicable release contracts, and fixture oracle needed for the declared audit scope.

At minimum, the audit must determine:

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

The audit report is advisory evidence. The orchestrator may use its validated severity to select `needs-review`, but it must not apply remediation or create roadmap findings automatically.

## Repository evidence

Keep durable records small and reviewable. A run record should contain or link to:

- source and target identity
- all bound execution inputs and digests
- fixture and image identities
- model and OpenCode versions
- scenario outcomes
- session inventory
- independent audit report
- structured issues
- conformance and run-manifest results
- external raw-evidence location and archive digest when retained
- final automated state
- later user signoff state

Do not commit generated raw corpus files, copied corpus images, release asset archives, isolated projects, complete JSONL transcripts, provider credentials, or unrelated OpenCode session data. The five canonical pinned image inputs under the internal fixture are the only image-file exception.

## Failure and rerun policy

- Preserve a failed or `needs-review` external workspace for diagnosis.
- A corrected rerun receives a new run identifier and does not overwrite prior compact evidence.
- Reuse passing scenarios only under the complete bound execution identity.
- A changed pair, release digest, fixture digest, matrix digest, model, OpenCode version, repository revision, or audit contract starts a new execution identity.
- Interactive approval, clarification, or semantic judgment that cannot be resolved from checked-in approved state becomes a recorded nonzero result.
- Never convert a failed or audited `needs-review` run into `awaiting-user-signoff` by editing only the summary state.

## Implementation plan

1. Define and validate the internal qualification configuration, release-pair catalog, run-record, session-inventory, audit-output, and current-state schemas.
2. Add the checked-in alpha.13-to-alpha.14 historical pair and separate qualification/audit model fields.
3. Validate the committed pinned qualification-image manifest and exact source-to-corpus placement contract.
4. Implement published and local release-asset resolution with strict identity, attestation, checksum, edge, and boundary checks.
5. Compose fixture generation, pinned-image placement, finalization, verification, variant materialization, and temporary test-project creation.
6. Harden runner ownership and rerun state so retained scenarios are bound to the complete execution identity.
7. Add complete top-level and nested OpenCode session inventory capture.
8. Implement the fresh-session audit prompt, output schema, validation, and severity gate.
9. Write compact repository evidence and current pair state without committing.
10. Update the internal release procedure and V1 operator path to use the automated entry point.

## Test requirements

Automated tests must not require GitHub network access, model credentials, image generation, or a complete OpenCode qualification run.

Use local fakes and fixtures to cover:

- exact published-tag selection and mutable-alias refusal
- attestation and checksum failure
- published and local asset identity
- pinned image manifest identity, byte integrity, and five-file placement
- deterministic fixture generation composition
- complete execution-identity binding and safe scenario reuse
- changed asset, model, matrix, repository, OpenCode, fixture, or image identity refusing retained outcomes
- top-level and nested session inventory completeness
- audit schema validation and severity exit behavior
- compact evidence writing without raw-data leakage
- `awaiting-user-signoff` versus `needs-review` state transitions
- no automatic Git commit or dogfood finding creation
- exclusion of all internal automation, configuration, and evidence from assembled release assets

## Completion criteria

- one documented internal command performs the approved hands-off procedure without user interaction
- the command supports exact published and exact local source/target assets
- published release assets receive immutable attestation and checksum verification, and committed pinned images receive exact manifest verification
- a clean fixture, finalized image inventory, variants, test boundary, qualification run, session audit, and compact evidence record are produced in one operation
- every retained result is cryptographically and semantically bound to its complete execution identity
- the audit runs in a fresh session, accounts for nested sessions, and validates against a maintained schema
- blocking or major audit findings produce nonzero status and `needs-review`
- a clean result produces `awaiting-user-signoff`, never automatic acceptance
- alpha.13-to-alpha.14 appears as historical pair state without being reused for another release
- raw release assets, generated corpus copies, workspaces, and transcripts remain outside the repository; only the five canonical internal fixture images are committed
- generated compact evidence remains uncommitted
- repository tests, boundary validation, and internal release tests pass
- the V1 operator path names the automated operation as the required next qualification entry point
