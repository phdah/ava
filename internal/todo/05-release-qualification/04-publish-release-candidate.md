---
type: Internal Development Task
title: Publish the 1.0.0 Release Candidate
description: Freeze the intended v1 public behavior and publish an immutable release candidate after alpha findings and required fixes are resolved.
tags: [internal, roadmap, releases, rc, publishing, compatibility]
status: pending
phase: 5
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
---

# Publish the `1.0.0` Release Candidate

## Entry gate

Do not begin until:

- alpha dogfooding is complete
- no blocker remains open
- every required-v1 finding that affects public behavior is complete
- the intended v1 format, role catalog, workflow catalog, routing, ownership, state, path, and OpenCode contracts are frozen
- no known incompatible public-contract change is planned before stable publication
- the latest supported alpha has an explicitly declared and tested path to the release candidate

## Prepare

- select `1.0.0-rc.1` unless an approved release sequence requires another canonical RC identifier
- build and verify the exact immutable asset set twice from one clean source revision
- run the complete conformance matrix against fresh installation and every supported prerelease source
- run the complete OpenCode fixture against assembled assets
- verify Ava Maintenance, Upgrade Role, recovery, finalization, and uninstall behavior
- verify release notes describe the full intended `1.0.0` behavior and every remaining known limitation
- verify documentation presents the RC as a final compatibility candidate rather than stable support

## Publish

- obtain explicit approval for the exact RC version and source revision
- create the immutable tag and draft GitHub Release
- mark it as a prerelease and never as `latest`
- upload and verify exactly the required asset set
- publish once all local and draft-release checks agree
- verify immutability, attestation, source revision, asset digests, and pinned URLs
- install and upgrade from the published assets

## RC policy

After RC publication:

- accept only release-blocking fixes, documentation corrections, or compatibility-preserving repairs required for stable qualification
- any incompatible contract or behavior change requires another RC and a repeated qualification cycle
- add every such fix as a bounded roadmap task before stable publication
- ensure `1.0.0` has a tested direct or declared chained upgrade path from the latest RC

## Completion criteria

- an immutable RC is published from the approved source revision
- fresh installation and every declared prerelease upgrade source pass using published assets
- OpenCode passes the complete supported-host fixture
- no known incompatible public change remains planned
- every remaining known issue is either a stable blocker or an explicitly approved post-v1 item
- the RC is ready to serve as the final input to stable qualification
