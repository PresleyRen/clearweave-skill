"""Deterministic checks of the local helper's stated, limited contract."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "clearweave" / "scripts" / "clearweave_check.py"
SPEC = importlib.util.spec_from_file_location("clearweave_check_under_test", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
checker = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = checker
SPEC.loader.exec_module(checker)


def literals(text: str, kind: str | None = None, custom=()) -> list[str]:
    return [span.literal for span in checker.collect_protected_spans(text, custom)
            if kind is None or span.kind == kind]


def cli(*args: str, input_text: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args], input=input_text,
                          capture_output=True, text=True, encoding="utf-8", check=False)


class LintTests(unittest.TestCase):
    def test_bilingual_candidates_have_source_coordinates(self):
        report = checker.lint_text("前言\n甲：值得注意的是，正文在后。\nIt is important to note that the limit applies.")
        self.assertEqual(report["candidate_count"], 2)
        self.assertEqual(report["languages_scanned"], ["en", "zh"])
        first, second = report["diagnostics"]
        self.assertEqual((first["rule_id"], first["line"], first["column"]), ("ZH002", 2, 3))
        self.assertEqual((second["rule_id"], second["line"], second["column"]), ("EN001", 3, 1))
        for item in report["diagnostics"]:
            self.assertEqual(set(item), {"rule_id", "line", "column", "excerpt", "reason"})
            self.assertTrue(item["reason"])

    def test_manual_language_filters_candidates(self):
        text = "值得注意的是。 It is worth noting that this remains a candidate."
        self.assertEqual(checker.lint_text(text, "en")["candidate_count"], 1)
        self.assertEqual(checker.lint_text(text, "zh")["candidate_count"], 1)
        self.assertEqual(checker.lint_text(text, "both")["candidate_count"], 2)
        with self.assertRaises(ValueError):
            checker.lint_text(text, "invalid")

    def test_legitimate_terms_grammar_and_punctuation_are_not_rules(self):
        text = ("This robust framework produced a statistically significant result. "
                "The samples were shuffled. We tested A, B, and C—under the same budget.\n"
                "第一组、第二组和第三组均被处理。保留必要重复——这是一项要求。")
        self.assertEqual(checker.lint_text(text)["candidate_count"], 0)

    def test_apostrophes_are_not_quotation_delimiters(self):
        text = "I don't mind the team's wording. It's important to note that the cap remains."
        self.assertEqual(literals(text, "quotation"), [])
        self.assertEqual(checker.lint_text(text)["candidate_count"], 1)

    def test_all_supported_quote_delimiters_skip_candidates(self):
        text = ('"It is worth noting that this is quoted."\n'
                '“值得注意的是。”\n「综上所述」\n『未来可期』')
        self.assertEqual(checker.lint_text(text)["candidate_count"], 0)
        self.assertEqual(len(literals(text, "quotation")), 4)

    def test_code_math_blockquotes_and_keep_skip_lint(self):
        text = ("```text\nIt is important to note that x = 2.\n```\n"
                "`值得注意的是`\n"
                "> In conclusion, this is a quotation.\n> 总而言之。\n"
                "$It is worth noting that$\n"
                "<!-- clearweave:keep -->未来可期<!-- /clearweave:keep -->")
        self.assertEqual(checker.lint_text(text, "both")["candidate_count"], 0)

    def test_frontmatter_only_at_document_start(self):
        yaml = "---\ntitle: It is worth noting that\n---\n"
        self.assertEqual(checker.lint_text(yaml)["candidate_count"], 0)
        self.assertEqual(checker.lint_text("Introduction\n" + yaml)["candidate_count"], 1)

    def test_currency_is_not_accidentally_a_math_region(self):
        text = "$20; it is important to note that the alternative costs $30."
        self.assertEqual(checker.lint_text(text)["candidate_count"], 1)
        self.assertEqual(literals(text, "math"), [])

    def test_protection_does_not_hide_adjacent_unprotected_sentence(self):
        text = '"It is important to note that" It is worth noting that this is outside.'
        report = checker.lint_text(text)
        self.assertEqual([item["rule_id"] for item in report["diagnostics"]], ["EN002"])

    def test_supported_traditional_word_forms_are_detected(self):
        report = checker.lint_text("綜上所述，未來可期。", "zh")
        self.assertEqual(report["candidate_count"], 2)
        self.assertTrue(report["semantic_review_required"])


class ProtectionTests(unittest.TestCase):
    def test_inner_structural_examples_do_not_hide_later_prose(self):
        tail = "It is worth noting that the cap remains.\n"
        cases = [
            ("yaml_fence", "---\nexample: |\n  ```\n---\n", "frontmatter"),
            ("yaml_keep", "---\nexample: <!-- clearweave:keep -->\n---\n", "frontmatter"),
            ("fence_keep", "```markdown\n<!-- clearweave:keep -->\n```\n", "fenced_code"),
            ("keep_fence", "<!-- clearweave:keep -->\n```\n<!-- /clearweave:keep -->\n", "keep"),
            ("inline_keep", "Example: `<!-- clearweave:keep -->`.\n", "inline_code"),
            ("multiline_inline_keep", "Example: `start\n<!-- clearweave:keep -->\nend`.\n", "inline_code"),
            ("blockquote_keep", "> <!-- clearweave:keep -->\n", "blockquote"),
        ]
        for name, prefix, kind in cases:
            with self.subTest(scope=name):
                text = prefix + tail
                report = checker.lint_text(text, "en")
                self.assertEqual([item["rule_id"] for item in report["diagnostics"]], ["EN002"])
                spans = checker.collect_protected_spans(text)
                self.assertEqual([span.kind for span in spans], [kind])
                self.assertLessEqual(spans[0].end, len(prefix))

    def test_secondary_delimiters_inside_code_cannot_extend_into_later_prose(self):
        tail = "It is worth noting that the cap remains.\n"
        for inner, ending in [('"', '"later quotation"'), (r"\[", r"\]")]:
            with self.subTest(inner=inner):
                text = "```text\n" + inner + "\n```\n" + tail + ending
                report = checker.lint_text(text, "en")
                self.assertEqual([item["rule_id"] for item in report["diagnostics"]], ["EN002"])

    def test_inline_code_does_not_pair_across_a_block_boundary(self):
        text = ("An unmatched `opener.\n\n```text\na later ` run\n```\n"
                "It is worth noting that the cap remains.")
        self.assertEqual([span.kind for span in checker.collect_protected_spans(text)], ["fenced_code"])
        self.assertEqual(checker.lint_text(text)["candidate_count"], 1)

    def test_inline_code_can_contain_a_shorter_backtick_run(self):
        text = "Use ``print('`')`` and then `x = 1`."
        self.assertEqual(literals(text, "inline_code"), ["``print('`')``", "`x = 1`"])

    def test_tilde_fences_and_unclosed_fence(self):
        self.assertEqual(literals("~~~py\nx = 1\n~~~\n", "fenced_code"), ["~~~py\nx = 1\n~~~\n"])
        self.assertEqual(checker.lint_text("```\nIt is worth noting that")["candidate_count"], 0)

    def test_math_forms_are_outer_protection(self):
        forms = [r"$x=3$", "$$x=3\ny=4$$", r"\(x=3\)", r"\[x=3\]",
                 r"\begin{align}x &= 3\\ y &= 4\end{align}"]
        for form in forms:
            with self.subTest(form=form):
                self.assertEqual(literals(form, "math"), [form])
                self.assertEqual(literals(form, "number"), [])

    def test_numeric_and_author_year_and_latex_citations(self):
        markers = ["[1–3, 7]", "[@alpha; @beta]", r"\citep[see][p. 2]{alpha}",
                   "(Ren et al., 2025)", "(Ren and Li, 2025; Park, 2024)"]
        for marker in markers:
            with self.subTest(marker=marker):
                self.assertEqual(literals(marker, "citation"), [marker])

    def test_bare_at_keys_are_separate_from_established_citation_syntax(self):
        text = "See @smith2024 and -@doe:2025. Compare [@other]."
        self.assertEqual(literals(text, "at_key"), ["@smith2024", "-@doe:2025"])
        self.assertEqual(literals(text, "citation"), ["[@other]"])

    def test_bare_at_keys_do_not_match_email_local_parts_or_escaped_at(self):
        samples = ["author@example.org", "first.last+tag@sub.example.org", "first-@example.org",
                   '"first last"@example.org', "作者@example.org", r"Literal \@smith2024"]
        for text in samples:
            with self.subTest(text=text):
                self.assertEqual(literals(text, "at_key"), [])
                self.assertEqual(literals(text, "citation"), [])

    def test_at_mention_remains_an_ambiguous_literal_not_a_citation_claim(self):
        text = "Ask @editor for comments."
        self.assertEqual(literals(text, "at_key"), ["@editor"])
        self.assertEqual(literals(text, "citation"), [])

    def test_bare_url_keeps_internal_parentheses_and_trims_external_ones(self):
        text = "See (https://example.test/a_(b)?q=1). Next."
        self.assertEqual(literals(text, "url"), ["https://example.test/a_(b)?q=1"])

    def test_markdown_targets_support_balanced_parentheses_and_relative_paths(self):
        text = '[spec](https://example.test/a_(b)?x=1 "label") ![plot](../figures/a(b).svg)'
        self.assertEqual(literals(text, "markdown_target"),
                         ["https://example.test/a_(b)?x=1", "../figures/a(b).svg"])

    def test_angle_and_reference_link_targets(self):
        text = '[one](<../a b.md>)\n[ref]: <https://example.test/a_(b)> "title"\n'
        self.assertEqual(literals(text, "markdown_target"),
                         ["../a b.md", "https://example.test/a_(b)"])

    def test_numbers_next_to_chinese_and_common_units(self):
        text = "共有12条记录，阈值0.75，下降5%，温度-5°C，电压+3.2mV。"
        self.assertEqual(literals(text, "number"), ["12条", "0.75", "5%", "-5°C", "+3.2mV"])

    def test_signed_decimal_scientific_grouped_and_compound_units(self):
        text = "+7.5% −.25 kg 1,024MiB 2e+3ms 1E−3s +3 m/s² $12.50"
        self.assertEqual(literals(text, "number"),
                         ["+7.5%", "−.25 kg", "1,024MiB", "2e+3ms", "1E−3s", "+3 m/s²", "$12.50"])

    def test_nested_keep_blocks_and_custom_literals(self):
        text = ("<!-- clearweave:keep -->A<!-- clearweave:keep -->B"
                "<!-- /clearweave:keep -->C<!-- /clearweave:keep -->")
        self.assertEqual(literals(text, "keep"), [text])
        custom = "It is worth noting that"
        self.assertEqual(checker.lint_text(custom, custom_literals=[custom, custom])["candidate_count"], 0)
        self.assertEqual(literals(custom, "custom", [custom, custom]), [custom])

    def test_outer_region_counts_once_without_nested_numeric_noise(self):
        text = '"The limit is 12 ms; see https://example.test/?n=3."'
        spans = checker.collect_protected_spans(text)
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].kind, "quotation")

    def test_direct_quotation_can_enclose_inline_code_without_losing_outer_protection(self):
        for left, right in [('"', '"'), ('“', '”')]:
            with self.subTest(left=left):
                text = left + "It is worth noting that `retry` remains optional." + right
                self.assertEqual(literals(text, "quotation"), [text])
                self.assertEqual(len(checker.collect_protected_spans(text)), 1)
                self.assertEqual(checker.lint_text(text)["candidate_count"], 0)
                report = checker.compare_texts(text, text.replace("optional", "required"))
                self.assertTrue(report["supported_literal_changes"])
                self.assertEqual({item["kind"] for item in report["changes"]}, {"quotation"})


class CompareTests(unittest.TestCase):
    def test_bare_key_change_is_detected_without_claiming_bibliographic_identity(self):
        report = checker.compare_texts("See @smith2024.", "See @doe2025.")
        self.assertTrue(report["supported_literal_changes"])
        self.assertEqual({(item["kind"], item["literal"], item["delta"]) for item in report["changes"]},
                         {("at_key", "@smith2024", -1), ("at_key", "@doe2025", 1)})
        self.assertTrue(report["semantic_review_required"])

    def test_changed_chinese_adjacent_number(self):
        report = checker.compare_texts("共有12条记录。", "共有13条记录。")
        self.assertTrue(report["supported_literal_changes"])
        self.assertEqual({(item["literal"], item["delta"]) for item in report["changes"]},
                         {("12条", -1), ("13条", 1)})

    def test_unit_change_and_equivalent_conversion_are_both_literal_changes(self):
        for before, after in [("延迟10ms", "延迟10s"), ("延迟1000ms", "延迟1s"),
                              ("memory 1 GB", "memory 1 GiB")]:
            with self.subTest(before=before, after=after):
                report = checker.compare_texts(before, after)
                self.assertTrue(report["supported_literal_changes"])
                self.assertTrue(report["semantic_review_required"])

    def test_url_query_and_parenthesized_path_change(self):
        before = "[spec](https://example.test/a_(b)?q=1)"
        after = "[spec](https://example.test/a_(c)?q=2)"
        report = checker.compare_texts(before, after)
        self.assertEqual({item["kind"] for item in report["changes"]}, {"markdown_target"})
        self.assertEqual({item["literal"] for item in report["changes"]},
                         {"https://example.test/a_(b)?q=1", "https://example.test/a_(c)?q=2"})

    def test_code_change_is_reported_as_a_code_literal(self):
        before = "```python\nreturn retries < 3\n```\n"
        after = "```python\nreturn retries <= 3\n```\n"
        report = checker.compare_texts(before, after)
        self.assertEqual({item["kind"] for item in report["changes"]}, {"fenced_code"})
        self.assertEqual(len(report["changes"]), 2)

    def test_loss_is_a_count_change_even_if_one_copy_remains(self):
        report = checker.compare_texts("A=4, B=4.", "A=4.")
        self.assertEqual(len(report["changes"]), 1)
        change = report["changes"][0]
        self.assertEqual((change["literal"], change["original_count"], change["revision_count"]), ("4", 2, 1))
        self.assertEqual(len(change["original_locations"]), 2)

    def test_explicit_custom_protection_detects_non_numeric_loss(self):
        report = checker.compare_texts("Keep service-SLA here.", "Keep the term here.", ["service-SLA"])
        self.assertEqual([(item["kind"], item["literal"], item["status"]) for item in report["changes"]],
                         [("custom", "service-SLA", "lost")])

    def test_numeric_role_exchange_is_an_explicit_known_blind_spot(self):
        report = checker.compare_texts("A得分0.8，B得分0.6。", "A得分0.6，B得分0.8。")
        self.assertFalse(report["supported_literal_changes"])
        self.assertTrue(report["semantic_review_required"])
        self.assertNotIn("meaning_pass", report)
        self.assertNotIn("passed", report)

    def test_negation_change_is_an_explicit_known_blind_spot(self):
        report = checker.compare_texts("该方案支持离线部署。", "该方案不支持离线部署。")
        self.assertFalse(report["supported_literal_changes"])
        self.assertTrue(report["semantic_review_required"])
        self.assertIn("not checked", " ".join(report["limitations"]))

    def test_written_out_numbers_are_not_arabic_numeric_protection(self):
        report = checker.compare_texts("three results; 三个结果", "four results; 四个结果")
        self.assertFalse(report["supported_literal_changes"])
        self.assertTrue(report["semantic_review_required"])

    def test_blockquotes_and_kept_material_are_literal_comparisons(self):
        for before, after, kind in [(
            "> The draft is ready.\n", "> The draft is final.\n", "blockquote"), (
            "<!-- clearweave:keep -->pending<!-- /clearweave:keep -->",
            "<!-- clearweave:keep -->approved<!-- /clearweave:keep -->", "keep")]:
            with self.subTest(kind=kind):
                report = checker.compare_texts(before, after)
                self.assertEqual({item["kind"] for item in report["changes"]}, {kind})


class CommandLineTests(unittest.TestCase):
    def test_help_and_invalid_parameters(self):
        for args in [("--help",), ("lint", "--help"), ("compare", "--help")]:
            self.assertEqual(cli(*args).returncode, 0)
        self.assertEqual(cli("lint", "-", "--language", "bad").returncode, 2)
        self.assertEqual(cli("compare", "-", "-").returncode, 2)
        self.assertEqual(cli("lint", "-", "--protect-file", "-").returncode, 2)

    def test_lint_stdin_reports_candidates_with_success_exit_code(self):
        result = cli("lint", "-", "--format", "json", input_text="值得注意的是，情况未定。")
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["candidate_count"], 1)
        self.assertNotIn("probability", result.stdout.lower())

    def test_compare_stdin_status_codes_and_read_only_files(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "original.txt"
            path.write_bytes("共有12条记录。\r\n".encode("utf-8"))
            content = path.read_bytes()
            same = cli("compare", str(path), "-", "--format", "json", input_text=content.decode("utf-8"))
            changed = cli("compare", str(path), "-", "--format", "json", input_text="共有13条记录。\r\n")
            self.assertEqual(same.returncode, 0, same.stderr)
            self.assertEqual(changed.returncode, 1, changed.stderr)
            self.assertTrue(json.loads(same.stdout)["semantic_review_required"])
            self.assertEqual(path.read_bytes(), content)

    def test_missing_file_invalid_utf8_and_protection_file(self):
        with tempfile.TemporaryDirectory() as temp:
            bad = Path(temp) / "bad.txt"
            bad.write_bytes(b"\xff")
            self.assertEqual(cli("lint", str(bad)).returncode, 2)
            self.assertEqual(cli("lint", str(Path(temp) / "missing.txt")).returncode, 2)
            protection = Path(temp) / "protect.txt"
            protection.write_text("\nIt is worth noting that\nIt is worth noting that\n", encoding="utf-8")
            result = cli("lint", "-", "--protect-file", str(protection), "--format", "json",
                         input_text="It is worth noting that the value is protected.")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["candidate_count"], 0)


if __name__ == "__main__":
    unittest.main()
