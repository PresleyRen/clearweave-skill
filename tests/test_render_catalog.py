"""Keep generated documentation and its bilingual navigation reproducible."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cw_render_catalog", ROOT / "tools/render_catalog.py")
render_catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_catalog)


class RenderCatalogTests(unittest.TestCase):
    def test_tracked_generated_documents_are_current(self):
        self.assertEqual(render_catalog.stale_documents(), [])

    def test_capability_atlas_retains_resolving_bilingual_navigation(self):
        document = render_catalog.expected_documents()["docs/capabilities.md"]
        self.assertIn("[简体中文](capabilities.zh-CN.md)", document)
        self.assertIn("[Documentation index](README.md)", document)
        self.assertTrue((ROOT / "docs/capabilities.zh-CN.md").is_file())
        self.assertTrue((ROOT / "docs/README.md").is_file())

    def test_generated_content_drift_remains_an_error(self):
        expected = render_catalog.expected_documents()
        expected["docs/capabilities.md"] += "\nUnrendered change\n"
        with patch.object(render_catalog, "expected_documents", return_value=expected):
            self.assertEqual(render_catalog.stale_documents(), ["docs/capabilities.md"])


if __name__ == "__main__":
    unittest.main()
