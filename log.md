# Repository Update Log

This log records major conceptual and structural changes across the Ava repository. It does not replace Git history.

## 2026-07-26

* **OKF v0.2 metadata contract**: Adopted OKF version 0.2 for the repository and initialized projects. Defined open document types, required Ava semantic metadata, prose-based role routing, single-primary-role workflow metadata, OKF provenance and verification, lifecycle and replacement rules, forward-compatible unknown fields, validation severity, and Obsidian-compatible authoring conventions.
* **Initialized project structure**: Finalized the minimal `ava init` tree with stable top-level locations for the agent router, inbox, knowledge, roles, workflows, and shared context. The structure remains extensible beneath those locations, creates logs only when needed, and requires migration support only when stable initialized paths are changed or repurposed.
* **Index hierarchy**: Defined `index.md` files as direct-child navigation only. Child directories own discovery of their descendants, preventing ancestor indexes from flattening or duplicating deeper navigation.
* **Template navigation**: Added `templates/base/index.md` and reduced `templates/index.md` to reference only its direct `base/` child.
* **Role activation visibility**: Required the generated agent router to announce the selected role after its complete required instruction set has been loaded and before acting under that role.
* **Delegation visibility**: Required the Ava Internal Maintainer to announce both its active primary role and each delegated specialist before specialist instructions affect the work.

## 2026-07-25

* **Git operation delegation**: Removed role-level Git and GitHub workflow rules and commit-specific workspace-provider semantics. Active repository tooling and providers now determine those operations.

## 2026-07-24

* **Role and workflow model**: Defined workflows as reusable predefined prompts that activate one primary role, while roles retain durable instructions, authority, and context.
* **Core role direction**: Consolidated the proposed initialized-project catalog around Role Manager, Project Steward, Inbox Ingester, and Change Reviewer responsibilities.
* **Project Steward**: Added the initialized-project role for maintaining trusted project-wide guidance, workflows, and knowledge with scoped audits, safe consolidation, and explicit routing boundaries.
* **Inbox ingestion**: Added the initialized-project inbox lifecycle and Inbox Ingester role with untrusted-input handling, provenance preservation, conflict escalation, and post-ingestion source retention.
* **Workspace abstraction**: Introduced a provider contract so Ava semantic operations can work with GitHub, local filesystems, or future backends without coupling the format to storage.
* **GitHub integration**: Defined client-coordinated GitHub MCP, Ava-managed GitHub provider, and host-supported delegation as distinct integration modes.
* **Roadmap**: Expanded the implementation roadmap to cover workflows, providers, semantic tools, change planning, validation, application services, MCP, CLI, testing, compatibility, and migration work.

## 2026-07-23

* **Conformance**: Established the repository root as an Open Knowledge Format version 0.1 bundle.
* **Metadata**: Added OKF concept metadata to the project overview.
* **Navigation**: Added a root index for progressive discovery of repository knowledge.
* **Initialization templates**: Added `templates/base/` as the source tree for files copied into new Ava projects.
* **Agent routing**: Defined root `AGENTS.md` as the automatically loaded router that selects and loads the best matching role for each request.
