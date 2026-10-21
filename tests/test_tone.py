"""Executable mechanics and counterexample tests for Chinese precision cleanup."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/clearweave/scripts'))
import clearweave_tone as tone

class ToneTests(unittest.TestCase):
 def ids(self,text,**kwargs):return {x['rule'] for x in tone.scan(text,**kwargs)['candidates']}
 def ledger(self,text,source,replacement,rule):
  i=text.index(source);return [dict(start=i,end=i+len(source),source=source,replacement=replacement,rule=rule,reason='Reviewed local candidate')]
 def test_exact_rule_inventory(self):self.assertEqual(list(tone.rules()),[f'LF{i:02}' for i in range(1,12)])
 def test_five_translation_subtypes(self):self.assertEqual([p['subtype'] for p in tone.rules()['LF10']['patterns']],list('abcde'))
 def test_wrapped_paragraphs(self):self.assertEqual(tone.scan('段落内容写在这里，\n并在下一行继续。\n\n另外一个段落。')['counts']['paragraphs'],2)
 def test_first_paragraph_no_reference_requirement(self):self.assertNotIn('LF11',self.ids('听起来很合理，但还需要检查。'))
 def test_reference_anywhere_first_sentence(self):self.assertNotIn('LF11',self.ids('这是上一段。\n\n值得注意的是，这个结论还有条件。'))
 def test_second_sentence_reference_does_not_mask_first(self):self.assertIn('LF11',self.ids('这是上一段。\n\n听起来很合理。这个结论有条件。'))
 def test_fenced_code_not_scanned(self):self.assertEqual(tone.scan('```text\n说白了，值得注意的是：测试。\n```')['candidate_count'],0)
 def test_tilde_fence_not_scanned(self):self.assertEqual(tone.scan('~~~text\n说白了，这意味着测试。\n~~~')['candidate_count'],0)
 def test_unclosed_fence_not_scanned(self):self.assertEqual(tone.scan('```\n说白了，测试。')['candidate_count'],0)
 def test_quotes_and_inline_code_not_scanned(self):self.assertEqual(tone.scan('“说白了，核心是：测试。” `说穿了，测试。`')['candidate_count'],0)
 def test_blockquote_not_scanned(self):self.assertEqual(tone.scan('> 说白了，测试。\n> 核心是：测试。')['candidate_count'],0)
 def test_math_not_scanned(self):self.assertEqual(tone.scan('\\[说白了，测试\\]')['candidate_count'],0)
 def test_table_not_scanned(self):self.assertEqual(tone.scan('| 内容 |\n| --- |\n| 核心是：测试 |')['candidate_count'],0)
 def test_list_and_lazy_continuation_not_scanned(self):self.assertEqual(tone.scan('- 说白了，测试。\n核心是：继续。')['candidate_count'],0)
 def test_prose_after_blank_list_boundary(self):self.assertIn('LF09',self.ids('- 测试。\n\n说白了，预算不足。'))
 def test_frontmatter_not_scanned(self):self.assertEqual(tone.scan('---\ntitle: 说白了，测试\n---')['candidate_count'],0)
 def test_non_chinese_unchanged(self):self.assertEqual(tone.scan('However, this is not proof.\n\nWhen x > 0, stop.')['candidate_count'],0)
 def test_sentence_ordinals_not_heading_rule(self):self.assertNotIn('LF06',self.ids('首先，采集数据。其次，分析数据。最后，报告结果。'))
 def test_two_numbered_headings_not_flagged(self):self.assertNotIn('LF06',self.ids('## 一、背景\n\n## 二、方法'))
 def test_bold_heading_run(self):self.assertIn('LF06',self.ids('**一、背景**\n\n**二、方法**\n\n**三、结果**'))
 def test_heading_reference_preserved(self):self.assertNotIn('LF06',self.ids('## 一、背景\n\n## 二、方法\n\n## 三、结果\n\n详见第三节。'))
 def test_procedure_heading_numbers_preserved(self):self.assertNotIn('LF06',self.ids('## 一、开始\n\n## 二、执行\n\n## 三、退出',genre='procedure'))
 def test_style_dash_exception(self):self.assertNotIn('LF04',self.ids('结果清楚——样本不足。',keep_rules=['LF04']))
 def test_unknown_keep_rule_fails(self):
  with self.assertRaises(ValueError):tone.scan('文本',keep_rules=['LF99'])
 def test_literary_parallel_and_dash_kept(self):self.assertNotIn('LF04',self.ids('眼前是一片海——广阔的海。',genre='literary'))
 def test_nominalization_not_standalone_trigger(self):self.assertEqual(tone.scan('团队完成了对系统的优化。')['candidate_count'],0)
 def test_passive_not_trigger(self):self.assertEqual(tone.scan('这被认为是一种有效方法。')['candidate_count'],0)
 def test_question_not_trigger(self):self.assertEqual(tone.scan('## 怎样处理数据？\n\n数据能回答什么问题？')['candidate_count'],0)
 def test_metaphor_not_generic_trigger(self):self.assertNotIn('LF07',self.ids('记忆像一条河。'))
 def test_no_data_no_lf08(self):self.assertNotIn('LF08',self.ids('新系统效率显著提升。'))
 def test_real_data_lf08(self):self.assertIn('LF08',self.ids('新系统效率显著提升。处理时间为40分钟。'))
 def test_counts_have_correct_denominators(self):
  r=tone.measure(['段落写在这里。\n\n听起来很合理。'])['rules']
  self.assertEqual(r['LF11']['denominator'],'nonfirst_paragraphs');self.assertEqual(r['LF11']['rate'],100)
  self.assertEqual(r['LF03']['denominator'],'paragraphs');self.assertEqual(r['LF06']['denominator'],'headings')
 def test_nonfirst_reset_per_document(self):self.assertEqual(tone.measure(['听起来很合理。','听起来很合理。'])['rules']['LF11']['hits'],0)
 def test_zero_denominator_json_null(self):
  r=tone.compare_corpora(['正常的文本。'],['说白了，文本。']);self.assertIsNone(r['comparison']['LF09']['b_over_a']);json.dumps(r,allow_nan=False)
 def test_ratio_direction_and_symmetry(self):
  a=['说白了，预算不足。'];b=['说白了，预算不足。说穿了，资金短缺。'];r=tone.compare_corpora(a,b)
  x=r['a']['rules']['LF09']['rate'];y=r['b']['rules']['LF09']['rate'];self.assertEqual(r['comparison']['LF09']['b_over_a'],y/x)
 def test_empty_corpus_fails(self):
  with self.assertRaises(ValueError):tone.measure([])
 def test_single_line_offsets(self):
  s='背景。\n\n说白了，预算不足。';c=next(c for c in tone.scan(s)['candidates'] if c['rule']=='LF09');self.assertEqual(s[c['start']:c['end']],c['excerpt']);self.assertEqual(c['line'],3)
 def test_valid_minimal_ledger(self):
  s='说白了，预算不足。';r=tone.verify_edits(s,'预算不足。',self.ledger(s,'说白了，','','LF09'));self.assertEqual(r['mechanical_checks'],'passed')
 def test_noop_ledger(self):self.assertEqual(tone.verify_edits('正常文本。','正常文本。',[])['edit_count'],0)
 def test_unlisted_edit_fails(self):
  s='说白了，预算不足。'
  with self.assertRaises(ValueError):tone.verify_edits(s,'预算充足。',self.ledger(s,'说白了，','','LF09'))
 def test_number_change_fails(self):
  s='核心是：样本为20个。'
  with self.assertRaises(ValueError):tone.verify_edits(s,'样本为30个。',self.ledger(s,s,'样本为30个。','LF05'))
 def test_rule_unknown_fails(self):
  s='说白了，预算不足。'
  with self.assertRaises(ValueError):tone.verify_edits(s,'预算不足。',self.ledger(s,'说白了，','','LF99'))
 def test_arbitrary_rule_label_fails(self):
  s='没有候选的正文。'
  with self.assertRaises(ValueError):tone.verify_edits(s,'正文。',self.ledger(s,'没有候选的','','LF09'))
 def test_false_source_fails(self):
  s='说白了，预算不足。';e=self.ledger(s,'说白了，','','LF09');e[0]['source']='不匹配'
  with self.assertRaises(ValueError):tone.verify_edits(s,'预算不足。',e)
 def test_overlap_fails(self):
  s='说白了，预算不足。';e=self.ledger(s,'说白了，','','LF09')
  with self.assertRaises(ValueError):tone.verify_edits(s,'预算不足。',e+e)
 def test_invalid_bool_range_fails(self):
  s='说白了，预算不足。';e=self.ledger(s,'说白了，','','LF09');e[0]['start']=False
  with self.assertRaises(ValueError):tone.verify_edits(s,'预算不足。',e)
 def test_newline_change_fails(self):
  s='说白了，预算不足。'
  with self.assertRaises(ValueError):tone.verify_edits(s,'\n预算不足。',self.ledger(s,'说白了，','\n','LF09'))
 def test_heading_ordinal_only(self):
  s='## 一、背景\n\n## 二、方法\n\n## 三、结果';e=self.ledger(s,'一、','','LF06');after=s.replace('一、','',1);self.assertEqual(tone.verify_edits(s,after,e)['edit_count'],1)
 def test_heading_rewording_fails(self):
  s='## 一、背景\n\n## 二、方法\n\n## 三、结果'
  with self.assertRaises(ValueError):tone.verify_edits(s,s.replace('一、背景','绪论'),self.ledger(s,'一、背景','绪论','LF06'))
 def test_insert_referent(self):
  s='上段有一个对象。\n\n听起来很合理。';i=s.index('听起来');e=[dict(start=i,end=i,source='',replacement='这',rule='LF11',reason='Unique antecedent')];self.assertEqual(tone.verify_edits(s,s[:i]+'这'+s[i:],e)['edit_count'],1)
 def test_cli_read_only_and_error(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'draft.md';p.write_text('说白了，测试。');before=p.read_bytes();exe=[sys.executable,str(ROOT/'skills/clearweave/scripts/clearweave_tone.py')]
   good=subprocess.run(exe+['scan',str(p)],capture_output=True,text=True);self.assertEqual(good.returncode,0);self.assertEqual(json.loads(good.stdout)['candidate_count'],1);self.assertEqual(p.read_bytes(),before)
   bad=subprocess.run(exe+['scan',str(p)+'-missing'],capture_output=True,text=True);self.assertEqual(bad.returncode,2)
 def test_cli_compare_empty_fails(self):
  with tempfile.TemporaryDirectory() as d:
   result=subprocess.run([sys.executable,str(ROOT/'skills/clearweave/scripts/clearweave_tone.py'),'compare-corpora','--a',d,'--b',d],capture_output=True);self.assertEqual(result.returncode,2)
 def test_routing_and_docs(self):
  for name in ['README.md','README.zh-CN.md','skills/clearweave/SKILL.md']:
   text=(ROOT/name).read_text();self.assertIn('lieflat',text.lower());self.assertIn('LF01',text)
  self.assertIn('54',(ROOT/'README.zh-CN.md').read_text())

class ToneContractTests(unittest.TestCase):
 def test_translation_subtypes_located(self):
  cases={'a':'这是一套能够满足多个团队在不同地区开展工作时共同协作需求的方法。','b':'当温度超过80°C时，系统停机。','c':'对于测试团队来说，时间有限。','d':'然而，样本数量不足。','e':'这表明结论仍需验证。'}
  for expected,text in cases.items():
   with self.subTest(expected=expected):self.assertIn(expected,{c['subtype'] for c in tone.scan(text)['candidates'] if c['rule']=='LF10'})
 def test_keep_rule_applies_to_ledger(self):
  s='说白了，预算不足。';e=[dict(start=0,end=4,source=s[:4],replacement='',rule='LF09',reason='cue')]
  with self.assertRaises(ValueError):tone.verify_edits(s,s[4:],e,keep_rules=['LF09'])
 def test_procedure_applies_to_ledger(self):
  s='## 一、开始\n\n## 二、执行\n\n## 三、退出';e=[dict(start=3,end=5,source='一、',replacement='',rule='LF06',reason='ordinal')]
  with self.assertRaises(ValueError):tone.verify_edits(s,s[:3]+s[5:],e,genre='procedure')
 def test_read_preserves_crlf(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'source.md';p.write_bytes('说白了，测试。\r\n下一行。'.encode());self.assertIn('\r\n',tone.read(str(p)))
 def test_standalone_empty_list_lead_candidate(self):
  self.assertIn('LF05',{c['rule'] for c in tone.scan('具体如下：\n- 检查数据\n- 检查输出')['candidates']})
 def test_discourse_new_inference_is_only_candidate(self):
  r=tone.scan('样本下降。這不是结论。\n\n这表明原因可能另有来源。');self.assertEqual(r['judgment'],'editorial_candidates')

POSITIVES={
'LF01':'问题不是速度，而是成本。','LF02':'系统提供采集、存储、展示。',
'LF03':'甲组负责采集信息，乙组核对原始数据。丙组负责收集样本，丁组核对实验结果。',
'LF04':'答案很直接——减少等待。','LF05':'核心是：样本不足。',
'LF06':'## 一、背景\n\n## 二、方法\n\n## 三、结果',
'LF07':'系统像一位全能的导师，为用户提供说明。','LF08':'效率显著提升。处理时间为40分钟。',
'LF09':'说白了，项目预算不足。','LF10':'此外，成本也是一个因素。',
'LF11':'前段描述了一个方案。\n\n听起来很合理，但还需要检查。'}
for rid,text in POSITIVES.items():
 def test(self,r=rid,t=text):self.assertIn(r,self.ids(t))
 setattr(ToneTests,'test_candidate_'+rid,test)
if __name__=='__main__':unittest.main()
