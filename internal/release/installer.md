---
type: Internal Release Implementation
title: Ava Release Assembler and Installer
description: Documents the implemented deterministic release assembly, installation, upgrade, migration, host integration, and recovery tooling.
tags: [internal, releases, installer, updater, assembly, migrations]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T15:15:00+02:00
---

# Ava release tooling

Ava uses two maintainer-facing source tools and one distributed entry point:

- `assemble.sh` invokes `assemble.py` to build the exact seven-asset GitHub Release set.
- `assemble.py` classifies every distributed source file, creates reproducible archives, emits the release manifest, and writes `SHA256SUMS`.
- `ava-install.sh` and the ordered Python fragments under `installer/` are assembled into the distributed `ava-install.sh` asset with immutable release identity embedded near its beginning.

The installed entry point remains one POSIX shell file. It delegates strict JSON, archive, checksum, path, transaction, and migration handling to embedded Python rather than parsing structured release state in shell.

# Requirements

Release assembly requires:

- POSIX `sh`
- Python 3.11 or newer
- a clean repository source revision and its full 40-character Git SHA
- a stable `SOURCE_DATE_EPOCH`, normally the source commit timestamp

Installation requires:

- POSIX `sh`
- Python 3.11 or newer
- HTTPS access to GitHub Releases unless `--asset-dir` supplies a local release set
- `gh` only when `--verified` is used

The initial installer does not require `jq`, GNU `tar`, a package manager, an Ava runtime, or a persistent CLI.

# Assemble a release

```sh
sh internal/release/assemble.sh \
  --version 0.1.0 \
  --source-revision "$SOURCE_REVISION" \
  --source-date-epoch "$SOURCE_DATE_EPOCH" \
  --output dist/v0.1.0 \
  --release-notes internal/release/notes/v0.1.0.md
```

A direct supported upgrade edge is added with:

```sh
--upgrade-from 0.1.0
```

A chained edge is declared as source followed by mandatory intermediates:

```sh
--upgrade-from 0.1.0:0.2.0,0.3.0
```

Each adjacent intermediate release must still declare its own direct edge. The installer verifies the complete graph before mutation.

Optional assembly inputs are:

- `--guidance-dir DIR` to package relative guidance paths
- `--migrations-dir DIR` to package declarative deterministic migrations
- `--semantic-review-required` to mark project-owned reconciliation as required

Assembly maps:

- `templates/base/AGENTS.md` to `/AGENTS.md`
- the base index, roles, workflows, and shared instructions to `/.ava/base/`
- `templates/project-scaffolds/` to project-root create-if-absent paths

The `knowledge/` and `inbox/` examples under `templates/base/` are not inferred as managed merely because of their source location. Installed ownership is determined only by the generated release mapping.

Host-specific project files are not release sources. Ava does not package `CODEX.md`, `CLAUDE.md`, Copilot instructions, or similar host entrypoints.

# Install and upgrade

The standard convenience path remains:

```sh
curl -fsSL https://github.com/phdah/ava/releases/latest/download/ava-install.sh | sh
```

A target directory and explicit release may be selected:

```sh
sh ava-install.sh --target /path/to/project --version 1.2.3
```

Inspect the complete plan without applying it:

```sh
sh ava-install.sh --target /path/to/project --dry-run
```

Use normalized JSON Lines output for automation:

```sh
sh ava-install.sh --target /path/to/project --dry-run --json
```

A pre-existing root `AGENTS.md` blocks installation. After its project-specific meaning has been preserved or deliberately discarded, replacement requires the explicit option:

```sh
sh ava-install.sh --adopt-existing-agents
```

# Project-provided host entrypoint

A project may already contain a host-specific instruction file, for example:

```text
/CODEX.md
/.github/copilot-instructions.md
```

The project owner may record one such file during installation:

```sh
sh ava-install.sh --host-entrypoint CODEX.md
```

The installer:

- requires the path to resolve to an existing normal file inside the selected project root
- rejects `/AGENTS.md`, `/.ava/`, and paths below `/.ava/`
- records the normalized path as `project-owned` and `project-provided` host integration metadata
- preserves the metadata across upgrades unless another entrypoint is explicitly supplied
- never reads, rewrites, creates, deletes, checksums, backs up, or rolls back the project file
- never adds the file to the release inventory or `managed_files`

The project owner remains responsible for ensuring that the host file directs the host to load and follow `/AGENTS.md`. Ava records the integration point but does not interpret its prose.

Without recorded host integration, discovery is reported as `explicit-only`. No host is reported as natively supported by this implementation.

The installed manifest representation is either `null` or:

```json
{
  "entrypoint": "/CODEX.md",
  "ownership": "project-owned",
  "discovery": "project-provided"
}
```

# Verified bootstrap

The caller must verify a pinned installer before executing it:

```sh
version=v1.2.3
curl -fsSLO "https://github.com/phdah/ava/releases/download/${version}/ava-install.sh"
gh release verify "$version" --repo phdah/ava
gh release verify-asset "$version" ./ava-install.sh --repo phdah/ava
sh ./ava-install.sh --verified
```

`--verified` repeats immutable-release verification and verifies every downloaded asset through `gh`. This does not replace the required download-first verification of the installer itself.

`--asset-dir DIR` supports development, fixtures, and offline use of a complete local asset set. It verifies the release manifest and all checksums but does not independently authenticate the directory's publisher.

# Transaction and recovery model

Before managed mutation, the updater:

1. validates release identity, checksums, archive safety, source mapping, installed state, optional host entrypoint, and the complete upgrade graph
2. performs three-way reconciliation of prior, current, and target managed payloads
3. stages the complete managed target tree inside the selected target root
4. records a durable transaction plan and rollback backup
5. executes declared migrations only against staged managed content
6. validates the candidate tree

During apply, managed files are replaced with per-file atomic renames where supported. The candidate `manifest.json` is written last as the managed commit boundary. Any handled failure restores the source managed state and removes project scaffolds created by the failed fresh installation.

An interrupted transaction supports:

```sh
sh ava-install.sh --resume
sh ava-install.sh --abort
sh ava-install.sh --rollback
```

`--resume` accepts only source or target checksums recorded by the transaction. Any unrelated managed edit blocks continuation. `--abort` is available before live mutation and becomes rollback after mutation starts.

After deterministic work requiring semantic reconciliation, the journal remains `active/semantic`, normal routing stays blocked, and rollback material is retained. The managed Upgrade Role applies installed guidance and records project-owned changes. Once semantic compatibility is complete:

```sh
sh ava-install.sh --finalize
```

Automatic rollback never reverses project-owned edits, including a recorded host entrypoint. Recorded semantic project changes must first be explicitly reverted before managed rollback is permitted.

# Path and archive safety

The installer rejects:

- absolute archive paths
- `..` traversal
- backslash path ambiguity
- duplicate archive entries
- symlinks, hard links, devices, sockets, and non-regular archive payloads
- symlink components in installed destinations
- destinations resolving outside the canonical target root
- undeclared managed paths
- project scaffolds outside accepted project-owned extension roots
- file-directory prefix collisions in the release mapping
- host entrypoints that are missing, non-regular, outside the project root, or inside Ava-managed paths

Downloads, staging, backup, migration application, rollback, and cleanup use paths beneath the selected target root. A local asset directory is read-only input.

# Deterministic migrations

The initial migration protocol is declarative rather than arbitrary executable shell. Each migration descriptor names JSON apply and verify files from `ava-migrations.tar.gz`.

Apply operations are limited to:

- writing a declared managed path from an archive-relative source
- deleting a declared managed path

Verification checks existence and optional SHA-256 values. Migration dependencies are topologically sorted, cycles and missing dependencies are rejected, and the final staged payload must still match the target release manifest.

This restricted protocol prevents a migration from obtaining general filesystem execution authority and keeps every mutation inside the staged managed tree.

# Validation

Run the focused implementation suite with:

```sh
sh internal/release/test.sh
```

The suite covers clean installation, explicit adoption, project-owned preservation, managed conflicts, checksum failures, unsafe archives, symlink escapes, project-provided host entrypoints, direct and chained upgrades, declarative migrations, semantic blocking, rollback, and post-upgrade rollback conflicts.

Broader conformance matrices and compatibility fixtures remain Phase 4 task 8.
