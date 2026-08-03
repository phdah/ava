---
okf_version: "0.2"
---

# Ava Base Format Source

This directory contains the current authored Ava-managed release payload plus project-format references retained for design context.

It is not copied verbatim to an installed project. Release assembly maps the root router and managed base content into `./AGENTS.md` and `./.ava/base/`. Project-owned create-if-absent sources live separately under [`templates/project-scaffolds/`](../project-scaffolds/).

Follow the linked indexes progressively instead of scanning the complete source tree.

## Contents

- [Agent router source](AGENTS.md) - Source for the Ava-managed root router.
- [Inbox format reference](inbox/) - Project-owned inbox format reference, not an installed release source.
- [Knowledge format reference](knowledge/) - Project-owned knowledge format reference, not an installed release source.
- [Default roles](roles/) - Ava-managed role sources for the installed base catalog.
- [Default workflows](workflows/) - Ava-managed workflow sources for the installed base catalog.
- [Shared context](shared/) - Ava-managed shared instruction sources.

Release assembly classifies each source file explicitly. Repository location under `templates/base/` alone does not make a file Ava-managed, and reference content is excluded unless an explicit release mapping declares it.
