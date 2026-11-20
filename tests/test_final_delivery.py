"""Protege historial, estados crudos, repeticiones y ausencia de evidencia."""
from pathlib import Path
import copy,json,sys,tempfile,unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import final_delivery as final
from kiwi_sync import aggregate_case,payload

class FinalDeliveryTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.db=Path(self.tmp.name)/'history.sqlite'
  self.case={'id':'E2E-G4-401','version':'abc','title':'Login','hu':['HU-N-02'],'layer':'Web','file':'features/e2e/nucleo.feature'}
  self.test={'case_id':self.case['id'],'variant':'feature::401','state':'failed','classification':'known_issue','defect':'D-01','error':'expected 422 to equal 201'}
  self.run={'key':'web:run1','layer':'web','started':'2026-11-19T00:00:00Z','revision':'abc','source_hash':'abc','url':None,'tests':[self.test]}
 def test_history_reimport_is_idempotent(self):
  final.history([self.case],[self.run],self.db);rows=final.history([self.case],[self.run],self.db)
  self.assertEqual(len(rows),1);self.assertEqual(rows[0]['executions'],1)
 def test_history_does_not_overwrite_a_failure_with_pass(self):
  final.history([self.case],[self.run],self.db);changed=copy.deepcopy(self.run);changed['tests'][0]['state']='passed'
  with self.assertRaises(ValueError):final.history([self.case],[changed],self.db)
 def test_history_rejects_same_run_with_different_sources(self):
  final.history([self.case],[self.run],self.db);changed=copy.deepcopy(self.run);changed['source_hash']='other'
  with self.assertRaises(ValueError):final.history([self.case],[changed],self.db)
 def test_three_repetitions_remain_three_runs(self):
  runs=[]
  for n in range(3):r=copy.deepcopy(self.run);r['key']='web:run'+str(n);runs.append(r)
  rows=final.history([self.case],runs,self.db);self.assertEqual(len(rows),3)
 def test_known_issue_stays_failed_in_kiwi(self):
  self.assertEqual(aggregate_case([self.test]),'FAILED')
 def test_one_failed_variant_fails_case(self):
  passed={**self.test,'state':'passed'};self.assertEqual(aggregate_case([passed,self.test]),'FAILED')
 def test_skipped_is_not_pass(self):
  self.assertEqual(aggregate_case([{**self.test,'state':'skipped'}]),'BLOCKED')
 def test_payload_preserves_variants_and_revision(self):
  p=payload({'cases':[self.case],'runs':[self.run]})
  self.assertEqual(p['runs'][0]['cases'][0]['variants'][0]['classification'],'known_issue')
  self.assertEqual(p['runs'][0]['revision'],'abc')
 def test_windows_evidence_path_is_portable(self):
  with patch.object(final,'ROOT',Path(self.tmp.name)):
   self.assertEqual(final.repo_path('tests\\performance\\resultados\\run'),Path(self.tmp.name)/'tests/performance/resultados/run')
 def test_evidence_path_cannot_leave_repository(self):
  with patch.object(final,'ROOT',Path(self.tmp.name)):
   with self.assertRaises(ValueError):final.repo_path('../outside')
 def test_missing_evidence_blocks_without_creating_success(self):
  with patch.object(final,'ROOT',Path(self.tmp.name)),patch.object(final,'git',return_value='abc'):
   runs,gates,issues=final.collect()
  self.assertFalse(runs);self.assertFalse(gates);self.assertGreaterEqual(len(issues),6)
if __name__=='__main__':unittest.main()
