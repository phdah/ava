# Phase 05: V1 Release Qualification

Turn the completed Ava format, managed roles, release tooling, OpenCode support, and conformance suite into a tested prerelease programme and the first supported stable distribution.

A prerelease is a real immutable Ava release, but it is not the first supported stable user state. Incompatible changes remain permitted between prereleases when clearly declared. Every supported prerelease transition must still be explicit and tested.

## Tasks

1. [x] [Define alpha acceptance and prerelease upgrade policy](01-define-alpha-acceptance-and-upgrade-policy.md)
2. [x] [Integrate release-please](02-integrate-release-please.md)
3. [ ] [Publish `1.0.0-alpha.1`](03-publish-first-alpha-release.md)
4. [ ] [Dogfood the alpha and track findings](04-dogfood-alpha-and-track-findings.md)
5. [ ] [Publish the `1.0.0` release candidate](05-publish-release-candidate.md)
6. [ ] [Qualify and publish `1.0.0`](06-qualify-and-publish-v1.md)

Alpha findings may add bounded task files to this phase. Insert blocking fixes before task 5 and update this index rather than treating the original six tasks as immutable.

Additional `alpha.N`, beta, or RC releases may be added when the findings require another published validation cycle. Each added release must have its own bounded task and declared upgrade policy.

## Qualification policy

The [alpha qualification policy](../../release/alpha-qualification.md) and its machine-readable fixture define the required gates, defect classes, protected impacts, prerelease support boundary, and exact publication approval for `1.0.0-alpha.1`.

The first alpha has no supported earlier Ava source. Later supported transitions must be explicit release-manifest upgrade edges and must preserve a tested path from the latest supported prerelease through RC to stable `1.0.0`.

## Release automation boundary

The [release automation contract](../../release/release-please.md) now establishes Conventional Commit classification, version proposals, changelog updates, one release pull request, immutable tags, draft release preparation, exact-SHA qualification, reproducible assembly, attestation, and non-clobbering asset upload.

Release automation does not replace qualification, deterministic assembly, source-revision binding, or explicit publication approval.

## Entry conditions

Phase 5 begins only after:

- installed project paths are unambiguous
- OpenCode passes its maintained host-conformance fixture
- document update metadata is complete
- the Ava Maintenance role is implemented
- the complete validation, conformance, recovery, uninstall, and upgrade matrix passes

All entry conditions are complete.

## Current active task

[Publish `1.0.0-alpha.1`](03-publish-first-alpha-release.md).

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
