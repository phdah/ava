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
3. [ ] [Stabilize the published release candidate](05a-stabilize-release-candidate.md)

## Canonical remaining path to `1.0.0`

The core-gate numbering and supporting-task numbering above describe roadmap structure. They are not by themselves the operator order. The official remaining sequence is:

1. finish the synthetic v1 qualification vault
2. qualify and publish the corrective alpha
3. obtain explicit user closure of alpha dogfooding
4. publish the `1.0.0` release candidate
5. stabilize the published release candidate
6. qualify and publish `1.0.0`

A newly discovered `blocker` or `required-v1` finding preempts this sequence until resolved. An approved `post-v1` finding does not.

Dogfooding intentionally remains open during steps 1 and 2. The user does not need to close dogfooding before completing the synthetic-vault work or corrective-alpha qualification. Explicit user closure is required before step 4 may begin, and an empty findings backlog does not substitute for that closure.

## Dogfood findings

Use the [Alpha Dogfood Findings](dogfood/) index.

- 1 pending finding
- 0 pending blockers
- 1 pending required-v1 finding
- 16 completed findings

Findings 01 through 16 are implementation-complete. [Finding 17](dogfood/17-add-resume-abort-qualification-checkpoints.md) is pending and requires deterministic qualification-only checkpoints for authentic resume and abort execution. Finding 12's realistic multi-turn installed-project exercise, finding 15's fresh-agent terminal-finalization exercise, and finding 16's published Inbox Ingester scoped-history exercise remain release qualification evidence required during the corrective-alpha path rather than pending implementation work.

## Qualification policy

Every new release inherits the previous canonical catalog unchanged and authors exactly one adjacent edge. Older sources qualify through unique composition. Published legacy direct representations remain readable but cannot be selected for new authoring.

The dogfood umbrella remains pending until the user explicitly declares it complete. A passing suite, an empty findings backlog, or publication of another alpha does not complete it automatically.

## Current active work

**Step 1 of 6 is preempted by Finding 17.**

The user has confirmed that corpus generation, all five image generations, image finalization, and finalized-corpus verification are complete and recorded locally.

Use:

```text
qualification vault: ~/stuff/ava-qualification-vault/
test project:        ~/stuff/project-vault
```

The user has materialized the variants and exercised ingestion, routing, managed-content damage, semantic reconciliation, finalization, rollback, uninstall, and reinstall behavior. Resolve [Finding 17](dogfood/17-add-resume-abort-qualification-checkpoints.md), execute the authentic resume and abort scenarios, and then return to the remaining Step 1 evidence and signoff gate.

Do not regenerate, re-finalize, or re-verify the corpus or images unless later qualification exposes a fixture defect or invalid local evidence. After the Step 1 qualification gate passes, continue directly to corrective-alpha qualification unless a new blocker or `required-v1` finding has preempted the path.

## Previous phase

[Versioned distribution and upgrades](../04-distribution-and-upgrades/).
