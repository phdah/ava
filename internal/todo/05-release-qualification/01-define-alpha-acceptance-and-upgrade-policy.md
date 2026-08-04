---
type: Internal Development Task
title: Define Alpha Acceptance and Prerelease Upgrade Policy
description: Define the exact readiness gate, test scope, defect policy, support boundary, and upgrade declarations required before publishing the first Ava alpha.
tags: [internal, roadmap, releases, alpha, acceptance, upgrades]
status: completed
phase: 5
order: 1
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-04T09:21:00+02:00
---

# Define Alpha Acceptance and Prerelease Upgrade Policy

## Purpose

The first alpha must be testable as the intended v1 product rather than published merely because release tooling exists. This task converts the completed implementation and conformance work into an explicit prerelease gate.

## Define alpha readiness

Require at least:

- every Phase 1 through Phase 4 v1 blocker is complete
- public format, ownership, path, routing, metadata, state, and release schemas are internally consistent
- the Ava Maintenance and Upgrade roles have distinct tested authority
- OpenCode passes the supported-host fixture
- fresh installation, non-empty-project installation, recovery, role-led uninstall, and verified bootstrap tests pass
- release assembly is reproducible from one clean source revision
- generated release notes and guidance state known limitations and compatibility impact
- no unresolved defect can corrupt managed state, overwrite project-owned content, escape the target root, bypass authority, or make the installation unrecoverable

## Define defect handling

Create stable prerelease finding classes:

- `blocker`: publication or the next release stage is prohibited
- `required-v1`: must be completed before stable `1.0.0`, but may be discovered or implemented during alpha
- `post-v1`: explicitly outside the approved v1 scope and not required for stable qualification

Do not classify missing approved v1 behavior as `post-v1` merely to preserve a release date.

Every alpha finding that requires repository work must become a bounded task file with completion criteria and be inserted before the next release gate it blocks.

## Define prerelease support

- `1.0.0-alpha.1` has no supported earlier Ava installation source
- no historical unversioned Ava installation is a supported migration source
- subsequent prereleases explicitly declare which earlier prereleases can upgrade directly or through required intermediates
- prerelease-to-prerelease compatibility may be intentionally broken, but release notes, guidance, migrations, and installer metadata must agree
- the latest supported prerelease must have a tested path to the release candidate
- the release candidate must have a tested path to stable `1.0.0`
- prereleases are selected only by exact version and never through the stable `latest` URL
- stable support guarantees begin with `1.0.0`, not with alpha publication

## Define publication approval

Publishing any prerelease requires explicit approval for the exact version and source revision. Approval to define this policy or prepare assets does not authorize publication.

## Implemented result

- [Alpha qualification policy](../../release/alpha-qualification.md) defines the two-state gate, required evidence, defect classes, protected impacts, prerelease support boundary, and approval scope.
- [Alpha qualification fixture](../../release/fixtures/alpha-qualification.json) freezes the machine-readable gate and intended source-to-target transitions.
- [Alpha qualification tests](../../release/tests/test_alpha_qualification.py) validate Phase 1 through Phase 4 completion, evidence references, reproducible assembly, the first-alpha empty upgrade-edge list, explicit later prerelease edges, refusal of unversioned sources, and revision-bound approval.
- [Release publication procedure](../../release/procedure.md) now requires the applicable qualification gate before publication.

## Completion criteria

- alpha readiness is measurable and executable through the maintained validation suite
- defect severity controls roadmap insertion and later release gates
- unsupported historical migration is excluded explicitly
- every intended prerelease transition has a machine-readable declaration model
- stable support and prerelease testing boundaries cannot be confused
- the first alpha cannot be published until every blocker in this task is satisfied
