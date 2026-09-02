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
  at: 2026-09-02T17:30:00+02:00
---

# Ava Release Publication Procedure

When the user asks to make, prepare, review, accept, merge, publish, or qualify an Ava release, the Ava Internal Maintainer must follow this procedure.

Every release uses the same fail-fast two-phase qualification chain. All qualification work that is not already executed by GitHub Actions runs in **ChatGPT Work Cloud**, using OpenAI-hosted filesystem/shell execution and fresh Work subagents. No qualification step requires OpenCode or the user's computer.

The exact Work execution loop is defined in [ChatGPT Work Cloud qualification execution](qualification-work.md).

# Release flow

1. Let release-please determine the target version and release PR.
2. Configure the qualification active pair as exact immutable previous published release -> exact local target version.
3. Start a ChatGPT Work Cloud task from the exact clean release PR revision. Do not use Work Local, Codex Local, OpenCode, or a developer terminal.
4. Inside Work Cloud, download and verify the exact immutable previous release assets, generate the finalized synthetic qualification vault, and create the external test boundary.
5. Assemble the provisional target with `assemble-candidate.sh --phase edge-independent`.
6. Run the edge-independent Work qualification protocol with `qualify-release.sh init`, repeated `advance` calls and fresh scenario subagents, then a fresh independent audit subagent and `finalize`.
7. If the early result is `failed` or `needs-review`, stop. Report the exact result and findings. Do not perform managed-delta review or author the adjacent catalog, guidance, migrations, or source-retirement state.
8. When the early result is `passed`, commit its compact `phase-runs/` evidence and `phase-state.json` to the release PR through the connected GitHub action.
9. Review the exact previous-to-target managed delta and complete the project-owned semantic-impact assessment.
10. Author exactly one adjacent release record for `<previous> -> <target>`, plus only the guidance, migrations, and retirement decisions introduced by that edge.
11. Run release-PR validation and the complete repository test suite.
12. Start the final qualification from the new exact release PR revision in a new Work Cloud run root. Do not reuse early scenario workspaces.
13. Assemble the reviewed target with `assemble-candidate.sh --phase edge-dependent`.
14. Run the edge-dependent Work qualification protocol. Initialization must first prove the committed early result is for the same source/target and was not invalidated by intervening changes.
15. Any final `failed` or `needs-review` result leaves the release PR blocked. Report the result and findings, then ask whether the user wants those findings recorded as bounded Backlog.md tasks on `main`.
16. When the final run reaches `awaiting-user-signoff`, present the complete two-phase Work evidence to the user.
17. Only after explicit user approval, record acceptance with `accept-release-qualification.sh` and commit the resulting qualification-state changes to the release PR.
18. Require the Release PR policy check to pass.
19. Merge only after the release PR content, semantic-impact decision, both qualification phases, independent audits, and user acceptance are all accepted.
20. Publication automation creates and verifies the immutable release.

# ChatGPT Work Cloud boundary

Qualification runs in a Work cloud task on web/mobile or a cloud Work task on desktop. It must not open a local folder for the qualification operation.

Required capabilities are:

- cloud filesystem and shell execution
- network access for the exact GitHub repository and release assets
- connected GitHub write access for committing compact evidence to the release PR
- fresh Work subagent delegation
- shared cloud filesystem access between the parent task and those subagents

If any required Work capability is unavailable, stop. Do not move the operation to local compute.

# Agent execution model

`qualify-release.sh` is not an agent runner. It is a deterministic Work protocol driver.

The parent Work task repeatedly calls `advance`. Deterministic scenarios run directly in the Work cloud shell. When semantic behavior is required, the command emits one `SUBAGENT_REQUIRED` request bound to an exact isolated workspace and prompt.

The parent delegates that exact request to one fresh Work subagent. The subagent reads and follows the installed Ava project, performs the user prompt, writes the declared structured response into the shared Work filesystem, and returns control. The parent calls `advance` again, which verifies deterministic postconditions before continuing.

Scenario subagents must not use web search, cloud browser, plugins, apps, MCPs, other repositories, memory, or user-local files. This prevents unrelated connected context from entering qualification.

After all scenarios pass mechanically, `audit-request` emits one independent read-only request. A new fresh Work subagent performs that audit and writes only the audit response. `finalize` validates audit immutability and writes compact repository evidence.

# Early phase and fail-fast boundary

The edge-independent phase validates target behavior that does not depend on an authored source-to-target edge. The maintained qualification matrix marks every scenario with `qualification_phase`.

The provisional candidate is assembled from the current clean release PR revision without `internal/release/catalogs/<target>.json`. Its release identity remains pinned to the same previous published release and target version used by the final phase.

A clean early result is reusable evidence, not acceptance. Commit the compact early evidence before edge authoring so the final phase can prove ordering and revision ancestry.

# Adjacent release state

Only after the early phase passes may the maintainer perform managed-delta review and adjacent-edge authoring.

The authored upgrade history under `internal/release/catalogs/` is immutable. Each release adds exactly one record:

`internal/release/catalogs/<target>.json`

That record contains only the immediately previous-to-target edge, migrations introduced by that edge, semantic guidance introduced by that edge, and source-retirement decisions introduced by that release.

Existing release records must not be rewritten or copied into cumulative state.

# Project-owned semantic-impact assessment

For the exact previous-to-target managed delta, answer:

1. **Managed delta:** Which managed contracts, behavior, authority, routing, validation, metadata, paths, or lifecycle rules changed?
2. **Project-owned compatibility:** Could valid active project-owned context remain structurally unchanged yet become conflicting, misleading, semantically invalid, or behaviorally incompatible under the target?
3. **Required reconciliation:** If yes, which bounded project-owned concepts must be inspected or reconciled before semantic compatibility may advance?

Set `semantic_review_required: true` only when project-owned semantic reconciliation may be required. When true, transition-local guidance must define affected concepts, bounded discovery conditions, and completion criteria.

A managed behavior change alone does not decide semantic impact, and the presence or absence of a deterministic project-file migration does not decide it either.

# Early-result invalidation

The final phase may reuse the early result only if the early qualified revision is an ancestor of the final qualified revision and every intervening change is limited to:

- compact evidence for the exact early run under `internal/release/qualification/phase-runs/`
- `internal/release/qualification/phase-state.json`
- `internal/release/catalogs/<target>.json`
- `internal/release/guidance/<target>/...`
- `internal/release/migrations/...`

Any other change invalidates the early evidence and requires a new edge-independent Work qualification before edge authoring can continue.

The phase gate also verifies that the target adjacent catalog and target guidance did not exist at the early qualified revision.

# Final edge-dependent qualification

The final phase uses a new Work cloud run root and the reviewed adjacent catalog.

Before the first final scenario runs, qualification requires:

- one committed clean edge-independent prerequisite for the active pair
- identical source release identity across both phases
- identical target version across both phases
- early target assets bound to the early repository revision
- final target assets bound to the final repository revision
- an authentic final source-to-target upgrade edge
- only allowed edge-authoring changes between the qualified revisions

Terminal final states are `failed`, `needs-review`, and `awaiting-user-signoff`. Only `awaiting-user-signoff` may proceed to user acceptance.

# Qualification evidence boundary

Raw scenario workspaces, downloaded release assets, generated fixture data, and Work protocol request files remain in the Work cloud run root and outside Git.

Compact early evidence is written under `internal/release/qualification/phase-runs/`. Compact final evidence and release-quality state are written under `internal/release/qualification/runs/` and `current-state.json`.

Compact Work evidence is independent of ChatGPT thread IDs and product-internal session identifiers. It records exact prompt/model/workspace identity, ordered required-reading evidence, structured subagent responses, deterministic results, independent audit, and exact repository/release hashes.

# User acceptance

Qualification does not accept itself.

After the user explicitly approves the complete evidence, record that decision with:

```sh
internal/release/accept-release-qualification.sh \
  --identity user:<stable-identity> \
  [--run-id <run-id>]
```

The acceptance entry point validates the two-phase prerequisite chain before recording the final run signoff and `release_acceptance` entry.

# Release PR merge gate

The Release PR policy must fail until qualification is accepted. It verifies:

- all prior catalog releases have accepted release-quality state
- the target has a current `qualified-run` acceptance
- the final run is clean and explicitly signed off
- the final run is `edge-dependent`
- it references one clean `edge-independent` prerequisite
- both phases use the same immutable source and target version
- the early edge was absent when early qualification ran
- no invalidating change occurred between early and final qualification
- final target assets were assembled from the final qualified revision
- the final qualified revision belongs to the release PR
- only `internal/release/qualification/` changes occurred after final qualification

A release-content change after final qualification requires new applicable Work qualification evidence and fresh user acceptance.

# Publication

After the accepted release PR is merged, publication automation binds the final tag/version/revision, validates the recursive release catalog, runs deterministic repository/release checks, assembles reproducible assets, validates checksums and conformance, verifies attestations, and publishes the immutable GitHub release.

Publication must not bypass the pre-merge qualification gate.

# Failure handling

Any qualification failure leaves publication blocked.

Report the exact result and each actionable finding. Do not modify repository or release content automatically to make the run pass.

After reporting findings, ask whether the user wants them recorded as bounded native Backlog.md tasks on `main`. Create no tasks without explicit approval.

If the user directs a repository correction, treat it as ordinary repository work. The invalidation rules determine whether the early phase must rerun, and any final release-content correction requires new final Work qualification and fresh user acceptance.
