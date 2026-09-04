# Deterministic release qualification

Ava release qualification is a deterministic mechanical gate around one exact adjacent release pair. The active pair lives in `qualification/config.json` and resolves through `qualification/pair-catalog.json`.

## Inputs

A qualification execution binds:

- the exact repository revision,
- one published source release and verified asset digests,
- one local target release assembled from the same repository revision,
- the synthetic qualification matrix,
- the deterministic qualification engine,
- the execution stage.

All mutable workspaces and test projects must be outside the Ava repository.

## Pre-edge stage

The `pre-edge` stage selects deterministic fresh-install, mature-install, and managed-damage scenarios. It is a fail-fast gate before adjacent edge authoring. It writes no repository acceptance evidence.

## Semantic review boundary

Semantic impact is reviewed by the Ava Internal Maintainer before edge authoring.

### Managed delta

Record the relevant managed behavior change.

### Project-owned compatibility

Decide whether project-owned roles, workflows, shared instructions, indexes, host entrypoints, or other extensions can be affected. Deterministic project-file migration presence or absence does not make this decision.

### Required reconciliation

If semantic compatibility can be affected, record bounded discovery conditions, completion criteria, and reviewed reconciliation guidance. Otherwise record the rationale for no project-owned reconciliation.

## Final stage

The `final` stage requires the exact reviewed adjacent edge. It runs the deterministic mechanical scenarios plus resume, abort, rollback, and a deterministic source-to-target upgrade.

A successful final run writes a run record and runner summary under `qualification/runs/`, updates `qualification/current-state.json` to `awaiting-user-signoff`, and exposes the evidence through GitHub Actions.

The evidence schema is `qualification/schemas/qualification-run-record.schema.json`. New evidence records executor provenance as `qualification_executor`.

## Acceptance

Qualification acceptance is an explicit user decision bound to one final run. `qualification_acceptance.py` validates the run identity, active pair, revision, source and target identities, and current state before recording acceptance.

The release PR policy validator requires accepted final qualification before merge.

## Behavioral fixture coverage

The synthetic qualification corpus also contains behavioral scenarios used by repository tests and targeted QA. They are not selected by the mandatory deterministic release gate and do not create release acceptance state.
