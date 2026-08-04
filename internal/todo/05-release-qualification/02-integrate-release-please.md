---
type: Internal Development Task
title: Integrate release-please
description: Configure release-please, Conventional Commit release classification, version and changelog management, and draft release orchestration before the first Ava alpha.
tags: [internal, roadmap, releases, automation, release-please, conventional-commits]
status: pending
phase: 5
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:28:00+02:00
---

# Integrate `release-please`

## Purpose

Introduce release automation before `1.0.0-alpha.1` so Ava versions and changelog entries are derived consistently from reviewed changes rather than assembled manually at publication time.

`release-please` coordinates release intent and preparation. Ava's qualification policy, deterministic assembler, conformance suite, exact version-and-revision approval, and final publication procedure remain authoritative.

## Accepted direction

- use `release-please` for version proposals, changelog maintenance, release pull requests, tags, and draft GitHub Release preparation
- classify releasable changes through Conventional Commit semantics
- enforce the merge-boundary format through Conventional Commit pull-request titles and squash merging so each merged pull request produces one canonical release-classified commit
- keep internal-only changes available as non-releasable commit types when they do not affect the distributed product
- bootstrap the first managed prerelease as `1.0.0-alpha.1` without interpreting the complete historical repository as unreleased product history
- never treat merging a release pull request, creating a tag, or preparing a draft release as authorization to publish

## Implementation requirements

- add the release-please action workflow and repository configuration for Ava's single-package release model
- add the maintained version file and changelog expected by the selected release strategy
- configure prerelease handling for the alpha, later prereleases, release candidate, and stable `1.0.0`
- add a pull-request check that rejects titles which cannot be classified according to the accepted Conventional Commit policy
- document the supported title types, breaking-change notation, and how internal-only work avoids an unintended release
- ensure the repository merge strategy preserves the validated pull-request title as the canonical commit consumed by release-please
- ensure release-please prepares a draft release rather than bypassing Ava's exact publication approval boundary
- connect a prepared release to the existing qualification, reproducible assembly, asset validation, attestation, and upload procedure
- use credentials or workflow structure that allow required validation and asset workflows to run for release-please-created pull requests and releases
- prevent duplicate tags, mutable replacement, or release creation from an unqualified source revision

## Validation

Cover at least:

- `feat`, `fix`, breaking-change, documentation-only, and internal-only pull-request titles
- expected version selection for prerelease and stable examples
- changelog generation from representative merged pull requests
- creation or update of one release pull request rather than competing release pull requests
- draft release preparation without final publication
- handoff of the exact tag and source revision to Ava qualification and deterministic assembly
- failure when a title, version transition, source revision, or release state conflicts with Ava's release contracts

## Completion criteria

- release-please configuration and workflows are committed and validated
- pull requests have an enforced Conventional Commit title contract at the merge boundary
- release-please can prepare the `1.0.0-alpha.1` release pull request from the intended baseline
- the resulting version, changelog, tag, and draft release identity agree with Ava's release manifest model
- Ava's qualification and asset-building workflows run against the exact prepared source revision
- final publication still requires explicit approval for the exact canonical version and full source revision
- no alpha release is published as part of this task
- the roadmap advances to publishing `1.0.0-alpha.1`
