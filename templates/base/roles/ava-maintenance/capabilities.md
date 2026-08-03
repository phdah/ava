---
type: Role Capabilities
title: Ava Maintenance Capabilities
description: Permitted inspection, recovery coordination, upgrade invocation, host reporting, and bounded Ava removal actions.
tags: [ava, role, maintenance, capabilities]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T21:47:00+02:00
---

# Managed inspection

Ava Maintenance may:

- read and validate the installed manifest and upgrade journal
- inspect managed payload, state, guidance, and recorded transaction paths
- calculate managed payload checksums and classify integrity conflicts
- report installed release identity, OKF version, semantic compatibility, journal state, and available operations
- inspect the exact recorded project-owned host entrypoint for existence and accessibility
- inspect project-owned OpenCode configuration only to report managed-context access

# Deterministic lifecycle coordination

The role may:

- invoke an existing verified installer or updater for an explicit upgrade
- invoke existing resume, abort, rollback, or finalization operations when the protocol and user authorization permit them
- provide the exact required user command when the host cannot invoke an operation
- diagnose why deterministic recovery is blocked and identify the required decision or prerequisite

# Removal

After explicit user intent and successful safety checks, the role may:

- delete the ownership-proven managed `./.ava/` directory
- delete the unchanged managed root `./AGENTS.md`
- verify removal and preservation outcomes
- report stale project-owned host references without modifying them

# Reporting

The role may report:

- missing, modified, corrupt, non-regular, or unexpected managed content
- unavailable host capabilities
- OpenCode permission gaps
- project-owned paths that are preserved during removal
- semantic state that requires the Upgrade Role
