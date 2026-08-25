from __future__ import annotations

import os
import re
import shlex
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
LAUNCHER = REPOSITORY_ROOT / "internal/release/qualify-release-detached.sh"


class QualificationDetachedTests(unittest.TestCase):
    @staticmethod
    def wait_until(predicate, *, timeout: float = 5.0) -> None:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if predicate():
                return
            time.sleep(0.05)
        raise AssertionError("condition did not become true before timeout")

    @unittest.skipUnless(
        hasattr(os, "setsid") and shutil.which("setsid") and shutil.which("nohup"),
        "detachment test requires Unix setsid and nohup",
    )
    def test_detached_child_survives_parent_process_group_sighup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            release_root = root / "repo/internal/release"
            release_root.mkdir(parents=True)
            launcher = release_root / "qualify-release-detached.sh"
            shutil.copy2(LAUNCHER, launcher)

            marker = root / "marker.txt"
            fake_qualification = release_root / "qualify-release.sh"
            fake_qualification.write_text(
                "#!/bin/sh\n"
                "set -eu\n"
                "printf 'started\\n' >> \"$AVA_DETACH_TEST_MARKER\"\n"
                "sleep 2\n"
                "printf 'completed\\n' >> \"$AVA_DETACH_TEST_MARKER\"\n",
                encoding="utf-8",
            )
            fake_qualification.chmod(0o755)

            external_root = root / "external"
            external_root.mkdir()
            launcher_output = root / "launcher.out"
            environment = os.environ.copy()
            environment["AVA_DETACH_TEST_MARKER"] = str(marker)
            environment["AVA_QUALIFICATION_RUN_ROOT_PARENT"] = str(external_root)

            command = (
                f"sh {shlex.quote(str(launcher))} --target-assets /tmp/fake "
                f"> {shlex.quote(str(launcher_output))} 2>&1; sleep 30"
            )
            parent = subprocess.Popen(
                ["sh", "-c", command],
                env=environment,
                preexec_fn=os.setsid,
            )
            child_pid: int | None = None
            try:
                self.wait_until(
                    lambda: launcher_output.is_file()
                    and "qualification PID:" in launcher_output.read_text(encoding="utf-8")
                    and marker.is_file()
                    and "started" in marker.read_text(encoding="utf-8")
                )
                output = launcher_output.read_text(encoding="utf-8")
                match = re.search(r"qualification PID: (\d+)", output)
                self.assertIsNotNone(match)
                child_pid = int(match.group(1))

                os.killpg(parent.pid, signal.SIGHUP)
                time.sleep(0.1)
                os.kill(child_pid, 0)

                self.wait_until(
                    lambda: marker.is_file()
                    and "completed" in marker.read_text(encoding="utf-8")
                )
            finally:
                try:
                    os.killpg(parent.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                if child_pid is not None:
                    try:
                        os.kill(child_pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass


if __name__ == "__main__":
    unittest.main()
