# Ava Release Guidance Sources

This directory contains reviewed semantic upgrade guidance.

Each release-local edge record selects its own guidance by exact path and SHA-256 digest. Recursive upgrade composition collects guidance only from the edge records between the semantic source and target. Release assembly stages only those referenced files.

## Canonical adjacent guidance

- `1.0.0-alpha.10/1.0.0-alpha.9-to-1.0.0-alpha.10/UPGRADE.md` is the canonical obligation introduced by the alpha.9 to alpha.10 transition and is owned by `catalogs/1.0.0-alpha.10.json`.

## Archival cumulative guidance

The remaining target-scoped files under `1.0.0-alpha.10/`, `1.0.0-alpha.11/`, and `1.0.0-alpha.12/` preserve repository evidence for immutable published releases. They are read-only compatibility material and are not selected for new releases unless a release-local edge record references their exact path and digest.

Do not create new cumulative source-to-target guidance directories.
