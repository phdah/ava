# Release qualification execution

Mandatory release qualification runs in GitHub Actions for the exact Release Please PR revision.

The workflow `.github/workflows/release-qualification.yml` invokes:

```sh
python3 -m internal.release.qualification_ci
```

`qualification_ci.py` resolves the current qualification operation, prepares repository-external fixture state, and invokes `run-release-qualification.sh`. That setup runner calls the stable `qualify-release.sh` entry point, which executes `qualification.py` and the deterministic `qualification_engine.py`.

## Root release `1.0.0`

The first stable release has no source release and no adjacent edge. The `bootstrap-to-1.0.0` operation therefore prepares only exact local target assets and runs target-only deterministic qualification.

The final root-release run covers the applicable installation, mature-project preservation, managed-damage, target identity, and conformance checks. Source-to-target upgrade, resume, abort, rollback, and semantic transition checks are inapplicable.

A successful run writes final evidence with status `awaiting-user-signoff`.

## Later releases

Starting with `1.0.1`, qualification binds exact verified source assets for the immediately previous published stable release.

`pre-edge` runs before the adjacent upgrade edge is authored. It validates behavior independent of that edge and writes no acceptance state.

`final` requires the reviewed adjacent edge, reruns deterministic mechanical scenarios, validates lifecycle recovery paths, performs a deterministic source-to-target upgrade, and writes evidence with status `awaiting-user-signoff`.

## Evidence and acceptance

Final CI evidence records the exact repository revision, target release identity, matrix digest, engine digest, executor label, outcomes, run ID, and source release identity when one exists.

A passing final run is not accepted automatically. User approval is applied only to that exact run through `accept-release-qualification.sh` or the validated acceptance-request path in `qualification_ci.py`.

## Diagnostic execution

When a shell environment is available, the maintained helper is:

```sh
internal/release/run-release-qualification.sh pre-edge
internal/release/run-release-qualification.sh final
```

The root release may resolve both requested stages to the applicable target-only qualification behavior. Direct execution is diagnostic. GitHub Actions remains the mandatory release gate.
