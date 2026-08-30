---
okf_version: "0.2"
---

# Project Context

This project may extend the Ava-managed base through the project-owned locations below.

- [Roles](roles/) - Project-specific role definitions.
- [Workflows](workflows/) - Project-specific reusable procedures.
- [Shared](shared/) - Project-wide instructions and context.
- [Knowledge](knowledge/) - Trusted project knowledge.
- [Inbox](inbox/) - Untrusted or unclassified source material awaiting ingestion.
- `backlog.config.yml` and `backlog/` - Project-owned Backlog.md configuration and native task board.

The Backlog.md scaffold is ready for local `backlog task`, `backlog board`, and `backlog browser` use. Agents performing task management should load the current workflow with `backlog instructions overview` rather than relying on a copied CLI manual. Valid native Markdown under the configured backlog directory remains project-owned and Git-reviewable.

Ava upgrades never replace content under these paths. Newly introduced project-owned scaffolds are create-if-absent installation defaults, not managed upgrade payloads.
