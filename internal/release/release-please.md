---
type: Internal Release Procedure
title: Ava Release Automation
description: Defines release-please version proposals, pull-request qualification, channel transitions, agent completion of release state, and qualified automatic publication.
tags: [internal, releases, automation, release-please, conventional-commits]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T13:45:00+02:00
---

# Ava Release Automation

Ava uses release-please as a single-package release coordinator. It proposes versions, maintains `CHANGELOG.md` and `version.txt`, keeps one release pull request current, creates immutable `v<version>` tags, prepares draft GitHub Releases, qualifies their exact source revision, uploads verified assets, and publishes only after every maintained gate succeeds.

Reviewing and merging the release pull request is the explicit publication approval. The release pull request is intentionally incomplete when release-please first creates it. Its policy check remains red until an agent has completed the release-specific upgrade review directly on the release-please branch.

## Merge-boundary contract

Every ordinary pull request title must use:

```text
<type>(<optional-scope>)!: <subject>
```

Releasable types are `feat`, `fix`, `perf`, and `revert`. Other supported types are internal-only unless marked breaking. The validated pull-request title becomes the canonical squash commit consumed by release-please.

A merged releasable commit causes release-please to create or update `release-please--branches--main`. Ordinary implementation pull requests must not predeclare the next release version or its upgrade edges.

## Release pull-request contract

The release-please pull request proposes the target version and changelog. It does not initially contain a valid `internal/release/upgrade-impact.json` for that target.

The `Release PR policy` workflow applies only to the release-please branch. It validates:

- the target in `version.txt` and `.release-please-manifest.json`
- monotonic SemVer advancement from the pull-request base
- the release-please configuration for the target channel
- the presence and target of `upgrade-impact.json`
- the inherited and protected direct source set
- explicit source retirements
- actual managed payload deltas from immutable source tags
- migration, guidance, and semantic-review assessments
- exact cumulative changelog coverage

The failed check is the activation boundary for release work. When an agent is asked to merge the release pull request, it must inspect the included changes, create the required release impact on the same branch, validate it, push it, wait for green checks, and then merge the pull request.

## One source of release edges

Current releases do not maintain a separate `upgrade-sources.txt`. The source assessments in `internal/release/upgrade-impact.json` are authoritative, and the reviewed assembler derives `upgrade_paths.edges` directly from them.

Qualification inherits direct support from the previous immutable release. For historical tags that predate reviewed impact files, it reads the legacy `upgrade-sources.txt` stored in that tag. This compatibility read does not recreate a current duplicate declaration.

## Release channels

The checked-in release-please configuration controls which type of version release-please proposes.

For prereleases:

```json
{
  "prerelease": true,
  "versioning": "prerelease",
  "prerelease-type": "alpha"
}
```

The prerelease type may be `alpha`, `beta`, or `rc` and must match the target version.

For stable releases:

```json
{
  "prerelease": false,
  "versioning": "default"
}
```

The stable configuration must not contain `prerelease-type`.

Continuing within the current channel requires no configuration change. The first release in another channel requires a dedicated reviewed configuration change before release-please creates that release pull request. The generic release-impact and publication machinery is identical across alpha, beta, release candidate, stable, patch, minor, and major releases.

## Bootstrap

The first managed release is configured by `initial_release_version` in `internal/release/fixtures/release-upgrade-policy.json`. Its impact file has no sources or retirements. Later releases always include the immediately previous release as a required direct source.

## Qualified release handoff

When the completed release pull request is merged, the workflow:

1. creates the immutable tag and draft GitHub Release
2. checks out the exact SHA reported by release-please with complete history and tags
3. verifies tag, version, channel, and source revision identity
4. reruns release PR and reviewed upgrade-impact validation
5. runs the maintained release qualification suite
6. assembles the seven release assets twice from `upgrade-impact.json`
7. compares every digest and validates release conformance
8. confirms the GitHub Release is still a draft
9. attests and uploads the verified assets without replacement
10. publishes the qualified release

Any mismatch or failed step leaves the draft unpublished. Existing tags and assets are never moved, replaced, or reused.
