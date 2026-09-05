# Deterministic release qualification

Ava release qualification is a deterministic mechanical gate around one exact release candidate. The active operation lives in `qualification/config.json` and resolves through `qualification/pair-catalog.json`.

## Inputs

Every qualification execution binds:

- the exact repository revision,
- one local target release assembled from that revision,
- the synthetic qualification matrix,
- the deterministic qualification engine,
- the execution stage.

Starting with `1.0.1`, qualification additionally binds the exact immediately previous published release and its verified asset digests.

For root release `1.0.0`, no source release exists. The checked-in `bootstrap-to-1.0.0` operation therefore has no source selector and qualification is target-only.

All mutable workspaces and test projects must be outside the Ava repository.

## Root-release qualification

`1.0.0` proves the root distribution itself. Applicable deterministic checks cover fresh installation, installation into a mature project without modifying project-owned content, managed-content damage detection, release conformance, and exact target identity.

Upgrade-only checks are not run because there is no supported installed source to upgrade, abort, resume, roll back, or semantically reconcile from.

A successful final root-release run writes normal qualification evidence with status `awaiting-user-signoff`.

## Ordinary pre-edge stage

Starting with `1.0.1`, `pre-edge` selects deterministic fresh-install, mature-install, and managed-damage scenarios before adjacent edge authoring. It is a fail-fast gate and writes no acceptance evidence.

## Semantic review boundary

Semantic impact review applies only when a source release exists. The maintainer records the managed delta, project-owned compatibility assessment, and any required bounded reconciliation before authoring a later adjacent edge.

## Ordinary final stage

Starting with `1.0.1`, `final` requires the exact reviewed adjacent edge. It reruns deterministic mechanical scenarios, exercises resume, abort, and rollback, and performs a deterministic source-to-target upgrade.

A successful final run writes a run record and runner summary under `qualification/runs/`, updates `qualification/current-state.json` to `awaiting-user-signoff`, and exposes the evidence through GitHub Actions.

## Acceptance

Qualification acceptance is an explicit user decision bound to one final run. `qualification_acceptance.py` validates the run identity, revision, target identity, current state, and source identity when one exists before recording acceptance.

A passing run never accepts itself.

## Behavioral fixture coverage

The synthetic qualification corpus also contains behavioral scenarios used by repository tests and targeted QA. They are not selected by the mandatory deterministic release gate and do not create release acceptance state.
