#!/usr/bin/env python3
"""Validate the ClearWeave package, source coverage, and recorded output structure."""
from __future__ import annotations
import json
import importlib.util
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def validate() -> list[str]:
    errors = []
    for file in ROOT.rglob("*.json"):
        if ".git" in file.relative_to(ROOT).parts:
            continue
        try:
            json.loads(file.read_text(encoding="utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON: {file.relative_to(ROOT)}: {exc}")
    skill = ROOT / "skills" / "clearweave"
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    front = re.match(r"\A---\nname: ([a-z0-9-]+)\ndescription: (.+)\n---\n", text)
    if not front:
        errors.append("SKILL.md must have the expected name/description YAML frontmatter")
    else:
        if front.group(1) != skill.name:
            errors.append("Skill name does not match its directory")
        try:
            desc = json.loads(front.group(2))
            if not isinstance(desc, str) or not 1 <= len(desc) <= 1024:
                errors.append("Description must have 1–1024 characters")
        except json.JSONDecodeError:
            errors.append("Description must be a valid quoted YAML/JSON string")
    if len(text.splitlines()) >= 500:
        errors.append("Main skill should stay below 500 lines")
    for link in re.findall(r"\]\((references/[^)#]+)(?:#[^)]*)?\)", text):
        if not (skill / link).is_file():
            errors.append(f"Missing linked reference: {link}")
    for file in skill.rglob("*.md"):
        if "[TODO" in file.read_text(encoding="utf-8"):
            errors.append(f"Unfinished template: {file.relative_to(ROOT)}")
    audit = json.loads((ROOT / "docs/source-audit.json").read_text(encoding="utf-8"))["sources"]
    catalog = json.loads((skill / "assets/capabilities.json").read_text(encoding="utf-8"))
    source_count = catalog["source_inventory_count"]
    if [s["id"] for s in audit] != [f"S{i:02}" for i in range(1, source_count + 1)]:
        errors.append("Source IDs differ from the declared inventory")
    if len({s["repo"] for s in audit}) != source_count:
        errors.append("Source repositories must be distinct within the declared inventory")
    if (ROOT / "VERSION").read_text().strip() != catalog["version"]:
        errors.append("VERSION and capability catalog differ")
    for source in audit:
        expected = f"https://github.com/{source['repo']}/blob/main/{source['skill_path']}"
        if source["url"] != expected:
            errors.append(f"Source URL mismatch: {source['id']}")
        for key in ("evidence_basis", "license_observed", "relationship", "adopted", "rejected_or_modified", "target_modules"):
            if not source.get(key):
                errors.append(f"Missing source audit field: {source['id']} {key}")
        for path in source["target_modules"]:
            if not (ROOT / path).is_file():
                errors.append(f"Unresolved target: {source['id']} {path}")
    for required in ("README.md", "README.zh-CN.md", "LICENSE", "NOTICE.md", "VERSION",
                     "docs/evaluation.md", "evals/PROTOCOL.md", "skills/clearweave/LICENSE.txt",
                     "skills/clearweave/agents/openai.yaml", "skills/clearweave/scripts/clearweave_check.py"):
        if not (ROOT / required).is_file():
            errors.append(f"Missing release file: {required}")
    cases = json.loads((ROOT / "evals/cases.json").read_text(encoding="utf-8"))["cases"]
    expected_ids = {c["id"] for c in cases}
    for condition in ("plain", "clearweave"):
        ids = []
        for batch in ("a", "b"):
            file = ROOT / f"evals/runs/{condition}-{batch}.json"
            if not file.exists():
                errors.append(f"Missing writing outputs: {file.relative_to(ROOT)}")
                continue
            for row in json.loads(file.read_text(encoding="utf-8")):
                ids.append(row["id"])
                if not isinstance(row.get("text"), str) or not row["text"].strip():
                    errors.append(f"Empty output: {condition} {row['id']}")
        if len(ids) != len(set(ids)) or set(ids) != expected_ids:
            errors.append(f"Writing case coverage mismatch: {condition}")
    for module_name in ("coverage", "render_catalog"):
        spec = importlib.util.spec_from_file_location("cw_" + module_name, ROOT / "tools" / (module_name + ".py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if module_name == "coverage":
            errors.extend(module.validate(ROOT)["structural_errors"])
        else:
            errors.extend("Stale generated documentation: " + p for p in module.stale_documents())
    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"Validation error: {exc}", file=sys.stderr)
        return 1
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Package, decision crosswalk, generated documentation, and historical writing record structure: OK")
    print("This checks structure and coverage; it does not establish writing quality or semantic fidelity.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
