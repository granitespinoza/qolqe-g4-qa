"""Publica casos versionados y corridas separadas en Kiwi TCMS; sin credenciales queda preparado."""
from pathlib import Path
import argparse,hashlib,json,os,sys
ROOT=Path(__file__).resolve().parents[1]
def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=True).encode()).hexdigest()
def aggregate_case(tests):
 return 'FAILED'if any(t['state']=='failed'for t in tests)else'PASSED'if tests and all(t['state']=='passed'for t in tests)else'BLOCKED'
def payload(report):
 catalogue={c['id']:c for c in report['cases']};runs=[]
 for run in report['runs']:
  if run['layer']=='schemathesis':continue # contract checks remain a separate signal report
  grouped={}
  for t in run['tests']:grouped.setdefault(t['case_id'],[]).append(t)
  rows=[]
  for ident,tests in grouped.items():
   case=catalogue.get(ident)
   if not case:raise ValueError('Caso sin catálogo: '+ident)
   rows.append({'case':case,'state':aggregate_case(tests),'variants':tests})
  runs.append({'key':run['key'],'revision':run['revision'],'url':run.get('url'),'started':run['started'],'cases':rows,'fingerprint':digest(rows)})
 return {'runs':runs,'note':'FAIL conocido permanece FAILED; cada repetición y variante se conserva. No se escriben credenciales.'}
def sync(data,rpc,plan_id,build_id,manager_id,product_id,category_id):
 confirmed=rpc.TestCaseStatus.filter({'name':'CONFIRMED'})
 if not confirmed:raise ValueError('Kiwi no tiene estado CONFIRMED')
 statuses={x['name'].upper():x['id']for x in rpc.TestExecutionStatus.filter({})}
 for state in ['PASSED','FAILED','BLOCKED']:
  if state not in statuses:raise ValueError('Falta estado Kiwi: '+state)
 created=[]
 for run in data['runs']:
  summary='Qolqe '+run['key']+' '+run['fingerprint'][:12]
  # Primero resolvemos casos; una interrupción no debe crear una corrida vacía que luego parezca completa.
  items=[]
  for item in run['cases']:
   c=item['case'];prefix=c['id']+' ['+c['version'][:12]+']';name=prefix+' '+c['title']
   matches=rpc.TestCase.filter({'category__product':product_id,'summary__startswith':prefix})
   if len(matches)>1:raise ValueError('Version de caso duplicada en Kiwi: '+prefix)
   if matches:case_id=matches[0]['id']
   else:
    case=rpc.TestCase.create({'product':product_id,'category':category_id,'priority':1,'case_status':confirmed[0]['id'],'summary':name,'text':'HU: '+', '.join(c['hu'])+'\nFuente: '+c['file']+'\nSHA256: '+c['version']})
    case_id=case['id']
   rpc.TestPlan.add_case(plan_id,case_id)
   items.append((case_id,item))
  existing=rpc.TestRun.filter({'plan':plan_id,'summary':summary})
  if existing:run_id=existing[0]['id']
  else:
   target=rpc.TestRun.create({'plan':plan_id,'build':build_id,'manager':manager_id,'summary':summary});run_id=target['id']
   rpc.TestRun.add_property(run_id,'qa-run-key',run['key']);rpc.TestRun.add_property(run_id,'qa-revision',run['revision']);rpc.TestRun.add_property(run_id,'qa-results-sha256',run['fingerprint'])
  writes=0
  for case_id,item in items:
   executions=rpc.TestRun.add_case(run_id,case_id)
   if not executions:raise ValueError('Kiwi no devolvió ejecución para el caso '+str(case_id))
   comment=json.dumps({'run':run['key'],'commit':run['revision'],'pipeline':run.get('url'),'variants':item['variants']},ensure_ascii=False)
   for execution in executions:
    expected=statuses[item['state']];actual=execution['status']
    if actual!=expected:
     if actual!=statuses.get('IDLE'):raise ValueError('Se rechaza sobrescribir un resultado distinto en Kiwi: '+str(execution['id']))
     rpc.TestExecution.update(execution['id'],{'status':expected});writes+=1
    comments=rpc.TestExecution.get_comments(execution['id'])
    if not any(x.get('comment')==comment for x in comments):rpc.TestExecution.add_comment(execution['id'],comment);writes+=1
  expected_states={case_id:statuses[item['state']]for case_id,item in items}
  observed=rpc.TestExecution.filter({'run':run_id})
  if {x['case']:x['status']for x in observed}!=expected_states:raise ValueError('Kiwi no conserva los resultados esperados para la corrida '+str(run_id))
  created.append({'key':run['key'],'id':run_id,'status':'created'if not existing else'resumed'if writes else'already_exists_not_modified','cases':len(items)})

 return created
def main():
 p=argparse.ArgumentParser();p.add_argument('--dry-run',action='store_true');p.add_argument('--report',type=Path,default=ROOT/'data/final-report.json');args=p.parse_args()
 report=args.report
 if not report.exists():raise SystemExit('Primero ejecutar scripts/final_delivery.py report')
 data=payload(json.loads(report.read_text(encoding='utf-8')))
 output=ROOT/'results/final';output.mkdir(parents=True,exist_ok=True)
 (output/'kiwi-payload.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
 required=['KIWI_URL','KIWI_USER','KIWI_PASSWORD','KIWI_PLAN_ID','KIWI_BUILD_ID','KIWI_MANAGER_ID','KIWI_PRODUCT_ID','KIWI_CATEGORY_ID']
 missing=[k for k in required if not os.environ.get(k)]
 if args.dry_run or missing:
  result={'status':'dry_run'if args.dry_run else'not_configured','missing_variables':missing,'runs_prepared':len(data['runs']),'remote_verified':False}
 else:
  from tcms_api import TCMS
  rpc=TCMS(os.environ['KIWI_URL'],os.environ['KIWI_USER'],os.environ['KIWI_PASSWORD']).exec
  ids=[int(os.environ[k])for k in ['KIWI_PLAN_ID','KIWI_BUILD_ID','KIWI_MANAGER_ID','KIWI_PRODUCT_ID','KIWI_CATEGORY_ID']]
  result={'status':'synced','remote_verified':True,'readback_verified':True,'runs':sync(data,rpc,*ids)}
 result['payload_sha256']=digest(data)
 if result.get('remote_verified'):
  from urllib.parse import urlsplit
  endpoint=urlsplit(os.environ['KIWI_URL']);result['plan_url']=endpoint.scheme+'://'+endpoint.netloc.rsplit('@',1)[-1]+'/plan/'+os.environ['KIWI_PLAN_ID']+'/'
 (output/'kiwi-status.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=True,indent=2))
if __name__=='__main__':main()
