#!/usr/bin/env python3
"""Summarize recorded editor judgements and limited local checks; no model calls."""
from __future__ import annotations
from collections import Counter
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    cases = {row["id"]: row for row in read("evals/cases.json")["cases"]}
    reviews = read("evals/blind-review-results.json")
    mapping = read("evals/condition-map.json")
    if {r["id"] for r in reviews} != set(cases) or len(reviews) != len(cases):
        raise ValueError("The review must contain each original case exactly once")
    conditions = {}
    for condition in ("plain", "clearweave"):
        output = {}
        for batch in ("a", "b"):
            output.update({r["id"]: r["text"] for r in read(f"evals/runs/{condition}-{batch}.json")})
        conditions[condition] = output
    stats = {condition: {"fidelity_pass": 0, "task_pass": 0, "restraint_pass": 0,
                         "preferred_cases": 0} for condition in conditions}
    rows, preferences = [], Counter()
    for review in reviews:
        record = {"id": review["id"], "reason": review["reason"]}
        for label in ("A", "B"):
            condition = mapping[review["id"]][label]
            record[condition] = review[label]
            for criterion in ("fidelity_pass", "task_pass", "restraint_pass"):
                stats[condition][criterion] += int(review[label][criterion])
        preferred = review["preference"]
        winner = "tie" if preferred == "tie" else mapping[review["id"]][preferred]
        preferences[winner] += 1
        if winner != "tie":
            stats[winner]["preferred_cases"] += 1
        record["preference"] = winner
        rows.append(record)
    module_path = ROOT / "skills/clearweave/scripts/clearweave_check.py"
    spec = importlib.util.spec_from_file_location("clearweave_checker_summary", module_path)
    checker = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = checker
    spec.loader.exec_module(checker)
    eligible = {f"CW{i:02}" for i in (*range(1, 9), 13, 14, 17, 18)}
    literal_checks = []
    for ident in sorted(eligible):
        report = checker.compare_texts(cases[ident]["source"], conditions["clearweave"][ident])
        literal_checks.append({"id": ident, "supported_literal_changes": report["supported_literal_changes"],
                               "change_count": report["change_count"], "changes": report["changes"]})
    followup = read("evals/regression-review.json")
    followup_requests = read("evals/regression-requests.json")["cases"]
    if {r["id"] for r in followup} != {r["id"] for r in followup_requests}:
        raise ValueError("Regression review coverage mismatch")
    summary = {
        "recorded_on": "2026-10-20", "writing_cases_per_condition": len(cases),
        "judgement_type": "anonymous fresh-context model editor; not human review",
        "conditions": stats, "preferences": dict(preferences),
        "no_op_controls": {c: {i: conditions[c][i] == cases[i]["source"] for i in ("CW07", "CW08")}
                           for c in conditions},
        "post_refinement_cases": {"count": len(followup),
                                  "fidelity_pass": sum(int(r["fidelity_pass"]) for r in followup),
                                  "task_pass": sum(int(r["task_pass"]) for r in followup)},
        "literal_checks_scope": "12 original edit/shorten outputs, selected before reporting. Translation, diagnosis, critique and drafting are excluded because their output contract differs.",
        "literal_checks": literal_checks, "case_reviews": rows,
        "limitations": "One response per case and condition, two batches per condition, one host model family, synthetic short texts, subjective model judgements. The 18-case comparison precedes the documented generic-aspiration clarification; four new cases test the clarification. No population success rate, authorship inference, or detector measurement."
    }
    (ROOT / "evals/summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cases": len(cases), "conditions": stats, "preferences": dict(preferences),
                      "post_refinement": summary["post_refinement_cases"],
                      "literal_cases_with_changes": [r["id"] for r in literal_checks if r["supported_literal_changes"]]},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
