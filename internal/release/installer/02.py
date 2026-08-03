def validate_host_integration(value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, dict):
        raise AvaError("INVALID_INSTALLED_STATE", "host_integration must be null or an object")
    require_exact_keys(value, {"entrypoint", "ownership", "discovery"}, "host integration")
    entrypoint = value.get("entrypoint")
    if not isinstance(entrypoint, str):
        raise AvaError("INVALID_INSTALLED_STATE", "host entrypoint must be a project-root path")
    destination_relative(entrypoint)
    if entrypoint == "/AGENTS.md" or entrypoint == "/.ava" or entrypoint.startswith("/.ava/"):
        raise AvaError("INVALID_INSTALLED_STATE", "host entrypoint must be project-owned and outside Ava-managed paths")
    if value.get("ownership") != "project-owned" or value.get("discovery") != "project-provided":
        raise AvaError("INVALID_INSTALLED_STATE", "invalid host integration ownership or discovery mode")


def validate_installed_manifest(manifest: Any) -> None:
    if not isinstance(manifest, dict):
        raise AvaError("INVALID_INSTALLED_STATE", "installed manifest must be an object")
    required = {
        "manifest_schema", "ava_version", "okf_version", "installed_at", "release",
        "managed_files", "host_integration", "semantic_compatibility",
    }
    require_exact_keys(manifest, required, "installed manifest")
    if manifest["manifest_schema"] != 1:
        raise AvaError("UNSUPPORTED_SCHEMA", "unsupported installed manifest schema")
    canonical_version(manifest["ava_version"])
    release = manifest["release"]
    if not isinstance(release, dict) or set(release) != {"tag", "channel", "source_revision", "release_manifest_sha256"}:
        raise AvaError("INVALID_INSTALLED_STATE", "invalid installed release identity")
    if release["tag"] != f"v{manifest['ava_version']}" or release["channel"] != derive_channel(manifest["ava_version"]):
        raise AvaError("INVALID_INSTALLED_STATE", "installed version identity mismatch")
    if not SHA1_RE.fullmatch(release["source_revision"]) or not SHA256_RE.fullmatch(release["release_manifest_sha256"]):
        raise AvaError("INVALID_INSTALLED_STATE", "invalid installed release checksums")
    files = manifest["managed_files"]
    if not isinstance(files, list):
        raise AvaError("INVALID_INSTALLED_STATE", "managed_files must be an array")
    paths: set[str] = set()
    state_paths = set()
    for item in files:
        if not isinstance(item, dict):
            raise AvaError("INVALID_INSTALLED_STATE", "managed file must be an object")
        destination_relative(item.get("path", ""))
        if item["path"] in paths:
            raise AvaError("INVALID_INSTALLED_STATE", "duplicate managed file path")
        paths.add(item["path"])
        if item.get("kind") == "payload":
            if set(item) != {"path", "role", "kind", "sha256"} or not SHA256_RE.fullmatch(item["sha256"]):
                raise AvaError("INVALID_INSTALLED_STATE", f"invalid payload state: {item['path']}")
        elif item.get("kind") == "state":
            if set(item) != {"path", "role", "kind"} or item["role"] != "state":
                raise AvaError("INVALID_INSTALLED_STATE", f"invalid state record: {item['path']}")
            state_paths.add(item["path"])
        else:
            raise AvaError("INVALID_INSTALLED_STATE", f"invalid managed kind: {item.get('kind')}")
    if "/AGENTS.md" not in paths or state_paths != {"/.ava/state/manifest.json", "/.ava/state/upgrade.json"}:
        raise AvaError("INVALID_INSTALLED_STATE", "required managed paths are missing")
    validate_host_integration(manifest["host_integration"])
    compatibility = manifest["semantic_compatibility"]
    required_compatibility = {"compatible_through", "target_version", "status", "unresolved_decisions"}
    if not isinstance(compatibility, dict) or set(compatibility) != required_compatibility:
        raise AvaError("INVALID_INSTALLED_STATE", "invalid semantic compatibility state")
    canonical_version(compatibility["compatible_through"])
    if compatibility["target_version"] is not None:
        canonical_version(compatibility["target_version"])
    if compatibility["status"] not in {"complete", "pending", "partial", "blocked"} or not isinstance(compatibility["unresolved_decisions"], list):
        raise AvaError("INVALID_INSTALLED_STATE", "invalid semantic compatibility status")
    if compatibility["status"] == "complete" and (compatibility["target_version"] is not None or compatibility["unresolved_decisions"]):
        raise AvaError("INVALID_INSTALLED_STATE", "complete compatibility has pending state")


def release_state(bundle: Bundle) -> dict[str, str]:
    return {
        "ava_version": bundle.version,
        "okf_version": bundle.manifest["okf_version"],
        "tag": bundle.tag,
        "source_revision": bundle.manifest["source_revision"],
        "release_manifest_sha256": bundle.manifest_sha256,
    }


def safe_extract(archive: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    names: set[str] = set()
    total_size = 0
    with tarfile.open(archive, "r:gz") as handle:
        members = handle.getmembers()
        if len(members) > 10000:
            raise AvaError("UNSAFE_ARCHIVE", f"too many archive entries: {archive.name}")
        for member in members:
            name = safe_relative(member.name)
            if name in names:
                raise AvaError("UNSAFE_ARCHIVE", f"duplicate archive entry: {name}")
            names.add(name)
            if member.isdir():
                continue
            if not member.isfile() or member.issym() or member.islnk() or member.isdev():
                raise AvaError("UNSAFE_ARCHIVE", f"unsupported archive entry: {name}")
            total_size += member.size
            if total_size > 256 * 1024 * 1024:
                raise AvaError("UNSAFE_ARCHIVE", f"archive exceeds extraction limit: {archive.name}")
            target = destination.joinpath(*PurePosixPath(name).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            source = handle.extractfile(member)
            if source is None:
                raise AvaError("UNSAFE_ARCHIVE", f"cannot read archive entry: {name}")
            with target.open("wb") as output:
                shutil.copyfileobj(source, output)


def validate_asset_identity(directory: Path, name: str, role: str, manifest: dict[str, Any]) -> None:
    path = directory / "ava-asset.json"
    if not path.is_file():
        raise AvaError("IDENTITY_MISMATCH", f"{name} has no ava-asset.json")
    identity = json.loads(path.read_text())
    expected = {
        "asset_schema": 1,
        "asset_name": name,
        "asset_role": role,
        "ava_version": manifest["ava_version"],
        "tag": manifest["tag"],
        "channel": manifest["channel"],
        "source_repository": REPOSITORY,
        "source_revision": manifest["source_revision"],
    }
    if identity != expected:
        raise AvaError("IDENTITY_MISMATCH", f"archive identity mismatch: {name}")


def run_gh(args: list[str]) -> None:
    try:
        result = subprocess.run(args, check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError as exc:
        raise AvaError("VERIFICATION_UNAVAILABLE", "verified mode requires GitHub CLI") from exc
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "GitHub verification failed"
        raise AvaError("AUTHENTICITY_FAILURE", message)


def locate_asset_directory(base: Path, version: str, target_version: str) -> Path:
    candidates: list[Path] = []
    if version == target_version and (base / "ava-release.json").is_file():
        candidates.append(base)
    candidates.extend((base / f"v{version}", base.parent / f"v{version}"))
    for candidate in candidates:
        if (candidate / "ava-release.json").is_file():
            return candidate.resolve()
    raise AvaError("MISSING_ASSETS", f"cannot locate local assets for v{version}")


