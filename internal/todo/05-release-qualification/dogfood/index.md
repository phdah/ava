# Alpha Dogfood Findings

This index is the mutable backlog for findings discovered while exercising published Ava prereleases. The parent task remains [Dogfood the Alpha and Track Findings](../04-dogfood-alpha-and-track-findings.md).

Dogfooding remains active until the user explicitly declares it complete.

## Current next finding

A two-day operational-reliability investigation (2026-08-24 to 2026-08-25) into the release qualification pipeline itself recorded Findings 30-36. Finding 30 was later closed as a no-op, Finding 33 is complete, and the user explicitly removed the original Findings 34, 35, and 36. Findings 31 and 32 are now also removed after reassessment because their resume and run-status work primarily mitigated the former multi-hour ingestion workload. Finding 33 reduced `complete-pending-inbox` from 305 live sources to seven representative sources, so those mitigations no longer justify prerelease blockers without fresh evidence.

**Finding 34 is next up and is the sole remaining next-prerelease blocker.** If the next real qualification run exposes a concrete reliability problem, record a new finding from that observed behavior rather than preemptively restoring Findings 31 or 32.

[Decide whether to keep, shrink, or remove the complete-pending-inbox qualification scenario](33-decide-keep-minimize-or-remove-complete-pending-inbox-scenario.md) is complete. The maintained one-command fixture now deterministically reduces the live inbox workload to seven sources, one for each maintained text/document format, while leaving the immutable 305-file corpus unchanged. The decision retains end-to-end Inbox Ingester coverage while removing redundant live volume from every release qualification run.

[Detach qualification automation's process tree from the operator session lifecycle](30-detach-qualification-process-tree-from-session.md) is complete as a no-op. The original diagnosis was not proven, and detaching a local process would not solve a computer shutdown. Existing qualification behavior remains unchanged.

[Restore agent tool freedom during inbox ingestion](34-restore-agent-tool-freedom-during-inbox-ingestion.md) is pending. Finding 27 introduced a mechanism-level prohibition on scripts, code execution, temporary helpers, and programmatic transformations. The user has explicitly rejected that restriction: Ava should constrain authority, trust, semantic fidelity, provenance, and final state, while allowing the host agent to choose and use its available tools.

Qualification run `20260824T122451984003Z-alpha14-to-alpha15-corrective-local` (candidate `77977f8`) ended `needs-review`. Findings 27, 28, and 29 record its independent-audit findings. Findings 28 and 29 remain the desired semantic safeguards. Finding 27 is historically implementation-complete, but replacement Finding 34 will supersede only its execution-mechanism restriction.

[Decide how qualification should detect inbox semantic-disposition failures](29-decide-runner-inbox-semantic-detection-approach.md) is complete. The approved approach separates deterministic `structural-pass` from evaluator-only semantic judgment and adds bounded non-oracle processed-source, metadata, and footnote checks while leaving semantic fidelity to the independent audit.

[Require reconciled per-passage disposition evidence before inbox completion](28-require-reconciled-inbox-disposition-evidence.md) is complete. Inbox completion now requires section ledgers to be reconciled against rendered trusted destinations, explicitly verifies that non-durable passages are not promoted, keeps ambiguous sections pending, and gives independent qualification audit coverage for whole-source promotion and unsupported totals.

[Prohibit ad hoc code execution during inbox ingestion](27-prohibit-ad-hoc-code-during-inbox-ingestion.md) is complete as historical implementation evidence. Its mechanism-level prohibition is now scheduled for reversal by replacement Finding 34; its original semantic-fidelity concerns remain covered by Findings 28 and 29.

[Offer optional todo tracking for qualification failures](25-offer-qualification-failure-todo-tracking.md) is pending. It is a `post-v1` process improvement and is not release-blocking.

[Remove the hardcoded semantic-inspection-path qualification gate](26-remove-hardcoded-semantic-inspection-path-gate.md) is complete. The deterministic qualification-matrix gate that compared recorded inspection paths against a fixed, edge-agnostic list is removed; semantic-inspection adequacy is judged by the independent audit instead.

[Fix the OpenCode session-export pipe truncation](24-fix-opencode-session-export-pipe-truncation.md) is complete. The maintained qualification OpenCode adapter now buffers session-list database JSON and session exports through regular temporary files before re-emitting them, with oversized pipe-sensitive regression coverage. Fresh qualification must prove the former external shim is no longer needed.

[Report the inspected root index during pending-semantic-reconciliation](23-report-inspected-path-during-pending-semantic-reconciliation.md) is complete. Upgrade Role now explicitly confirms each inspection-only project-owned path in its completion report, and fixture coverage requires all four expected reported project-owned paths for the pending semantic-reconciliation scenario.

[Report inspected project-owned paths during interrupted-finalize](22-report-inspected-paths-during-interrupted-finalize.md) is complete. Ava Maintenance now reports durable semantic inspection evidence from the validated terminal journal during interrupted cleanup without rereading project-owned semantic inputs, and fixture coverage requires all four expected project-owned paths.

[Record semantic inspection paths before completion](21-record-semantic-inspection-paths.md) is complete. Upgrade Role now records guidance-driven inspection-only paths explicitly, and the synthetic qualification gate fails known semantic scenarios whose required path accounting is missing, duplicated, or unresolved.

[Preserve large-batch inbox fidelity and claim provenance](20-preserve-large-batch-inbox-fidelity.md) is complete. Delegated inbox batches now retain one coordinator-owned selected-source ledger, complete per-source child evidence, cross-child provenance reconciliation, and precise attribution for source-specific claims.

[Add one-command synthetic qualification runner](19-add-one-command-qualification-runner.md) is complete. The complete corrected matrix now has one internal manual shell entry point with pinned-input preflight, isolated runner-owned workspaces, Finding 17's authentic resume/abort checkpoints, Finding 18's calendar regression, exact managed-damage rule checks, bounded OpenCode prompts, interrupted reruns, and nonzero terminal summary semantics.

[Verify relative calendar dates before persisting](18-verify-relative-calendar-dates.md) is complete. Relevant persistence work conditionally loads a deterministic calendar-verification contract, preserves unresolved relative wording instead of inventing absolute dates, distinguishes current-host and source-document reference contexts, and gives Change Reviewer explicit semantic-fidelity coverage for contradictory weekday/date values.

The immediate release action remains blocked only until Finding 34 is resolved. After that blocker is complete, assemble a new exact corrective-alpha candidate from the updated release PR revision and execute the complete runner matrix with a fresh independent audit. A newly discovered blocker preempts that run; a `required-v1` finding preempts the release gate named by its `blocks` field.

[Add deterministic resume and abort qualification checkpoints](17-add-resume-abort-qualification-checkpoints.md) is complete. The synthetic-vault interrupted-upgrade plans have a repository-only harness that creates authentic abortable and resumable installer transactions without adding a public installer mode or fabricating managed state.

[Preserve existing scoped history during ingestion](16-preserve-existing-scoped-history-during-ingestion.md) is complete. Inbox Ingester now has additive-only authority over a qualifying scoped-history update, preserves all pre-existing entries, and hands cleanup or retirement to Project Steward or prior fixture preparation.

[Permit agent-driven upgrade finalization](15-permit-agent-driven-upgrade-finalization.md) is complete. Ava Maintenance now performs successful terminal finalization directly after proving the protocol preconditions, without searching for an installer binary, while resume, abort, rollback, and non-terminal mutations remain installer-backed.

The dogfood umbrella remains active regardless of backlog state. New blockers preempt the next prerelease, while `required-v1` findings preempt their declared release gates.

## Backlog status

- 2 pending findings
- 1 pending blocker
- 0 pending required-v1 findings
- 1 pending post-v1 finding
- 30 completed findings

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
| 16 | completed | required-v1 | release candidate | [Preserve existing scoped history during ingestion](16-preserve-existing-scoped-history.md) |
| 17 | completed | required-v1 | release candidate | [Add deterministic resume and abort qualification checkpoints](17-add-resume-abort-qualification-checkpoints.md) |
| 18 | completed | required-v1 | release candidate | [Verify relative calendar dates before persisting](18-verify-relative-calendar-dates.md) |
| 19 | completed | required-v1 | release candidate | [Add one-command synthetic qualification runner](19-add-one-command-qualification-runner.md) |
| 20 | completed | required-v1 | release candidate | [Preserve large-batch inbox fidelity and claim provenance](20-preserve-large-batch-inbox-fidelity.md) |
| 21 | completed | required-v1 | release candidate | [Record semantic inspection paths before completion](21-record-semantic-inspection-paths.md) |
| 22 | completed | blocker | next prerelease | [Report inspected project-owned paths during interrupted-finalize](22-report-inspected-paths-during-interrupted-finalize.md) |
| 23 | completed | blocker | next prerelease | [Report the inspected root index during pending-semantic-reconciliation](23-report-inspected-path-during-pending-semantic-reconciliation.md) |
| 24 | completed | required-v1 | release candidate | [Fix OpenCode session-export pipe truncation](24-fix-opencode-session-export-pipe-truncation.md) |
| 25 | pending | post-v1 | none | [Offer optional todo tracking for qualification failures](25-offer-qualification-failure-todo-tracking.md) |
| 26 | completed | blocker | next prerelease | [Remove hardcoded semantic-inspection-path qualification gate](26-remove-hardcoded-semantic-inspection-path-gate.md) |
| 27 | completed | blocker | next prerelease | [Prohibit ad hoc code execution during inbox ingestion](27-prohibit-ad-hoc-code-during-inbox-ingestion.md) |
| 28 | completed | blocker | next prerelease | [Require reconciled per-passage disposition evidence before inbox completion](28-require-reconciled-inbox-disposition-evidence.md) |
| 29 | completed | blocker | next prerelease | [Decide how qualification should detect inbox semantic-disposition failures](29-decide-runner-inbox-semantic-detection-approach.md) |
| 30 | completed | blocker | next prerelease | [Detach qualification automation's process tree from the operator session lifecycle](30-detach-qualification-process-tree-from-session.md) |
| 33 | completed | blocker | next prerelease | [Decide whether to keep, shrink, or remove the complete-pending-inbox qualification scenario](33-decide-keep-minimize-or-remove-complete-pending-inbox-scenario.md) |
| 34 | pending | blocker | next prerelease | [Restore agent tool freedom during inbox ingestion](34-restore-agent-tool-freedom-during-inbox-ingestion.md) |

## Backlog rules

- Add every repository finding as the next numbered bounded task.
- Resolve blockers before the next prerelease.
- Mark a finding complete in its implementation PR when code, tests, documentation, indexes, and resolution evidence are complete.
- Keep immutable-release follow-up as a release gate rather than returning implemented work to pending.
- Completed findings remain durable evidence.
- Only the user may complete the parent dogfood task.

Finding 11 requires the next release to prove immutable catalog inheritance, one-edge authoring, multi-source composition, and exact-once semantic guidance against the tagged release. Finding 12 additionally requires realistic multi-turn evidence that full routing occurs only at defined transition points while the Finding 07 no-bypass guarantee remains intact. Finding 13 is implemented: every release PR must apply the project-owned semantic-impact assessment and preserve reviewed rationale before accepting its adjacent edge. Finding 14 is implemented: Inbox Ingester required reading uses explicit project-root inbox paths with installed-payload regression coverage. Finding 15 is implemented: Ava Maintenance owns successful terminal finalization directly, with mandatory preconditions and no installer-binary dependency, while all broader deterministic mutation boundaries remain intact. Finding 16 is implemented: ingestion-time scoped-history authority is additive-only, prior entries are preserved, and cleanup or retirement remains outside Inbox Ingester authority. Finding 17 is implemented: the repository-only checkpoint harness executes the exact assembled installer transaction machinery, exposes no public mode, and supplies deterministic authentic setup states for the real `--abort` and `--resume` qualification operations. Finding 18 is implemented: relevant persistence uses conditional deterministic calendar verification, source-relative dates remain source-anchored, unresolved semantics are preserved or clarified, and contradictory weekday/date persistence is a semantic-fidelity review concern. Finding 19 is implemented: one internal shell command now composes the maintained pinned-input qualification matrix while preserving the finalized corpus and external test project as read-only boundaries. Finding 20 is implemented: delegated and large-batch ingestion preserves complete per-source evidence and cross-source provenance before batch completion. Finding 21 is implemented: semantic completion records inspection-only and changed project paths explicitly, and deterministic qualification postconditions reject missing accounting. Finding 22 is implemented: interrupted terminal cleanup reports every project-owned path recorded by semantic reconciliation from durable terminal journal evidence without broadening Ava Maintenance authority to reread project-owned context. Finding 23 is implemented: Upgrade Role's semantic completion report explicitly confirms each inspection-only project-owned path, and the pending semantic-reconciliation fixture pins the expected paths. Finding 24 is implemented: qualification buffers OpenCode session-list and export JSON through regular files so oversized evidence capture no longer depends on an external shim. Finding 26 is implemented: the fixed, edge-agnostic expected-inspected-path list and its deterministic qualification-matrix gate are removed because they do not generalize across release edges; semantic-inspection adequacy is judged by the independent audit. Finding 27 is implemented historically, but replacement Finding 34 will reverse its tool/script prohibition while keeping the final-state and semantic safeguards separate. Finding 28 is implemented: Inbox completion reconciles per-section dispositions against final rendered trusted destinations, rejects promoted non-durable content and unresolved ambiguity, and the independent qualification audit checks those semantics against the evaluator-only oracle. Finding 29 is implemented: evidence-only runner scenarios can report structural success without claiming semantic success, complete-inbox adds bounded non-oracle fidelity checks, and the independent audit remains the semantic authority. Finding 30 is resolved as a no-op after its proposed root cause was not established; no detached qualification implementation is retained. Finding 33 is implemented: the maintained one-command fixture keeps `complete-pending-inbox` but reduces it to the exact seven-source format lower bound, records the deterministic selection, preserves all three section dispositions, and leaves the complete 305-file corpus unchanged. Finding 34 is pending: restore agent tool freedom during ingestion and judge correctness by authority, fidelity, provenance, and final state rather than implementation mechanism.
