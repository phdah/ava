---
type: Internal Release Qualification Host Procedure
title: ChatGPT Work Cloud Qualification Execution
description: Required ChatGPT-hosted execution procedure for Ava release qualification without OpenCode or user-local compute.
tags: [internal, release, qualification, chatgpt, work, cloud, subagents]
generated:
  by: agent:openai-chatgpt
  at: 2026-09-02T17:30:00+02:00
updated:
  by: agent:openai-chatgpt
  at: 2026-09-02T17:55:00+02:00
---

# Purpose

Ava release qualification runs completely on ChatGPT-hosted compute.

The supported execution surface is **ChatGPT Work Cloud**. Qualification must not depend on a developer workstation, Work Local, Codex Local, OpenCode, a local shell, a locally mounted repository, or another user-hosted process.

GitHub Actions continues to own the repository checks that already run in CI. This procedure owns the release qualification work that requires isolated mutable projects and agent behavior. The GitHub Actions Python/repository suite is not duplicated inside the Work qualification task merely to satisfy this procedure.

# Required Work capabilities

The Work task must have:

- Work Cloud execution, not Work Local
- code and shell execution in the Work cloud environment
- network access for the GitHub endpoints needed to fetch the repository and immutable release assets
- the GitHub connection with permission to update the release PR branch when compact qualification evidence must be committed
- the ability to create a **fresh blank-slate Work agent context** for each semantic qualification interaction
- read/write access from that fresh context to the exact isolated scenario workspace prepared by the parent qualification driver
- a cloud-only evidence handoff back to the parent Work task

The product may expose the fresh context as a delegated subagent, an additional Work agent, or another equivalent isolated Work execution primitive. The protocol does not depend on a product-internal session identifier or UI label. It does require the semantic agent to start without inherited parent conversation, saved memory, prior scenario context, or unrelated connected tools, while still operating against the exact prepared scenario workspace.

A separate fresh Work chat is acceptable only if ChatGPT can give that chat read/write access to the exact same isolated cloud scenario workspace and return its response without leaving ChatGPT-hosted compute. Returning only a text/JSON answer from a disconnected chat is not sufficient because semantic qualification scenarios mutate and are then deterministically validated against that workspace.

If one of these capabilities is unavailable, stop and report the missing Work capability. Do not fall back to OpenCode or to the user's computer.

# Agent isolation contract

Every qualification interaction emitted by `qualification_work.py` is executed by one fresh blank-slate Work agent context.

The generated request is the only conversational instruction supplied to that context. Do not pass the parent Work conversation, prior qualification conversations, saved memory, unrelated project context, or previous scenario responses.

The fresh agent receives the generated request plus access to the exact `workspace_root`. It must:

1. operate only inside the request's `workspace_root`, except for reading the request and writing or returning the declared structured response
2. use only the Work cloud filesystem and shell needed for the isolated project
3. not use web search, cloud browser, plugins, apps, MCPs, other repositories, memory, or user-local files
4. read `AGENTS.md` first and follow all required Ava routing, role, workflow, and managed-state instructions
5. perform the exact scenario prompt as the isolated project's user request
6. write or return the structured response requested by the protocol, including ordered pre-mutation required-reading evidence

The parent task must not perform the semantic action in place of the fresh agent. The parent owns orchestration and deterministic validation.

Most semantic scenarios start from an isolated project in which the target Ava candidate was freshly installed by the deterministic runner. Scenarios intentionally testing upgrade, semantic reconciliation, interruption, finalization, or another lifecycle state instead receive that exact prepared lifecycle workspace. A fresh agent context does not mean erasing the scenario state being tested.

# Independent audit isolation

After all scenarios in a phase pass mechanically, the parent creates a **new fresh blank-slate Work agent context** that did not execute any qualification scenario.

The audit agent receives only the generated audit request and read access to:

- the Ava repository
- source and target release assets
- the finalized synthetic qualification vault
- scenario workspaces and deterministic command logs
- Work interaction request/response evidence
- the evaluator-only oracle

Its only permitted write is the declared audit response JSON. The parent validates that repository, scenario, asset, and fixture digests remained unchanged while the audit ran.

# Work Cloud setup

Start the release qualification from a Work chat on web or mobile, or from a cloud Work chat on desktop. Do not open a local folder for this operation.

Use the connected GitHub repository as the authoritative source, then create one repository-external Work cloud run root. A typical setup is:

```sh
set -eu
repo="$PWD"
run_parent="${TMPDIR:-/tmp}/ava-work-qualification"
mkdir -p "$run_parent"
run_root=$(mktemp -d "$run_parent/run.XXXXXX")
mkdir -p "$run_root/assets/source" "$run_root/fixture" "$run_root/test-project" "$run_root/execution"
```

The Work task must be checked out at the exact release PR revision that is being qualified. `qualification_work.py init` binds the target release assets to that repository revision and refuses a mismatch.

# Resolve the exact source release

Read the active pair from `internal/release/qualification/config.json` and `pair-catalog.json`. Download the exact published source tag into `$run_root/assets/source` and verify its immutable release/asset attestations before qualification.

The existing checked-in pair catalog contains the expected source revision, manifest digest, and every release-asset digest. `qualification_work.py init` revalidates the downloaded bytes against that catalog, so a mutable or mismatched source cannot enter the run.

This step may use `gh release download`, `gh release verify`, and `gh release verify-asset` inside Work Cloud, or equivalent connected GitHub operations. It must not use a release bundle from the user's machine.

# Generate the fixture and test boundary

Generate the qualification vault inside Work Cloud:

```sh
TMPDIR="$run_root/fixture" internal/release/generate-synthetic-qualification-vault.sh
```

Use the path printed by the generator as `qualification_root`.

Create the repository-external read-only test boundary:

```sh
cat > "$run_root/test-project/index.md" <<'EOF'
# Qualification test boundary

Repository-external byte-integrity sentinel.
EOF
cat > "$run_root/test-project/sentinel.json" <<'EOF'
{"purpose":"qualification-test-boundary","schema_version":1}
EOF
```

# Edge-independent phase

From the exact clean release PR revision, before the target adjacent catalog or guidance is authored:

```sh
target_assets="$(internal/release/assemble-candidate.sh --phase edge-independent)"
internal/release/qualify-release.sh init \
  --phase edge-independent \
  --qualification-root "$qualification_root" \
  --execution-root "$run_root/execution" \
  --source-assets "$run_root/assets/source" \
  --target-assets "$target_assets" \
  --test-project "$run_root/test-project"
```

Then run the Work orchestration loop.

# Work orchestration loop

Call:

```sh
internal/release/qualify-release.sh advance \
  --execution-root "$run_root/execution"
```

Exit meanings are:

- `0`: every scenario in the phase has passed mechanically
- `1`: a scenario failed or requires a user decision; stop and report the exact summary
- `2`: the qualification protocol or inputs are invalid; stop
- `3`: a fresh blank-slate Work agent context is required

When exit `3` prints `SUBAGENT_REQUIRED <request-path>`, treat `SUBAGENT_REQUIRED` as the protocol name for the required fresh Work agent context, not as a dependency on a particular product UI label.

1. read the complete generated request JSON
2. create one fresh blank-slate Work agent context with no inherited parent conversation, saved memory, prior scenario context, or unrelated tools
3. give it only the generated request plus read/write access to the exact `workspace_root`
4. require it to satisfy the request's execution contract and produce the declared structured response without using external tools
5. when the Work execution primitive shares the filesystem, let it write `response_path` directly; otherwise transfer the response back inside ChatGPT and write those exact bytes to `response_path` without rewriting or normalizing them
6. do not accept a disconnected fresh chat unless it also had read/write access to the exact scenario workspace and its mutations are present there when control returns
7. call `advance` again

Repeat until `advance` exits `0` or a non-passing result stops the phase.

The loop executes deterministic-only scenarios directly in the Work cloud shell. Agent scenarios are prepared by the deterministic runner, executed by fresh blank-slate Work agent contexts, and then validated deterministically before the next scenario starts.

# Independent audit

After `advance` exits `0`:

```sh
internal/release/qualify-release.sh audit-request \
  --execution-root "$run_root/execution"
```

The command exits `3` and prints `AUDIT_SUBAGENT_REQUIRED <request-path>`.

Create one new fresh blank-slate Work agent context that executed no qualification scenario. Give it only the generated audit request and the declared read-only evidence inputs. It must produce only the requested audit JSON response. Then finalize:

```sh
internal/release/qualify-release.sh finalize \
  --execution-root "$run_root/execution"
```

Finalization verifies audit immutability, validates the maintained audit schema, writes compact Work evidence under `internal/release/qualification/`, and updates the phase state.

For the edge-independent phase, a clean audit produces `passed`. Commit the exact generated `phase-runs/` evidence and `phase-state.json` to the release PR using the connected GitHub action before edge authoring.

# Edge-dependent phase

After semantic-impact review and adjacent edge authoring are complete, create a new Work cloud run root from the new exact release PR revision. Do not reuse the early scenario workspaces.

Assemble the reviewed candidate:

```sh
target_assets="$(internal/release/assemble-candidate.sh --phase edge-dependent)"
```

Initialize the final phase with the same steps as above, changing only the phase and new external run paths:

```sh
internal/release/qualify-release.sh init \
  --phase edge-dependent \
  --qualification-root "$qualification_root" \
  --execution-root "$run_root/execution" \
  --source-assets "$run_root/assets/source" \
  --target-assets "$target_assets" \
  --test-project "$run_root/test-project"
```

Initialization validates the committed early Work evidence with `qualification_phase_gate.py`, including revision ancestry, source identity, target version, early absence of the adjacent edge, and the allowed intervening change set.

Run the same `advance`, fresh-agent, `audit-request`, fresh-audit-agent, and `finalize` loop.

A clean final audit produces `awaiting-user-signoff`. No agent may accept its own qualification.

# GitHub Actions boundary

The normal pull-request checks remain GitHub Actions work. In particular, `.github/workflows/python-tests.yml` executes the internal Backlog validation, installed-project task-board checks, and `internal/release/test.sh`, which runs the repository Python/unit test suite.

The Work release task must require those checks to pass but does not need to duplicate them in its own cloud shell. It may inspect their results through GitHub. Rerunning the repository test suite inside Work is optional diagnostic work only when investigating a failure, not part of the qualification evidence contract.

# Evidence

Work qualification does not depend on ChatGPT thread IDs, hidden product session identifiers, OpenCode session IDs, provider databases, or local transcript files.

Each agent interaction is bound to:

- one scenario and stage
- the exact scenario prompt digest
- the configured model identifier
- the exact isolated workspace path
- an ordered required-reading manifest bound to the pre-interaction workspace bytes
- a structured final response
- an assertion that no external tools were used
- the deterministic postconditions run after the fresh agent returns

The compact committed interaction evidence includes the structured response and its digest. The final run record binds the Work protocol, phase, exact repository revision, release identities, matrix digest, fixture digest, and qualification driver digest.

# No local fallback

OpenCode is not a supported release-qualification runtime. Neither is a developer terminal, Work Local, Codex Local, or a remotely controlled developer workstation.

If Work Cloud cannot create the isolated run root, run shell commands, access the exact GitHub inputs, create a fresh blank-slate agent context with read/write access to the exact prepared scenario workspace, return the evidence to the parent Work task, or write the compact evidence back to the release PR, qualification cannot proceed on that Work configuration. Report that exact missing capability instead of moving execution to a local machine.
