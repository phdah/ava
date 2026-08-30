#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from pathlib import Path

TODO_ROOT = Path(__file__).resolve().parent
REPO_ROOT = TODO_ROOT.parents[1]
CONFIG = REPO_ROOT / "backlog.config.yml"
TASK_DIRS = (TODO_ROOT / "tasks", TODO_ROOT / "completed")
ALLOWED_STATUSES = {"To Do", "In Progress", "Parked", "Done"}
PARKED_RELEASE_IDS = {
    "ava-504",
    "ava-505",
    "ava-506",
    "ava-541",
    "ava-542",
    "ava-551",
    "ava-5625",
}
SPEC_EXCLUSIONS = {"index.md", "v1-release-operator-path.md", "finding-template.md"}


class ValidationError(Exception):
    pass


def parse_frontmatter(path: Path) -> tuple[dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValidationError(f"{path}: missing YAML frontmatter")
    try:
        frontmatter, body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValidationError(f"{path}: unterminated YAML frontmatter") from exc

    data: dict[str, object] = {}
    for raw_line in frontmatter.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            items = []
            for item in value[1:-1].split(","):
                item = item.strip().strip("\"'")
                if item:
                    items.append(item)
            data[key] = items
        else:
            data[key] = value.strip("\"'")
    return data, body


def fail(message: str) -> None:
    raise ValidationError(message)


def expected_legacy_specs() -> set[Path]:
    specs: set[Path] = set()
    for phase_dir in sorted(TODO_ROOT.glob("[0-9][0-9]-*")):
        for path in phase_dir.rglob("*.md"):
            if path.name in SPEC_EXCLUSIONS:
                continue
            specs.add(path.resolve())
    return specs


def main() -> int:
    config = CONFIG.read_text(encoding="utf-8")
    required_config = (
        "backlog_directory: internal/todo",
        'task_prefix: "ava"',
        'statuses: ["To Do", "In Progress", "Parked", "Done"]',
        "remote_operations: false",
        "auto_commit: false",
    )
    for entry in required_config:
        if entry not in config:
            fail(f"backlog.config.yml missing required setting: {entry}")

    tasks: dict[str, dict[str, object]] = {}
    referenced_specs: set[Path] = set()

    for task_dir in TASK_DIRS:
        if not task_dir.is_dir():
            fail(f"missing Backlog.md directory: {task_dir.relative_to(REPO_ROOT)}")
        for path in sorted(task_dir.glob("task-*.md")):
            match = re.fullmatch(r"task-(\d+(?:\.\d+)?) - .+\.md", path.name)
            if not match:
                fail(f"{path}: filename is not Backlog.md native task form")

            data, body = parse_frontmatter(path)
            task_id = str(data.get("id", ""))
            expected_id = f"ava-{match.group(1)}"
            if task_id != expected_id:
                fail(f"{path}: id {task_id!r} does not match filename ({expected_id})")
            if task_id in tasks:
                fail(f"duplicate task id: {task_id}")

            title = str(data.get("title", ""))
            status = str(data.get("status", ""))
            if not title:
                fail(f"{path}: missing title")
            if status not in ALLOWED_STATUSES:
                fail(f"{path}: unsupported status {status!r}")
            if task_dir.name == "completed" and status != "Done":
                fail(f"{path}: completed/ may contain only Done tasks")

            labels = data.get("labels", [])
            if not isinstance(labels, list):
                fail(f"{path}: labels must be a list")
            dependencies = data.get("dependencies", [])
            if not isinstance(dependencies, list):
                fail(f"{path}: dependencies must be a list")

            if "legacy-spec" in labels:
                links = re.findall(
                    r"\[Retained specification\]\((\.\./[^)]+\.md)\)",
                    body,
                )
                if len(links) != 1:
                    fail(f"{path}: migrated task must link one retained specification")
                spec = (task_dir / links[0]).resolve()
                try:
                    spec.relative_to(TODO_ROOT.resolve())
                except ValueError:
                    fail(f"{path}: retained specification escapes internal/todo")
                if not spec.is_file():
                    fail(f"{path}: retained specification does not exist: {links[0]}")
                referenced_specs.add(spec)

            tasks[task_id] = {
                "path": path,
                "status": status,
                "dependencies": dependencies,
            }

    if not tasks:
        fail("no Backlog.md tasks found")

    missing_specs = expected_legacy_specs() - referenced_specs
    extra_specs = referenced_specs - expected_legacy_specs()
    if missing_specs:
        formatted = ", ".join(
            str(path.relative_to(TODO_ROOT)) for path in sorted(missing_specs)
        )
        fail(f"legacy task specifications missing Backlog cards: {formatted}")
    if extra_specs:
        formatted = ", ".join(
            str(path.relative_to(TODO_ROOT)) for path in sorted(extra_specs)
        )
        fail(f"Backlog cards reference non-task legacy specs: {formatted}")

    for task_id, task in tasks.items():
        for dependency in task["dependencies"]:
            if dependency not in tasks:
                fail(f"{task_id}: unknown dependency {dependency}")
            if dependency == task_id:
                fail(f"{task_id}: self dependency")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str) -> None:
        if task_id in visiting:
            fail(f"dependency cycle includes {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in tasks[task_id]["dependencies"]:
            visit(str(dependency))
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id)

    required_queue = {
        "ava-601": ("Done", []),
        "ava-602": ("To Do", ["ava-601"]),
        "ava-701": ("To Do", ["ava-602"]),
    }
    for task_id, (status, dependencies) in required_queue.items():
        task = tasks.get(task_id)
        if task is None:
            fail(f"missing roadmap task {task_id}")
        if task["status"] != status:
            fail(f"{task_id}: expected status {status}, got {task['status']}")
        if task["dependencies"] != dependencies:
            fail(
                f"{task_id}: expected dependencies {dependencies}, "
                f"got {task['dependencies']}"
            )

    for task_id in PARKED_RELEASE_IDS:
        task = tasks.get(task_id)
        if task is None:
            fail(f"missing parked release task {task_id}")
        if task["status"] != "Parked":
            fail(f"{task_id}: release work must remain Parked until explicitly resumed")

    print(f"Backlog.md validation passed: {len(tasks)} tasks")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationError as exc:
        print(f"todo validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
