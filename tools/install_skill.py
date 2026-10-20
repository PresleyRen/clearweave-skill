#!/usr/bin/env python3
"""Copy ClearWeave into an explicitly selected project; never overwrite."""
from __future__ import annotations
import argparse
from pathlib import Path
import shutil
import sys


def install(project: Path) -> Path:
    project = project.expanduser().resolve(strict=True)
    if not project.is_dir():
        raise ValueError("--project must be an existing directory")
    source = Path(__file__).resolve().parents[1] / "skills" / "clearweave"
    destination = project / ".agents" / "skills" / "clearweave"
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(f"Refusing to overwrite existing destination: {destination}")
    if not destination.parent.resolve().is_relative_to(project):
        raise ValueError("The skill destination resolves outside the selected project")
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True,
                        help="Existing project directory; installs into .agents/skills/clearweave")
    args = parser.parse_args(argv)
    try:
        destination = install(args.project)
    except (OSError, ValueError) as exc:
        print(f"clearweave install: {exc}", file=sys.stderr)
        return 2
    print(f"Installed: {destination}")
    print("Select clearweave in your host, or invoke $clearweave in Codex CLI/IDE.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
