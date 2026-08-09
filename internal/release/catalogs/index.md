# Immutable Release Edge Records

Each JSON file belongs to one target release and contains exactly one edge from the immediately previous release. It also contains only that edge's guidance and source-retirement decisions.

- [1.0.0-alpha.6](1.0.0-alpha.6.json) records `1.0.0-alpha.5 -> 1.0.0-alpha.6`.
- [1.0.0-alpha.7](1.0.0-alpha.7.json) records `1.0.0-alpha.6 -> 1.0.0-alpha.7`.
- [1.0.0-alpha.8](1.0.0-alpha.8.json) records `1.0.0-alpha.7 -> 1.0.0-alpha.8`.
- [1.0.0-alpha.9](1.0.0-alpha.9.json) records `1.0.0-alpha.8 -> 1.0.0-alpha.9`.
- [1.0.0-alpha.10](1.0.0-alpha.10.json) records `1.0.0-alpha.9 -> 1.0.0-alpha.10` and owns that transition's semantic guidance.
- [1.0.0-alpha.11](1.0.0-alpha.11.json) records `1.0.0-alpha.10 -> 1.0.0-alpha.11`.
- [1.0.0-alpha.12](1.0.0-alpha.12.json) records `1.0.0-alpha.11 -> 1.0.0-alpha.12`.

To resolve an upgrade, start with the target release record and follow each edge's `from` version backwards until the installed source release is reached. The selected records are then composed chronologically in memory. No release file repeats older edges.

For a new release:

1. leave every existing release record unchanged
2. create only `internal/release/catalogs/<target>.json`
3. author exactly one edge, `<previous> -> <target>`
4. add only guidance, migrations, and retirement decisions introduced by that edge
5. validate the recursive chain from retained sources to the target

Published direct source-to-target representations are generated compatibility output, not catalog-authoring templates.
