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
  at: 2026-08-17T12:26:00+02:00
---

# Ava Release Publication Procedure

When the user asks to make, prepare, review, accept, merge, publish, or qualify an Ava release, the Ava Internal Maintainer must follow this procedure.

Every Ava release uses the same flow. Full `qualify-release.sh` qualification and explicit user acceptance are mandatory before the release-please PR may merge.

# Release flow

1. Let release-please determine the target version and release PR.
2. Review the exact previous-to-target managed delta.
3. Complete the project-owned semantic-impact assessment.
4. Author exactly one adjacent release record for `<previous> -> <target>`.
5. Run release-PR validation and the complete repository test suite.
6. Assemble the exact target release assets from a clean release PR revision.
7. Configure the qualification active pair as exact published previous release -> exact local target.
8. Run `qualify-release.sh` against those local target assets.
9. Any `failed` or `needs-review` result leaves the release PR blocked; report it to the user without modifying repository or release content to make it pass.
10. When the run reaches `awaiting-user-signoff`, present the evidence to the user.
11. Only after explicit user approval, record acceptance with `accept-release-qualification.sh` and commit the qualification-state changes to the release PR.
12. Require the Release PR policy check to pass.
13. Merge only after the release PR content, semantic-impact decision, qualification evidence, and user acceptance are all accepted.
14. Publication automation creates and verifies the immutable release.

Any non-qualification-state change after the qualified revision invalidates acceptance and requires requalification.

# Adjacent release state

The authored upgrade history under `internal/release/catalogs/` is immutable.

Each release adds exactly one record:

`internal/release/catalogs/<target>.json`

That record contains only:

- the immediately previous-to-target edge
- migrations introduced by that edge
- semantic guidance introduced by that edge
- source-retirement decisions introduced by that release

Existing release records must not be rewritten or copied into cumulative state.

# Project-owned semantic-impact assessment

For the exact previous-to-target managed delta, answer:

1. **Managed delta:** Which managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed?
2. **Project-owned compatibility:** Could valid active project-owned context remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible under the target?
3. **Required reconciliation:** If yes, which bounded project-owned concepts must be inspected or reconciled before semantic compatibility may advance?

Set `semantic_review_required: true` only when project-owned semantic reconciliation may be required. When true, transition-local guidance must define affected concepts, bounded discovery conditions, and completion criteria.

A managed behavior change alone does not decide semantic impact, and the presence or absence of a deterministic project-file migration does not decide it either. The release PR must preserve the reviewed rationale for the decision.

Tooling must not guess semantic migration need from changed file paths, managed behavior categories, or the presence or absence of deterministic project-file migrations.

This decision is separate from release qualification. Full release qualification is always required.

# Release PR preparation

Before qualification, the release PR must contain the complete candidate release content:

- target version and release-please identity
- one adjacent release record
- reviewed semantic-impact decision and any required guidance
- all intended release behavior changes
- passing deterministic release validation and repository tests

Prepare the qualification pair so the source is the exact immutable previous published release and the target is local with the release PR target version.

Assemble the target assets from the clean release PR revision being qualified. The local release manifest `source_revision` must equal that revision.

# Mandatory qualification

Run:

```sh
internal/release/qualify-release.sh \
  --target-assets /absolute/path/to/target/assets
```

The operation must run the maintained 17-scenario matrix, capture all top-level and nested OpenCode sessions, execute the independent audit, and write compact evidence.

Terminal states are:

- `failed`
- `needs-review`
- `awaiting-user-signoff`

Only `awaiting-user-signoff` may proceed to user acceptance.

# User acceptance

Qualification does not accept itself.

After the user explicitly approves the evidence, record that decision with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

Commit the resulting files under `internal/release/qualification/` to the release PR branch.

The release-quality ledger in `current-state.json` records the target as `accepted` with `basis: qualified-run`.

Historical releases through `v1.0.0-alpha.14` are backfilled as accepted with `basis: historical-backfill`; this preserves the historical release chain without claiming those releases ran the current qualification system.

# Release PR merge gate

The Release PR policy check must fail until qualification is accepted.

It verifies:

- all prior catalog releases have accepted release-quality state
- the target has a current `qualified-run` acceptance
- the referenced run is clean and explicitly signed off
- run source and target match the release edge
- target assets were assembled from the qualified repository revision
- the qualified revision belongs to the release PR
- only `internal/release/qualification/` changed after qualification

A code, template, distribution, catalog, guidance, fixture, matrix, or other release-content change after qualification requires a new qualification run and new user acceptance.

# Publication

After the accepted release PR is merged, publication automation:

1. binds the final tag, version, channel, and source revision
2. validates the complete recursive release catalog
3. runs deterministic repository/release checks
4. assembles reproducible release assets
5. validates release conformance and checksums
6. creates/verifies attestations
7. publishes the immutable GitHub release without replacing existing assets

Publication must not bypass the pre-merge qualification gate.

Post-publication verification checks immutable tag, asset inventory, checksums, attestations, and release identity. It does not replace or retroactively grant pre-merge qualification acceptance.

# Failure handling

Any failure leaves publication blocked. Existing tags and assets are never moved, overwritten, or reused.

A `failed` or `needs-review` qualification result leaves the release PR unmerged. Report the exact result to the user. Do not modify repository or release content to resolve it.

If the user directs a repository change in response, treat it as ordinary repository work outside the qualification loop: it requires its own review, and any resulting release-content change requires a new candidate, a new full qualification run, and fresh user acceptance.

Never carry acceptance forward across changed release content.
