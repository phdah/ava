# Phase 05: V1 Release Qualification

Turn the completed Ava format, managed roles, release tooling, OpenCode support, and conformance suite into a tested prerelease programme and the first supported stable distribution.

A prerelease is a real immutable Ava release, but it is not the first supported stable user state. Incompatible changes remain permitted between prereleases when clearly declared. Every supported prerelease transition must still be explicit and tested.

## Core release gates

The six core gates remain stable while dogfood findings grow in their own backlog.

1. [x] [Define alpha acceptance and prerelease upgrade policy](01-define-alpha-acceptance-and-upgrade-policy.md)
2. [x] [Integrate release-please](02-integrate-release-please.md)
3. [x] [Publish `1.0.0-alpha.1`](03-publish-first-alpha-release.md)
4. [ ] [Dogfood the alpha and track findings](04-dogfood-alpha-and-track-findings.md)
5. [ ] [Publish the `1.0.0` release candidate](05-publish-release-candidate.md)
6. [ ] [Qualify and publish `1.0.0`](06-qualify-and-publish-v1.md)

Core progress: 3 of 6 complete.

## Supporting qualification tasks

These tasks add executable evidence beneath the stable six core gates without renumbering them:

1. [ ] [Build the synthetic v1 qualification vault](04a-build-synthetic-qualification-vault.md) - Generate a reproducible 200-400-file raw corpus covering six coherent months of Adam's fictional private and work life in Stockholm.
2. [ ] [Qualify and publish the corrective alpha](04b-qualify-and-publish-corrective-alpha.md) - Publish the routing correction and collect immutable evidence for findings 03 through 08.
3. [ ] [Stabilize the published release candidate](05a-stabilize-release-candidate.md) - Repeat the complete generated-vault and lifecycle matrix before stable qualification.

The [repository-only synthetic qualification fixture](../../release/fixtures/synthetic-qualification-vault/) implements the reviewed 300-file deterministic baseline, five external image specifications, expected-outcome oracle, run-manifest schema, validators, and eight variant workspaces with explicit execution plans. Its task records reproducibility and repository-suite evidence; managed-state execution, external image finalization, and real OpenCode qualification remain pending.

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index to add and resolve bounded findings without renumbering the core release gates.

Current findings:

- 2 pending findings
- 1 pending blocker
- 1 pending required-v1 finding
- 9 completed findings

[Normalize and enforce adjacent-edge release authoring](dogfood/11-enforce-adjacent-edge-release-authoring.md) is the current next finding and blocks the next prerelease. It must normalize the active historical upgrade graph, make legacy direct source-to-target data read-only compatibility input, and require release-policy tests to prove that every future release inherits all prior edges unchanged and adds exactly one new adjacent edge.

[Define release-impact-based change types](dogfood/10-define-release-impact-based-change-types.md) remains pending `required-v1` work before release-candidate publication and follows finding 11.

[Compose semantic upgrades from adjacent release edges](dogfood/09-compose-semantic-upgrades-from-adjacent-edges.md) is complete in PR [#76](https://github.com/phdah/ava/pull/76). The accepted catalog model composes immutable adjacent edges, resolves managed and semantic paths separately, applies guidance exactly once in edge order, and rejects invalid or altered graphs before mutation. Published multi-edge qualification remains release evidence rather than pending implementation work.

[Define review sufficiency and termination criteria](dogfood/08-define-review-sufficiency-and-termination.md) is complete in its resolving implementation PR. Ordinary bounded review now defaults to a stable acceptance threshold, exhaustive audit requires explicit scope, and re-review must terminate successfully once material findings are resolved without new threshold-exceeding evidence.

[Enforce role routing before every response](dogfood/07-enforce-role-routing-before-every-response.md) is complete in its resolving implementation PR. The managed root router now requires state gating and explicit workflow or role routing before every substantive response, refusal, task execution, or project action. The corrective immutable prerelease must still repeat the warranty and unresolved-routing scenarios in a realistic fresh session.

[Enforce faithful inbox ingestion completion](dogfood/04-enforce-faithful-inbox-ingestion-completion.md) is complete through merged PR [#67](https://github.com/phdah/ava/pull/67) and published `1.0.0-alpha.10`. Repeated realistic ingestion, final count reconciliation, and independent semantic review remain corrective-release qualification evidence.

[Make knowledge hierarchy promotion predictable](dogfood/03-make-knowledge-hierarchy-promotion-predictable.md) is complete through merged PR #65. Repeated realistic ingestion and independent semantic review remain corrective-release qualification evidence.

[Restore complete prerelease upgrade coverage](dogfood/05-restore-complete-prerelease-upgrade-coverage.md) is complete through merged PR #60.

[Remove empty upgrade transaction containers](dogfood/06-remove-empty-upgrade-transaction-containers.md) is complete through PR #62.

The completed findings still requiring immutable-release evidence retain that obligation as release qualification follow-up, not pending implementation work.

[Repair installed context link resolution](dogfood/02-repair-installed-context-link-resolution.md) is complete after immutable alpha.7 validation loaded the complete Inbox Ingester required-reading chain from exact installed-project paths.

The dogfood umbrella remains pending until the user explicitly declares it complete. Having no pending blockers does not automatically make task 5 current.

## Finding and release ordering

- blockers are resolved before the next prerelease
- required-v1 findings name the exact release gate they block
- post-v1 dispositions require explicit user approval and durable rationale
- additional `alpha.N`, beta, or RC releases may be inserted when findings require another immutable validation cycle
- every added release declares and tests its supported source prereleases
- completed findings may still carry explicit immutable-release evidence before a release gate passes

## Qualification policy

The [alpha qualification policy](../../release/alpha-qualification.md) and its machine-readable fixture define the required gates, defect classes, protected impacts, prerelease support boundary, and publication approval.

The first alpha has no supported earlier Ava source. Later supported transitions must remain explicit and tested. Catalog-based releases compose retained adjacent edges into a unique supported path while preserving immutable edge and guidance identity. Finding 11 must make this the only active authoring model and require a strict inherited-versus-proposed catalog delta containing exactly one new adjacent edge.

## Release automation boundary

The [release automation contract](../../release/release-please.md) establishes Conventional Commit classification, version proposals, changelog updates, one release pull request, immutable tags, exact-SHA qualification, reproducible assembly, attestation, non-clobbering asset upload, and automatic publication after every gate passes.

Release automation does not replace reviewed compatibility declarations, deterministic assembly, source-revision binding, or dogfood completion authority.

## Phase entry baseline

Phase 5 begins only after:

- installed project paths are unambiguous
- OpenCode passes its maintained host-conformance fixture
- document update metadata is complete
- the Ava Maintenance role is implemented
- the complete validation, conformance, recovery, uninstall, and upgrade matrix passes

These entry conditions allowed Phase 5 to begin. Subsequent dogfooding exposed and resolved findings 02 through 09. Their required real-release checks remain qualification evidence where named, but they are not pending roadmap tasks.

## Current active work

The umbrella task remains [Dogfood the alpha and track findings](04-dogfood-alpha-and-track-findings.md).

Complete [normalize and enforce adjacent-edge release authoring](dogfood/11-enforce-adjacent-edge-release-authoring.md) next. No further prerelease may be prepared until the historical graph is normalized and required release-policy tests enforce exactly one new adjacent edge. Then resume the supporting qualification sequence and complete [release-impact-based change types](dogfood/10-define-release-impact-based-change-types.md) before release-candidate publication. Continue dogfooding until the user explicitly closes the umbrella or another higher-priority finding is added.

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
