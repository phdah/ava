# Ava Release Guidance Sources

This directory contains reviewed semantic upgrade guidance.

Each release-local edge record selects its own guidance by exact path and SHA-256 digest. Recursive upgrade composition collects guidance only from the edge records between the semantic source and target. Release assembly stages only those referenced files.

## Canonical adjacent guidance

- `1.0.0-alpha.10/1.0.0-alpha.9-to-1.0.0-alpha.10/UPGRADE.md` is the canonical obligation introduced by the alpha.9 to alpha.10 transition and is owned by `catalogs/1.0.0-alpha.10.json`.
- `1.0.0-alpha.14/1.0.0-alpha.13-to-1.0.0-alpha.14/UPGRADE.md` is the canonical routing-compatibility obligation introduced by the alpha.13 to alpha.14 transition and is owned by `catalogs/1.0.0-alpha.14.json`.
- `1.0.0-alpha.15/1.0.0-alpha.14-to-1.0.0-alpha.15/UPGRADE.md` is the canonical ingestion-fidelity, calendar-verification, and upgrade-lifecycle obligation introduced by the alpha.14 to alpha.15 transition and is owned by `catalogs/1.0.0-alpha.15.json`.
- `1.0.0-alpha.16/1.0.0-alpha.15-to-1.0.0-alpha.16/UPGRADE.md` is the canonical interaction-evidence, task-routing, and claim-provenance obligation introduced by the alpha.15 to alpha.16 transition and is owned by `catalogs/1.0.0-alpha.16.json`.

## Archival cumulative guidance

The remaining target-scoped files under `1.0.0-alpha.10/`, `1.0.0-alpha.11/`, and `1.0.0-alpha.12/` preserve repository evidence for immutable published releases. They are read-only compatibility material and are not selected for new releases unless a release-local edge record references their exact path and digest.

Do not create new cumulative source-to-target guidance directories.
