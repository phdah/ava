---
type: Internal Development Task
title: Qualify and Publish 1.0.0
description: Apply the stable acceptance gate, verify upgrade from the release candidate, and publish Ava's first supported stable distribution.
tags: [internal, roadmap, releases, stable, v1, publishing]
status: pending
phase: 5
order: 6
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-07T15:45:02+02:00
---

# Qualify and Publish `1.0.0`

## Stable acceptance gate

Stable publication requires:

- no unresolved blocker or required-v1 task
- [published release-candidate stabilization](05a-stabilize-release-candidate.md) is complete
- no known corruption, project-owned overwrite, path escape, authority bypass, or unrecoverable transaction defect
- public format, metadata, roles, workflows, routing, ownership, host, state, release, and migration contracts are frozen and aligned
- every maintained validator and conformance fixture passes
- OpenCode passes fresh-install, repeated-session, upgrade, recovery, and uninstall fixtures
- Ava Maintenance and Upgrade Role authority boundaries pass all state transitions
- the latest RC upgrades to `1.0.0` through an explicitly declared and tested path
- user-facing installation, verified bootstrap, OpenCode setup, maintenance, recovery, upgrade, semantic reconciliation, and removal documentation is complete
- release assembly is reproducible from one clean source revision
- release automation uses the same assets and paths validated by CI and dogfooding
- a revision-bound machine-readable stable qualification result references the complete generated-vault and release evidence
- known post-v1 work is documented without weakening v1 guarantees

## Prepare

- delete all immutable alpha prerelease GitHub Releases in order from oldest to newest, then delete their now-unlocked tags; this removes the old commit SHAs containing redacted content from accessible history and source archives (note: deleted immutable release tag names cannot be reused)
- build the exact seven-asset stable release set twice and require identical digests
- verify fresh installation and RC-to-stable upgrade from assembled assets
- verify semantic compatibility transitions independently from installed `ava_version`
- verify the stable convenience URL will resolve only after publication is complete
- verify the pinned authenticated installation path
- verify GitHub release immutability is enabled and detectable
- prepare final release notes with SemVer rationale, support guarantees, trust assumptions, host support, known limitations, and supported upgrade sources
- update the README and other public status documentation so they describe the implemented release tooling and the exact stable support boundary

## Publish

- obtain explicit approval for version `1.0.0` and the exact source revision
- create the immutable `v1.0.0` tag and draft GitHub Release through the maintained release automation
- attach and verify exactly the required assets
- publish the release as stable and set it as `latest` only after every check succeeds
- verify GitHub reports the release as immutable
- verify the release attestation, tag target, asset inventory, checksums, and published download URLs
- install fresh and upgrade from the latest RC using the published assets
- update repository documentation to identify `1.0.0` as the first supported stable Ava distribution

## Support boundary

Stable support guarantees begin at `1.0.0`. No historical unversioned Ava installation becomes supported merely because stable has been published.

Future changes follow the accepted Ava SemVer, deprecation, support-window, release-guidance, and upgrade contracts.

## Completion criteria

- `1.0.0` is published as an immutable stable GitHub Release from the approved source revision
- the stable convenience URL installs the published release
- the pinned verified flow authenticates and installs the same release
- the latest supported RC upgrades successfully to stable
- OpenCode is documented and tested as a supported host
- installed base version and project semantic compatibility remain separately observable
- recovery, finalization, and role-led uninstall work against the published stable assets
- all stable acceptance evidence is recorded and no required-v1 work remains open
