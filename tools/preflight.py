#!/usr/bin/env python3
"""Test the working tree on code regressions and real source data before pushing.

Offline: --source-cache <downloaded-research> --hc3-samples <samples.json>
Online:  --download (explicitly fetches pinned public source data).
Reports and logs go to .preflight/; a failing check returns a nonzero exit code.
"""
from __future__ import annotations
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.preflight'


def snapshot() -> dict[str, str]:
    result = {}
    for path in sorted(ROOT.rglob('*')):
        rel = path.relative_to(ROOT)
        if any(p in {'.git', '.preflight', '__pycache__', '.venv', 'research'} for p in rel.parts):
            continue
        if path.is_file() and path.suffix not in {'.pyc', '.zip'}:
            result[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-cache', type=Path)
    parser.add_argument('--hc3-samples', type=Path)
    parser.add_argument('--download', action='store_true')
    args = parser.parse_args(argv)
    if args.download and (args.source_cache or args.hc3_samples):
        parser.error('Choose online downloads or two explicit offline data paths')
    if not args.download and not (args.source_cache and args.hc3_samples):
        parser.error('Offline tests require both --source-cache and --hc3-samples')
    OUT.mkdir(exist_ok=True)
    before = snapshot()
    python = sys.executable
    collection = [python, 'tools/collect_academic_sources.py', '--out', str(OUT/'research')]
    hc3 = [python, 'tools/evaluate_hc3.py', '--report', str(OUT/'hc3-checks.json')]
    if args.download:
        collection += ['--download']
        hc3 += ['--download', '--samples', str(OUT/'hc3-samples.json')]
    else:
        collection += ['--cache', str(args.source_cache.resolve())]
        hc3 += ['--samples', str(args.hc3_samples.resolve())]
    commands = [
        ('unit', [python, '-m', 'unittest', 'discover', '-s', 'tests', '-v']),
        ('package', [python, 'tools/validate_repo.py']),
        ('real-acl-records', [python, 'tools/collect_academic_sources.py', '--replay-fixtures']),
        ('full-source-replay', collection),
        ('hc3-recorded-edits', hc3),
        ('scholarly-current-edits', [python, 'tools/evaluate_scholarly.py'] + (['--download'] if args.download else [])),
    ]
    results = []
    for name, command in commands:
        try:
            run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=420)
            log = run.stdout + run.stderr
            code = run.returncode
        except (OSError, subprocess.TimeoutExpired) as exc:
            code, log = 2, str(exc)
        (OUT/(name+'.log')).write_text(log, encoding='utf-8')
        results.append({'check': name, 'returncode': code, 'log': name+'.log'})
        print(name + ': ' + ('PASS' if code == 0 else 'FAIL'))
    unchanged = before == snapshot()
    passed = unchanged and all(r['returncode'] == 0 for r in results)
    report = {'status': 'passed' if passed else 'failed',
              'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'python': sys.version, 'source_tree_unchanged_during_tests': unchanged,
              'tested_files': before, 'checks': results,
              'data_mode': 'pinned-downloads' if args.download else 'verified-offline-source-replay'}
    (OUT/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Preflight ' + report['status'] + '; report: ' + str(OUT/'report.json'))
    return 0 if passed else 1


if __name__ == '__main__':
    raise SystemExit(main())
