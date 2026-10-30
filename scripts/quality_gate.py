"""Escenario A: resultados crudos inmutables, excepciones exactas y veto a flakiness."""
import argparse
import hashlib
import json
import re
import subprocess
from urllib.parse import urlsplit, parse_qsl
from pathlib import Path
from diagnose_api import parse_karate, diagnose_schemathesis
from qa_provenance import validate

ROOT=Path(__file__).resolve().parents[1]

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def canonical_hash(path):return hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()

def permitted(rule, policy):
    d=policy['defects'].get(rule.get('defect'),{})
    return d.get('accepted_for_academic_gate') is True and d.get('scope')=='isolated-academic-tests'

def match_api(row, policy):
    if row['status']=='passed':return {'case':row['key'],'status':'passed','defect':None}
    for rule in policy['api_rules']:
        if (row['status']=='failed' and '@known_issue' in row.get('tags',[]) and not row['background_failed'] and row['key']==rule['key']
            and row.get('failure_signatures')==rule['failures'] and permitted(rule,policy)):
            return {'case':row['key'],'status':'known_issue','defect':rule['defect']}
    return {'case':row['key'],'status':'unknown_failure','defect':None}

def web_error_signature(error):
    # El tiempo impreso por Cypress puede variar un ciclo de sondeo; no cambia la causa.
    return re.sub(r'Timed out retrying after \d+ms:', 'Timed out retrying after <timeout>ms:',(error or '').split('\n')[0])

def match_web(test, policy):
    ident=re.search(r'E2E-G4-\d+',' '.join(test['title']))
    key=ident.group() if ident else 'sin-ID'
    if test['state']=='passed':return {'case':key,'status':'passed','defect':None}
    rule=policy['web_rules'].get(key)
    error=web_error_signature(test.get('error'))
    allowed=rule and permitted(rule,policy) and test['spec']==rule['file'] and error==web_error_signature(rule['error']) and '@known_issue' in ' '.join(test['title'])
    return {'case':key,'status':'known_issue' if test['state']=='failed' and allowed else 'unknown_failure','defect':rule['defect'] if allowed else None}

def combine_web_runs(classified):
    combined=[]
    for key in sorted({r['case'] for run in classified for r in run}):
        values=[next((r for r in run if r['case']==key),{'case':key,'status':'missing','defect':None}) for run in classified]
        combined.append({'case':key,'status':'flaky','defect':None} if len({r['status'] for r in values})!=1 else values[0])
    return combined

def aggregate(rows, blockers=None):
    blockers=list(blockers or [])
    blockers += [f"{r['case']}: {r['status']}" for r in rows if r['status'] not in ('passed','known_issue')]
    if not rows:blockers.append('No hay pruebas ejecutadas')
    return dict(approved=not blockers,scenario='A' if not blockers and any(r['status']=='known_issue' for r in rows) else '100% exitoso' if not blockers else 'BLOQUEADO',
                counts={s:sum(r['status']==s for r in rows) for s in ('passed','known_issue','unknown_failure','flaky')},blockers=blockers,tests=rows)

def evaluate(tool, policy):
    if subprocess.check_output(['git','-C',str(ROOT/'referencias/qolqe-wallet'),'status','--porcelain'],text=True).strip():raise ValueError('Qolqe fue modificado')
    for name,digest in policy['source_hashes'].items():
        if canonical_hash(ROOT/name)!=digest:raise ValueError('Cambió una fuente aprobada: '+name)
    if tool=='karate':
        m=load(ROOT/'reports/latest-karate.json')
        if m['reference_commit']!=policy['reference_commit'] or m.get('tag') or m.get('scope')!='all':raise ValueError('Karate incompleto o referencia distinta')
        if not m.get('isolated_database'):raise ValueError('Solo se admite QA con base aislada')
        installed={k.lower():v for k,v in m.get('installed_dependencies',{}).items()}
        if any(installed.get(k)!=v for k,v in policy['runtime_versions'].items()):raise ValueError('Entorno API distinto del fijado')
        rows=parse_karate(validate(m))
        if len(rows)!=policy['expected_api_tests']:raise ValueError('Cantidad de escenarios API inesperada')
        out=aggregate([match_api(r,policy) for r in rows])
        out.update(run_id=m['run_id'],raw_exit_code=m['exit_code'],report_dir=m['report_dir'],pipeline_url=m.get('github_run_url'),qa_revision=m.get('qa_revision'))
        # Un error del proceso no explicado por los resultados no se tolera.
        if m['exit_code'] and not any(r['status']=='failed' for r in rows):out=aggregate(out['tests'],['Salida de proceso sin fallo funcional explicado'])
        return out
    if tool=='web':
        pointer=load(ROOT/'reports/cypress/latest-stability.json');m=load(ROOT/pointer['dir']/'stability.json')
        verdict=m['verdict'];required=('sameTests','sameSources','completeSuite','sameEnvironment')
        blockers=[k+' no verificado' for k in required if not verdict.get(k)]
        if m.get('completed')!=3 or len(m['runs'])!=3:raise ValueError('Se requieren tres corridas completas')
        for name,digest in m['sourceFingerprint']['files'].items():
            if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:raise ValueError('Fuentes web modificadas desde la evidencia')
        classified=[]
        for run in m['runs']:
            if run['counts']['total']!=policy['expected_web_tests'] or run['specErrors']:blockers.append('Suite web incompleta o error del spec')
            if any(run.get('runtime',{}).get(k)!=v for k,v in policy['runtime_versions'].items()):blockers.append('Entorno web distinto del fijado')
            if not run.get('databaseRemoved'):blockers.append('Aislamiento web no confirmado')
            if run['sutRevision']!=policy['reference_commit']:blockers.append('Referencia web distinta')
            classified.append([match_web(t,policy) for t in run['tests']])
        combined=combine_web_runs(classified)
        out=aggregate(combined,blockers)
        out.update(raw_runs=[r['counts'] for r in m['runs']],raw_exit_codes=[r['code'] for r in m['runs']],report_dir=pointer['dir'],pipeline_url=m['runs'][0].get('pipelineUrl'),qa_revision=m['runs'][0].get('revision'))
        return out
    m=load(ROOT/'reports/latest-schemathesis.json');detail=diagnose_schemathesis(ROOT/'reports/latest-schemathesis.json')
    if m['reference_commit']!=policy['reference_commit']:raise ValueError('Referencia de contrato distinta')
    if not m.get('isolated_database'):raise ValueError('Contrato fuera del entorno aislado')
    if m.get('openapi_sha256')!=policy.get('contract_schema_sha256'):raise ValueError('Contrato distinto del revisado')
    installed={k.lower():v for k,v in m.get('installed_dependencies',{}).items()}
    if any(installed.get(k)!=v for k,v in policy['runtime_versions'].items()):raise ValueError('Entorno de contrato distinto del fijado')
    report=load(ROOT/detail['report_dir']/'schemathesis-detallado.json')
    rows=[]
    for request in report['requests']:
        for check in request.get('checks',[]):
            if check['status']!='failure':continue
            signature=contract_signature(request,check)
            rule=policy['contract_rules'].get(signature)
            rows.append(dict(case=signature,status='known_issue' if rule and permitted(rule,policy) else 'unknown_failure',defect=rule['defect'] if rule else None))
    blockers=[]
    if m.get('seed')!=20261013 or m.get('max_examples')!=20 or m.get('stateful') is not False:blockers.append('Configuración de exploración distinta de la revisada')
    if detail['interactions']<1 or detail['context_controls']!=9:blockers.append('Exploración incompleta o sin controles')
    if detail['junit_errors'] or detail['context_controls']!=detail['context_successful_controls']:blockers.append('Error de ejecución o control contextual fallido')
    if len(rows)!=detail['failure_occurrences']:blockers.append('Detalle de contrato inconsistente')
    if m['exit_code'] and not rows:blockers.append('Salida de contrato sin fallos clasificados')
    out=aggregate(rows if rows else [{'case':'contrato','status':'passed','defect':None}],blockers)
    out.update(raw_exit_code=m['exit_code'],report_dir=m['report_dir'],pipeline_url=m.get('github_run_url'),qa_revision=m.get('qa_revision'),summary=detail)
    return out

def contract_signature(request,check):
    # Request/response ya están redactados por el exportador; se omiten headers y tiempos.
    url=urlsplit(request['url'])
    fields=dict(operation=request['operation'],method=request['method'],path=url.path,
                query=sorted(parse_qsl(url.query,keep_blank_values=True)),body=request['request_body'],
                status=request['status'],response=request['response_body'],phase=request['phase'],
                mode=request.get('metadata',{}).get('generation',{}).get('mode'),check=check['name'],
                failure_type=check.get('failure_info',{}).get('failure',{}).get('type'))
    # La cadena aleatoria del alias no cambia la causa: rechazo 409 por contacto existente
    # antes de validar un alias inválido. Se conservan operación, celular, estado y respuesta.
    body=request.get('request_body')
    if (request['operation']=='POST /api/contactos' and check['name']=='negative_data_rejection'
        and request['status']==409 and (request.get('response_body') or {}).get('codigo')=='CONTACTO_EXISTENTE'
        and isinstance(body,dict) and isinstance(body.get('alias'),str)
        and re.fullmatch(r'9[0-9]{8}',str(body.get('celular','')))):
        alias=body['alias'].strip()
        if not 3<=len(alias)<=20 or not re.fullmatch(r'[A-Za-zÁÉÍÓÚÜáéíóúüÑñ0-9 ]+',alias):
            fields['body']={'celular':body['celular'],'alias_class':'invalid_alias_rejected_by_existing_contact'}
    return hashlib.sha256(json.dumps(fields,sort_keys=True,ensure_ascii=True).encode()).hexdigest()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('tool',choices=['karate','schemathesis','web']);a=p.parse_args()
    output=ROOT/'reports/gate';output.mkdir(parents=True,exist_ok=True)
    try:
        policy=load(ROOT/'data/quality-policy.json');result=evaluate(a.tool,policy)
        result['policy_sha256']=hashlib.sha256((ROOT/'data/quality-policy.json').read_bytes()).hexdigest()
    except (Exception,SystemExit) as e:
        result=aggregate([],['Evidencia o preparación inválida: '+str(e)])
    result['tool']=a.tool
    (output/(a.tool+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='tests'},ensure_ascii=True,indent=2))
    raise SystemExit(0 if result['approved'] else 1)
