# Phase 05: V1 Release Qualification

Turn Ava's format, roles, release tooling, OpenCode support, and conformance suite into tested prereleases and the first stable distribution.

Use the [V1 Release Operator Path](v1-release-operator-path.md) as the canonical release-ordering and advancement contract when the user explicitly resumes progression toward `1.0.0`.

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
3. [x] [Automate release qualification and evidence state](04c-automate-release-qualification-evidence.md)
4. [ ] [Harden Qualification OpenCode Permissions](04d-harden-qualification-opencode-permissions.md)
5. [ ] [Isolate Qualification Session Inventory](04e-isolate-qualification-session-inventory.md)
6. [ ] [Stabilize the published release candidate](05a-stabilize-release-candidate.md)

## Current active work

Further alpha dogfooding and immediate V1 progression are parked by explicit user decision. The dogfood umbrella remains pending, but it is not the current work queue.

The next work is ordinary implementation hardening discovered during the `v1.0.0-alpha.15` release process:

1. [Harden Qualification OpenCode Permissions](04d-harden-qualification-opencode-permissions.md)
2. [Isolate Qualification Session Inventory](04e-isolate-qualification-session-inventory.md)

After both tasks complete, roadmap execution moves to [Backlog.md integration](../06-backlog-md/) and then [Durable interaction evidence](../07-interaction-evidence/) before the roadmap is reassessed with the user.

## Qualification-hardening rationale

The alpha.15 release process exposed two root-cause infrastructure defects rather than release-content defects:

- the independent audit could be denied access to qualification evidence under `/tmp` because required OpenCode permission was not fully self-contained in the release process
- the session inventory could include historical OpenCode sessions from earlier qualification runs, contaminating the exact-run evidence set

These are tracked as bounded supporting tasks rather than new dogfood findings. Do not add an exceptional acceptance or failed-state override mechanism as part of this work. The current direction is to make normal qualification reliable enough that such recovery is unnecessary.

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index for historical and still-open dogfood state.

The dogfood umbrella remains pending until the user explicitly declares it complete. It is currently parked rather than closed. Existing completed findings remain durable history and must not be renumbered or reconstructed to represent the new qualification-hardening work.

## Parked path to `1.0.0`

The release path remains conceptually:

1. finish qualification-system evidence required for release progression
2. complete any remaining corrective-alpha evidence obligations
3. obtain explicit user closure of alpha dogfooding
4. publish the `1.0.0` release candidate
5. stabilize the published release candidate
6. qualify and publish `1.0.0`

This sequence is not the current implementation queue. Consult [V1 Release Operator Path](v1-release-operator-path.md) only when the user explicitly resumes release progression.

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
