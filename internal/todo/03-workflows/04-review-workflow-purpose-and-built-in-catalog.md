---
type: Internal Development Task
title: Review Workflow Purpose and Built-in Catalog
description: Define when a reusable workflow is justified and align the built-in catalog with free-form role work and deterministic release tooling.
tags: [internal, roadmap, workflows, catalog, routing]
status: pending
phase: 3
order: 4
timestamp: 2026-07-28T00:00:00Z
---

# Review Workflow Purpose and Built-in Catalog

## Why

The initial built-in catalog includes workflows that may duplicate ordinary free-form requests already handled by a role. Ava needs an explicit distinction between durable role behaviour, reusable procedures, and deterministic distribution mechanics before trigger portability and workflow lifecycle design are finalized.

A workflow should represent a repeatable, bounded semantic procedure or outcome with useful procedural constraints. It should not exist only to give a command-like name to normal work already covered by a role or to wrap installation, file replacement, checksum verification, deterministic migration, or structural validation.

## Define

- the boundary between a free-form request handled directly by a role and an explicitly invoked registered workflow
- the criteria that justify a reusable workflow, including repeatability, bounded scope, meaningful inputs, operating mode, required context, procedure, and expected output
- the warning signs that a proposed workflow merely restates a role responsibility or wraps deterministic installer and updater mechanics
- how workflows provide value for audits, reviews, batch processing, recurring maintenance, migration preparation, and standardized semantic upgrades
- how explicitly invoked workflows remain optional procedural scopes rather than the only way to request work from a role
- how workflow definitions are versioned and migrated without making Ava a workflow execution runtime

## Audit the built-in catalog

Evaluate every registered built-in workflow and classify it as:

- retain unchanged
- revise to express a stronger reusable procedure or outcome
- deprecate or remove because free-form role routing is sufficient
- replace with a role instruction, release migration procedure, deterministic installer behavior, or more useful workflow

The audit must specifically reassess command-like workflows such as `create-role`, `update-role`, `repair-role`, `configure-project`, and `tighten-instructions`. It must also evaluate whether the catalog needs outcome-oriented workflows such as reviewing the complete role catalog or applying release-specific semantic upgrade guidance to project-owned context.

Do not assume that any named workflow must be retained or removed before completing the audit.

## Dependencies and follow-up

Complete the distribution ownership, versioning, and migration contracts before this task. They determine which operations belong to release tooling and which semantic procedures may justify workflows.

Use the result as input to workflow trigger portability and workflow lifecycle ownership.

## Completion criteria

- document a clear purpose boundary between free-form role work, workflows, and deterministic release tooling
- define concrete criteria for adding a workflow to the built-in catalog
- audit every current built-in workflow against those criteria
- update, deprecate, replace, or remove workflows and registry entries according to the audit
- decide whether a semantic project-upgrade workflow is justified
- ensure retained workflows provide procedural value beyond ordinary free-form role routing
- ensure workflow bodies do not duplicate durable role instructions or deterministic installer behavior
- update affected workflow, role-routing, versioning, roadmap, index, and conceptual documentation
