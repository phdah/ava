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
  at: 2026-07-30T11:26:00Z
---

# Publish First Versioned Ava Release

## Prepare

- select the initial release version according to the accepted pre-1.0 or stable-version policy
- freeze the public base bundle and manifest schema for the release
- build the installer, bundle, checksums, release manifest, notes, guidance, and migrations from one commit
- verify fresh installation through the latest and pinned-version URLs
- verify every supported upgrade path into the release
- document known limitations and compatibility guarantees

## Publish

- create the Git tag and GitHub Release
- attach the complete immutable asset set
- mark the correct stable or prerelease channel
- verify downloaded assets independently after publication
- update repository documentation to reference the released version

## Completion criteria

- a user can install Ava with one release URL command
- a project can record and validate the installed Ava version
- the release can upgrade every explicitly supported prior state
- deterministic and semantic migration status is observable
- release notes and agent guidance accurately describe all compatibility-impacting changes
