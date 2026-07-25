---
type: Internal Development Task
title: Implement the Initial Workspace Provider
description: Implement the first provider only after the workspace contract is stable.
tags: [internal, roadmap, workspace, implementation]
status: pending
phase: 4
order: 3
timestamp: 2026-07-25T00:00:00Z
---

# Implement the Initial Workspace Provider

Choose one after the provider contract is stable:

- local filesystem provider for simple development and testing
- GitHub API provider for repository-native use
- client-coordinated change-plan mode if direct providers are deferred

The first implementation must not leak provider-specific assumptions into role or workflow documents.
