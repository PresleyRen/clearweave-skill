#!/usr/bin/env python3
"""Read pinned writing instructions from a companion checkout or upstream."""
from __future__ import annotations

import argparse
from hashlib import sha256
from http.client import HTTPException
import os
from pathlib import Path
import sys
from typing import NamedTuple
from urllib.request import HTTPRedirectHandler, build_opener


class Companion(NamedTuple):
    repo: str
    commit: str
    skill_digest: str
    academic_digest: str | None = None
    skill_root: str = ""


COMPANIONS = {
    "humanizer": Companion(
        "Aparnabuilds/humanizer", "fd9728f1a66a5338dff533c712dd44509900e065",
        "456e4d040933468b64e6cd44cad9c390502f4e5e51100cbc5467e5baf671f588"),
    "humanizer-zh": Companion(
        "op7418/Humanizer-zh", "f4518a8eab97b8bfebc66a89d34320a89bef6930",
        "95627fd4437d886f98032ccc62d79136e6310f1fc04e354bb86431795ff206df"),
    "zh-tw-humanizer": Companion(
        "acchuang/zh-tw-humanizer", "76d7d181067a0cd160d021e0e7b02cc50b191fc6",
        "d66b9b537e6cdac745f669294d89bff90e785faf24b181a4b4f76e4f5a61cdf8"),
    "anti-defensive-writing-zh": Companion(
        "Devilyuu/anti-defensive-writing-zh", "1b0e2025cb42186767db903231db536be1e32405",
        "1e7b3b8545f9ba8f73bfea7099747a4c7324dfaac45bf3417d64481d56013016",
        "656626f512aacf5e9a29fe6c559897c4a0de6cca913c96ccae5213a9f274f225"),
    "nature-writing": Companion(
        "Yuan1z0825/nature-skills", "fe5d5d5c06f0eefe8bbb68fc945dc328f93c5fcb",
        "ce7c4d20329b96b03b0f0c0bb744411b1b4deaa7a7b69b90757705a83c195b12", skill_root="skills/nature-writing"),
    "paperwriter": Companion(
        "Hongcheng-LI/paperwriter", "a5cb8fab75b4bba0bde618d2e3b3ed1bf9a6997f",
        "c6952b68d0193728fc247a4104a8461aee27c92a0becdf3cde44be3b5151d840", skill_root=""),
    "academic-humanizer": Companion(
        "junbolian/Academic-Humanizer", "62b0a02627e063015466c70f0a4dd4929a9f7f5b",
        "fa41c41363c0fed74ca90082ab5c7928a1f98e4710f461d8f11e06792e7b20c8", skill_root="academic-humanizer"),
}

RESOURCES = {
    ("Yuan1z0825/nature-skills", "workflow"): (
        "static/core/workflow.md", "e02426a89e729d6f725d83a4ad41f8393a3aa0fcd968c7a0402a0e2b6b6293fd"),
    ("Hongcheng-LI/paperwriter", "evidence"): (
        "references/evidence.md", "73e7e8f15e56e5a506dcd630496e6ed851b3057b54cbbff49f0b1edf2a14692d"),
    ("Hongcheng-LI/paperwriter", "consistency"): (
        "references/manuscript-si-consistency.md", "dd072a39692f504788a51796508f7045c38d6a059a729ed71e139207df93173f"),
}

MAX_BYTES = 128 * 1024


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Request only the pinned raw URL.


def fetch(url: str) -> bytes:
    with build_opener(NoRedirect()).open(url, timeout=12) as response:
        return response.read(MAX_BYTES + 1)


def installed_directories(name: str) -> tuple[Path, ...]:
    home = Path.home()
    codex = Path(os.environ.get("CODEX_HOME") or home / ".codex")
    roots = (Path(__file__).absolute().parents[2], Path.cwd() / ".agents" / "skills",
             home / ".agents" / "skills", codex / "skills")
    return tuple(dict.fromkeys(root / name for root in roots))


def read_rules(companion: Companion, resource: str, local: Path | None, offline: bool,
               installed: tuple[Path, ...] = ()) -> tuple[str, str]:
    path, digest = "SKILL.md", companion.skill_digest
    if resource == "academic" and companion.academic_digest:
        path, digest = "references/academic-zh.md", companion.academic_digest
    elif (companion.repo, resource) in RESOURCES:
        path, digest = RESOURCES[(companion.repo, resource)]
    elif resource != "skill":
        raise ValueError(f"{companion.repo} has no pinned {resource} resource")

    upstream_path = "/".join(filter(None, (companion.skill_root, path)))
    origin = f"{companion.repo}@{companion.commit}/{upstream_path}"
    candidates = (local,) if local is not None else installed
    for directory in candidates:
        candidate = directory.expanduser() / path
        try:
            if candidate.is_file():
                with candidate.open("rb") as stream:
                    data = stream.read(MAX_BYTES + 1)
                if sha256(data).hexdigest() == digest:
                    return data.decode("utf-8"), f"local {origin}"
        except OSError:
            continue
    if offline:
        raise ValueError(f"no matching local copy of {origin} in offline mode")

    url = f"https://raw.githubusercontent.com/{companion.repo}/{companion.commit}/{upstream_path}"
    data = fetch(url)
    if sha256(data).hexdigest() != digest:
        raise ValueError(f"upstream digest mismatch for {origin}")
    return data.decode("utf-8"), f"upstream {origin}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("companion", choices=COMPANIONS)
    parser.add_argument("--resource", choices=("skill", "academic", "workflow", "evidence", "consistency"), default="skill")
    parser.add_argument("--local", type=Path, metavar="SKILL_DIRECTORY",
                        help="Check this directory instead of the usual installed locations")
    parser.add_argument("--offline", action="store_true", help="Use matching local rules only")
    args = parser.parse_args(argv)
    try:
        locations = () if args.local is not None else installed_directories(args.companion)
        rules, source = read_rules(COMPANIONS[args.companion], args.resource, args.local, args.offline,
                                   locations)
    except (OSError, ValueError, HTTPException) as exc:
        print(f"read_companion: {exc}", file=sys.stderr)
        return 1
    print(f"read_companion: {source}", file=sys.stderr)
    sys.stdout.buffer.write(rules.encode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
