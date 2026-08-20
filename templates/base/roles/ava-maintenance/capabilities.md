---
type: Role Capabilities
title: Ava Maintenance Capabilities
description: Permitted inspection, recovery coordination, terminal finalization, upgrade invocation, host reporting, and bounded Ava removal actions.
tags: [ava, role, maintenance, capabilities]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T21:47:00+02:00
updated:
  by: agent:openai-opencode
  at: 2026-08-20T15:36:31Z
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
- invoke existing resume, abort, or rollback operations when the protocol and user authorization permit them
- directly perform the protocol-defined terminal journal write, recursively remove the exact transaction directory derived from the validated journal, and remove its transaction container only through a non-recursive empty-directory operation when semantic compatibility is complete and every finalization precondition is proven
- replay only bounded terminal cleanup when a valid `complete`, `aborted`, or `rolled-back` journal identifies the exact transaction, or when any safe terminal journal and one residual transaction plan, source manifest backup, source journal backup, and live managed checksums prove an exact restored-source cleanup path
- remove an empty transaction container through the same non-recursive operation when no transaction directory remains
- provide the exact required user command when the host cannot invoke an installer-backed operation
- diagnose why deterministic recovery or finalization is blocked and identify the required decision or prerequisite

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
