#!/usr/bin/env python3
"""Surface editing candidates and supported literal comparisons; no semantic verdict.

Python 3.10+, standard library only. This program reads files or stdin and writes
reports to stdout. It never rewrites the input and never makes network requests.
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import Counter, defaultdict
from dataclasses import dataclass
import json
from pathlib import Path
import re
import sys
from typing import Sequence


@dataclass(frozen=True, slots=True)
class Span:
    kind: str
    start: int
    end: int
    literal: str


@dataclass(frozen=True, slots=True)
class Rule:
    rule_id: str
    language: str
    pattern: re.Pattern[str]
    reason: str


def _rule(rule_id: str, language: str, pattern: str, reason: str) -> Rule:
    return Rule(rule_id, language, re.compile(pattern, re.IGNORECASE), reason)


RULES = (
    _rule("EN001", "en", r"\bit(?:\s+is|['’]s)\s+important\s+to\s+note\s+that\b",
          "Check whether the introductory emphasis adds information; retain the actual qualification."),
    _rule("EN002", "en", r"\bit(?:\s+is|['’]s)\s+worth\s+noting\s+that\b",
          "Consider stating the relevant fact directly; do not delete a meaningful limitation."),
    _rule("EN003", "en", r"\bin\s+today['’]s\s+(?:(?:rapidly|ever)[ -])?(?:evolving|changing|fast[ -]paced)\s+(?:world|landscape)\b",
          "Check whether this broad opening identifies a relevant change or only delays the subject."),
    _rule("EN004", "en", r"\b(?:serves?\s+as\s+)?a\s+testament\s+to\b",
          "Check whether symbolic praise is supported and useful for this document's purpose."),
    _rule("EN005", "en", r"\bpaves?\s+the\s+way\s+for\s+(?:a\s+)?(?:brighter|better)\s+future\b",
          "Check whether this optimistic conclusion contains a concrete, supported consequence."),
    _rule("EN006", "en", r"\bunlock(?:ing)?\s+(?:the\s+)?(?:full|limitless)\s+potential\b",
          "Check whether the text explains the actual capability and its limits."),
    _rule("EN007", "en", r"\b(?:in\s+conclusion|to\s+sum\s+up)\b",
          "Retain useful synthesis or navigation; remove only an unnecessary announcement."),
    _rule("EN008", "en", r"\bI\s+hope\s+this\s+helps\b",
          "This may be an appropriate message closing; check for accidental assistant residue in standalone prose."),
    _rule("ZH001", "zh", r"在当今(?:日新月异|快速发展|飞速发展|不断变化)的?(?:时代|社会)",
          "检查背景是否提供本文需要的信息；仅有泛泛铺垫时，可直接进入具体主题。"),
    _rule("ZH002", "zh", r"值得(?:注意|一提)的是",
          "检查强调语是否必要；可直接陈述重点，但要保留后面的条件或限制。"),
    _rule("ZH003", "zh", r"具有(?:里程碑式的?|划时代的?|深远的?)(?:重要)?意义",
          "检查重要性评价是否有依据，以及是否说明了具体影响。"),
    _rule("ZH004", "zh", r"(?:赋能|助力)(?:高质量发展|业务腾飞|美好未来)",
          "检查是否写清具体行动与对象；不要用未提供的数据补造效果。"),
    _rule("ZH005", "zh", r"(?:让我们共同|让我们一起)(?:期待|见证|携手)",
          "检查号召是否符合文体和任务；事实性文章通常需要具体结论。"),
    _rule("ZH006", "zh", r"(?:未来可期|共创美好未来|开启崭新篇章|谱写新的篇章)",
          "检查收尾是否增加独立信息；保留有内容的计划或结论。"),
    _rule("ZH007", "zh", r"(?:综上所述|总而言之)",
          "检查是否存在真正的归纳或必要导航；总结连接词本身并不是错误。"),
    _rule("ZH008", "zh", r"(?:不难发现|毋庸置疑|众所周知)",
          "检查确定程度是否与依据相称；不要把来源或不确定性一起删掉。"),
)

_HAN = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
_FENCE_OPEN = re.compile(r" {0,3}(`{3,}|~{3,})([^\r\n]*)$")
_KEEP_TAG = re.compile(r"<!--\s*(/?)clearweave:keep\s*-->")
_BLOCKQUOTE = re.compile(r"(?m)^ {0,3}>[^\r\n]*(?:\r?\n|$)")
_STRUCTURAL_TOKEN = re.compile(
    r"(?P<fence>^ {0,3}(?:`{3,}|~{3,})[^\r\n]*(?:\r?\n|$))"
    r"|(?P<blockquote>^ {0,3}>[^\r\n]*(?:\r?\n|$))"
    r"|(?P<keep><!--\s*clearweave:keep\s*-->)"
    r"|(?P<inline>`+)",
    re.MULTILINE,
)
_INLINE_BREAK = re.compile(r"\n[ \t]*\r?\n|^ {0,3}(?:`{3,}|~{3,}|>)", re.MULTILINE)
_ASCII_QUOTE = re.compile(r'"(?:\\.|[^"\\])*"', re.DOTALL)
_URL = re.compile(r"(?:https?|ftp)://[^\s<>\"“”]+|mailto:[^\s<>\"“”]+", re.IGNORECASE)
_LINK_OPEN = re.compile(r"(?<!\\)!?\[[^\]\n]*\]\(")
_REFERENCE_LINK = re.compile(r"(?m)^ {0,3}\[[^\]\n]+\]:[ \t]*(?:<([^>\n]+)>|([^\s]+))")

_UNITS = (
    "%", "％", "‰", "ms", "s", "min", "h", "Hz", "kHz", "MHz", "GHz",
    "B", "KB", "MB", "GB", "TB", "KiB", "MiB", "GiB", "TiB",
    "bps", "kbps", "Mbps", "Gbps", "mm", "cm", "m", "km", "nm", "µm", "μm",
    "kg", "g", "mg", "µg", "μg", "L", "mL", "ml", "°C", "°F", "K",
    "J", "kJ", "W", "kW", "MW", "V", "mV", "A", "mA", "Pa", "kPa",
    "MPa", "eV", "keV", "MeV", "mol", "mmol", "N", "dB",
    "USD", "KRW", "CNY", "EUR", "JPY", "RMB", "元", "美元", "韩元", "日元", "人民币",
    "毫秒", "秒", "分钟", "小时", "天", "周", "个月", "月", "年",
    "字节", "千字节", "兆字节", "吉字节", "千米", "公里", "米", "毫米", "厘米", "纳米",
    "千克", "公斤", "克", "毫克", "升", "毫升", "次", "个", "条", "份", "项",
    "人", "组", "步", "页", "倍", "度", "百分点",
)
_UNIT_ATOM = "(?:" + "|".join(re.escape(unit) for unit in sorted(_UNITS, key=lambda s: (-len(s), s))) + ")"
_UNIT = _UNIT_ATOM + r"(?:\^[-−]?\d+|[²³])?(?:[/·*]" + _UNIT_ATOM + r"(?:\^[-−]?\d+|[²³])?){0,2}"
_NUMBER = re.compile(
    r"(?<![A-Za-z0-9_.])"
    r"(?:[+\-−＋－][¥￥$€£₩]?|[¥￥$€£₩][+\-−＋－]?)?"
    r"(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?|\.\d+)"
    r"(?:[eE][+\-−]?\d+)?"
    r"(?:[ \t]*" + _UNIT + r")?"
    r"(?![A-Za-z0-9_]|\.\d)"
)

_MATH_PATTERNS = (
    re.compile(r"(?<!\\)\$\$[\s\S]*?(?<!\\)\$\$"),
    re.compile(r"\\\([\s\S]*?\\\)"),
    re.compile(r"\\\[[\s\S]*?\\\]"),
    re.compile(r"(?<![\\$])\$(?![$\s])(?:\\.|[^\\$\n])*?(?<!\s)\$(?![$\d])"),
    re.compile(r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?|math|displaymath)\}[\s\S]*?\\end\{\1\}"),
)
_AUTHOR = r"[A-Z][A-Za-z'’.-]+(?:\s+(?:et\s+al\.|(?:and|&)\s+[A-Z][A-Za-z'’.-]+))?"
_AUTHOR_YEAR = _AUTHOR + r",?\s+(?:19|20)\d{2}[a-z]?"
_CITATION_PATTERNS = (
    re.compile(r"\[\d+[a-z]?(?:\s*(?:[,;]|[-–—])\s*\d+[a-z]?)*\]"),
    re.compile(r"\[-?@[A-Za-z0-9_:./+-]+(?:\s*;\s*-?@[A-Za-z0-9_:./+-]+)*\]"),
    re.compile(r"\\(?:cite|citep|citet|autocite|parencite|textcite)\*?(?:\[[^\]\n]*\]){0,2}\{[^{}\n]+\}"),
    re.compile(r"\(" + _AUTHOR_YEAR + r"(?:;\s*" + _AUTHOR_YEAR + r")*\)"),
)
# Keep bare @keys distinct from established citation syntax. The left boundary
# excludes email local-part characters, escaped @ signs and quoted local parts.
# A bare @mention remains ambiguous without a bibliography or document metadata.
_BARE_AT_KEY = re.compile(
    r"(?<![\w@./+%=!#$&'*?^`{|}~\"\\-])"
    r"-?@[A-Za-z_][A-Za-z0-9_]*(?:[.:/-][A-Za-z0-9_]+)*(?![\w@])"
)
_PRIORITY = {kind: rank for rank, kind in enumerate((
    "keep", "frontmatter", "fenced_code", "blockquote", "inline_code", "custom",
    "math", "markdown_target", "url", "quotation", "citation", "at_key", "number",
))}


def _span(text: str, kind: str, start: int, end: int) -> Span:
    return Span(kind, start, end, text[start:end])


def _overlaps(start: int, end: int, spans: Sequence[Span]) -> bool:
    return any(start < item.end and end > item.start for item in spans)


def _structural_spans(text: str) -> list[Span]:
    """Scan outer regions in source order; their contents cannot open new regions."""
    spans: list[Span] = []
    lines = text.splitlines(keepends=True)
    offsets: list[int] = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)

    if lines and re.fullmatch(r"\ufeff?---[ \t]*", lines[0].rstrip("\r\n")):
        for i in range(1, len(lines)):
            if re.fullmatch(r"(?:---|\.\.\.)[ \t]*", lines[i].rstrip("\r\n")):
                spans.append(_span(text, "frontmatter", 0, offsets[i] + len(lines[i])))
                break

    position = spans[-1].end if spans else 0
    while (match := _STRUCTURAL_TOKEN.search(text, position)) is not None:
        kind = match.lastgroup
        start, opening_end = match.span()
        if kind == "fence":
            opening = _FENCE_OPEN.fullmatch(match[0].rstrip("\r\n"))
            assert opening is not None
            marker = opening[1]
            if marker[0] != "`" or "`" not in opening[2]:
                closing = re.compile(r"^ {0,3}" + re.escape(marker[0]) + "{" + str(len(marker))
                                     + r",}[ \t]*(?:\r?\n|$)", re.MULTILINE)
                close = closing.search(text, opening_end)
                end = close.end() if close else len(text)
                spans.append(_span(text, "fenced_code", start, end))
                position = end
                continue
            # A backtick-bearing info string is not a fence. Its initial run
            # may still form an inline code span on this paragraph.
            start += len(match[0]) - len(match[0].lstrip(" "))
            opening_end = start + len(marker)
            kind = "inline"
        if kind == "blockquote":
            end = opening_end
            while (following := _BLOCKQUOTE.match(text, end)) is not None:
                end = following.end()
            spans.append(_span(text, "blockquote", start, end))
            position = end
            continue
        if kind == "keep":
            depth, end = 1, len(text)
            for tag in _KEEP_TAG.finditer(text, opening_end):
                depth += -1 if tag[1] else 1
                if depth == 0:
                    end = tag.end()
                    break
            spans.append(_span(text, "keep", start, end))
            position = end
            continue
        if kind == "inline":
            boundary = _INLINE_BREAK.search(text, opening_end)
            limit = boundary.start() if boundary else len(text)
            closing = re.compile(r"(?<!`)`{" + str(opening_end - start) + r"}(?!`)")
            close = closing.search(text, opening_end, limit)
            if close:
                spans.append(_span(text, "inline_code", start, close.end()))
                position = close.end()
                continue
        position = opening_end
    return spans


def _markdown_targets(text: str) -> list[Span]:
    spans = []
    for match in _LINK_OPEN.finditer(text):
        start = match.end()
        while start < len(text) and text[start] in " \t":
            start += 1
        if start >= len(text):
            continue
        if text[start] == "<":
            end = text.find(">", start + 1)
            if end != -1 and "\n" not in text[start:end]:
                spans.append(_span(text, "markdown_target", start + 1, end))
            continue
        end, depth = start, 0
        while end < len(text):
            char = text[end]
            if char == "\\" and end + 1 < len(text):
                end += 2
                continue
            if char.isspace():
                break
            if char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
            end += 1
        if end > start:
            spans.append(_span(text, "markdown_target", start, end))
    for match in _REFERENCE_LINK.finditer(text):
        group = 1 if match[1] is not None else 2
        spans.append(_span(text, "markdown_target", match.start(group), match.end(group)))
    return spans


def _url_spans(text: str) -> list[Span]:
    spans = []
    closing = {")": "(", "]": "[", "}": "{"}
    for match in _URL.finditer(text):
        start, end = match.span()
        while end > start:
            char = text[end - 1]
            value = text[start:end]
            if char in ".,;:!?，。；：！？、":
                end -= 1
            elif char in closing and value.count(char) > value.count(closing[char]):
                end -= 1
            else:
                break
        spans.append(_span(text, "url", start, end))
    return spans


def _outer_spans(text: str, candidates: Sequence[Span]) -> list[Span]:
    """Retain outer regions; merge partial overlaps so lint leaves no gap."""
    ordered = sorted(candidates, key=lambda item: (item.start, -item.end, _PRIORITY.get(item.kind, 99)))
    result: list[Span] = []
    for item in ordered:
        if item.start == item.end:
            continue
        if result and item.start < result[-1].end:
            if item.end > result[-1].end:
                result[-1] = _span(text, "overlapping_protection", result[-1].start, item.end)
        else:
            result.append(item)
    return result


def collect_protected_spans(text: str, custom_literals: Sequence[str] = ()) -> list[Span]:
    """Recognize supported literal regions, without parsing their meaning."""
    structural = _structural_spans(text)
    candidates = list(structural)
    # Hide delimiters printed inside structural regions. Outside quote/math
    # delimiters can still enclose an inline code span; preserve the original
    # characters and offsets when collecting that larger literal.
    opaque = list(text)
    for region in structural:
        for index in range(region.start, region.end):
            if opaque[index] not in "\r\n":
                opaque[index] = "\ufffc"
    opaque_text = "".join(opaque)
    quote_patterns = (_ASCII_QUOTE, re.compile(r"“[^”]*”"), re.compile(r"「[^」]*」"), re.compile(r"『[^』]*』"))
    for kind, patterns in (("quotation", quote_patterns), ("math", _MATH_PATTERNS)):
        for pattern in patterns:
            candidates.extend(_span(text, kind, *match.span()) for match in pattern.finditer(opaque_text))

    # URLs, citation tokens and numbers are confined to the remaining gaps.
    position = 0
    gaps = []
    for region in structural:
        gaps.append((position, region.start))
        position = region.end
    gaps.append((position, len(text)))
    for begin, end in gaps:
        chunk = text[begin:end]
        local = _markdown_targets(chunk) + _url_spans(chunk)
        for kind, patterns in (("citation", _CITATION_PATTERNS),
                               ("at_key", (_BARE_AT_KEY,)), ("number", (_NUMBER,))):
            for pattern in patterns:
                local.extend(_span(chunk, kind, *match.span()) for match in pattern.finditer(chunk))
        candidates.extend(Span(item.kind, begin + item.start, begin + item.end, item.literal) for item in local)
    for literal in dict.fromkeys(custom_literals):
        if not literal:
            continue
        start = text.find(literal)
        while start != -1:
            candidates.append(_span(text, "custom", start, start + len(literal)))
            start = text.find(literal, start + len(literal))
    return _outer_spans(text, candidates)


def _line_starts(text: str) -> list[int]:
    return [0] + [match.end() for match in re.finditer("\n", text)]


def _location(starts: Sequence[int], position: int) -> dict[str, int]:
    line = bisect_right(starts, position)
    return {"line": line, "column": position - starts[line - 1] + 1}


def lint_text(text: str, language: str = "auto", custom_literals: Sequence[str] = ()) -> dict:
    if language not in {"auto", "en", "zh", "both"}:
        raise ValueError("language must be auto, en, zh, or both")
    protected = collect_protected_spans(text, custom_literals)
    visible = list(text)
    for span in protected:
        for i in range(span.start, span.end):
            if visible[i] not in "\r\n":
                visible[i] = " "
    visible_text = "".join(visible)
    if language == "both":
        languages = ["en", "zh"]
    elif language == "auto":
        languages = (["en"] if re.search(r"[A-Za-z]", visible_text) else [])
        if _HAN.search(visible_text):
            languages.append("zh")
    else:
        languages = [language]
    starts, diagnostics = _line_starts(text), []
    for rule in RULES:
        if rule.language not in languages:
            continue
        for match in rule.pattern.finditer(text):
            if _overlaps(match.start(), match.end(), protected):
                continue
            diagnostics.append({"rule_id": rule.rule_id, **_location(starts, match.start()),
                                "excerpt": match[0], "reason": rule.reason})
    diagnostics.sort(key=lambda item: (item["line"], item["column"], item["rule_id"]))
    return {"mode": "lint", "language_requested": language, "languages_scanned": languages,
            "candidate_count": len(diagnostics), "diagnostics": diagnostics,
            "protected_span_count": len(protected), "judgment": "editorial_candidates_only",
            "semantic_review_required": True}


def compare_texts(original: str, revision: str, custom_literals: Sequence[str] = ()) -> dict:
    old_spans = collect_protected_spans(original, custom_literals)
    new_spans = collect_protected_spans(revision, custom_literals)
    old = Counter((span.kind, span.literal) for span in old_spans)
    new = Counter((span.kind, span.literal) for span in new_spans)
    locations: list[dict[tuple[str, str], list[dict[str, int]]]] = []
    for text, spans in ((original, old_spans), (revision, new_spans)):
        found: dict[tuple[str, str], list[dict[str, int]]] = defaultdict(list)
        starts = _line_starts(text)
        for span in spans:
            found[(span.kind, span.literal)].append(_location(starts, span.start))
        locations.append(found)
    changes = []
    for key in sorted(old.keys() | new.keys()):
        delta = new[key] - old[key]
        if delta:
            changes.append({"kind": key[0], "literal": key[1],
                            "original_count": old[key], "revision_count": new[key], "delta": delta,
                            "status": "added" if delta > 0 else "lost",
                            "original_locations": locations[0].get(key, []),
                            "revision_locations": locations[1].get(key, [])})
    return {"mode": "compare", "comparison_scope": "supported_literal_multiset",
            "supported_literal_changes": bool(changes), "change_count": len(changes),
            "original_span_count": len(old_spans), "revision_span_count": len(new_spans),
            "changes": changes, "semantic_review_required": True,
            "limitations": [
                "Counts are literal and unordered; moving values between roles may be invisible.",
                "Negation, attribution, causal strength, and other prose meaning are not checked.",
                "Only documented syntax and units are recognized; no completeness guarantee.",
            ]}


def _read_utf8(path: str) -> str:
    if path == "-":
        if hasattr(sys.stdin, "buffer"):
            return sys.stdin.buffer.read().decode("utf-8")
        return sys.stdin.read()
    return Path(path).read_bytes().decode("utf-8")


def _custom_literals(path: str | None) -> list[str]:
    if path is None:
        return []
    if path == "-":
        raise ValueError("--protect-file must be a file path, not stdin (-)")
    return list(dict.fromkeys(line for line in _read_utf8(path).splitlines() if line != ""))


def _render_text(report: dict) -> str:
    if report["mode"] == "lint":
        lines = [f"Editorial candidates: {report['candidate_count']} (not an authorship assessment)."]
        for item in report["diagnostics"]:
            lines.append(f"{item['rule_id']} {item['line']}:{item['column']} {item['excerpt']!r}\n  {item['reason']}")
    else:
        lines = [f"Supported literal count changes: {report['change_count']}."]
        for item in report["changes"]:
            preview = repr(item["literal"])
            if len(preview) > 160:
                preview = preview[:157] + "..."
            lines.append(f"{item['status']} {abs(item['delta'])} [{item['kind']}] {preview} "
                         f"({item['original_count']} -> {item['revision_count']})")
        lines.append("Unchanged counts do not establish preserved meaning; order and prose semantics are not checked.")
    lines.append("Semantic review required: yes.")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    commands = parser.add_subparsers(dest="command", required=True)
    lint = commands.add_parser("lint", help="Report surface editing candidates; never rewrite.")
    lint.add_argument("input", metavar="INPUT", help="UTF-8 input file, or - for stdin")
    lint.add_argument("--language", choices=("auto", "en", "zh", "both"), default="auto")
    compare = commands.add_parser("compare", help="Compare counts of supported protected literals.")
    compare.add_argument("original", metavar="ORIGINAL", help="UTF-8 original file, or - for stdin")
    compare.add_argument("revision", metavar="REVISION", help="UTF-8 revision file, or - for stdin")
    for command in (lint, compare):
        command.add_argument("--format", choices=("json", "text"), default="text")
        command.add_argument("--protect-file", metavar="FILE", help="UTF-8 file: one additional literal per line")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "compare" and args.original == args.revision == "-":
            raise ValueError("compare accepts at most one stdin (-) input")
        literals = _custom_literals(args.protect_file)
        if args.command == "lint":
            report = lint_text(_read_utf8(args.input), args.language, literals)
            status = 0
        else:
            report = compare_texts(_read_utf8(args.original), _read_utf8(args.revision), literals)
            status = 1 if report["supported_literal_changes"] else 0
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"clearweave-check: error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.format == "json" else _render_text(report))
    return status


if __name__ == "__main__":
    raise SystemExit(main())
