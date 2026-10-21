#!/usr/bin/env python3
"""Replay recorded public-paper/HC3 edits and verify provenance. No model inference."""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
import re
from pathlib import Path
import sys
import urllib.request
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'evals/scholarly-2026-10-20'
RUNTIME = DATA / 'runtime-v0.3.0'
sys.path.insert(0,str(RUNTIME/'skills/clearweave/scripts'))
import clearweave_scholar as scholar
import clearweave_check as checker
import clearweave_risk as risk

def digest(text: str)->str:return hashlib.sha256(text.encode('utf-8')).hexdigest()
def load(path: Path):return json.loads(path.read_text(encoding='utf-8'))
def reviewed_pdf_text(record: dict, root: Path=ROOT) -> str:
    """Verify the reviewed excerpt's identity and text; never claim a PDF re-fetch."""
    provenance=record.get('abstract_source', {})
    if provenance.get('kind')!='reviewed-pdf-excerpt':raise ValueError('Missing excerpt provenance')
    overrides=load(root/'evals/academic-sources/abstract-overrides.json')
    excerpt=overrides[record['id']]
    expected_url=f"https://aclanthology.org/{record['id']}.pdf"
    if excerpt['url']!=expected_url or provenance.get('url')!=expected_url or provenance.get('page')!=1:
        raise ValueError('Excerpt URL/page differs')
    if excerpt['title']!=record['title'] or excerpt['authors']!=record['authors']:
        raise ValueError('Excerpt bibliographic identity differs')
    if digest(excerpt['text'])!=excerpt['text_sha256'] or excerpt['text_sha256']!=record['text_sha256']:
        raise ValueError('Excerpt text hash differs')
    return excerpt['text']

def source_verify(samples: list[dict])->dict:
    cache={};verified=[];excerpts=[]
    for r in samples:
        if not re.fullmatch(r'[0-9a-f]{40}',r['revision']):raise ValueError('Invalid revision')
        if not re.fullmatch(r'[A-Za-z0-9_.-]+',r['source_file']):raise ValueError('Invalid source file')
        if r['source_type']=='published_paper':
            url=f"https://raw.githubusercontent.com/acl-org/acl-anthology/{r['revision']}/data/xml/{r['source_file']}"
        else:
            if r['dataset']!='Hello-SimpleAI/HC3-Chinese':raise ValueError('Unexpected dataset')
            url=f"https://huggingface.co/datasets/{r['dataset']}/resolve/{r['revision']}/{r['source_file']}"
            if url!=r['url']:raise ValueError('Unexpected source URL')
        if url not in cache:
            request=urllib.request.Request(url,headers={'User-Agent':'ClearWeave-scholarly-evaluation/0.3.0'})
            with urllib.request.urlopen(request,timeout=90) as response:blob=response.read(40_000_001)
            if len(blob)>40_000_000:raise ValueError('Source exceeds size limit')
            cache[url]=blob
        blob=cache[url]
        if r['source_type']=='published_paper':
            if hashlib.sha256(blob).hexdigest()!=r['source_sha256']:raise ValueError('XML hash differs: '+r['id'])
            node=ET.fromstring(blob).find(f"volume[@id='{r['volume']}']/paper[@id='{r['paper_id']}']/abstract")
            text='' if node is None else ''.join(node.itertext())
            if not text and r.get('abstract_source',{}).get('kind')=='reviewed-pdf-excerpt':
                text=reviewed_pdf_text(r);excerpts.append(r['id'])
        else:
            lines=blob.decode('utf-8').splitlines();record=json.loads(lines[r['row_index']])
            text=record[r['answer_field']][r['answer_index']]
        if digest(text)!=r['text_sha256']:raise ValueError('Source text differs: '+r['id'])
        verified.append(r['id'])
    return {'files':len(cache),'records_verified':verified,'reviewed_pdf_excerpts_checked':excerpts,'verification':'Pinned XML/JSONL downloaded; reviewed PDF excerpt checked against its attributed record, not fetched again.'}

def evaluate(samples: list[dict], outputs: list[dict], protocol: dict, root: Path=ROOT)->dict:
    if not isinstance(samples,list) or not isinstance(outputs,list):raise ValueError('Expected record lists')
    ids=[r['id'] for r in samples]
    if len(ids)!=len(set(ids)):raise ValueError('Duplicate sample ID')
    for r in samples:
        if not isinstance(r['text'],str) or digest(r['text'])!=r['text_sha256']:raise ValueError('Input hash differs: '+r['id'])
        if r['role'] not in {'profile','edit'}:raise ValueError('Unknown sample role')
        if r['source_type'] not in {'published_paper','HC3_chatgpt_answer'}:raise ValueError('Unknown provenance')
        if len(r['revision'])!=40 or not r.get('url') or not r.get('license'):raise ValueError('Missing source provenance')
        if r.get('abstract_source',{}).get('kind')=='reviewed-pdf-excerpt':reviewed_pdf_text(r,root)
    prof=[r for r in samples if r['role']=='profile']; edits=[r for r in samples if r['role']=='edit']
    if {r['work_id'] for r in prof}&{r['work_id'] for r in edits}:raise ValueError('Profile/edit work overlap')
    if {r['text_sha256'] for r in prof}&{r['text_sha256'] for r in edits if r['text']}:raise ValueError('Profile/edit text overlap')
    out={r['id']:r for r in outputs}
    if len(out)!=len(outputs) or set(out)!={r['id'] for r in edits}:raise ValueError('Output coverage differs')
    for name,sha in protocol['runtime_files'].items():
        p=Path(name)
        if p.is_absolute() or '..' in p.parts or not name.startswith('skills/clearweave/'):raise ValueError('Invalid runtime path')
        if hashlib.sha256((root/'evals/scholarly-2026-10-20/runtime-v0.3.0'/p).read_bytes()).hexdigest()!=sha:raise ValueError('Runtime differs: '+name)
    records=[]
    for r in edits:
        o=out[r['id']];before=r['text'];after=o['revision']
        if o['input_sha256']!=r['text_sha256'] or digest(after)!=o['revision_sha256']:raise ValueError('Output hash differs: '+r['id'])
        if o['action'] not in {'edit','keep','missing_source'}:raise ValueError('Unknown action')
        if o['action']!='edit' and before!=after:raise ValueError('Non-edit changed source')
        if o['action']=='edit' and (not before or not after or before==after):raise ValueError('Invalid edit')
        if (o['action']=='missing_source')!= (not before):raise ValueError('Missing source mislabeled')
        if 'initial_revision' in o and digest(o['initial_revision'])!=o.get('initial_revision_sha256'):raise ValueError('Initial revision hash differs')
        if not o.get('notes') or not o.get('reviewer'):raise ValueError('Review record missing')
        records.append(dict(id=r['id'],action=o['action'],source_type=r['source_type'],language=r['language'],characters_before=len(before),characters_after=len(after),words_before=len(before.split()) if r['language']=='en' else None,words_after=len(after.split()) if r['language']=='en' else None,academic_before=scholar.scan(before,r['language']),academic_after=scholar.scan(after,r['language']),literal=checker.compare_texts(before,after),risk=risk.assess(before,after)))
    measured=scholar.profile({'samples':samples},'field','NLP-abstracts')
    return dict(schema_version=1,skill_version=protocol['skill_version'],runtime_files_verified=len(protocol['runtime_files']),profile_samples=measured['sample_count'],editing_records=len(edits),actions=dict(Counter(r['action'] for r in records)),academic_candidates_before=sum(len(r['academic_before']['findings']) for r in records),academic_candidates_after=sum(len(r['academic_after']['findings']) for r in records),edited_with_literal_differences=sum(r['action']=='edit' and bool(r['literal']['supported_literal_changes']) for r in records),edited_with_risk_candidates=sum(r['action']=='edit' and r['risk']['candidate_count']>0 for r in records),evaluation_kind='recorded same-assistant applications / deterministic replay',records=records)

def main()->int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--download',action='store_true',help='Re-fetch pinned public sources and check their text hashes');p.add_argument('--write',action='store_true',help='Write replay report.json; otherwise print a summary')
    args=p.parse_args()
    try:
        samples=load(DATA/'samples.json')['samples'];outputs=load(DATA/'outputs.json');protocol=load(DATA/'protocol.json')
        report=evaluate(samples,outputs,protocol)
        if args.download:report['fresh_source_verification']=source_verify(samples)
        if args.write:(DATA/'report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in report.items() if k!='records'},ensure_ascii=False,indent=2));return 0
    except (OSError,ValueError,KeyError,TypeError,ET.ParseError) as exc:
        print(f'scholarly-evaluation: {exc}',file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
