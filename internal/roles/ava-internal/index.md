# Ava Internal Maintainer Bootstrap

This file is the single bootstrap entry point for the Ava Internal Maintainer role.

To activate the role, the user only needs to tell the agent to use the Ava Internal Maintainer role defined at:

`/internal/roles/ava-internal/index.md`

The user does not need to name or provide any other role files. After reading this file, the agent is responsible for loading all required context listed below.

Use this role only when the user explicitly activates it for work on the Ava repository.

# Bootstrap procedure

When this role is activated, the agent must:

1. treat this file as the only initial role file supplied by the user
2. read every file under **Required reading** in the listed order
3. follow further indexes only when a required file or the current task directs it to do so
4. resolve the complete active instruction set before modifying the repository
5. ask the user about any material ambiguity or conflict
6. confirm that the Ava Internal Maintainer role is active after all required files have been read

# Required reading

Read these files before acting:

1. [Repository bundle index](/index.md) - OKF version, repository-level navigation, and scoped history.
2. [Repository README](/README.md) - Project purpose, architectural direction, boundaries, and current design questions.
3. [Role definition](role.md) - Purpose, authority, activation, and scope.
4. [Instructions](instructions.md) - Required working behaviour and repository maintenance rules.
5. [Capabilities](capabilities.md) - Actions the role is allowed to perform.
6. [Constraints](constraints.md) - Actions and decisions the role must avoid or escalate.

# Optional reading

Read these only when relevant:

- [Role update log](log.md) - Major conceptual changes to this role.
- [Internal update log](/internal/log.md) - Major conceptual changes across internal development instructions.
- [Repository update log](/log.md) - Major conceptual and structural changes across the repository.

Do not scan unrelated files unless the task requires them or another index directs you to them.
