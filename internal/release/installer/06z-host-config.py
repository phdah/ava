OPENCODE_PROJECT_CONFIG = {
    "$schema": "https://opencode.ai/config.json",
    "permission": {
        "read": {
            "AGENTS.md": "allow",
            ".ava/**": "allow",
        },
        "edit": {
            "AGENTS.md": "ask",
            ".ava/**": "ask",
        },
    },
}


def print_opencode_merge_guidance(existing: list[str], *, json_output: bool, reason: str) -> None:
    if json_output:
        print(
            json.dumps(
                {
                    "type": "host-config",
                    "host": "opencode",
                    "operation": "skipped",
                    "reason": reason,
                    "existing": existing,
                    "merge": OPENCODE_PROJECT_CONFIG,
                },
                sort_keys=True,
            )
        )
        return

    if existing:
        joined = ", ".join(f"./{path}" for path in existing)
        print(f"OpenCode configuration was not installed because {joined} already exists.")
    else:
        print("OpenCode configuration could not be installed automatically.")
    print("Ava installation completed. Merge this configuration manually if needed:")
    print(json.dumps(OPENCODE_PROJECT_CONFIG, indent=2, sort_keys=True))


def install_host_configuration(
    root: Path,
    selection: str,
    *,
    dry_run: bool,
    json_output: bool,
) -> None:
    if selection == "none":
        if json_output:
            print(json.dumps({"type": "host-config", "host": "none", "operation": "skip"}, sort_keys=True))
        elif dry_run:
            print("HOST CONFIG  none")
        return

    config_path = root / "opencode.json"
    candidates = (root / "opencode.json", root / "opencode.jsonc")
    existing = [path.name for path in candidates if path.exists() or path.is_symlink()]
    if existing:
        print_opencode_merge_guidance(existing, json_output=json_output, reason="existing-config")
        return

    if dry_run:
        if json_output:
            print(
                json.dumps(
                    {
                        "type": "host-config",
                        "host": "opencode",
                        "operation": "create",
                        "path": "./opencode.json",
                    },
                    sort_keys=True,
                )
            )
        else:
            print("HOST CONFIG  create ./opencode.json [project-owned]")
        return

    data = (json.dumps(OPENCODE_PROJECT_CONFIG, indent=2, sort_keys=True) + "\n").encode()
    try:
        descriptor = os.open(config_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    except FileExistsError:
        existing = [path.name for path in candidates if path.exists() or path.is_symlink()]
        print_opencode_merge_guidance(existing, json_output=json_output, reason="existing-config")
        return
    except OSError as exc:
        if json_output:
            print(
                json.dumps(
                    {
                        "type": "host-config",
                        "host": "opencode",
                        "operation": "skipped",
                        "reason": "write-failed",
                        "message": str(exc),
                        "merge": OPENCODE_PROJECT_CONFIG,
                    },
                    sort_keys=True,
                )
            )
        else:
            print(f"WARNING: OpenCode configuration could not be written: {exc}")
            print_opencode_merge_guidance([], json_output=False, reason="write-failed")
        return

    if json_output:
        print(
            json.dumps(
                {
                    "type": "host-config",
                    "host": "opencode",
                    "operation": "created",
                    "path": "./opencode.json",
                    "ownership": "project-owned",
                },
                sort_keys=True,
            )
        )
    else:
        print("Installed project-owned OpenCode configuration at ./opencode.json.")


perform_install_without_host_configuration = perform_install


def perform_install(args: argparse.Namespace) -> None:
    perform_install_without_host_configuration(args)
    install_host_configuration(
        args.target.expanduser().resolve(),
        AVA_HOST_SELECTION,
        dry_run=args.dry_run,
        json_output=args.json,
    )
