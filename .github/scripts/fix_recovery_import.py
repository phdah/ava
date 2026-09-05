from pathlib import Path

root = Path(__file__).resolve().parents[2]
workflow_path = root / ".github/workflows/release-please.yml"
test_path = root / "internal/release/tests/test_publication_workflow.py"

workflow = workflow_path.read_text(encoding="utf-8")
old = 'PYTHONPATH="$GITHUB_WORKSPACE/tooling" \\\n            python3 -m internal.release.publication \\\n'
new = 'python3 "$GITHUB_WORKSPACE/tooling/internal/release/publication.py" \\\n'
count = workflow.count(old)
if count != 5:
    raise SystemExit(f"expected 5 maintained publication module invocations, found {count}")
workflow = workflow.replace(old, new)
workflow_path.write_text(workflow, encoding="utf-8")

tests = test_path.read_text(encoding="utf-8")
tests = tests.replace(
    '        self.assertIn("python3 -m internal.release.publication", WORKFLOW)\n',
    '        self.assertIn(\n'
    '            \'python3 "$GITHUB_WORKSPACE/tooling/internal/release/publication.py"\',\n'
    '            WORKFLOW,\n'
    '        )\n',
)
needle = '        self.assertNotIn("--clobber", WORKFLOW)\n'
replacement = (
    '        self.assertNotIn("--clobber", WORKFLOW)\n'
    '        self.assertNotIn("python3 -m internal.release.publication", WORKFLOW)\n'
    '        self.assertEqual(\n'
    '            WORKFLOW.count(\n'
    '                \'python3 "$GITHUB_WORKSPACE/tooling/internal/release/publication.py"\'\n'
    '            ),\n'
    '            5,\n'
    '        )\n'
)
if needle not in tests:
    raise SystemExit("publication workflow test insertion point missing")
tests = tests.replace(needle, replacement, 1)
test_path.write_text(tests, encoding="utf-8")
