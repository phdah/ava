# Repository Update Log

This log records major conceptual and structural changes across the Ava repository. It does not replace Git history.

## 2026-08-10

* **Conversation-aware routing**: Split the unconditional per-request managed-state gate from full workflow and role resolution. Normal-operation turns are now classified as roleless conversational follow-ups, same-role continuations, or fresh routing.
* **Roleless clarification boundary**: Pure clarification or refinement of the immediately preceding result may run without an active role only when no project action, workflow procedure, role capability, constraint, authority, or new decision boundary is required. A roleless turn clears active-role continuity.
* **Same-role continuation**: Same-objective scoped follow-ups may retain the already-active role and its already-loaded unchanged required reading, with `Active role remains: <role title>` announced before role-scoped handling.
* **Fresh-routing triggers**: New tasks, explicit workflow or role activation, changed domain or authority, role mismatch, unavailable role context, scoped work after a roleless turn, and managed-state overrides force fresh routing.
* **No persistent role state**: Role continuity is conversation-scoped only and does not introduce a runtime service, manifest field, project metadata, or other durable Ava state.
* **No-bypass preservation**: The finding 07 generic-host safeguard remains intact because every request still enters Ava's managed-state gate and continuity decision before substantive handling, including apparently out-of-domain requests.
* **Routing compatibility coverage**: Added maintained source and assembled-installation fixtures for roleless clarification, same-role continuation, role transitions, scoped work after roleless handling, unresolved routing, and the original warranty bypass.

## 2026-08-07

* **Substantive ingestion inventory**: Required every substantive source section to receive an explicit `mapped`, `non-durable`, or `pending` disposition before an inbox source can be marked processed.
* **Epistemic fidelity**: Required destination wording to preserve uncertainty, causality, authorship, chronology, and the distinction between source claims, trusted context, and user-approved decisions.
* **Renderable claim provenance**: Defined standard Markdown footnotes whose labels match OKF `sources` identifiers, resolve to the same preserved source, name the supporting passage, and reflect the claim's actual certainty.
* **Final-state reconciliation**: Required ingestion reports to recompute pending, processed, destination, concept, and section counts from final paths and indexes while excluding reserved inbox entries.
* **Semantic review boundary**: Required Change Reviewer to compare completed ingestion with every selected source and kept semantic meaning review separate from deterministic metadata, path, link, and count validation.
* **Ingestion fidelity regression coverage**: Added realistic fixtures and executable tests for multi-topic omissions, uncertain causality, cross-source attribution, unresolved footnotes, wrong-source citations, empty sources, and final count reconciliation.

## 2026-08-06

* **Durable subject identity**: Required canonical knowledge to follow the stable project, integration, system, person, agreement, decision, process, or event it describes rather than the shape of a meeting note, daily note, message, report, or export.
* **Concept and collection boundary**: Distinguished one independently maintainable canonical subject from a collection that provides a reusable semantic routing choice among multiple current concepts.
* **Semantic hierarchy promotion**: Required mature index subgroups to become child collections before further flat growth when their headings already encode durable routing decisions.
* **Project-owned taxonomy**: Kept exact scopes, domains, collection names, identity choices, and ambiguous ownership decisions project-owned, with no numeric split threshold or speculative empty taxonomy.
* **Knowledge reorganization ownership**: Required Inbox Ingester to block further flat growth and leave the source pending when promotion is needed, assigned trusted-branch restructuring to the Project Steward, and added independent hierarchy criteria to Change Reviewer.
* **Promotion regression coverage**: Added semantic fixtures for mixed initiatives, integrations, meeting-shaped input, temporary headings, cross-links, and ambiguous handoff, enforced through the release test suite.

## 2026-08-03

* **Document update provenance**: Added canonical `updated.by` and `updated.at` metadata for the latest meaningful mutation while preserving `generated` as immutable creation provenance.
* **Meaningful mutation threshold**: Defined semantic, authority, trust, identity, lifecycle, discovery, and behaviour changes as meaningful while excluding provably meaning-preserving formatting and mechanical edits.
* **Provenance actor format**: Standardized human, agent, and deterministic-tool provenance identifiers under a shared `<kind>:<stable-identifier>` format.
* **Update history boundary**: Kept only the latest meaningful update in frontmatter, retained Git as the complete audit trail, and preserved scoped logs for major conceptual or structural history only.
* **Legacy and reserved documents**: Required forward-compatible preservation of legacy and unknown update fields, adopted canonical metadata on the next meaningful mutation, and kept reserved indexes, logs, and the root README free from provenance-only frontmatter.
* **Update metadata validation**: Reserved stable `AVA-META-*` diagnostics and added machine-readable fixtures for creation, meaningful and trivial mutation, repetition, legacy metadata, malformed state, timestamp regression, stale verification, and reserved documents.
* **Workflow lifecycle ownership**: Assigned project-owned workflow creation, update, repair, reorganization, rename, deprecation, replacement, removal, and migration to the Project Steward.
* **No Workflow Manager**: Kept workflow lifecycle within the Project Steward's existing project-wide authority and trust boundary rather than adding an overlapping default role.
* **Workflow lifecycle procedure**: Added a progressively loaded shared contract for required inspection, approval-sensitive changes, references, deprecation, removal, migration, and validation.
* **Lifecycle responsibility separation**: Kept role lifecycle with the Role Manager, independent review with the Change Reviewer, active semantic upgrade work with the Upgrade Role, and managed replacement and structural validation with deterministic tooling.
* **Workflow catalog boundary**: Added no workflow-maintenance or semantic-upgrade workflow because both would duplicate durable role or managed pre-routing behavior.
* **Workflow phase completion**: Completed all six workflow-system tasks and resumed Phase 4 with installer and updater implementation next.
* **Distribution responsibility boundary**: Moved public distribution contracts and schemas into `/distribution/`, kept release payload and scaffold sources under `/templates/`, and added maintainer-only publication procedures under `/internal/release/`.
* **Explicit release inclusion**: Clarified that public contracts are not automatically installed and that release manifests must explicitly select every distributed source and destination.
* **Boundary validation**: Added a POSIX repository check that rejects stale contract locations, unexpected template roots, invalid schema identifiers, and references from public release sources into internal maintainer content.
* **Workflow purpose boundary**: Defined workflows as optional explicit procedural scopes that require repeatable bounded value beyond ordinary free-form role work.
* **Reduced built-in workflow catalog**: Reduced the managed catalog from ten workflows to four: batch inbox ingestion, bounded change review, complete role-catalog review, and bounded project-context audit.
* **Free-form role work**: Removed command-like role lifecycle and routine stewardship workflows while retaining their behavior through direct Role Manager and Project Steward routing.
* **Managed workflow routing**: Aligned workflow and primary-role resolution with managed `/.ava/base/` registries and project-owned extension registries, excluding the managed Upgrade Role from workflow routing.
* **Workflow compatibility**: Defined managed workflow replacement, project-owned semantic migration, and pre-`1.0.0` direct-removal boundaries.

## 2026-07-31

* **Release guidance contract**: Defined canonical installed `UPGRADE.md` guidance with validated source-to-target metadata, explicit changed contracts, affected project-owned concepts, required decisions, semantic procedures, completion criteria, rollback implications, and ordered multi-version composition.
* **Managed Upgrade Role**: Added a dedicated Ava-managed role with direct pre-routing activation, bounded cross-scope authority for project-owned semantic migration, exclusive semantic-state update authority, and strict separation from deterministic installer and updater work.
* **Upgrade routing boundary**: Made semantic version reconciliation a direct managed role activation rather than a workflow, kept project-owned registries unreachable until upgrade authority is active, and required normal routing to remain blocked until a safe terminal state.
* **Workflow phase resumed**: Marked the workflow system active again now that ownership, versioning, transaction, guidance, and Upgrade Role boundaries are explicit. The built-in workflow purpose audit is the next task.
* **Upgrade transaction protocol**: Defined explicit direct and chained release edges, durable `upgrade.json` journaling, stage-specific permitted operations, manifest-last managed commit semantics, interruption recovery, abort, and rollback.
* **Managed reconciliation and migrations**: Defined three-way managed-file comparison and structured deterministic migration descriptors with stable IDs, dependencies, checksums, apply and verification entry points, idempotency, and durable completion records.
* **Managed upgrade routing**: Required the root router to check managed upgrade and semantic state before ordinary routing, activate the managed Upgrade Role without project-owned registries, and block normal operations until a safe terminal state.
* **Rollback boundary**: Required managed rollback to restore the recorded source release while never automatically reversing project-owned semantic edits. Rollback after project edits remains blocked until explicit reconciliation and source compatibility validation.
* **Immutable release contract**: Defined one version-consistent GitHub Release asset set, exact stable and prerelease selection behavior, reproducible archive rules, source-to-installed mapping, and indefinite retention for published distributions.
* **Bootstrap trust modes**: Separated convenience execution, which trusts GitHub delivery before installer execution, from pinned verified execution, which validates the immutable release attestation and installer asset first.
* **Release authenticity**: Selected GitHub immutable release attestations as Ava's initial authenticity mechanism and kept SHA-256 checksums scoped to byte integrity rather than publisher authentication.
* **Publication verification**: Required repository release immutability before publication, draft-first asset assembly, post-publication immutable-state and attestation verification, and new-version correction instead of mutation.
* **Versioning and compatibility contract**: Defined `ava_version` strictly as installed managed-base state, kept `okf_version` separate, and established explicit semantic compatibility fields and `complete`, `pending`, `partial`, and `blocked` migration states.
* **Manifest integrity model**: Defined immutable managed payload entries with SHA-256 checksums and mutable managed state entries validated through schema and authorized transitions. The manifest and upgrade state are recorded without impossible self-checksums.
* **Behavior-sensitive SemVer**: Required PATCH to preserve supported behavior, MINOR to prove unchanged routing, resolution, authority, validation, and intended behavior or remain explicitly unreachable without opt-in, and MAJOR for behavior-changing additions even when old files remain readable.
* **Compatibility lifecycle**: Defined prerelease representation, direct and chained upgrade eligibility, versioned deprecation fields, host-conformance limits, release reporting requirements, and stable support windows.
* **Installed ownership instruction**: Split repository release and installation rules from agent-facing ownership behavior. The managed root router now loads a shared instruction that distinguishes release ownership from role mutation authority while preserving the repository contract for assembly, adoption, and upgrade mechanics.
* **Installed ownership boundary**: Established `/AGENTS.md` as the canonical managed router, `/.ava/base/` as the managed default context, `/.ava/state/` as the manifest and upgrade-state location, and `/.ava/guidance/` as the managed release-guidance location.
* **Project-owned extension paths**: Established `/roles/`, `/workflows/`, `/shared/`, `/knowledge/`, `/inbox/`, and root project indexes or logs as project-owned when present, including content that predates Ava installation.
* **Managed customization policy**: Prohibited direct customization of managed files. Local modifications remain managed-file conflicts and must be restored, discarded, or migrated into project-owned paths explicitly.
* **Repository source mapping**: Clarified that the Ava repository does not mirror an installed project. `templates/base/` is authored source material and release assembly must map every file to an explicit installed destination and ownership class.
* **Adoption contract**: Defined safe fresh installation, create-if-absent project scaffolding, explicit existing-project adoption, collision aborts, and migration of unversioned Ava projects without silent ownership transfer.
* **Bootstrap discovery**: Defined native root-router discovery, optional thin managed host bootstraps, explicit activation, and unsupported-host reporting while retaining `/AGENTS.md` as the only canonical router.

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
* **Role activation visibility**: Required the generated agent router to announce the selected role after its complete required instruction set has been loaded and before acting under it.
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
