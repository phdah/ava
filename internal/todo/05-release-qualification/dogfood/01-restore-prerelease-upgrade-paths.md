---
type: Internal Development Task
title: Restore Supported Prerelease Upgrade Paths
description: Make release orchestration declare and validate supported source prereleases so published upgrades do not fail with an empty upgrade-edge manifest.
tags: [internal, roadmap, dogfood, releases, upgrades, blocker]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 1
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-05T09:00:00+02:00
---

# Restore Supported Prerelease Upgrade Paths

## Observed behavior

A project installed with `1.0.0-alpha.3` cannot upgrade to the published `1.0.0-alpha.4` release.

## Reproduction and evidence

From an alpha.3 project:

```sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.0.0-alpha.4/ava-install.sh | sh
```

The installer reports:

```text
ERROR [UNSUPPORTED_TRANSITION]: release v1.0.0-alpha.4 does not support upgrade from 1.0.0-alpha.3
```

The alpha.4 release workflow invoked the assembler without any `--upgrade-from` arguments. The generated `ava-release.json` therefore contained an empty `upgrade_paths.edges` list.

## Classification

This is a `blocker`. Published prerelease upgrades are an explicit v1 contract and continued dogfooding must be able to move realistic projects between supported immutable releases. The next prerelease and every later release gate are blocked until a supported path is restored and tested.

## Root cause

Release Please selects the version and creates the tag, but it does not know Ava's compatibility policy. Ava's assembler creates upgrade edges only from explicit `--upgrade-from` arguments. The release workflow currently supplies none, and existing tests prove only that the assembler can create edges when called correctly. They do not prove that real release orchestration supplies the intended sources.

## Scope

- establish one explicit source of truth for the supported upgrade sources of each planned release
- make release orchestration pass every declared source to the assembler as `--upgrade-from`
- fail qualification before publication when a later prerelease has no intended upgrade edge
- keep the first managed alpha as the only release allowed to have no supported source by default
- add regression coverage for the real workflow-to-assembler handoff
- publish a new immutable prerelease rather than modifying alpha.4

The corrective prerelease must support direct upgrades from both `1.0.0-alpha.3` and `1.0.0-alpha.4`, unless a reviewed compatibility decision explicitly declares a different supported path.

## Completion criteria

- the release workflow obtains supported source versions from reviewed repository state rather than implicit version guessing
- the assembler receives one `--upgrade-from` argument for every declared direct source
- PR qualification fails when a later planned prerelease would be assembled without its required edges
- release qualification verifies the generated manifest contains the exact intended upgrade edges before publication
- a new prerelease is published with supported paths from alpha.3 and alpha.4
- a real alpha.3 installation upgrades successfully to that prerelease
- a real alpha.4 installation upgrades successfully to that prerelease
- managed files reconcile correctly and project-owned files remain preserved
- the finding index records the implementing PR, published version, and dogfood evidence before this task is completed

## Resolution evidence

Partial. The following completion criteria are addressed:

- **Criteria 3 - PR qualification fails for missing edges:** `conformance_release.py` now emits `AVA-RELEASE-UPGRADE-EDGES` (error) when any release other than `1.0.0-alpha.1` has an empty `upgrade_paths.edges` list. Two new tests in `test_alpha_qualification.py` cover both the failing and the allowed case. The new case `release-manifest-upgrade-edges-missing` is registered in the conformance matrix and wired into the `contracts-consistent` gate.

- **Criteria 4 - release qualification verifies edges before publication:** The same `conformance_release.py` check runs during `conformance.py --mode release`, which the release workflow invokes after double assembly. A release assembled without `--upgrade-from` will now fail qualification before publication.

Supporting procedure changes were also made: `procedure.md` has a new Release PR review section and an explicit preparation step for fixture and edge declaration; `04-dogfood-alpha-and-track-findings.md` requires fixture updates before each additional prerelease; `instructions.md` documents the direct-push-to-release-branch pattern and the release PR review obligation.

The following criteria remain open:

- Criteria 1: the release workflow does not yet obtain upgrade sources from reviewed repository state; `--upgrade-from` is still not passed in `.github/workflows/release-please.yml`.
- Criteria 2: the assembler therefore still receives no `--upgrade-from` argument for declared sources.
- Criteria 5-9: the corrective prerelease (alpha.5) has not yet been published; dogfood evidence of successful upgrades from alpha.3 and alpha.4 is pending.
