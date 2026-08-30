---
type: Internal Development Task
title: Harden Qualification OpenCode Permissions
description: Make temporary qualification and audit evidence readable by every maintained OpenCode session without relying on hidden global host configuration.
tags: [internal, roadmap, release, qualification, opencode, permissions, reliability]
status: complete
phase: 5
parent: 04c-automate-release-qualification-evidence
order: 4.4
generated:
  by: agent:openai-chatgpt
  at: 2026-08-30T14:00:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-30T15:32:00+02:00
---

# Harden Qualification OpenCode Permissions

## Purpose

Remove the host-permission failure observed during `v1.0.0-alpha.15` qualification, where the independent audit could not read qualification evidence under `/tmp` and therefore failed despite a mechanically successful 17-scenario run.

The release process must not depend on an undocumented personal or global OpenCode configuration to read the temporary roots that Ava itself creates.

## Approved direction

Use both repository-level host configuration and qualification-owned session configuration:

- track an Ava-root OpenCode configuration that grants the repository's OpenCode agents the required access to `/tmp/**`; remove the current `opencode.json` Git ignore rule if tracking that file is the correct implementation
- preserve existing project configuration semantics rather than replacing unrelated OpenCode settings
- make `qualify-release.sh` and its maintained OpenCode adapter explicitly provide the required temporary-root permission to every OpenCode session they spawn, including scenario agents, nested sessions, and the independent audit
- bind qualification-owned permission to the temporary roots used by the current operation rather than assuming the caller has equivalent global OpenCode permissions
- keep the automated qualification path non-interactive once the user starts it

The tracked root configuration is useful for ordinary Ava development and direct OpenCode use. The qualification-owned permission is the release-system guarantee and must work even when the caller has no permissive global OpenCode configuration.

## Implementation

The completed implementation uses both layers without making the tracked project file a release-system dependency:

- root `opencode.json` is tracked and grants `permission.external_directory` access to `/tmp/**` for ordinary Ava development and direct repository sessions
- `qualify-release.sh` creates a unique repository-external operation parent under the selected run-root parent and binds the automation to that parent
- the wrapper includes any caller-supplied source or target asset directory that is outside both the repository and the operation parent in the qualification-owned external-root scope
- `qualification-opencode.sh` requires that scope for every `opencode run` and merges exact `<root>/**` allow rules into `OPENCODE_CONFIG_CONTENT` without replacing unrelated inline configuration or permission defaults
- the same inline configuration is inherited by scenario sessions and nested OpenCode work, while the repository-root independent audit receives explicit access to the generated evidence root
- session listing and export behavior remain unchanged, including the existing large-JSON buffering workaround
- generated workspaces, transcripts, raw evidence, and qualification roots remain outside Git

The adapter fails before starting an OpenCode run when qualification-owned external-root scope is absent or unsafe. This makes the maintained automation self-contained instead of falling back to user-global permission state.

## Implementation considerations

- inspect the current OpenCode permission schema and use the narrowest supported rule that reliably permits maintained qualification work under `/tmp`
- ensure permission configuration is passed through the repository-owned OpenCode adapter rather than duplicated ad hoc across individual scenarios
- include the independent audit explicitly, because it executes from the Ava repository while reading evidence from an external temporary run root
- do not weaken evaluator-only fixture separation or expose oracle content to qualification agents
- do not solve the problem by relocating qualification evidence into the repository

## Regression coverage

Regression tests now demonstrate that:

- the tracked repository OpenCode configuration contains the deliberate `/tmp/**` external-directory policy and is no longer ignored
- every adapter `run` receives exact qualification-owned external-root rules
- existing inline model and unrelated permission configuration is preserved, including scalar permission defaults
- missing qualification-owned scope fails before OpenCode starts
- an audit-style run rooted in the Ava repository can read generated external evidence when no user-global OpenCode configuration is supplied
- `qualify-release.sh` wires a unique operation parent and external asset roots into the adapter
- generated workspaces, raw transcripts, and execution evidence remain repository-external by construction

## Completion criteria

- Ava has a deliberate, reviewable OpenCode permission policy for its temporary development and qualification roots
- every maintained qualification OpenCode session receives sufficient temporary-root access automatically
- a fresh audit can read the exact run evidence it is given without a permission rejection
- repository tests cover the permission propagation path
- the release procedure no longer has a hidden dependency on local OpenCode permission state

## Completion

Complete. Qualification-owned permission is now propagated through the maintained adapter independently of user-global OpenCode configuration, with tracked repository policy and regression coverage for the audit failure mode.
