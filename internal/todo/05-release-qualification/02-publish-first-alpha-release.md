---
type: Internal Development Task
title: Publish 1.0.0-alpha.1
description: Build, verify, document, and publish the first immutable Ava prerelease for real installation and dogfooding.
tags: [internal, roadmap, releases, alpha, publishing]
status: pending
phase: 5
order: 2
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
---

# Publish `1.0.0-alpha.1`

This task begins only after the alpha acceptance and prerelease upgrade policy is complete and every alpha blocker passes.

## Prepare

- freeze the alpha candidate's public base bundle, role catalog, workflow catalog, schemas, path conventions, and OpenCode support documentation
- build all required release assets twice from one clean source revision and require identical digests
- validate the exact asset inventory, release identity, checksums, archive safety, guidance, migrations, and notes
- verify fresh installation into an empty project and a non-empty non-Ava project
- verify the documented OpenCode setup against the assembled alpha assets
- verify Ava Maintenance reporting, deterministic recovery coordination, and role-led uninstall against the assembled alpha assets
- verify the separately authenticated pinned-version installation path
- state clearly that no earlier Ava or unversioned installation is a supported upgrade source
- document known limitations, trust assumptions, and the alpha defect-reporting process

## Publish

- obtain explicit approval for version `1.0.0-alpha.1` and the exact source revision
- create the immutable tag and draft GitHub Release
- attach exactly the required release assets
- mark the GitHub Release as a prerelease and never as `latest`
- publish only after draft assets and metadata match the locally verified outputs
- verify release immutability, attestation, tag target, asset digests, and pinned download URLs after publication
- install once more from the published assets rather than local build output
- update repository documentation to identify the alpha as the current test release without presenting it as stable support

## Completion criteria

- `1.0.0-alpha.1` is published as an immutable prerelease from the approved source revision
- the release cannot be selected through the stable `latest` URL
- the convenience and verified pinned installation paths work from published assets
- OpenCode can load and use the published installation according to the supported-host contract
- Ava Maintenance can explain and safely remove the published installation
- release notes identify all known limitations and the absence of prior supported upgrade sources
- dogfooding can begin using the exact public assets a future user would install
