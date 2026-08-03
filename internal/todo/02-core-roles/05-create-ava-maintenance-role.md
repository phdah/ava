---
type: Internal Development Task
title: Create the Ava Maintenance Role
description: Add the agent-facing role responsible for understanding installed Ava state, coordinating deterministic lifecycle operations, and safely removing Ava without introducing status, repair, or uninstall command surfaces.
tags: [internal, roadmap, roles, maintenance, status, recovery, uninstall]
status: completed
phase: 2
order: 5
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T18:13:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-08-03T21:47:00+02:00
---

# Create the Ava Maintenance Role

## Why

Ava is agent-first. Users should ask the active agent to inspect, explain, recover, upgrade, or remove Ava rather than learn a growing command interface for status, repair, and installation administration.

The installer and updater remain responsible for deterministic managed-state mutation. A dedicated managed role is required to interpret installed state, explain available actions, and invoke those deterministic operations through the host's available tools.

This public role must remain distinct from:

- the repository-only Ava Internal Maintainer under `internal/`
- the managed Upgrade Role that performs semantic reconciliation of project-owned context
- project roles that maintain roles, workflows, knowledge, or shared instructions

## Role responsibilities

Create a managed `ava-maintenance` role that can:

- report the installed Ava version, release channel, source revision, and OKF version
- explain semantic compatibility separately from the installed managed-base version
- inspect and explain `manifest.json` and `upgrade.json` without treating them as ordinary project documents
- identify missing, modified, corrupt, or unexpected managed files using manifest and release evidence
- explain host discovery and managed-context accessibility, including OpenCode configuration
- diagnose interrupted deterministic transactions and recommend the safe next action
- invoke existing deterministic installer operations such as resume, abort, rollback, finalize, or an explicit upgrade when authorized by the user and available through the host
- explain when deterministic recovery is impossible without a user decision
- remove Ava through a simple role-led filesystem operation when the installation is healthy and no transaction is active

## Agent-first interface

Do not add standalone `status`, `version`, `repair`, or `uninstall` command modes merely to expose this role's responsibilities.

The role may execute existing installer operations as implementation mechanisms, but the primary interface is a user request interpreted through Ava routing.

Repair means diagnosing the recorded transaction and using the existing resume, abort, rollback, finalize, reinstall, or upgrade mechanisms. The role must not invent a parallel repair protocol or manually reconstruct managed release content.

## Uninstall behavior

Uninstall is not a new deterministic release transaction. The role performs a bounded removal after inspection and explicit user intent.

It must:

1. verify the target is an Ava installation through the managed manifest
2. refuse or escalate when a deterministic or semantic transaction is active
3. report locally modified, missing, or unexpected managed content before removal
4. remove the managed `.ava/` directory
5. remove the root `AGENTS.md` only when it is still the recorded Ava-managed router
6. preserve project-owned roles, workflows, shared instructions, knowledge, inbox content, indexes, logs, and host entrypoints
7. report the exact removed and preserved paths

Removing `.ava/` while leaving the Ava-managed root router is incomplete because the router would reference missing managed content. Project-owned host entrypoints are never modified automatically; the role reports any stale reference for the user to remove or update.

## Routing and state authority

Define routing clearly across installation states:

- ordinary requests about Ava version, status, installation health, host access, recovery, upgrade preparation, or removal select Ava Maintenance
- deterministic transaction states that require resume, abort, rollback, or diagnosis select Ava Maintenance before ordinary project routing
- semantic reconciliation states continue to select the Upgrade Role
- Ava Maintenance may explain semantic state but must not mark semantic compatibility `partial`, `blocked`, or `complete`
- the Upgrade Role must not take over deterministic transaction recovery or general installation administration

Update the root router and shared upgrade-state contract so deterministic maintenance and semantic reconciliation have distinct pre-routing ownership.

## Required role structure

Create the mandatory role files and deterministic required-reading closure:

- `index.md`
- `role.md`
- `instructions.md`
- `capabilities.md`
- `constraints.md`

Register the role in the managed role catalog with narrow, non-overlapping routing conditions.

## Validation

Add fixtures covering:

- healthy installed-version and compatibility reporting
- missing, modified, corrupt, and unexpected managed content
- interrupted transaction diagnosis and each permitted deterministic next action
- deterministic state routing to Ava Maintenance
- semantic state routing to the Upgrade Role
- unavailable host capabilities and required user instructions
- OpenCode managed-context accessibility reporting
- successful uninstall of an unmodified installation
- uninstall refusal during active deterministic or semantic work
- modified root router and modified managed-directory cases
- preservation of every project-owned path and host entrypoint
- detection and reporting of a stale project-owned host entrypoint after removal

## Completion criteria

- users can ask Ava itself to understand and administer the installed distribution
- no new standalone status, version, repair, or uninstall command surface is required
- deterministic managed-state mutation remains inside installer and updater mechanisms
- deterministic recovery and semantic reconciliation route to different roles with explicit precedence
- uninstall removes all Ava-managed routing and state while preserving project-owned content
- the public Ava Maintenance role cannot be confused with or load the internal Ava Internal Maintainer role
- role catalog, router, state contracts, tests, indexes, and conceptual documentation remain aligned

## Implemented

- Added the complete managed `ava-maintenance` role with deterministic required reading.
- Split managed pre-routing between deterministic maintenance and semantic reconciliation.
- Narrowed Upgrade Role activation to project-owned semantic reconciliation.
- Defined agent-first status, integrity, recovery, host-access, explicit-upgrade, finalization, and bounded removal procedures.
- Kept manifest, journal, payload replacement, resume, abort, rollback, and finalization mutations inside existing deterministic tooling.
- Added machine-readable Ava Maintenance fixtures and focused tests for routing, integrity, host capability, OpenCode access, and removal preservation.
- Advanced the roadmap to the final validation, conformance, and upgrade-fixture task.
