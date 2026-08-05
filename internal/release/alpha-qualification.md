---
type: Internal Release Procedure
title: Ava Alpha Qualification Policy
description: Defines the executable readiness gate, defect classes, prerelease support boundary, transition declarations, and approval required before the first Ava alpha.
tags: [internal, release, qualification, alpha, prerelease, upgrades]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T09:21:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-05T14:49:04+02:00
---

# Purpose

This policy defines when `1.0.0-alpha.1` is ready to publish and how findings discovered during prerelease qualification affect later release gates.

The first alpha is a testable build of the intended v1 product. It is not a supported stable user state and it is not publication authority by itself.

The public release identity, assets, and upgrade-edge model remain defined by:

- [Ava GitHub Release Assets](../../distribution/releases.md)
- [Ava Versioning and Compatibility](../../distribution/versioning.md)
- [Ava Release Manifest Schema](../../distribution/schemas/release.schema.json)

The machine-readable qualification policy is frozen in [alpha-qualification.json](fixtures/alpha-qualification.json). The maintained test suite validates the policy, its evidence references, reproducible assembly, and prerelease upgrade declarations.

# Qualification result

Alpha qualification has exactly two outcomes:

- `ready`: every required gate passes, no blocking finding remains open, and publication approval has been granted for the exact version and source revision.
- `blocked`: at least one required gate fails, a blocking finding remains open, or exact publication approval is absent.

A partial pass is `blocked`. Warnings and known limitations may remain only when they are classified under this policy and do not violate a required gate.

# Required gates

## Roadmap completion

Every Phase 1 through Phase 4 task must be `completed`. The current alpha-policy task must also be complete before publication preparation begins.

A pending approved v1 behavior is not reclassified as post-v1 merely to pass this gate.

## Repository and contract consistency

The maintained release test runner and repository conformance mode must pass from the exact source revision:

```sh
internal/release/test.sh
python3 internal/release/conformance.py --root . --mode repository --format text
```

The result must cover public format, ownership, path, routing, metadata, installed state, release schemas, and internal-to-distributed boundary checks.

## Role authority separation

The conformance evidence must continue to prove:

- deterministic or malformed managed state routes to Ava Maintenance
- project-owned semantic reconciliation routes to Upgrade Role
- neither role gains the authority of the other
- semantic compatibility cannot be marked complete while required project-owned changes remain inconsistent

## Supported host behavior

OpenCode must pass the maintained fixture for:

- default project-owned configuration creation
- preservation of existing configuration
- non-destructive reporting when required permissions are absent

No other named host may be described as maintained without its own accepted fixture and roadmap task.

## Installation lifecycle safety

The maintained suite must pass the required fresh-install, non-empty-project, recovery, migration, uninstall, and verified-bootstrap scenarios.

Unknown historical or unversioned Ava layouts must be refused. They are not supported migration sources for `1.0.0-alpha.1`.

## Reproducible release assembly

The exact source revision must be assembled twice in clean directories with identical inputs. Every generated release asset must have the same SHA-256 digest in both outputs.

Before either assembly writes an asset, every distributed local inline Markdown link must resolve against the complete source-to-installed payload mapping without escaping the selected project. A repository source target that is excluded or installed at another destination does not satisfy this gate.

The first alpha manifest must contain:

```json
{
  "ava_version": "1.0.0-alpha.1",
  "channel": "alpha",
  "upgrade_paths": {
    "edges": []
  }
}
```

An empty edge list is an explicit declaration that no earlier Ava installation is a supported upgrade source.

## Release notes and guidance

Generated release notes and guidance must state:

- that the release is a prerelease selected only by exact version
- that stable support guarantees have not started
- every known limitation relevant to installation, upgrade, host access, managed state, or project-owned context
- whether semantic review is required
- every supported source-to-target upgrade edge, or that none exist
- compatibility impact and any intentionally incompatible prerelease behavior

The release manifest, notes, guidance, migrations, and installer metadata must agree.

## Protected-state defect gate

No open finding may allow or risk:

- managed-state corruption
- overwrite or reclassification of project-owned content
- escape outside the selected target root
- bypass of role or deterministic-tool authority
- an installation or upgrade that cannot be recovered, aborted, rolled back, finalized, or safely diagnosed

Any such finding is always a `blocker`.

# Finding classes

Every qualification or dogfooding finding that requires repository work must be recorded as a bounded task file under the active Phase 5 roadmap.

The finding record must identify:

- summary and observed behavior
- affected version or source revision
- classification
- affected gate or protected impact
- reproduction or evidence
- completion criteria
- the next release gate it blocks

## `blocker`

A blocker prohibits publication of the current candidate and every later release stage until resolved.

Protected-state impacts are always blockers. Missing required release assets, inconsistent identity, non-reproducible assembly, unsupported authority, or an absent required qualification test are also blockers.

## `required-v1`

A required-v1 finding is approved v1 behavior or quality work that must be complete before stable `1.0.0`.

It may remain open during alpha only when:

- it is not a protected-state impact
- the known limitation is stated accurately
- a bounded roadmap task exists
- the task is placed before the release gate it blocks

A required-v1 finding blocks the release candidate when it affects the path that the release candidate is intended to prove. Otherwise it blocks stable qualification at the latest.

## `post-v1`

A post-v1 finding is outside the approved v1 scope and does not weaken a v1 contract, safety property, or stated behavior.

The classification requires an explicit rationale. Missing approved v1 behavior cannot be moved to post-v1 to preserve a date.

# Prerelease upgrade support

## First alpha

`1.0.0-alpha.1` has no supported earlier Ava installation source.

Its release manifest must declare an empty `upgrade_paths.edges` array. Historical unversioned Ava repositories and development snapshots are unsupported and must be refused rather than inferred or adopted as an upgrade source.

## Later prereleases

Every later prerelease declares support only through the target release manifest:

- each supported direct source has one explicit edge
- a required intermediate sequence is declared as a chained edge
- omitted sources are unsupported
- unresolved semantic state may be carried only when the edge explicitly permits it
- guidance and migration inventories must satisfy every declared edge

Prerelease compatibility may intentionally break. When it does, the target release notes, guidance, migrations, and edge declarations must describe the same supported path.

## Required path to stable

Before an RC is published, the latest supported prerelease must have a tested declared path to that RC.

Before stable `1.0.0` is published, the release candidate must have a tested declared path to stable. Additional prereleases may be inserted, but every supported transition remains explicit and independently tested.

## Selection and support boundary

Prereleases are installed only through exact version-pinned URLs. They are never selected through the stable `latest` URL.

Stable maintenance and compatibility guarantees begin with `1.0.0`. Alpha, beta, and RC publication establish only the explicitly declared test and upgrade paths for those exact releases.

# Publication approval

Publishing any prerelease requires explicit user approval for both:

- the exact canonical version
- the exact full source revision

Approval to define this policy, implement tooling, prepare assets, create a tag, or create a draft release does not authorize publication.

A source revision change invalidates earlier approval and requires complete requalification and renewed approval.

# Completion evidence

This policy is executable through:

- [the release test runner](test.sh)
- [the conformance matrix](fixtures/conformance-matrix.json)
- [the alpha qualification fixture](fixtures/alpha-qualification.json)
- [the alpha qualification tests](tests/test_alpha_qualification.py)

After release-please integration is complete, the alpha publication task may prepare and publish `1.0.0-alpha.1` only after these checks pass for the selected source revision and the exact publication transaction is approved.
