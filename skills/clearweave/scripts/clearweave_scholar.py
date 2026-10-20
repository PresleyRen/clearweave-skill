#!/usr/bin/env python3
"""Read-only academic candidates, corpus profiles, and revision-learning proposals."""
from __future__ import annotations
import argparse
from bisect import bisect_right
from collections import Counter
import difflib
import hashlib
import json
import math
from pathlib import Path
import re
import statistics
import sys
from typing import Sequence
from clearweave_check import collect_protected_spans

# These are review questions, not unconditional replacements or authorship labels.
RULES = [
    ('AD01','en',r'\b(?:may\s+possibly|could\s+potentially|might\s+perhaps)',
     'Inspect stacked uncertainty; retain the uncertainty actually carried by the claim.'),
    ('AD02','en',r'\b(?:unfortunately|regrettably)\b|\bonly\s+achieves?\b',
     'State the result directly; retain the baseline and any substantive negative finding.'),
    ('AD03','en',r'\b(?:we\s+(?:do\s+not\s+claim|acknowledge\s+that)|this\s+(?:paper|study)\s+does\s+not\s+claim)\b',
     'Separate a real scope condition or reviewer answer from a repeated disclaimer.'),
    ('AD04','en',r'\b(?:it\s+(?:is\s+worth\s+noting|should\s+be\s+noted)\s+that|to\s+be\s+clear)\b',
     'Check whether the framing adds information; keep the content it introduces.'),
    ('AD05','zh',r'(?:遗憾|遺憾|很抱歉|必须承认|必須承認|我们承认|我們承認)(?:的是|的?是|，|,)?',
     '直接陈述结果；区分空自谦、真实缺点与审稿回复。'),
    ('AD06','zh',r'(?:可能也许|可能也許|也许可能|也許可能|或许可能|或許可能)',
     '检查重复的不确定表达，保留实际概率强度。'),
    ('AD07','zh',r'(?:我们并不声称|我們並不聲稱|本文并不声称|本文並不聲稱|需要(?:特别|特別)?说明的是|需要(?:特别|特別)?說明的是)',
     '把范围和贡献直接写清楚，保留确有信息的排除条件。'),
    ('AD08','zh',r'(?:值得注意的是|值得一提的是|不可否认的是|不可否認的是)',
     '检查引导语的作用，保留事实与必要限定。'),
    ('GR01','en',r'\b[A-Z][A-Za-z0-9_-]*(?:\s*\([^\n)]*\))?\s+and\s+[A-Z][A-Za-z0-9_-]*(?:\s*\([^\n)]*\))?\s+(?:has|is|was)\b',
     'Check agreement with a coordinated subject; a single named unit can be an exception.'),
    ('GR02','en',r'\b(?:model|network|method|framework|system|approach)\s+that\s+(?:use|produce|generate|provide|require|reduce|support|yield)\b',
     'Identify the relative-clause antecedent; a singular head normally takes a singular verb.'),
    ('GR03','en',r'\b(?:an\s+(?:model|method|network)|a\s+(?:information|evidence)|these\s+(?:method|result|criterion))\b',
     'Check article/countability or demonstrative agreement in this local noun phrase.'),
    ('GR04','en',r'\b(?:this\s+criteria|a\s+criteria|these\s+phenomenon)\b',
     'Check the singular/plural word form while retaining the intended quantity.'),
]
COMPILED = [(i,l,re.compile(p, re.IGNORECASE if i!='GR01' else 0),q) for i,l,p,q in RULES]
HAN = re.compile(r'[\u3400-\u4dbf\u4e00-\u9fff]')
WORD = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|[\u3400-\u4dbf\u4e00-\u9fff]|\d+(?:\.\d+)?")


def digest(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def language_of(text: str) -> str:
    return 'zh' if len(HAN.findall(text)) > len(re.findall(r'[A-Za-z]+',text)) else 'en'


def mask_protected(text: str) -> str:
    chars = list(text)
    for span in collect_protected_spans(text):
        for i in range(span.start, span.end):
            if chars[i] not in '\r\n': chars[i] = ' '
    return ''.join(chars)


def scan(text: str, language: str = 'both') -> dict:
    if language not in {'en','zh','both'}: raise ValueError('language must be en, zh or both')
    protected = collect_protected_spans(text)
    starts = [0] + [m.end() for m in re.finditer('\n', text)]
    findings = []
    for rid,lang,pattern,question in COMPILED:
        if language != 'both' and lang != language: continue
        for m in pattern.finditer(text):
            # Citation-only spans may occur between a coordinated subject and verb.
            # We permit those inside GR01, but never report an edit inside a quote/code/math span.
            blockers = [s for s in protected if s.start < m.end() and m.start() < s.end]
            if blockers and not (rid == 'GR01' and all(s.kind in {'number','citation'} for s in blockers)):
                continue
            line = bisect_right(starts, m.start())
            findings.append({'rule':rid,'language':lang,'start':m.start(),'end':m.end(),
                             'line':line,'column':m.start()-starts[line-1]+1,
                             'span':m.group(),'question':question,'status':'review_candidate'})
    findings.sort(key=lambda r:(r['start'],r['rule']))
    return {'schema_version':1,'operation':'academic_scan','input_sha256':digest(text),
            'findings':findings,'counts':dict(Counter(r['rule'] for r in findings))}


def metrics(text: str) -> dict:
    prose = mask_protected(text)
    # Protect common abbreviation periods and decimals during approximate splitting.
    segmented = re.sub(r'\b(?:e\.g|i\.e|et al|Fig|Eq|Dr|vs)\.',
                       lambda m:m.group().replace('.','\u2024'), prose, flags=re.I)
    segmented = re.sub(r'(?<=\d)\.(?=\d)','\u2024',segmented)
    sentences = [s for s in re.split(r'[.!?。！？]+(?:[ \t\r\n]+|$)|[。！？]+',segmented) if WORD.search(s)]
    lengths = [len(WORD.findall(s)) for s in sentences]
    tokens = WORD.findall(prose)
    n = len(tokens)
    return {'characters':len(text),'token_units':n,'sentences_approx':len(sentences),
            'paragraphs':len([p for p in re.split(r'\n\s*\n',prose) if WORD.search(p)]),
            'mean_sentence_units':round(statistics.mean(lengths),3) if lengths else 0,
            'median_sentence_units':statistics.median(lengths) if lengths else 0,
            'first_person_per_100_units':round(100*len(re.findall(r'\b(?:we|our|I|my)\b|我们|我們',prose,re.I))/n,3) if n else 0,
            'semicolons':prose.count(';')+prose.count('；'),
            'dashes':prose.count('—')}


def profile(data: dict, kind: str = 'field', label: str = 'academic') -> dict:
    if kind not in {'field','house','author'}: raise ValueError('Invalid profile kind')
    if not isinstance(data,dict) or not isinstance(data.get('samples'),list):
        raise ValueError('Expected an object containing a samples list')
    if not label.strip(): raise ValueError('Profile label must not be empty')
    records, skipped, works, hashes, ids, languages = [], [], set(), set(), set(), set()
    for row in data['samples']:
        if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'].strip():
            raise ValueError('Each sample needs a nonempty string id')
        sid = row['id']
        if sid in ids: raise ValueError('Duplicate sample id: '+sid)
        ids.add(sid)
        if row.get('role','profile') != 'profile':
            skipped.append({'id':sid,'reason':'different_role'});continue
        text = row.get('text')
        if not isinstance(text,str): raise ValueError('Sample text must be a string')
        if not text.strip():
            skipped.append({'id':sid,'reason':'empty_text'});continue
        work = row.get('work_id',sid)
        if not isinstance(work,str) or not work.strip(): raise ValueError('Invalid work_id')
        sha = digest(text)
        if work in works or sha in hashes:
            skipped.append({'id':sid,'reason':'duplicate_work_or_text'});continue
        lang = row.get('language',language_of(text))
        if lang not in {'en','zh'}: raise ValueError('Invalid sample language')
        languages.add(lang);works.add(work);hashes.add(sha)
        records.append({'id':sid,'work_id':work,'text_sha256':sha,'metrics':metrics(text)})
    if not records: raise ValueError('No nonempty profile samples')
    if len(languages)>1: raise ValueError('Use separate profiles for English and Chinese')
    return {'schema_version':1,'operation':'corpus_profile','kind':kind,'label':label,
            'language':next(iter(languages)),'sample_count':len(records),
            'samples':records,'skipped':skipped,
            'means':{k:round(statistics.mean(r['metrics'][k] for r in records),3) for k in records[0]['metrics']},
            'measurement':'Approximate editable-prose units; English words and Chinese characters. Descriptive, not targets.',
            'traits':[],'approval':'observed_metrics'}


def compare_profile(p: dict, text: str) -> dict:
    if not isinstance(p,dict) or p.get('operation')!='corpus_profile' or p.get('schema_version')!=1:
        raise ValueError('Expected a corpus_profile schema_version 1')
    if not text.strip(): raise ValueError('Draft must not be empty')
    if p.get('language') != language_of(text): raise ValueError('Draft/profile language mismatch')
    current=metrics(text)
    if not isinstance(p.get('means'),dict) or set(current)!=set(p['means']):
        raise ValueError('Invalid profile means')
    if any(type(v) not in {int,float} or not math.isfinite(v) for v in p['means'].values()): raise ValueError('Non-numeric profile mean')
    return {'operation':'profile_comparison','profile_label':p.get('label'),
            'draft_sha256':digest(text),'metrics':current,
            'difference_from_sample_mean':{k:round(v-p['means'][k],3) for k,v in current.items()}}


def learn(original: str, final: str, scope: str) -> dict:
    if not scope.strip() or not original.strip() or not final.strip():
        raise ValueError('Scope, original and final must be nonempty')
    before=re.findall(r'\S+|\s+',original);after=re.findall(r'\S+|\s+',final)
    changes=[{'operation':tag,'before':''.join(before[a:b]),'after':''.join(after[c:d])}
             for tag,a,b,c,d in difflib.SequenceMatcher(a=before,b=after,autojunk=False).get_opcodes() if tag!='equal']
    return {'schema_version':1,'operation':'preference_proposal','scope':scope,
            'original_sha256':digest(original),'final_sha256':digest(final),'changes':changes,
            'approval':'pending','rules':[],
            'next_step':'Classify changes as preference, grammar, facts, or task-specific edits; approve scoped rules separately.'}


def read_text(path: str) -> str:
    return sys.stdin.read() if path=='-' else Path(path).read_text(encoding='utf-8')


def main(argv: Sequence[str] | None = None) -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('scan');p.add_argument('file');p.add_argument('--language',choices=['en','zh','both'],default='both')
    p=sub.add_parser('profile');p.add_argument('samples');p.add_argument('--kind',choices=['field','house','author'],default='field');p.add_argument('--label',default='academic')
    p=sub.add_parser('compare-profile');p.add_argument('profile');p.add_argument('draft')
    p=sub.add_parser('learn');p.add_argument('original');p.add_argument('final');p.add_argument('--scope',required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='scan': result=scan(read_text(args.file),args.language)
        elif args.command=='profile': result=profile(json.loads(read_text(args.samples)),args.kind,args.label)
        elif args.command=='compare-profile':
            if args.profile=='-' and args.draft=='-': raise ValueError('At most one input can use stdin')
            result=compare_profile(json.loads(read_text(args.profile)),read_text(args.draft))
        else:
            if args.original=='-' and args.final=='-': raise ValueError('At most one input can use stdin')
            result=learn(read_text(args.original),read_text(args.final),args.scope)
        print(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False));return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        print(f'clearweave-scholar: {exc}',file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
