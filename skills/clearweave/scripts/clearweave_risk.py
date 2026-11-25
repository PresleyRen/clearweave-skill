#!/usr/bin/env python3
"""Read-only EN/ZH revision-risk candidates, not semantic equivalence or authorship.

Python 3.10+, standard library. Reports changed inventories of a small set of
semantic cues and reordered numeric literals. Paraphrases can trigger warnings;
unchanged inventories can still conceal a meaning change. No network or writes.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import sys
from typing import Sequence
import clearweave_check as checker

# Avoid treating "not only" as propositional negation. These are intentionally
# limited cue inventories, not language parsers or a list of forbidden words.
CUES = (
    ("R01", "negation", r"\b(?:not(?!\s+only\b)|never|neither|without|cannot)\b|\b\w+n['’]t\b|(?:并未|並未|尚未|不能|不支持|没有|沒有|不得|无需|無需|未能|不需要)", "CW05"),
    ("R02", "uncertainty", r"\b(?:may|might|possibly|probably|approximately|suggests?|uncertain)\b|(?:可能|或许|或許|大约|大約|尚不确定|尚不確定|推测|推測)", "CW06"),
    ("R03", "obligation", r"\b(?:must|shall|should|required|optional|permitted|recommended)\b|(?:必须|必須|应当|應當|建议|建議|可以|可选|可選|允许|允許)", "CW06"),
    ("R04", "causal_strength", r"\b(?:causes?|caused|associated|correlat(?:e[ds]?|ion)|because|therefore)\b|(?:导致|導致|相关|相關|因果|因为|因為|因此)", "CW07"),
    ("R05", "work_status", r"\b(?:planned|planning|proposed|simulated|completed|validated|deployed|will)\b|(?:计划|計劃|拟于|擬於|已完成|已经|已經|模拟|模擬|拟议|擬議|已部署|将于|將於)", "CW03"),
    ("R06", "scope", r"\b(?:only|unless|except|all|some|under|at\s+least|at\s+most)\b|(?:仅|僅|只有|除非|至少|至多|所有|部分|条件下|條件下)", "CW05"),
    ("R10", "assumption", r"\b(?:independent|dependent|uncorrelated|correlated)\b|(?:独立|獨立|相依|不相关|不相關)", "CW05"),
    ("R07", "attribution", r"\b(?:according\s+to|reported|claimed|estimated)\b|(?:据称|據稱|据报道|據報導|根据|根據|声称|聲稱|估计|估計)", "CW07"),
)
PATTERNS = [(rid, name, re.compile(pattern, re.I), cap) for rid, name, pattern, cap in CUES]


def _visible(text: str) -> str:
    chars = list(text)
    for span in checker.collect_protected_spans(text):
        for pos in range(span.start, span.end):
            if chars[pos] not in "\r\n":
                chars[pos] = " "
    return "".join(chars)


def _hits(text: str, pattern: re.Pattern[str]) -> list[dict]:
    visible = _visible(text)
    result = []
    for match in pattern.finditer(visible):
        # Uppercase May followed by a date is probably the month, not modality.
        if match.group() == "May" and re.match(r"\s+\d", text[match.end():]):
            continue
        start = match.start()
        result.append({"cue": match.group(), "line": text.count("\n", 0, start) + 1,
                       "column": start - text.rfind("\n", 0, start),
                       "context": text[max(0, start-48): min(len(text), match.end()+48)]})
    return result


def _anchored_words(text: str) -> dict[str, dict[str, str]]:
    """Associate distinctive words with unique numbers or citations in single-anchor clauses."""
    spans = [span for span in checker.collect_protected_spans(text)
             if span.kind in {"number", "citation", "at_key"}]
    counts = Counter((span.kind, span.literal) for span in spans)
    owners = {}
    visible = _visible(text)
    index = 0
    for clause in re.finditer(r"[^.!?;。！？；，,\n]+", visible):
        anchors = []
        while index < len(spans) and spans[index].start < clause.end():
            span = spans[index]
            if clause.start() <= span.start:
                anchors.append(span)
            index += 1
        if len(anchors) != 1:
            continue
        anchor = anchors[0]
        if counts[(anchor.kind, anchor.literal)] != 1:
            continue
        terms = owners.setdefault(anchor.kind, {})
        for word in set(re.findall(r"[^\W\d_]+", clause.group().casefold())):
            previous = terms.setdefault(word, anchor.literal)
            if previous != anchor.literal:
                terms[word] = ""
    return owners


def _binding_swaps(original: str, revision: str) -> list[dict]:
    before, after = _anchored_words(original), _anchored_words(revision)
    findings = []
    for kind in sorted(before.keys() & after.keys()):
        moves = {}
        for term, source in before[kind].items():
            target = after[kind].get(term)
            if source and target and source != target:
                moves.setdefault((source, target), []).append(term)
        for (left, right), terms in sorted(moves.items()):
            reverse = moves.get((right, left))
            if left < right and reverse:
                findings.append({"risk_id": "R09", "capability": "CW04" if kind == "number" else "CW07",
                                 "category": kind + "_binding", "original": [left, right],
                                 "revision": [right, left], "moved_terms": [sorted(terms), sorted(reverse)],
                                 "reason": "Context terms exchanged anchors. Check the two source claims."})
    return findings


def assess(original: str, revision: str) -> dict:
    findings = []
    for rid, category, pattern, cap in PATTERNS:
        before, after = _hits(original, pattern), _hits(revision, pattern)
        # Inventory, not merely total count: 'must' -> 'should' remains visible.
        a = Counter(h["cue"].casefold() for h in before)
        b = Counter(h["cue"].casefold() for h in after)
        if a != b:
            findings.append({"risk_id": rid, "capability": cap, "category": category,
                             "original": before, "revision": after,
                             "reason": "Cue inventory changed. Check the claim and its scope; a faithful paraphrase may also trigger this candidate."})
    old = [s.literal for s in checker.collect_protected_spans(original) if s.kind == "number"]
    new = [s.literal for s in checker.collect_protected_spans(revision) if s.kind == "number"]
    if Counter(old) == Counter(new) and old != new:
        findings.append({"risk_id": "R08", "capability": "CW04", "category": "number_order",
                         "original": old, "revision": new,
                         "reason": "The numeric inventory is unchanged but its order differs. Check which actor/metric owns each value. Legitimate sentence reordering also triggers this."})
    findings.extend(_binding_swaps(original, revision))
    return {"mode": "risk", "candidate_count": len(findings), "findings": findings,
            "semantic_review_required": True, "verdict": "not_provided",
            "limitations": ["Lexical cues are incomplete and do not resolve scope, roles, or logical equivalence.",
                            "Unchanged cue and numeric inventories can conceal meaning changes.",
                            "Translation and faithful paraphrases can legitimately change cue inventories.",
                            "Run the separate literal comparison for changes inside protected spans."]}


def _read(path: str) -> str:
    return checker._read_utf8(path)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("original")
    parser.add_argument("revision")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    parser.add_argument("--fail-on-candidate", action="store_true",
                        help="Opt-in exit 1 for review candidates, not a semantic rejection")
    args = parser.parse_args(argv)
    try:
        if args.original == args.revision == "-":
            raise ValueError("at most one stdin input is supported")
        report = assess(_read(args.original), _read(args.revision))
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"clearweave-risk: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Revision-risk candidates: {report['candidate_count']} (not a semantic verdict)")
        for finding in report["findings"]:
            print(f"{finding['risk_id']} / {finding['capability']}: {finding['category']}")
            print(f"  {finding['reason']}")
        print("Semantic review required: yes; zero candidates is not a pass.")
    return 1 if args.fail_on_candidate and report["candidate_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
