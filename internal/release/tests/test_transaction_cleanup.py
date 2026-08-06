from __future__ import annotations

import unittest

from internal.release.tests import test_installer


class TransactionCleanupTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixture = test_installer.InstallerTests(methodName="runTest")
        self.fixture.setUp()
        self.addCleanup(self.fixture.tearDown)

    @property
    def transaction_container(self):
        return self.fixture.target / ".ava/state/transactions"

    def build_upgrade(self, *, semantic: bool = False, guidance: bool = False):
        first = self.fixture.build("0.1.0")
        self.fixture.install(first)
        (self.fixture.repo / "templates/base/AGENTS.md").write_text("# Router 0.2.0\n")
        return self.fixture.build(
            "0.2.0",
            upgrade_from=["0.1.0"],
            semantic=semantic,
            guidance=guidance,
        )

    def test_successful_upgrade_removes_empty_transaction_container(self) -> None:
        second = self.build_upgrade()
        self.fixture.install(second)
        self.assertFalse(self.transaction_container.exists())

    def test_active_semantic_transaction_is_preserved_until_rollback(self) -> None:
        second = self.build_upgrade(semantic=True, guidance=True)
        self.fixture.install(second)
        self.assertTrue(self.transaction_container.is_dir())
        self.assertEqual(len(list(self.transaction_container.iterdir())), 1)
        self.fixture.install(second, "--rollback")
        self.assertFalse(self.transaction_container.exists())

    def test_non_empty_transaction_container_is_preserved(self) -> None:
        second = self.build_upgrade()
        preserved = self.transaction_container / "other-transaction"
        preserved.mkdir(parents=True)
        recovery = preserved / "recovery.json"
        recovery.write_text("{}\n")
        self.fixture.install(second)
        self.assertTrue(recovery.is_file())
        self.assertEqual(
            sorted(path.name for path in self.transaction_container.iterdir()),
            ["other-transaction"],
        )


if __name__ == "__main__":
    unittest.main()
