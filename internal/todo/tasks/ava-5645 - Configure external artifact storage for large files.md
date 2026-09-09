---
id: ava-5645
title: Configure external artifact storage for large files
status: To Do
assignee: []
created_date: '2026-09-09 21:08'
labels:
  - internal
  - roadmap
  - storage
  - configuration
  - provenance
  - distribution
milestone: m-1
dependencies: []
references: []
type: enhancement
ordinal: 6644
---

## Description

Add an optional project-level capability for Ava vaults to declare where and how large or binary source artifacts should be stored outside the Git repository while keeping durable provenance links inside the vault.

The motivating dogfood case is receipt images: the semantic knowledge belongs in Markdown in the vault, while the original JPEG receipts are better kept in an external file store such as Google Drive and referenced from the relevant `sources[].resource` metadata. The same mechanism should generalize to PDFs, images, exports, archives, and other artifacts that are useful as preserved evidence but undesirable to accumulate in Git history.

The feature should introduce a project-owned configuration contract for external artifact storage. The exact config path and schema are part of this task's design work, but it must remain optional and backward-compatible. A configured storage target should be able to describe the external place and the host capability or method used to put files there, without making Ava itself a persistent storage runtime.

Examples of possible destinations include Google Drive, S3-compatible object storage, another cloud file provider, or a project-defined filesystem location. The public contract must be provider-neutral. Google Drive should be covered as a concrete qualification/example because it is the current dogfood use case, but it must not become a required dependency or privileged provider.

The configuration must not contain credentials, tokens, or other secrets. Ava should describe the desired storage target and durable reference semantics while the host agent uses whatever connected tool, connector, CLI, or filesystem capability is actually available. When the configured method cannot be used in the current host, the agent must report that clearly rather than pretending the artifact was persisted.

The design must also define how this interacts with `inbox/`, `inbox/processed/`, and trusted knowledge provenance. Large source artifacts may begin as inbox material, be persisted externally when the configured policy applies, and then leave a durable resource reference in the canonical knowledge or processed source metadata. The original artifact must remain retrievable from the recorded external reference, and the vault must not silently lose provenance merely because the bytes no longer live in Git.

## Required behavior

1. Define an optional project-owned configuration contract for external artifact storage, including the destination/location and enough method/provider information for an agent to identify the required host capability.
2. Keep the storage contract provider-neutral while documenting and qualifying Google Drive as one supported dogfood scenario.
3. Do not store secrets, access tokens, credentials, or provider session material in the vault configuration.
4. Define when source artifacts may be externalized instead of retained as Git-tracked files, with emphasis on large and binary evidence such as images, PDFs, archives, and exports.
5. Preserve durable provenance after externalization, including a stable resource reference to the externally stored artifact and enough metadata to identify what was stored.
6. Define the lifecycle interaction with `inbox/`, `inbox/processed/`, and canonical knowledge so an externally stored source remains evidence rather than becoming detached from the knowledge derived from it.
7. Keep host responsibility explicit: Ava supplies configuration and behavior contracts; the active host/tool/connector performs the actual upload or file operation.
8. If the configured storage method is unavailable to the active host, stop or fall back only according to an explicitly defined safe behavior and report that the external persistence did not occur.
9. When no external artifact storage is configured, existing Ava behavior remains unchanged.
10. Installation and upgrades preserve project-owned storage configuration and existing external resource references without rewriting or deleting them.
11. Add public documentation, project scaffolding/config guidance, validation, fixtures, and qualification coverage needed to make this a supported Ava 1.1 capability.
12. Review SemVer impact and keep the implementation backward-compatible for the `1.1.0` milestone. If the required design would instead break Ava's stable public format contract and require `2.0.0`, stop and return the scope for milestone re-evaluation rather than implementing the breaking design under `m-1`.

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Ava defines an optional project-owned external-artifact-storage configuration contract without requiring a persistent Ava runtime
- [ ] #2 The configuration can identify an external destination and the method/provider capability required to store artifacts there
- [ ] #3 The contract is provider-neutral, with Google Drive covered as a concrete supported example/qualification scenario rather than a hard dependency
- [ ] #4 Credentials and secrets are explicitly excluded from the configuration and durable project context
- [ ] #5 Large or binary source artifacts can be externalized while the vault retains a stable provenance reference to the original artifact
- [ ] #6 Inbox and knowledge lifecycle guidance defines how externally stored artifacts remain preserved source evidence and how canonical documents reference them
- [ ] #7 The host agent must verify that the configured storage operation actually succeeded before recording the artifact as externally persisted
- [ ] #8 Absence of storage configuration preserves current behavior and does not force external storage on existing Ava projects
- [ ] #9 Installation and upgrades preserve project-owned storage configuration and external references
- [ ] #10 Validation and qualification cover configured and unconfigured projects, unavailable host capability, and at least the Google Drive dogfood flow
- [ ] #11 Public documentation clearly separates Ava's configuration/provenance responsibilities from the host tool or connector that performs storage operations
- [ ] #12 The completed design remains backward-compatible and suitable for the `v1.1.0` milestone, or implementation stops for explicit major-version re-evaluation
<!-- AC:END -->
