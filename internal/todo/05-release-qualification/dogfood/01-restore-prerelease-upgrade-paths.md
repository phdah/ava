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

Criteria 1 and 2 addressed in PR #50 (`fix/release-workflow-upgrade-from-wiring`):

- `internal/release/upgrade-sources.txt` introduced as the reviewed source of truth for supported upgrade sources for the next release; currently declares `1.0.0-alpha.3` and `1.0.0-alpha.4` as sources for alpha.5.
- `.github/workflows/release-please.yml` updated to read `upgrade-sources.txt` and pass one `--upgrade-from` argument per declared version to the assembler.
- `procedure.md` step 7 and `04-dogfood-alpha-and-track-findings.md` updated to require `upgrade-sources.txt` updates alongside fixture updates before each prerelease.
- `test_release_please.py` extended with two new tests: `test_release_workflow_reads_upgrade_sources_file` and `test_upgrade_sources_file_contains_valid_versions`.
- Conformance matrix `prerelease_transitions` and `alpha-qualification.json` `transitions` updated to reflect the actual known path through alpha.5 and to alpha.2 -> alpha.3 intermediate.
- `test_prerelease_transitions_are_machine_readable_release_edges` refactored to handle releases with multiple sources (alpha.5 from both alpha.3 and alpha.4) and to compare order-independently.

Criteria 3 and 4 addressed in PR #49 (merged).

Criteria 5 addressed by release PR #51, which published immutable prerelease `v1.0.0-alpha.5` from revision `7f6abf3acf190cdb668f7f3b3ea0d6b8cd3ae179`. The qualified release manifest declares direct upgrade edges from both alpha.3 and alpha.4.

Criterion 6 was verified on 2026-08-05 by upgrading a real alpha.3 installation with the version-pinned alpha.5 installer. The installer completed successfully, reported `Installed Ava 1.0.0-alpha.5`, retained the existing managed files, advanced semantic compatibility through alpha.5, and preserved the existing project-owned `opencode.json` rather than replacing it.

Criterion 7 was verified on 2026-08-05 by upgrading a real alpha.4 installation in a non-empty project with the version-pinned alpha.5 installer. The installer retained every byte-identical managed payload, advanced the installed and semantic-compatible version to alpha.5, and again preserved the existing project-owned `opencode.json`.

The all-`RETAIN` payload result is expected because alpha.5 corrects release orchestration and upgrade-edge metadata without changing the distributed managed base from alpha.4. The upgrade therefore changes managed state and release identity rather than replacing payload files.

Criterion 8 was verified against the real project commits that bracket the alpha.3 installation and alpha.5 upgrade. `git diff --name-status cd37e54..7e767ba -- index.md inbox knowledge roles shared workflows opencode.json` produced no changes, while the complete upgrade commit changed only `/.ava/state/manifest.json` and `/.ava/state/upgrade.json`. The upgrade therefore preserved every tracked project-owned scaffold and OpenCode configuration while advancing only managed state.

Criterion 9 is satisfied by the implementing PRs #49 and #50, published release PR #51, the two real supported-source upgrades recorded above, and the indexed dogfood evidence in the parent task. All completion criteria are met.
