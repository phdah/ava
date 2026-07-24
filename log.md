# Repository Update Log

This log records major conceptual and structural changes across the Ava repository. It does not replace Git history.

## 2026-07-24

* **Role and workflow model**: Defined workflows as reusable predefined prompts that activate one primary role, while roles retain durable instructions, authority, and context.
* **Core role direction**: Consolidated the proposed initialized-project catalog around Role Manager, Project Steward, Inbox Ingester, and Change Reviewer responsibilities.
* **Project Steward**: Added the initialized-project role for maintaining trusted project-wide guidance, workflows, and knowledge with scoped audits, safe consolidation, and explicit routing boundaries.
* **Workspace abstraction**: Introduced a provider contract so Ava semantic operations can work with GitHub, local filesystems, or future backends without coupling the format to storage.
* **GitHub integration**: Defined client-coordinated GitHub MCP, Ava-managed GitHub provider, and host-supported delegation as distinct integration modes.
* **Roadmap**: Expanded the implementation roadmap to cover workflows, providers, semantic tools, change planning, validation, application services, MCP, CLI, and migrations.

## 2026-07-23

* **Conformance**: Established the repository root as an Open Knowledge Format version 0.1 bundle.
* **Metadata**: Added OKF concept metadata to the project overview.
* **Navigation**: Added a root index for progressive discovery of repository knowledge.
* **Initialization templates**: Added `templates/base/` as the source tree for files copied into new Ava projects.
* **Agent routing**: Defined root `AGENTS.md` as the automatically loaded router that selects and loads the best matching role for each request.
