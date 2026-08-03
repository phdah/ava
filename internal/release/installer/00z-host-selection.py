host_parser = argparse.ArgumentParser(add_help=False)
host_parser.add_argument("--host", choices=("opencode", "none"), default="opencode")
host_args, remaining_args = host_parser.parse_known_args()
AVA_HOST_SELECTION = host_args.host
sys.argv[:] = [sys.argv[0], *remaining_args]
