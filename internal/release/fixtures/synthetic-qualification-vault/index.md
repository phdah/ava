# Synthetic Qualification Vault

This repository-only fixture generates the repeatable raw corpus used for Ava v1 qualification. Generated content and qualification evidence always remain outside the repository.

- [Reviewed blueprint](blueprint.md) - Narrative, inventory, safety, reproducibility, and command contract.
- [Canonical fact sheet](blueprint.json) - Sole machine-readable source for identities, dates, recurring facts, state transitions, class counts, formats, and image slots.
- [Generator and validator](fixture.py) - Standard-library generation, verification, image finalization, and variant materialization entry point.
- [Dependency lock](requirements.lock) - Runtime and dependency boundary for deterministic generation.
- [Oracle schema](oracle.schema.json) - Contract for the generated baseline oracle and per-source expected outcomes.
- [Run manifest schema](run-manifest.schema.json) - Contract for binding qualification scenarios to releases, environments, transcripts, inventories, and decisions.
