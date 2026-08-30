---
id: ava-5601
title: "Restore supported prerelease upgrade paths"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "dogfood", "blocker"]
ordinal: 5601
---

## Description

Make release orchestration declare and validate supported source prereleases so published upgrades do not fail with an empty upgrade-edge manifest. This native Backlog.md task preserves the complete finding, implementation, and qualification evidence.

## Migrated task record

---
type: Internal Development Task
title: Restore Supported Prerelease Upgrade Paths
description: Make release orchestration declare and validate supported source prereleases so published upgrades do not fail with an empty upgrade-edge manifest.
tags: [internal, roadmap, dogfood, releases, upgrades, blocker]
status: completed
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: 1
classification: blocker
blocks: next-prerelease
affected_version: 1.0.0-alpha.4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-05T09:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-05T14:13:28+02:00
---

# Restore Supported Prerelease Upgrade Paths

## Observed behavior

A project installed with `1.0.0-alpha.3` cannot upgrade to the published `1.0.0-alpha.4` release.

## Reproduction and evidence

From an alpha.3 project, the version-pinned alpha.4 installer reported:

```text
ERROR [UNSUPPORTED_TRANSITION]: release v1.0.0-alpha.4 does not support upgrade from 1.0.0-alpha.3
```

The alpha.4 release workflow invoked the assembler without any `--upgrade-from` arguments. The generated `ava-release.json` therefore contained an empty `upgrade_paths.edges` list.

## Classification

This was a `blocker`. Published prerelease upgrades are an explicit v1 contract and continued dogfooding had to move realistic projects between supported immutable releases. The next prerelease and later release gates were blocked until a supported path was restored and tested.

## Root cause

Release Please selects the version and creates the tag, but does not know Ava's compatibility policy. Ava's assembler creates upgrade edges only from explicit `--upgrade-from` arguments. Release orchestration supplied none, and existing tests proved only that the assembler could create edges when called correctly rather than that real release orchestration supplied intended sources.

## Scope

- establish one explicit source of truth for supported upgrade sources of each planned release
- make release orchestration pass every declared source to the assembler as `--upgrade-from`
- fail qualification before publication when a later prerelease has no intended upgrade edge
- keep the first managed alpha as the only release allowed to have no supported source by default
- add regression coverage for the real workflow-to-assembler handoff
- use a new immutable prerelease rather than modifying alpha.4

The corrective prerelease was required to support direct upgrades from both `1.0.0-alpha.3` and `1.0.0-alpha.4` unless a reviewed compatibility decision declared a different path.

## Completion criteria

- release workflow obtains supported source versions from reviewed repository state rather than implicit guessing
- assembler receives one `--upgrade-from` argument per declared direct source
- PR qualification fails when a later planned prerelease lacks required edges
- release qualification verifies the exact intended manifest edges
- a new prerelease has supported paths from alpha.3 and alpha.4
- real alpha.3 and alpha.4 installations upgrade successfully
- managed files reconcile correctly and project-owned files remain preserved
- implementing PR, published version, and dogfood evidence are recorded

## Resolution evidence

Criteria 1 and 2 were addressed in PR #50 (`fix/release-workflow-upgrade-from-wiring`): `internal/release/upgrade-sources.txt` became reviewed source state, `.github/workflows/release-please.yml` read it and passed one `--upgrade-from` per version, release procedure and parent dogfood state required updates before each prerelease, and release-please tests plus conformance transition fixtures were expanded. Criteria 3 and 4 were addressed in merged PR #49.

Criterion 5 was addressed by release PR #51, which published immutable prerelease `v1.0.0-alpha.5` from revision `7f6abf3acf190cdb668f7f3b3ea0d6b8cd3ae179` with direct edges from alpha.3 and alpha.4.

On 2026-08-05 a real alpha.3 installation upgraded successfully to alpha.5, retained managed payload, advanced semantic compatibility, and preserved project-owned `opencode.json`. A real alpha.4 installation in a non-empty project also upgraded successfully and preserved project-owned configuration. The all-`RETAIN` payload result was expected because alpha.5 corrected orchestration/edge metadata without changing the distributed managed base from alpha.4.

Project-owned preservation was verified against bracketing project commits: the tracked project-owned scaffold and OpenCode configuration had no changes while the upgrade changed only `/.ava/state/manifest.json` and `/.ava/state/upgrade.json`. Implementing PRs #49/#50, release PR #51, both real upgrades, and parent dogfood evidence satisfied the final criterion.