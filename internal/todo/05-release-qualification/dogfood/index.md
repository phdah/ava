# Alpha Dogfood Findings

This index is the mutable backlog for findings discovered while exercising published Ava prereleases. The parent task remains [Dogfood the Alpha and Track Findings](../04-dogfood-alpha-and-track-findings.md).

Dogfooding remains active until the user explicitly declares it complete.

## Current next finding

[Verify relative calendar dates before persisting](18-verify-relative-calendar-dates.md) is the current finding. It requires deterministic verification when relevant persistence work converts relative calendar language into an absolute fact.

[Add deterministic resume and abort qualification checkpoints](17-add-resume-abort-qualification-checkpoints.md) is complete. The synthetic-vault interrupted-upgrade plans now have a repository-only harness that creates authentic abortable and resumable installer transactions without adding a public installer mode or fabricating managed state.

After finding 18 is complete, repeat its affected scenario, execute resume and abort against the selected qualification assets, record the terminal evidence, and finish the synthetic-vault Step 1 signoff gate. A newly discovered `blocker` or `required-v1` finding still preempts that sequence.

[Preserve existing scoped history during ingestion](16-preserve-existing-scoped-history-during-ingestion.md) is complete. Inbox Ingester now has additive-only authority over a qualifying scoped-history update, preserves all pre-existing entries, and hands cleanup or retirement to Project Steward or prior fixture preparation.

[Permit agent-driven upgrade finalization](15-permit-agent-driven-upgrade-finalization.md) is complete. Ava Maintenance now performs successful terminal finalization directly after proving the protocol preconditions, without searching for an installer binary, while resume, abort, rollback, and non-terminal mutations remain installer-backed.

The dogfood umbrella remains active regardless of backlog state. New `blocker` or `required-v1` findings still preempt the qualification sequence if discovered.

## Backlog status

- 1 pending finding
- 0 pending blockers
- 1 pending required-v1 finding
- 17 completed findings

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
| 09 | completed | required-v1 | release candidate | [Compose semantic upgrades from adjacent release edges](09-compose-semantic-upgrades-from-adjacent-release-edges.md) |
| 10 | completed | required-v1 | release candidate | [Define release-impact-based change types](10-define-release-impact-based-change-types.md) |
| 11 | completed | blocker | next prerelease | [Normalize and enforce adjacent-edge release authoring](11-enforce-adjacent-edge-release-authoring.md) |
| 12 | completed | required-v1 | release candidate | [Avoid redundant routing for conversational follow-ups](12-avoid-redundant-followup-routing.md) |
| 13 | completed | blocker | next prerelease | [Clarify release semantic-impact assessment](13-clarify-release-semantic-impact-assessment.md) |
| 14 | completed | blocker | next prerelease | [Repair Inbox Ingester project-root links](14-repair-inbox-ingester-project-root-links.md) |
| 15 | completed | blocker | next prerelease | [Permit agent-driven upgrade finalization](15-permit-agent-driven-upgrade-finalization.md) |
| 16 | completed | required-v1 | release candidate | [Preserve existing scoped history during ingestion](16-preserve-existing-scoped-history-during-ingestion.md) |
| 17 | completed | required-v1 | release candidate | [Add deterministic resume and abort qualification checkpoints](17-add-resume-abort-qualification-checkpoints.md) |
| 18 | pending | required-v1 | release candidate | [Verify relative calendar dates before persisting](18-verify-relative-calendar-dates.md) |

## Backlog rules

- Add every repository finding as the next numbered bounded task.
- Resolve blockers before the next prerelease.
- Mark a finding complete in its implementation PR when code, tests, documentation, indexes, and resolution evidence are complete.
- Keep immutable-release follow-up as a release gate rather than returning implemented work to pending.
- Completed findings remain durable evidence.
- Only the user may complete the parent dogfood task.

Finding 11 requires the next release to prove immutable catalog inheritance, one-edge authoring, multi-source composition, and exact-once semantic guidance against the tagged release. Finding 12 additionally requires realistic multi-turn evidence that full routing occurs only at defined transition points while the finding 07 no-bypass guarantee remains intact. Finding 13 is implemented: every release PR must apply the project-owned semantic-impact assessment and preserve reviewed rationale before accepting its adjacent edge. Finding 14 is implemented: Inbox Ingester required reading uses explicit project-root inbox paths with installed-payload regression coverage. Finding 15 is implemented: Ava Maintenance owns successful terminal finalization directly, with mandatory preconditions and no installer-binary dependency, while all broader deterministic mutation boundaries remain intact. Finding 16 is implemented: ingestion-time scoped-history authority is additive-only, prior entries are preserved, and cleanup or retirement remains outside Inbox Ingester authority. Finding 17 is implemented: the repository-only checkpoint harness executes the exact assembled installer transaction machinery, exposes no public mode, and supplies deterministic authentic setup states for the real `--abort` and `--resume` qualification operations. Finding 18 requires deterministic verification before relevant persistence work converts relative calendar language into absolute project facts.
