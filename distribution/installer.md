---
type: Distribution Implementation
title: Ava Installer and Updater
description: Documents the implemented release assembler and thin manifest-driven installation and upgrade entry point.
tags: [ava, distribution, installer, updater, release, shell]
generated:
  by: agent:openai-chatgpt
  at: 2026-08-03T16:30:00+02:00
---

# Ava Installer and Updater

Ava releases are assembled with `internal/release/build-assets.sh`. The generated `ava-install.sh` is the single POSIX shell entry point for fresh installation and versioned upgrades.

The shell bootstrap performs argument parsing, release selection checks, asset download, optional GitHub immutable-release verification, and SHA-256 verification. It then executes the installer engine embedded in the already verified `ava-base.tar.gz` asset.

# Requirements

Installation requires:

- a POSIX shell
- Python 3.10 or later
- `curl` when assets are downloaded
- `sha256sum` or `shasum`
- GitHub CLI only for `--verified`

Release assembly additionally requires Git and a clean source revision identity.

# Release assembly

```sh
internal/release/build-assets.sh \
  --version 1.2.3 \
  --source-revision "$(git rev-parse HEAD)" \
  --source-date-epoch "$(git show -s --format=%ct HEAD)" \
  --published-at 2026-08-03T14:00:00Z \
  --output dist
```

Repeat `--upgrade-from VERSION` for each supported direct source version. Use `--semantic-review-required` when the target release requires project-owned context reconciliation.

Assembly generates the seven assets required by the [release contract](releases.md). Every installed file is mapped explicitly in `ava-release.json`; source location alone never determines ownership.

# Installer usage

```sh
sh ava-install.sh --target /path/to/project --dry-run --assets-dir ./dist
sh ava-install.sh --target /path/to/project --assets-dir ./dist
```

The immutable installer URL selects the version. `--version` only asserts that the downloaded installer matches the requested version.

Use `--adopt-agents` only after preserving or explicitly discarding the project-specific meaning of an existing `/AGENTS.md`. Use `--bootstrap PATH` to select one bootstrap destination declared by the release manifest.

# Safety model

The installer:

- validates checksums, release identity, archive identity, archive entry types, and every mapped payload checksum
- rejects absolute paths, parent traversal, duplicate archive entries, links, devices, FIFOs, and target-root symlink escapes
- preserves existing project-owned paths and applies scaffolds only when absent
- verifies every installed managed payload before an upgrade
- rejects undeclared upgrade transitions and requires declared intermediate releases in order
- stages changes under the target root, records `upgrade.json`, backs up replaced managed files, and rolls back live changes on failure
- commits `manifest.json` only after managed files and migrations validate
- leaves semantic compatibility pending and blocks normal routing when release guidance requires project-owned reconciliation

Dry-run validates release assets and prints every planned operation without mutating the target project.

# Validation

Run:

```sh
internal/release/validate-boundaries.sh
internal/release/test-installer.sh
```

The smoke suite covers dry-run, clean installation, direct upgrade, project-owned scaffold preservation, modified managed-file refusal, explicit router adoption, unrecognized `/.ava/` refusal, and unsafe destination rejection.
