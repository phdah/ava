---
okf_version: "0.2"
---

# Ava Base Format Source

This directory contains the current authored release payload and project-scaffold source material for Ava-managed defaults and project-format examples.

It is not copied verbatim to an installed project. The accepted [distribution and ownership contract](../../distribution/ownership.md) maps managed base content into `/.ava/base/`, maps the canonical router to `/AGENTS.md`, and treats project extension paths as project-owned.

Follow the linked indexes progressively instead of scanning the complete source tree.

## Contents

- [Agent router source](AGENTS.md) - Source for the Ava-managed root router.
- [Inbox format](inbox/) - Current project-owned inbox structure used as scaffold and format reference.
- [Knowledge format](knowledge/) - Current project-owned knowledge structure used as scaffold and format reference.
- [Default roles](roles/) - Ava-managed role sources for the installed base catalog.
- [Default workflows](workflows/) - Ava-managed workflow sources for the installed base catalog.
- [Shared context](shared/) - Ava-managed shared instruction sources and current project-format context.

Release assembly must classify each source file explicitly. Repository location under `templates/base/` alone does not make a file Ava-managed.
