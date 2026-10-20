"""Real-data record and hash regression; no simulated model generation."""
from copy import deepcopy
import importlib.util,json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cw_scholarly_eval',ROOT/'tools/evaluate_scholarly.py');ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
D=ROOT/'evals/scholarly-2026-10-20'
class PublicDataTests(unittest.TestCase):
 def setUp(self):
  self.s=json.loads((D/'samples.json').read_text())['samples'];self.o=json.loads((D/'outputs.json').read_text());self.p=json.loads((D/'protocol.json').read_text())
 def test_recorded_replay(self):
  r=ev.evaluate(self.s,self.o,self.p);self.assertEqual(r['actions'],{'edit':6,'keep':2});self.assertEqual(r['profile_samples'],3)
 def test_corrupt_input_fails(self):
  self.s[0]['text']+='x'
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_corrupt_output_fails(self):
  self.o[0]['revision']+='x'
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_overlap_rejected(self):
  self.s[3]['work_id']=self.s[0]['work_id']
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_duplicate_ids_rejected(self):
  self.s.append(self.s[0])
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_missing_output_rejected(self):
  self.o.pop()
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_snapshot_drift_rejected(self):
  self.p['runtime_files'][next(iter(self.p['runtime_files']))]='0'*64
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_runtime_path_escape_rejected(self):
  self.p['runtime_files']={'../other':'0'*64}
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_sbert_corrections_and_numbers(self):
  o=next(x for x in self.o if x['id']=='D19-1410')['revision'];self.assertIn('that uses',o)
  for token in ('have set','10,000','50 million','~65 hours','about 5 seconds'):self.assertIn(token,o)
 def test_real_negative_result_preserved(self):
  o=next(x for x in self.o if x['id']=='W19-5028')['revision'];self.assertIn('do not yield performance gains',o);self.assertNotIn('Unfortunately',o)
 def test_real_hedge_retained(self):
  o=next(x for x in self.o if x['id']=='W19-4703')['revision'];self.assertIn('may be continuing',o);self.assertIn('likely',o)
 def test_recovered_squad_control(self):
  r=next(x for x in self.s if x['id']=='D16-1264');o=next(x for x in self.o if x['id']==r['id'])
  self.assertEqual(o['action'],'keep');self.assertEqual(o['revision'],ev.reviewed_pdf_text(r))
  for token in ('100,000+','51.0%','20%','86.8%','However'):self.assertIn(token,o['revision'])
 def test_corrupt_pdf_provenance_rejected(self):
  r=next(x for x in self.s if x['id']=='D16-1264');r['abstract_source']['url']='https://example.com/other.pdf'
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_historical_runtime_is_exact(self):
  import hashlib
  m=json.loads((ROOT/'evals/hc3-2026-10-20/manifest.json').read_text())
  for name,sha in m['skill_hashes'].items():
   self.assertEqual(hashlib.sha256((ROOT/'evals/hc3-2026-10-20/runtime-v0.2.0'/name).read_bytes()).hexdigest(),sha)
 def test_control_untouched(self):
  o=next(x for x in self.o if x['id']=='W19-5034');self.assertEqual(o['input_sha256'],o['revision_sha256'])
if __name__=='__main__':unittest.main()
