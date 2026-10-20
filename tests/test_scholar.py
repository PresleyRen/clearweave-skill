"""Deterministic helper contracts; semantic judgments stay in the application report."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/clearweave/scripts'))
import clearweave_scholar as s
SCRIPT=ROOT/'skills/clearweave/scripts/clearweave_scholar.py'
def cli(*args,text=None):
 return subprocess.run([sys.executable,str(SCRIPT),*args],input=text,text=True,capture_output=True)
def sample(i,text='We present a model. It maps inputs to outputs.',**kw):
 return dict(id=i,text=text,**kw)
class ScanTests(unittest.TestCase):
 def test_compound_subject_with_citations(self):
  text='BERT (Devlin et al., 2018) and RoBERTa (Liu et al., 2019) has improved accuracy.'
  self.assertEqual(s.scan(text)['counts'],{'GR01':1})
 def test_relative_head(self):self.assertEqual(s.scan('a network that use embeddings')['counts'],{'GR02':1})
 def test_correct_grammar_no_hits(self):self.assertFalse(s.scan('A model that uses context and a method that produces vectors have been evaluated.')['findings'])
 def test_articles_and_plural(self):self.assertEqual(s.scan('an model; a evidence; these criterion; this criteria')['counts'],{'GR03':3,'GR04':1})
 def test_article_pattern_word_boundary(self):self.assertFalse(s.scan('an modelled; a evidenced; these methods')['findings'])
 def test_locations(self):
  text='正文\n可能也许有用。\nIt should be noted that x may possibly improve.'
  for r in s.scan(text)['findings']:
   self.assertEqual(text[r['start']:r['end']],r['span']);self.assertEqual(r['status'],'review_candidate')
  self.assertEqual(s.scan(text)['findings'][0]['line'],2)
 def test_simple_and_traditional(self):self.assertEqual(s.scan('遗憾的是，可能也许；遺憾的是，可能也許。')['counts'],{'AD05':2,'AD06':2})
 def test_language_filter(self):self.assertEqual(s.scan('可能也许 may possibly','en')['counts'],{'AD01':1})
 def test_invalid_language(self):
  with self.assertRaises(ValueError):s.scan('text','fr')
 def test_necessary_conditions_not_banned(self):self.assertFalse(s.scan('Only if data are available, the model may improve. We did not evaluate deployment. 然而，仅在离线测试中有效。')['findings'])
 def test_unknown_actor_and_technical_terms(self):self.assertFalse(s.scan('Samples were shuffled. Robust estimation preserves provenance.')['findings'])
 def test_protected_content(self):
  text='"may possibly" `an model`\n> 遗憾的是\n\n```text\na network that use\n```\n$This and That has$\n<!-- clearweave:keep -->可能也许<!-- /clearweave:keep -->'
  self.assertFalse(s.scan(text)['findings'])
 def test_adjacent_prose_not_hidden(self):self.assertEqual(s.scan('"may possibly" may possibly improve')['counts'],{'AD01':1})
 def test_legitimate_unit_stays_candidate(self):
  # No unconditional replacement: this department name can be singular.
  self.assertEqual(s.scan('Research and Development is a department.')['findings'][0]['status'],'review_candidate')
 def test_no_mutation(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'input.md';p.write_text('may possibly help');before=p.read_bytes()
   self.assertEqual(cli('scan',str(p)).returncode,0);self.assertEqual(before,p.read_bytes())
 def test_empty_is_empty(self):self.assertEqual(s.scan('')['findings'],[])
class ProfileTests(unittest.TestCase):
 def test_measured_and_no_raw_text(self):
  p=s.profile({'samples':[sample('a')]});self.assertEqual(p['sample_count'],1);self.assertNotIn('text',p['samples'][0]);self.assertEqual(p['traits'],[])
 def test_human_profile_label_not_identity_score(self):
  p=s.profile({'samples':[sample('a')]},kind='author',label='supplied author');self.assertEqual(p['kind'],'author');self.assertNotIn('score',p)
 def test_dedup_text_and_work(self):
  p=s.profile({'samples':[sample('a',work_id='x'),sample('b'),sample('c',text='Different content.',work_id='x')]})
  self.assertEqual(p['sample_count'],1);self.assertEqual(len(p['skipped']),2)
 def test_eval_role_excluded(self):
  p=s.profile({'samples':[sample('a'),sample('eval',text='This output is for evaluation.',role='edit')]});self.assertEqual(p['samples'][0]['id'],'a');self.assertEqual(p['skipped'][0]['reason'],'different_role')
 def test_empty_retained_in_skip(self):
  p=s.profile({'samples':[sample('a'),sample('b',text=' ')]});self.assertEqual(p['skipped'][0]['reason'],'empty_text')
 def test_duplicate_id_error(self):
  with self.assertRaises(ValueError):s.profile({'samples':[sample('a'),sample('a')]})
 def test_mixed_language_error(self):
  with self.assertRaises(ValueError):s.profile({'samples':[sample('a'),sample('b',text='我们提出一种方法，适用于文本检索。')]})
 def test_invalid_shape(self):
  for val in ([],{}, {'samples':[]}, {'samples':[{}]}, {'samples':[sample('a',text=2)]}):
   with self.subTest(val=val),self.assertRaises(ValueError):s.profile(val)
 def test_invalid_profile_kind(self):
  with self.assertRaises(ValueError):s.profile({'samples':[sample('a')]},'famous-author')
 def test_invalid_work_id(self):
  with self.assertRaises(ValueError):s.profile({'samples':[sample('a',work_id=42)]})
 def test_comparison_no_forced_target(self):
  p=s.profile({'samples':[sample('a')]});r=s.compare_profile(p,'We use vectors.')
  self.assertIn('difference_from_sample_mean',r);self.assertNotIn('match_percentage',r)
 def test_non_finite_mean_rejected(self):
  p=s.profile({'samples':[sample('a')]});p['means']['characters']=float('nan')
  with self.assertRaises(ValueError):s.compare_profile(p,'Text.')
 def test_comparison_language_mismatch(self):
  p=s.profile({'samples':[sample('a')]})
  with self.assertRaises(ValueError):s.compare_profile(p,'我们提出一种新的算法。')
 def test_bad_comparison_schema(self):
  with self.assertRaises(ValueError):s.compare_profile({},'text')
 def test_common_abbreviation(self):self.assertEqual(s.metrics('We test models, e.g. encoders. They work.')['sentences_approx'],2)
 def test_chinese_sentences(self):self.assertEqual(s.metrics('我们采用该模型。测试仍在进行。')['sentences_approx'],2)
 def test_protection_affects_metrics(self):self.assertEqual(s.metrics('`this is code.`')['token_units'],0)
class LearnTests(unittest.TestCase):
 def test_pending_scoped(self):
  r=s.learn('We conducted an evaluation.','We evaluated the model.','English / methods')
  self.assertEqual(r['approval'],'pending');self.assertEqual(r['rules'],[]);self.assertTrue(r['changes'])
 def test_unchanged_no_proposal(self):self.assertEqual(s.learn('Clear.','Clear.','abstract')['changes'],[])
 def test_empty_inputs_rejected(self):
  for args in (('','a','b'),('a','','b'),('a','b','')):
   with self.assertRaises(ValueError):s.learn(*args)
 def test_chinese_changes_retained(self):self.assertTrue(s.learn('我们进行了分析。','我们分析了数据。','中文结果')['changes'])
class CliTests(unittest.TestCase):
 def test_scan_stdin(self):
  r=cli('scan','-',text='may possibly improve');self.assertEqual(r.returncode,0);self.assertEqual(json.loads(r.stdout)['counts'],{'AD01':1})
 def test_invalid_json(self):self.assertEqual(cli('profile','-',text='{').returncode,2)
 def test_missing_file(self):self.assertEqual(cli('scan','/no-such-clearweave-file').returncode,2)
 def test_double_stdin_learn(self):self.assertEqual(cli('learn','-','-','--scope','a',text='x').returncode,2)
 def test_double_stdin_compare(self):self.assertEqual(cli('compare-profile','-','-',text='{}').returncode,2)
 def test_profile_stdin(self):
  r=cli('profile','-','--kind','field',text=json.dumps({'samples':[sample('a')]}));self.assertEqual(r.returncode,0)
if __name__=='__main__':unittest.main()
