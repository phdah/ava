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
  at: 2026-09-02T12:45:00+02:00
---

# Ava Release Publication Procedure

When the user asks to make, prepare, review, accept, merge, publish, or qualify an Ava release, the Ava Internal Maintainer must follow this procedure.

Every Ava release uses the same two-phase qualification flow. Edge-independent qualification runs before adjacent-edge authoring. Edge-dependent qualification, independent audit, and explicit user acceptance remain mandatory before the release-please PR may merge.

# Release flow

1. Let release-please determine the target version and release PR.
2. Configure the qualification active pair as exact immutable previous published release -> exact local target version.
3. From the clean release PR revision, assemble a provisional target with `assemble-candidate.sh --phase edge-independent`.
4. Run `qualify-release.sh --phase edge-independent` against that provisional target.
5. If the early result is `failed` or `needs-review`, stop. Report the exact result and findings. Do not perform managed-delta review or author the adjacent catalog, guidance, migrations, or source-retirement state.
6. When the early result is `passed`, commit its compact `phase-runs/` evidence and `phase-state.json` to the release PR.
7. Review the exact previous-to-target managed delta and complete the project-owned semantic-impact assessment.
8. Author exactly one adjacent release record for `<previous> -> <target>`, plus only the guidance, migrations, and retirement decisions introduced by that edge.
9. Run release-PR validation and the complete repository test suite.
10. Assemble the reviewed target with `assemble-candidate.sh --phase edge-dependent`.
11. Run `qualify-release.sh --phase edge-dependent`. The command must first prove the committed early result is for the same source and target and was not invalidated by intervening changes.
12. Any final `failed` or `needs-review` result leaves the release PR blocked. Report the result and findings, then ask whether the user wants those findings recorded as bounded Backlog.md tasks on `main`. Create nothing unless the user explicitly agrees.
13. When the final run reaches `awaiting-user-signoff`, present the complete two-phase evidence to the user.
14. Only after explicit user approval, record acceptance with `accept-release-qualification.sh` and commit the qualification-state changes to the release PR.
15. Require the Release PR policy check to pass.
16. Merge only after the release PR content, semantic-impact decision, both qualification phases, and user acceptance are all accepted.
17. Publication automation creates and verifies the immutable release.

# Early phase and fail-fast boundary

The early phase validates target behavior that does not depend on an authored source-to-target edge. The maintained qualification matrix marks every scenario with `qualification_phase`.

The edge-independent phase contains fresh install, mature install, registered routing, calendar, ambiguity, inbox ingestion and semantic audit, managed-damage detection, and uninstall/reinstall checks. It intentionally excludes authentic upgrade resume, abort, rollback, finalization, and semantic reconciliation.

Assemble and run it with:

```sh
early_assets="$(internal/release/assemble-candidate.sh --phase edge-independent)"
internal/release/qualify-release.sh \
  --phase edge-independent \
  --target-assets "$early_assets"
```

The provisional candidate is assembled from the current clean release PR revision without `internal/release/catalogs/<target>.json`. Its release identity remains pinned to the same previous published release and target version used by the final phase.

A clean early result is reusable evidence, not acceptance. Commit the compact early evidence before edge authoring so the later phase can prove ordering and revision ancestry.

# Adjacent release state

Only after the early phase passes may the maintainer perform managed-delta review and adjacent-edge authoring.

The authored upgrade history under `internal/release/catalogs/` is immutable. Each release adds exactly one record:

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

A managed behavior change alone does not decide semantic impact, and the presence or absence of a deterministic project-file migration does not decide it either. Tooling must not guess semantic migration need from changed paths or categories.

# Early-result invalidation

The final phase may reuse the early result only if the early qualified revision is an ancestor of the final qualified revision and every intervening change is limited to:

- compact evidence for the exact early run under `internal/release/qualification/phase-runs/`
- `internal/release/qualification/phase-state.json`
- `internal/release/catalogs/<target>.json`
- `internal/release/guidance/<target>/...`
- `internal/release/migrations/...`

Any other change invalidates the early evidence and requires a new edge-independent run before edge authoring can continue. In particular, changes to templates, distribution assets, installer behavior, release notes, fixtures, matrix classification, qualification tooling, or other candidate inputs must rerun the early phase.

The phase gate also verifies that the target adjacent catalog and target guidance did not exist at the early qualified revision. This prevents an operator from running the early command after doing the expensive edge-authoring work and still claiming fail-fast coverage.

# Final edge-dependent qualification

After the adjacent edge is complete, assemble and run:

```sh
final_assets="$(internal/release/assemble-candidate.sh --phase edge-dependent)"
internal/release/qualify-release.sh \
  --phase edge-dependent \
  --target-assets "$final_assets"
```

The final candidate uses the reviewed adjacent catalog. Before the first scenario runs, qualification requires:

- one committed clean edge-independent prerequisite for the active pair
- identical source release identity across both phases
- identical target version across both phases
- early target assets bound to the early repository revision
- final target assets bound to the final repository revision
- an authentic final source-to-target upgrade edge
- only allowed edge-authoring changes between the qualified revisions

The edge-dependent phase runs authentic resume, abort, rollback, finalization, and semantic-reconciliation scenarios. It captures its own session inventory and independent audit.

Terminal final states are:

- `failed`
- `needs-review`
- `awaiting-user-signoff`

Only `awaiting-user-signoff` may proceed to user acceptance.

# Qualification evidence boundary

`qualify-release.sh` owns the OpenCode access required for repository-external temporary evidence. It creates a unique external operation root and passes the exact required roots through the maintained OpenCode adapter. Qualification must not rely on user-global OpenCode permissions or a global auto-approval mode.

Raw workspaces, release assets, transcripts, and generated roots remain outside Git. Compact early evidence is written under `internal/release/qualification/phase-runs/`; compact final evidence and release-quality state are written under `internal/release/qualification/runs/` and `current-state.json`.

The independent audit runs for both phases. It is scoped to scenarios present in the current phase and does not treat the other phase as missing evidence.

# User acceptance

Qualification does not accept itself.

After the user explicitly approves the complete evidence, record that decision with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

The acceptance entry point validates the two-phase prerequisite chain before recording the existing final run signoff and `release_acceptance` entry.

Commit the resulting files under `internal/release/qualification/` to the release PR branch. The target is recorded as `accepted` with `basis: qualified-run`.

Historical releases through `v1.0.0-alpha.14` remain backfilled as accepted with `basis: historical-backfill`; this preserves history without claiming those releases ran the current system.

# Release PR merge gate

The Release PR policy check must fail until qualification is accepted. It verifies both the existing final acceptance requirements and the phase-chain requirements:

- all prior catalog releases have accepted release-quality state
- the target has a current `qualified-run` acceptance
- the final run is clean and explicitly signed off
- the final run is `edge-dependent`
- it references one clean `edge-independent` prerequisite
- both phases use the same immutable source and target version
- the early edge was absent when early qualification ran
- no invalidating change occurred between the early and final qualified revisions
- final target assets were assembled from the final qualified revision
- the final qualified revision belongs to the release PR
- only `internal/release/qualification/` changes occurred after final qualification

A release-content change after final qualification requires new applicable qualification evidence and fresh user acceptance. Acceptance is never carried forward blindly across changed release content.

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

For either qualification phase, report the exact result and each actionable finding. Do not modify repository or release content automatically to make the run pass.

After reporting findings, ask whether the user wants them recorded as bounded native Backlog.md tasks on `main`. Create no tasks without explicit approval. Task creation is tracking only and does not accept qualification or advance release state.

If the user directs a repository correction, treat it as ordinary repository work. The invalidation rules determine whether the edge-independent phase must rerun, and any final release-content correction requires a new final qualification and fresh user acceptance.
