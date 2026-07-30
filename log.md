# Repository Update Log

This log records major conceptual and structural changes across the Ava repository. It does not replace Git history.

## 2026-07-30

* **Versioned context distribution pivot**: Reframed Ava as a versioned, file-based context distribution rather than an MCP server, workspace-provider application, or feature-rich CLI. The files remain the public product and the host agent supplies navigation, editing, and repository operations.
* **GitHub Release distribution**: Established immutable GitHub Release assets as the installation and upgrade channel, with latest-stable and version-pinned URLs, a thin shell installer, versioned base bundle, integrity checksums, release manifest, change notes, agent upgrade guidance, deterministic migrations, and an explicit signing or attestation decision.
* **Ownership model**: Limited the design to two ownership classes. Ava-managed content includes the root `AGENTS.md` and all bootstrap files. Project customization remains project-owned and outside managed paths.
* **Version-state separation**: Defined `ava_version` solely as the installed Ava-managed base version and required semantic compatibility of project-owned context to be tracked separately.
* **Migration guidance and logs**: Retained scoped `log.md` files as conceptual history and release-note source material, while requiring release-specific structured guidance to state compatibility impact, affected project context, deterministic migrations, required decisions, and completion criteria.
* **Roadmap replacement**: Superseded the provider, semantic MCP tool, shared application service, MCP implementation, companion CLI, and application-specific compatibility phases with an active distribution and upgrade roadmap.
* **Host capability terminology**: Replaced public instruction dependence on a workspace-provider abstraction with the active role, user-approved scope, and capabilities exposed by the host agent and its available tools.

## 2026-07-28

* **Initial built-in workflow catalog**: Added ten registered workflows for role lifecycle, project stewardship, inbox ingestion, and semantic review. Mutation remains bounded by each primary role, recurring daily maintenance is suggestion-only, semantic reviews are read-only, and scheduling remains outside Ava's runtime.
* **Workflow registry and routing contract**: Defined `/workflows/index.md` as the canonical registry root, made workflow invocation explicit by canonical path or unambiguous filename stem, gave explicit workflows precedence over free-form role selection, prohibited semantic workflow inference and fallback after routing failure, required one registered non-deprecated primary role, and made deprecation replacements advisory rather than automatic.
* **Workflow format contract**: Defined workflows as path-identified Markdown prompts with one `primary_role`, a required `read-only`, `suggestion`, or `mutation` mode, structured inputs, optional required-context links, ordered procedure and expected-output sections, explicit composition boundaries, and validation rules. Trigger metadata remains deferred to the dedicated portability task.

## 2026-07-26

* **Instruction resolution and composition**: Defined instruction scope through explicit activation rather than directory depth. Established one active primary role, prohibited initial role inheritance, composition, supporting-role activation, and delegation, allowed narrower ordinary instructions to refine broader behaviour only within their active scope, and made capabilities and constraints cumulative and non-expandable at narrower scopes.
* **Scoped history contract**: Defined when project, role, workflow, and knowledge changes require the nearest relevant `log.md`, while keeping routine wording, metadata, index synchronization, implementation details, and ordinary content edits in Git history only.
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