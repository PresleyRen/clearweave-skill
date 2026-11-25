"""Exercise companion lookup, source identity, offline handling and pinned resources."""
import importlib.util
from contextlib import redirect_stderr
from hashlib import sha256
from io import BytesIO, StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/clearweave/scripts/read_companion.py"
spec = importlib.util.spec_from_file_location("cw_read_companion", SCRIPT)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)

SKILL = "# Writing\n写正文\n".encode()
ACADEMIC = b"# Academic guidance\n"
COMPANION = reader.Companion("example/writing", "a" * 40, sha256(SKILL).hexdigest(),
                             sha256(ACADEMIC).hexdigest())


class CompanionTests(unittest.TestCase):
    def test_cli_skips_wrong_sibling_then_loads_personal_installation(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            skills_dir = root / "project/.agents/skills"
            sibling = skills_dir / "humanizer"
            personal = root / "user/.agents/skills/humanizer"
            for folder, content in [(sibling, b"another fork"), (personal, SKILL)]:
                folder.mkdir(parents=True)
                (folder / "SKILL.md").write_bytes(content)
            script = skills_dir / "clearweave/scripts/read_companion.py"
            with (
                patch.object(reader, "__file__", str(script)),
                patch.object(reader.Path, "home", return_value=root / "user"),
                patch.object(reader.Path, "cwd", return_value=root / "project"),
                patch.dict(reader.COMPANIONS, {"humanizer": COMPANION}),
                patch.object(reader, "fetch") as fetch,
            ):
                for switches in ([], ["--offline"], ["--offline", "--local", str(sibling)]):
                    with self.subTest(switches=switches):
                        out, err = Mock(buffer=BytesIO()), StringIO()
                        with patch.object(reader.sys, "stdout", out), redirect_stderr(err):
                            status = reader.main(["humanizer", *switches])
                        if "--local" in switches:
                            self.assertNotEqual(status, 0)
                            self.assertEqual(out.buffer.getvalue(), b"")
                            self.assertIn("no matching local copy", err.getvalue())
                        else:
                            self.assertEqual(status, 0)
                            self.assertEqual(out.buffer.getvalue(), SKILL)
                            self.assertIn("local example/writing@", err.getvalue())
                fetch.assert_not_called()

    def test_installed_pin_returns_exact_markdown_without_network(self):
        with TemporaryDirectory() as directory, patch.object(reader, "fetch") as fetch:
            root = Path(directory)
            (root / "SKILL.md").write_bytes(SKILL)
            text, source = reader.read_rules(COMPANION, "skill", root, False)
            self.assertEqual(text.encode(), SKILL)
            self.assertEqual(source, f"local example/writing@{'a' * 40}/SKILL.md")
            fetch.assert_not_called()

    def test_missing_or_other_fork_offline_never_reads_remote(self):
        with TemporaryDirectory() as directory, patch.object(reader, "fetch") as fetch:
            root = Path(directory)
            for data in (None, b"# Another skill with the same name"):
                with self.subTest(data=data):
                    if data is not None:
                        (root / "SKILL.md").write_bytes(data)
                    with self.assertRaisesRegex(ValueError, "no matching local copy"):
                        reader.read_rules(COMPANION, "skill", root, True)
            fetch.assert_not_called()

    def test_mismatched_local_uses_only_the_pinned_upstream_url(self):
        with TemporaryDirectory() as directory, patch.object(reader, "fetch", return_value=SKILL) as fetch:
            root = Path(directory)
            local = root / "SKILL.md"
            local.write_bytes(b"newer local rules")
            text, source = reader.read_rules(COMPANION, "skill", root, False)
            self.assertEqual(text.encode(), SKILL)
            self.assertTrue(source.startswith("upstream "))
            self.assertEqual(local.read_bytes(), b"newer local rules")
            fetch.assert_called_once_with(f"https://raw.githubusercontent.com/example/writing/{'a' * 40}/SKILL.md")

    def test_remote_bytes_must_match_before_output(self):
        with patch.object(reader, "fetch", return_value=b"<html>gateway</html>"):
            with self.assertRaisesRegex(ValueError, "upstream digest mismatch"):
                reader.read_rules(COMPANION, "skill", None, False)

    def test_academic_uses_its_own_path_and_digest(self):
        with patch.object(reader, "fetch", return_value=ACADEMIC) as fetch:
            text, source = reader.read_rules(COMPANION, "academic", None, False)
            self.assertEqual(text.encode(), ACADEMIC)
            self.assertTrue(source.endswith("/references/academic-zh.md"))
            fetch.assert_called_once_with(
                f"https://raw.githubusercontent.com/example/writing/{'a' * 40}/references/academic-zh.md")

    def test_unsupported_resources_fail_before_fetch(self):
        with patch.object(reader, "fetch") as fetch:
            for name in ("humanizer", "humanizer-zh", "zh-tw-humanizer"):
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "no pinned academic"):
                    reader.read_rules(reader.COMPANIONS[name], "academic", None, False)
            with self.assertRaisesRegex(ValueError, "no pinned"):
                reader.read_rules(COMPANION, "../SKILL.md", None, False)
            fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
