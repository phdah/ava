---
type: Internal Development Task
title: Publish First Versioned Ava Release
description: Build, verify, document, and publish the first installable and upgradeable Ava distribution through GitHub Releases.
tags: [internal, roadmap, releases, publishing]
status: pending
phase: 4
order: 8
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T15:26:00Z
---

# Publish First Versioned Ava Release

This task begins after completion of all preceding phase tasks.

## Prepare

- select the initial release version according to the defined pre-1.0 or stable-version policy
- freeze the public base bundle, manifest schema, and separate semantic-compatibility schema for the release
- build the installer, bundle, integrity checksums, release manifest, notes, guidance, migrations, and provenance from one commit
- verify fresh installation through latest and pinned-version URLs
- verify the separately authenticated pinned-version installation path
- verify every supported upgrade path into the release
- document known limitations, compatibility guarantees, and trust assumptions

## Publish

- create the Git tag and GitHub Release
- attach the complete immutable asset set
- publish the selected signature, provenance, or attestation evidence
- mark the correct stable or prerelease channel
- verify downloaded assets independently after publication
- update repository documentation to reference the released version

## Completion criteria

- a user can install Ava through the documented convenience command
- a user can install a pinned version through the documented verified flow
- a project can record and validate installed `ava_version`
- semantic compatibility of project-owned context is separately observable
- the release can upgrade every explicitly supported prior state
- release notes and agent guidance accurately describe all compatibility-impacting changes
- documentation does not claim that same-release checksums independently authenticate the bootstrap installer