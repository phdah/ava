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
EXPECTED_TASK_COUNT = 72
PARKED_RELEASE_IDS = {
    "ava-504",
    "ava-505",
    "ava-506",
    "ava-541",
    "ava-542",
    "ava-551",
    "ava-5625",
}
LEGACY_PHASE_PATTERN = re.compile(r"[0-9][0-9]-.*")
TASK_FILENAME_PATTERN = re.compile(r"ava-(\d+(?:\.\d+)?) - .+\.md")


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_inline_list(value: str) -> list[str]:
    inner = value[1:-1].strip()
    if not inner:
        return []
    return [unquote(item) for item in inner.split(",") if item.strip()]


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path}: missing YAML frontmatter")
    try:
        frontmatter, _body = text[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValidationError(f"{path}: unterminated YAML frontmatter") from exc

    lines = frontmatter.splitlines()
    data: dict[str, object] = {}
    index = 0
    while index < len(lines):
        raw_line = lines[index]
        line = raw_line.strip()
        if not line or line.startswith("#") or raw_line[:1].isspace() or ":" not in line:
            index += 1
            continue

        key, raw_value = line.split(":", 1)
        value = raw_value.strip()
        if value.startswith("[") and value.endswith("]"):
            data[key] = parse_inline_list(value)
            index += 1
            continue
        if value:
            data[key] = unquote(value)
            index += 1
            continue

        items: list[str] = []
        lookahead = index + 1
        while lookahead < len(lines):
            candidate = lines[lookahead]
            stripped = candidate.strip()
            if not stripped:
                lookahead += 1
                continue
            if not candidate[:1].isspace():
                break
            if stripped.startswith("- "):
                items.append(unquote(stripped[2:]))
            lookahead += 1
        data[key] = items
        index = lookahead

    return data


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

    legacy_dirs = [
        path.name
        for path in TODO_ROOT.iterdir()
        if path.is_dir() and LEGACY_PHASE_PATTERN.fullmatch(path.name)
    ]
    if legacy_dirs:
        fail(f"legacy phase directories remain after Backlog migration: {legacy_dirs}")
    if (REPO_ROOT / "internal" / "todo.md").exists():
        fail("legacy internal/todo.md remains after Backlog migration")

    tasks: dict[str, dict[str, object]] = {}
    for task_dir in TASK_DIRS:
        if not task_dir.is_dir():
            fail(f"missing Backlog.md directory: {task_dir.relative_to(REPO_ROOT)}")

        for path in sorted(task_dir.glob("*.md")):
            match = TASK_FILENAME_PATTERN.fullmatch(path.name)
            if not match:
                fail(f"{path}: filename is not native Backlog task form for prefix ava")

            data = parse_frontmatter(path)
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
            dependencies = data.get("dependencies", [])
            if not isinstance(labels, list):
                fail(f"{path}: labels must be a list")
            if not isinstance(dependencies, list):
                fail(f"{path}: dependencies must be a list")
            if "legacy-spec" in labels:
                fail(f"{path}: legacy-spec indirection is not allowed after full migration")

            tasks[task_id] = {
                "path": path,
                "status": status,
                "dependencies": dependencies,
            }

    if len(tasks) != EXPECTED_TASK_COUNT:
        fail(f"expected {EXPECTED_TASK_COUNT} migrated tasks, found {len(tasks)}")

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
