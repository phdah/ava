# Phase 05: V1 Release Qualification

Turn the completed Ava format, managed roles, release tooling, OpenCode support, and conformance suite into a tested prerelease programme and the first supported stable distribution.

A prerelease is a real immutable Ava release, but it is not the first supported stable user state. Incompatible changes remain permitted between prereleases when clearly declared. Every supported prerelease transition must still be explicit and tested.

## Tasks

1. [x] [Define alpha acceptance and prerelease upgrade policy](01-define-alpha-acceptance-and-upgrade-policy.md)
2. [ ] [Publish `1.0.0-alpha.1`](02-publish-first-alpha-release.md)
3. [ ] [Dogfood the alpha and track findings](03-dogfood-alpha-and-track-findings.md)
4. [ ] [Publish the `1.0.0` release candidate](04-publish-release-candidate.md)
5. [ ] [Qualify and publish `1.0.0`](05-qualify-and-publish-v1.md)

Alpha findings may add bounded task files to this phase. Insert blocking fixes before task 4 and update this index rather than treating the original five tasks as immutable.

Additional `alpha.N`, beta, or RC releases may be added when the findings require another published validation cycle. Each added release must have its own bounded task and declared upgrade policy.

## Qualification policy

The [alpha qualification policy](../../release/alpha-qualification.md) and its machine-readable fixture define the required gates, defect classes, protected impacts, prerelease support boundary, and exact publication approval for `1.0.0-alpha.1`.

The first alpha has no supported earlier Ava source. Later supported transitions must be explicit release-manifest upgrade edges and must preserve a tested path from the latest supported prerelease through RC to stable `1.0.0`.

## Entry conditions

Phase 5 begins only after:

- installed project paths are unambiguous
- OpenCode passes its maintained host-conformance fixture
- document update metadata is complete
- the Ava Maintenance role is implemented
- the complete validation, conformance, recovery, uninstall, and upgrade matrix passes

All entry conditions are complete.

## Current active task

[Publish `1.0.0-alpha.1`](02-publish-first-alpha-release.md).

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
