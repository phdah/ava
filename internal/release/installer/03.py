def fetch_bundle(version: str, args: argparse.Namespace, download_root: Path, target_version: str) -> Bundle:
    version = canonical_version(version)
    tag = f"v{version}"
    destination = download_root / tag
    destination.mkdir(parents=True, exist_ok=False)
    source_dir: Path | None = None
    if args.asset_dir:
        source_dir = locate_asset_directory(args.asset_dir.resolve(), version, target_version)
    if args.verified:
        run_gh(["gh", "release", "verify", tag, "--repo", REPOSITORY])

    for name in ASSETS:
        target = destination / name
        if source_dir:
            source = source_dir / name
            if not source.is_file():
                raise AvaError("MISSING_ASSETS", f"missing release asset: {source}")
            shutil.copyfile(source, target)
        else:
            url = f"https://github.com/{REPOSITORY}/releases/download/{tag}/{name}"
            try:
                with urllib.request.urlopen(url) as response, target.open("wb") as output:
                    shutil.copyfileobj(response, output)
            except (urllib.error.URLError, OSError) as exc:
                raise AvaError("DOWNLOAD_FAILED", f"failed to download {url}: {exc}") from exc
        if args.verified:
            run_gh(["gh", "release", "verify-asset", tag, str(target), "--repo", REPOSITORY])

    checksums = parse_checksums(destination / "SHA256SUMS")
    for name, expected in checksums.items():
        actual = sha256_file(destination / name)
        if actual != expected:
            raise AvaError("CHECKSUM_MISMATCH", f"checksum mismatch: {name}")
    manifest_path = destination / "ava-release.json"
    manifest_sha = sha256_file(manifest_path)
    manifest = json.loads(manifest_path.read_text())
    validate_release_manifest(manifest, version)
    assets_by_name = {item["name"]: item for item in manifest["assets"]}
    for name in ASSETS:
        item = assets_by_name[name]
        if name in ("ava-release.json", "SHA256SUMS"):
            continue
        path = destination / name
        if item["sha256"] != sha256_file(path) or item["size"] != path.stat().st_size:
            raise AvaError("ASSET_MISMATCH", f"asset metadata mismatch: {name}")

    embedded_version = os.environ.get("AVA_VERSION", "")
    if version == target_version and embedded_version == version:
        expected = {
            "AVA_TAG": manifest["tag"],
            "AVA_CHANNEL": manifest["channel"],
            "AVA_SOURCE_REVISION": manifest["source_revision"],
        }
        for key, value in expected.items():
            if os.environ.get(key) != value:
                raise AvaError("IDENTITY_MISMATCH", f"installer identity differs from selected release: {key}")

    base = destination / "base"
    guidance = destination / "guidance"
    migrations = destination / "migrations"
    safe_extract(destination / "ava-base.tar.gz", base)
    safe_extract(destination / "ava-guidance.tar.gz", guidance)
    safe_extract(destination / "ava-migrations.tar.gz", migrations)
    validate_asset_identity(base, "ava-base.tar.gz", "base", manifest)
    validate_asset_identity(guidance, "ava-guidance.tar.gz", "guidance", manifest)
    validate_asset_identity(migrations, "ava-migrations.tar.gz", "migrations", manifest)

    base_inventory = {item["source_path"]: item for item in manifest["installed_files"]}
    actual_base_files = {
        path.relative_to(base).as_posix()
        for path in base.rglob("*") if path.is_file() and path.name != "ava-asset.json"
    }
    if actual_base_files != set(base_inventory):
        raise AvaError("ASSET_MISMATCH", "base archive inventory differs from installed mapping")
    for source_path, item in base_inventory.items():
        if sha256_file(base / source_path) != item["sha256"]:
            raise AvaError("ASSET_MISMATCH", f"base archive file checksum mismatch: {source_path}")
    for item in manifest["guidance"]["entries"]:
        path = guidance / item["path"]
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            raise AvaError("ASSET_MISMATCH", f"guidance archive mismatch: {item['path']}")
    for item in manifest["migrations"]["files"]:
        path = migrations / item["path"]
        if not path.is_file() or sha256_file(path) != item["sha256"]:
            raise AvaError("ASSET_MISMATCH", f"migration archive mismatch: {item['path']}")
    for step in manifest["migrations"]["steps"]:
        descriptor_path = migrations / "descriptors" / f"{step['id']}.json"
        if not descriptor_path.is_file() or sha256_file(descriptor_path) != step["descriptor_sha256"]:
            raise AvaError("ASSET_MISMATCH", f"migration descriptor mismatch: {step['id']}")
        descriptor = read_json(descriptor_path, "ASSET_MISMATCH")
        expected_descriptor = {key: value for key, value in step.items() if key != "descriptor_sha256"}
        if descriptor != expected_descriptor:
            raise AvaError("ASSET_MISMATCH", f"migration descriptor content mismatch: {step['id']}")

    return Bundle(version, tag, destination, manifest, manifest_sha, base, guidance, migrations)


def find_edge(bundle: Bundle, source_version: str) -> dict[str, Any]:
    for edge in bundle.manifest["upgrade_paths"]["edges"]:
        if edge["from"] == source_version:
            return edge
    raise AvaError("UNSUPPORTED_TRANSITION", f"release {bundle.tag} does not support upgrade from {source_version}")


def resolve_bundles(source_version: str | None, target_version: str, args: argparse.Namespace, download_root: Path) -> tuple[list[Bundle], list[dict[str, Any]]]:
    target = fetch_bundle(target_version, args, download_root, target_version)
    if source_version is None:
        return [target], []
    edge = find_edge(target, source_version)
    versions = [*edge["intermediates"], target_version]
    bundles_by_version = {target_version: target}
    for version in versions[:-1]:
        bundles_by_version[version] = fetch_bundle(version, args, download_root, target_version)
    bundles = [bundles_by_version[version] for version in versions]
    edges: list[dict[str, Any]] = []
    current = source_version
    for bundle in bundles:
        adjacent = find_edge(bundle, current)
        if adjacent["mode"] != "direct" or adjacent["intermediates"]:
            raise AvaError("INVALID_UPGRADE_GRAPH", f"intermediate release {bundle.tag} lacks direct edge from {current}")
        edges.append(adjacent)
        current = bundle.version
    if current != target_version:
        raise AvaError("INVALID_UPGRADE_GRAPH", "upgrade path does not reach target")
    if edge["mode"] == "direct" and len(bundles) != 1:
        raise AvaError("INVALID_UPGRADE_GRAPH", "direct edge unexpectedly resolved intermediates")
    if edge["mode"] == "chained" and edge["intermediates"] != [bundle.version for bundle in bundles[:-1]]:
        raise AvaError("INVALID_UPGRADE_GRAPH", "chained edge intermediate order mismatch")
    return bundles, edges


def read_json(path: Path, code: str) -> Any:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as exc:
        raise AvaError(code, f"cannot read valid JSON from {path}: {exc}") from exc


def installed_payload(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {item["path"]: item for item in manifest["managed_files"] if item["kind"] == "payload"}


def load_installed_state(root: Path) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    ava = root / ".ava"
    manifest_path = ava / "state" / "manifest.json"
    upgrade_path = ava / "state" / "upgrade.json"
    if not ava.exists():
        return None, None
    if ava.is_symlink() or not ava.is_dir():
        raise AvaError("UNRECOGNIZED_AVA", "/.ava exists but is not a normal directory")
    if not manifest_path.is_file():
        raise AvaError("UNRECOGNIZED_AVA", "/.ava exists without a supported manifest")
    manifest = read_json(manifest_path, "INVALID_INSTALLED_STATE")
    validate_installed_manifest(manifest)
    if not upgrade_path.is_file():
        raise AvaError("INVALID_INSTALLED_STATE", "installed project has no upgrade.json")
    upgrade = read_json(upgrade_path, "INVALID_INSTALLED_STATE")
    if not isinstance(upgrade, dict) or upgrade.get("status") not in {"idle", "complete", "aborted", "rolled-back", "active", "blocked"}:
        raise AvaError("INVALID_INSTALLED_STATE", "invalid upgrade journal envelope")
    return manifest, upgrade


def select_bootstraps(target: Bundle, installed: dict[str, Any] | None, requested: list[str]) -> set[str]:
    available = {
        item["destination"] for item in target.manifest["installed_files"]
        if item["ownership"] == "ava-managed" and item["role"] == "bootstrap"
    }
    selected: set[str] = set()
    if installed:
        selected.update(
            item["path"] for item in installed["managed_files"]
            if item.get("kind") == "payload" and item.get("role") == "bootstrap" and item["path"] in available
        )
    for path in requested:
        destination_relative(path)
        if path not in available:
            raise AvaError("UNKNOWN_BOOTSTRAP", f"release does not declare host bootstrap: {path}")
        selected.add(path)
    return selected


def allowed_managed_destination(item: dict[str, Any]) -> None:
    path = item["destination"]
    role = item["role"]
    if role == "router" and path == "/AGENTS.md":
        return
    if role == "base" and path.startswith("/.ava/base/"):
        return
    if role == "bootstrap":
        return
    raise AvaError("INVALID_MANIFEST", f"managed mapping is outside allowed destinations: {path}")


