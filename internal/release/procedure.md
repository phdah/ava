---
type: Internal Release Procedure
title: Ava Release Publication Procedure
description: Defines release-please preparation, agent completion of release-specific upgrade state, approval, publication, verification, and failure handling for immutable Ava releases.
tags: [internal, releases, publication, verification, maintenance]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T10:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-06T15:55:00+02:00
---

# Ava Release Publication Procedure

This procedure coordinates maintainers around the public contracts under `/distribution/`. It does not replace deterministic release automation and must never be included in an Ava release payload.

Ava has one release flow for alpha, beta, release candidate, and stable releases. The proposed version and channel come from the release-please pull request. Release-specific upgrade edges are never prepared in an ordinary implementation pull request.

# Release chain

1. A normal pull request containing a user-facing releasable change is merged to `main`.
2. Release-please creates or updates `release-please--branches--main` with the proposed version, changelog, version file, and manifest state.
3. The release pull request is expected to fail the `Release PR policy` check until its release-specific upgrade review has been completed.
4. When an agent is asked to merge the release pull request, it first completes the release state directly on that release-please branch.
5. The agent inspects every change included since each required source release, writes `internal/release/upgrade-impact.json`, validates the actual tagged source deltas, and pushes the completed release state.
6. The release pull request may be merged only after all required checks pass.
7. Merging the release pull request authorizes the exact proposed version and tagged source revision for qualification and publication.
8. The release workflow creates the immutable tag and draft release, reruns qualification, assembles reproducibly, validates, attests, uploads, and publishes.

# Channel configuration

The channel is derived from the proposed SemVer version:

- `x.y.z-alpha.n` is alpha
- `x.y.z-beta.n` is beta
- `x.y.z-rc.n` is release candidate
- `x.y.z` is stable

The release-please configuration must match that channel. Continuing within the current channel requires no configuration change. Moving to beta, release candidate, or stable requires a separate reviewed change to `release-please-config.json` before release-please proposes the first release in that channel.

# Required direct sources

For every release after the first, qualification derives the minimum direct source set from:

- the immediately previous published version
- every direct source declared by the previous release
- any source listed in `internal/release/fixtures/release-upgrade-policy.json`

For older releases that predate `upgrade-impact.json`, qualification reads the legacy `upgrade-sources.txt` from the immutable previous tag. Current releases use only `upgrade-impact.json` as the source of truth.

A release pull request may retire an inherited source only by adding it to `retired_sources` with a non-empty reviewed reason. A protected source cannot be retired inside the release pull request. Its protection must first be changed through a separate ordinary pull request.

# Agent completion of a release pull request

Before merging a release-please pull request, the Ava Internal Maintainer must:

1. Confirm that `version.txt`, `.release-please-manifest.json`, the pull-request proposal, and release-please channel configuration agree.
2. Confirm that the target is newer than the version on the pull-request base revision.
3. Determine the required direct source set from immutable release history and the upgrade policy.
4. Review all changes included between each source tag and the proposed target.
5. Create or replace `internal/release/upgrade-impact.json` directly on the release-please branch.
6. For every source, record exact retained, replaced, created, and deleted managed paths.
7. For every created, replaced, or deleted managed path, record one `semantic_impact_evidence` item with the installed path, whether that specific contract change affects project-owned context, and the evidence-backed reason.
8. Record the deterministic migration IDs and installed guidance paths required for that source.
9. Set `semantic_review_required` to the logical result of the path-by-path evidence, then provide an explicit overall assessment. A `false` decision is never an implicit default.
10. When any evidence item affects project-owned context, provide bounded guidance for the source edge. When no evidence item does, declare no guidance for that edge.
11. Reference every changelog release after the source through the target. The validator requires exact cumulative coverage.
12. Record any explicit source retirement and its reviewed reason.
13. Run `validate_release_pr.py`, `validate_upgrade_impact.py`, and the complete maintained release test suite.
14. Push the release state and confirm every required pull-request check passes.
15. Merge the release pull request.

The validator uses the deterministic managed delta only to require complete review scope. It does not infer semantic impact from file names, diffs, or arbitrary prose. The maintainer remains responsible for the substantive judgment, and reviewers must challenge unsupported reasons.

Empty migration lists remain valid when normal managed reconciliation is sufficient. Empty guidance lists are valid only when every changed managed path has explicit no-impact evidence and the overall assessment explains why project-owned context remains compatible.

# Release-specific impact format

`internal/release/upgrade-impact.json` belongs to the release pull request and is the only current declaration used to build `upgrade_paths.edges`.

Schema version 2 contains:

- the exact target version
- explicit retired sources and reasons
- one reviewed assessment per direct source
- exact managed payload deltas
- one semantic evidence item for every created, replaced, or deleted managed path
- deterministic migration references
- source-edge semantic-review decisions and exact guidance references
- explicit overall semantic assessments, including no-impact explanations
- cumulative changelog versions

The evidence list must exactly cover the changed managed paths. `semantic_review_required` must equal whether any evidence item declares project-owned impact. A required review must have at least one guidance path, and a no-impact edge must have none.

The reviewed assembler derives the manifest edge source set directly from this file. It copies `semantic_review_required`, `migration_ids`, and `guidance_paths` onto each exact source-to-target edge. The release-wide semantic flag is only a summary across edges and must not drive a different source edge.

# Approval boundary

Reviewing and merging the release-please pull request is the explicit publication approval. Approval of implementation work, release tooling, policy, or an unmerged release proposal does not authorize publication.

A release pull request remains blocked when:

- the release-specific impact file is missing, uses an obsolete current schema, or targets another version
- required inherited sources are omitted
- a protected source is retired without a prior policy change
- managed deltas disagree with the tagged source comparison
- semantic evidence omits or invents a changed managed path
- the semantic-review decision disagrees with its evidence
- semantic review is required without bounded guidance
- guidance is declared for an edge assessed as having no project-owned semantic impact
- migration or guidance references are absent from the release assets
- cumulative changelog references are incomplete
- the release-please channel configuration disagrees with the proposed version
- any maintained qualification check fails

# Automated publication

After the release pull request is merged, the workflow must:

1. Bind the release-please tag, version, full source revision, and derived channel.
2. Rerun release PR and upgrade-impact validation against the exact tagged source.
3. Run the complete maintained qualification suite.
4. Assemble every required asset twice from the reviewed impact and require identical digests.
5. Validate release conformance and confirm the GitHub Release is still a draft.
6. Attest and upload the complete asset set without replacement.
7. Publish the existing draft without moving the tag or recreating the release.

Any failure leaves publication blocked. Existing tags or uploaded assets are never moved, overwritten, or reused.

# Post-publication verification

After publication, verify:

- the release is immutable and no longer a draft
- prerelease and latest status match the channel
- the tag and release target match the verified source revision
- every asset and checksum verifies
- every declared direct source upgrades successfully
- each installed journal edge preserves its reviewed semantic decision and exact guidance paths
- Ava-managed state advances correctly
- project-owned files remain byte-for-byte preserved until the Upgrade Role applies required semantic guidance
- normal routing remains blocked until semantic compatibility advances and the transaction is finalized

Record the release URL, source revision, supported sources, per-source results, and incidents in the required release history.

# Failure handling

Before publication, correct the defect on the release pull request. If an immutable tag already exists, use a new version. Never move or recreate a tag, overwrite an asset, or reuse a published version.

After publication, a failed verification is a release incident. Corrective work uses a new release or an explicit security withdrawal under the public release contract.
