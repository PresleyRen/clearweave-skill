#!/usr/bin/env python3
"""Replay diagnostics on recorded HC3 edits; never generates text or an AI score.

Offline by default. --download fetches two pinned public data files, verifies
whole-file hashes, and extracts the exact original answers. No dataset code runs.
Dataset/adapted text is CC BY-SA 4.0 subject to upstream terms; this script is MIT.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
EVAL = ROOT / 'evals' / 'hc3-2026-10-20'
# Historical evaluations retain the exact instruction and helper snapshot.
RUNTIME = EVAL / 'runtime-v0.2.0'
sys.path.insert(0, str(RUNTIME / 'skills' / 'clearweave' / 'scripts'))
import clearweave_check as checker
import clearweave_risk as risk


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def checked_sources(manifest: dict, case_specs: list[dict]) -> list[dict]:
    originals = []
    for source in manifest['files']:
        url = source['url']
        expected = f"https://huggingface.co/datasets/{source['repo']}/resolve/{source['revision']}/{source['file']}"
        if url != expected or len(source['revision']) != 40:
            raise ValueError('Source URL is not the recorded pinned revision')
        request = urllib.request.Request(url, headers={'User-Agent': 'ClearWeave-HC3-evaluation/0.2.0'})
        with urllib.request.urlopen(request, timeout=90) as response:
            data = response.read(20_000_001)
        if len(data) > 20_000_000 or digest(data) != source['sha256']:
            raise ValueError('Upstream source checksum or size failed')
        rows = [json.loads(line) for line in data.decode('utf-8').splitlines() if line.strip()]
        if len(rows) != source['rows']:
            raise ValueError('Upstream row count changed')
        for case in case_specs:
            if case['language'] != source['language']:
                continue
            row = rows[case['row_index']]
            original = row[case['answer_field']][case['answer_index']]
            if digest(original.encode('utf-8')) != case['original_sha256']:
                raise ValueError('Original answer checksum failed: ' + case['id'])
            originals.append({**case, 'question': row['question'], 'original': original})
    by_id = {r['id']: r for r in originals}
    return [by_id[c['id']] for c in case_specs]


def evaluate(manifest: dict, specs: list[dict], edits: list[dict], samples: list[dict]) -> dict:
    ids = [c['id'] for c in specs]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate case IDs')
    maps = []
    for group in (edits, samples):
        mapped = {r['id']: r for r in group}
        if len(mapped) != len(group) or set(mapped) != set(ids):
            raise ValueError('Case coverage differs')
        maps.append(mapped)
    outputs, originals = maps
    skill_matches = {name: digest((RUNTIME / name).read_bytes()) == sha for name, sha in manifest['skill_hashes'].items()}
    if not all(skill_matches.values()):
        raise ValueError('Runtime skill differs from the evaluated snapshot')
    records = []
    for case in specs:
        sid = case['id']; source = originals[sid]; output = outputs[sid]
        text = source['original']
        if digest(text.encode('utf-8')) != case['original_sha256']:
            raise ValueError('Original checksum failed: ' + sid)
        revision = output.get('revision')
        if revision is None:
            if output['action'] == 'edit':
                raise ValueError('Edited case has no revision')
            revision = text
        if output['action'] != 'edit' and revision != text:
            raise ValueError('A held/excluded/no-op source was changed')
        if digest(revision.encode('utf-8')) != output['revision_sha256']:
            raise ValueError('Revision checksum failed: ' + sid)
        before = checker.lint_text(text, case['language'])
        after = checker.lint_text(revision, case['language'])
        records.append({'id': sid, 'action': output['action'],
                        'language': case['language'], 'label': case['label'],
                        'changed': text != revision,
                        'original_chars': len(text), 'revision_chars': len(revision),
                        'original_words': len(text.split()) if case['language']=='en' else None,
                        'revision_words': len(revision.split()) if case['language']=='en' else None,
                        'lint_before': before, 'lint_after': after,
                        'literal': checker.compare_texts(text, revision),
                        'risk': risk.assess(text, revision)})
    return {'skill_snapshot': manifest['skill_commit'], 'skill_files_verified': len(skill_matches),
            'selected': len(records), 'actions': dict(Counter(r['action'] for r in records)),
            'authorship_labels': dict(Counter(r['label'] for r in records)),
            'original_lint_candidate_total': sum(r['lint_before']['candidate_count'] for r in records),
            'revision_lint_candidate_total': sum(r['lint_after']['candidate_count'] for r in records),
            'edited_cases_with_literal_changes': sum(r['action']=='edit' and r['literal']['supported_literal_changes'] for r in records),
            'edited_cases_with_risk_candidates': sum(r['action']=='edit' and r['risk']['candidate_count']>0 for r in records),
            'semantic_verdict': 'not_provided', 'naturalness_score': None,
            'warning': 'Counts are diagnostics, not semantic fidelity, authorship probabilities, or superiority evidence. Editing and self-review were by the same assistant.',
            'records': records}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--samples', type=Path, default=EVAL/'samples.json')
    parser.add_argument('--download', action='store_true', help='Opt-in network retrieval of pinned public originals')
    parser.add_argument('--report', type=Path, default=EVAL/'checks.json')
    args = parser.parse_args()
    try:
        manifest, specs, edits = [load_json(EVAL/name) for name in ('manifest.json','cases.json','edits.json')]
        if args.download:
            samples = checked_sources(manifest, specs)
            args.samples.parent.mkdir(parents=True, exist_ok=True)
            args.samples.write_text(json.dumps(samples,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        else:
            samples = load_json(args.samples)
        report = evaluate(manifest, specs, edits, samples)
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in report.items() if k!='records'},ensure_ascii=False,indent=2))
        return 0
    except (OSError, ValueError, KeyError, IndexError, TypeError) as exc:
        print(f'hc3-evaluation: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
