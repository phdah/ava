"""Release-asset conformance checks."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from internal.release.conformance_common import (
    RELEASE_ASSETS,
    SEMVER_RE,
    Finding,
    ValidationResult,
    read_json,
)


def parse_checksum_file(path: Path) -> tuple[dict[str, str], str | None]:
    checksums: dict[str, str] = {}
    try:
        lines = path.read_text().splitlines()
    except FileNotFoundError:
        return {}, "missing"
    for number, line in enumerate(lines, 1):
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9._-]+)", line)
        if not match:
            return {}, f"invalid line {number}"
        digest, name = match.groups()
        if name in checksums:
            return {}, f"duplicate entry {name}"
        checksums[name] = digest
    return checksums, None


def validate_release(root: Path, require_publication_evidence: bool = False) -> ValidationResult:
    findings: list[Finding] = []
    for name in RELEASE_ASSETS:
        if not (root / name).is_file():
            findings.append(Finding("AVA-RELEASE-ASSET", "error", name, "required release asset is missing", category="release"))
    checksums, error = parse_checksum_file(root / "SHA256SUMS")
    if error:
        findings.append(Finding("AVA-RELEASE-CHECKSUMS", "error", "SHA256SUMS", error, category="release"))
    else:
        expected = set(RELEASE_ASSETS) - {"SHA256SUMS"}
        if set(checksums) != expected:
            findings.append(Finding("AVA-RELEASE-INVENTORY", "error", "SHA256SUMS", "checksum inventory does not exactly match release assets", category="release"))
        for name, digest in checksums.items():
            path = root / name
            if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                findings.append(Finding("AVA-RELEASE-CHECKSUM", "error", name, "asset checksum does not match SHA256SUMS", category="release"))

    manifest, manifest_error = read_json(root / "ava-release.json")
    if manifest_error:
        findings.append(Finding("AVA-RELEASE-MANIFEST", "error", "ava-release.json", f"release manifest is {manifest_error}", category="release"))
    elif isinstance(manifest, dict):
        version = manifest.get("ava_version") or manifest.get("version")
        channel = manifest.get("channel")
        tag = manifest.get("tag")
        if not isinstance(version, str) or not SEMVER_RE.fullmatch(version):
            findings.append(Finding("AVA-RELEASE-VERSION", "error", "ava-release.json", "release version is invalid", category="release"))
        else:
            if tag is not None and tag != f"v{version}":
                findings.append(Finding("AVA-RELEASE-VERSION", "error", "ava-release.json", "release tag does not match ava_version", category="release"))
            if channel not in {"stable", "rc", "beta", "alpha"}:
                findings.append(Finding("AVA-RELEASE-CHANNEL", "error", "ava-release.json", "release channel is invalid", category="release"))
            elif (channel == "stable") != ("-" not in version):
                findings.append(Finding("AVA-RELEASE-CHANNEL", "error", "ava-release.json", "release channel does not match version prerelease suffix", category="release"))

        upgrade_paths = manifest.get("upgrade_paths")
        if isinstance(upgrade_paths, dict):
            edges = upgrade_paths.get("edges")
            if isinstance(edges, list) and len(edges) == 0 and isinstance(version, str) and version != "1.0.0-alpha.1":
                findings.append(Finding("AVA-RELEASE-UPGRADE-EDGES", "error", "ava-release.json", "release must declare at least one supported upgrade source; only 1.0.0-alpha.1 may have an empty edge list", category="release"))

        assets = manifest.get("assets")
        if not isinstance(assets, list):
            findings.append(Finding("AVA-RELEASE-ASSET-METADATA", "error", "ava-release.json", "release manifest assets must be a list", category="release"))
        else:
            by_name: dict[str, dict[str, Any]] = {}
            for item in assets:
                if not isinstance(item, dict) or not isinstance(item.get("name"), str):
                    findings.append(Finding("AVA-RELEASE-ASSET-METADATA", "error", "ava-release.json", "release asset entries must be named objects", category="release"))
                    continue
                name = item["name"]
                if name in by_name:
                    findings.append(Finding("AVA-RELEASE-ASSET-METADATA", "error", "ava-release.json", f"duplicate release asset metadata: {name}", category="release"))
                by_name[name] = item
            if set(by_name) != set(RELEASE_ASSETS):
                findings.append(Finding("AVA-RELEASE-ASSET-METADATA", "error", "ava-release.json", "release manifest asset inventory is incomplete or unexpected", category="release"))
            for name in set(by_name) & (set(RELEASE_ASSETS) - {"ava-release.json", "SHA256SUMS"}):
                path = root / name
                item = by_name[name]
                if not path.is_file() or item.get("sha256") != hashlib.sha256(path.read_bytes()).hexdigest() or item.get("size") != path.stat().st_size:
                    findings.append(Finding("AVA-RELEASE-ASSET-METADATA", "error", name, "release manifest asset size or checksum does not match the file", category="release"))

    evidence, evidence_error = read_json(root / "publication.json")
    if evidence_error:
        severity = "error" if require_publication_evidence else "recommendation"
        findings.append(
            Finding(
                "AVA-RELEASE-PUBLICATION-EVIDENCE",
                severity,
                "publication.json",
                "publication evidence is required to qualify an immutable published release" if require_publication_evidence else "publication evidence is absent; this is expected before publication qualification",
                category="release",
            )
        )
    elif isinstance(evidence, dict):
        required_true = ("immutable_releases_enabled", "release_immutable", "attestation_verified")
        for key in required_true:
            if evidence.get(key) is not True:
                findings.append(Finding("AVA-RELEASE-IMMUTABILITY", "error", "publication.json", f"{key} must be true for release qualification", category="release"))

    return ValidationResult("release", findings)
