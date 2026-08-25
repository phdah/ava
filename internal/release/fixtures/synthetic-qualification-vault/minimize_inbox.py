#!/usr/bin/env python3
"""Minimize the complete-pending-inbox qualification variant deterministically."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


FORMAT_ORDER = ("md", "txt", "csv", "docx", "pdf", "pptx", "ics")
REQUIRED_DISPOSITIONS = {"mapped", "non-durable", "pending"}
VARIANT_RELATIVE = Path("variants/04-complete-pending-inbox")


class MinimizationError(RuntimeError):
    pass


def canonical_json(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record_dispositions(record: dict[str, Any]) -> set[str]:
    sections = record.get("sections")
    if not isinstance(sections, list):
        raise MinimizationError(f"oracle record has no section inventory: {record.get('path')}")
    dispositions = {
        section.get("disposition")
        for section in sections
        if isinstance(section, dict) and isinstance(section.get("disposition"), str)
    }
    if not dispositions or not dispositions.issubset(REQUIRED_DISPOSITIONS):
        raise MinimizationError(f"oracle record has unsupported dispositions: {record.get('path')}")
    return dispositions


def select_minimum_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    for format_name in FORMAT_ORDER:
        candidates = [record for record in records if record.get("format") == format_name]
        if not candidates:
            raise MinimizationError(f"oracle has no source for required format: {format_name}")
        selected.append(
            min(
                candidates,
                key=lambda record: (
                    -len(record_dispositions(record)),
                    str(record.get("path", "")).encode("utf-8"),
                ),
            )
        )

    observed_formats = {record.get("format") for record in selected}
    observed_dispositions = {
        disposition
        for record in selected
        for disposition in record_dispositions(record)
    }
    if len(selected) != len(FORMAT_ORDER) or observed_formats != set(FORMAT_ORDER):
        raise MinimizationError("selection does not contain exactly one source per required format")
    if observed_dispositions != REQUIRED_DISPOSITIONS:
        raise MinimizationError(
            "minimum format selection does not preserve mapped, non-durable, and pending dispositions"
        )

    names = [Path(str(record["path"])).name for record in selected]
    if len(names) != len(set(names)):
        raise MinimizationError("selected source basenames are not unique after inbox flattening")
    return sorted(selected, key=lambda record: str(record["path"]).encode("utf-8"))


def tree_inventory(root: Path) -> list[dict[str, Any]]:
    return [
        {
            "path": path.relative_to(root).as_posix(),
            "sha256": sha256_file(path),
            "bytes": path.stat().st_size,
        }
        for path in sorted(
            (item for item in root.rglob("*") if item.is_file()),
            key=lambda item: item.relative_to(root).as_posix().encode("utf-8"),
        )
    ]


def minimize(output: Path) -> list[dict[str, Any]]:
    output = output.expanduser().resolve()
    baseline_path = output / "oracle/baseline.json"
    inbox = output / VARIANT_RELATIVE / "project/inbox"
    scenario_path = output / VARIANT_RELATIVE / "scenario.json"
    variants_index_path = output / "variants/index.json"
    for path in (baseline_path, scenario_path, variants_index_path):
        if path.is_symlink() or not path.is_file():
            raise MinimizationError(f"required fixture control file is missing: {path}")
    if inbox.is_symlink() or not inbox.is_dir():
        raise MinimizationError(f"complete-pending-inbox directory is missing: {inbox}")

    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    records = baseline.get("files")
    if not isinstance(records, list) or not all(isinstance(record, dict) for record in records):
        raise MinimizationError("baseline oracle has no valid file inventory")
    selected = select_minimum_records(records)
    selected_names = {Path(str(record["path"])).name for record in selected}

    direct_entries = list(inbox.iterdir())
    if any(entry.is_symlink() or not entry.is_file() for entry in direct_entries):
        raise MinimizationError("complete-pending-inbox must contain only direct regular source files")
    existing_names = {entry.name for entry in direct_entries}
    missing = selected_names - existing_names
    if missing:
        raise MinimizationError(f"selected sources are absent from materialized inbox: {sorted(missing)}")

    selected_by_name = {Path(str(record["path"])).name: record for record in selected}
    for name, record in selected_by_name.items():
        path = inbox / name
        if sha256_file(path) != record.get("sha256"):
            raise MinimizationError(f"materialized source digest differs from oracle: {name}")
    for entry in direct_entries:
        if entry.name not in selected_names:
            entry.unlink()

    selection = {
        "schema_version": 1,
        "strategy": "minimum-format-disposition-cover",
        "minimum_source_count": len(FORMAT_ORDER),
        "required_formats": list(FORMAT_ORDER),
        "required_dispositions": sorted(REQUIRED_DISPOSITIONS),
        "selected_sources": [
            {
                "path": Path(str(record["path"])).name,
                "format": record["format"],
                "dispositions": sorted(record_dispositions(record)),
                "sha256": record["sha256"],
            }
            for record in selected
        ],
    }
    selection_path = output / VARIANT_RELATIVE / "selection.json"
    selection_path.write_text(canonical_json(selection), encoding="utf-8")

    scenario = json.loads(scenario_path.read_text(encoding="utf-8"))
    scenario["purpose"] = (
        "Ingest the exact seven-source representative inbox set preserving every maintained "
        "text/document format and section disposition."
    )
    scenario["operations"] = [
        "install assets",
        "use the deterministic seven-source selection recorded in selection.json",
        "process every selected direct inbox source",
        "reconcile every selected source and section against the oracle",
    ]
    scenario_path.write_text(canonical_json(scenario), encoding="utf-8")

    variants_index = json.loads(variants_index_path.read_text(encoding="utf-8"))
    families = variants_index.get("families")
    if not isinstance(families, list):
        raise MinimizationError("variants/index.json has no family inventory")
    matches = [family for family in families if isinstance(family, dict) and family.get("id") == "complete-pending-inbox"]
    if len(matches) != 1:
        raise MinimizationError("variants/index.json must contain exactly one complete-pending-inbox family")
    matches[0]["inventory"] = tree_inventory(output / VARIANT_RELATIVE)
    variants_index_path.write_text(canonical_json(variants_index), encoding="utf-8")

    remaining = [entry for entry in inbox.iterdir() if entry.is_file()]
    if len(remaining) != len(FORMAT_ORDER) or {entry.name for entry in remaining} != selected_names:
        raise MinimizationError("minimized inbox does not match the recorded seven-source selection")
    return selected


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="generated synthetic qualification vault root")
    args = parser.parse_args(argv)
    try:
        selected = minimize(Path(args.output))
    except (MinimizationError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"qualification inbox minimization error: {exc}", file=__import__("sys").stderr)
        return 1
    formats = ", ".join(record["format"] for record in selected)
    print(f"minimized complete-pending-inbox: {len(selected)} sources ({formats})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
