---
okf_version: "0.2"
---

# Ava Base Format Source

This directory contains the current authored release payload and project-scaffold source material for Ava-managed defaults and project-format examples.

It is not copied verbatim to an installed project. The accepted [distribution and ownership contract](../../distribution/ownership.md) maps managed base content into `/.ava/base/`, maps the canonical router to `/AGENTS.md`, and treats project extension paths as project-owned.

Follow the linked indexes progressively instead of scanning the complete source tree.

## Contents

- [Agent router source](AGENTS.md) - Source for the Ava-managed root router.
- [Managed base index source](base-index.md) - Source installed at `/.ava/base/index.md`.
- [Default roles](roles/) - Ava-managed role sources for the installed base catalog.
- [Default workflows](workflows/) - Ava-managed workflow sources for the installed base catalog.
- [Shared context](shared/) - Ava-managed shared instruction sources and current project-format context.
- [Project scaffold sources](scaffold/) - Minimal create-if-absent project-owned extension files.
- [Inbox format](inbox/) - Project-owned inbox scaffold and format reference.
- [Knowledge format](knowledge/) - Project-owned knowledge scaffold and format reference.

Release assembly must classify each installed source file explicitly. Repository location under `templates/base/` alone does not make a file Ava-managed.
