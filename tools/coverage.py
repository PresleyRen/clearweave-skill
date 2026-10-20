#!/usr/bin/env python3
"""Validate the source -> decision -> capability -> module -> case crosswalk.

Structural coverage is not evidence of model writing quality. No network access.
"""
from __future__ import annotations
from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Sequence
ROOT = Path(__file__).resolve().parents[1]


def read(root: Path, path: str) -> dict:
    return json.loads((root / path).read_text(encoding="utf-8"))


def check_example(text: str, checks: list[dict]) -> list[str]:
    errors = []
    for check in checks:
        kind, value = check["type"], check["value"]
        if kind == "contains": ok = value in text
        elif kind == "excludes": ok = value not in text
        elif kind == "equals": ok = text == value
        else: raise ValueError(f"Unknown check type: {kind}")
        if not ok: errors.append(f"{kind}: {value!r}")
    return errors


def validate(root: Path = ROOT) -> dict:
    audit = read(root, "docs/source-audit.json")["sources"]
    features = read(root, "docs/feature-map.json")["features"]
    catalog = read(root, "skills/clearweave/assets/capabilities.json")
    cases = read(root, "evals/conflict-cases.json")["cases"]
    errors: list[str] = []
    def unique(rows, name):
        ids = [r["id"] for r in rows]
        if len(ids) != len(set(ids)): errors.append(f"Duplicate {name} ID")
        return {r["id"]: r for r in rows}
    sources = unique(audit, "source")
    caps = unique(catalog["capabilities"], "capability")
    conflicts = unique(catalog["conflicts"], "conflict")
    case_map = unique(cases, "case")
    unique(features, "feature")
    if len(sources) != catalog["source_inventory_count"]:
        errors.append("Source count differs from declared inventory")
    if set(sources) != {f'S{i:02}' for i in range(1, catalog['source_inventory_count']+1)}:
        errors.append("Source identifiers are not the declared complete inventory")
    expected = {(s["id"], field, i): text for s in audit
                for field in ("adopted", "rejected_or_modified") for i, text in enumerate(s[field])}
    actual = []
    for f in features:
        key = (f["source"], f["audit_field"], f["audit_index"])
        actual.append(key)
        if key not in expected:
            errors.append(f"Unknown audit statement: {f['id']}"); continue
        if hashlib.sha256(expected[key].encode()).hexdigest() != f["statement_sha256"]:
            errors.append(f"Changed audit statement needs remapping: {f['id']}")
        expected_disposition = "adopted" if key[1] == "adopted" else "adapted_or_excluded"
        if f["disposition"] != expected_disposition:
            errors.append(f"Misrepresented source disposition: {f['id']}")
        if not f["capabilities"] or not set(f["capabilities"]) <= set(caps):
            errors.append(f"Missing capability mapping: {f['id']}")
        for cap_id in f["capabilities"]:
            if cap_id in caps and f["source"] not in caps[cap_id]["sources"]:
                errors.append(f"One-way source mapping: {f['id']} -> {cap_id}")
    if Counter(actual) != Counter(expected.keys()):
        errors.append("Source statement coverage is missing or duplicated")
    skill = root / "skills/clearweave"
    for cap in caps.values():
        module = (skill / cap["module"]).resolve()
        if not module.is_relative_to(skill.resolve()) or not module.is_file():
            errors.append(f"Invalid module: {cap['id']}")
        elif f'id="{cap["anchor"]}"' not in module.read_text(encoding="utf-8"):
            errors.append(f"Missing stable anchor: {cap['id']}")
        if not cap["sources"] or not set(cap["sources"]) <= set(sources):
            errors.append(f"Invalid inspiration source: {cap['id']}")
        if not cap["cases"] or not set(cap["cases"]) <= set(case_map):
            errors.append(f"Missing scenario coverage: {cap['id']}")
        if not cap.get("implementation_boundary"):
            errors.append(f"Missing capability boundary: {cap['id']}")
    for conflict in conflicts.values():
        ids = conflict["cases"]
        if not set(conflict["capabilities"]) <= set(caps):
            errors.append(f"Unknown conflict capability: {conflict['id']}")
        found = [case_map[i] for i in ids if i in case_map]
        if len(found) != 2 or {c["language"] for c in found} != {"en", "zh"}:
            errors.append(f"Conflict needs one English and one Chinese case: {conflict['id']}")
        for c in found:
            if c["conflict"] != conflict["id"]:
                errors.append(f"Conflicting case ownership: {c['id']}")
            for cap_id in conflict["capabilities"]:
                if cap_id in caps and c["id"] not in caps[cap_id]["cases"]:
                    errors.append(f"One-way conflict mapping: {c['id']} -> {cap_id}")
    fixture_results = []
    for case in cases:
        if case["conflict"] not in conflicts:
            errors.append(f"Unknown conflict: {case['id']}")
        if not case["checks"] or not all(isinstance(case.get(k), str) and case[k].strip() for k in ("request", "original", "faithful_example", "unsafe_example")):
            errors.append(f"Incomplete case: {case['id']}"); continue
        good = check_example(case["faithful_example"], case["checks"])
        bad = check_example(case["unsafe_example"], case["checks"])
        if good: errors.append(f"Faithful fixture violates declared constraints: {case['id']} {good}")
        if not bad: errors.append(f"Unsafe fixture is not rejected by its constraints: {case['id']}")
        fixture_results.append({"id":case["id"],"faithful_constraints_satisfied":not good,
                                "unsafe_constraints_rejected":bool(bad),"unsafe_violations":bad})
    dispositions = Counter(f["disposition"] for f in features)
    return {"schema_version":1,"sources":len(sources),"audited_statements":len(expected),
            "mapped_statements":len(features),"dispositions":dict(dispositions),
            "capabilities":len(caps),"conflicts":len(conflicts),"authored_cases":len(cases),
            "structural_errors":errors,"fixture_results":fixture_results,
            "evidence_scope":"Structural links and authored-fixture constraints, not independent host-model effectiveness or complete semantic equivalence."}


def main(argv: Sequence[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format",choices=["text","json"],default="text")
    parser.add_argument("--source",help="Show audited statements and locations for S01 etc.")
    args=parser.parse_args(argv)
    try:
        report=validate()
        if args.source:
            sources=read(ROOT,"docs/source-audit.json")["sources"]
            selected=next((s for s in sources if s["id"]==args.source.upper()),None)
            if selected is None: raise ValueError("Unknown source ID")
            feature_rows=read(ROOT,"docs/feature-map.json")["features"]
            report["source_detail"]=[{**f,"statement":selected[f["audit_field"]][f["audit_index"]]}
                                      for f in feature_rows if f["source"]==selected["id"]]
        if args.format=="json": print(json.dumps(report,ensure_ascii=False,indent=2))
        else:
            for k in ("sources","audited_statements","mapped_statements","capabilities","conflicts","authored_cases"):
                print(f"{k}: {report[k]}")
            print(f"Structural errors: {len(report['structural_errors'])}")
            for e in report["structural_errors"]: print(f"ERROR: {e}")
            if args.source:
                for f in report["source_detail"]:
                    print(f"{f['id']} [{f['disposition']}] {', '.join(f['capabilities'])}: {f['statement']}")
            print(report["evidence_scope"])
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(f"coverage: {exc}",file=sys.stderr);return 2
    return 1 if report["structural_errors"] else 0

if __name__=="__main__": raise SystemExit(main())
