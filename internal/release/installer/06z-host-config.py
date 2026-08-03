OPENCODE_PROJECT_CONFIG = {
    "$schema": "https://opencode.ai/config.json",
    "permission": {
        "read": {".ava/**": "allow"},
        "edit": {".ava/**": "ask"},
    },
}


def existing_opencode_configs(root: Path) -> list[str]:
    paths = (root / "opencode.json", root / "opencode.jsonc")
    return [path.name for path in paths if path.exists() or path.is_symlink()]


def print_opencode_guidance(existing: list[str], *, json_output: bool) -> None:
    if json_output:
        print(
            json.dumps(
                {
                    "type": "host-config",
                    "host": "opencode",
                    "operation": "skipped",
                    "existing": existing,
                    "merge": OPENCODE_PROJECT_CONFIG,
                },
                sort_keys=True,
            )
        )
        return

    if existing:
        paths = ", ".join(f"./{path}" for path in existing)
        print(f"OpenCode configuration was not installed because {paths} already exists.")
    else:
        print("OpenCode configuration could not be installed automatically.")
    print("Ava installation completed. Merge this configuration manually if needed:")
    print(json.dumps(OPENCODE_PROJECT_CONFIG, indent=2, sort_keys=True))


def install_host_configuration(root: Path, *, dry_run: bool, json_output: bool) -> None:
    if AVA_HOST_SELECTION == "none":
        if dry_run and not json_output:
            print("HOST CONFIG  none")
        return

    existing = existing_opencode_configs(root)
    if existing:
        print_opencode_guidance(existing, json_output=json_output)
        return

    if dry_run:
        if json_output:
            print(json.dumps({"type": "host-config", "host": "opencode", "operation": "create", "path": "./opencode.json"}, sort_keys=True))
        else:
            print("HOST CONFIG  create ./opencode.json [project-owned]")
        return

    config_path = root / "opencode.json"
    try:
        with config_path.open("x") as handle:
            json.dump(OPENCODE_PROJECT_CONFIG, handle, indent=2, sort_keys=True)
            handle.write("\n")
    except FileExistsError:
        print_opencode_guidance(existing_opencode_configs(root), json_output=json_output)
        return
    except OSError as exc:
        if not json_output:
            print(f"WARNING: OpenCode configuration could not be written: {exc}")
        print_opencode_guidance([], json_output=json_output)
        return

    if json_output:
        print(json.dumps({"type": "host-config", "host": "opencode", "operation": "created", "path": "./opencode.json"}, sort_keys=True))
    else:
        print("Installed project-owned OpenCode configuration at ./opencode.json.")


perform_install_without_host_configuration = perform_install


def perform_install(args: argparse.Namespace) -> None:
    perform_install_without_host_configuration(args)
    install_host_configuration(
        args.target.expanduser().resolve(),
        dry_run=args.dry_run,
        json_output=args.json,
    )
