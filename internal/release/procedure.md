---
type: Internal Release Procedure
title: Ava Release Publication Procedure
description: Defines maintainer preparation, approval, publication supervision, verification, and failure handling for immutable Ava releases.
tags: [internal, releases, publication, verification, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
---

# Ava Release Publication Procedure

This procedure coordinates maintainers around the public contracts under `/distribution/`. It does not replace deterministic release automation and must never be included in an Ava release payload.

# Preconditions

Before preparing a release:

1. The intended version, channel, SemVer rationale, compatibility impact, and upgrade paths are approved.
2. The source revision is clean, reviewed, and suitable for an immutable tag.
3. Public contracts and schemas under `/distribution/` are internally consistent.
4. Release sources under `/templates/` contain no internal repository content.
5. The repository-boundary validator passes.
6. Required release automation, credentials, repository permissions, and immutable-release settings are available.

When deterministic assembly or verification automation is unavailable, publication is blocked rather than reproduced manually with weaker guarantees.

# Preparation

1. Run `internal/release/validate-boundaries.sh`.
2. Execute deterministic release assembly from one clean source revision.
3. Build every required asset twice and require identical digests.
4. Validate schemas, archive safety, source-to-installed mapping, identity metadata, checksums, release notes, guidance, migrations, and upgrade declarations.
5. Prepare the canonical tag without moving or reusing an existing release tag.
6. Create the GitHub Release as a draft and upload the exact required asset set without clobber behavior.
7. Re-fetch the draft and compare filenames, sizes, digests, embedded identities, and target revision with local verified outputs.

# Approval boundary

A maintainer may prepare and validate a draft release under an approved implementation scope. Publishing a stable or prerelease release requires explicit approval for the exact version and source revision unless the user has already authorized that publication transaction.

Approval to prepare a draft does not authorize changing public contracts, compatibility declarations, tag targets, release notes, or asset contents outside the reviewed change.

# Publication supervision

1. Confirm the tag still points to the verified source revision.
2. Confirm repository release immutability is enabled.
3. Confirm the draft contains exactly the validated assets.
4. Publish once, without replacement or post-publication editing.
5. For a stable release, set or retain `latest` only when the release contract declares that outcome.

# Post-publication verification

After publication, verify:

- the release is immutable and no longer a draft
- prerelease and latest status match the channel
- the tag and release target match the verified source revision
- the release attestation verifies
- every retained local asset verifies against the release
- `SHA256SUMS`, `ava-release.json`, embedded identities, and archive inventories agree
- version-pinned download URLs resolve to the published assets

Record the release URL, source revision, verification result, and any incident in the release workflow summary and repository history required by the public contracts.

# Failure handling

Before publication, correct or discard the draft and rerun the complete deterministic validation.

After publication, never edit assets, move or recreate the tag, or reuse the version. A failed post-publication verification is a release incident. Corrective work uses a new version or an explicit security withdrawal under the public release contract.

# Completion report

A completed publication report states:

- version, channel, tag, and source revision
- release URL and immutable status
- exact asset inventory
- integrity and attestation verification result
- supported source versions and semantic-review requirement
- unresolved incidents or follow-up work
