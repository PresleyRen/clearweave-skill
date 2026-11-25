#!/usr/bin/env python3
"""Chinese tone candidates, comparable corpus counts and allowlisted edit checking.

Read-only, offline, Python 3.10+. The host editor decides which candidates merit
an edit. LF01–LF11 are traceable rule families, not authorship classifications.
"""
from __future__ import annotations
import argparse
from collections import Counter
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Sequence
import clearweave_check as core

ASSET = Path(__file__).resolve().parents[1] / 'assets/lieflat-rules.json'
HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
ORDINAL = re.compile(r'^(?:第[一二三四五六七八九十百0-9]+[章节部分]*|[一二三四五六七八九十百]+)[、．.：:]\s*')
HEAD = re.compile(r'^( {0,3}#{1,6}[ \t]+)(.*?)(\s+#+)?$')
BOLD = re.compile(r'^(\s*\*\*)(.*?)(\*\*\s*)$')
LIST = re.compile(r'^\s*(?:[-+*]|[0-9]+[.)])[ \t]+')
REFER = re.compile(r'(?:参见|见|按照|根据|第)第?[一二三四五六七八九十百0-9]+(?:条|节|章|步|部分)')
COMMENTS = re.compile(r'^(?:听起来|看起来|看上去|听上去|说白了|值得注意的是|更重要的是|关键在于|问题在于|意味着|不难看出)')
REFERENT = re.compile(r'这|那|其|此|上面|前面|以上|该|它|他|她')
LIST_LEAD = re.compile(r'^(?:具体如下|有以下几点|包括以下(?:内容|方面)|下面列出几点)[：:]\s*$')
DETAIL = re.compile(r'\d|[一二两三四五六七八九十百千万]+(?:小时|分钟|天|年|次|人|个|项)')

@dataclass(frozen=True)
class Block:
    kind: str
    start: int
    end: int
    text: str


def rules() -> dict:
    data = json.loads(ASSET.read_text(encoding='utf-8'))
    result = {r['id']: r for r in data['rules']}
    if list(result) != [f'LF{i:02}' for i in range(1,12)]:
        raise ValueError('Invalid LF rule inventory')
    return result


def blocks(text: str) -> list[Block]:
    """Conservative Markdown blocks: wrapped prose is one paragraph, not lines."""
    protected = [s for s in core.collect_protected_spans(text) if s.kind != 'number']
    visible = list(text)
    for s in protected:
        for i in range(s.start, s.end):
            if visible[i] not in '\r\n': visible[i] = '\ufffc'
    visible = ''.join(visible)
    out, pending, offset, in_list = [], None, 0, False
    lines = text.splitlines(keepends=True)
    for j, line in enumerate(lines):
        end = offset + len(line.rstrip('\r\n')); raw = line.rstrip('\r\n')
        shown = visible[offset:end]; clean = shown.strip()
        next_line = lines[j+1].strip() if j+1<len(lines) else ''
        prev_line = lines[j-1].strip() if j else ''
        if not raw.strip(): kind = 'blank'; in_list = False
        elif not clean.replace('\ufffc','').strip(): kind = 'protected'
        elif HEAD.fullmatch(raw) or BOLD.fullmatch(raw): kind = 'heading'; in_list = False
        elif re.fullmatch(r'(?:=+|-+)\s*',raw.strip()) and len(raw.strip())>=3:
            kind = 'setext' if prev_line and not re.match(r'[#>|]',prev_line) else 'protected'
        elif re.fullmatch(r'(?:=+|-+)',next_line) and len(next_line)>=3: kind='setext'
        elif LIST.match(raw): kind='list'; in_list=True
        elif in_list: kind='list'
        elif '|' in raw: kind='table'
        elif raw.startswith(('    ','\t')) or clean.startswith(('<','![')) or re.match(r'^\[[^\]]+\]:',raw): kind='protected'
        else: kind='prose'
        if kind=='prose':
            if pending is None: pending=offset
        else:
            if pending is not None:
                e=offset
                while e>pending and text[e-1] in '\r\n':e-=1
                out.append(Block('prose',pending,e,visible[pending:e]));pending=None
            out.append(Block(kind,offset,end,shown))
        offset+=len(line)
    if pending is not None:
        e=len(text)
        while e>pending and text[e-1] in '\r\n':e-=1
        out.append(Block('prose',pending,e,visible[pending:e]))
    return out


def _sentences(block: Block):
    for m in re.finditer(r'[^。！？；]+[。！？；]?',block.text):
        lead=len(m[0])-len(m[0].lstrip())
        value=m[0].strip()
        if value:yield block.start+m.start()+lead,value


def heading_parts(text: str):
    m=HEAD.fullmatch(text) or BOLD.fullmatch(text)
    return (m[1],m[2],m[3] or '') if m else None


def scan(text: str, *, keep_rules: Sequence[str]=(), genre: str='general') -> dict:
    catalog=rules();keep=set(keep_rules)
    if keep-set(catalog):raise ValueError('Unknown keep-rule ID')
    if genre not in {'general','academic','literary','procedure'}:raise ValueError('Unknown genre')
    protected = [s for s in core.collect_protected_spans(text) if s.kind!='number']
    bs=blocks(text);ps=[b for b in bs if b.kind=='prose' and HAN.search(b.text)]
    hs=[b for b in bs if b.kind=='heading'];found=[]
    def add(rid,start,end,subtype='',proxy=False):
        if rid in keep or start>=end:return
        if genre in {'literary','procedure'} and rid in {'LF02','LF03','LF04','LF06','LF07'}:return
        excerpt=text[start:end]
        if '\ufffc' in excerpt:return
        # Preserve protected regions even when a broad pattern spans them.
        if any(start<s.end and end>s.start for s in protected):return
        found.append({'rule':rid,'subtype':subtype,'start':start,'end':end,'line':text.count('\n',0,start)+1,
                      'excerpt':excerpt,'review':catalog[rid]['review'],'shape_proxy':proxy})
    for index,b in enumerate(ps):
        sentences=list(_sentences(b))
        for start,sentence in sentences:
            for rid,row in catalog.items():
                if rid=='LF08':
                    adjacent=' '.join(p.text for p in ps[max(0,index-1):index+2])
                    if not DETAIL.search(adjacent):continue
                for pattern in row['patterns']:
                    for m in re.finditer(pattern['pattern'],sentence):add(rid,start+m.start(),start+m.end(),pattern['subtype'])
        for (p,a),(q,c) in zip(sentences,sentences[1:]):
            sig=lambda s:(s.count('，'), '：' in s, ('（' in s or '(' in s),len(s)//15)
            if min(len(a),len(c))>10 and sig(a)==sig(c) and sig(a)[0]>0:
                add('LF03',p,q+len(c),proxy=True)
        if index and sentences:
            start,first=sentences[0];m=COMMENTS.match(first)
            if m and not REFERENT.search(first):add('LF11',start,start+m.end(),proxy=True)
        if LIST_LEAD.fullmatch(b.text.strip()) and re.match(r'\s*(?:[-+*]|\d+[.)])\s',text[b.end:]):
            start=b.start+len(b.text)-len(b.text.lstrip());add('LF05',start,b.end,'list-lead')
    if not REFER.search(text):
        run=[]
        def flush():
            if len(run)>=3:
                for h,m in run:
                    p=heading_parts(text[h.start:h.end]);start=h.start+len(p[0]);add('LF06',start,start+m.end())
        last_level=None
        for h in hs:
            parts=heading_parts(text[h.start:h.end]);m=ORDINAL.match(parts[1]);level=parts[0]
            if not m or (last_level is not None and level!=last_level):flush();run=[]
            if m:run.append((h,m))
            last_level=level
        flush()
    unique={(f['rule'],f['subtype'],f['start'],f['end']):f for f in found}
    found=sorted(unique.values(),key=lambda x:(x['start'],x['rule'],x['subtype']))
    han=sum(len(HAN.findall(b.text)) for b in ps)
    return {'schema_version':1,'mode':'scan','language':'zh','genre':genre,'kept_rules':sorted(keep),
            'counts':{'han_characters':han,'paragraphs':len(ps),'nonfirst_paragraphs':max(0,len(ps)-1),'headings':len(hs)},
            'candidate_count':len(found),'candidates':found,'judgment':'editorial_candidates'}


def measure(texts: Sequence[str]) -> dict:
    if not texts:raise ValueError('Empty corpus')
    totals=Counter();hits=Counter();coverage=Counter();documents=[]
    for text in texts:
        report=scan(text);totals.update(report['counts']);one=Counter(c['rule'] for c in report['candidates'])
        hits.update(one);coverage.update(one.keys())
        documents.append({'sha256':hashlib.sha256(text.encode()).hexdigest(),'counts':report['counts'],'hits':dict(one)})
    result={}
    for rid in rules():
        denominator,scale=('paragraphs',100) if rid=='LF03' else ('nonfirst_paragraphs',100) if rid=='LF11' else ('headings',100) if rid=='LF06' else ('han_characters',1000)
        n=totals[denominator]
        result[rid]={'hits':hits[rid],'documents_with_candidates':coverage[rid],'denominator':denominator,
                     'denominator_value':n,'per':scale,'rate':hits[rid]*scale/n if n else None}
    return {'documents':len(texts),'counts':dict(totals),'rules':result,'per_document':documents}


def compare_corpora(a: Sequence[str], b: Sequence[str]) -> dict:
    left,right=measure(a),measure(b);result={}
    for rid,l in left['rules'].items():
        r=right['rules'][rid];x,y=l['rate'],r['rate']
        result[rid]={'a':x,'b':y,'b_over_a':y/x if x not in (None,0) and y is not None else None,
                     'ratio_status':'defined' if x not in (None,0) and y is not None else 'undefined_denominator'}
    return {'mode':'compare-corpora','ratio_direction':'B / A','a':left,'b':right,'comparison':result}


def verify_edits(original: str, revision: str, edits: list[dict], *, genre: str='general', keep_rules: Sequence[str]=()) -> dict:
    """Check exact reconstruction, locked structure and protected literals."""
    if not isinstance(edits,list):raise ValueError('Edit ledger must be a list')
    catalog=rules();bs=blocks(original);scan_hits=scan(original,genre=genre,keep_rules=keep_rules)['candidates'];checked=[];previous=-1
    for e in edits:
        if not isinstance(e,dict):raise ValueError('Edit must be an object')
        a,b=e.get('start'),e.get('end');rid=e.get('rule');replacement=e.get('replacement')
        if type(a)!=int or type(b)!=int or not (0<=a<=b<=len(original)):raise ValueError('Invalid edit range')
        if a<previous or (a==b==previous):raise ValueError('Overlapping or unordered edits')
        previous=b
        if rid not in catalog or not isinstance(replacement,str) or not isinstance(e.get('reason'),str) or not e['reason'].strip():raise ValueError('Rule, replacement and reason required')
        if e.get('source')!=original[a:b]:raise ValueError('Source span differs')
        if not any(h['rule']==rid and (a<h['end'] and b>h['start'] or a==b==h['start']) for h in scan_hits):raise ValueError('No located candidate for edit')
        block=next((v for v in bs if v.start<=a<=b<=v.end),None)
        if block is None or block.kind not in {'prose','heading'}:raise ValueError('Edit crosses or changes a locked block')
        if block.kind=='heading':
            parts=heading_parts(original[block.start:block.end]);m=ORDINAL.match(parts[1]) if parts else None
            if rid!='LF06' or not m or a!=block.start+len(parts[0]) or b!=a+m.end() or replacement!='':raise ValueError('Only the heading ordinal may change')
        elif rid=='LF06':raise ValueError('LF06 applies only to headings')
        if re.findall(r'\r?\n',original[a:b])!=re.findall(r'\r?\n',replacement):raise ValueError('Line structure changed')
        if any(a<s.end and b>s.start or a==b and s.start<a<s.end for s in core.collect_protected_spans(original) if s.kind!='number'):raise ValueError('Protected span changed')
        checked.append(e)
    rebuilt=original
    for e in reversed(checked):rebuilt=rebuilt[:e['start']]+e['replacement']+rebuilt[e['end']:]
    if rebuilt!=revision:raise ValueError('Revision contains unlisted changes')
    old_shape=[b.kind for b in bs];new_shape=[b.kind for b in blocks(revision)]
    if old_shape!=new_shape:raise ValueError('Document block structure changed')
    literal=core.compare_texts(original,revision)
    if literal['supported_literal_changes']:raise ValueError('Protected literals differ')
    return {'mode':'verify-edits','mechanical_checks':'passed','edit_count':len(checked),
            'rules_used':sorted({e['rule'] for e in checked}),'unlisted_changes':False,
            'block_structure_preserved':True,'semantic_review':'Required for applicability, relationships and antecedents'}


def read(path: str)->str:
    if path=='-':return sys.stdin.read()
    with Path(path).open(encoding='utf-8',newline='') as handle:return handle.read()


def corpus(paths: Sequence[str])->list[str]:
    files=[]
    for name in paths:
        p=Path(name)
        selected=sorted(p.rglob('*.md')) if p.is_dir() else [p]
        for f in selected:
            if f.is_symlink() or '_meta' in f.parts:continue
            if f.resolve() not in files:files.append(f.resolve())
    return [read(str(f)) for f in files]


def main(argv: Sequence[str]|None=None)->int:
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='command',required=True)
    q=sub.add_parser('scan');q.add_argument('file');q.add_argument('--genre',choices=['general','academic','literary','procedure'],default='general');q.add_argument('--keep-rule',action='append',default=[])
    q=sub.add_parser('measure');q.add_argument('paths',nargs='+')
    q=sub.add_parser('compare-corpora');q.add_argument('--a',nargs='+',required=True);q.add_argument('--b',nargs='+',required=True)
    q=sub.add_parser('verify-edits');q.add_argument('original');q.add_argument('revision');q.add_argument('ledger');q.add_argument('--genre',choices=['general','academic','literary','procedure'],default='general');q.add_argument('--keep-rule',action='append',default=[])
    args=p.parse_args(argv)
    try:
        if args.command=='scan':result=scan(read(args.file),keep_rules=args.keep_rule,genre=args.genre)
        elif args.command=='measure':result=measure(corpus(args.paths))
        elif args.command=='compare-corpora':result=compare_corpora(corpus(args.a),corpus(args.b))
        else:
            if '-' in (args.original,args.revision,args.ledger):raise ValueError('verify-edits requires three files')
            result=verify_edits(read(args.original),read(args.revision),json.loads(read(args.ledger)),genre=args.genre,keep_rules=args.keep_rule)
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False));return 0
    except (OSError,UnicodeError,ValueError,KeyError,TypeError) as exc:
        print(f'clearweave-tone: {exc}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
