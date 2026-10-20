"""Regression checks for installation boundaries and refusal to overwrite."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("clearweave_installer", ROOT / "tools/install_skill.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def test_copies_real_skill_and_preserves_existing_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            result = installer.install(project)
            self.assertEqual((result / "SKILL.md").read_bytes(), (ROOT / "skills/clearweave/SKILL.md").read_bytes())
            marker = result / "local-note.txt"
            marker.write_text("keep this")
            with self.assertRaises(FileExistsError):
                installer.install(project)
            self.assertEqual(marker.read_text(), "keep this")

    def test_rejects_parent_symlink_outside_project(self):
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            project, outside = parent / "project", parent / "outside"
            project.mkdir()
            outside.mkdir()
            (project / ".agents").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(project)
            self.assertEqual(list(outside.iterdir()), [])

    def test_rejects_non_directory_project(self):
        with tempfile.TemporaryDirectory() as directory:
            file = Path(directory) / "file"
            file.write_text("content")
            with self.assertRaises(ValueError):
                installer.install(file)


if __name__ == "__main__":
    unittest.main()
