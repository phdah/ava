#!/usr/bin/env python3
"""Generate and validate the repository-external synthetic qualification vault."""

from __future__ import annotations

import argparse
import calendar
import csv
import hashlib
import io
import json
import platform
import re
import shutil
import struct
import sys
import textwrap
import zipfile
import zlib
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from xml.etree import ElementTree


FIXTURE_ROOT = Path(__file__).resolve().parent
REPOSITORY_ROOT = FIXTURE_ROOT.parents[3]
BLUEPRINT_PATH = FIXTURE_ROOT / "blueprint.json"
LOCK_PATH = FIXTURE_ROOT / "requirements.lock"
PINNED_IMAGES_ROOT = FIXTURE_ROOT / "images"
PINNED_IMAGE_MANIFEST_PATH = PINNED_IMAGES_ROOT / "manifest.json"
SCRIPT_PATH = Path(__file__).resolve()
_BLUEPRINT_CONSTANTS = json.loads(BLUEPRINT_PATH.read_text(encoding="utf-8"))
_INTERVAL_START = date.fromisoformat(_BLUEPRINT_CONSTANTS["interval"]["start"])
FIXED_ZIP_TIME = (_INTERVAL_START.year, _INTERVAL_START.month, _INTERVAL_START.day, 0, 0, 0)
FIXED_DOCUMENT_TIME = f"{_INTERVAL_START.isoformat()}T00:00:00Z"
ALLOWED_OUTPUT_CHILDREN = {"corpus", "image-prompts", "oracle", "variants"}
CORPUS_BATCH_NAMES = ("01-pre-move", "02-move-transition", "03-renovation", "04-settled")
FIXTURE_YEAR = _INTERVAL_START.year
RELEASE_ASSET_NAMES = {"ava-install.sh", "ava-base.tar.gz", "ava-guidance.tar.gz", "ava-migrations.tar.gz", "ava-release.json", "ava-release-notes.md", "SHA256SUMS"}
VARIANT_FAMILIES = {"empty-before-installation", "mature-mixed-project", "registered-private-work-roles", "complete-pending-inbox", "managed-content-damage", "interrupted-upgrade-states", "pending-semantic-reconciliation", "uninstall-reinstallation"}


class FixtureError(RuntimeError):
    pass


def load_blueprint() -> dict:
    return json.loads(BLUEPRINT_PATH.read_text(encoding="utf-8"))


def load_pinned_image_manifest(blueprint: dict) -> dict:
    manifest = json.loads(PINNED_IMAGE_MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("schema_version") != 1 or manifest.get("fixture_id") != blueprint["fixture_id"]:
        raise FixtureError("pinned image manifest identity is invalid")
    images = manifest.get("images")
    if not isinstance(images, list) or len(images) != blueprint["counts"]["external_images"]:
        raise FixtureError("pinned image manifest must contain exactly five images")
    expected_keys = {"file", "destination", "sha256", "bytes", "media_type", "width", "height"}
    expected_destinations = {slot["path"] for slot in blueprint["image_slots"]}
    if {item.get("destination") for item in images if isinstance(item, dict)} != expected_destinations:
        raise FixtureError("pinned image destinations differ from the blueprint")
    if {path.name for path in PINNED_IMAGES_ROOT.glob("*.png")} != {item.get("file") for item in images if isinstance(item, dict)}:
        raise FixtureError("pinned image file inventory differs from the manifest")
    for item in images:
        if not isinstance(item, dict) or set(item) != expected_keys:
            raise FixtureError(f"pinned image entry must contain exactly {sorted(expected_keys)}")
        source = PINNED_IMAGES_ROOT / item["file"]
        if source.is_symlink() or not source.is_file() or source.parent != PINNED_IMAGES_ROOT:
            raise FixtureError(f"pinned image must be a direct regular file: {source}")
        if not re.fullmatch(r"[0-9a-f]{64}", item["sha256"]):
            raise FixtureError(f"pinned image has invalid SHA-256: {source}")
        if sha256_file(source) != item["sha256"] or source.stat().st_size != item["bytes"]:
            raise FixtureError(f"pinned image digest or size mismatch: {source}")
        if image_type(source, "png") != item["media_type"]:
            raise FixtureError(f"pinned image media type mismatch: {source}")
        width, height = struct.unpack(">II", source.read_bytes()[16:24])
        if width != item["width"] or height != item["height"]:
            raise FixtureError(f"pinned image dimensions mismatch: {source}")
    return manifest


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def generator_revision() -> str:
    digest = hashlib.sha256()
    inputs = [SCRIPT_PATH, BLUEPRINT_PATH, LOCK_PATH, FIXTURE_ROOT / "oracle.schema.json", FIXTURE_ROOT / "run-manifest.schema.json", PINNED_IMAGE_MANIFEST_PATH]
    inputs.extend(sorted(PINNED_IMAGES_ROOT.glob("*.png"), key=lambda path: path.name.encode("utf-8")))
    for path in inputs:
        digest.update(path.name.encode("ascii"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def resolved_output(value: str) -> Path:
    path = Path(value).expanduser().resolve()
    repository = REPOSITORY_ROOT.resolve()
    if path == repository or path.is_relative_to(repository):
        raise FixtureError(f"output must be outside the Ava repository: {path}")
    return path


def require_clean_output(path: Path) -> None:
    if path.exists() and (not path.is_dir() or any(path.iterdir())):
        raise FixtureError(f"output must be a new or empty directory: {path}")
    path.mkdir(parents=True, exist_ok=True)


def parse_date(value: str) -> date:
    return date.fromisoformat(value)


def require_supported_runtime() -> None:
    if platform.python_implementation() != "CPython" or sys.version_info < (3, 11):
        raise FixtureError("fixture requires CPython 3.11 or newer")


def corpus_batch(source_date: date) -> str:
    if source_date < date(2025, 2, 15):
        return "01-pre-move"
    if source_date < date(2025, 3, 3):
        return "02-move-transition"
    if source_date < date(2025, 4, 1):
        return "03-renovation"
    return "04-settled"


def month_dates(month: int, count: int) -> list[date]:
    days = calendar.monthrange(FIXTURE_YEAR, month)[1]
    if count == 1:
        return [date(FIXTURE_YEAR, month, 15)]
    return [date(FIXTURE_YEAR, month, 2 + (index * (days - 3) // (count - 1))) for index in range(count)]


def diary_dates(seed: int) -> list[date]:
    selected: list[date] = []
    anchors = {
        1: {1, 18, 24},
        2: {15, 22, 27},
        3: {3, 12, 21, 28},
        4: {5, 19, 30},
        5: {6, 17, 29},
        6: {14, 20, 30},
    }
    for month in range(1, 7):
        days = list(range(1, calendar.monthrange(FIXTURE_YEAR, month)[1] + 1))
        required = anchors[month]
        remaining = [day for day in days if day not in required]
        ranked = sorted(
            remaining,
            key=lambda day: hashlib.sha256(f"{seed}:{month}:{day}".encode("ascii")).digest(),
        )
        chosen = sorted(required | set(ranked[: 25 - len(required)]))
        selected.extend(date(FIXTURE_YEAR, month, day) for day in chosen)
    return selected


def current_address(blueprint: dict, source_date: date) -> str:
    transition = parse_date(blueprint["move"]["completed"])
    key = "new" if source_date >= transition else "old"
    return blueprint["addresses"][key]["value"]


def current_home_state(blueprint: dict, source_date: date) -> str:
    move = parse_date(blueprint["move"]["completed"])
    renovation_start = parse_date(blueprint["renovation"]["started"])
    renovation_end = parse_date(blueprint["renovation"]["completed"])
    if source_date < move:
        return "living at the old apartment while preparing the move"
    if source_date < renovation_start:
        return "unpacking at the new apartment before renovation starts"
    if source_date < renovation_end:
        return "living at the new apartment with the kitchen renovation active"
    return "settled at the new apartment with the renovated kitchen complete"


def month_arc(blueprint: dict, source_date: date) -> str:
    return blueprint["monthly_arcs"][f"{source_date.month:02d}"]


def transition_by_id(blueprint: dict, transition_id: str) -> dict:
    return next(item for item in blueprint["transitions"] if item["id"] == transition_id)


def source_record(
    path: str,
    source_date: date,
    extension: str,
    structural_class: str,
    domain: str,
    durable_subjects: list[str],
    non_durable: list[str],
    sections: list[dict],
    claims: list[dict],
    source_text: str,
    duplicates: list[str] | None = None,
) -> dict:
    if domain == "work":
        destination_scope = "work"
    elif domain == "private":
        destination_scope = "private"
    else:
        destination_scope = "shared"
    qualified_sections = []
    for item in sections:
        disposition = item["disposition"]
        if structural_class == "diary" and item["locator"] == "Home and Uno":
            destinations = ["knowledge/private/residence.md", "knowledge/private/uno.md"]
        elif structural_class == "diary" and item["locator"] == "Work":
            destinations = ["knowledge/work/projects.md"]
        elif structural_class == "diary" and item["locator"] == "Running, reading, and cooking":
            destinations = ["knowledge/private/running.md", "knowledge/private/reading.md", "knowledge/private/cooking.md"]
        elif structural_class == "household-finance" and item["locator"] == "Transactions and warranty rows except shared headset":
            destinations = ["knowledge/private/household-finance.md"]
        else:
            destinations = [f"knowledge/{destination_scope}/{structural_class}.md"]
        qualified_sections.append({
            **item,
            "destinations": destinations if disposition == "mapped" else [],
            "attribution_required": disposition == "mapped" and any(
                value["attribution"] != load_blueprint()["identity"]["full_name"]
                or value["certainty"] != "certain"
                or value["decision_status"] != "fact"
                for value in claims
            ),
            "blocker": item.get("blocker") if disposition == "pending" else None,
        })
    source_lines = [line.strip() for line in source_text.splitlines() if line.strip()]
    for value in claims:
        if value.get("source_excerpt"):
            if value["source_excerpt"] not in source_lines:
                raise FixtureError(f"explicit claim support is absent from {path}: {value['source_excerpt']}")
            continue
        claim_words = set(re.findall(r"[a-z0-9]+", value["text"].lower()))
        supporting_line = max(
            source_lines,
            key=lambda line: len(claim_words & set(re.findall(r"[a-z0-9]+", line.lower()))),
        )
        if not claim_words & set(re.findall(r"[a-z0-9]+", supporting_line.lower())):
            raise FixtureError(f"claim has no source support in {path}: {value['text']}")
        value["source_excerpt"] = supporting_line
    return {
        "path": f"corpus/{corpus_batch(source_date)}/{path}",
        "date": source_date.isoformat(),
        "month": source_date.strftime("%Y-%m"),
        "format": extension,
        "class": structural_class,
        "domain": domain,
        "durable_subjects": durable_subjects,
        "non_durable": non_durable,
        "sections": qualified_sections,
        "claims": claims,
        "duplicates": duplicates or [],
    }


def claim(text: str, source_date: date, *, certainty: str = "certain", attribution: str | None = None, status: str = "fact", source_excerpt: str | None = None) -> dict:
    value = {
        "text": text,
        "date": source_date.isoformat(),
        "certainty": certainty,
        "attribution": attribution or load_blueprint()["identity"]["full_name"],
        "decision_status": status,
    }
    if source_excerpt:
        value["source_excerpt"] = source_excerpt
    return value


def section(locator: str, disposition: str, expected: str, *, blocker: str | None = None) -> dict:
    if disposition == "pending" and not blocker:
        raise FixtureError(f"pending section requires an explicit blocker: {locator}")
    return {"locator": locator, "disposition": disposition, "expected": expected, "blocker": blocker}


def diary_source(blueprint: dict, source_date: date, index: int) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    identity = blueprint["identity"]
    dog = blueprint["dog"]
    work = blueprint["work"]
    running = blueprint["running"]
    reading = blueprint["reading"]
    cooking = blueprint["cooking"]
    month_books = [book for book in reading["books"] if source_date.month in book["months"]]
    active_books = [book for book in month_books if source_date <= parse_date(book["completed"])]
    book = (active_books or month_books)[index % len(active_books or month_books)]
    if source_date < parse_date(book["completed"]):
        reading_state = f"continued {book['title']} by {book['author']}"
    elif source_date == parse_date(book["completed"]):
        reading_state = f"finished {book['title']} by {book['author']} today"
    else:
        reading_state = f"looked back on the completed {book['title']} by {book['author']}"
    route = running["routes"][(index + source_date.month) % len(running["routes"])]
    project_key = "aurora" if (index + source_date.month) % 2 == 0 else "harbor"
    project = work["projects"][project_key]
    address = current_address(blueprint, source_date)
    home_state = current_home_state(blueprint, source_date)
    commute = transition_by_id(blueprint, "commute-change")
    commute_value = commute["to"] if source_date >= parse_date(commute["effective"]) else commute["from"]
    observation = (
        f"{dog['name']} seemed a little stiff after the evening walk, but this is only an observation and not a diagnosis."
        if index % 17 == 0
        else f"{dog['name']} ate {dog['food']} on schedule and settled after the longest walk."
    )
    work_note = (
        f"{work['manager']} suggested moving the {project} checkpoint earlier; that remains her proposal until the team records a decision."
        if index % 13 == 0
        else f"Work on the {project} stayed within the current milestone and I recorded the next operational follow-up."
    )
    detail_variations = [
        "A short entry today because the evening routine ran late.",
        "I compared the day with last week's rhythm and noticed that the home transition affected time more than motivation.",
        "I wrote a longer reflection: keeping work decisions, private plans, and uncertain observations separate made the next action clearer without pretending every passing thought was durable knowledge.",
        "Only the dated state and explicit decisions should survive beyond this diary texture.",
    ]
    content = (
        f"# Diary - {source_date.isoformat()}\n\n"
        f"Monthly context: {month_arc(blueprint, source_date)}\n\n"
        f"## Home and Uno\n\n"
        f"I am {home_state}. Today's current home address is {address}. Current commute: {commute_value}. {observation} "
        f"The ordinary routine remains {dog['routine']}, with meals at {dog['feeding']}.\n\n"
        f"## Work\n\n"
        f"I worked as {work['role']} at {work['employer']}. {work_note} "
        f"The useful durable context is the project state, not the order in which I answered messages.\n\n"
        f"## Running, reading, and cooking\n\n"
        f"The current running thread used the {route}; recovery was {running['recovery'][index % len(running['recovery'])]}. "
        f"I {reading_state} and wrote a personal reflection rather than a scholarly claim. "
        f"Pizza practice still starts from {cooking['baseline_dough']} using {cooking['flour']}.\n\n"
        f"## Passing detail\n\n"
        f"The day's small detail was variation {index % 9 + 1}: laundry timing, a delayed tram, a short call, or a changed grocery order. "
        f"It explains the diary rhythm but does not need durable promotion. {detail_variations[index % len(detail_variations)]}\n"
    )
    claims = [
        claim(f"Current home address was {address}", source_date),
        claim(f"{identity['first_name']} worked on {project}", source_date),
    ]
    if index % 17 == 0:
        claims.append(claim(f"{dog['name']} seemed stiff after a walk", source_date, certainty="uncertain", status="observation"))
    if index % 13 == 0:
        claims.append(claim(f"Move the {project} checkpoint earlier", source_date, attribution=work["manager"], status="proposal"))
    return (
        content,
        [
            section("Home and Uno", "mapped", "Preserve dated residence state and recurring Uno care; preserve uncertain health wording when present."),
            section("Work", "mapped", "Route work project state separately and preserve attributed proposals as proposals."),
            section("Running, reading, and cooking", "mapped", "Update recurring private subject histories without treating personal reflection as external fact."),
            section("Passing detail", "non-durable", "Retain in the source but do not promote routine diary texture."),
        ],
        claims,
        [f"{identity['first_name']} residence timeline", "Uno care", project, "running", "classic literature", "Neapolitan pizza"],
        ["message order", "transit delay", "laundry timing"],
    )


def todo_source(blueprint: dict, source_date: date, index: int, work_domain: bool) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    if work_domain:
        work = blueprint["work"]
        task_events = blueprint["task_events"]
        project_key = "aurora" if index % 2 == 0 else "harbor"
        project = work["projects"][project_key]
        owner = work["colleagues"][index % len(work["colleagues"])]
        title = "Work priorities"
        milestone_date = task_events[f"{project_key}_milestone_completed"]
        milestone_done = source_date >= parse_date(milestone_date)
        milestone_state = f"Completed on {milestone_date}" if milestone_done else "Carry over"
        incident_done = source_date >= parse_date(task_events["incident_followup_completed"])
        incident_state = f"Closed after review on {task_events['incident_followup_completed']}" if incident_done else "Carry over without claiming a root cause"
        lines = [
            f"- [{'x' if milestone_done else ' '}] W-{project_key.upper()}-01: {milestone_state} the reviewed milestone for {project} with {owner}",
            f"- [{'x' if incident_done else ' '}] W-INC-02: {incident_state} for the retry-spike follow-up",
            f"- [ ] W-OPS-03: Prepare evidence for {work['recurring'][index % len(work['recurring'])]}",
            "- [x] W-MTG-04: Cancel duplicate status meeting after the written update was accepted",
            "- [ ] W-CLEAN-05: Reprioritized behind the integration deadline; no completion claimed",
        ]
        subjects = [project, owner, "work priority history"]
        domain = "work"
    else:
        dog = blueprint["dog"]
        task_events = blueprint["task_events"]
        title = "Personal priorities"
        address_done = source_date >= parse_date(task_events["address_receipt_completed"])
        race_done = source_date >= parse_date(blueprint["running"]["race_date"])
        warranty_created = source_date >= parse_date(blueprint["renovation"]["completed"])
        warranty_done = source_date >= parse_date(task_events["kitchen_warranty_completed"])
        address_state = f"Address-change receipt confirmed {task_events['address_receipt_completed']}" if address_done else "Carry packing and address-change evidence forward"
        warranty_state = f"Warranty inventory completed {task_events['kitchen_warranty_completed']}" if warranty_done else ("Create and carry the warranty inventory" if warranty_created else "Not created until renovation completion")
        lines = [
            f"- [x] P-UNO-01: Bought the current bag of {dog['food']}; this recurring purchase will be created again when needed",
            f"- [{'x' if address_done else ' '}] P-MOVE-02: {address_state}",
            f"- [{'x' if race_done else ' '}] P-RUN-03: {'Race completed; switch to recovery' if race_done else 'Continue the half-marathon training block'}",
            f"- [{'x' if warranty_done else ' '}] P-KITCHEN-04: {warranty_state}",
            "- [x] P-DUP-05: Cancelled duplicate household reminder",
            "- [ ] P-CUPBOARD-06: Optional cupboard organization reprioritized behind move or recovery work",
        ]
        subjects = ["personal task history", "Uno care", "move follow-up"]
        domain = "private"
    content = f"# {title} - {source_date.isoformat()}\n\n" + "\n".join(lines) + "\n\nNotes: checked items are completed; unchecked items remain pending unless a later list cancels or supersedes them.\n"
    claims = [claim(f"Todo list recorded for {title.lower()}", source_date, status="observation")]
    sections = [
        section("Checklist", "mapped", "Preserve stable task IDs with their creation, carry-over, completion, cancellation, and reprioritization chronology."),
        section("Notes", "non-durable", "Use as interpretation guidance, not a new task."),
    ]
    return content, sections, claims, subjects, ["list ordering"]


def running_source(blueprint: dict, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    running = blueprint["running"]
    route = running["routes"][index % len(running["routes"])]
    distance = 7 + (index * 3 % 18)
    minutes = distance * 5 + 3 + index % 7
    shoe = running["shoes"][index % len(running["shoes"])]
    race_date = parse_date(running["race_date"])
    if source_date < race_date:
        training_purpose = f"build toward {running['race']} on {running['race_date']} without turning every long run into a race"
    elif source_date == race_date:
        training_purpose = f"complete {running['race']}; recorded finish time {running['race_finish_time']}"
    else:
        training_purpose = f"recover from {running['race']} and rebuild ordinary mileage after the {running['race_finish_time']} finish"
    if extension == "csv":
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["date", "route", "distance_km", "duration_minutes", "shoes", "effort", "recovery"])
        for offset in range(4):
            day = source_date + timedelta(days=offset)
            writer.writerow([day.isoformat(), route, f"{distance + offset * 0.5:.1f}", minutes + offset * 3, shoe, "easy" if offset < 2 else "steady", running["recovery"][(index + offset) % len(running["recovery"])]])
        content = buffer.getvalue()
        locator = "CSV rows"
    else:
        content = (
            f"# Run log - {source_date.isoformat()}\n\n"
            f"Route: {route}\n\nDistance: {distance} km\n\nTime: {minutes} minutes\n\nShoes: {shoe}\n\n"
            f"Training purpose: {training_purpose}.\n\n"
            f"Recovery: {running['recovery'][index % len(running['recovery'])]}. The pace felt {'controlled' if index % 5 else 'heavier than expected'}, which is a subjective observation.\n"
        )
        locator = "Run log fields"
    return (
        content,
        [section(locator, "mapped", "Update dated route, distance, equipment, subjective effort, and recovery history.")],
        [claim(f"Ran {distance} km on {route} using {shoe}", source_date)],
        ["running training", route, shoe, running["race"]],
        ["momentary weather impression"],
    )


def reading_source(blueprint: dict, source_date: date, index: int) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    books = blueprint["reading"]["books"]
    first_name = blueprint["identity"]["first_name"]
    candidates = [book for book in books if source_date.month in book["months"]]
    completing = [book for book in candidates if parse_date(book["completed"]) == source_date]
    book = (completing or candidates)[index % len(completing or candidates)]
    pages = 35 + (index * 17 % 310)
    completed = source_date >= parse_date(book["completed"])
    progress = f"Completed on {book['completed']}" if completed else f"In progress at page {pages}"
    content = (
        f"# Reading notes - {book['title']}\n\nDate: {source_date.isoformat()}\n\nAuthor: {book['author']}\n\n"
        f"Progress: {progress}.\n\n"
        f"## Personal reflection\n\nThe tension between duty and chosen loyalty felt more interesting today than the plot mechanics. This is {first_name}'s interpretation, not a claim about authorial intent.\n\n"
        f"## Copied quotation\n\n\"{book['quotation']}\" - copied into {first_name}'s personal reading note and attributed to {book['author']}.\n\n"
        "## Passage reminder\n\nReturn to the marked library-copy passage about memory before writing the next reflection.\n"
    )
    return (
        content,
        [section("Progress", "mapped", "Update dated reading progress and completion state."), section("Personal reflection", "mapped", f"Attribute the interpretation to {first_name}."), section("Copied quotation", "mapped", "Preserve the copied quotation and its named author attribution."), section("Passage reminder", "non-durable", "Keep the reminder in source only.")],
        [claim(f"Reading state for {book['title']}: {progress}", source_date, source_excerpt=f"Progress: {progress}."), claim("Duty and chosen loyalty were the most interesting theme today", source_date, status="observation", source_excerpt=f"The tension between duty and chosen loyalty felt more interesting today than the plot mechanics. This is {first_name}'s interpretation, not a claim about authorial intent."), claim(book["quotation"], source_date, attribution=book["author"], status="observation", source_excerpt=f"\"{book['quotation']}\" - copied into {first_name}'s personal reading note and attributed to {book['author']}.")],
        [book["title"], "classic literature reading history"],
        ["return-to-passage reminder"],
    )


def cooking_source(blueprint: dict, source_date: date, index: int) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    cooking = blueprint["cooking"]
    renovation_start = parse_date(blueprint["renovation"]["started"])
    renovation_end = parse_date(blueprint["renovation"]["completed"])
    hydration = [60, 62, 64, 65][index % 4]
    hours = [18, 24, 36, 48][index % 4]
    if renovation_start <= source_date < renovation_end:
        outcome = "No pizza bake because the renovation left only the temporary induction plate; mixed a small dough solely to compare fermentation texture."
    else:
        outcome = f"Baked in the {cooking['oven']} with the stone position at level {index % 3 + 1}; rim color was even and the center held together."
    content = (
        f"# Neapolitan pizza experiment - {source_date.isoformat()}\n\n"
        f"Flour: {cooking['flour']}\n\nTomatoes: {cooking['tomatoes']}\n\nHydration: {hydration}%\n\nSalt: 2.8%\n\nFermentation: {hours} hours cold\n\n"
        f"Experiment: {cooking['experiments'][index % len(cooking['experiments'])]}.\n\nOutcome: {outcome}\n\n"
        "Next time: change only one variable so the comparison remains useful. This intention is not a completed recipe decision.\n"
    )
    return (
        content,
        [section("Formula", "mapped", "Record dated dough variables and ingredients."), section("Outcome", "mapped", "Preserve the renovation cooking constraint when active."), section("Next time", "non-durable", "Keep the uncommitted one-session reminder only in the source; the proposal remains attributable without blocking ingestion.")],
        [claim(f"Pizza experiment used {hydration}% hydration and {hours}-hour cold fermentation", source_date), claim("Change only one variable next time", source_date, status="proposal")],
        ["Neapolitan pizza experiments", cooking["oven"], cooking["flour"]],
        ["next-session reminder"],
    )


def dog_source(blueprint: dict, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    dog = blueprint["dog"]
    identity = blueprint["identity"]
    neighbor = blueprint["relationships"]["neighbor"]
    vet_visit = index in {3, 9}
    health = f"Routine visit at {dog['vet']}; weight 8.1 kg and no treatment change." if vet_visit else "No confirmed health change; ordinary appetite and energy."
    care_note = f"{neighbor} handled the evening walk while {identity['first_name']} was at a work event." if index % 4 == 0 else f"{identity['first_name']} handled all three walks."
    prefix = "Uno care record" if extension == "txt" else "# Uno care record"
    content = (
        f"{prefix} - {source_date.isoformat()}\n\n"
        f"Dog: {dog['name']}, {dog['breed']}, born {dog['birth_date']}\n"
        f"Food: {dog['food']}; {dog['feeding']}\n"
        f"Walks: {dog['routine']}\n"
        f"Health: {health}\n"
        f"Care note: {care_note}\n"
        "Passing note: Uno chose the same window spot after breakfast; this does not need durable promotion.\n"
    )
    return (
        content,
        [section("Care fields", "mapped", "Update recurring feeding, walks, care arrangements, and confirmed vet outcomes."), section("Passing note", "non-durable", "Do not promote incidental behavior.")],
        [claim(f"Uno followed the {dog['food']} feeding routine", source_date), claim(health, source_date, attribution=dog["vet"] if vet_visit else None, status="observation")],
        ["Uno", dog["vet"], dog["food"], "dog care history"],
        ["window spot"],
    )


def housing_source(blueprint: dict, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    move = blueprint["move"]
    old_address = blueprint["addresses"]["old"]["value"]
    new_address = blueprint["addresses"]["new"]["value"]
    completed = parse_date(move["completed"])
    lease_signed = parse_date(move["lease_signed"])
    lease_start = parse_date(move["new_lease_start"])
    key_return = parse_date(move["old_key_return"])
    if source_date < completed:
        status = f"Current residence remains {old_address}. The planned destination is {new_address}; it must not be treated as current before {move['completed']}."
        provider = f"Current providers are {move['electricity_old']} and {move['internet_old']}."
    elif source_date == completed:
        status = f"Move completed today from {old_address} to {new_address}. The new address becomes current on this date."
        provider = f"Provider handoff changes to {move['electricity_new']} and {move['internet_new']}."
    else:
        status = f"Current residence is {new_address}. {old_address} is retained only as the historical pre-move address."
        provider = f"Current providers are {move['electricity_new']} and {move['internet_new']}."
    if source_date < lease_signed:
        lease_history = f"The destination lease is still under review; no signature or start is recorded yet. Planned move date: {move['completed']}."
    elif source_date < lease_start:
        lease_history = f"Lease signed on {move['lease_signed']}; start on {move['new_lease_start']} and move on {move['completed']} remain planned."
    elif source_date < completed:
        lease_history = f"Lease signed on {move['lease_signed']} and started on {move['new_lease_start']}; move on {move['completed']} remains planned."
    elif source_date < key_return:
        lease_history = f"Lease signed {move['lease_signed']}, started {move['new_lease_start']}, and move completed {move['completed']}; old keys remain due {move['old_key_return']}."
    else:
        lease_history = f"Lease signed {move['lease_signed']}, started {move['new_lease_start']}, move completed {move['completed']}, and old keys returned {move['old_key_return']}."
    heading = "# Housing and move record" if extension == "md" else "Housing and move record"
    content = (
        f"{heading} - {source_date.isoformat()}\n\n"
        f"{status}\n\n{provider}\n\n"
        f"Mover: {move['mover']}. {lease_history}\n\n"
        f"Record {index + 1}: {'packing and quote comparison' if source_date < completed else 'address update and unpacking follow-up'}. "
        "A quoted option is not an accepted purchase unless a later source marks it accepted.\n"
    )
    if extension == "csv":
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["date", "category", "details", "status", "amount_sek", "provider"])
        writer.writerow([source_date.isoformat(), "residence", status, "dated state", 0, blueprint["identity"]["first_name"]])
        writer.writerow([source_date.isoformat(), "lease", lease_history, "dated state", 0, move["mover"]])
        writer.writerow([source_date.isoformat(), "providers", provider, "dated state", 499, move["internet_new"] if source_date >= completed else move["internet_old"]])
        writer.writerow([source_date.isoformat(), "moving quote", "reviewed option, not accepted purchase", "reviewed", 8200 + index * 150, move["mover"]])
        writer.writerow([source_date.isoformat(), "address update", "postal address change", "planned" if source_date < completed else "completed", 0, blueprint["providers"]["postal"]])
        content = buffer.getvalue()
    return (
        content,
        [section("Residence state", "mapped", "Preserve old and new address validity dates and supersession."), section("Provider state", "mapped", "Preserve dated provider transition."), section("Quoted option", "mapped", "Preserve the reviewed option as a proposal and do not turn it into an accepted purchase.")],
        [claim(status, source_date), claim(provider, source_date), claim("A moving or supply option was reviewed", source_date, status="proposal")],
        ["apartment move", old_address, new_address, "provider transitions"],
        ["packing order"],
    )


def renovation_source(blueprint: dict, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    renovation = blueprint["renovation"]
    first_name = blueprint["identity"]["first_name"]
    planned = parse_date(renovation["planned"])
    start = parse_date(renovation["started"])
    end = parse_date(renovation["completed"])
    approval = parse_date(renovation["materials_approved"])
    if source_date < planned:
        state = "Preliminary kitchen notes only. No contractor, supplier, budget, material, or start date has been approved."
        parties = "Contractor: not selected\nSupplier: not selected"
        budget = "Budget: not approved"
        materials = "Materials: options not yet selected"
        status = "observation"
    elif source_date < start:
        state = f"Planning only. Work is scheduled to start {renovation['started']}."
        parties = f"Contractor: {renovation['contractor']}\nSupplier: {renovation['supplier']}"
        budget = f"Budget: SEK {renovation['budget_sek']}"
        materials = f"Approved materials: {renovation['worktop']} worktop and {renovation['cabinet_color']} cabinets" if source_date >= approval else f"Materials under review: {renovation['worktop']} worktop and {renovation['cabinet_color']} cabinets"
        status = "proposal"
    elif source_date < end:
        delay = f" {renovation['delay']}." if source_date >= parse_date(renovation["delay_announced"]) else " No delivery delay has been recorded yet."
        state = f"Renovation active with {renovation['contractor']}.{delay}"
        parties = f"Contractor: {renovation['contractor']}\nSupplier: {renovation['supplier']}"
        budget = f"Budget: SEK {renovation['budget_sek']}"
        materials = f"Approved materials: {renovation['worktop']} worktop and {renovation['cabinet_color']} cabinets"
        status = "fact"
    else:
        state = f"Renovation completed on {renovation['completed']}; follow-up and warranty tracking remain."
        parties = f"Contractor: {renovation['contractor']}\nSupplier: {renovation['supplier']}"
        budget = f"Budget: SEK {renovation['budget_sek']}"
        materials = f"Installed materials: {renovation['worktop']} worktop and {renovation['cabinet_color']} cabinets"
        status = "fact"
    heading = "# Kitchen renovation record" if extension == "md" else "Kitchen renovation record"
    cost = f"Final cost: SEK {renovation['final_cost_sek']}" if source_date >= end else "Final cost: not yet known"
    if source_date < planned:
        decision_text = "No supplier recommendation or material decision is recorded."
        decision_status = "observation"
        attribution = first_name
    elif source_date < approval:
        decision_text = f"The supplier recommended the material combination; {first_name} had not yet approved it."
        decision_status = "proposal"
        attribution = renovation["supplier"]
    else:
        decision_text = f"{first_name} approved the material combination on {renovation['materials_approved']}."
        decision_status = "decision"
        attribution = blueprint["identity"]["full_name"]
    content = (
        f"{heading} - {source_date.isoformat()}\n\n"
        f"State: {state}\n\n{parties}\n"
        f"{budget}\n{cost}\n"
        f"{materials}.\n\n"
        f"Decision log item {index + 1}: {decision_text}\n"
        "Temporary note: delivery-window text messages are operational detail unless they change the recorded delay.\n"
    )
    return (
        content,
        [section("State", "mapped", "Preserve planning, active, completion, delay, and warranty chronology."), section("Decision log", "mapped", f"Keep supplier recommendation distinct from {first_name}'s later approval."), section("Temporary note", "non-durable", "Do not promote ordinary delivery messages.")],
        [claim(state, source_date, status=status), claim(decision_text, source_date, attribution=attribution, status=decision_status)],
        ["kitchen renovation", "renovation budget"] + ([renovation["contractor"], renovation["supplier"]] if source_date >= planned else []),
        ["delivery-window messages"],
    )


def work_source(blueprint: dict, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    work = blueprint["work"]
    key = "aurora" if index % 2 == 0 else "harbor"
    project = work["projects"][key]
    colleague = work["colleagues"][index % len(work["colleagues"])]
    stakeholder = work["stakeholders"][index % len(work["stakeholders"])]
    decision = work["decisions"][key]
    heading = f"# {project}" if extension == "md" else project
    content = (
        f"{heading} - status record {source_date.isoformat()}\n\n"
        f"Employer: {work['employer']}\nOwner: {blueprint['identity']['full_name']}, {work['role']}\nContributor: {colleague}\nStakeholder: {stakeholder}\n\n"
        f"Decision: {decision}. {blueprint['identity']['first_name']} recorded this after team review; it is not merely a stakeholder suggestion.\n\n"
        f"Operations: review latency, failed synchronization count, alert ownership, and rollback readiness during {work['recurring'][index % len(work['recurring'])]}.\n\n"
        f"Incident note: {'The retry spike may have contributed to delayed updates, but root cause remains uncertain.' if index % 5 == 0 else 'No open incident changed the project plan.'}\n\n"
        "Operational follow-up: carry one measurable action to the next checkpoint and close duplicate reminders.\n\n"
        "Social detail: meeting jokes and lunch details are non-durable.\n"
    )
    claims = [claim(decision, source_date, status="decision")]
    if index % 5 == 0:
        claims.append(claim("Retry spike contributed to delayed updates", source_date, certainty="uncertain", attribution=work["incident_observation_attribution"], status="observation"))
    return (
        content,
        [section("Decision", "mapped", "Record the accepted architecture decision and its source."), section("Operations", "mapped", "Route procedures and operational state to work knowledge."), section("Incident note", "mapped", "Preserve uncertainty and attribution."), section("Operational follow-up", "mapped", "Promote the measurable action and duplicate-reminder cleanup."), section("Social detail", "non-durable", "Omit meeting jokes and lunch details because they do not affect durable work state.")],
        claims,
        [project, work["employer"], colleague, stakeholder, "architecture decisions", "operations"],
        ["meeting jokes", "lunch details"],
    )


def finance_source(blueprint: dict, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    providers = blueprint["providers"]
    move = blueprint["move"]
    rows = [
        ("mobile subscription", 299, providers["mobile"], "recurring"),
        ("home insurance", 189, providers["insurance"], "recurring"),
        ("dog food", 649, blueprint["dog"]["food"], "purchase"),
        ("household maintenance", 420 + index * 35, providers["household_supplier"], "purchase"),
        (f"glasses warranty from {providers['glasses_purchase']} for {providers['glasses_warranty_months']} months", 0, providers["glasses_retailer"], "warranty"),
        ("shared headset expense; personal purchase or work reimbursement not yet determined", 1190, blueprint["work"]["employer"], "classification pending"),
    ]
    if extension == "csv":
        buffer = io.StringIO(newline="")
        writer = csv.writer(buffer, lineterminator="\n")
        writer.writerow(["date", "item", "amount_sek", "provider", "kind"])
        writer.writerow([source_date.isoformat(), f"Transaction count: {len(rows)}", 0, "summary", "summary"])
        for item, amount, provider, kind in rows:
            writer.writerow([source_date.isoformat(), item, amount, provider, kind])
        content = buffer.getvalue()
    else:
        content = f"Household finance record - {source_date.isoformat()}\n\nTransaction count: {len(rows)}\n" + "\n".join(f"{item}: SEK {amount}, {provider}, {kind}" for item, amount, provider, kind in rows)
        content += f"\n\nCurrent internet provider: {move['internet_new'] if source_date >= parse_date(move['completed']) else move['internet_old']}.\nGlasses warranty: purchase at {providers['glasses_retailer']} on {providers['glasses_purchase']}, warranty term {providers['glasses_warranty_months']} months.\nReceipt order is not a budget priority ranking.\n"
    return (
        content,
        [section("Transactions and warranty rows except shared headset", "mapped", "Record recurring subscriptions, purchases, providers, and the source-backed glasses warranty dates; explicitly exclude the separately pending headset row."), section("Shared headset expense row", "pending", f"Do not route the headset expense until {blueprint['identity']['first_name']} decides whether it is personal or reimbursable work equipment.", blocker=f"{blueprint['identity']['first_name']} has not decided whether the shared headset expense is personal or a work reimbursement."), section("Ordering", "non-durable", "Do not infer priority from receipt order.")],
        [claim(f"Transaction count: {len(rows)}", source_date), claim(f"Glasses from {providers['glasses_retailer']} retain a {providers['glasses_warranty_months']}-month warranty from {providers['glasses_purchase']}", source_date), claim("The shared headset expense may be personal or reimbursable work equipment", source_date, certainty="uncertain", status="observation")],
        ["household finances", providers["insurance"], providers["mobile"], providers["glasses_retailer"]],
        ["receipt row order"],
    )


def ics_escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def ics_fold(lines: list[str]) -> str:
    folded = []
    for line in lines:
        remaining = line
        first = True
        while len(remaining.encode("utf-8")) > (75 if first else 74):
            limit = 75 if first else 74
            split = limit
            while len(remaining[:split].encode("utf-8")) > limit:
                split -= 1
            folded.append(("" if first else " ") + remaining[:split])
            remaining = remaining[split:]
            first = False
        folded.append(("" if first else " ") + remaining)
    return "\r\n".join(folded) + "\r\n"


def appointment_source(blueprint: dict, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str]]:
    dog = blueprint["dog"]
    travel = blueprint["travel"]
    if source_date.month == 5:
        event = travel["work_trip"]
        title = f"{blueprint['work']['projects']['harbor']} partner workshop"
        domain = "overlapping"
    elif source_date.month == 6:
        event = travel["private_trip"]
        title = f"{event['destination']} weekend with {dog['name']}"
        domain = "private"
    else:
        event = {"destination": "Stockholm", "start": source_date.isoformat(), "end": source_date.isoformat(), "purpose": "scheduled appointment"}
        title = blueprint["appointments"][index % len(blueprint["appointments"])]
        domain = "private"
    completed = source_date >= parse_date(event["end"])
    event_state = "completed" if completed else "scheduled"
    uno_care = f"{blueprint['identity']['first_name']} travels with {dog['name']}." if source_date.month == 6 else f"Care follows the routine with {dog['vet']} as provider if needed."
    if extension == "ics":
        uid = f"ava-{source_date.strftime('%Y%m%d')}-{index}@example.invalid"
        start = event["start"].replace("-", "")
        end_date = parse_date(event["end"]) + timedelta(days=1)
        content = ics_fold([
            "BEGIN:VCALENDAR",
            "VERSION:2.0",
            "PRODID:-//Ava Synthetic Qualification//EN",
            "CALSCALE:GREGORIAN",
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTAMP:{_INTERVAL_START.strftime('%Y%m%d')}T000000Z",
            f"DTSTART;VALUE=DATE:{start}",
            f"DTEND;VALUE=DATE:{end_date.strftime('%Y%m%d')}",
            f"SUMMARY:{ics_escape(title)}",
            f"DESCRIPTION:{ics_escape(event['purpose'])} in {ics_escape(event['destination'])}\\; state {event_state}\\; fictional fixture event.",
            "END:VEVENT",
            "END:VCALENDAR",
        ])
    else:
        content = (
            f"Appointment and travel record - {source_date.isoformat()}\n\nTitle: {title}\nDestination: {event['destination']}\n"
            f"Start: {event['start']}\nEnd: {event['end']}\nPurpose: {event['purpose']}\nState: {event_state}\n"
            f"Uno care: {uno_care}\n"
            "A tentative packing reminder is not proof that travel occurred; completion follows the dated end-of-trip source.\n"
        )
    return (
        content,
        [section("Event", "mapped", "Record appointment or travel dates, purpose, domain, and completion state."), section("Reminder", "non-durable", "Keep the tentative packing reminder in source only and do not infer completion from it.")],
        [claim(f"{event_state.capitalize()} {title} in {event['destination']}", source_date, status="decision" if not completed else "fact")],
        [title, event["destination"], "appointments and travel"],
        ["packing reminder"],
    )


def text_for_class(blueprint: dict, structural_class: str, source_date: date, index: int, extension: str) -> tuple[str, list[dict], list[dict], list[str], list[str], str]:
    if structural_class == "diary":
        values = diary_source(blueprint, source_date, index)
        domain = "overlapping"
    elif structural_class in {"personal-todo", "work-todo"}:
        values = todo_source(blueprint, source_date, index, structural_class == "work-todo")
        domain = "work" if structural_class == "work-todo" else "private"
    elif structural_class == "running":
        values = running_source(blueprint, source_date, index, extension)
        domain = "private"
    elif structural_class == "reading":
        values = reading_source(blueprint, source_date, index)
        domain = "private"
    elif structural_class == "cooking":
        values = cooking_source(blueprint, source_date, index)
        domain = "private"
    elif structural_class == "dog-care":
        values = dog_source(blueprint, source_date, index, extension)
        domain = "private"
    elif structural_class == "housing-move":
        values = housing_source(blueprint, source_date, index, extension)
        domain = "private"
    elif structural_class == "kitchen-renovation":
        values = renovation_source(blueprint, source_date, index, extension)
        domain = "private"
    elif structural_class == "work-artifact":
        values = work_source(blueprint, source_date, index, extension)
        domain = "work"
    elif structural_class == "household-finance":
        values = finance_source(blueprint, source_date, index, extension)
        domain = "ambiguous"
    elif structural_class == "appointment-travel":
        values = appointment_source(blueprint, source_date, index, extension)
        domain = "overlapping" if source_date.month == 5 else "private"
    else:
        raise FixtureError(f"unsupported structural class: {structural_class}")
    content, sections, claims, subjects, non_durable = values
    return content, sections, claims, subjects, non_durable, domain


def zip_bytes(files: dict[str, bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED, strict_timestamps=True) as archive:
        for name in sorted(files, key=lambda item: item.encode("utf-8")):
            info = zipfile.ZipInfo(name, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_STORED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, files[name])
    return output.getvalue()


def paragraph_xml(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "".join(f'<w:p><w:r><w:t xml:space="preserve">{escape(line)}</w:t></w:r></w:p>' for line in lines)


def docx_bytes(title: str, text: str) -> bytes:
    content_types = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>'''
    rels = b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>'''
    document = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{paragraph_xml(text)}<w:sectPr><w:pgSz w:w="12240" w:h="15840"/></w:sectPr></w:body></w:document>'''.encode("utf-8")
    core = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>{escape(title)}</dc:title><dc:creator>Ava synthetic fixture</dc:creator><cp:lastModifiedBy>Ava synthetic fixture</cp:lastModifiedBy><dcterms:created xsi:type="dcterms:W3CDTF">{FIXED_DOCUMENT_TIME}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{FIXED_DOCUMENT_TIME}</dcterms:modified><cp:revision>1</cp:revision></cp:coreProperties>'''.encode("utf-8")
    return zip_bytes({"[Content_Types].xml": content_types, "_rels/.rels": rels, "docProps/core.xml": core, "word/document.xml": document})


def pptx_bytes(title: str, text: str) -> bytes:
    lines = [line.strip() for line in text.splitlines() if line.strip()][:12]
    runs = "".join(f'<a:p><a:r><a:rPr lang="en-US"/><a:t>{escape(line)}</a:t></a:r><a:endParaRPr lang="en-US"/></a:p>' for line in lines)
    files = {
        "[Content_Types].xml": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/><Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/><Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/><Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/><Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/><Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>''',
        "_rels/.rels": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/></Relationships>''',
        "docProps/core.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>{escape(title)}</dc:title><dc:creator>Ava synthetic fixture</dc:creator><dcterms:created xsi:type="dcterms:W3CDTF">{FIXED_DOCUMENT_TIME}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{FIXED_DOCUMENT_TIME}</dcterms:modified></cp:coreProperties>'''.encode("utf-8"),
        "ppt/presentation.xml": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst><p:sldId id="256" r:id="rId2"/></p:sldIdLst><p:sldSz cx="12192000" cy="6858000"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>''',
        "ppt/_rels/presentation.xml.rels": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>''',
        "ppt/slides/slide1.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:sp><p:nvSpPr><p:cNvPr id="2" name="Status text"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="457200" y="457200"/><a:ext cx="11277600" cy="5943600"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr/><a:lstStyle/>{runs}</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''.encode("utf-8"),
        "ppt/slides/_rels/slide1.xml.rels": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>''',
        "ppt/slideLayouts/slideLayout1.xml": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank"><p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>''',
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>''',
        "ppt/slideMasters/slideMaster1.xml": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/></p:spTree></p:cSld><p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/><p:sldLayoutIdLst><p:sldLayoutId id="1" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>''',
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>''',
        "ppt/theme/theme1.xml": b'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Ava Synthetic"><a:themeElements><a:clrScheme name="Ava"><a:dk1><a:srgbClr val="000000"/></a:dk1><a:lt1><a:srgbClr val="FFFFFF"/></a:lt1><a:dk2><a:srgbClr val="333333"/></a:dk2><a:lt2><a:srgbClr val="EEEEEE"/></a:lt2><a:accent1><a:srgbClr val="245C4A"/></a:accent1><a:accent2><a:srgbClr val="B76E3B"/></a:accent2><a:accent3><a:srgbClr val="557A95"/></a:accent3><a:accent4><a:srgbClr val="806A9B"/></a:accent4><a:accent5><a:srgbClr val="8A7B32"/></a:accent5><a:accent6><a:srgbClr val="A05A6C"/></a:accent6><a:hlink><a:srgbClr val="0000FF"/></a:hlink><a:folHlink><a:srgbClr val="800080"/></a:folHlink></a:clrScheme><a:fontScheme name="Ava"><a:majorFont><a:latin typeface="Arial"/></a:majorFont><a:minorFont><a:latin typeface="Arial"/></a:minorFont></a:fontScheme><a:fmtScheme name="Ava"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>''',
    }
    return zip_bytes(files)


def pdf_bytes(title: str, text: str) -> bytes:
    lines: list[str] = []
    for paragraph in text.splitlines():
        if not paragraph.strip():
            continue
        lines.extend(textwrap.wrap(paragraph.strip(), width=88, replace_whitespace=True) or [""])
    lines = lines[:52]
    commands = ["BT", "/F1 9 Tf", "50 790 Td", "11 TL"]
    for index, line in enumerate(lines):
        safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        if index:
            commands.append("T*")
        commands.append(f"({safe}) Tj")
    commands.append("ET")
    stream = ("\n".join(commands) + "\n").encode("ascii", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        f"<< /Length {len(stream)} >>\nstream\n".encode("ascii") + stream + b"endstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Title ({title}) /Author (Ava synthetic fixture) /CreationDate (D:{_INTERVAL_START.strftime('%Y%m%d')}000000Z) /ModDate (D:{_INTERVAL_START.strftime('%Y%m%d')}000000Z) >>".encode("ascii", errors="replace"),
    ]
    output = io.BytesIO()
    output.write(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, value in enumerate(objects, 1):
        offsets.append(output.tell())
        output.write(f"{number} 0 obj\n".encode("ascii"))
        output.write(value)
        output.write(b"\nendobj\n")
    xref = output.tell()
    output.write(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.write(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        output.write(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.write(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 6 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii"))
    return output.getvalue()


def encode_source(extension: str, title: str, content: str) -> bytes:
    if extension == "docx":
        return docx_bytes(title, content)
    if extension == "pptx":
        return pptx_bytes(title, content)
    if extension == "pdf":
        return pdf_bytes(title, content)
    newline = "" if extension == "ics" else None
    value = content if newline == "" else content.replace("\r\n", "\n")
    return value.encode("utf-8")


def inventory_plan(blueprint: dict) -> list[tuple[str, date, str]]:
    plan: list[tuple[str, date, str]] = []
    plan.extend(("diary", day, "md") for day in diary_dates(blueprint["seed"]))
    for structural_class in ("personal-todo", "work-todo"):
        for month in range(1, 7):
            plan.extend((structural_class, day, "md") for day in month_dates(month, 2))
    for month in range(1, 7):
        running_dates = month_dates(month, 4)
        if month == 5:
            running_dates[2] = parse_date(blueprint["running"]["race_date"])
        for index, day in enumerate(running_dates):
            plan.append(("running", day, "csv" if index == 0 else "md"))
    for month in range(1, 7):
        reading_dates = month_dates(month, 2)
        completion_dates = [parse_date(book["completed"]) for book in blueprint["reading"]["books"] if parse_date(book["completed"]).month == month]
        if completion_dates:
            reading_dates[-1] = completion_dates[0]
        plan.extend(("reading", day, "md") for day in reading_dates)
        plan.extend(("cooking", day, "md") for day in month_dates(month, 3))
    for month in range(1, 7):
        for index, day in enumerate(month_dates(month, 2)):
            plan.append(("dog-care", day, "txt" if index == 0 else "md"))
    housing_month_counts = [5, 7, 3, 1, 1, 1]
    housing_formats = ["md"] * 10 + ["docx"] * 2 + ["pdf"] * 2 + ["txt"] * 2 + ["csv"] * 2
    housing_dates = [day for month, count in enumerate(housing_month_counts, 1) for day in month_dates(month, count)]
    plan.extend(("housing-move", day, extension) for day, extension in zip(housing_dates, housing_formats, strict=True))
    renovation_dates = [*month_dates(2, 2), *month_dates(3, 8), *month_dates(4, 2)]
    renovation_formats = ["md"] * 8 + ["docx"] * 2 + ["pdf"] * 2
    plan.extend(("kitchen-renovation", day, extension) for day, extension in zip(renovation_dates, renovation_formats, strict=True))
    work_formats = ["md"] * 8 + ["docx"] * 3 + ["pdf"] * 3 + ["pptx"] * 2 + ["txt"] * 2
    work_dates = [day for month in range(1, 7) for day in month_dates(month, 3)]
    plan.extend(("work-artifact", day, extension) for day, extension in zip(work_dates, work_formats, strict=True))
    finance_formats = ["csv", "pdf", "txt", "csv", "pdf", "txt"]
    appointment_formats = ["ics", "txt", "ics", "txt", "ics", "txt"]
    for month in range(1, 7):
        plan.append(("household-finance", month_dates(month, 1)[0], finance_formats[month - 1]))
        plan.append(("appointment-travel", month_dates(month, 1)[0], appointment_formats[month - 1]))
    return plan


def prompt_content(blueprint: dict, slot: dict, prompt_number: int) -> tuple[str, list[str], list[str]]:
    identity = blueprint["identity"]
    dog = blueprint["dog"]
    work = blueprint["work"]
    renovation = blueprint["renovation"]
    destination = slot["path"]
    if "uno" in destination:
        scene = f"A candid winter photograph of {dog['name']}, a salt-and-pepper {dog['breed']}, wearing a plain red harness on a snowy Stockholm footpath."
        required = [dog["name"], dog["breed"], "winter setting", "no readable private data"]
        forbidden = ["real address", "microchip number", "other named person", "brand logo"]
        durable = [f"{dog['name']} is {identity['first_name']}'s {dog['breed']}", "winter walk routine"]
    elif "moving-boxes" in destination:
        box_label = f"{identity['first_name'].upper()} - KITCHEN - {blueprint['addresses']['new']['value'].upper()}"
        scene = f"Documentary photograph of apartment moving boxes on {slot['date']}, with one clearly legible label reading {box_label} and a small invoice card naming {blueprint['move']['mover']}."
        required = [blueprint["move"]["mover"], blueprint["addresses"]["new"]["value"], slot["date"], "moving boxes"]
        forbidden = [blueprint["addresses"]["old"]["value"], "real phone number", "barcode", "credential"]
        durable = ["move completed on February 22", "new apartment destination", "mover identity"]
    elif "receipt" in destination:
        scene = f"Top-down photograph of a fictional receipt from {renovation['supplier']}, dated {slot['date']}, showing LIGHT GRAY COMPOSITE SAMPLE SEK 1,200 and MATTE SAGE PANEL SEK 850, total SEK 2,050, paid by {blueprint['providers']['test_card_label']}."
        required = [renovation["supplier"], slot["date"], "SEK 2,050", renovation["worktop"], renovation["cabinet_color"], blueprint["providers"]["test_card_label"]]
        forbidden = ["real card number", "QR code", "usable barcode", "real tax identifier", "cashier identity"]
        durable = ["kitchen material purchase", "supplier", "purchase date and total", "selected materials"]
    elif "settled-kitchen" in destination:
        scene = f"Natural daylight photograph of a completed compact Stockholm kitchen with {renovation['cabinet_color']} cabinets and a {renovation['worktop']} worktop, clean but lived in, with a pizza peel visible."
        required = [renovation["cabinet_color"], renovation["worktop"], "pizza peel", "completed state"]
        forbidden = ["person", "address label", "unfinished construction", "luxury showroom styling"]
        durable = ["renovation completed", "material choices", "pizza equipment in settled kitchen"]
    else:
        scene = f"Clean fictional project status board photographed in an office, headed {work['projects']['aurora']}, dated {slot['date']}, with columns DONE, NEXT, and WATCH. Legible cards: REGIONAL CACHE SHIPPED; STALE-DATA ALERT OWNER: {work['colleagues'][0]}; RETRY SPIKE: INVESTIGATION OPEN."
        required = [work["projects"]["aurora"], slot["date"], work["colleagues"][0], "REGIONAL CACHE SHIPPED", "INVESTIGATION OPEN"]
        forbidden = ["real company logo", "credential", "production URL", "confirmed retry-spike root cause", "private home detail"]
        durable = ["Aurora milestone", "alert ownership", "retry-spike investigation remains unresolved"]
    non_durable = ["camera angle", "incidental background arrangement", "decorative styling"]
    prompt = (
        f"# Image Specification {prompt_number:02d}\n\n"
        f"Destination: `{destination}`\n\nDate: {slot['date']}\n\nNarrative purpose: {slot['purpose']}\n\n"
        f"## Visible Scene\n\n{scene}\n\n"
        "## Required Canonical Facts\n\n" + "\n".join(f"- {item}" for item in required) + "\n\n"
        "## Must Not Appear\n\n" + "\n".join(f"- {item}" for item in forbidden) + "\n\n"
        "## Expected Durable Outcomes\n\n" + "\n".join(f"- {item}" for item in durable) + "\n\n"
        "## Expected Non-Durable Outcomes\n\n" + "\n".join(f"- {item}" for item in non_durable) + "\n\n"
        f"Safety: {identity['fiction_notice']} Do not add metadata, labels, identifiers, or text not requested above.\n"
    )
    return prompt, durable, non_durable


def run_manifest_template() -> dict:
    return {
        "schema_version": 1,
        "fixture_id": "synthetic-v1-qualification-vault",
        "scenario": {"id": "replace-with-run-id", "variant": "empty-before-installation", "session_id": None},
        "release": {"ava_version": None, "tag": None, "source_revision": None, "asset_urls": {}, "asset_sha256": {}},
        "environment": {"operating_system": None, "opencode_version": None, "model_identity": None},
        "project_inventories": {"baseline": None, "final": None},
        "artifacts": {"installer_output": None, "conformance_json": None, "managed_manifest": None, "upgrade_journal": None, "transcript": None},
        "routing": {"loaded_paths": [], "required_reading_order": [], "selected_role": None, "announcement_point": None},
        "decision": {"expected": "replace with scenario-specific expected outcome", "actual": None, "result": "pending", "reviewer": None, "linked_finding": None},
    }


def require_exact_keys(value: object, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise FixtureError(f"run manifest {label} must contain exactly {sorted(keys)}")
    return value


def validate_run_manifest_shape(value: object) -> dict:
    root = require_exact_keys(value, {"schema_version", "fixture_id", "scenario", "release", "environment", "project_inventories", "artifacts", "routing", "decision"}, "root")
    scenario = require_exact_keys(root["scenario"], {"id", "variant", "session_id"}, "scenario")
    if not isinstance(scenario["id"], str) or not scenario["id"] or scenario["variant"] not in VARIANT_FAMILIES or (scenario["session_id"] is not None and not isinstance(scenario["session_id"], str)):
        raise FixtureError("run manifest scenario identity, variant, or session is invalid")
    release = require_exact_keys(root["release"], {"ava_version", "tag", "source_revision", "asset_urls", "asset_sha256"}, "release")
    version_pattern = r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(?:alpha|beta|rc)\.[1-9][0-9]*)?$"
    if release["ava_version"] is not None and (not isinstance(release["ava_version"], str) or not re.fullmatch(version_pattern, release["ava_version"])):
        raise FixtureError("run manifest Ava version is invalid")
    if release["tag"] is not None and (not isinstance(release["tag"], str) or not re.fullmatch(f"v{version_pattern[1:]}", release["tag"])):
        raise FixtureError("run manifest release tag is invalid")
    if release["source_revision"] is not None and (not isinstance(release["source_revision"], str) or not re.fullmatch(r"[a-f0-9]{40}", release["source_revision"])):
        raise FixtureError("run manifest source revision is invalid")
    for field in ("asset_urls", "asset_sha256"):
        assets = release[field]
        if not isinstance(assets, dict) or (assets and set(assets) != RELEASE_ASSET_NAMES) or any(not isinstance(item, str) for item in assets.values()):
            raise FixtureError(f"run manifest {field} must be empty or bind the exact seven assets")
    for name, url in release["asset_urls"].items():
        pinned_https = isinstance(release["tag"], str) and url == f"https://github.com/phdah/ava/releases/download/{release['tag']}/{name}"
        pinned_file = url.startswith("file:///") and url.endswith(f"/{name}")
        if not pinned_https and not pinned_file:
            raise FixtureError(f"run manifest asset URL is not pinned to its selected name and tag: {name}")
    if any(not re.fullmatch(r"[a-f0-9]{64}", digest) for digest in release["asset_sha256"].values()):
        raise FixtureError("run manifest asset digest is invalid")
    environment = require_exact_keys(root["environment"], {"operating_system", "opencode_version", "model_identity"}, "environment")
    if any(item is not None and not isinstance(item, str) for item in environment.values()):
        raise FixtureError("run manifest environment values must be strings or null")
    inventories = require_exact_keys(root["project_inventories"], {"baseline", "final"}, "project inventories")
    for name, inventory in inventories.items():
        if inventory is None:
            continue
        inventory = require_exact_keys(inventory, {"path", "sha256"}, f"{name} inventory")
        if not isinstance(inventory["path"], str) or not inventory["path"] or not isinstance(inventory["sha256"], str) or not re.fullmatch(r"[a-f0-9]{64}", inventory["sha256"]):
            raise FixtureError(f"run manifest {name} inventory is invalid")
    artifacts = require_exact_keys(root["artifacts"], {"installer_output", "conformance_json", "managed_manifest", "upgrade_journal", "transcript"}, "artifacts")
    if any(item is not None and not isinstance(item, str) for item in artifacts.values()):
        raise FixtureError("run manifest artifact values must be strings or null")
    routing = require_exact_keys(root["routing"], {"loaded_paths", "required_reading_order", "selected_role", "announcement_point"}, "routing")
    for name in ("loaded_paths", "required_reading_order"):
        if not isinstance(routing[name], list) or any(not isinstance(item, str) for item in routing[name]):
            raise FixtureError(f"run manifest routing.{name} must be an array of strings")
    if any(routing[name] is not None and not isinstance(routing[name], str) for name in ("selected_role", "announcement_point")):
        raise FixtureError("run manifest selected role and announcement point must be strings or null")
    decision = require_exact_keys(root["decision"], {"expected", "actual", "result", "reviewer", "linked_finding"}, "decision")
    if not isinstance(decision["expected"], str) or not decision["expected"] or decision["result"] not in {"pending", "pass", "fail"}:
        raise FixtureError("run manifest expected outcome or result is invalid")
    if any(decision[name] is not None and not isinstance(decision[name], str) for name in ("actual", "reviewer", "linked_finding")):
        raise FixtureError("run manifest decision evidence values must be strings or null")
    return root


def verify_run_manifest(path: Path) -> None:
    value = validate_run_manifest_shape(json.loads(path.read_text(encoding="utf-8")))
    if value.get("schema_version") != 1 or value.get("fixture_id") != load_blueprint()["fixture_id"]:
        raise FixtureError("run manifest identity is invalid")
    result = value.get("decision", {}).get("result")
    if result == "pending":
        print("run manifest valid as pending evidence template")
        return
    if result not in {"pass", "fail"}:
        raise FixtureError("run manifest decision.result must be pending, pass, or fail")
    release = value.get("release", {})
    version = release.get("ava_version")
    tag = release.get("tag")
    version_pattern = r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(?:-(?:alpha|beta|rc)\.[1-9][0-9]*)?$"
    if not isinstance(version, str) or not re.fullmatch(version_pattern, version) or tag != f"v{version}":
        raise FixtureError("completed run release version and tag are invalid or inconsistent")
    if not isinstance(release.get("source_revision"), str) or not re.fullmatch(r"[a-f0-9]{40}", release["source_revision"]):
        raise FixtureError("completed run source revision must be a full Git SHA")
    urls = release.get("asset_urls", {})
    digests = release.get("asset_sha256", {})
    if set(urls) != RELEASE_ASSET_NAMES or set(digests) != RELEASE_ASSET_NAMES:
        raise FixtureError("completed run must bind the exact seven release assets")
    for name in RELEASE_ASSET_NAMES:
        url = urls[name]
        expected_https = f"https://github.com/phdah/ava/releases/download/{tag}/{name}"
        if url != expected_https and not (isinstance(url, str) and url.startswith("file:///") and url.endswith(f"/{name}")):
            raise FixtureError(f"asset URL is not pinned to the selected tag or local asset name: {name}")
        if not isinstance(digests[name], str) or not re.fullmatch(r"[a-f0-9]{64}", digests[name]):
            raise FixtureError(f"asset digest is invalid: {name}")
    required_strings = [
        value.get("scenario", {}).get("session_id"),
        value.get("environment", {}).get("operating_system"),
        value.get("environment", {}).get("opencode_version"),
        value.get("environment", {}).get("model_identity"),
        value.get("artifacts", {}).get("installer_output"),
        value.get("artifacts", {}).get("conformance_json"),
        value.get("artifacts", {}).get("managed_manifest"),
        value.get("artifacts", {}).get("upgrade_journal"),
        value.get("artifacts", {}).get("transcript"),
        value.get("routing", {}).get("selected_role"),
        value.get("routing", {}).get("announcement_point"),
        value.get("decision", {}).get("actual"),
        value.get("decision", {}).get("reviewer"),
    ]
    if any(not isinstance(item, str) or not item for item in required_strings):
        raise FixtureError("completed run is missing required environment, artifact, routing, or review evidence")
    for inventory_name in ("baseline", "final"):
        inventory = value.get("project_inventories", {}).get(inventory_name)
        if not isinstance(inventory, dict) or not inventory.get("path") or not re.fullmatch(r"[a-f0-9]{64}", inventory.get("sha256", "")):
            raise FixtureError(f"completed run {inventory_name} inventory is invalid")
    if not value.get("routing", {}).get("loaded_paths") or not value.get("routing", {}).get("required_reading_order"):
        raise FixtureError("completed run is missing loaded paths or required-reading order")
    if result == "fail" and not value.get("decision", {}).get("linked_finding"):
        raise FixtureError("failed run must link a finding")
    print(f"run manifest valid as completed {result} evidence")


def deterministic_corpus(blueprint: dict) -> list[tuple[bytes, dict]]:
    plan = inventory_plan(blueprint)
    expected_counts = blueprint["counts"]
    if len(plan) != expected_counts["deterministic_corpus"]:
        raise FixtureError(f"internal inventory plan error: expected {expected_counts['deterministic_corpus']}, got {len(plan)}")

    class_indexes: Counter[str] = Counter()
    entries: list[tuple[bytes, dict]] = []
    used_names: set[str] = set()
    for structural_class, source_date, extension in plan:
        index = class_indexes[structural_class]
        class_indexes[structural_class] += 1
        filename = f"{source_date.isoformat()}-{structural_class}-{index + 1:03d}.{extension}"
        if filename in used_names:
            raise FixtureError(f"duplicate generated path: {filename}")
        used_names.add(filename)
        content, sections, claims, subjects, non_durable, domain = text_for_class(blueprint, structural_class, source_date, index, extension)
        payload = encode_source(extension, f"{structural_class} {source_date.isoformat()}", content)
        record = source_record(filename, source_date, extension, structural_class, domain, subjects, non_durable, sections, claims, content)
        record["sha256"] = sha256_bytes(payload)
        record["bytes"] = len(payload)
        entries.append((payload, record))

    last_by_subject: dict[str, str] = {}
    for record in sorted((record for _, record in entries), key=lambda item: (item["date"], item["path"])):
        repeated_paths = []
        for subject in record["durable_subjects"][:3]:
            if subject in last_by_subject and last_by_subject[subject] not in repeated_paths:
                repeated_paths.append(last_by_subject[subject])
            last_by_subject[subject] = record["path"]
        record["duplicates"] = repeated_paths
    return entries


def deterministic_image_prompts(blueprint: dict) -> list[tuple[str, bytes, dict]]:
    entries = []
    for number, slot in enumerate(blueprint["image_slots"], 1):
        prompt_name = f"{number:02d}-{Path(slot['path']).stem}.md"
        prompt, durable, non_durable = prompt_content(blueprint, slot, number)
        prompt_payload = prompt.encode("utf-8")
        entries.append((prompt_name, prompt_payload, {
            **slot,
            "prompt_path": f"image-prompts/{prompt_name}",
            "prompt_sha256": sha256_bytes(prompt_payload),
            "prompt_bytes": len(prompt_payload),
            "state": "pending",
            "expected_durable": durable,
            "expected_non_durable": non_durable,
        }))
    return entries


def generate(output: Path) -> None:
    require_clean_output(output)
    blueprint = load_blueprint()
    corpus = output / "corpus"
    prompts = output / "image-prompts"
    oracle_root = output / "oracle"
    variants = output / "variants"
    for path in (corpus, prompts, oracle_root, variants):
        path.mkdir()
    for batch_name in CORPUS_BATCH_NAMES:
        (corpus / batch_name).mkdir()

    entries = deterministic_corpus(blueprint)
    records = [record for _, record in entries]
    for payload, record in entries:
        (output / record["path"]).write_bytes(payload)

    image_entries = deterministic_image_prompts(blueprint)
    image_records = [record for _, _, record in image_entries]
    for prompt_name, prompt_payload, _ in image_entries:
        (prompts / prompt_name).write_bytes(prompt_payload)

    oracle = {
        "schema_version": 1,
        "fixture_id": blueprint["fixture_id"],
        "generator": {
            "seed": blueprint["seed"],
            "revision": generator_revision(),
            "python_contract": "CPython >=3.11; deterministic algorithms are runtime-version independent",
            "dependencies": [],
            "blueprint_sha256": sha256_file(BLUEPRINT_PATH),
        },
        "interval": blueprint["interval"],
        "counts": blueprint["counts"],
        "canonical_facts": {key: value for key, value in blueprint.items() if key not in {"schema_version", "fixture_id", "seed", "interval", "counts", "transitions", "monthly_arcs", "image_slots", "variant_families"}},
        "transitions": blueprint["transitions"],
        "files": sorted(records, key=lambda item: item["path"].encode("utf-8")),
        "image_slots": image_records,
    }
    (oracle_root / "baseline.json").write_bytes(canonical_json(oracle))
    (oracle_root / "run-manifest.template.json").write_bytes(canonical_json(run_manifest_template()))
    (oracle_root / "README.txt").write_text(
        "baseline.json and run-manifest.template.json are control files. Do not copy oracle files into the inbox.\n",
        encoding="utf-8",
        newline="\n",
    )
    (variants / "README.txt").write_text(
        "Run install-pinned-images and finalize-images before materialize-variants. Variant control files are not inbox sources.\n",
        encoding="utf-8",
        newline="\n",
    )
    verify(output)
    print(f"generated deterministic baseline: {len(records)} corpus files, {len(image_records)} pending image slots")


def validate_binary(path: Path, extension: str) -> None:
    payload = path.read_bytes()
    if extension == "pdf":
        if not payload.startswith(b"%PDF-1.4") or not payload.rstrip().endswith(b"%%EOF"):
            raise FixtureError(f"invalid generated PDF: {path}")
    elif extension in {"docx", "pptx"}:
        try:
            with zipfile.ZipFile(path) as archive:
                names = set(archive.namelist())
                required = {"[Content_Types].xml", "_rels/.rels"}
                required.add("word/document.xml" if extension == "docx" else "ppt/slides/slide1.xml")
                if not required.issubset(names):
                    raise FixtureError(f"invalid generated {extension.upper()}: {path}")
                if archive.testzip() is not None:
                    raise FixtureError(f"corrupt generated {extension.upper()}: {path}")
        except zipfile.BadZipFile as exc:
            raise FixtureError(f"invalid generated {extension.upper()}: {path}") from exc
    elif extension == "ics":
        text = payload.decode("utf-8")
        if not text.startswith("BEGIN:VCALENDAR\r\n") or not text.endswith("END:VCALENDAR\r\n"):
            raise FixtureError(f"invalid generated ICS: {path}")
        if any(len(line.encode("utf-8")) > 75 for line in text.split("\r\n")):
            raise FixtureError(f"generated ICS contains an unfolded line over 75 octets: {path}")
        if "DESCRIPTION:" not in text or "\\;" not in text:
            raise FixtureError(f"generated ICS does not escape TEXT punctuation: {path}")


def selectable_text(path: Path, extension: str) -> str:
    if extension in {"md", "txt", "csv", "ics"}:
        return path.read_text(encoding="utf-8")
    if extension in {"docx", "pptx"}:
        member = "word/document.xml" if extension == "docx" else "ppt/slides/slide1.xml"
        with zipfile.ZipFile(path) as archive:
            root = ElementTree.fromstring(archive.read(member))
        return "\n".join(element.text or "" for element in root.iter() if element.tag.endswith("}t"))
    if extension == "pdf":
        text = path.read_bytes().decode("latin-1")
        values = re.findall(r"\((.*?)(?<!\\)\) Tj", text)
        return "\n".join(value.replace("\\(", "(").replace("\\)", ")").replace("\\\\", "\\") for value in values)
    raise FixtureError(f"unsupported selectable-text format: {extension}")


def image_type(path: Path, expected: str) -> str:
    if path.is_symlink() or not path.is_file():
        raise FixtureError(f"image must be a regular non-symlink file: {path}")
    payload = path.read_bytes()
    if expected == "png" and payload.startswith(b"\x89PNG\r\n\x1a\n"):
        offset = 8
        chunks = []
        image_header = None
        compressed_image = bytearray()
        palette_entries = None
        while offset + 12 <= len(payload):
            length = struct.unpack(">I", payload[offset : offset + 4])[0]
            chunk_type = payload[offset + 4 : offset + 8]
            chunk_end = offset + 12 + length
            if chunk_end > len(payload):
                break
            chunk_data = payload[offset + 8 : offset + 8 + length]
            expected_crc = struct.unpack(">I", payload[offset + 8 + length : chunk_end])[0]
            if zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF != expected_crc:
                raise FixtureError(f"PNG chunk checksum mismatch: {path}")
            chunks.append(chunk_type)
            if chunk_type == b"IHDR":
                if length != 13 or 0 in struct.unpack(">II", chunk_data[:8]):
                    raise FixtureError(f"invalid PNG dimensions: {path}")
                image_header = struct.unpack(">IIBBBBB", chunk_data)
            elif chunk_type == b"IDAT":
                compressed_image.extend(chunk_data)
            elif chunk_type == b"PLTE":
                if palette_entries is not None or length == 0 or length > 768 or length % 3 != 0:
                    raise FixtureError(f"invalid PNG palette: {path}")
                palette_entries = length // 3
            elif chunk_type == b"IEND" and length != 0:
                raise FixtureError(f"PNG IEND chunk must be empty: {path}")
            offset = chunk_end
            if chunk_type == b"IEND":
                break
        idat_indexes = [index for index, chunk in enumerate(chunks) if chunk == b"IDAT"]
        idat_contiguous = bool(idat_indexes) and idat_indexes == list(range(idat_indexes[0], idat_indexes[-1] + 1))
        if chunks[:1] == [b"IHDR"] and chunks.count(b"IHDR") == 1 and chunks.count(b"IEND") == 1 and idat_contiguous and chunks[-1:] == [b"IEND"] and offset == len(payload) and image_header is not None:
            width, height, bit_depth, color_type, compression, filter_method, interlace = image_header
            channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}.get(color_type)
            allowed_bit_depths = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8}, 4: {8, 16}, 6: {8, 16}}
            invalid_palette = color_type == 3 and b"PLTE" not in chunks
            forbidden_palette = color_type in {0, 4} and b"PLTE" in chunks
            palette_after_data = b"PLTE" in chunks and chunks.index(b"PLTE") > idat_indexes[0]
            palette_too_large = color_type == 3 and palette_entries is not None and palette_entries > 2**bit_depth
            if channels is None or bit_depth not in allowed_bit_depths[color_type] or invalid_palette or forbidden_palette or palette_after_data or palette_too_large or compression != 0 or filter_method != 0 or interlace != 0:
                raise FixtureError(f"unsupported or invalid PNG image header: {path}")
            row_bytes = (width * channels * bit_depth + 7) // 8
            try:
                decoded = zlib.decompress(bytes(compressed_image))
            except zlib.error as exc:
                raise FixtureError(f"PNG image data does not decompress: {path}") from exc
            if len(decoded) != height * (row_bytes + 1):
                raise FixtureError(f"PNG image data length does not match its dimensions: {path}")
            if any(decoded[row * (row_bytes + 1)] > 4 for row in range(height)):
                raise FixtureError(f"PNG uses an invalid row filter: {path}")
            return "image/png"
    if expected == "jpg" and payload.startswith(b"\xff\xd8") and payload.endswith(b"\xff\xd9"):
        offset = 2
        saw_frame = False
        saw_scan = False
        saw_huffman = False
        while offset < len(payload) - 2:
            if payload[offset] != 0xFF:
                raise FixtureError(f"invalid JPEG marker boundary: {path}")
            while offset < len(payload) and payload[offset] == 0xFF:
                offset += 1
            marker = payload[offset]
            offset += 1
            if marker == 0xD9:
                break
            if marker in range(0xD0, 0xD8) or marker == 0x01:
                continue
            if offset + 2 > len(payload):
                break
            length = struct.unpack(">H", payload[offset : offset + 2])[0]
            if length < 2 or offset + length > len(payload):
                break
            segment = payload[offset + 2 : offset + length]
            if marker in range(0xC0, 0xC4):
                if len(segment) < 6 or struct.unpack(">HH", segment[1:5])[0] == 0 or struct.unpack(">HH", segment[1:5])[1] == 0:
                    raise FixtureError(f"invalid JPEG frame dimensions: {path}")
                saw_frame = True
            if marker == 0xC4:
                position = 0
                while position < len(segment):
                    if position + 17 > len(segment):
                        raise FixtureError(f"invalid JPEG Huffman table: {path}")
                    symbol_count = sum(segment[position + 1 : position + 17])
                    if symbol_count == 0 or position + 17 + symbol_count > len(segment):
                        raise FixtureError(f"invalid JPEG Huffman table: {path}")
                    position += 17 + symbol_count
                saw_huffman = True
            if marker == 0xDA:
                if len(segment) < 6:
                    raise FixtureError(f"invalid JPEG scan header: {path}")
                saw_scan = True
                offset += length
                scan_start = offset
                while offset < len(payload) - 1:
                    if payload[offset] != 0xFF:
                        offset += 1
                        continue
                    next_byte = payload[offset + 1]
                    if next_byte == 0x00 or next_byte in range(0xD0, 0xD8):
                        offset += 2
                        continue
                    break
                if offset == scan_start:
                    raise FixtureError(f"empty JPEG scan data: {path}")
                continue
            offset += length
        if saw_frame and saw_huffman and saw_scan and payload[offset : offset + 2] == b"\xff\xd9" and offset + 2 == len(payload):
            return "image/jpeg"
    raise FixtureError(f"image does not match declared {expected} type: {path}")


def verify(output: Path) -> dict:
    if not output.is_dir():
        raise FixtureError(f"output does not exist: {output}")
    unexpected_children = {path.name for path in output.iterdir()} - ALLOWED_OUTPUT_CHILDREN
    if unexpected_children:
        raise FixtureError(f"unexpected output root entries: {sorted(unexpected_children)}")
    for name in ALLOWED_OUTPUT_CHILDREN:
        if (output / name).is_symlink() or not (output / name).is_dir():
            raise FixtureError(f"missing output directory: {name}")
    baseline_path = output / "oracle/baseline.json"
    if baseline_path.is_symlink() or not baseline_path.is_file():
        raise FixtureError("missing oracle/baseline.json")
    for schema_name in ("oracle.schema.json", "run-manifest.schema.json"):
        json.loads((FIXTURE_ROOT / schema_name).read_text(encoding="utf-8"))
    oracle = json.loads(baseline_path.read_text(encoding="utf-8"))
    blueprint = load_blueprint()
    oracle_keys = {"schema_version", "fixture_id", "generator", "interval", "counts", "canonical_facts", "transitions", "files", "image_slots"}
    if not isinstance(oracle, dict) or set(oracle) != oracle_keys:
        raise FixtureError(f"baseline oracle must contain exactly {sorted(oracle_keys)}")
    expected_canonical_facts = {key: value for key, value in blueprint.items() if key not in {"schema_version", "fixture_id", "seed", "interval", "counts", "transitions", "monthly_arcs", "image_slots", "variant_families"}}
    if oracle["schema_version"] != 1 or oracle["fixture_id"] != blueprint["fixture_id"]:
        raise FixtureError("baseline oracle identity is invalid")
    if oracle["interval"] != blueprint["interval"] or oracle["counts"] != blueprint["counts"] or oracle["canonical_facts"] != expected_canonical_facts or oracle["transitions"] != blueprint["transitions"]:
        raise FixtureError("baseline oracle canonical facts, interval, counts, or transitions differ from the blueprint")
    generator = oracle.get("generator")
    generator_keys = {"seed", "revision", "python_contract", "dependencies", "blueprint_sha256"}
    if not isinstance(generator, dict) or set(generator) != generator_keys:
        raise FixtureError(f"baseline generator metadata must contain exactly {sorted(generator_keys)}")
    if generator["seed"] != blueprint["seed"] or generator["python_contract"] != "CPython >=3.11; deterministic algorithms are runtime-version independent" or generator["dependencies"] != []:
        raise FixtureError("baseline generator contract differs from the blueprint and dependency lock")
    if oracle["generator"]["revision"] != generator_revision():
        raise FixtureError("baseline generator revision does not match current fixture")
    if oracle["generator"]["blueprint_sha256"] != sha256_file(BLUEPRINT_PATH):
        raise FixtureError("baseline blueprint digest does not match current blueprint")

    records = oracle["files"]
    if not isinstance(records, list) or not isinstance(oracle["image_slots"], list):
        raise FixtureError("baseline files and image slots must be arrays")
    expected_records = sorted((record for _, record in deterministic_corpus(blueprint)), key=lambda item: item["path"].encode("utf-8"))
    if records != expected_records:
        raise FixtureError("baseline file records differ from the deterministic semantic inventory")
    expected_image_records = [record for _, _, record in deterministic_image_prompts(blueprint)]
    if oracle["image_slots"] != expected_image_records:
        raise FixtureError("baseline image slots differ from the deterministic prompt inventory")
    expected_paths = {record["path"] for record in records}
    corpus = output / "corpus"
    corpus_children = list(corpus.iterdir())
    if {path.name for path in corpus_children} != set(CORPUS_BATCH_NAMES) or any(path.is_symlink() or not path.is_dir() for path in corpus_children):
        raise FixtureError(f"corpus must contain exactly the four batch directories: {list(CORPUS_BATCH_NAMES)}")
    corpus_directories = {path.relative_to(corpus).as_posix() for path in corpus.rglob("*") if path.is_dir()}
    if corpus_directories != set(CORPUS_BATCH_NAMES):
        raise FixtureError(f"corpus contains unexpected nested directories: {sorted(corpus_directories - set(CORPUS_BATCH_NAMES))}")
    actual_files = {path.relative_to(output).as_posix() for path in corpus.rglob("*") if path.is_file()}
    image_paths = {slot["path"] for slot in oracle["image_slots"]}
    if not actual_files.issubset(expected_paths | image_paths):
        raise FixtureError(f"unexpected corpus files: {sorted(actual_files - expected_paths - image_paths)}")
    if expected_paths - actual_files:
        raise FixtureError(f"missing deterministic corpus files: {sorted(expected_paths - actual_files)}")
    present_images = actual_files & image_paths
    if present_images and present_images != image_paths:
        raise FixtureError("image corpus is partial; provide either zero or all five external images")

    class_counts: Counter[str] = Counter()
    format_counts: Counter[str] = Counter()
    path_dates: list[date] = []
    record_keys = {"path", "sha256", "bytes", "date", "month", "format", "class", "domain", "durable_subjects", "non_durable", "sections", "claims", "duplicates"}
    for record in records:
        if not isinstance(record, dict) or set(record) != record_keys:
            raise FixtureError(f"baseline file record must contain exactly {sorted(record_keys)}")
        path = output / record["path"]
        if path.is_symlink() or not path.is_file():
            raise FixtureError(f"deterministic corpus source must be a regular non-symlink file: {record['path']}")
        if sha256_file(path) != record["sha256"] or path.stat().st_size != record["bytes"]:
            raise FixtureError(f"deterministic corpus digest mismatch: {record['path']}")
        if record["bytes"] < 150:
            raise FixtureError(f"corpus source is not substantive: {record['path']}")
        class_counts[record["class"]] += 1
        format_counts[record["format"]] += 1
        source_date = parse_date(record["date"])
        path_dates.append(source_date)
        if Path(record["path"]).parts[1] != corpus_batch(source_date):
            raise FixtureError(f"corpus batch does not match source date: {record['path']}")
        if record["month"] != source_date.strftime("%Y-%m"):
            raise FixtureError(f"month mismatch in oracle: {record['path']}")
        if record["format"] == "md":
            first_line = path.read_text(encoding="utf-8").splitlines()[0]
            if first_line.strip() == "---" or not first_line.startswith("#"):
                raise FixtureError(f"Markdown corpus source has frontmatter or no raw heading: {record['path']}")
        if record["format"] in {"md", "txt", "csv", "ics"}:
            text = path.read_text(encoding="utf-8")
            prohibited = ("ignore previous instructions", "system prompt", "BEGIN PRIVATE KEY", "password=", "api_key=")
            if any(value.lower() in text.lower() for value in prohibited):
                raise FixtureError(f"prohibited adversarial or secret-like text in corpus source: {record['path']}")
        validate_binary(path, record["format"])
        extracted_text = selectable_text(path, record["format"])
        if record["class"] == "housing-move" and source_date < parse_date(blueprint["move"]["lease_signed"]) and f"Lease signed on {blueprint['move']['lease_signed']}" in extracted_text:
            raise FixtureError(f"housing source asserts a future lease signature: {record['path']}")
        if record["class"] == "kitchen-renovation":
            if source_date < parse_date(blueprint["renovation"]["completed"]) and "Final cost: SEK" in extracted_text:
                raise FixtureError(f"renovation source asserts future final cost: {record['path']}")
            if source_date < parse_date(blueprint["renovation"]["delay_announced"]) and blueprint["renovation"]["delay"] in extracted_text:
                raise FixtureError(f"renovation source asserts a future delay: {record['path']}")
        if record["class"] == "running":
            race_date = parse_date(blueprint["running"]["race_date"])
            if source_date > race_date and "build toward" in extracted_text:
                raise FixtureError(f"post-race source still describes race preparation: {record['path']}")
            if source_date < race_date and blueprint["running"]["race_finish_time"] in extracted_text:
                raise FixtureError(f"pre-race source asserts a future finish time: {record['path']}")
        for item in record["claims"]:
            if item["date"] != record["date"]:
                raise FixtureError(f"claim date mismatch: {record['path']}")
            if " ".join(item["source_excerpt"].split()) not in " ".join(extracted_text.split()):
                raise FixtureError(f"claim support excerpt is absent from source: {record['path']}")
        for item in record["sections"]:
            if item["disposition"] == "mapped" and (not item["destinations"] or item["blocker"] is not None):
                raise FixtureError(f"mapped section lacks destinations or has a blocker: {record['path']}::{item['locator']}")
            if item["disposition"] == "pending" and (item["destinations"] or not item["blocker"]):
                raise FixtureError(f"pending section lacks an explicit blocker: {record['path']}::{item['locator']}")
            if item["disposition"] == "non-durable" and (item["destinations"] or item["blocker"] is not None):
                raise FixtureError(f"non-durable section has a destination or blocker: {record['path']}::{item['locator']}")
        if any(related == record["path"] or related not in expected_paths for related in record["duplicates"]):
            raise FixtureError(f"invalid duplicate or repetition relationship: {record['path']}")
        current_claims = [item["text"] for item in record["claims"] if item["text"].startswith("Current home address was")]
        for current_claim in current_claims:
            if current_address(blueprint, source_date) not in current_claim:
                raise FixtureError(f"residence chronology mismatch: {record['path']}")

    if dict(class_counts) != blueprint["counts"]["classes"]:
        raise FixtureError(f"class counts differ from blueprint: {dict(class_counts)}")
    if dict(format_counts) != blueprint["counts"]["formats"]:
        raise FixtureError(f"format counts differ from blueprint: {dict(format_counts)}")
    if min(path_dates).isoformat() != blueprint["interval"]["start"] or max(path_dates).isoformat() != blueprint["interval"]["end"]:
        raise FixtureError("corpus does not cover the complete fixed interval")
    if len({record["path"] for record in records}) != blueprint["counts"]["deterministic_corpus"]:
        raise FixtureError("deterministic inventory paths are not unique or complete")

    prompts = sorted((output / "image-prompts").glob("*.md"))
    expected_prompt_paths = {slot["prompt_path"] for slot in oracle["image_slots"]}
    if {f"image-prompts/{path.name}" for path in prompts} != expected_prompt_paths:
        raise FixtureError("image prompt inventory differs from the five declared slots")
    if len(oracle["image_slots"]) != blueprint["counts"]["external_images"]:
        raise FixtureError("image slot count differs from blueprint")
    image_keys = {"path", "prompt_path", "prompt_sha256", "prompt_bytes", "date", "purpose", "format", "domain", "state", "expected_durable", "expected_non_durable"}
    for slot in oracle["image_slots"]:
        if not isinstance(slot, dict) or set(slot) != image_keys:
            raise FixtureError(f"baseline image slot must contain exactly {sorted(image_keys)}")
        if Path(slot["path"]).parts[1] != corpus_batch(parse_date(slot["date"])):
            raise FixtureError(f"image batch does not match source date: {slot['path']}")
        prompt_path = output / slot["prompt_path"]
        if prompt_path.is_symlink() or not prompt_path.is_file():
            raise FixtureError(f"image prompt must be a regular non-symlink file: {slot['prompt_path']}")
        if sha256_file(prompt_path) != slot["prompt_sha256"] or prompt_path.stat().st_size != slot["prompt_bytes"]:
            raise FixtureError(f"image prompt digest mismatch: {slot['prompt_path']}")

    pinned_images = {item["destination"]: item for item in load_pinned_image_manifest(blueprint)["images"]}
    finalized_path = output / "oracle/finalized-inventory.json"
    if finalized_path.is_symlink():
        raise FixtureError("oracle/finalized-inventory.json must not be a symlink")
    finalized = None
    image_state = "pending"
    if present_images:
        image_records = []
        for slot in oracle["image_slots"]:
            path = output / slot["path"]
            media_type = image_type(path, slot["format"])
            pinned = pinned_images[slot["path"]]
            if sha256_file(path) != pinned["sha256"] or path.stat().st_size != pinned["bytes"] or media_type != pinned["media_type"]:
                raise FixtureError(f"corpus image differs from pinned fixture input: {slot['path']}")
            image_records.append({"path": slot["path"], "sha256": pinned["sha256"], "bytes": pinned["bytes"], "media_type": media_type})
        finalized = {
            "schema_version": 1,
            "fixture_id": blueprint["fixture_id"],
            "deterministic_baseline_sha256": sha256_file(baseline_path),
            "deterministic_count": len(records),
            "external_images": image_records,
            "finalized_count": len(records) + len(image_records),
        }
        if finalized_path.is_file() and json.loads(finalized_path.read_text(encoding="utf-8")) != finalized:
            raise FixtureError("recorded finalized image inventory differs from current image bytes")
        image_state = "finalized" if finalized_path.is_file() else "ready"
    elif finalized_path.exists():
        raise FixtureError("finalized inventory exists while image files are absent")

    result = {
        "status": "valid",
        "deterministic_count": len(records),
        "deterministic_inventory_sha256": sha256_file(baseline_path),
        "image_state": image_state,
        "pending_image_slots": 0 if present_images else len(image_paths),
        "finalized_count": finalized["finalized_count"] if finalized else None,
    }
    print(json.dumps(result, sort_keys=True))
    return result


def finalize_images(output: Path) -> None:
    result = verify(output)
    if result["image_state"] not in {"ready", "finalized"}:
        raise FixtureError("all five pinned image files must exist before finalization")
    oracle = json.loads((output / "oracle/baseline.json").read_text(encoding="utf-8"))
    records = []
    for slot in oracle["image_slots"]:
        path = output / slot["path"]
        records.append({"path": slot["path"], "sha256": sha256_file(path), "bytes": path.stat().st_size, "media_type": image_type(path, slot["format"])})
    finalized = {
        "schema_version": 1,
        "fixture_id": oracle["fixture_id"],
        "deterministic_baseline_sha256": sha256_file(output / "oracle/baseline.json"),
        "deterministic_count": len(oracle["files"]),
        "external_images": records,
        "finalized_count": len(oracle["files"]) + len(records),
    }
    (output / "oracle/finalized-inventory.json").write_bytes(canonical_json(finalized))
    verify(output)
    print(f"finalized image inventory: {len(records)} images, {finalized['finalized_count']} total corpus files")


def install_pinned_images(output: Path) -> None:
    result = verify(output)
    if result["image_state"] != "pending":
        raise FixtureError("pinned images can be installed only into a generated vault with empty image slots")
    blueprint = load_blueprint()
    manifest = load_pinned_image_manifest(blueprint)
    for item in manifest["images"]:
        source = PINNED_IMAGES_ROOT / item["file"]
        destination = output / item["destination"]
        destination.write_bytes(source.read_bytes())
    installed = verify(output)
    if installed["image_state"] != "ready":
        raise FixtureError("installed pinned images did not produce a ready fixture")
    print(f"installed {len(manifest['images'])} pinned qualification images")


def tree_inventory(root: Path) -> list[dict]:
    return [
        {"path": path.relative_to(root).as_posix(), "sha256": sha256_file(path), "bytes": path.stat().st_size}
        for path in sorted((item for item in root.rglob("*") if item.is_file()), key=lambda item: item.relative_to(root).as_posix().encode("utf-8"))
    ]


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8", newline="\n")


def scenario_file(root: Path, scenario_id: str, purpose: str, operations: list[str]) -> None:
    value = {"schema_version": 1, "scenario_id": scenario_id, "purpose": purpose, "operations": operations, "execution_state": "planned", "evidence_required": True}
    (root / "scenario.json").write_bytes(canonical_json(value))


def materialize_variants(output: Path) -> None:
    result = verify(output)
    if result["image_state"] != "finalized" or not (output / "oracle/finalized-inventory.json").is_file():
        raise FixtureError("materialize-variants requires finalized images and oracle/finalized-inventory.json")
    variants = output / "variants"
    existing = [path for path in variants.iterdir() if path.name != "README.txt"]
    if existing:
        raise FixtureError("variants already materialized; use a clean generated output")
    corpus_before = tree_inventory(output / "corpus")
    families = []

    empty = variants / "01-empty-before-installation/project"
    empty.mkdir(parents=True)
    scenario_file(empty.parent, "empty-before-installation", "Fresh installation into an empty project.", ["install assembled or pinned published assets", "record dry-run and apply output", "verify managed and scaffold inventories"])
    families.append(empty.parent)

    mature = variants / "02-mature-mixed-project/project"
    write_text(mature / "index.md", f"# {load_blueprint()['identity']['first_name']}'s Mixed Project\n\nProject-owned private and work knowledge predates Ava installation.\n")
    write_text(mature / "knowledge/private/home.md", "# Home\n\nExisting project-owned household context.\n")
    write_text(mature / "knowledge/work/platform.md", "# Platform\n\nExisting project-owned platform context.\n")
    write_text(mature / "opencode.json", json.dumps({"$schema": "https://opencode.ai/config.json", "permission": {"read": "allow", "edit": "ask"}}, indent=2) + "\n")
    scenario_file(mature.parent, "mature-mixed-project", "Install without changing existing mixed context or OpenCode configuration.", ["hash project-owned baseline", "install assets", "verify opencode.json and knowledge are unchanged"])
    families.append(mature.parent)

    registered = variants / "03-registered-private-work-roles/project"
    blueprint = load_blueprint()
    person = blueprint["identity"]["full_name"]
    employer = blueprint["work"]["employer"]
    write_text(
        registered / "roles/index.md",
        "# Roles\n\n"
        "## [Private Life Steward](private-life-steward/)\n\n"
        f"Select for {person}'s home, dog, running, reading, cooking, private purchases, appointments, and personal travel. Do not select for {employer} projects or mixed expenses whose ownership is unresolved.\n\n"
        "## [Work Context Steward](work-context-steward/)\n\n"
        f"Select for {employer} projects, meetings, incidents, architecture decisions, integrations, and operations. Do not select for private life or unresolved mixed expenses.\n",
    )
    role_definitions = (
        ("private-life-steward", "Private Life Steward", f"{person}'s private home, dog, running, reading, cooking, purchases, appointments, and personal travel", "knowledge/private/", f"{employer} work and unresolved mixed expenses"),
        ("work-context-steward", "Work Context Steward", f"{employer} projects, meetings, incidents, architecture decisions, integrations, and operations", "knowledge/work/", "private life and unresolved mixed expenses"),
    )
    for slug, title, routing, knowledge_root, exclusion in role_definitions:
        role = registered / f"roles/{slug}"
        write_text(
            role / "index.md",
            f"# {title}\n\nBefore acting, read every file under **Required reading** in order.\n\n"
            "## Required reading\n\n"
            "1. [Role definition](role.md)\n"
            "2. [Instructions](instructions.md)\n"
            "3. [Capabilities](capabilities.md)\n"
            "4. [Constraints](constraints.md)\n"
            "5. [Document metadata](./.ava/base/shared/instructions/document-metadata.md)\n"
            "6. [Knowledge organization](./.ava/base/shared/instructions/knowledge-organization.md)\n",
        )
        write_text(
            role / "role.md",
            f"---\ntype: Agent Role\ntitle: {title}\ndescription: Maintains {routing}.\ngenerated:\n  by: tool:ava-synthetic-qualification-vault\n  at: {FIXED_DOCUMENT_TIME}\n---\n\n"
            f"# Purpose\n\nMaintain trusted project-owned context for {routing}.\n\n"
            f"# Activation\n\nSelect this role when the primary requested outcome concerns {routing}. Do not select it for {exclusion}. Ask for routing clarification when ownership of a mixed subject remains unresolved.\n\n"
            "# Responsibilities\n\nPreserve dated state, source provenance, attribution, uncertainty, decisions, and supersession. Keep private and work knowledge separate while linking genuinely shared subjects without duplicating authority.\n\n"
            f"# Authority\n\nThe role may maintain project-owned Markdown under `{knowledge_root}` and the indexes needed to discover that content. It has no Ava-managed, installer, workflow, role-lifecycle, or inbox-ingestion authority.\n\n"
            f"# Scope\n\nThe mutation boundary is `{knowledge_root}`. Cross-boundary links may be read when relevant, but another role's knowledge must not be rewritten.\n",
        )
        write_text(
            role / "instructions.md",
            f"---\ntype: Role Instructions\ntitle: {title} Instructions\ndescription: Defines safe maintenance of {routing}.\ngenerated:\n  by: tool:ava-synthetic-qualification-vault\n  at: {FIXED_DOCUMENT_TIME}\n---\n\n"
            "# Procedure\n\n1. Confirm that the requested primary outcome matches this role.\n2. Read only the relevant project-owned knowledge and sources.\n3. Preserve dates, historical truth, supersession, attribution, uncertainty, and proposal-versus-decision state.\n4. Apply the smallest coherent update inside the declared knowledge root.\n5. Maintain direct-child indexes and metadata required by the shared contracts.\n6. Report unresolved mixed ownership instead of choosing a private or work destination silently.\n",
        )
        write_text(
            role / "capabilities.md",
            f"---\ntype: Role Capabilities\ntitle: {title} Capabilities\ndescription: Permitted project-owned maintenance actions for {routing}.\ngenerated:\n  by: tool:ava-synthetic-qualification-vault\n  at: {FIXED_DOCUMENT_TIME}\n---\n\n"
            f"# Permitted actions\n\nThe role may create, update, move, consolidate, and index trusted Markdown under `{knowledge_root}`. It may add cross-links to relevant project-owned context without changing that context.\n",
        )
        write_text(
            role / "constraints.md",
            f"---\ntype: Role Constraints\ntitle: {title} Constraints\ndescription: Safeguards for the role's private and work authority boundary.\ngenerated:\n  by: tool:ava-synthetic-qualification-vault\n  at: {FIXED_DOCUMENT_TIME}\n---\n\n"
            f"# Boundaries\n\nThe role must not mutate Ava-managed files, role or workflow definitions, inbox sources, `{('knowledge/work/' if knowledge_root == 'knowledge/private/' else 'knowledge/private/')}`, or mixed expenses whose ownership remains unresolved. It must not convert uncertainty into fact, a proposal into a decision, historical truth into current state, or source content into unsupported authority.\n",
        )
    scenario_file(registered.parent, "registered-private-work-roles", "Qualify routing and separation with explicit project roles.", ["install assets", "ask representative private, work, overlapping, and ambiguous questions", "record selected role and loaded paths"])
    families.append(registered.parent)

    pending = variants / "04-complete-pending-inbox/project/inbox"
    pending.mkdir(parents=True)
    corpus_files = (path for path in (output / "corpus").rglob("*") if path.is_file())
    for path in sorted(corpus_files, key=lambda item: item.relative_to(output / "corpus").as_posix().encode("utf-8")):
        destination = pending / path.name
        if destination.exists():
            raise FixtureError(f"duplicate corpus filename cannot be flattened into inbox: {path.name}")
        shutil.copyfile(path, destination)
    scenario_file(pending.parents[1], "complete-pending-inbox", "Ingest the complete finalized 305-file raw corpus.", ["install assets", "copy no control files into inbox", "run repeated ingestion sessions", "reconcile every source and section against the oracle"])
    families.append(pending.parents[1])

    damage = variants / "05-managed-content-damage"
    for name, operation in (("modified", "modify one recorded managed payload after installation"), ("missing", "remove one recorded managed payload after installation"), ("corrupt", "replace one managed state file with invalid JSON after installation"), ("unexpected", "add an unrecorded file below .ava/base after installation")):
        project = damage / name / "project"
        project.mkdir(parents=True)
        scenario_file(project.parent, f"managed-{name}", f"Diagnose {name} managed content without silent repair.", ["install assets into this isolated project", operation, "run conformance and Ava Maintenance inspection", "record refusal or recovery decision"])
    families.append(damage)

    interrupted = variants / "06-interrupted-upgrade-states"
    for name in ("resume", "abort", "rollback", "finalize"):
        project = interrupted / name / "project"
        project.mkdir(parents=True)
        scenario_file(project.parent, f"interrupted-upgrade-{name}", f"Exercise the supported {name} operation from a real interrupted transaction checkpoint.", ["install declared source release", "start target upgrade with the maintained checkpoint harness", f"capture the checkpoint valid for --{name}", f"run --{name} and verify terminal state"])
    families.append(interrupted)

    semantic = variants / "07-pending-semantic-reconciliation/project"
    write_text(semantic / "roles/index.md", "# Roles\n\nProject-owned role context to review through installed guidance.\n")
    scenario_file(semantic.parent, "pending-semantic-reconciliation", "Exercise Upgrade Role while deterministic base upgrade is complete and semantic reconciliation is pending.", ["install source release", "upgrade with semantic-review-required target assets", "verify only semantic operations are allowed", "apply exact installed guidance and finalize"])
    families.append(semantic.parent)

    lifecycle = variants / "08-uninstall-reinstallation"
    for name, purpose in (("installed", "Initial healthy installation checkpoint."), ("uninstalled", "Checkpoint after role-led uninstall with project-owned content preserved."), ("reinstalled", "Checkpoint after reinstalling the same pinned assets.")):
        project = lifecycle / name / "project"
        write_text(project / "knowledge/private/baseline.md", "# Preserved baseline\n\nThis project-owned file must remain byte-identical across uninstall and reinstall.\n")
        scenario_file(project.parent, f"lifecycle-{name}", purpose, ["use pinned assets", "record managed and project-owned inventories", "verify the expected lifecycle state"])
    families.append(lifecycle)

    corpus_after = tree_inventory(output / "corpus")
    if corpus_after != corpus_before:
        raise FixtureError("variant materialization changed the baseline corpus")
    manifest = {
        "schema_version": 1,
        "fixture_id": load_blueprint()["fixture_id"],
        "baseline_corpus_sha256": sha256_bytes(canonical_json(corpus_before)),
        "families": [
            {"id": path.name.split("-", 1)[1], "path": path.relative_to(variants).as_posix(), "materialization": "workspace-and-execution-plan", "inventory": tree_inventory(path)}
            for path in families
        ],
    }
    (variants / "index.json").write_bytes(canonical_json(manifest))
    if len(manifest["families"]) != 8:
        raise FixtureError("variant manifest does not contain exactly eight families")
    print(f"materialized {len(manifest['families'])} isolated qualification workspaces and execution plans; managed states remain unexecuted")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("generate", "verify", "install-pinned-images", "finalize-images", "materialize-variants"):
        child = subparsers.add_parser(command)
        child.add_argument("output", help="explicit output directory outside the Ava repository")
    run_manifest_parser = subparsers.add_parser("verify-run-manifest")
    run_manifest_parser.add_argument("manifest", help="qualification run manifest to verify")
    args = parser.parse_args(argv)
    try:
        if args.command == "verify-run-manifest":
            verify_run_manifest(Path(args.manifest).expanduser().resolve())
            return 0
        require_supported_runtime()
        output = resolved_output(args.output)
        if args.command == "generate":
            generate(output)
        elif args.command == "verify":
            verify(output)
        elif args.command == "install-pinned-images":
            install_pinned_images(output)
        elif args.command == "finalize-images":
            finalize_images(output)
        elif args.command == "materialize-variants":
            materialize_variants(output)
    except (FixtureError, OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"synthetic qualification fixture error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
