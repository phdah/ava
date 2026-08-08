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
2. [ ] [Qualify and publish the corrective alpha](04b-qualify-and-publish-corrective-alpha.md) - Publish the routing correction and collect immutable evidence for findings 03 through 07.
3. [ ] [Stabilize the published release candidate](05a-stabilize-release-candidate.md) - Repeat the complete generated-vault and lifecycle matrix before stable qualification.

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index to add and resolve bounded findings without renumbering the core release gates.

Current findings:

- 2 pending findings
- 1 pending blocker
- 1 pending required-v1 finding
- 6 completed findings

[Enforce role routing before every response](dogfood/07-enforce-role-routing-before-every-response.md) is the current pending blocker. The managed root router must not let an agent bypass state checks and role routing because a request appears unrelated to its generic host persona.

[Define review sufficiency and termination criteria](dogfood/08-define-review-sufficiency-and-termination.md) is a pending `required-v1` finding that must be completed before the release candidate. It does not block the corrective prerelease required to qualify finding 07.

[Enforce faithful inbox ingestion completion](dogfood/04-enforce-faithful-inbox-ingestion-completion.md) is complete through merged PR [#67](https://github.com/phdah/ava/pull/67) and published `1.0.0-alpha.10`. Repeated realistic ingestion, final count reconciliation, and independent semantic review remain corrective-release qualification evidence.

[Make knowledge hierarchy promotion predictable](dogfood/03-make-knowledge-hierarchy-promotion-predictable.md) is complete through merged PR #65. Repeated realistic ingestion and independent semantic review remain corrective-release qualification evidence.

[Restore complete prerelease upgrade coverage](dogfood/05-restore-complete-prerelease-upgrade-coverage.md) is complete through merged PR #60.

[Remove empty upgrade transaction containers](dogfood/06-remove-empty-upgrade-transaction-containers.md) is complete through merged PR #62.

The completed findings still requiring corrective immutable-release evidence retain that obligation as release qualification follow-up, not pending implementation work.

[Repair installed context link resolution](dogfood/02-repair-installed-context-link-resolution.md) is complete after immutable alpha.7 validation loaded the complete Inbox Ingester required-reading chain from exact installed-project paths.

The dogfood umbrella remains pending until the user explicitly declares it complete. Having no pending findings does not automatically make task 5 current.

## Finding and release ordering

- blockers are resolved before the next prerelease
- required-v1 findings name the exact release gate they block
- post-v1 dispositions require explicit user approval and durable rationale
- additional `alpha.N`, beta, or RC releases may be inserted when findings require another immutable validation cycle
- every added release declares and tests its supported source prereleases
- completed findings may still carry explicit release qualification follow-up without returning to pending status

## Qualification policy

The [alpha qualification policy](../../release/alpha-qualification.md) and its machine-readable fixture define the required gates, defect classes, protected impacts, prerelease support boundary, and publication approval.

The first alpha has no supported earlier Ava source. Later supported transitions must be explicit release-manifest upgrade edges and must preserve a tested path from the latest supported prerelease through RC to stable `1.0.0`.

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

These entry conditions allowed Phase 5 to begin. Subsequent dogfooding exposed and validated the installed-path defect tracked by completed [finding 02](dogfood/02-repair-installed-context-link-resolution.md). The semantic hierarchy contract from completed [finding 03](dogfood/03-make-knowledge-hierarchy-promotion-predictable.md), faithful ingestion contract from completed [finding 04](dogfood/04-enforce-faithful-inbox-ingestion-completion.md), prerelease support fix from completed [finding 05](dogfood/05-restore-complete-prerelease-upgrade-coverage.md), and terminal transaction cleanup from completed [finding 06](dogfood/06-remove-empty-upgrade-transaction-containers.md) are implemented. Their required real corrective-release checks remain qualification evidence where named, but they are not pending roadmap tasks.

## Current active work

The umbrella task is [Dogfood the alpha and track findings](04-dogfood-alpha-and-track-findings.md).

[Enforce role routing before every response](dogfood/07-enforce-role-routing-before-every-response.md) is the current bounded implementation finding. After it is resolved, build the [synthetic qualification vault](04a-build-synthetic-qualification-vault.md) and [qualify the corrective alpha](04b-qualify-and-publish-corrective-alpha.md). Then complete [review sufficiency and termination criteria](dogfood/08-define-review-sufficiency-and-termination.md) before release-candidate publication, and continue dogfooding until the user explicitly closes the umbrella or another finding is added.

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
