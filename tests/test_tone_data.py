"""Replay actual public-text records and reject corrupted evaluation evidence."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('cw_tone_eval',ROOT/'tools/evaluate_lieflat.py');ev=importlib.util.module_from_spec(spec);spec.loader.exec_module(ev)
D=ROOT/'evals/lieflat-2026-10-21'
class TonePublicTextTests(unittest.TestCase):
 def setUp(self):self.s=json.loads((D/'samples.json').read_text())['samples'];self.o=json.loads((D/'outputs.json').read_text());self.p=json.loads((D/'protocol.json').read_text())
 def test_recorded_replay(self):self.assertEqual(ev.evaluate(self.s,self.o,self.p)['summary']['edited'],1)
 def test_all_other_text_exact(self):
  o=next(x for x in self.o if x['action']=='edit');s=next(x for x in self.s if x['id']==o['id']);self.assertEqual(o['revision'],s['text'].replace('此外，','',1));self.assertEqual(len(o['edits']),1)
 def test_preserve_contrast_and_inference(self):
  o=next(x for x in self.o if x['action']=='edit')['revision'];self.assertIn('然而',o);self.assertIn('因此',o);self.assertIn('并不一定',o)
 def test_invented_extra_edit_fails(self):
  o=self.o[1];o['revision']=o['revision'].replace('可能','肯定',1);o['revision_sha256']=ev.digest(o['revision'])
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_source_corruption_fails(self):
  self.s[0]['text']+='x'
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_missing_output_fails(self):
  self.o.pop()
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_runtime_drift_fails(self):
  self.p['runtime_files']['skills/clearweave/SKILL.md']='0'*64
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_runtime_path_escape_fails(self):
  self.p['runtime_files']={'../outside':'0'*64}
  with self.assertRaises(ValueError):ev.evaluate(self.s,self.o,self.p)
 def test_historical_snapshot_still_exact(self):
  import hashlib
  protocol=json.loads((ROOT/'evals/scholarly-2026-10-20/protocol.json').read_text())
  for name,sha in protocol['runtime_files'].items():self.assertEqual(hashlib.sha256((ROOT/'evals/scholarly-2026-10-20/runtime-v0.3.0'/name).read_bytes()).hexdigest(),sha)
if __name__=='__main__':unittest.main()
