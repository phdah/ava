# Phase 05: V1 Release Qualification

Turn Ava's format, roles, release tooling, OpenCode support, and conformance suite into tested prereleases and the first stable distribution.

## Core release gates

1. [x] [Define alpha acceptance and prerelease upgrade policy](01-define-alpha-acceptance-and-upgrade-policy.md)
2. [x] [Integrate release-please](02-integrate-release-please.md)
3. [x] [Publish `1.0.0-alpha.1`](03-publish-first-alpha-release.md)
4. [ ] [Dogfood the alpha and track findings](04-dogfood-alpha-and-track-findings.md)
5. [ ] [Publish the `1.0.0` release candidate](05-publish-release-candidate.md)
6. [ ] [Qualify and publish `1.0.0`](06-qualify-and-publish-v1.md)

Core progress: 3 of 6 complete.

## Supporting qualification tasks

1. [ ] [Build the synthetic v1 qualification vault](04a-build-synthetic-qualification-vault.md)
2. [ ] [Qualify and publish the corrective alpha](04b-qualify-and-publish-corrective-alpha.md)
3. [ ] [Stabilize the published release candidate](05a-stabilize-release-candidate.md)

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index.

- 1 pending finding
- 1 pending blocker
- 0 pending required-v1 findings
- 12 completed findings

[Clarify release semantic-impact assessment](dogfood/13-clarify-release-semantic-impact-assessment.md) is pending. Release completion must explicitly distinguish changes to Ava-managed behavior from possible incompatibility in existing project-owned context before deciding `semantic_review_required`.

[Avoid redundant routing for conversational follow-ups](dogfood/12-avoid-redundant-followup-routing.md) is complete. The managed-state gate remains unconditional, while normal turns may be roleless clarifications, same-role continuations, or fresh routing according to explicit boundaries that preserve finding 07's no-bypass guarantee.

[Define release-impact-based change types](dogfood/10-define-release-impact-based-change-types.md) is complete. Release classification follows supported distribution impact rather than implementation novelty or repository location.

[Normalize and enforce adjacent-edge release authoring](dogfood/11-enforce-adjacent-edge-release-authoring.md) is complete. The canonical alpha.12 catalog contains the retained adjacent graph, strict inherited-versus-proposed validation is required by release policy, and legacy cumulative authoring is disabled.

## Qualification policy

Every new release inherits the previous canonical catalog unchanged and authors exactly one adjacent edge. Older sources qualify through unique composition. Published legacy direct representations remain readable but cannot be selected for new authoring.

The dogfood umbrella remains pending until the user explicitly declares it complete. An empty findings backlog does not automatically advance or complete the core dogfood gate.

## Current active work

Resolve [Clarify release semantic-impact assessment](dogfood/13-clarify-release-semantic-impact-assessment.md) before completing another release PR. After the blocker is resolved, resume [Build the synthetic v1 qualification vault](04a-build-synthetic-qualification-vault.md), then continue the corrective immutable alpha qualification sequence and any newly discovered higher-priority dogfood findings. Finding 12's realistic multi-turn installed-project exercise remains a release qualification gate, not pending implementation work.

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
