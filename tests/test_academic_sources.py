"""Regression tests against real ACL records and collection failures."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('academic_collector', ROOT/'tools/collect_academic_sources.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)
PLAN = c.read_json(c.DATA/'plan.json')
RECORDS = c.read_json(c.DATA/'records.json')
OVERRIDES = c.read_json(c.DATA/'abstract-overrides.json')
TARGETS = {t['id']:t for t in PLAN['targets']}


class AcademicSourcesTests(unittest.TestCase):
    def test_six_real_records_replay(self):
        self.assertEqual(c.replay_records(), {'real_acl_records_checked':6, 'status':'passed'})

    def test_original_missing_abstract_reproduced(self):
        raw = next(r['xml'] for r in RECORDS if r['id']=='D16-1264')
        self.assertIsNone(ET.fromstring(raw).find('./volume/paper/abstract'))
        with self.assertRaisesRegex(ValueError, 'missing abstract'):
            c.extract_record(raw.encode(), TARGETS['D16-1264'], {})

    def test_same_paper_excerpt_recovers_original_numbers(self):
        raw = next(r['xml'] for r in RECORDS if r['id']=='D16-1264').encode()
        record = c.extract_record(raw, TARGETS['D16-1264'], OVERRIDES)
        self.assertEqual(record['abstract_source']['kind'], 'reviewed-pdf-excerpt')
        for number in ('100,000+', '51.0%', '20%', '86.8%'):
            self.assertIn(number, record['text'])

    def test_existing_xml_abstract_has_precedence(self):
        row = RECORDS[0]; overrides = {row['id']: {'title':'Wrong paper'}}
        record = c.extract_record(row['xml'].encode(), TARGETS[row['id']], overrides)
        self.assertEqual(record['abstract_source']['kind'], 'acl-xml')

    def test_mismatched_fallback_identity_rejected(self):
        row = RECORDS[-1]; fallback = copy.deepcopy(OVERRIDES)
        fallback['D16-1264']['title'] = 'Different paper'
        with self.assertRaisesRegex(ValueError, 'different paper'):
            c.extract_record(row['xml'].encode(), TARGETS[row['id']], fallback)

    def test_fallback_corruption_rejected(self):
        row = RECORDS[-1]; fallback = copy.deepcopy(OVERRIDES)
        fallback['D16-1264']['text'] += ' Invented detail.'
        with self.assertRaisesRegex(ValueError, 'checksum'):
            c.extract_record(row['xml'].encode(), TARGETS[row['id']], fallback)

    def test_fallback_wrong_url_rejected(self):
        row = RECORDS[-1]; fallback = copy.deepcopy(OVERRIDES)
        fallback['D16-1264']['url'] = 'https://aclanthology.org/N19-1423.pdf'
        with self.assertRaisesRegex(ValueError, 'provenance'):
            c.extract_record(row['xml'].encode(), TARGETS[row['id']], fallback)

    def test_missing_or_duplicate_paper_is_error(self):
        row = RECORDS[0]; target = TARGETS[row['id']]
        for raw in (b'<collection/>', row['xml'].replace('</volume>', row['xml'].split('<volume id="1">')[1].split('</volume>')[0]+'</volume>').encode()):
            with self.subTest(raw_length=len(raw)):
                with self.assertRaisesRegex(ValueError, 'expected one paper'):
                    c.extract_record(raw, target, OVERRIDES)

    def test_changed_bibliographic_identity_is_error(self):
        row = RECORDS[0]; target = copy.deepcopy(TARGETS[row['id']]);target['authors']=['Other person']
        with self.assertRaisesRegex(ValueError, 'bibliographic'):
            c.extract_record(row['xml'].encode(), target, OVERRIDES)

    def test_correct_old_and_new_identifier_padding(self):
        self.assertEqual(c.paper_identifier('D16','1','3'),'D16-1003')
        self.assertEqual(c.paper_identifier('W19','50','34'),'W19-5034')
        self.assertEqual(c.paper_identifier('2020.acl','demos','14'),'2020.acl-demos.14')

    def test_duplicate_plan_id_is_error(self):
        plan=copy.deepcopy(PLAN);plan['targets'].append(plan['targets'][0])
        with self.assertRaisesRegex(ValueError,'Duplicate IDs'):
            c.validate_plan(plan)

    def test_pinned_revision_and_paths_required(self):
        with self.assertRaisesRegex(ValueError,'pinned'):
            c.source_url('acl-org/acl-anthology','main','data/xml/D16.xml')
        for name in ('../outside','/tmp/out','x/../z','a\\b'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                c.relative(name)

    def test_symlink_cannot_escape_output(self):
        with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as other:
            root=Path(d);(root/'link').symlink_to(other,target_is_directory=True)
            with self.assertRaisesRegex(ValueError,'escapes'):
                c.contained(root,'link/out')

    def test_incomplete_collection_is_not_success(self):
        def broken(url,local): raise FileNotFoundError(local)
        with tempfile.TemporaryDirectory() as d:
            result=c.collect(PLAN,OVERRIDES,broken,Path(d))
            self.assertEqual(result['status'],'incomplete')
            self.assertEqual(result['completed_samples'],0)
            self.assertTrue(result['errors'])
            self.assertEqual(c.read_json(Path(d)/'collection-report.json'), result)

    def test_corrupt_source_bytes_are_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            result=c.collect(PLAN,OVERRIDES,lambda *_:b'wrong',Path(d))
            self.assertEqual(result['status'],'incomplete')
            self.assertEqual(result['verified_source_files'],0)

    def test_cli_failure_returns_nonzero_and_saves_report(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'out'
            with patch('sys.stdout',new=io.StringIO()):
                status=c.main(['--cache',d,'--out',str(out)])
            self.assertEqual(status,1)
            self.assertEqual(c.read_json(out/'collection-report.json')['status'],'incomplete')

    def test_cli_fixture_mode(self):
        with patch('sys.stdout',new=io.StringIO()):
            self.assertEqual(c.main(['--replay-fixtures']),0)

    def test_retry_transient_http_error(self):
        url='https://raw.githubusercontent.com/example/repo/'+'a'*40+'/SKILL.md'
        response=io.BytesIO(b'content');response.url=url
        error=urllib.error.HTTPError(url,503,'busy',{},None)
        with patch.object(c.urllib.request,'urlopen',side_effect=[error,response]) as opened, patch.object(c.time,'sleep'):
            self.assertEqual(c.download(url),b'content')
            self.assertEqual(opened.call_count,2)

    def test_http_404_not_retried(self):
        url='https://raw.githubusercontent.com/example/repo/'+'a'*40+'/missing'
        error=urllib.error.HTTPError(url,404,'missing',{},None)
        with patch.object(c.urllib.request,'urlopen',side_effect=error) as opened:
            with self.assertRaises(urllib.error.HTTPError):c.download(url)
            self.assertEqual(opened.call_count,1)

    def test_network_retry_is_bounded(self):
        url='https://raw.githubusercontent.com/example/repo/'+'a'*40+'/SKILL.md'
        with patch.object(c.urllib.request,'urlopen',side_effect=urllib.error.URLError('offline')) as opened, patch.object(c.time,'sleep'):
            with self.assertRaises(urllib.error.URLError):c.download(url)
            self.assertEqual(opened.call_count,3)

    def test_unexpected_host_rejected(self):
        with self.assertRaises(ValueError):c.download('https://other.example/file')


if __name__=='__main__':unittest.main()
