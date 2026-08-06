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

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index to add and resolve bounded findings without renumbering the core release gates.

Current findings:

- 2 pending blockers
- 2 pending required-v1 findings
- 1 completed finding

Current next actionable finding: [Restore complete prerelease upgrade coverage](dogfood/05-restore-complete-prerelease-upgrade-coverage.md).

[Repair installed context link resolution](dogfood/02-repair-installed-context-link-resolution.md) remains pending only for separate validation against published alpha.7 assets. Its repository implementation is complete, so it does not prevent the next actionable implementation finding from proceeding.

The dogfood umbrella remains pending until the user explicitly declares it complete. Having no pending findings does not automatically make task 5 current.

## Finding and release ordering

- blockers are resolved before the next prerelease
- required-v1 findings name the exact release gate they block
- post-v1 dispositions require explicit user approval and durable rationale
- additional `alpha.N`, beta, or RC releases may be inserted when findings require another immutable validation cycle
- every added release declares and tests its supported source prereleases

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

These entry conditions allowed Phase 5 to begin. Subsequent dogfooding exposed two pending release blockers: the assembled installed-path defect tracked by [finding 02](dogfood/02-repair-installed-context-link-resolution.md), whose implementation now awaits alpha.7 validation, and the stranded prerelease upgrade support tracked by [finding 05](dogfood/05-restore-complete-prerelease-upgrade-coverage.md). These blockers do not rewind completed phases, but they must be resolved before another prerelease.

## Current active work

The umbrella task is [Dogfood the alpha and track findings](04-dogfood-alpha-and-track-findings.md).

The current executable implementation task is [Restore complete prerelease upgrade coverage](dogfood/05-restore-complete-prerelease-upgrade-coverage.md).

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
