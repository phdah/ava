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
  at: 2026-09-02T20:30:00+02:00
---

# Ava Release Publication Procedure

When the user asks to make, prepare, review, accept, merge, publish, or qualify an Ava release, the Ava Internal Maintainer must follow this procedure.

The normal release gate is intentionally deterministic. Synthetic consumer-agent behavior is optional QA, not mandatory publication evidence.

All non-CI qualification for the currently validated workflow runs in **ChatGPT Work Cloud**. GitHub Actions continues to own the repository checks that already run in CI.

The concrete Work commands are documented in [ChatGPT Work Cloud deterministic qualification](qualification-work.md).

# Release flow

1. Let release-please determine the target version and release PR.
2. Configure the active qualification pair as the exact immutable previous published release -> exact local target version.
3. Start from the exact clean release PR revision in ChatGPT Work Cloud and acquire/verify the exact previous release assets.
4. Generate the finalized synthetic qualification vault and a repository-external test boundary in Work Cloud.
5. Assemble the provisional target with `assemble-candidate.sh --phase edge-independent`.
6. Run `qualify-release.sh pre-edge`. This is a cheap deterministic fail-fast preflight only; it writes no committed qualification evidence.
7. If the pre-edge preflight fails, stop before semantic review and edge authoring.
8. Review the exact previous-to-target managed delta and complete the project-owned semantic-impact assessment, including an explicit decision and rationale.
9. Author exactly one adjacent release record for `<previous> -> <target>`, plus only the guidance, deterministic migrations, and retirement decisions introduced by that edge.
10. Require the release PR's normal GitHub Actions checks to pass.
11. Assemble the reviewed target with `assemble-candidate.sh --phase edge-dependent` from the new exact release PR revision.
12. Use a new Work Cloud execution root and run `qualify-release.sh final`.
13. The final deterministic qualification reruns the fail-fast checks and additionally proves the authentic source-to-target edge, deterministic upgrade, interrupted resume, abort, rollback, project-owned preservation, and final asset/revision identity.
14. If final qualification fails, stop and report the exact deterministic finding.
15. If final qualification passes, it writes one authoritative final run under `internal/release/qualification/runs/` and enters `awaiting-user-signoff`.
16. Present the final deterministic evidence and required GitHub Actions results to the user.
17. Only after explicit user approval, run `accept-release-qualification.sh` and commit the resulting qualification-state changes to the release PR.
18. Require the Release PR policy check to pass.
19. Merge only after the adjacent edge, semantic-impact decision, final deterministic qualification, required GitHub Actions checks, and user acceptance are all accepted.
20. Publication automation creates and verifies the immutable release.

# Qualification boundary

Mandatory release qualification uses **zero delegated qualification agents**.

The release-maintainer Work session may reason about the release itself, especially the semantic-impact assessment and adjacent-edge authoring. It does not spawn synthetic consumer agents as a publication requirement.

The mandatory deterministic checks cover:

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

The pre-edge run exists only to avoid wasting release-maintainer effort on an obviously broken candidate.

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

It must be assembled and executed from the exact final release PR revision after edge authoring. The run record binds that revision to the local target asset identity, source release identity, qualification matrix digest, driver digest, deterministic summary, and `awaiting-user-signoff` state.

The final run does not require:

- a prerequisite committed pre-edge run
- an independent LLM audit
- agent interaction transcripts
- provider session IDs
- OpenCode session state

Any release-content change after the final qualified revision invalidates acceptance and requires a new final qualification. Changes confined to `internal/release/qualification/` may record qualification evidence and user acceptance without changing release content.

# GitHub Actions boundary

Repository checks that already run on pull requests remain GitHub Actions responsibilities. In particular, `.github/workflows/python-tests.yml` runs internal Backlog validation, installed-project task-board checks, and `internal/release/test.sh`, which exercises the repository Python/unit suite.

The Work release task inspects and requires those checks to pass. It **does not need to rerun** the full repository test suite inside Work as qualification evidence. A Work-side rerun is diagnostic only when investigating a failure.

# Optional behavioral QA

The synthetic qualification vault may continue to contain agent-behavior scenarios. These can be run deliberately when a change materially affects routing, inbox behavior, semantic reconciliation, role maintenance, or another agent-interpreted contract.

Optional behavioral QA is not part of normal release acceptance. A future task may expose it through a generic protocol with ChatGPT Work, OpenCode, or other host adapters.

# User acceptance

Qualification does not accept itself.

After the user explicitly approves the final deterministic evidence, record that decision with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

The accepted run must still be bound to the exact release PR revision and local target assets.

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
