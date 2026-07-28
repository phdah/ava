---
type: Internal Development Task
title: Review Workflow Purpose and Built-in Catalog
description: Define when a reusable workflow is justified and align the built-in catalog with the boundary between free-form role work, workflows, and semantic tools.
tags: [internal, roadmap, workflows, catalog, routing]
status: pending
phase: 3
order: 4
timestamp: 2026-07-28T00:00:00Z
---

# Review Workflow Purpose and Built-in Catalog

## Why

The initial built-in catalog includes workflows that may duplicate ordinary free-form requests already handled by a role. Ava needs an explicit distinction between durable role behaviour, reusable procedures, and deterministic semantic tools before trigger portability and workflow lifecycle design are finalized.

A workflow should represent a repeatable, bounded procedure or outcome with useful procedural constraints. It should not exist only to give a command-like name to normal work already covered by a role or to wrap deterministic scaffolding and validation mechanics.

## Define

- the boundary between a free-form request handled directly by a role, an explicitly invoked registered workflow, and an Ava semantic tool
- the criteria that justify a reusable workflow, including repeatability, bounded scope, meaningful inputs, operating mode, required context, procedure, and expected output
- the warning signs that a proposed workflow merely restates a role responsibility or wraps deterministic create, update, scaffold, move, or validation mechanics
- how workflows provide value for audits, reviews, batch processing, recurring maintenance, migration preparation, and other standardized multi-step outcomes
- how explicitly invoked workflows remain optional procedural scopes rather than the only way to request work from a role

## Audit the built-in catalog

Evaluate every registered built-in workflow and classify it as:

- retain unchanged
- revise to express a stronger reusable procedure or outcome
- deprecate or remove because free-form role routing is sufficient
- replace with a semantic tool, role instruction, or more useful workflow

The audit must specifically reassess command-like workflows such as `create-role`, `update-role`, `repair-role`, `configure-project`, and `tighten-instructions`. It must also evaluate whether the catalog needs outcome-oriented workflows such as reviewing the complete role catalog for ambiguity, overlap, inconsistent authority, unclear exclusions, or required-reading misalignment.

Do not assume that any named workflow must be retained or removed before completing the audit.

## Dependencies and follow-up

Complete this task before defining workflow trigger portability. Trigger and scheduler metadata should be designed around workflows that meet the accepted purpose criteria.

Use the result as input to workflow lifecycle ownership and the semantic role and workflow maintenance tool catalog. Lifecycle ownership determines who maintains justified workflows, while semantic tools provide deterministic mechanics beneath roles and workflows.

## Completion criteria

- document a clear and portable purpose boundary between roles, workflows, and semantic tools
- define concrete criteria for adding a workflow to the built-in catalog
- audit every current built-in workflow against those criteria
- update, deprecate, replace, or remove workflows and registry entries according to the audit
- decide whether one or more role-catalog audit workflows should be added
- ensure retained workflows provide procedural value beyond ordinary free-form role routing
- ensure workflow bodies do not duplicate durable role instructions or deterministic tool behavior
- update affected workflow, role-routing, roadmap, index, and conceptual documentation
