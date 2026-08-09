from __future__ import annotations

import unittest
from pathlib import Path

from internal.release.release_catalog import (
    read_catalog,
    read_release_chain,
    read_release_record,
)


ROOT = Path(__file__).resolve().parents[3]


class ReleaseCatalogHistoryTests(unittest.TestCase):
    def test_every_alpha_release_has_exactly_one_local_edge_record(self) -> None:
        targets = [f"1.0.0-alpha.{number}" for number in range(1, 13)]
        expected_sources = ["0.0.0", *targets[:-1]]

        chain = read_release_chain(ROOT, targets[-1])

        self.assertEqual(targets, [record["target_version"] for record in chain])
        self.assertEqual(
            expected_sources,
            [record["edge"]["from"] for record in chain],
        )
        self.assertEqual(
            targets,
            [record["edge"]["to"] for record in chain],
        )

        for target in targets:
            with self.subTest(target=target):
                path = ROOT / f"internal/release/catalogs/{target}.json"
                self.assertTrue(path.is_file(), f"missing release record: {path}")
                record = read_release_record(ROOT, target)
                self.assertEqual(
                    {
                        "catalog_schema",
                        "target_version",
                        "edge",
                        "guidance",
                        "retired_sources",
                    },
                    set(record),
                )
                self.assertNotIn("edges", record)
                self.assertNotIn("supported_sources", record)

    def test_alpha_12_composes_all_published_alpha_sources(self) -> None:
        catalog = read_catalog(ROOT, "1.0.0-alpha.12")
        self.assertEqual(
            [f"1.0.0-alpha.{number}" for number in range(1, 12)],
            catalog["supported_sources"],
        )
        self.assertEqual(12, len(catalog["edges"]))


if __name__ == "__main__":
    unittest.main()
