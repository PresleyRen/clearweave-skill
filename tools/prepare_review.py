#!/usr/bin/env python3
"""Prepare anonymous A/B candidates from recorded writing outputs; no model calls."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_condition(prefix: str, expected: set[str]) -> dict[str, str]:
    out = {}
    for batch in ("a", "b"):
        path = ROOT / "evals" / "runs" / f"{prefix}-{batch}.json"
        rows = json.loads(path.read_text(encoding="utf-8"))
        for row in rows:
            if row["id"] in out:
                raise ValueError(f"Duplicate case in {prefix}: {row['id']}")
            if not isinstance(row.get("text"), str) or not row["text"].strip():
                raise ValueError(f"Missing response in {path}: {row.get('id')}")
            out[row["id"]] = row["text"]
    if set(out) != expected:
        raise ValueError(f"Case coverage mismatch in {prefix}")
    return out


def main() -> None:
    cases_path = ROOT / "evals" / "cases.json"
    cases = json.loads(cases_path.read_text(encoding="utf-8"))["cases"]
    ids = {c["id"] for c in cases}
    plain, skill = (read_condition(p, ids) for p in ("plain", "clearweave"))
    candidates, mapping = [], {}
    for index, case in enumerate(cases):
        a, b = ("plain", "clearweave") if index % 2 == 0 else ("clearweave", "plain")
        response = {"plain": plain[case["id"]], "clearweave": skill[case["id"]]}
        candidates.append({"id": case["id"], "request": case["request"], "source": case["source"],
                           "A": response[a], "B": response[b]})
        mapping[case["id"]] = {"A": a, "B": b}
    dump = lambda p, value: (ROOT / p).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dump("evals/blind-review.json", {"cases": candidates})
    dump("evals/condition-map.json", mapping)
    recorded = [cases_path, ROOT / "evals" / "rubric.json"]
    recorded += sorted((ROOT / "evals" / "runs").glob("*.json"))
    recorded += sorted(p for p in (ROOT / "skills" / "clearweave").rglob("*")
                       if p.is_file() and p.suffix in {".md", ".yaml"})
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in recorded}
    dump("evals/generation-manifest.json", {
        "recorded_on": "2026-10-20", "cases_per_condition": len(cases),
        "batches_per_condition": 2, "fresh_context_per_batch": True,
        "inherited_conversation_history": False, "responses_per_case_per_condition": 1,
        "generation_instructions": {
            "plain": "Complete the writing requests CW01–CW09 (or CW10–CW18) in evals/cases.json. Follow each request and source using normal writing judgement. Read only that input; no web or other project files. Save id/text JSON. Do not change inputs or ask follow-up questions.",
            "clearweave": "Use skills/clearweave/SKILL.md and relevant local references to complete the same requests. Read only the input and installed skill files, not other repository material. No web. Save id/text JSON. Do not modify inputs or skill or ask follow-up questions."
        },
        "model_environment": "ChatGPT agent session identified as GPT-6 Astra Pro; child snapshot and sampling parameters not exposed; no overrides requested.",
        "sha256_at_review_preparation": hashes,
        "scope_note": "Hashes record inputs, outputs and skill Markdown/YAML present when review was prepared. Local checker implementation was developed separately; it is not a rewriting engine."
    })
    print(f"Prepared {len(candidates)} anonymous comparisons; mapping kept in a separate file.")


if __name__ == "__main__":
    main()
