"""Reproduce helper outputs on author-applied examples, not semantic quality scores."""
from pathlib import Path
import json
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/clearweave/scripts'))
import clearweave_check as checker
import clearweave_risk as risk

class ApplicationRecordTests(unittest.TestCase):
    def setUp(self):
        self.record=json.loads((ROOT/'evals/v0.2.0/applications.json').read_text(encoding='utf-8'))
    def test_complete_declared_examples_and_capabilities(self):
        rows=self.record['cases']; self.assertEqual(len(rows),12)
        self.assertEqual(len({r['id'] for r in rows}),12)
        ids={c['id'] for c in json.loads((ROOT/'skills/clearweave/assets/capabilities.json').read_text())['capabilities']}
        for row in rows:
            self.assertTrue(set(row['capabilities'])<=ids)
            self.assertTrue(row['request'] and row['original'] and row['revision'])
        self.assertIn('not an independent',self.record['method'])
    def test_literal_reports_reproduce(self):
        for row in self.record['cases']:
            with self.subTest(row['id']):
                self.assertEqual(checker.compare_texts(row['original'],row['revision']),row['literal_check'])
    def test_risk_reports_reproduce(self):
        for row in self.record['cases']:
            with self.subTest(row['id']):
                self.assertEqual(risk.assess(row['original'],row['revision']),row['risk_check'])
