---
type: Internal Development Task
title: Dogfood the Alpha and Track Findings
description: Exercise the published alpha through real Ava and OpenCode usage, convert defects into bounded roadmap tasks, and publish additional prereleases when another validation cycle is required.
tags: [internal, roadmap, alpha, dogfooding, defects, opencode]
status: pending
phase: 5
order: 3
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
---

# Dogfood the Alpha and Track Findings

## Purpose

The alpha exists to expose failures that fixtures and design review did not reveal. This task validates Ava as an agent-first product using the published immutable assets rather than repository-local shortcuts.

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
- exact-version prerelease upgrade when a later alpha is published

Use realistic projects large enough to expose discovery, path, ambiguity, context-loading, and performance problems. Do not limit dogfooding to synthetic minimal fixtures.

## Finding handling

For every finding:

1. record the observed behavior and reproduction conditions
2. classify it as `blocker`, `required-v1`, or `post-v1`
3. determine whether the failure is in contracts, templates, routing, host integration, release tooling, validation, documentation, or implementation
4. create a bounded task file when repository work is required
5. insert blocking and required-v1 tasks before the release stage they block
6. update the relevant phase index and current roadmap counts

Do not bury unresolved defects only in prose, issue comments, or an informal checklist.

## Additional prereleases

Publish another `alpha.N` when completed fixes require validation through immutable public assets. Add a bounded publication task specifying:

- the exact version
- supported source prereleases
- compatibility impact
- required guidance and migrations
- the repeated dogfood scope

A beta may be introduced when useful, but it is not mandatory. The roadmap must describe its purpose and gate rather than using the label decoratively.

## Completion criteria

- the published alpha has been exercised through realistic OpenCode and project scenarios
- every discovered repository defect is represented by a bounded roadmap task or an explicit approved post-v1 decision
- no blocker remains open
- every required-v1 finding is complete or scheduled before stable qualification
- recovery and uninstall have been performed against published assets
- the latest supported prerelease has a tested upgrade path toward the release candidate
- the roadmap and phase indexes accurately represent all inserted alpha work
