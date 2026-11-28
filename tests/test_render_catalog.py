"""Keep generated documentation and its bilingual navigation reproducible."""
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cw_render_catalog", ROOT / "tools/render_catalog.py")
render_catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_catalog)


class RenderCatalogTests(unittest.TestCase):
    def copy_catalog(self) -> Path:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for name in ("tools/render_catalog.py", "skills/clearweave/assets/capabilities.json",
                     "docs/source-audit.json", "docs/feature-map.json",
                     "docs/capabilities.md", "README.md", "README.zh-CN.md"):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        return root

    def render(self, root: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(root / "tools/render_catalog.py"), *args],
                              capture_output=True, text=True)

    def test_tracked_generated_documents_are_current(self):
        self.assertEqual(render_catalog.stale_documents(), [])

    def test_capability_atlas_retains_resolving_bilingual_navigation(self):
        document = render_catalog.expected_documents()["docs/capabilities.md"]
        self.assertIn("[简体中文](capabilities.zh-CN.md)", document)
        self.assertIn("[Documentation index](README.md)", document)
        self.assertTrue((ROOT / "docs/capabilities.zh-CN.md").is_file())
        self.assertTrue((ROOT / "docs/README.md").is_file())

    def test_navigation_and_authored_notes_do_not_trigger_drift(self):
        root = self.copy_catalog()
        atlas = root / "docs/capabilities.md"
        text = atlas.read_text(encoding="utf-8")
        amended = text.replace("[Documentation index]", "[Documentation and usage guides]", 1)
        amended += f"\n## Maintainer notes\n\nAdd examples outside the `{render_catalog.START}` block.\n"
        atlas.write_text(amended, encoding="utf-8")
        for args in ((), ("--write",)):
            result = self.render(root, *args)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(atlas.read_text(encoding="utf-8"), amended)

    def test_generated_content_drift_remains_an_error(self):
        root = self.copy_catalog()
        atlas = root / "docs/capabilities.md"
        text = atlas.read_text(encoding="utf-8")
        atlas.write_text(text.replace(render_catalog.START, render_catalog.START + "\nUnrendered change", 1),
                         encoding="utf-8")
        with patch.object(render_catalog, "ROOT", root):
            self.assertEqual(render_catalog.stale_documents(), ["docs/capabilities.md"])

    def test_new_capability_refreshes_tables_without_removing_notes(self):
        root = self.copy_catalog()
        atlas = root / "docs/capabilities.md"
        note = "\nA note about when to use the new capability.\n"
        atlas.write_text(atlas.read_text(encoding="utf-8") + note, encoding="utf-8")
        catalog = root / "skills/clearweave/assets/capabilities.json"
        data = json.loads(catalog.read_text(encoding="utf-8"))
        new_capability = dict(data["capabilities"][-1], id="CW999", name_en="Example capability",
                              name_zh="示例能力")
        data["capabilities"].append(new_capability)
        catalog.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

        stale = self.render(root)
        self.assertEqual(stale.returncode, 1, stale.stderr)
        self.assertIn("docs/capabilities.md, README.md, README.zh-CN.md", stale.stderr)
        result = self.render(root, "--write")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(atlas.read_text(encoding="utf-8").endswith(note))
        for name, label in (("docs/capabilities.md", "Example capability"), ("README.md", "Example capability"),
                            ("README.zh-CN.md", "示例能力")):
            self.assertIn(f"**CW999** {label}", (root / name).read_text(encoding="utf-8"))
        self.assertEqual(self.render(root).returncode, 0)


if __name__ == "__main__":
    unittest.main()
