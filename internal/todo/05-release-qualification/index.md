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

1. finish the synthetic v1 qualification vault
2. qualify and publish the corrective alpha
3. obtain explicit user closure of alpha dogfooding
4. publish the `1.0.0` release candidate
5. stabilize the published release candidate
6. qualify and publish `1.0.0`

A newly discovered `blocker` or `required-v1` finding preempts this sequence until resolved. An approved `post-v1` finding does not.

Dogfooding intentionally remains open during steps 1 and 2. Explicit user closure is required before step 4 may begin, and an empty findings backlog does not substitute for that closure.

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index.

- 4 pending findings
- 2 pending blockers
- 1 pending required-v1 finding
- 1 pending post-v1 finding
- 21 completed findings

Findings 01 through 19 are implementation-complete. Finding 17 provides deterministic qualification-only setup states for authentic assembled-installer resume and abort execution. Finding 18 provides conditional deterministic calendar verification for relative-to-absolute persistence, with source anchoring, ambiguity handling, boundary fixtures, Change Reviewer fidelity checks, and assembled-payload coverage. Finding 19 composes the complete maintained matrix behind one internal manual shell entry point with pinned-input preflight, isolated runner-owned scenario workspaces, exact managed-damage rules, bounded OpenCode prompts, interrupted reruns, and final summary semantics. Finding 12's realistic multi-turn installed-project exercise, Finding 15's fresh-agent terminal-finalization exercise, Finding 16's published Inbox Ingester scoped-history exercise, Finding 17's selected-asset resume/abort execution, Finding 18's clean-session registered-role calendar exercise, and Finding 19's complete selected-asset runner execution remain release qualification evidence rather than pending implementation work.

## Qualification policy

Every new release inherits the previous canonical catalog unchanged and authors exactly one adjacent edge. Older sources qualify through unique composition. Published legacy direct representations remain readable but cannot be selected for new authoring.

The dogfood umbrella remains pending until the user explicitly declares it complete. A passing suite, an empty findings backlog, or publication of another alpha does not complete it automatically.

## Current active work

**Step 1 of 6 is active. The required qualification-automation implementation is complete, so execute the automated evidence gate next.**

The user has confirmed the generated corpus and all five image results. The exact visually accepted PNG bytes are pinned under the repository-only fixture, while generated vaults and execution evidence remain external.

The reviewed active pair is immutable published `v1.0.0-alpha.14` to exact caller-supplied local `v1.0.0-alpha.15`. Execute:

```sh
internal/release/qualify-release.sh \
  --target-assets /absolute/path/to/v1.0.0-alpha.15/assets
```

The operation owns exact input acquisition, pinned-image verification, clean fixture generation, isolated test boundaries, the complete maintained matrix, top-level and nested OpenCode session inventory, a fresh-session independent audit, and compact uncommitted release evidence.

Do not manually reconstruct the earlier runner sequence. Step 1 may advance only from a mechanically clean result whose audit state is `awaiting-user-signoff` and whose generated compact evidence is explicitly accepted. A `failed` or `needs-review` run preempts the path until corrected.

After the Step 1 qualification gate passes, continue directly to corrective-alpha qualification unless a new blocker or `required-v1` finding has preempted the path.

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
