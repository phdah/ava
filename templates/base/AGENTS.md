---
type: Agent Router
title: Ava Agent Router
description: Root instructions for selecting and loading the Ava role that best matches a user request.
tags: [ava, agent-router, roles]
---

# Ava

This project uses Ava roles to provide task-specific instructions to agents.

Before acting on a user request:

1. Read [`roles/index.md`](roles/index.md) to discover the available roles.
2. Select the role whose purpose and activation conditions best match the request.
3. Read the selected role's `index.md` and every document it marks as required.
4. Follow the selected role's instructions, capabilities, and constraints.
5. Load additional context only when the selected role or task requires it.

Select roles automatically. Ask the user only when no role clearly matches or when multiple roles would materially change the result.

Do not infer permissions or instructions from missing documentation.
