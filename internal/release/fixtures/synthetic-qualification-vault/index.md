# Synthetic Qualification Vault

This repository-only fixture generates the repeatable raw corpus used for Ava v1 qualification. Generated content and qualification evidence always remain outside the repository.

- [Reviewed blueprint](blueprint.md) - Narrative, inventory, safety, reproducibility, and command contract.
- [Canonical fact sheet](blueprint.json) - Sole machine-readable source for identities, dates, recurring facts, state transitions, class counts, formats, and image slots.
- [Generator and validator](fixture.py) - Standard-library generation, verification, image finalization, and variant materialization entry point.
- [Qualification scenario matrix](qualification-matrix.json) - Deterministic eight-family scenario order, exact bounded OpenCode prompts, calendar assertions, and stable managed-damage rule expectations used by the one-command runner.
- [Interrupted upgrade checkpoint harness](checkpoint.py) - Qualification-only execution of the exact assembled installer with deterministic abort and resume interruption boundaries.
- [Interrupted upgrade checkpoint procedure](checkpoints.md) - Exact checkpoint, recovery, terminal-state, cleanup, and evidence commands for the interrupted-upgrade scenarios.
- [Dependency lock](requirements.lock) - Runtime and dependency boundary for deterministic generation.
- [Oracle schema](oracle.schema.json) - Contract for the generated baseline oracle and per-source expected outcomes.
- [Run manifest schema](run-manifest.schema.json) - Contract for binding qualification scenarios to releases, environments, transcripts, inventories, and decisions.

For generated `06-interrupted-upgrade-states` scenarios, the execution-plan phrase `maintained checkpoint harness` refers specifically to `checkpoint.py` and the command contract in `checkpoints.md`. The checkpoint JSON is setup evidence only. The real assembled `ava-install.sh --abort` or `--resume` result and its terminal state must still be recorded before the scenario is accepted.
