---
type: Internal Release Procedure
title: Ava Release Publication Procedure
description: Defines maintainer preparation, release-PR approval, automatic publication, verification, and failure handling for immutable Ava releases.
tags: [internal, releases, publication, verification, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-05T09:13:00+02:00
---

# Ava Release Publication Procedure

This procedure coordinates maintainers around the public contracts under `/distribution/`. It does not replace deterministic release automation and must never be included in an Ava release payload.

The [release automation contract](release-please.md) prepares versions and changelog entries, runs pull-request qualification, creates immutable tags and draft releases, qualifies the exact tagged source, uploads verified assets, and publishes after every maintained gate succeeds. The first alpha and later prerelease gates are additionally constrained by the [Ava Alpha Qualification Policy](alpha-qualification.md).

# Preconditions

Before preparing a release:

1. The intended version, channel, SemVer rationale, compatibility impact, and upgrade paths are approved.
2. The source revision is clean, reviewed, and suitable for an immutable tag.
3. Public contracts and schemas under `/distribution/` are internally consistent.
4. Release sources under `/templates/` contain no internal repository content.
5. The repository-boundary validator and maintained pull-request qualification check pass.
6. Required release automation, credentials, repository permissions, and immutable-release settings are available.
7. For a prerelease, every required qualification gate for that stage passes and every repository-work finding has the required roadmap task and classification.

When deterministic assembly or verification automation is unavailable, publication is blocked rather than reproduced manually with weaker guarantees.

# Release-please preparation

1. Merge only pull requests whose title passes the Conventional Commit title check and whose release qualification check passes.
2. Use squash merging with the pull-request title preserved as the canonical commit title.
3. Review the single release-please pull request and confirm its version, changelog, version file, manifest, and channel match the active release task.
4. Merging that release pull request explicitly authorizes publication of the resulting tagged revision after the maintained workflow gates succeed.
5. Require the same workflow run to bind the release-please tag and full source revision, rerun qualification, assemble twice, validate release conformance, attest the assets, confirm draft state, upload without replacement, and publish.
6. Treat any failure before publication as a blocked draft. Never move the tag, overwrite an asset, or continue with a different source revision under the same version.

# Preparation

1. Run `internal/release/validate-boundaries.sh`.
2. Run the complete maintained release test suite.
3. Execute deterministic release assembly from one clean source revision.
4. Build every required asset twice and require identical digests.
5. Validate schemas, archive safety, source-to-installed mapping, identity metadata, checksums, release notes, guidance, migrations, and upgrade declarations.
6. For `1.0.0-alpha.1`, require an empty `upgrade_paths.edges` declaration and refuse historical unversioned sources.
7. Confirm the canonical tag is new and still points to the qualified source revision.
8. Confirm the GitHub Release remains a draft until the complete asset set has been validated, attested, and uploaded.

# Approval boundary

A maintainer approves publication by reviewing and merging the release-please pull request. That merge authorizes only the exact version proposed by the pull request and the resulting immutable tagged revision produced by the merge.

The workflow must publish only after it has bound that tag to the source revision and all qualification, reproducibility, conformance, attestation, and asset-upload steps succeed. A failure leaves the draft unpublished. A source revision or version change requires a new release pull request and complete requalification.

Approval of ordinary implementation work, release tooling, policy, or an unmerged release proposal does not authorize publication. The release pull request remains the explicit publication boundary.

# Automated publication

1. Confirm the tag points to the exact revision reported by release-please.
2. Confirm the release is still a draft before attaching assets.
3. Confirm every maintained qualification and release-conformance check succeeds.
4. Confirm the assembled outputs are reproducible and the attestation step succeeds.
5. Upload the complete asset set without replacement.
6. Publish the existing draft without moving the tag or recreating the release.
7. Preserve prerelease and latest status established by the active channel configuration.

# Post-publication verification

After publication, verify:

- the release is immutable and no longer a draft
- prerelease and latest status match the channel
- the tag and release target match the verified source revision
- the release attestation verifies
- every retained local asset verifies against the release
- `SHA256SUMS`, `ava-release.json`, embedded identities, and archive inventories agree
- version-pinned download URLs resolve to the published assets

Record the release URL, source revision, verification result, supported upgrade sources, and any incident in the release workflow summary and repository history required by the public contracts.

# Failure handling

Before publication, correct the defect and use a new version when an immutable tag already exists. Do not move or recreate the tag, overwrite an uploaded asset, or reuse the version.

After publication, never edit assets, move or recreate the tag, or reuse the version. A failed post-publication verification is a release incident. Corrective work uses a new version or an explicit security withdrawal under the public release contract.

Every prerelease finding that requires repository work becomes a bounded Phase 5 task before the next release gate it blocks.

# Completion report

A completed publication report states:

- version, channel, tag, and source revision
- release URL and immutable status
- exact asset inventory
- integrity and attestation verification result
- supported source versions and semantic-review requirement
- qualification result and finding classification summary
- unresolved incidents or follow-up work
