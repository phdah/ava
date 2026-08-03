def extract_host_selection(argv: list[str]) -> tuple[str, list[str]]:
    selected = "opencode"
    cleaned = [argv[0]]
    seen = False
    index = 1

    def fail(message: str) -> None:
        if "--json" in argv:
            print(
                json.dumps(
                    {"type": "error", "code": "INVALID_ARGUMENT", "message": message},
                    sort_keys=True,
                ),
                file=sys.stderr,
            )
            raise SystemExit(1)
        raise SystemExit(f"ERROR [INVALID_ARGUMENT]: {message}")

    while index < len(argv):
        argument = argv[index]
        if argument == "--host":
            if seen:
                fail("--host may be supplied only once")
            if index + 1 >= len(argv):
                fail("--host requires one of: opencode, none")
            selected = argv[index + 1]
            seen = True
            index += 2
            continue
        if argument.startswith("--host="):
            if seen:
                fail("--host may be supplied only once")
            selected = argument.partition("=")[2]
            seen = True
            index += 1
            continue
        cleaned.append(argument)
        index += 1

    if selected not in {"opencode", "none"}:
        fail(f"unsupported host configuration: {selected}; expected opencode or none")
    return selected, cleaned


AVA_HOST_SELECTION, sys.argv[:] = extract_host_selection(sys.argv)
