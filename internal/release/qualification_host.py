"""Host-neutral agent execution and evidence contract for release qualification."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Protocol, Sequence

from internal.release import qualification_automation as legacy_automation
from internal.release import qualification_runner

CAP_LOCAL_PROCESS = "local-process-execution"
CAP_MUTABLE_EXTERNAL_WORKSPACE = "mutable-external-workspace"
CAP_LOCAL_RELEASE_ASSETS = "local-release-assets"
CAP_AGENT_INTERACTION = "agent-interaction"
CAP_EXTERNAL_EVIDENCE_READ = "external-evidence-read"
CAP_INDEPENDENT_AUDIT = "independent-audit"

AGENT_SCENARIO_KINDS = {
    "registered-routing",
    "registered-calendar",
    "registered-clarification",
    "complete-inbox",
    "finalize",
    "semantic-reconciliation",
    "lifecycle",
}


class QualificationHostError(RuntimeError):
    pass


@dataclass(frozen=True)
class HostProfile:
    host_id: str
    capabilities: frozenset[str]
    description: str


@dataclass(frozen=True)
class HostAssessment:
    host_id: str
    complete: bool
    global_missing: tuple[str, ...]
    scenario_missing: dict[str, tuple[str, ...]]


@dataclass(frozen=True)
class HostDescriptor:
    adapter: str
    version: str

    def compact(self) -> dict[str, str]:
        return {"adapter": self.adapter, "version": self.version}


class CommandRunner(Protocol):
    def __call__(
        self,
        args: Sequence[str],
        *,
        cwd: Path | None = None,
        check: bool = True,
    ) -> legacy_automation.CommandResult: ...


class AgentHostAdapter(Protocol):
    adapter_id: str

    def descriptor(self) -> HostDescriptor: ...

    def interaction_command(
        self,
        *,
        project: Path,
        model: str,
        prompt: str,
        title: str | None = None,
    ) -> list[str]: ...

    def snapshot(self) -> object: ...

    def collect_interactions(
        self,
        *,
        before: object,
        after: object,
        execution_root: Path,
        configured_model: str,
        allow_empty: bool,
    ) -> dict[str, Any]: ...

    def audit_command(
        self,
        *,
        repository_root: Path,
        model: str,
        prompt: str,
    ) -> list[str]: ...


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def local_host_profile() -> HostProfile:
    return HostProfile(
        host_id="local-agent-host",
        capabilities=frozenset(
            {
                CAP_LOCAL_PROCESS,
                CAP_MUTABLE_EXTERNAL_WORKSPACE,
                CAP_LOCAL_RELEASE_ASSETS,
                CAP_AGENT_INTERACTION,
                CAP_EXTERNAL_EVIDENCE_READ,
                CAP_INDEPENDENT_AUDIT,
            }
        ),
        description="Local host with process execution, mutable external sandboxes, agent execution, and raw evidence access.",
    )


def chatgpt_github_profile() -> HostProfile:
    return HostProfile(
        host_id="chatgpt-github-connector",
        capabilities=frozenset({CAP_AGENT_INTERACTION}),
        description=(
            "ChatGPT with repository access can reason about and mutate repository files, but the GitHub connector does not provide "
            "the release qualification process sandbox, mutable repository-external project roots, local release assets, or raw external evidence roots."
        ),
    )


def scenario_requirements(scenario: dict[str, Any]) -> frozenset[str]:
    requirements = {
        CAP_LOCAL_PROCESS,
        CAP_MUTABLE_EXTERNAL_WORKSPACE,
        CAP_LOCAL_RELEASE_ASSETS,
    }
    if scenario.get("kind") in AGENT_SCENARIO_KINDS:
        requirements.add(CAP_AGENT_INTERACTION)
    return frozenset(requirements)


def assess_host(profile: HostProfile, matrix: dict[str, Any]) -> HostAssessment:
    global_required = {CAP_EXTERNAL_EVIDENCE_READ, CAP_INDEPENDENT_AUDIT}
    global_missing = tuple(sorted(global_required - profile.capabilities))
    scenario_missing = {
        scenario["id"]: tuple(sorted(scenario_requirements(scenario) - profile.capabilities))
        for scenario in matrix["scenarios"]
    }
    complete = not global_missing and all(not missing for missing in scenario_missing.values())
    return HostAssessment(profile.host_id, complete, global_missing, scenario_missing)


def validate_interaction_inventory(value: dict[str, Any]) -> None:
    if value.get("schema_version") != 1:
        raise QualificationHostError("interaction inventory schema_version must be 1")
    adapter = value.get("host_adapter")
    interactions = value.get("interactions")
    if not isinstance(adapter, str) or not adapter:
        raise QualificationHostError("interaction inventory requires host_adapter")
    if not isinstance(interactions, list):
        raise QualificationHostError("interaction inventory interactions must be an array")
    ids: set[str] = set()
    for record in interactions:
        if not isinstance(record, dict):
            raise QualificationHostError("interaction inventory contains a non-object record")
        required = {
            "interaction_id",
            "parent_interaction_id",
            "scenario",
            "prompt_sha256",
            "model",
            "workspace_root",
            "transcript_sha256",
            "terminal_state",
        }
        if set(record) != required:
            raise QualificationHostError(
                f"interaction inventory record fields differ from host-neutral contract: {sorted(record)}"
            )
        interaction_id = record["interaction_id"]
        if not isinstance(interaction_id, str) or not interaction_id.startswith("int_"):
            raise QualificationHostError("interaction inventory has invalid interaction_id")
        if interaction_id in ids:
            raise QualificationHostError("interaction inventory contains duplicate interaction_id")
        ids.add(interaction_id)
        for digest_field in ("prompt_sha256", "transcript_sha256"):
            digest = record[digest_field]
            if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise QualificationHostError(f"interaction inventory has invalid {digest_field}")
        if record["terminal_state"] != "completed":
            raise QualificationHostError("interaction inventory contains non-completed evidence")
        for field in ("scenario", "model", "workspace_root"):
            if not isinstance(record[field], str) or not record[field]:
                raise QualificationHostError(f"interaction inventory has invalid {field}")
    for record in interactions:
        parent = record["parent_interaction_id"]
        if parent is not None and parent not in ids:
            raise QualificationHostError(
                f"interaction inventory parent is absent from current evidence: {parent}"
            )


def normalize_opencode_inventory(session_inventory: dict[str, Any]) -> dict[str, Any]:
    sessions = session_inventory.get("sessions")
    if session_inventory.get("schema_version") != 1 or not isinstance(sessions, list):
        raise QualificationHostError("OpenCode adapter returned invalid session evidence")

    ordered = sorted(
        sessions,
        key=lambda item: (
            str(item.get("scenario", "")),
            str(item.get("prompt_sha256", "")),
            str(item.get("transcript_sha256", "")),
            str(item.get("session_id", "")),
        ),
    )
    id_map: dict[str, str] = {}
    for ordinal, record in enumerate(ordered, 1):
        session_id = record.get("session_id")
        if not isinstance(session_id, str) or not session_id:
            raise QualificationHostError("OpenCode session evidence has no session id")
        identity = {
            "ordinal": ordinal,
            "scenario": record.get("scenario"),
            "prompt_sha256": record.get("prompt_sha256"),
            "transcript_sha256": record.get("transcript_sha256"),
            "model": record.get("model"),
        }
        id_map[session_id] = "int_" + sha256_text(canonical_json(identity))[:24]

    interactions: list[dict[str, Any]] = []
    for record in ordered:
        session_id = record["session_id"]
        parent_session_id = record.get("parent_session_id")
        parent_interaction_id = None
        if parent_session_id is not None:
            parent_interaction_id = id_map.get(parent_session_id)
            if parent_interaction_id is None:
                raise QualificationHostError(
                    "OpenCode adapter evidence references a parent outside the current interaction set"
                )
        interactions.append(
            {
                "interaction_id": id_map[session_id],
                "parent_interaction_id": parent_interaction_id,
                "scenario": record["scenario"],
                "prompt_sha256": record["prompt_sha256"],
                "model": record["model"],
                "workspace_root": record["project_root"],
                "transcript_sha256": record["transcript_sha256"],
                "terminal_state": record["terminal_state"],
            }
        )
    inventory = {
        "schema_version": 1,
        "host_adapter": "opencode",
        "interactions": interactions,
    }
    validate_interaction_inventory(inventory)
    return inventory


class OpenCodeHostAdapter:
    """OpenCode implementation of the host-neutral qualification boundary."""

    adapter_id = "opencode"

    def __init__(
        self,
        executable: str,
        *,
        command_runner: Callable[..., legacy_automation.CommandResult] = legacy_automation.run_command,
    ) -> None:
        self.executable = executable
        self._command_runner = command_runner
        version = legacy_automation.opencode_version(
            executable,
            command_runner=command_runner,
        )
        self._descriptor = HostDescriptor(self.adapter_id, version)

    def descriptor(self) -> HostDescriptor:
        return self._descriptor

    def interaction_command(
        self,
        *,
        project: Path,
        model: str,
        prompt: str,
        title: str | None = None,
    ) -> list[str]:
        command = [
            self.executable,
            "run",
            "--dir",
            str(project),
            "--model",
            model,
            "--format",
            "json",
        ]
        if title:
            command.extend(["--title", title])
        command.append(prompt)
        return command

    def snapshot(self) -> object:
        return legacy_automation.snapshot_sessions(
            self.executable,
            command_runner=self._command_runner,
        )

    def collect_interactions(
        self,
        *,
        before: object,
        after: object,
        execution_root: Path,
        configured_model: str,
        allow_empty: bool,
    ) -> dict[str, Any]:
        if not isinstance(before, list) or not isinstance(after, list):
            raise QualificationHostError("OpenCode adapter session snapshots must be arrays")
        session_inventory = legacy_automation.build_session_inventory(
            before=before,
            after=after,
            execution_root=execution_root,
            opencode=self.executable,
            configured_model=configured_model,
            command_runner=self._command_runner,
            allow_empty=allow_empty,
        )
        return normalize_opencode_inventory(session_inventory)

    def audit_command(
        self,
        *,
        repository_root: Path,
        model: str,
        prompt: str,
    ) -> list[str]:
        return self.interaction_command(
            project=repository_root,
            model=model,
            prompt=prompt,
            title="Ava qualification independent audit",
        )


def resolve_host_adapter(
    kind: str,
    executable: str,
    *,
    command_runner: Callable[..., legacy_automation.CommandResult] = legacy_automation.run_command,
) -> AgentHostAdapter:
    if kind == "opencode":
        return OpenCodeHostAdapter(executable, command_runner=command_runner)
    raise QualificationHostError(f"unsupported qualification host adapter: {kind}")


def run_independent_audit(
    *,
    adapter: AgentHostAdapter,
    audit_model: str,
    prompt: str,
    repository_root: Path,
    raw_evidence_root: Path,
    command_runner: Callable[..., legacy_automation.CommandResult] = legacy_automation.run_command,
) -> tuple[dict[str, Any], str]:
    before_repo = legacy_automation.tree_digest(
        repository_root,
        exclude=[repository_root / ".git"],
    )
    before_raw = legacy_automation.tree_digest(raw_evidence_root)
    result = command_runner(
        adapter.audit_command(
            repository_root=repository_root,
            model=audit_model,
            prompt=prompt,
        ),
        check=False,
    )
    if result.returncode != 0:
        raise QualificationHostError(
            f"independent audit host failed: {result.stderr.strip()}"
        )
    if legacy_automation.tree_digest(
        repository_root,
        exclude=[repository_root / ".git"],
    ) != before_repo:
        raise QualificationHostError("independent audit mutated the Ava repository")
    if legacy_automation.tree_digest(raw_evidence_root) != before_raw:
        raise QualificationHostError("independent audit mutated qualification evidence")
    audit = legacy_automation.extract_audit_json(result.stdout)
    schema = legacy_automation.load_json(
        repository_root
        / legacy_automation.SCHEMA_ROOT.relative_to(legacy_automation.REPOSITORY_ROOT)
        / "audit-output.schema.json"
    )
    legacy_automation.validate_schema(audit, schema, label="audit output")
    return audit, result.stdout
