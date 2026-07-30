---
type: Internal Development Task
title: Define Release Logs and Agent Upgrade Guidance
description: Define structured release information that lets an Ava agent migrate project-owned context from one version to another through one explicit request.
tags: [internal, roadmap, releases, logs, migration, agents]
status: pending
phase: 4
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-07-30T11:26:00Z
---

# Define Release Logs and Agent Upgrade Guidance

## Goal

A user should be able to issue one explicit request to the local Ava agent to reconcile project-owned context after a deterministic base upgrade.

## Define

- how scoped `log.md` entries contribute to release change information
- which upgrade-relevant facts must be recorded more explicitly than ordinary conceptual history
- the release manifest or `UPGRADE.md` structure for source version, target version, changed contracts, affected project concepts, required decisions, and completion criteria
- how guidance references deterministic migration IDs and changed managed paths
- how an agent discovers all applicable guidance across a multi-version upgrade
- how the agent records semantic migration completion without hiding unresolved decisions
- the canonical one-prompt upgrade procedure and expected report

## Required distinction

Scoped logs remain human-readable conceptual history. They may be an input to release guidance, but an agent must not infer migration obligations from arbitrary log prose alone. Release-specific guidance must state compatibility impact and required action directly.

## Completion criteria

- define a structured, agent-readable release guidance contract
- define any required structure or metadata additions for upgrade-relevant `log.md` entries
- define the one-prompt semantic migration procedure
- define completion, partial completion, conflict, and user-decision states
- align the guidance with roles, workflows, manifests, validation, and release assets
