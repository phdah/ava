# Release qualification execution

Mandatory release qualification runs in GitHub Actions for the exact release PR revision.

The workflow `.github/workflows/release-qualification.yml` invokes:

```sh
python3 -m internal.release.qualification_ci
```

`qualification_ci.py` determines whether the candidate needs the `pre-edge` or `final` stage, prepares immutable source assets and repository-external fixture state, then invokes `run-release-qualification.sh`. That setup runner calls the stable `qualify-release.sh` entry point, which executes `qualification.py` and the deterministic `qualification_engine.py`.

## Stages

`pre-edge` runs before the adjacent upgrade edge is authored. It validates installation and managed-damage behavior that is independent of the edge and writes no acceptance state.

`final` requires the reviewed adjacent edge. It reruns deterministic mechanical scenarios, validates lifecycle recovery paths, runs a deterministic source-to-target upgrade, and writes final evidence with status `awaiting-user-signoff`.

## Evidence and acceptance

The final CI run exposes qualification evidence as an Actions artifact. The evidence records the exact repository revision, source and target release identities, matrix digest, engine digest, executor label, outcomes, and run ID.

A passing final run is not accepted automatically. User approval is applied only to that exact run through `accept-release-qualification.sh` or the validated acceptance-request path in `qualification_ci.py`.

## Diagnostic execution

When a shell environment is available, the maintained end-to-end setup helper is:

```sh
internal/release/run-release-qualification.sh pre-edge
internal/release/run-release-qualification.sh final
```

Direct execution is diagnostic. GitHub Actions remains the mandatory release gate.
