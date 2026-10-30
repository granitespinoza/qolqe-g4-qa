"""Pruebas del gate: proteger contra falsos verdes, causas nuevas y ausencia de evidencia."""
import copy
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from quality_gate import aggregate,match_api,match_web,combine_web_runs,contract_signature

class GateTests(unittest.TestCase):
    def setUp(self):
        self.policy={'defects':{'D-01':{'accepted_for_academic_gate':True,'scope':'isolated-academic-tests'}},'api_rules':[{'key':'a::1','defect':'D-01','failures':[{'step':'status 201','signature':'422 versus 201'}]}],
          'web_rules':{'E2E-G4-102':{'defect':'D-01','file':'Web/a.cy.ts','error':'AssertionError: expected 422 to equal 201'}}}
        self.api={'key':'a::1','status':'failed','background_failed':False,'tags':['@known_issue'],'failure_signatures':[{'step':'status 201','signature':'422 versus 201'}]}
        self.web={'title':['E2E-G4-102 @known_issue'],'spec':'Web/a.cy.ts','state':'failed','error':'AssertionError: expected 422 to equal 201\nstack'}
    def test_exact_known_failure_passes_scenario_a(self):
        result=aggregate([match_api(self.api,self.policy),match_web(self.web,self.policy)])
        self.assertTrue(result['approved']);self.assertEqual(result['scenario'],'A')
    def test_unknown_failure_blocks(self):
        self.web['error']='Selector not found';self.assertFalse(aggregate([match_web(self.web,self.policy)])['approved'])
    def test_same_case_different_actual_status_blocks(self):
        self.api['failure_signatures'][0]['signature']='401 versus 201';self.assertEqual(match_api(self.api,self.policy)['status'],'unknown_failure')
    def test_background_failure_never_tolerated(self):
        self.api['background_failed']=True;self.assertEqual(match_api(self.api,self.policy)['status'],'unknown_failure')
    def test_tag_alone_not_enough(self):
        self.web['spec']='Web/different.cy.ts';self.assertEqual(match_web(self.web,self.policy)['status'],'unknown_failure')
    def test_risk_acceptance_required(self):
        self.policy['defects']['D-01']['accepted_for_academic_gate']=False;self.assertEqual(match_web(self.web,self.policy)['status'],'unknown_failure')
    def test_empty_or_flaky_or_missing_evidence_blocks(self):
        self.assertFalse(aggregate([])['approved'])
        self.assertFalse(aggregate([{'case':'a','status':'flaky'}])['approved'])
        self.assertFalse(aggregate([{'case':'a','status':'passed'}],['missing report'])['approved'])
    def test_pending_test_not_passed(self):
        self.web['state']='pending';self.assertEqual(match_web(self.web,self.policy)['status'],'unknown_failure')
    def test_intermittence_between_pass_and_known_issue_is_flaky(self):
        p={'case':'a','status':'passed','defect':None};k={'case':'a','status':'known_issue','defect':'D-01'}
        self.assertEqual(combine_web_runs([[p],[k],[p]])[0]['status'],'flaky')
    def test_stable_known_failure_is_not_flaky(self):
        k={'case':'a','status':'known_issue','defect':'D-01'}
        self.assertTrue(aggregate(combine_web_runs([[k],[k],[k]]))['approved'])
    def test_contract_body_change_changes_signature(self):
        r={'url':'http://127.0.0.1:8000/api/contactos','operation':'POST /api/contactos','method':'POST','request_body':{'alias':'Niño'},'status':422,'response_body':{'codigo':'ALIAS_INVALIDO'},'phase':'Fuzzing'}
        sig=contract_signature(r,{'name':'check'});r['request_body']['alias']='Ana'
        self.assertNotEqual(sig,contract_signature(r,{'name':'check'}))
    def test_random_invalid_alias_does_not_change_known_priority_cause(self):
        r={'url':'http://127.0.0.1:8000/api/contactos','operation':'POST /api/contactos','method':'POST','request_body':{'alias':'Lu','celular':'912345678'},'status':409,'response_body':{'codigo':'CONTACTO_EXISTENTE'},'phase':'Coverage'}
        c={'name':'negative_data_rejection'};sig=contract_signature(r,c)
        r['request_body']['alias']='@otro-invalido';self.assertEqual(sig,contract_signature(r,c))
        r['request_body']['alias']='Ana';self.assertNotEqual(sig,contract_signature(r,c))
    def test_different_response_never_matches_known_contract_signature(self):
        r={'url':'http://127.0.0.1:8000/api/contactos','operation':'POST /api/contactos','method':'POST','request_body':{'alias':'Lu','celular':'912345678'},'status':409,'response_body':{'codigo':'CONTACTO_EXISTENTE'},'phase':'Coverage'}
        c={'name':'negative_data_rejection'};sig=contract_signature(r,c);r['status']=201
        self.assertNotEqual(sig,contract_signature(r,c))
    def test_known_tag_is_mandatory_for_api(self):
        self.api['tags']=[];self.assertEqual(match_api(self.api,self.policy)['status'],'unknown_failure')
    def test_cypress_poll_duration_is_not_a_new_cause(self):
        self.policy['web_rules']['E2E-G4-102']['error']='AssertionError: Timed out retrying after 4000ms: expected table to contain 10.00; actual empty'
        self.web['error']='AssertionError: Timed out retrying after 4050ms: expected table to contain 10.00; actual empty'
        self.assertEqual(match_web(self.web,self.policy)['status'],'known_issue')
        self.web['error']='AssertionError: Timed out retrying after 4050ms: selector not found'
        self.assertEqual(match_web(self.web,self.policy)['status'],'unknown_failure')
    def test_all_success_is_different_from_known_issue(self):
        self.assertEqual(aggregate([{'case':'a','status':'passed'}])['scenario'],'100% exitoso')

if __name__=='__main__':unittest.main()
