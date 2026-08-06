---
type: Internal Release Procedure
title: Ava Release Automation
description: Defines release-please configuration, Conventional Commit classification, pull-request qualification, release-channel transitions, and qualified automatic publication.
tags: [internal, releases, automation, release-please, conventional-commits]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T11:30:00+02:00
---

# Ava Release Automation

Ava uses `release-please` as a single-package release coordinator. It proposes versions, maintains `CHANGELOG.md` and `version.txt`, keeps one release pull request current, creates immutable `v<version>` tags, prepares draft GitHub Releases, qualifies their exact source revision, uploads verified assets, and publishes only after every maintained gate succeeds.

Reviewing and merging the release pull request is the explicit publication approval. The draft GitHub Release remains a temporary staging boundary so qualification, reproducible assembly, conformance, attestation, and asset upload complete before the release becomes public.

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
- `initial-version` remains aligned with the first managed release identity.
- `release-as` is a one-shot bootstrap override that forces the exact `1.0.0-alpha.1` proposal even though the bounded post-bootstrap history intentionally contains no releasable unit.

After the first release pull request is merged, `bootstrap-sha` is ignored and may be removed in a later maintenance change. Remove the one-shot `release-as` override before later release planning. The manifest then becomes the authoritative release-please version record.

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

Create an Actions secret named `RELEASE_PLEASE_TOKEN` using a fine-grained token or GitHub App token that can write repository contents, pull requests, issues, and releases. A separate token is required so release-please-created pull requests and release operations can trigger the maintained validation path.

Also enable Actions to create pull requests and protect `main` with the Conventional Commit title, repository qualification, and `Release PR policy / Validate release PR` checks. Do not permit direct pushes that bypass the validated merge title or qualification suite.

## Pull request qualification

The `release-qualification` workflow runs `internal/release/test.sh` for every pull request without requiring write permissions or repository secrets. This gives reviewers the same repository qualification entry point used again for the exact tagged release source.

The separate `Release PR policy` workflow resolves successfully without checking release state for ordinary pull requests. Only the exact `release-please--branches--main` branch checks out the proposed release and runs both release-only validators.

`validate_release_pr.py` requires the current `main` version and exact agreement between `upgrade-sources.txt`, `alpha-qualification.json`, and `conformance-matrix.json`. `validate_upgrade_impact.py` additionally requires every protected installed prerelease to remain directly supported and verifies each source-specific managed delta, migration decision, guidance decision, semantic-review decision, and cumulative changelog coverage against `upgrade-impact.json`.

Pull-request success does not replace release-time qualification. The release workflow reruns the suite and both release-only validators after the tag and draft release exist so the qualified source revision is exactly the revision that will be published.

## Qualified release handoff

When a release pull request is merged, the merge authorizes publication of the resulting tagged revision and the release workflow:

1. creates the immutable tag and draft GitHub Release
2. checks out the exact SHA reported by release-please
3. verifies tag, version file, action outputs, and checked-out revision agree
4. runs the maintained release qualification suite and exact-source impact validation
5. assembles the seven release assets twice from the reviewed per-source impact and compares every digest
6. validates the assembled release with the conformance suite
7. verifies the GitHub Release is still a draft
8. attests the verified assets
9. uploads assets without clobbering an existing filename
10. publishes the qualified release

The reviewed assembler requires every generated manifest edge to match its declared migration IDs and guidance paths exactly. Empty lists remain valid only when the source assessment records why ordinary managed reconciliation is sufficient and why project-owned semantic work is unnecessary.

Any mismatch or failed step leaves the release as a blocked draft. Existing tags or assets are never moved, replaced, or reused.
