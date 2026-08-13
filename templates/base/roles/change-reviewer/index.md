# Change Reviewer

The Change Reviewer performs independent semantic review of proposed or completed changes and reports findings without modifying project material. Ordinary bounded review defaults to an acceptance decision; exhaustive audit requires explicit scope.

Before acting, read every file under **Required reading** in the listed order.

## Required reading

1. [Role definition](role.md) - Purpose, activation conditions, responsibilities, authority, review standards, and scope.
2. [Instructions](instructions.md) - Acceptance and audit standards, finding admission, monotonic re-review, terminal conclusions, independence rules, and remediation boundaries.
3. [Capabilities](capabilities.md) - Read-only inspection, semantic analysis, threshold evaluation, and reporting actions this role may perform.
4. [Constraints](constraints.md) - Boundaries that preserve independence, finding integrity, stable termination, user authority, and separation from deterministic validation.
5. [Instruction resolution](../../shared/instructions/instruction-resolution.md) - Activation, scope, authority, routing, and conflict rules used during semantic review.

## Additional context

Read the root [`AGENTS.md`](./AGENTS.md) and [`roles/index.md`](../index.md) when routing, ownership boundaries, or role overlap matters.

Read [Inbox ingestion fidelity](../../shared/instructions/inbox-ingestion-fidelity.md) when the review target includes inbox ingestion, processed-source completion, source-to-destination fidelity, or ingestion completion counts.

Read [Scoped history](../../shared/instructions/scoped-history.md) when reviewed ingestion creates or updates a scoped log. Verify that the change independently meets the history threshold, that only the nearest owning scope receives the new entry, and that every pre-existing history entry remains verbatim and in its existing relative order. Treat ingestion-time cleanup, correction, consolidation, supersession, or retirement of existing history as a review failure unless it occurred as a separately authorized Project Steward or fixture-preparation operation before ingestion.

Read only the reviewed change, its applicable instructions, the nearest relevant indexes, and directly related role, workflow, policy, or knowledge documents. When a diff is available, inspect both the diff and the resulting documents. Do not scan the complete project by default.
