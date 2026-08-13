# Alpha Dogfood Findings

This index is the mutable backlog for findings discovered while exercising published Ava prereleases. The parent task remains [Dogfood the Alpha and Track Findings](../04-dogfood-alpha-and-track-findings.md).

Dogfooding remains active until the user explicitly declares it complete.

## Current next finding

[Preserve existing scoped history during ingestion](16-preserve-existing-scoped-history-during-ingestion.md) is the current pending finding. It requires Inbox Ingester to preserve pre-existing log entries, limit its scoped-history authority to appending a newly required entry, and hand cleanup or retirement of existing history to Project Steward or prior fixture preparation.

[Permit agent-driven upgrade finalization](15-permit-agent-driven-upgrade-finalization.md) is complete. Ava Maintenance now performs successful terminal finalization directly after proving the protocol preconditions, without searching for an installer binary, while resume, abort, rollback, and non-terminal mutations remain installer-backed.

[Repair Inbox Ingester project-root links](14-repair-inbox-ingester-project-root-links.md) is complete. The managed role now names the project-owned inbox through explicit project-root paths rather than nested Markdown links, and installed-payload regression coverage prevents the broken role-relative resolution from returning.

[Clarify release semantic-impact assessment](13-clarify-release-semantic-impact-assessment.md) is complete. Release completion now distinguishes Ava-managed behavioral change from possible project-owned semantic incompatibility before deciding `semantic_review_required`, requires reviewed rationale for both outcomes, and keeps semantic judgment out of deterministic validation.

[Avoid redundant routing for conversational follow-ups](12-avoid-redundant-followup-routing.md) is complete. Every request retains the managed-state gate, pure clarifications may be roleless, same-objective scoped follow-ups may retain the already-active role, and new or changed scoped work performs fresh routing.

Finding 16 preempts the synthetic qualification sequence until its `required-v1` repository work is resolved. The dogfood umbrella remains active regardless of backlog state.

## Backlog status

- 1 pending finding
- 0 pending blockers
- 1 pending required-v1 finding
- 15 completed findings

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
| 13 | completed | blocker | next prerelease | [Clarify release semantic-impact assessment](13-clarify-release-semantic-impact-assessment.md) |
| 14 | completed | blocker | next prerelease | [Repair Inbox Ingester project-root links](14-repair-inbox-ingester-project-root-links.md) |
| 15 | completed | blocker | next prerelease | [Permit agent-driven upgrade finalization](15-permit-agent-driven-upgrade-finalization.md) |
| 16 | pending | required-v1 | release candidate | [Preserve existing scoped history during ingestion](16-preserve-existing-scoped-history-during-ingestion.md) |

## Backlog rules

- Add every repository finding as the next numbered bounded task.
- Resolve blockers before the next prerelease.
- Mark a finding complete in its implementation PR when code, tests, documentation, indexes, and resolution evidence are complete.
- Keep immutable-release follow-up as a release gate rather than returning implemented work to pending.
- Completed findings remain durable evidence.
- Only the user may complete the parent dogfood task.

Finding 11 requires the next release to prove immutable catalog inheritance, one-edge authoring, multi-source composition, and exact-once semantic guidance against the tagged release. Finding 12 additionally requires realistic multi-turn evidence that full routing occurs only at defined transition points while the finding 07 no-bypass guarantee remains intact. Finding 13 is implemented: every release PR must apply the project-owned semantic-impact assessment and preserve reviewed rationale before accepting its adjacent edge. Finding 14 is implemented: Inbox Ingester required reading now uses explicit project-root inbox paths with installed-payload regression coverage. Finding 15 is implemented: Ava Maintenance owns successful terminal finalization directly, with mandatory preconditions and no installer-binary dependency, while all broader deterministic mutation boundaries remain intact. Finding 16 is pending and requires existing scoped history to remain immutable during ingestion except for appending a newly required entry.
