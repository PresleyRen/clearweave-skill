#!/usr/bin/env python3
"""Locate ClearWeave capabilities, modules and regression cases; no network/writes."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys
from typing import Sequence

SKILL_ROOT = Path(__file__).resolve().parents[1]


def load_catalog(root: Path = SKILL_ROOT) -> dict:
    catalog = json.loads((root / "assets/capabilities.json").read_text(encoding="utf-8"))
    if catalog.get("schema_version") != 1:
        raise ValueError("Unsupported catalog schema")
    for cap in catalog["capabilities"]:
        module = (root / cap["module"]).resolve()
        if not module.is_relative_to(root.resolve()) or not module.is_file():
            raise ValueError(f"Invalid module path: {cap['id']}")
    return catalog


def trace(catalog: dict, *, identifier: str | None = None, query: str | None = None) -> dict:
    caps = {row["id"]: row for row in catalog["capabilities"]}
    conflicts = {row["id"]: row for row in catalog["conflicts"]}
    identifier = identifier.strip() if identifier is not None else None
    query = query.strip() if query is not None else None
    if bool(identifier) == bool(query):
        raise ValueError("Provide exactly one nonempty id or query")
    selected_conflicts = []
    if identifier:
        key = identifier.upper().strip()
        if key in caps:
            matches = [caps[key]]
            selected_conflicts = [r for r in conflicts.values() if key in r["capabilities"]]
        elif key in conflicts:
            selected_conflicts = [conflicts[key]]
            matches = [caps[k] for k in conflicts[key]["capabilities"]]
        elif re.fullmatch(r"S\d{2,}", key):
            matches = [r for r in caps.values() if key in r["sources"]]
        else:
            matches = []
    else:
        needle = query.strip().casefold()
        tokens = [t for t in re.split(r"\s+", needle) if t]
        ranking = []
        for cap in caps.values():
            words = (cap["keywords"] + " " + cap["name_en"] + " " + cap["name_zh"]).casefold().split()
            score = sum(1 for word in words if word in needle or any(t in word for t in tokens))
            if score:
                ranking.append((-score, cap["id"], cap))
        matches = [x[2] for x in sorted(ranking)[:8]]
    return {"query": identifier or query, "matches": matches, "conflicts": selected_conflicts,
            "judgment": "index_lookup_not_root_cause_proof",
            "repository_evidence": "docs/source-audit.json, docs/feature-map.json, evals/conflict-cases.json",
            "next_step": "Read the located module, reproduce the failure, add a positive case and a counterexample, then rerun tests and a host-model trial."}


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", dest="identifier")
    group.add_argument("--query")
    parser.add_argument("--format", choices=["json", "text"], default="text")
    args = parser.parse_args(argv)
    try:
        report = trace(load_catalog(), identifier=args.identifier, query=args.query)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"clearweave-trace: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        for row in report["matches"]:
            print(f"{row['id']} {row['name_en']} / {row['name_zh']}")
            print(f"  Module: {row['module']}#{row['anchor']}")
            print(f"  Sources: {', '.join(row['sources'])}")
            print(f"  Cases (repository): {', '.join(row['cases'])}")
            print(f"  Boundary: {row['implementation_boundary']}")
        if not report["matches"]:
            print("No matching entry. Create a minimal reproduction; do not invent coverage.")
        print(report["next_step"])
    return 0 if report["matches"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
