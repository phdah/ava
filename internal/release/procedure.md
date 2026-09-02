---
type: Internal Release Procedure
title: Ava Release Publication Procedure
description: Authoritative procedure for preparing, qualifying, accepting, merging, publishing, and verifying Ava releases.
tags: [internal, releases, publication, verification, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T20:55:00+02:00
---

# Ava Release Publication Procedure

When the user asks to make, prepare, review, accept, merge, publish, or qualify an Ava release, the Ava Internal Maintainer must follow this procedure.

The normal release gate is intentionally deterministic. Synthetic consumer-agent behavior is optional QA, not mandatory publication evidence.

The release procedure is **session-neutral**. The maintainer may be operating from an ordinary ChatGPT chat, ChatGPT Work, or another repository-capable agent session. No particular ChatGPT mode is a release requirement.

Mandatory deterministic qualification runs in **GitHub Actions** on the release PR. The active maintainer session orchestrates the release through the connected repository: it reviews the release delta, authors the edge, inspects CI/evidence, applies validated qualification artifacts, records explicit user acceptance, and merges when all gates pass. The session itself does not need a shell or mutable local workspace.

The deterministic execution details are documented in [Session-neutral deterministic qualification](qualification-execution.md).

# Release flow

1. Let release-please determine the target version and release PR.
2. Configure the active qualification pair as the exact immutable previous published release -> exact local target version.
3. Work from the exact release PR branch using the current maintainer session. Do not require the user to switch ChatGPT modes.
4. The `Release qualification` GitHub Actions workflow detects that the target adjacent edge does not yet exist and runs the deterministic `pre-edge` qualification automatically.
5. The pre-edge run acquires and verifies the exact previous published release assets, generates the finalized synthetic qualification vault, assembles the provisional no-edge candidate, and runs the cheap deterministic fail-fast checks. It writes no qualification artifact because no repository evidence is required.
6. If pre-edge fails, stop before semantic review and edge authoring.
7. Review the exact previous-to-target managed delta and complete the project-owned semantic-impact assessment, including an explicit decision and rationale.
8. Author exactly one adjacent release record for `<previous> -> <target>`, plus only the guidance, deterministic migrations, and retirement decisions introduced by that edge.
9. Once the edge exists, the `Release qualification` workflow automatically runs the authoritative `final` deterministic qualification from the exact release PR revision.
10. The final run reruns the pre-edge checks and additionally proves the authentic source-to-target edge, deterministic upgrade, interrupted resume, abort, rollback, project-owned preservation, and exact asset/revision identity.
11. If final qualification fails, stop and report the exact deterministic finding.
12. If final qualification passes, the workflow creates one authoritative final run under `internal/release/qualification/runs/`, updates `current-state.json` to `awaiting-user-signoff`, and uploads those exact repository changes as a `release-qualification-evidence-*` artifact.
13. The active maintainer session downloads that artifact through the connected GitHub capability, validates its `artifact-manifest.json`, applies exactly the listed files/deletions to the release PR branch, and makes no other release-content change in that commit.
14. The resulting PR checks rerun normally. `Release qualification` reuses the committed final evidence when its qualified revision is an ancestor of the current head and every intervening change is confined to `internal/release/qualification/`.
15. Require the normal GitHub Actions checks, including Python/repository tests and deterministic release qualification, to be green. Release PR policy remains blocked until explicit acceptance exists.
16. Present the final deterministic evidence to the user.
17. Only after explicit user approval, record an acceptance request for the exact run. A session with direct shell execution may use `accept-release-qualification.sh`; a normal repository-connected chat may instead commit `internal/release/qualification/acceptance-request.json` as described below.
18. The `Release qualification` workflow validates the acceptance request, runs the maintained acceptance implementation in CI, removes the transient request in its checkout, and uploads the resulting qualification-state transition as a `release-qualification-acceptance-*` artifact.
19. The active maintainer session downloads that artifact, validates its manifest, applies the exact updated qualification files and deletion of `acceptance-request.json` to the release PR, and commits only those qualification changes.
20. Require the Release PR policy check to pass on that accepted state.
21. Merge only after the adjacent edge, semantic-impact decision, final deterministic qualification, required GitHub Actions checks, and explicit user acceptance are all accepted.
22. Publication automation creates and verifies the immutable release.

# Session boundary

Mandatory release qualification uses **zero delegated qualification agents** and does not require a particular ChatGPT session type.

The active maintainer session owns only work that genuinely benefits from maintainer judgment or repository orchestration:

- discover the release PR and exact release context
- configure the active release pair
- inspect the managed delta
- make and record the semantic-impact decision and rationale
- author the adjacent edge, guidance, migrations, and retirement decisions
- inspect deterministic CI results and compact evidence
- apply exact qualification artifacts through the connected repository capability
- request acceptance only after explicit user approval
- merge only after all checks are satisfied

The deterministic release checks themselves run in GitHub Actions. A session with shell access may invoke the same entry points directly for diagnostics, but normal release acceptance must not depend on Work, OpenCode, a user workstation, or another session-specific runtime.

# Mandatory deterministic checks

The mandatory release gate covers:

- exact source and target assets and checksums
- exact target/repository revision binding
- empty-project installation
- mature-project installation with project-owned preservation
- rejection of modified, missing, corrupt, and unexpected managed state
- exact adjacent edge presence in the final assets
- a real deterministic previous-to-target upgrade
- interrupted upgrade resume
- interrupted upgrade abort
- rollback to the previous release
- finalized synthetic corpus and external test-boundary integrity

Routing, calendar interpretation, ambiguous clarification, inbox ingestion, agent-led semantic reconciliation/finalization, and role-led uninstall/reinstall remain useful behavioral tests, but they are optional behavioral QA rather than release-gating evidence.

# Pre-edge fail-fast boundary

The pre-edge run exists only to avoid wasting maintainer effort on an obviously broken candidate.

It runs before the target adjacent catalog or guidance is authored and intentionally writes no repository evidence. There is no committed early-run ancestry chain to preserve.

A release-content change after pre-edge does not require proving that the early result remains valid; the authoritative final run simply reruns the applicable deterministic checks against the final exact revision.

# Adjacent release state

After pre-edge succeeds, author exactly one immutable release record:

`internal/release/catalogs/<target>.json`

That record contains only the immediately previous-to-target edge, migrations introduced by that edge, semantic guidance introduced by that edge, and source-retirement decisions introduced by that release.

Existing release records must not be rewritten or copied into cumulative state.

# Project-owned semantic-impact assessment

For the exact previous-to-target managed delta, answer:

1. **Managed delta:** Which managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed?
2. **Project-owned compatibility:** Could valid active project-owned context remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible under the target?
3. **Required reconciliation:** If yes, which bounded project-owned concepts must be inspected or reconciled before semantic compatibility may advance?

Record the reviewed decision and its rationale as release evidence.

Set `semantic_review_required: true` only when project-owned semantic reconciliation may be required. When true, transition-local guidance must define affected concepts, bounded discovery conditions, and completion criteria.

Tooling must not guess semantic migration need. The decision is reviewed maintainer judgment over the exact managed delta and project-owned compatibility question. A managed behavior change alone does not decide semantic impact, and the presence or absence of a deterministic project-file migration does not decide it either.

The deterministic final qualification verifies that the installer reaches the mechanically correct target state. When semantic review is required, that correct state may be `pending`; the release gate does not spend a synthetic agent turn pretending to reconcile arbitrary project-owned meaning.

# Final deterministic qualification

The final run is the only qualification run used for acceptance.

It must be assembled and executed from the exact final release PR revision after edge authoring. The run record binds that revision to the local target asset identity, source release identity, qualification matrix digest, deterministic driver digest, executor label, deterministic summary, and `awaiting-user-signoff` state.

The final run does not require:

- a prerequisite committed pre-edge run
- an independent LLM audit
- agent interaction transcripts
- provider session IDs
- OpenCode session state
- ChatGPT Work

Any release-content change after the final qualified revision invalidates acceptance and requires a new final qualification. Changes confined to `internal/release/qualification/` may record qualification evidence and user acceptance without changing release content.

# GitHub Actions execution and artifact handoff

`.github/workflows/release-qualification.yml` is the canonical deterministic executor for release PRs. It runs only for the release-please branch in the repository itself.

Before the edge exists it runs `pre-edge`. After the edge exists it runs `final`. The workflow does **not** push generated evidence with `GITHUB_TOKEN`; instead it uploads the exact qualification state transition as an artifact so the active repository-connected maintainer session can apply it. This keeps subsequent PR workflow runs attached to a normal repository commit rather than relying on recursive Actions pushes.

Each qualification artifact contains:

- `artifact-manifest.json` with `schema_version`, `kind`, exact `files`, and exact `delete` paths
- the complete bytes for every listed file at its repository-relative path

The maintainer must apply the manifest exactly. Do not rewrite, normalize, reinterpret, or mix unrelated changes into the qualification artifact commit.

The normal `.github/workflows/python-tests.yml` suite remains independently responsible for Backlog validation, installed-project task-board checks, and `internal/release/test.sh`. The release process does not duplicate that suite in the maintainer session.

# Session-neutral user acceptance

Qualification does not accept itself.

After the user explicitly approves the exact final run, a shell-capable environment may record acceptance with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

A normal repository-connected chat does not need shell access. It may create exactly this transient file on the release PR branch:

`internal/release/qualification/acceptance-request.json`

with exactly:

```json
{
  "identity": "user:<stable-identity>",
  "run_id": "<exact-final-run-id>",
  "schema_version": 1
}
```

Create that request only after explicit user approval. The Release qualification workflow validates the exact shape and invokes the maintained acceptance implementation in CI. It then uploads an acceptance artifact whose manifest includes the updated accepted qualification files and deletion of the transient request. The maintainer session applies that artifact exactly to finish the accepted state.

# Optional behavioral QA

The synthetic qualification vault may continue to contain agent-behavior scenarios. These can be run deliberately when a change materially affects routing, inbox behavior, semantic reconciliation, role maintenance, or another agent-interpreted contract.

Optional behavioral QA is not part of normal release acceptance. A future task may expose it through a generic protocol with ChatGPT Work, OpenCode, or other host adapters.

# Release PR merge gate

The Release PR policy verifies:

- all prior catalog releases have accepted release-quality state
- the target has a current `qualified-run` acceptance
- the accepted run was a clean `awaiting-user-signoff` final deterministic run
- source and target versions match the release edge
- target assets were assembled from the qualified repository revision
- the qualified revision belongs to the release PR
- only `internal/release/qualification/` changes occurred after final qualification

A release-content change after final qualification requires a new final deterministic run and fresh user acceptance.

# Publication

After the accepted release PR is merged, publication automation binds the final tag/version/revision, validates the recursive release catalog, runs deterministic repository/release checks, assembles reproducible assets, validates checksums and conformance, verifies attestations, and publishes the immutable GitHub release.

Publication must not bypass the pre-merge qualification gate.

# Failure handling

Any mandatory deterministic qualification failure leaves publication blocked.

Report the exact result and actionable finding. Do not weaken a deterministic check merely to make the release pass.

A failure in optional behavioral QA should be reported separately and judged according to whether it exposes a real release defect; optional QA does not automatically become release-gating evidence.
