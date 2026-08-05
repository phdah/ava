---
type: Distribution Contract
title: Ava GitHub Release Assets
description: Defines Ava release tags, immutable assets, channels, integrity metadata, bootstrap trust modes, publication, verification, and retention.
tags: [ava, distribution, releases, github, integrity, authenticity, provenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-05T14:49:04+02:00
---

# Ava GitHub Release Assets

This document defines the canonical GitHub Release contract for Ava. It specifies the immutable release identity, required assets, channels, integrity and authenticity model, publication transaction, post-publication verification, and retention guarantees.

The installed ownership boundary is defined by [Ava Distribution and Ownership Boundary](ownership.md). Ava SemVer, installed release identity, and semantic compatibility are defined by [Ava Versioning and Compatibility](versioning.md). The machine-readable release manifest conforms to [release.schema.json](schemas/release.schema.json).

# Release identity

Every published Ava release is identified by one canonical Semantic Version and one matching Git tag.

- Stable tag: `v1.2.3`
- Prerelease tag: `v2.0.0-rc.1`, `v2.0.0-beta.1`, or `v2.0.0-alpha.1`
- `ava_version` is the tag without the leading `v`.
- Published versions use canonical SemVer without build metadata.
- The tag points to the full source commit SHA used to build every release asset.
- The release manifest records the tag, version, channel, repository, and full source revision.
- Every archive and executable asset embeds matching release identity metadata.

A release is invalid when the tag, version, channel, source revision, embedded asset metadata, release manifest, or GitHub release target disagree.

# Canonical download URLs

The stable convenience installer URL is:

```text
https://github.com/phdah/ava/releases/latest/download/ava-install.sh
```

The version-pinned installer URL is:

```text
https://github.com/phdah/ava/releases/download/v1.2.3/ava-install.sh
```

`/releases/latest/` resolves only to the latest published stable release. Prereleases must be selected by an exact tag. Installation from mutable `main`, a branch archive, an Actions artifact, or a moving development alias is not a supported release installation path.

# Required release assets

Every stable or prerelease GitHub Release publishes exactly these named assets:

| Asset | Media type | Purpose |
|---|---|---|
| `ava-install.sh` | `text/x-shellscript` | Thin POSIX shell installer and updater bootstrap. |
| `ava-base.tar.gz` | `application/gzip` | Versioned distribution source used to install Ava-managed base content and create-if-absent project scaffolds through the explicit mapping in the release manifest. |
| `ava-guidance.tar.gz` | `application/gzip` | Agent-readable semantic upgrade guidance for supported source-to-target transitions. |
| `ava-migrations.tar.gz` | `application/gzip` | Deterministic migration scripts and metadata for supported upgrade paths. |
| `ava-release.json` | `application/json` | Canonical machine-readable release identity, asset inventory, installed mapping, compatibility declarations, and checksums. |
| `ava-release-notes.md` | `text/markdown` | Human-readable changes, SemVer rationale, compatibility impact, deprecations, and upgrade summary. |
| `SHA256SUMS` | `text/plain` | SHA-256 digest list for every other uploaded Ava asset. |

The guidance and migration archives are required even when a release has no semantic guidance or deterministic migrations. In that case they contain only their identity metadata and an explicit empty inventory. Fixed presence avoids conditional installer behavior and makes release validation deterministic.

GitHub-generated source archives are not Ava release assets. Their bytes are generated on demand, are not included in `SHA256SUMS`, and must not be used as installer payloads.

# Asset identity metadata

`ava-install.sh` declares immutable constants near its beginning:

```sh
AVA_VERSION='1.2.3'
AVA_TAG='v1.2.3'
AVA_CHANNEL='stable'
AVA_SOURCE_REVISION='0123456789abcdef0123456789abcdef01234567'
```

Each tar archive contains an `ava-asset.json` file at its root with:

- `asset_schema`
- `asset_name`
- `asset_role`
- `ava_version`
- `tag`
- `channel`
- `source_repository`
- `source_revision`

The release notes begin with equivalent YAML frontmatter. `SHA256SUMS` contains only digest and filename records and receives its release identity from the immutable release attestation and the manifest it authenticates.

Release automation rejects assets whose embedded identity differs from `ava-release.json`, the tag target, or the workflow checkout revision.

# Release manifest

`ava-release.json` is the authoritative machine-readable contract consumed by release validation, the installer, and the updater.

It contains:

- release schema revision
- Ava version, tag, channel, repository, and source revision
- publication timestamp
- minimum supported installer protocol
- complete uploaded asset inventory
- SHA-256 and byte size for every asset except `ava-release.json` and `SHA256SUMS`
- source-to-installed mapping for all managed payload and create-if-absent scaffold content
- supported direct upgrade sources and required intermediate releases
- semantic review requirement
- manifest schema and OKF version impact
- deterministic migration and guidance inventories

The release manifest does not contain its own checksum. `SHA256SUMS` records the digest of `ava-release.json` and every other asset except itself. After installation, `/.ava/state/manifest.json` records the verified `ava-release.json` digest as `release.release_manifest_sha256`.

The release manifest schema rejects unknown top-level fields. Future additions require an explicit schema revision and must follow the Ava compatibility contract.

# Archive rules

All release archives are reproducible inputs to the deterministic installer.

- Paths are relative and use `/` separators.
- Absolute paths, `..` traversal, device nodes, sockets, and hard links are prohibited.
- Symlinks are prohibited in the initial release format.
- File ownership is normalized to numeric user and group `0`.
- Modification times are normalized to `SOURCE_DATE_EPOCH`, derived from the source commit time.
- Entries are sorted bytewise by path.
- Locale and timezone are fixed during assembly.
- Gzip headers omit original filenames and use the normalized timestamp.
- Archive extraction never writes directly into the target project before validation and collision classification complete.

Release validation builds the assets twice in clean environments and compares their SHA-256 digests. A mismatch blocks publication.

# Distribution channels

## Stable

A stable release has canonical version `X.Y.Z`, tag `vX.Y.Z`, channel `stable`, and is not marked as a GitHub prerelease. It may become GitHub's latest release and is eligible for the `/releases/latest/download/` convenience URL.

Stable release automation must explicitly set the release as latest only after all validation succeeds. Stable installers never select prereleases.

## Prerelease

A prerelease uses one of the accepted identifiers:

- `X.Y.Z-alpha.N`
- `X.Y.Z-beta.N`
- `X.Y.Z-rc.N`

The channel is derived from the identifier and the GitHub release is marked as a prerelease. Prereleases are available only through exact version-pinned URLs and are never selected by `/releases/latest/`.

Prerelease-to-prerelease upgrade support is opt-in and must be declared in the target release manifest.

## Development

Development builds are GitHub Actions artifacts identified by full source revision and workflow run. They are mutable by retention and rerun behavior, are not GitHub Releases, receive no stable URL, and are never consumed by the installer unless an explicit development workflow downloads and validates them.

Development artifacts must use names that include the full source revision and must never use a stable or prerelease tag name. They may be deleted according to Actions retention policy without violating release retention guarantees.

# Integrity and authenticity

Ava distinguishes byte integrity from publisher authenticity.

## SHA-256 integrity

`SHA256SUMS` and the digest fields in `ava-release.json` detect corruption, truncation, substitution, and inconsistent assembly after the expected digest has been authenticated.

Checksums downloaded from the same unverified release do not independently authenticate the publisher or solve the bootstrap trust problem. The convenience path therefore relies on GitHub and repository trust. The verified path authenticates the immutable release attestation before executing the installer.

## Immutable release attestation

Ava uses GitHub immutable releases as its initial authenticity and release-provenance mechanism.

When release immutability is enabled, publishing the completed draft locks the release tag and uploaded assets and causes GitHub to generate a cryptographically verifiable release attestation covering the release tag, commit SHA, and release assets.

Ava does not initially add a second Sigstore key or project-managed signing hierarchy. This keeps the trust model minimal and avoids presenting two partially overlapping authorities. A future independent signing mechanism would be a separate approved architectural change and must document its key custody, rotation, revocation, and recovery model.

The GitHub attestation proves what GitHub published for the repository. It does not prove that the source was benign, that the workflow was uncompromised, or that the publisher account and repository controls were secure before publication.

# Bootstrap trust modes

## Convenience mode

Convenience mode executes the stable or pinned immutable installer directly:

```sh
curl -fsSL https://github.com/phdah/ava/releases/latest/download/ava-install.sh | sh
```

```sh
curl -fsSL https://github.com/phdah/ava/releases/download/v1.2.3/ava-install.sh | sh
```

Trust assumptions:

- GitHub account and repository ownership are trusted.
- TLS and GitHub release delivery are trusted.
- The selected immutable release is trusted.
- The bootstrap installer is executed before the consumer independently verifies it.

After startup, the installer verifies release identity and SHA-256 digests before extracting or applying payloads. This protects subsequent payload integrity but does not retroactively authenticate the already executed bootstrap script.

Any failed download, identity mismatch, unsupported channel, checksum mismatch, malformed manifest, unsafe archive entry, or immutable-release verification requirement aborts before project mutation.

## Verified mode

Verified mode requires an exact pinned tag and GitHub CLI support for immutable release verification.

```sh
version='v1.2.3'
curl -fsSLO "https://github.com/phdah/ava/releases/download/${version}/ava-install.sh"
gh release verify "$version" --repo phdah/ava
gh release verify-asset "$version" ./ava-install.sh --repo phdah/ava
sh ./ava-install.sh
```

The consumer verifies the release attestation and the downloaded installer's digest before execution. The installer then downloads and verifies `ava-release.json`, `SHA256SUMS`, and required payload assets.

Verified mode aborts when:

- the tag is absent or not immutable
- the release attestation is missing or invalid
- the local installer is not an attested asset of that release
- the attested tag or source revision disagrees with embedded installer identity
- any manifest, checksum, asset identity, archive-safety, or compatibility validation fails

Verification of the generated GitHub source archive is not supported and is irrelevant because Ava does not use it as a release asset.

# Repository configuration

Release immutability must be enabled before the first stable or prerelease publication. For this repository, an administrator enables **Settings > Releases > Enable release immutability**.

The setting affects future releases only. Releases published before it is enabled are not retroactively made immutable and must not be treated as supported Ava distributions.

Release automation performs a preflight request to GitHub's repository immutable-releases endpoint and requires:

```json
{
  "enabled": true
}
```

The response may also report that immutability is enforced by the repository owner. A missing or disabled setting blocks publication.

# Publication transaction

Release automation builds all assets from one clean checkout of the full source revision.

1. Resolve and validate the canonical version, tag, channel, and source revision.
2. Require the release tag to exist and point to the checked-out source revision.
3. Confirm repository release immutability is enabled.
4. Build every required asset twice and require identical digests.
5. Validate archive safety, embedded identity, JSON schemas, checksums, installed mapping, compatibility declarations, and release-note coverage.
6. Create a GitHub Release as a draft targeting the existing tag.
7. Upload all seven required assets without replacement or clobber behavior.
8. Re-fetch the draft and verify exact filenames, byte sizes, and uploaded digests.
9. Publish the draft. Publication is the point at which the release becomes immutable.
10. Verify the published release attestation, immutable state, tag target, and every local asset against the release.
11. For stable releases, confirm `latest` resolves to this release only when intended.
12. Record the verification result and release URL in the workflow summary.

No step may edit a published release, move or recreate its tag, replace an asset, or reuse the tag name. A failed post-publication verification is a release incident, not a reason to mutate the release. Corrective work uses a new version.

# Post-publication verification

Automation and maintainers must be able to repeat these checks:

```sh
gh release view v1.2.3 --repo phdah/ava --json tagName,isDraft,isPrerelease,isImmutable,targetCommitish,assets
gh release verify v1.2.3 --repo phdah/ava
```

For each locally retained asset:

```sh
gh release verify-asset v1.2.3 ./dist/ASSET_NAME --repo phdah/ava
```

Verification additionally checks:

- `isImmutable` is `true`
- `isDraft` is `false`
- prerelease state matches the derived channel
- the tag points to `source_revision`
- the asset set is exact, with no missing or unexpected Ava assets
- `SHA256SUMS` validates every other asset
- `ava-release.json` conforms to its schema
- all embedded release identities match

A release that fails any check is unsupported and must not be installed automatically.

# Retention and deletion

Supported GitHub Release assets are retained indefinitely while the repository exists. Support windows determine maintenance and upgrade guarantees, not asset deletion.

Immutable releases may be deleted only for legal, security, or repository-recovery reasons requiring explicit maintainer action. Deletion does not authorize reuse of the same release tag. A security withdrawal must publish an advisory or replacement release and cause installers to reject the withdrawn version through later release metadata when technically possible.

Development Actions artifacts follow repository retention settings and have no indefinite availability guarantee.

# Required release validation

A release candidate cannot be published unless automated validation proves:

- canonical SemVer, tag, and channel consistency
- one source revision across tag, checkout, manifest, installer, archives, and notes
- exact required filenames and media types
- schema-valid `ava-release.json`
- complete and non-cyclic checksum coverage
- safe and reproducible archives
- complete source-to-installed ownership mapping
- complete local inline Markdown link resolution against assembled installed destinations
- declared direct or chained upgrade support
- guidance and migration inventories consistent with their archives
- SemVer rationale and semantic-review impact in release notes
- immutable releases enabled before publication
- immutable and attested state after publication
- successful attestation verification for the release and every asset
