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
  at: 2026-08-06T16:18:00+02:00
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

- [ ] installation into an empty project
- [x] installation into a mature non-Ava project with existing project-owned Markdown and host configuration
- [ ] a clean OpenCode startup and repeated sessions against the installed project
- [ ] free-form role routing and every managed workflow
- [ ] role creation, project context maintenance, inbox ingestion, and independent review
- [x] Ava Maintenance version and state explanation
- [ ] modified, missing, and corrupt managed-file diagnosis
- [ ] interrupted deterministic upgrade recovery through resume, abort, rollback, and finalize
- [ ] semantic upgrade routing and completion through the Upgrade Role
- [x] role-led uninstall with project-owned content preserved
- [ ] reinstall after uninstall
- [ ] exact-version prerelease upgrades between every supported published transition

Use realistic projects large enough to expose discovery, path, ambiguity, context-loading, and performance problems. Do not limit dogfooding to synthetic minimal fixtures.

## Completed scenario evidence

### Non-empty project installation

On 2026-08-05, the version-pinned `1.0.0-alpha.4` installer completed successfully in a real non-empty project. It created the managed `/.ava/` payload and root `/AGENTS.md`, reported semantic compatibility complete through alpha.4, and left host discovery in the expected `explicit-only` state.

The installer skipped the existing project-owned `/index.md`, `/inbox/`, `/knowledge/`, `/roles/`, `/shared/`, and `/workflows/` scaffold destinations rather than replacing them. It also detected the existing project-owned `/opencode.json`, left it unchanged, and reported the permission fragment available for optional manual integration.

### Corrective prerelease upgrades

On 2026-08-05, real installations upgraded successfully from both supported direct sources, `1.0.0-alpha.3` and `1.0.0-alpha.4`, to `1.0.0-alpha.5` using the version-pinned published installer. Both runs retained the byte-identical managed payload, advanced installed and semantic compatibility state through alpha.5, and preserved the existing project-owned OpenCode configuration.

On 2026-08-06, a real project at `~/stuff/project-vault/` was freshly installed with immutable `1.0.0-alpha.6` assets and upgraded with immutable `1.0.0-alpha.7` assets. The updater retained all 54 recorded managed payload files, advanced installed and semantic compatibility through alpha.7, produced a terminal `complete` journal with only normal routing allowed, and preserved the existing project-owned OpenCode configuration.

### Alpha.7 installed-link validation

After the alpha.7 upgrade, the agent activated the Inbox Ingester through normal routing without processing any inbox content. It loaded the managed role index and all seven required-reading documents in declared order.

The cross-root links resolved exactly against the installed project:

- inbox convention to `./inbox/index.md`
- root router to `./AGENTS.md`
- managed role registry to `./.ava/base/roles/index.md`
- document metadata and knowledge organization to their managed shared-instruction paths

Every target existed and was readable. No repository-source substitution, path guessing, file creation, mutation, or source movement occurred. This published immutable validation completes [finding 02](dogfood/02-repair-installed-context-link-resolution.md).

### Ava Maintenance installation inspection

The same alpha.7 installation was inspected through the Ava Maintenance role. The role correctly reported the installed version, release channel, source revision, OKF version, manifest shape, terminal journal, semantic compatibility, normal routing state, OpenCode permissions, and host integration state.

All 54 recorded payload checksums matched. No recorded managed file was missing, modified, corrupt, or non-regular. The inspection nevertheless returned `FAIL` because the successful updater left an empty unrecorded `./.ava/state/transactions/` directory after deleting its final transaction workspace.

The identity and state explanation scenario is exercised. The cleanup defect is resolved by completed [finding 06](dogfood/06-remove-empty-upgrade-transaction-containers.md). A corrective immutable release must still verify the fixed behavior through a real supported-source upgrade and healthy Ava Maintenance inspection before that release qualifies.

### Inbox ingestion and independent review

On 2026-08-05, the alpha.5 Inbox Ingester processed realistic work notes from 2026-02-20 through 2026-07-01 in a non-empty Obsidian vault. It preserved 46 dated sources, correctly recognized 16 frontmatter-only files, linked all 30 substantive sources through destination `sources` metadata, and created 23 indexed canonical concepts under a progressively discoverable `knowledge/work/` scope.

Independent review found that this file-level coverage did not satisfy the complete ingestion contract. The installed role had an unresolved mandatory link, substantial sections of one processed source had no canonical destination, an uncertain incident contributor was presented as a confirmed cause, several claims had incorrect or non-renderable attribution, completion counts were inaccurate, and the projects collection mixed stable subject classes in a hierarchy likely to become too flat.

The installed-link defect is now resolved and validated through completed finding 02. Remaining follow-up is tracked by [predictable knowledge hierarchy promotion](dogfood/03-make-knowledge-hierarchy-promotion-predictable.md) and [faithful inbox ingestion completion](dogfood/04-enforce-faithful-inbox-ingestion-completion.md). The combined role and workflow checklist remains open because role creation and project context maintenance have not yet been qualified with this evidence.

### Role-led uninstall

On 2026-08-05, Ava Maintenance removed a real `1.0.0-alpha.5` installation after verifying all 54 managed payload files were unchanged. It removed `/.ava/`, including its 53 payload files and two state files, and the managed root `/AGENTS.md`.

The operation confirmed that project-owned `/index.md`, `/inbox/`, `/knowledge/`, `/roles/`, `/shared/`, `/workflows/`, and `/opencode.json` remained present and unchanged. It also reported the now-inert `.ava/**` permission entries in `opencode.json` without modifying that project-owned file. Post-removal validation confirmed that both managed paths were absent and every listed project-owned path remained present.

## Backlog operation

The [dogfood findings index](dogfood/index.md) is the stable entry point for adding and resolving findings.

For every finding:

1. record the observed behavior and reproduction conditions
2. classify it as `blocker`, `required-v1`, or `post-v1`
3. determine whether the failure is in contracts, templates, routing, host integration, release tooling, validation, documentation, or implementation
4. create one bounded finding task when repository work or an explicit disposition is required
5. add it to the findings index using the next unused number
6. make the first actionable pending finding the current next task, respecting explicit dependencies

The resolving implementation PR marks the finding `completed` and updates the finding task and findings index together once the repository change, regression coverage, documentation, indexes, and resolution evidence are complete. Completed findings remain as durable evidence and are never deleted or renumbered.

When several completed findings require validation through the same published assets, validate them through one corrective prerelease when practical and append that evidence afterward. Published-asset or realistic-project checks that can only happen after merge are release qualification evidence. They do not keep or return an implemented finding to `pending`.

Do not bury unresolved defects only in prose, issue comments, CI logs, release comments, or an informal checklist.

## Release-gate ordering

- `blocker` findings must be resolved before the next prerelease is published.
- `required-v1` findings must name whether they block the next prerelease, release candidate, or stable release.
- accepted `post-v1` findings require an explicit rationale and user-approved disposition.
- completed findings may still require explicit immutable-release evidence before a release gate passes.
- no release-candidate task becomes current while this umbrella task remains pending.

## Additional prereleases

Publish another `alpha.N` when completed fixes require validation through immutable public assets. Add a bounded publication task when the release itself requires work beyond the finding that motivates it, specifying:

- the exact version
- supported source prereleases
- compatibility impact
- required guidance and migrations
- the repeated dogfood scope

On the release-please branch, complete the reviewed `internal/release/upgrade-impact.json` assessment for every required source-to-target edge. Qualification must fail until the proposed release declares, assesses, and tests every required transition.

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
