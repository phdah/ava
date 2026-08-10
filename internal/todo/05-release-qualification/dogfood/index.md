# Alpha Dogfood Findings

This index is the mutable backlog for findings discovered while exercising published Ava prereleases. The parent task remains [Dogfood the Alpha and Track Findings](../04-dogfood-alpha-and-track-findings.md).

Dogfooding remains active until the user explicitly declares it complete.

## Current next finding

[Clarify release semantic-impact assessment](13-clarify-release-semantic-impact-assessment.md) is pending and blocks the next prerelease. Release completion must distinguish Ava-managed behavioral change from project-owned semantic incompatibility before deciding `semantic_review_required`, and must justify both `true` and `false` decisions without defaulting to either.

[Avoid redundant routing for conversational follow-ups](12-avoid-redundant-followup-routing.md) is complete. Every request retains the managed-state gate, pure clarifications may be roleless, same-objective scoped follow-ups may retain the already-active role, and new or changed scoped work performs fresh routing.

The synthetic qualification vault remains the next supporting qualification task after the pending blocker is resolved. The dogfood umbrella remains active regardless of backlog state.

## Backlog status

- 1 pending finding
- 1 pending blocker
- 0 pending required-v1 findings
- 12 completed findings

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
| 10 | completed | required-v1 | release candidate | [Define release-impact-based change types](10-define-release-impact-based-change-types.md) |
| 11 | completed | blocker | next prerelease | [Normalize and enforce adjacent-edge release authoring](11-enforce-adjacent-edge-release-authoring.md) |
| 12 | completed | required-v1 | release candidate | [Avoid redundant routing for conversational follow-ups](12-avoid-redundant-followup-routing.md) |
| 13 | pending | blocker | next prerelease | [Clarify release semantic-impact assessment](13-clarify-release-semantic-impact-assessment.md) |

## Backlog rules

- Add every repository finding as the next numbered bounded task.
- Resolve blockers before the next prerelease.
- Mark a finding complete in its implementation PR when code, tests, documentation, indexes, and resolution evidence are complete.
- Keep immutable-release follow-up as a release gate rather than returning implemented work to pending.
- Completed findings remain durable evidence.
- Only the user may complete the parent dogfood task.

Finding 11 requires the next release to prove immutable catalog inheritance, one-edge authoring, multi-source composition, and exact-once semantic guidance against the tagged release. Finding 12 additionally requires realistic multi-turn evidence that full routing occurs only at defined transition points while the finding 07 no-bypass guarantee remains intact. Finding 13 must be implemented before another release PR is completed so release authoring cannot mechanically advance semantic compatibility from an insufficient project-owned impact assessment.
