# Alpha Dogfood Findings

This index is the mutable backlog for findings discovered while exercising published Ava prereleases. The parent task remains [Dogfood the Alpha and Track Findings](../04-dogfood-alpha-and-track-findings.md).

Dogfooding remains active until the user explicitly declares it complete.

## Current next finding

[Define release-impact-based change types](10-define-release-impact-based-change-types.md) is the first actionable pending finding. It is `required-v1` work before release-candidate publication.

[Normalize and enforce adjacent-edge release authoring](11-enforce-adjacent-edge-release-authoring.md) is complete. The active alpha.5 through alpha.12 history is canonical adjacent state, legacy cumulative authoring is disabled, and required release gates enforce one new previous-to-target edge.

## Backlog status

- 1 pending finding
- 0 pending blockers
- 1 pending required-v1 finding
- 10 completed findings

## Findings

| ID | Status | Classification | Blocks | Finding |
|---|---|---|---|---|
| 01 | completed | blocker | next prerelease | [Restore supported prerelease upgrade paths](01-restore-prerelease-upgrade-paths.md) |
| 02 | completed | blocker | next prerelease | [Repair installed context link resolution](02-repair-installed-context-link-resolution.md) |
| 03 | completed | required-v1 | release candidate | [Make knowledge hierarchy promotion predictable](03-make-knowledge-hierarchy-promotion-predictable.md) |
| 04 | completed | required-v1 | release candidate | [Enforce faithful inbox ingestion completion](04-enforce-faithful-inbox-ingestion-completion.md) |
| 05 | completed | blocker | next prerelease | [Restore complete prerelease upgrade coverage](05-restore-complete-prerelease-upgrade-coverage.md) |
| 06 | completed | blocker | next prerelease | [Remove empty upgrade transaction containers](06-remove-empty-upgrade-transaction-containers.md) |
| 07 | completed | blocker | next prerelease | [Enforce role routing before every response](07-enforce-role-routing-before-every-response.md) |
| 08 | completed | required-v1 | release candidate | [Define review sufficiency and termination criteria](08-define-review-sufficiency-and-termination.md) |
| 09 | completed | required-v1 | release candidate | [Compose semantic upgrades from adjacent release edges](09-compose-semantic-upgrades-from-adjacent-edges.md) |
| 10 | pending | required-v1 | release candidate | [Define release-impact-based change types](10-define-release-impact-based-change-types.md) |
| 11 | completed | blocker | next prerelease | [Normalize and enforce adjacent-edge release authoring](11-enforce-adjacent-edge-release-authoring.md) |

## Backlog rules

- Add every repository finding as the next numbered bounded task.
- Resolve blockers before the next prerelease.
- Mark a finding complete in its implementation PR when code, tests, documentation, indexes, and resolution evidence are complete.
- Keep immutable-release follow-up as a release gate rather than returning implemented work to pending.
- Completed findings remain durable evidence.
- Only the user may complete the parent dogfood task.

Finding 11 requires the next release to prove immutable catalog inheritance, one-edge authoring, multi-source composition, and exact-once semantic guidance against the tagged release.
