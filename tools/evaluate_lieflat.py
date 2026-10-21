#!/usr/bin/env python3
"""Replay saved LF-only applications and optionally verify their public originals."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'evals/lieflat-2026-10-21'
sys.path.insert(0,str(ROOT/'skills/clearweave/scripts'))
import clearweave_tone as tone
import clearweave_risk as risk

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def digest(text):return hashlib.sha256(text.encode()).hexdigest()
def evaluate(samples,outputs,protocol,root=ROOT):
    if len(samples)!=len({s['id'] for s in samples}):raise ValueError('Duplicate source ID')
    by_id={o['id']:o for o in outputs}
    if len(by_id)!=len(outputs) or set(by_id)!={s['id'] for s in samples}:raise ValueError('Output coverage differs')
    for name,expected in protocol['runtime_files'].items():
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or not name.startswith('skills/clearweave/'):raise ValueError('Runtime path invalid')
        if hashlib.sha256((root/p).read_bytes()).hexdigest()!=expected:raise ValueError('Runtime differs: '+name)
    rows=[]
    for s in samples:
        o=by_id[s['id']]
        if digest(s['text'])!=s['text_sha256'] or o['input_sha256']!=s['text_sha256']:raise ValueError('Source hash differs')
        if digest(o['revision'])!=o['revision_sha256']:raise ValueError('Revision hash differs')
        if o['action'] not in {'edit','keep'} or (o['action']=='keep')!=(s['text']==o['revision']):raise ValueError('Action differs')
        verified=tone.verify_edits(s['text'],o['revision'],o['edits'])
        rows.append({'id':s['id'],'action':o['action'],'before':tone.scan(s['text']),
                     'after':tone.scan(o['revision']),'ledger':verified,'risk':risk.assess(s['text'],o['revision'])})
    return {'version':protocol['version'],'records':rows,'summary':{'inputs':len(rows),'edited':sum(x['action']=='edit' for x in rows),
            'unchanged':sum(x['action']=='keep' for x in rows),'edits':sum(x['ledger']['edit_count'] for x in rows),
            'candidates_before':sum(x['before']['candidate_count'] for x in rows),'candidates_after':sum(x['after']['candidate_count'] for x in rows),
            'mechanical_checks':'passed'},'evaluation_type':'Recorded same-assistant application; no authorship or quality score'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--download',action='store_true');p.add_argument('--write',action='store_true');a=p.parse_args()
    try:
        s=load(DATA/'samples.json')['samples'];o=load(DATA/'outputs.json');r=evaluate(s,o,load(DATA/'protocol.json'))
        if a.download:
            spec=importlib.util.spec_from_file_location('cw_historical_sources',ROOT/'tools/evaluate_scholarly.py')
            ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
            r['source_verification']=ev.source_verify(s)
        if a.write:(DATA/'report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in r.items() if k!='records'},ensure_ascii=False,indent=2));return 0
    except (OSError,UnicodeError,ValueError,TypeError,KeyError) as exc:
        print(f'lieflat-evaluation: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
