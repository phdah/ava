from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from internal.release import qualification_state as state


class QualificationStateTests(unittest.TestCase):
    def test_checked_in_configuration_has_one_active_operation(self) -> None:
        config, catalog, current = state.load_configuration()
        self.assertEqual(set(config), {"schema_version", "repository", "active_pair"})
        self.assertEqual(config["repository"], "phdah/ava")
        pairs = {item["id"]: item for item in catalog["pairs"]}
        self.assertEqual(set(pairs), {"bootstrap-to-1.0.0"})
        self.assertEqual(config["active_pair"], "bootstrap-to-1.0.0")
        self.assertEqual(current["active_pair"], config["active_pair"])
        active = pairs[config["active_pair"]]
        self.assertFalse(active["historical"])
        self.assertEqual(active["source"], {"kind": "bootstrap", "version": "0.0.0"})
        self.assertEqual(active["target"]["kind"], "local")
        self.assertEqual(active["target"]["version"], "1.0.0")
        self.assertEqual(current["release_acceptance"], {})

    def test_config_schema_has_no_agent_runtime_configuration(self) -> None:
        schema = state.load_json(
            state.REPOSITORY_ROOT
            / "internal/release/qualification/schemas/config.schema.json"
        )
        self.assertEqual(
            set(schema["properties"]),
            {"schema_version", "repository", "active_pair"},
        )

    def test_mutable_release_aliases_are_refused(self) -> None:
        for value in ("latest", "v1.0.0/latest", "LATEST"):
            with self.assertRaises(state.QualificationStateError):
                state.reject_mutable_tag(value)

    def test_schema_validator_rejects_unexpected_fields(self) -> None:
        schema = {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_version"],
            "properties": {"schema_version": {"const": 1, "type": "integer"}},
        }
        with self.assertRaises(state.QualificationStateError):
            state.validate_schema(
                {"schema_version": 1, "unexpected": True},
                schema,
                label="test",
            )

    def test_tree_digest_changes_with_content(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "file.txt"
            path.write_text("first\n", encoding="utf-8")
            first = state.tree_digest(root)
            path.write_text("second\n", encoding="utf-8")
            second = state.tree_digest(root)
            self.assertNotEqual(first, second)

    def test_run_ids_are_bound_to_operation(self) -> None:
        run_id = state.utc_run_id("stable100-to-stable101-local")
        self.assertTrue(run_id.endswith("-stable100-to-stable101-local"))


if __name__ == "__main__":
    unittest.main()
