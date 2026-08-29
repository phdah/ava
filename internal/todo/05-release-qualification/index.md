# Phase 05: V1 Release Qualification

Turn Ava's format, roles, release tooling, OpenCode support, and conformance suite into tested prereleases and the first stable distribution.

Use the [V1 Release Operator Path](v1-release-operator-path.md) as the canonical ordering, operator procedure, signoff, and advancement contract from the current alpha state through `1.0.0`.

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
4. [ ] [Stabilize the published release candidate](05a-stabilize-release-candidate.md)

## Canonical remaining path to `1.0.0`

The official remaining sequence is:

1. finish the synthetic v1 qualification vault through a fresh full run against the updated corrective-alpha candidate
2. qualify and publish the corrective alpha
3. obtain explicit user closure of alpha dogfooding
4. publish the `1.0.0` release candidate
5. stabilize the published release candidate
6. qualify and publish `1.0.0`

A newly discovered blocker preempts the next prerelease. A `required-v1` finding preempts the release gate named by its `blocks` field. An approved `post-v1` finding does not preempt this sequence.

Dogfooding intentionally remains open during steps 1 and 2. Explicit user closure is required before step 4 may begin, and an empty findings backlog does not substitute for that closure.

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index.

- 1 pending finding
- 0 pending blockers
- 0 pending required-v1 findings
- 1 pending post-v1 finding
- 31 completed findings

Findings 01 through 30 except post-v1 Finding 25 are implementation-complete, with Finding 30 complete as a no-op. Finding 33 and replacement Finding 34 are also complete. The original Findings 34, 35, and 36 were removed by explicit user decision, and Findings 31 and 32 were removed after reassessment because their resume and run-status work primarily mitigated the former multi-hour ingestion workload. Finding 33 reduced `complete-pending-inbox` from 305 live sources to seven representative sources. Replacement Finding 34 restored Inbox Ingester freedom to use available tools, scripts, code execution, document readers, and temporary helpers while keeping the semantic and authority requirements governing its result.

Finding 17 provides deterministic qualification-only setup states for authentic assembled-installer resume and abort execution. Finding 18 provides conditional deterministic calendar verification for relative-to-absolute persistence. Finding 19 composes the complete maintained matrix behind one internal manual shell entry point. Findings 22 and 23 repair semantic-path reporting scenarios. Finding 24 removes the OpenCode pipe truncation dependency. Finding 26 removes the hardcoded semantic-path-accounting gate. Findings 27 through 29 record the execution-scope and semantic issues from qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local`; Finding 34 supersedes only Finding 27's mechanism restriction, while Findings 28 and 29 remain the desired semantic safeguards.

## Qualification policy

Every new release inherits the previous canonical catalog unchanged and authors exactly one adjacent edge. Older sources qualify through unique composition. Published legacy direct representations remain readable but cannot be selected for new authoring.

The dogfood umbrella remains pending until the user explicitly declares it complete. A passing suite, an empty findings backlog, or publication of another alpha does not complete it automatically.

## Current active work

**Step 1 of 6 now advances to assembling a new corrective-alpha candidate and rerunning the complete qualification matrix.**

There are currently no pending next-prerelease blockers and no pending `required-v1` dogfood findings. If the next real qualification run demonstrates a concrete reliability or semantic problem, record a new finding from that observed behavior rather than restoring removed work preemptively.

The user has confirmed the generated corpus and all five image results. The exact visually accepted PNG bytes are pinned under the repository-only fixture, while generated vaults and execution evidence remain external.

Qualification run `20260820T120651086179Z-alpha14-to-alpha15-corrective-local` passed 15 of 17 scenarios; Findings 22, 23, and 24 resolved that run's failures. Qualification run `20260821T100350003229Z-alpha14-to-alpha15-corrective-local` then failed 2 of 17 scenarios on a hardcoded, edge-agnostic semantic-path-accounting gate that did not generalize across release edges; Finding 26 removed that gate as a qualification-tooling defect rather than a real regression.

Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local` (candidate `77977f8`) then passed all 17 runner scenarios and all 286 repository tests, but the independent audit found two major issues and one minor issue in inbox ingestion, ending the run `needs-review`. Findings 27 through 29 are implementation-complete. Finding 34 subsequently removed Finding 27's mechanism-level restriction while preserving the disposition-fidelity and semantic-evidence protections from Findings 28 and 29. Every qualification run that did not reach accepted evidence remains unaccepted and must not be reused as qualification evidence for a later candidate.

After this implementation reaches `main` and release-please updates the corrective-alpha release PR, assemble a new exact candidate for immutable published `v1.0.0-alpha.14` to caller-supplied local `v1.0.0-alpha.15`, then execute:

```sh
internal/release/qualify-release.sh \
  --target-assets /absolute/path/to/v1.0.0-alpha.15/assets
```

The operation owns exact input acquisition, pinned-image verification, clean fixture generation, isolated test boundaries, the complete maintained matrix, top-level and nested OpenCode session inventory, a fresh-session independent audit, and compact uncommitted release evidence. The maintained OpenCode adapter handles oversized session-list and export JSON internally, so this run must not use the former external large-JSON shim. The complete pending-inbox scenario reports audit-gated structural success rather than claiming semantic success before evaluator-only review, and it no longer constrains which host-agent execution mechanisms may be used during ingestion.

Do not manually reconstruct the earlier runner sequence. Step 1 may advance only from a mechanically clean result whose audit state is `awaiting-user-signoff` and whose generated compact evidence is explicitly accepted. A `failed` or `needs-review` run preempts the path until corrected.

After the Step 1 qualification gate passes, continue directly to corrective-alpha qualification. Finding 25 is post-v1 and does not block this sequence.

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
