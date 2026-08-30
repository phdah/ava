---
id: ava-502
title: "Integrate release-please"
status: "Done"
labels: ["internal", "roadmap", "phase-05", "release"]
ordinal: 502
---

## Description

Configure release-please, Conventional Commit release classification, version and changelog management, and draft release orchestration before the first Ava alpha. The complete pre-Backlog task record is preserved below.

## Migrated task record

---
type: Internal Development Task
title: Integrate release-please
description: Configure release-please, Conventional Commit release classification, version and changelog management, and draft release orchestration before the first Ava alpha.
tags: [internal, roadmap, releases, automation, release-please, conventional-commits]
status: completed
phase: 5
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:28:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-04T14:40:00+02:00
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

## Implemented result

- added a single-package `simple` release-please configuration, empty manifest, bootstrap version file, and changelog
- bounded first-run history to commit `8e41b99b90000ce684aac589cb1ef25217598956` and selected `1.0.0-alpha.1` as the initial managed version
- added Conventional Commit pull-request title validation and machine-readable title, changelog, and channel policy fixtures
- configured release-please to maintain one release pull request and create `v<version>` tags plus draft GitHub Releases
- bound draft preparation to the exact release-please SHA, complete release tests, two identical assemblies, release conformance, asset attestation, draft-state verification, and non-clobbering asset upload
- documented the required token, branch protection, squash-title preservation, alpha-to-RC-to-stable transitions, and explicit publication boundary

## Validation

Covered `feat`, `fix`, breaking-change, documentation-only, internal-only, malformed, and unknown pull-request titles; first alpha/later prerelease/RC/stable channel examples; visible/hidden changelog classification; the single root package; draft-only release creation; exact tag/source revision handoff; and workflow guards for identity mismatch, non-draft state, duplicate asset upload, invalid title, and unsupported prerelease form.

## Completion criteria

- [x] release-please configuration and workflows are committed and validated
- [x] pull requests have an enforced Conventional Commit title contract at the merge boundary
- [x] release-please can prepare the `1.0.0-alpha.1` release pull request from the intended baseline
- [x] the resulting version, changelog, tag, and draft release identity are checked before qualification and upload
- [x] Ava's qualification and asset-building workflow runs against the exact prepared source revision
- [x] final publication still requires explicit approval for the exact canonical version and full source revision
- [x] no alpha release is published as part of this task
- [x] the roadmap advances to publishing `1.0.0-alpha.1`