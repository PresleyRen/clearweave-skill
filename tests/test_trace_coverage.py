"""Structural coverage and fault-injection tests, not model-writing scores."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/clearweave/scripts'))
import clearweave_trace as trace
spec=importlib.util.spec_from_file_location('cw_coverage',ROOT/'tools/coverage.py')
coverage=importlib.util.module_from_spec(spec);spec.loader.exec_module(coverage)

class TraceTests(unittest.TestCase):
    def setUp(self):self.catalog=trace.load_catalog()
    def test_capability(self):
        self.assertEqual(trace.trace(self.catalog,identifier='CW05')['matches'][0]['id'],'CW05')
    def test_conflict(self):
        self.assertGreater(len(trace.trace(self.catalog,identifier='CF17')['matches']),0)
    def test_source(self):
        self.assertTrue(all('S04' in c['sources'] for c in trace.trace(self.catalog,identifier='S04')['matches']))
    def test_chinese_query(self):
        self.assertIn('CW05',{r['id'] for r in trace.trace(self.catalog,query='否定被删掉')['matches']})
    def test_english_query(self):
        self.assertIn('CW04',{r['id'] for r in trace.trace(self.catalog,query='numbers units')['matches']})
    def test_unknown(self):self.assertEqual(trace.trace(self.catalog,identifier='CW99')['matches'],[])
    def test_no_match_does_not_fabricate(self):self.assertEqual(trace.trace(self.catalog,query='zzzzzzzzzz')['matches'],[])
    def test_whitespace_rejected(self):
        with self.assertRaises(ValueError):trace.trace(self.catalog,query='  ')
    def test_both_options_rejected(self):
        with self.assertRaises(ValueError):trace.trace(self.catalog,identifier='CW01',query='scope')
    def test_catalog_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'assets').mkdir();cat=deepcopy(self.catalog)
            cat['capabilities'][0]['module']='../../outside.md'
            (root/'assets/capabilities.json').write_text(json.dumps(cat))
            with self.assertRaises(ValueError):trace.load_catalog(root)

class CoverageTests(unittest.TestCase):
    def test_complete_current_inventory(self):
        report=coverage.validate();self.assertEqual(report['structural_errors'],[])
        self.assertEqual((report['sources'],report['audited_statements'],report['capabilities'],report['conflicts'],report['authored_cases']),(32,194,36,26,52))
    def mutate(self,path,change):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'repo'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__','*.pyc'))
            p=root/path;data=json.loads(p.read_text());change(data);p.write_text(json.dumps(data))
            return coverage.validate(root)['structural_errors']
    def test_missing_feature_detected(self):
        self.assertTrue(self.mutate('docs/feature-map.json',lambda d:d['features'].pop()))
    def test_duplicate_feature_detected(self):
        self.assertTrue(self.mutate('docs/feature-map.json',lambda d:d['features'].append(d['features'][0])))
    def test_drifted_source_statement_detected(self):
        self.assertTrue(self.mutate('docs/source-audit.json',lambda d:d['sources'][0]['adopted'].append('New untracked rule')))
    def test_statement_hash_change_detected(self):
        def change(d):d['sources'][0]['adopted'][0]+=' changed'
        self.assertTrue(self.mutate('docs/source-audit.json',change))
    def test_exclusion_cannot_be_claimed_as_adoption(self):
        def change(d):next(f for f in d['features'] if f['disposition']=='adapted_or_excluded')['disposition']='adopted'
        self.assertTrue(self.mutate('docs/feature-map.json',change))
    def test_unknown_capability_detected(self):
        def change(d):d['features'][0]['capabilities']=['CW99']
        self.assertTrue(self.mutate('docs/feature-map.json',change))
    def test_missing_anchor_detected(self):
        def change(d):d['capabilities'][0]['anchor']='does-not-exist'
        self.assertTrue(self.mutate('skills/clearweave/assets/capabilities.json',change))
    def test_missing_chinese_conflict_case_detected(self):
        def change(d):d['cases']=[c for c in d['cases'] if c['id']!='CF01-ZH']
        self.assertTrue(self.mutate('evals/conflict-cases.json',change))
    def test_one_way_conflict_link_detected(self):
        def change(d):d['capabilities'][0]['cases']=[]
        self.assertTrue(self.mutate('skills/clearweave/assets/capabilities.json',change))
    def test_unconstrained_bad_example_detected(self):
        def change(d):d['cases'][0]['unsafe_example']=d['cases'][0]['faithful_example']
        self.assertTrue(self.mutate('evals/conflict-cases.json',change))
    def test_unknown_check_type_not_silently_accepted(self):
        with self.assertRaises(ValueError):coverage.check_example('x',[{'type':'bogus','value':'x'}])

class AuthoredConflictFixtures(unittest.TestCase):pass
for row in json.loads((ROOT/'evals/conflict-cases.json').read_text())['cases']:
    def test(self,case=row):
        self.assertEqual(coverage.check_example(case['faithful_example'],case['checks']),[])
        self.assertTrue(coverage.check_example(case['unsafe_example'],case['checks']))
    setattr(AuthoredConflictFixtures,'test_'+row['id'].replace('-','_'),test)

class SourceDecisionLinks(unittest.TestCase):pass
AUDIT=json.loads((ROOT/'docs/source-audit.json').read_text())['sources']
FEATURES=json.loads((ROOT/'docs/feature-map.json').read_text())['features']
for source in AUDIT:
    def test(self,src=source):
        linked=[f for f in FEATURES if f['source']==src['id']]
        self.assertEqual(len(linked),len(src['adopted'])+len(src['rejected_or_modified']))
        self.assertTrue(all(f['capabilities'] for f in linked))
    setattr(SourceDecisionLinks,'test_'+source['id'],test)

if __name__=='__main__':unittest.main()
