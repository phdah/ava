---
type: Internal Development Task
title: Dogfood the Alpha and Track Findings
description: Exercise published prereleases through real Ava and OpenCode usage, manage findings in a durable backlog, and continue until the user explicitly closes dogfooding.
tags: [internal, roadmap, alpha, dogfooding, defects, opencode]
status: pending
phase: 5
order: 4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-05T09:00:00+02:00
---

# Dogfood the Alpha and Track Findings

## Purpose

The alpha exists to expose failures that fixtures and design review did not reveal. This task validates Ava as an agent-first product using published immutable assets rather than repository-local shortcuts.

This is an umbrella task for the complete dogfood period. Individual findings are managed through the [Alpha Dogfood Findings](dogfood/) backlog so new work can be added and resolved without renumbering the six core Phase 5 release gates.

## Completion authority

Dogfooding remains active until the user explicitly declares it complete. The following do not complete this task automatically:

- resolving every currently known finding
- temporarily having no pending findings
- publishing another alpha, beta, or release candidate
- passing repository and release qualification
- completing an individual dogfood task

Only an explicit user decision may change this task to `completed` and advance the current roadmap task to release-candidate publication.

## Dogfood scope

Exercise at least:

- installation into an empty project
- installation into a mature non-Ava project with existing project-owned Markdown and host configuration
- a clean OpenCode startup and repeated sessions against the installed project
- free-form role routing and every managed workflow
- role creation, project context maintenance, inbox ingestion, and independent review
- Ava Maintenance version and state explanation
- modified, missing, and corrupt managed-file diagnosis
- interrupted deterministic upgrade recovery through resume, abort, rollback, and finalize
- semantic upgrade routing and completion through the Upgrade Role
- role-led uninstall with project-owned content preserved
- reinstall after uninstall
- exact-version prerelease upgrades between every supported published transition

Use realistic projects large enough to expose discovery, path, ambiguity, context-loading, and performance problems. Do not limit dogfooding to synthetic minimal fixtures.

## Backlog operation

The [dogfood findings index](dogfood/index.md) is the stable entry point for adding and resolving findings.

For every finding:

1. record the observed behavior and reproduction conditions
2. classify it as `blocker`, `required-v1`, or `post-v1`
3. determine whether the failure is in contracts, templates, routing, host integration, release tooling, validation, documentation, or implementation
4. create one bounded finding task when repository work or an explicit disposition is required
5. add it to the findings index using the next unused number
6. make the first pending finding the current next actionable task

The resolving implementation PR updates the finding task and findings index together. Completed findings remain as durable evidence and are never deleted or renumbered.

Do not bury unresolved defects only in prose, issue comments, CI logs, release comments, or an informal checklist.

## Release-gate ordering

- `blocker` findings must be resolved before the next prerelease is published.
- `required-v1` findings must name whether they block the next prerelease, release candidate, or stable release.
- accepted `post-v1` findings require an explicit rationale and user-approved disposition.
- no release-candidate task becomes current while this umbrella task remains pending.

## Additional prereleases

Publish another `alpha.N` when completed fixes require validation through immutable public assets. Add a bounded publication task when the release itself requires work beyond the finding that motivates it, specifying:

- the exact version
- supported source prereleases
- compatibility impact
- required guidance and migrations
- the repeated dogfood scope

A beta may be introduced when useful, but it is not mandatory. The roadmap must describe its purpose and gate rather than using the label decoratively.

## Completion criteria

After the user explicitly declares dogfooding complete:

- published prereleases have been exercised through realistic OpenCode and project scenarios
- every discovered finding is represented in the findings index with a completed resolution or explicit approved post-v1 disposition
- no blocker remains pending
- every required-v1 finding is complete or placed before the release gate it blocks
- recovery and uninstall have been performed against published assets
- the latest supported prerelease has a tested upgrade path toward the release candidate
- the roadmap, phase index, and findings index accurately represent all dogfood work
- this task and the phase index are updated together to make release-candidate publication current
