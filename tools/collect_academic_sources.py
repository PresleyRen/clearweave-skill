#!/usr/bin/env python3
"""Collect pinned writing references and complete, attributed ACL abstracts.

Use --cache for a no-network replay of downloaded source bytes, or --download
for network collection. Missing required data makes the run fail after saving
its diagnostic report. Curated same-paper excerpts repair missing metadata.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import time
from typing import Callable
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'evals' / 'academic-sources'
MAX_BYTES = 16_000_000


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_json(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def relative(name: str) -> Path:
    path = PurePosixPath(name)
    if not name or path.is_absolute() or '..' in path.parts or str(path) != name or '\\' in name:
        raise ValueError('Unsafe relative path: ' + name)
    return Path(name)


def contained(root: Path, name: str) -> Path:
    path = root / relative(name)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path escapes root: ' + name)
    return path


def source_url(repo: str, revision: str, path: str) -> str:
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repo):
        raise ValueError('Invalid repository')
    if not re.fullmatch(r'[a-f0-9]{40}', revision):
        raise ValueError('A pinned 40-character revision is required')
    relative(path)
    return 'https://raw.githubusercontent.com/' + repo + '/' + revision + '/' + urllib.parse.quote(path)


def download(url: str) -> bytes:
    if urllib.parse.urlsplit(url).hostname != 'raw.githubusercontent.com':
        raise ValueError('Only pinned public repository files are downloaded')
    request = urllib.request.Request(url, headers={'User-Agent': 'ClearWeave-source-collector/1'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                if urllib.parse.urlsplit(response.url).hostname != 'raw.githubusercontent.com':
                    raise ValueError('Unexpected download destination')
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError('Source exceeds size limit')
            return data
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2:
                raise
        time.sleep(2 ** attempt)
    raise RuntimeError('Download retries exhausted')


def paper_identifier(collection: str, volume: str, number: str) -> str:
    if '.' in collection:
        return f'{collection}-{volume}.{number}'
    if not volume.isdigit() or not number.isdigit() or len(volume) >= 4:
        raise ValueError('Invalid legacy ACL identifier')
    return collection + '-' + volume + number.zfill(4 - len(volume))


def extract_record(raw: bytes, target: dict, overrides: dict) -> dict:
    sid = paper_identifier(target['collection'], target['volume'], target['paper_id'])
    if sid != target['id']:
        raise ValueError('Paper identity mismatch: ' + target['id'])
    root = ET.fromstring(raw)
    matches = [p for v in root.findall('volume') if v.get('id') == target['volume']
               for p in v.findall('paper') if p.get('id') == target['paper_id']]
    if len(matches) != 1:
        raise ValueError(f'{sid}: expected one paper, got {len(matches)}')
    paper = matches[0]
    def text(element):
        return ''.join(element.itertext()).strip() if element is not None else ''
    title = text(paper.find('title'))
    authors = [' '.join(filter(None, (text(a.find('first')), text(a.find('last')))))
               for a in paper.findall('author')]
    if title != target['title'] or authors != target['authors']:
        raise ValueError(sid + ': bibliographic identity differs from the plan')
    abstract = text(paper.find('abstract'))
    provenance = {'kind': 'acl-xml', 'url': target['source_url']}
    if not abstract:
        fallback = overrides.get(sid)
        if not fallback:
            raise ValueError(sid + ': missing abstract and no reviewed same-paper excerpt')
        if fallback.get('title') != title or fallback.get('authors') != authors:
            raise ValueError(sid + ': fallback belongs to a different paper')
        abstract = fallback['text']
        if not abstract.strip() or digest(abstract.encode('utf-8')) != fallback['text_sha256']:
            raise ValueError(sid + ': fallback text checksum failed')
        if fallback.get('url') != f'https://aclanthology.org/{sid}.pdf' or fallback.get('page') != 1:
            raise ValueError(sid + ': unexpected fallback provenance')
        provenance = {'kind': 'reviewed-pdf-excerpt', 'url': fallback['url'],
                      'page': fallback['page'], 'capture': fallback['capture'],
                      'license': fallback['license']}
    return {'id': sid, 'role': target['role'], 'title': title, 'authors': authors,
            'url': f'https://aclanthology.org/{sid}/', 'text': abstract,
            'text_sha256': digest(abstract.encode('utf-8')), 'abstract_source': provenance,
            'xml_sha256': digest(raw), 'license': target['license']}


def validate_plan(plan: dict) -> None:
    if plan.get('schema_version') != 1 or not plan['sources'] or not plan['targets']:
        raise ValueError('Invalid or empty collection plan')
    for group in ('sources', 'targets'):
        ids = [row['id'] for row in plan[group]]
        if len(set(ids)) != len(ids):
            raise ValueError('Duplicate IDs in ' + group)
    keys = [row['collection'] for row in plan['collections']]
    if len(set(keys)) != len(keys):
        raise ValueError('Duplicate collections')
    for row in plan['sources']:
        if not re.fullmatch(r'S\d{2}', row['id']):
            raise ValueError('Invalid source ID')
        paths = [f['path'] for f in row['files']]
        if len(set(paths)) != len(paths) or row['entry'] not in paths:
            raise ValueError('Missing or duplicated entry file')
        for file in row['files']:
            source_url(row['repo'], row['revision'], file['path'])
    for row in plan['collections']:
        source_url('acl-org/acl-anthology', row['revision'], 'data/xml/' + row['collection'] + '.xml')
    for target in plan['targets']:
        if target['collection'] not in keys:
            raise ValueError('Target has no collection')
        collection = next(c for c in plan['collections'] if c['collection'] == target['collection'])
        url = source_url('acl-org/acl-anthology', collection['revision'], 'data/xml/' + target['collection'] + '.xml')
        if target['source_url'] != url:
            raise ValueError('Target provenance differs from collection')


def collect(plan: dict, overrides: dict, loader: Callable[[str, str], bytes], out: Path) -> dict:
    validate_plan(plan)
    sources, samples, errors = [], [], []
    def checked(url, local, expected):
        data = loader(url, local)
        if len(data) > MAX_BYTES or digest(data) != expected:
            raise ValueError('Source checksum or size failed: ' + local)
        path = contained(out, local)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return data
    for source in plan['sources']:
        result = {'id': source['id'], 'repo': source['repo'], 'revision': source['revision'], 'files': []}
        for file in source['files']:
            try:
                local = source['id'] + '/' + file['path']
                data = checked(source_url(source['repo'], source['revision'], file['path']), local, file['sha256'])
                result['files'].append({'path': file['path'], 'sha256': digest(data), 'bytes': len(data)})
            except (OSError, ValueError) as exc:
                errors.append({'kind': 'source', 'id': source['id'], 'path': file['path'], 'error': str(exc)})
        sources.append(result)
    for collection in plan['collections']:
        name = collection['collection']
        targets = [t for t in plan['targets'] if t['collection'] == name]
        try:
            raw = checked(source_url('acl-org/acl-anthology', collection['revision'], 'data/xml/' + name + '.xml'),
                          name + '.xml', collection['sha256'])
        except (OSError, ValueError) as exc:
            errors.append({'kind': 'collection', 'id': name, 'error': str(exc)})
            continue
        for target in targets:
            try:
                samples.append(extract_record(raw, target, overrides))
            except (ValueError, ET.ParseError, KeyError, TypeError) as exc:
                errors.append({'kind': 'sample', 'id': target['id'], 'error': str(exc)})
    summary = {'status': 'complete' if not errors and len(samples) == len(plan['targets']) else 'incomplete',
               'requested_sources': len(plan['sources']),
               'completed_sources': sum(len(r['files']) == len(s['files']) for r, s in zip(sources, plan['sources'])),
               'verified_source_files': sum(len(s['files']) for s in sources),
               'requested_samples': len(plan['targets']), 'completed_samples': len(samples),
               'fallbacks_used': [s['id'] for s in samples if s['abstract_source']['kind'] == 'reviewed-pdf-excerpt'],
               'errors': errors}
    write_json(out / 'source-manifest.json', sources)
    write_json(out / 'acl-samples.json', {'samples': samples})
    write_json(out / 'collection-report.json', summary)
    return summary


def replay_records() -> dict:
    plan = read_json(DATA / 'plan.json')
    overrides = read_json(DATA / 'abstract-overrides.json')
    records = read_json(DATA / 'records.json')
    expected = {t['id']: t for t in plan['targets']}
    if len(records) != len(expected) or {r['id'] for r in records} != set(expected):
        raise ValueError('Real-record fixture coverage mismatch')
    for row in records:
        raw = row['xml'].encode('utf-8')
        if digest(raw) != row['xml_sha256']:
            raise ValueError('Fixture checksum failed')
        result = extract_record(raw, expected[row['id']], overrides)
        if result['text_sha256'] != row['expected_text_sha256']:
            raise ValueError('Extracted abstract differs: ' + row['id'])
    return {'real_acl_records_checked': len(records), 'status': 'passed'}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--cache', type=Path, help='Replay exact downloaded source files without network access')
    mode.add_argument('--download', action='store_true')
    mode.add_argument('--replay-fixtures', action='store_true', help='Check six real ACL record fixtures offline')
    parser.add_argument('--out', type=Path, default=Path('research'))
    args = parser.parse_args(argv)
    try:
        if args.replay_fixtures:
            report = replay_records()
        else:
            if args.cache and args.cache.resolve() == args.out.resolve():
                raise ValueError('Input cache and output directory must differ')
            def loader(url, local):
                return contained(args.cache, local).read_bytes() if args.cache else download(url)
            report = collect(read_json(DATA / 'plan.json'), read_json(DATA / 'abstract-overrides.json'), loader, args.out)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report['status'] in ('complete', 'passed') else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        args.out.mkdir(parents=True, exist_ok=True)
        write_json(args.out / 'collection-report.json', {'status': 'incomplete', 'errors': [str(exc)]})
        print('academic-collection: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
