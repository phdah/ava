---
type: Host Support Contract
title: OpenCode Host Support
description: Defines Ava discovery, managed-directory access, configuration ownership, permissions, installation, and validation for OpenCode.
tags: [ava, hosts, opencode, discovery, permissions, installation]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T20:30:00+02:00
---

# OpenCode host support

OpenCode is Ava's first explicitly supported host.

Ava keeps `./.ava/` as the canonical managed directory. OpenCode support uses its native project-root `AGENTS.md` discovery and normal workspace file tools. Ava does not require or generate an OpenCode project configuration.

## Supported contract

Start OpenCode from the installed project root:

```sh
cd /path/to/project
opencode
```

OpenCode natively loads the nearest project `AGENTS.md`. The Ava-managed root router then directs OpenCode to read required files through explicit project-root-relative paths such as `./.ava/base/shared/instructions/instruction-resolution.md`.

The managed directory is hidden by filesystem naming convention, but it remains inside the OpenCode workspace. Direct reads under `./.ava/` do not require `external_directory` permission.

Ava guarantees that:

- the canonical router is installed as `./AGENTS.md`
- every static managed path named by the router resolves below the project root
- required managed reads use explicit `./.ava/...` paths
- the installer preserves `opencode.json`, `opencode.jsonc`, and global OpenCode configuration byte-for-byte
- no OpenCode configuration is created, adopted, checksummed, recorded as managed, upgraded, or removed by Ava
- deterministic installer and updater writes remain governed by the Ava release transaction

OpenCode and the adopting project remain responsible for:

- applying the effective OpenCode permission configuration
- providing a model and provider configuration
- honoring project and global OpenCode configuration precedence
- deciding whether managed edits should be allowed, denied, or require approval at the host layer

Instruction text cannot grant filesystem permissions. Ava instructions describe required behavior, but OpenCode remains the authority that allows, asks for, or denies each tool action.

## Permission behavior

With OpenCode defaults, workspace reads are allowed. The default external-directory prompt is irrelevant to `./.ava/` because the directory is inside the project worktree.

A project or user can override those defaults. A restrictive `read`, `glob`, `grep`, or agent-specific permission rule may prevent Ava from loading required context. In that case, the project owner must adjust the existing OpenCode configuration deliberately. Ava does not silently relax it.

Host-level managed write protection is optional. Projects that want an additional guard may configure OpenCode to ask or deny edits to `AGENTS.md` and `.ava/**`. That policy is project-owned and must still permit an explicitly authorized installer or updater command when a managed release transaction is intended.

## Configuration ownership

The following files are never Ava-managed:

- project `opencode.json`
- project `opencode.jsonc`
- global OpenCode configuration
- project `.opencode/` content

Ava does not offer an installer-managed OpenCode integration mode. Native `AGENTS.md` discovery is sufficient, and mutating project configuration would create unnecessary ownership, merge, rollback, and compatibility costs.

An existing project-provided host entrypoint can still be recorded through the generic `--host-entrypoint` option for other hosts or custom setups. OpenCode does not need that option when root `AGENTS.md` discovery is available.

## Hidden-file discovery policy

Required Ava context must be loaded through explicit direct paths from the root router, role indexes, workflow definitions, or active instructions. Ava does not depend on an unscoped hidden-file scan to discover mandatory managed context.

Search and glob behavior may follow host ignore rules. That does not affect the required-reading contract because mandatory managed files are addressed directly. Searches under `./.ava/` should use an explicit path when managed content is the intended scope.

## Troubleshooting

When OpenCode does not load Ava correctly:

1. Confirm OpenCode was started from the installed project root or a descendant where the intended root `AGENTS.md` is the nearest project rule file.
2. Confirm `./AGENTS.md` and `./.ava/state/manifest.json` exist.
3. Run `opencode debug config` and inspect project, global, and agent-specific permission overrides.
4. Check whether `read`, `glob`, or `grep` rules deny the resolved managed paths.
5. Check whether an agent-specific permission rule overrides the project default.
6. Do not move managed content out of `./.ava/` or copy managed rules into `opencode.json` as a workaround.

## Validation

Ava maintains fixtures that prove:

- fresh installation creates no OpenCode configuration
- existing project and global OpenCode configuration survives installation and upgrade unchanged
- root-router managed paths resolve inside the installed project
- the managed directory remains hidden and project-local
- a host-neutral root-router resolver can follow the same project-relative paths
- the pinned supported OpenCode CLI starts from an installed fixture and resolves configuration without extra project setup

A model-backed end-to-end session remains provider-dependent. The deterministic support boundary is native router discovery, project-local managed reads, preserved configuration, and executable OpenCode startup against the installed fixture.
