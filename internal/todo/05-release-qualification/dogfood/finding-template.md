# Dogfood Finding Template

Create one bounded task file for each finding that requires repository work. Replace every placeholder and remove sections that do not apply.

```markdown
---
type: Internal Development Task
title: <Imperative bounded outcome>
description: <One sentence describing the defect and intended result.>
tags: [internal, roadmap, dogfood, <area>]
status: pending
phase: 5
parent: 04-dogfood-alpha-and-track-findings
order: <next finding number>
classification: <blocker|required-v1|post-v1>
blocks: <next-prerelease|release-candidate|stable|none>
affected_version: <version or source revision>
generated:
  by: <actor>
  at: <timestamp>
---

# <Title>

## Observed behavior

Describe what happened from the user's perspective.

## Reproduction and evidence

Provide exact commands, inputs, versions, errors, logs, or release links needed to reproduce or verify the finding.

## Classification

Explain why the finding is a `blocker`, `required-v1`, or accepted `post-v1` decision and identify the release gate it blocks.

## Root cause

Record the known cause. Use `unknown` when investigation is part of the task rather than guessing.

## Scope

Define the bounded repository changes expected from the resolving PR.

## Completion criteria

- state the observable repository behavior that must work
- name the regression coverage that must be added
- require affected documentation and indexes to remain aligned
- require concrete resolution and repository-validation evidence

## Resolution evidence

Complete this section in the resolving implementation PR. Include the implementing PR, tests, and repository validation.

## Release qualification follow-up

When published-asset or realistic-project checks can only happen after merge, record them here as release-gate qualification. Append the resulting evidence later without keeping or returning the task to `pending`.
```

## Status and disposition rules

Use only `pending` and `completed` for task status. A completed task must include resolution evidence.

Mark a finding `completed` in the resolving implementation PR once its bounded repository change, tests, documentation, indexes, and resolution evidence are complete. Published-asset or realistic-project qualification that can only happen after merge is tracked separately and does not keep or return the implementation task to `pending`.

An accepted post-v1 finding is `completed` because the current decision is resolved, with `classification: post-v1`, `blocks: none`, and an explicit deferral rationale in its resolution evidence.

Do not mark the parent dogfood task completed from an individual finding PR.
