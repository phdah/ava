# Stable Release Edge Records

Stable `1.0.0` is the root of Ava's permanent release lineage. It is a first release, not an upgrade, so it has no release-edge record and declares no supported source releases.

For every release after `1.0.0`:

1. leave every existing stable release record unchanged
2. create only `internal/release/catalogs/<target>.json`
3. author exactly one edge from the immediately previous stable release to the target
4. add only guidance, migrations, and retirement decisions introduced by that edge
5. validate the complete recursive chain from `1.0.0` through the target

The first permanent edge is therefore `1.0.0 -> 1.0.1`.
