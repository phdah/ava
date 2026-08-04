---
type: Internal Release Procedure
title: Ava Release Automation
description: Defines release-please configuration, Conventional Commit classification, release-channel transitions, and the draft-release qualification handoff.
tags: [internal, releases, automation, release-please, conventional-commits]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
---

# Ava Release Automation

Ava uses `release-please` as a single-package release coordinator. It proposes versions, maintains `CHANGELOG.md` and `version.txt`, keeps one release pull request current, creates immutable `v<version>` tags, and prepares draft GitHub Releases.

Release automation does not authorize publication. The [release publication procedure](procedure.md), [alpha qualification policy](alpha-qualification.md), deterministic assembler, conformance suite, and explicit approval for the exact version and full source revision remain authoritative.

## Merge-boundary contract

Every pull request title must use:

```text
<type>(<optional-scope>)!: <subject>
```

Supported types:

- releasable: `feat`, `fix`, `perf`, `revert`
- internal-only unless marked breaking: `build`, `chore`, `ci`, `docs`, `refactor`, `style`, `test`

Append `!` before `:` for a breaking change, for example `feat!: replace the public manifest contract`. Internal-only work should use a non-releasable type such as `chore(internal): ...` so it does not create an unintended release.

The `conventional-pr-title` workflow enforces this syntax. Repository settings must require that check, require pull requests, use squash merging, and preserve the pull-request title as the squash commit title. The validated title is then the single canonical commit consumed by release-please.

## Bootstrap

The first managed release is `1.0.0-alpha.1`.

- `bootstrap-sha` is the full `main` revision immediately before this integration.
- `.release-please-manifest.json` starts empty.
- `version.txt` contains the non-release sentinel `0.0.0` until the first release pull request updates it.
- `initial-version` forces the first proposal to `1.0.0-alpha.1` without treating older repository history as unreleased product changes.

After the first release pull request is merged, `bootstrap-sha` is ignored and may be removed in a later maintenance change. The manifest becomes the authoritative release-please version record.

## Release channels

The checked-in configuration is initially set to:

```json
{"prerelease": true, "versioning": "prerelease", "prerelease-type": "alpha"}
```

A dedicated reviewed change advances the channel:

- later alpha: retain `alpha` prerelease settings
- release candidate: set `prerelease-type` to `rc`
- stable `1.0.0`: set `prerelease` to `false`, set `versioning` to `default`, and remove `prerelease-type`

The machine-readable fixture records representative alpha, RC, and stable identities. A channel transition that does not match the active Phase 5 task is invalid.

## Credentials and repository settings

Create an Actions secret named `RELEASE_PLEASE_TOKEN` using a fine-grained token or GitHub App token that can write repository contents, pull requests, and issues. A separate token is required so release-please-created pull requests and release operations can trigger the maintained validation path.

Also enable Actions to create pull requests and protect `main` with the title and test checks. Do not permit direct pushes that bypass the validated merge title.

## Draft release handoff

When a release pull request is merged, the release workflow:

1. creates the immutable tag and draft GitHub Release
2. checks out the exact SHA reported by release-please
3. verifies tag, version file, action outputs, and checked-out revision agree
4. runs the maintained release qualification suite
5. assembles the seven release assets twice and compares every digest
6. validates the assembled release with the conformance suite
7. verifies the GitHub Release is still a draft
8. attests the verified assets
9. uploads assets without clobbering an existing filename

Any mismatch fails before asset upload. Existing tags or assets are never moved, replaced, or reused.

Publishing the draft remains a separate explicit transaction under `procedure.md`.
