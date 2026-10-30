"""Guardrails: incomplete evidence and new failures must not look approved."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from diagnose_api import classify, parse_karate


class ClassificationTests(unittest.TestCase):
    def setUp(self):
        self.row = dict(key='API/features/a.feature::10', file='API/features/a.feature', status='failed',
                        background_failed=False, failed_steps=[dict(step='match r.statusCode == 201',error_sha256='error1')])
        self.manifest = dict(reference_commit='sut1',source_hashes={'API/features/a.feature':'source1'})
        self.catalog = dict(reference_commit='sut1',failures=[dict(key=self.row['key'],source_sha256='source1',
                            failed_steps=copy.deepcopy(self.row['failed_steps']),defect='D-01')])

    def test_exact_failure_classified_but_not_changed_to_pass(self):
        self.assertEqual(classify(self.row,self.manifest,self.catalog),'D-01')
        self.assertEqual(self.row['status'],'failed')

    def test_different_signature_not_hidden_under_known_case(self):
        self.row['failed_steps'][0]['error_sha256']='different'
        self.assertIsNone(classify(self.row,self.manifest,self.catalog))

    def test_new_step_not_hidden(self):
        self.row['failed_steps'][0]['step']='match r.statusCode == 401'
        self.assertIsNone(classify(self.row,self.manifest,self.catalog))

    def test_changed_reference_or_test_invalidates_classification(self):
        for changed in [dict(reference_commit='sut2',source_hashes=self.manifest['source_hashes']),
                        dict(reference_commit='sut1',source_hashes={'API/features/a.feature':'source2'})]:
            self.assertIsNone(classify(self.row,changed,self.catalog))

    def test_preparation_failure_not_functional_defect(self):
        self.row['background_failed']=True
        self.assertIsNone(classify(self.row,self.manifest,self.catalog))

    def test_passed_case_is_not_expected_failure(self):
        self.row['status']='passed'
        self.assertIsNone(classify(self.row,self.manifest,self.catalog))


class EvidenceTests(unittest.TestCase):
    def fixture(self, root, failed_background=False, count=1):
        elements=[]
        if failed_background:
            elements.append(dict(type='background',steps=[dict(name='setup',result={'status':'failed'})]))
        elements.append(dict(type='scenario',line=10,name='sample',tags=[{'name':'@G4-001'}],
            steps=[dict(name='match result',result={'status':'skipped' if failed_background else 'passed'})]))
        (root/'features.a.json').write_text(json.dumps([dict(uri='API/features/a.feature',elements=elements)]))
        (root/'karate-summary-json.txt').write_text(json.dumps(dict(scenariosPassed=0 if failed_background else count,scenariosfailed=1 if failed_background else 0)))

    def test_empty_or_incomplete_report_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(ValueError):parse_karate(root)
            self.fixture(root,count=2)
            with self.assertRaises(ValueError):parse_karate(root)

    def test_background_failure_is_not_a_passed_or_skipped_test(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);self.fixture(root,failed_background=True)
            row=parse_karate(root)[0]
            self.assertEqual(row['status'],'failed')
            self.assertTrue(row['background_failed'])


if __name__=='__main__':unittest.main()
