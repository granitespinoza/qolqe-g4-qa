"""Contrato de sincronización: reintentos, historial y estados crudos en Kiwi."""
from pathlib import Path
import json,sys,unittest
from unittest.mock import MagicMock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from kiwi_sync import sync
class KiwiSyncTests(unittest.TestCase):
 def setUp(self):
  self.case={'id':'E2E-G4-102','version':'abc','title':'Alta','hu':['HU-G4-01'],'file':'Web/features/contactos.feature'}
  self.item={'case':self.case,'state':'FAILED','variants':[{'state':'failed','classification':'known_issue','defect':'D-01'}]}
  self.run={'key':'web:run1','fingerprint':'abc','revision':'commit','url':None,'cases':[self.item]}
  self.rpc=MagicMock();self.rpc.TestCaseStatus.filter.return_value=[{'id':2}]
  self.rpc.TestExecutionStatus.filter.return_value=[{'id':1,'name':'IDLE'},{'id':2,'name':'PASSED'},{'id':3,'name':'FAILED'},{'id':4,'name':'BLOCKED'}]
  self.rpc.TestCase.filter.return_value=[{'id':10}];self.rpc.TestRun.filter.return_value=[];self.rpc.TestRun.create.return_value={'id':20}
  self.rpc.TestRun.add_case.return_value=[{'id':30,'status':1}];self.rpc.TestExecution.get_comments.return_value=[];self.rpc.TestExecution.filter.return_value=[{'case':10,'status':3}]
 def execute(self):return sync({'runs':[self.run]},self.rpc,1,2,3,4,5)
 def test_known_failure_is_written_as_failed(self):
  result=self.execute();self.rpc.TestExecution.update.assert_called_once_with(30,{'status':3});self.assertEqual(result[0]['status'],'created')
 def test_interrupted_import_is_resumed(self):
  self.rpc.TestRun.filter.return_value=[{'id':20}];result=self.execute();self.rpc.TestRun.create.assert_not_called();self.assertEqual(result[0]['status'],'resumed')
 def test_reimport_complete_result_does_not_rewrite_it(self):
  self.rpc.TestRun.filter.return_value=[{'id':20}];self.rpc.TestRun.add_case.return_value=[{'id':30,'status':3}]
  comment=json.dumps({'run':self.run['key'],'commit':'commit','pipeline':None,'variants':self.item['variants']},ensure_ascii=False)
  self.rpc.TestExecution.get_comments.return_value=[{'comment':comment}]
  result=self.execute();self.rpc.TestExecution.update.assert_not_called();self.rpc.TestExecution.add_comment.assert_not_called();self.assertEqual(result[0]['status'],'already_exists_not_modified')
 def test_readback_detects_a_result_not_persisted(self):
  self.rpc.TestExecution.filter.return_value=[{'case':10,'status':2}]
  with self.assertRaises(ValueError):self.execute()
 def test_different_recorded_result_is_never_overwritten(self):
  self.rpc.TestRun.filter.return_value=[{'id':20}];self.rpc.TestRun.add_case.return_value=[{'id':30,'status':2}]
  with self.assertRaises(ValueError):self.execute()
  self.rpc.TestExecution.update.assert_not_called()
if __name__=='__main__':unittest.main()
