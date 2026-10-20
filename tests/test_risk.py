"""Limited cue detector regression; explicitly exercise both usefulness and blind spots."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'skills/clearweave/scripts'
sys.path.insert(0,str(SCRIPTS))
import clearweave_risk as risk
import clearweave_check as literal

def ids(a,b): return {f['risk_id'] for f in risk.assess(a,b)['findings']}

class RiskTests(unittest.TestCase):
    def test_english_negation(self):
        self.assertIn('R01',ids('The model does not support retries.','The model supports retries.'))
    def test_chinese_negation(self):
        self.assertIn('R01',ids('系统不支持重试。','系统支持重试。'))
    def test_traditional_negation(self):
        self.assertIn('R01',ids('系統沒有部署。','系統已部署。'))
    def test_uncertainty(self):
        self.assertIn('R02',ids('It may reduce delay.','It reduces delay.'))
    def test_modal_strength_same_count(self):
        self.assertIn('R03',ids('You must restart.','You should restart.'))
    def test_causal_strength(self):
        self.assertIn('R04',ids('A was associated with B.','A caused B.'))
    def test_work_status(self):
        self.assertIn('R05',ids('试点仍在计划中。','试点已完成。'))
    def test_scope(self):
        self.assertIn('R06',ids('Only offline requests were tested.','Requests were tested.'))
    def test_attribution(self):
        self.assertIn('R07',ids('According to the report, it works.','It works.'))
    def test_numeric_role_swap_now_has_additional_candidate(self):
        a='A scored 0.8; B scored 0.6.';b='A scored 0.6; B scored 0.8.'
        self.assertFalse(literal.compare_texts(a,b)['supported_literal_changes'])
        self.assertIn('R08',ids(a,b))
    def test_legitimate_sentence_reordering_is_also_candidate_not_verdict(self):
        report=risk.assess('A scored 0.8. B scored 0.6.','B scored 0.6. A scored 0.8.')
        self.assertIn('R08',{f['risk_id'] for f in report['findings']})
        self.assertEqual(report['verdict'],'not_provided')
    def test_same_numeric_order_can_still_hide_changed_roles(self):
        report=risk.assess('A scored 0.8; B scored 0.6.','B scored 0.8; A scored 0.6.')
        self.assertEqual(report['candidate_count'],0)
        self.assertTrue(report['semantic_review_required'])
    def test_same_negation_inventory_can_hide_scope_swap(self):
        report=risk.assess('A works; B does not.','A does not; B works.')
        self.assertEqual(report['candidate_count'],0)
        self.assertTrue(report['semantic_review_required'])
    def test_protected_spans_use_separate_literal_check(self):
        a='"may not work"';b='"will work"'
        self.assertFalse(ids(a,b))
        self.assertTrue(literal.compare_texts(a,b)['supported_literal_changes'])
    def test_code_not_scanned(self):
        self.assertFalse(ids('`not ready`','`ready`'))
    def test_month_date_not_modality(self):
        self.assertNotIn('R02',ids('Start on May 12.','Start on June 12.'))
    def test_not_only_not_propositional_negation(self):
        self.assertNotIn('R01',ids('Not only A but also B.','A and B.'))
    def test_faithful_paraphrase_can_raise_candidate(self):
        self.assertIn('R02',ids('The method may help.','The method might help.'))
    def test_unchanged_has_no_verdict(self):
        r=risk.assess('Only A may work.','Only A may work.')
        self.assertEqual(r['candidate_count'],0);self.assertEqual(r['verdict'],'not_provided')
    def test_cli_statuses_and_no_source_writes(self):
        with tempfile.TemporaryDirectory() as d:
            a=Path(d)/'a';b=Path(d)/'b';a.write_text('It may work.');b.write_text('It works.')
            cmd=[sys.executable,str(SCRIPTS/'clearweave_risk.py'),str(a),str(b),'--format','json']
            out=subprocess.run(cmd,capture_output=True,text=True)
            self.assertEqual(out.returncode,0);self.assertGreater(json.loads(out.stdout)['candidate_count'],0)
            self.assertEqual(subprocess.run(cmd+['--fail-on-candidate'],capture_output=True).returncode,1)
            self.assertEqual(a.read_text(),'It may work.');self.assertEqual(b.read_text(),'It works.')
    def test_two_stdin_rejected(self):
        p=subprocess.run([sys.executable,str(SCRIPTS/'clearweave_risk.py'),'-','-'],capture_output=True)
        self.assertEqual(p.returncode,2)
    def test_invalid_utf8(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad';p.write_bytes(b'\xff')
            result=subprocess.run([sys.executable,str(SCRIPTS/'clearweave_risk.py'),str(p),str(p)],capture_output=True)
            self.assertEqual(result.returncode,2)
    def test_traditional_lint_candidates(self):
        text='在當今快速發展的社會，這具有深遠意義。綜上所述，讓我們共同見證。'
        found={d['rule_id'] for d in literal.lint_text(text)['diagnostics']}
        self.assertTrue({'ZH001','ZH003','ZH005','ZH007'}<=found)
    def test_traditional_quote_still_protected(self):
        self.assertEqual(literal.lint_text('「綜上所述，未來可期。」')['candidate_count'],0)

if __name__=='__main__':unittest.main()
