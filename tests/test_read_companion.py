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
ACADEMIC_SKILLS = {
    "academic-humanizer": b"---\nname: academic-humanizer\n---\n# Mathematics rules\n",
    "academic-humanizer-evidence": b"---\nname: academic-humanizer\n---\n# Evidence rules\n",
}


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

    def test_nested_repository_uses_skill_directory_locally(self):
        companion = COMPANION._replace(skill_root="skills/writing")
        with TemporaryDirectory() as directory, patch.object(reader, "fetch", return_value=SKILL) as fetch:
            root = Path(directory)
            (root / "SKILL.md").write_bytes(SKILL)
            self.assertEqual(reader.read_rules(companion, "skill", root, True)[0].encode(), SKILL)
            fetch.assert_not_called()
            reader.read_rules(companion, "skill", None, False)
            fetch.assert_called_once_with(
                f"https://raw.githubusercontent.com/example/writing/{'a' * 40}/skills/writing/SKILL.md")

    def test_same_name_academic_forks_are_selected_by_digest(self):
        companions = {name: reader.COMPANIONS[name]._replace(skill_digest=sha256(data).hexdigest())
                      for name, data in ACADEMIC_SKILLS.items()}
        for evidence_directory in ("academic-humanizer", "academic-humanizer-evidence"):
            with self.subTest(directory=evidence_directory), TemporaryDirectory() as directory:
                root = Path(directory)
                skills_dir = root / "project/.agents/skills"
                for folder, content in (
                    (skills_dir / "academic-humanizer", ACADEMIC_SKILLS["academic-humanizer"]),
                    (skills_dir / "academic-humanizer-evidence", ACADEMIC_SKILLS["academic-humanizer"]),
                    (root / "user/.agents/skills" / evidence_directory,
                     ACADEMIC_SKILLS["academic-humanizer-evidence"]),
                ):
                    folder.mkdir(parents=True)
                    (folder / "SKILL.md").write_bytes(content)
                with (
                    patch.object(reader, "__file__", str(skills_dir / "clearweave/scripts/read_companion.py")),
                    patch.object(reader.Path, "home", return_value=root / "user"),
                    patch.object(reader.Path, "cwd", return_value=root / "project"),
                    patch.dict(reader.os.environ, {"CODEX_HOME": str(root / "codex")}),
                    patch.dict(reader.COMPANIONS, companions),
                    patch.object(reader, "fetch") as fetch,
                ):
                    for name, content in ACADEMIC_SKILLS.items():
                        out, err = Mock(buffer=BytesIO()), StringIO()
                        with patch.object(reader.sys, "stdout", out), redirect_stderr(err):
                            status = reader.main([name, "--offline"])
                        self.assertEqual(status, 0, err.getvalue())
                        self.assertEqual(out.buffer.getvalue(), content)
                        self.assertIn(f"local {companions[name].repo}@{companions[name].commit}/", err.getvalue())
                    fetch.assert_not_called()

    def test_academic_wrong_fork_requires_selected_pinned_source(self):
        pins = {
            "academic-humanizer": (
                "https://raw.githubusercontent.com/junbolian/Academic-Humanizer/"
                "62b0a02627e063015466c70f0a4dd4929a9f7f5b/academic-humanizer/SKILL.md",
                "fa41c41363c0fed74ca90082ab5c7928a1f98e4710f461d8f11e06792e7b20c8"),
            "academic-humanizer-evidence": (
                "https://raw.githubusercontent.com/AIScientists-Dev/academic-humanizer/"
                "94b88b23703bed7df507acae7d6d5876209a0cdf/SKILL.md",
                "1f4501cb7331cffe9018960f8db045c719eea0658ce04e4af5e273ee59785a9c"),
        }
        for name, (url, digest) in pins.items():
            with self.subTest(name=name), TemporaryDirectory() as directory:
                registered = reader.COMPANIONS[name]
                self.assertEqual(registered.skill_digest, digest)
                data = ACADEMIC_SKILLS[name]
                companion = registered._replace(skill_digest=sha256(data).hexdigest())
                wrong = next(content for other, content in ACADEMIC_SKILLS.items() if other != name)
                root = Path(directory)
                (root / "SKILL.md").write_bytes(wrong)
                with patch.object(reader, "fetch") as fetch:
                    with self.assertRaisesRegex(ValueError, "no matching local copy"):
                        reader.read_rules(companion, "skill", root, True)
                    fetch.assert_not_called()
                    fetch.return_value = wrong
                    with self.assertRaisesRegex(ValueError, "upstream digest mismatch"):
                        reader.read_rules(companion, "skill", root, False)
                    fetch.assert_called_once_with(url)
                    fetch.reset_mock()
                    fetch.return_value = data
                    text, source = reader.read_rules(companion, "skill", root, False)
                    self.assertEqual(text.encode(), data)
                    self.assertTrue(source.startswith(f"upstream {registered.repo}@"))
                    fetch.assert_called_once_with(url)

    def test_examples_resource_has_own_digest_path_and_cli_option(self):
        companion = reader.COMPANIONS["academic-humanizer"]._replace(skill_digest=sha256(SKILL).hexdigest())
        key = (companion.repo, "examples")
        self.assertEqual(reader.RESOURCES[key], (
            "references/examples.md", "c59519e9ced2ebd5878b8547d86fc7b1b87fe7e2aee62fb1b9d0142490086f14"))
        examples = b"# Examples\nOriginal and revised manuscript paragraphs.\n"
        with (
            TemporaryDirectory() as directory,
            patch.dict(reader.COMPANIONS, {"academic-humanizer": companion}),
            patch.dict(reader.RESOURCES, {key: ("references/examples.md", sha256(examples).hexdigest())}),
            patch.object(reader, "fetch") as fetch,
        ):
            root = Path(directory)
            (root / "SKILL.md").write_bytes(SKILL)
            target = root / "references/examples.md"
            target.parent.mkdir()
            for content in (None, SKILL, examples):
                with self.subTest(content=content):
                    if content is not None:
                        target.write_bytes(content)
                    out, err = Mock(buffer=BytesIO()), StringIO()
                    with patch.object(reader.sys, "stdout", out), redirect_stderr(err):
                        status = reader.main(["academic-humanizer", "--resource", "examples",
                                              "--offline", "--local", str(root)])
                    self.assertEqual(status, 0 if content == examples else 1, err.getvalue())
                    self.assertEqual(out.buffer.getvalue(), examples if content == examples else b"")
            fetch.assert_not_called()
            target.unlink()
            fetch.return_value = examples
            text, source = reader.read_rules(companion, "examples", root, False)
            self.assertEqual(text.encode(), examples)
            self.assertTrue(source.endswith("/academic-humanizer/references/examples.md"))
            fetch.assert_called_once_with(
                "https://raw.githubusercontent.com/junbolian/Academic-Humanizer/"
                "62b0a02627e063015466c70f0a4dd4929a9f7f5b/academic-humanizer/references/examples.md")
            fetch.return_value = SKILL
            with self.assertRaisesRegex(ValueError, "upstream digest mismatch"):
                reader.read_rules(companion, "examples", root, False)

    def test_unsupported_resources_fail_before_fetch(self):
        with patch.object(reader, "fetch") as fetch:
            for name in ("humanizer", "humanizer-zh", "zh-tw-humanizer"):
                with self.subTest(name=name), self.assertRaisesRegex(ValueError, "no pinned academic"):
                    reader.read_rules(reader.COMPANIONS[name], "academic", None, False)
            with self.assertRaisesRegex(ValueError, "no pinned"):
                reader.read_rules(COMPANION, "../SKILL.md", None, False)
            with self.assertRaisesRegex(ValueError, "no pinned examples"):
                reader.read_rules(reader.COMPANIONS["academic-humanizer-evidence"], "examples", None, False)
            fetch.assert_not_called()


if __name__ == "__main__":
    unittest.main()
