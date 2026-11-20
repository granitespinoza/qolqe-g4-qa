"""Entrega consolidada: diseño, ejecución, historial y reporte sin fabricar aprobaciones."""
from pathlib import Path
import argparse, collections, csv, datetime as dt, hashlib, html, json, os, re, shutil, sqlite3, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from diagnose_api import parse_karate

def read(path):return json.loads(Path(path).read_text(encoding='utf-8-sig'))
def write(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def safe(s):
 s=re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+','[JWT redactado]',str(s))
 return html.escape(s)
def git(*args):return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()

def audit():
 source=ROOT/'referencias/qolqe-wallet/docs/requisitos.md'
 text=source.read_text(encoding='utf-8') if source.exists() else (ROOT/'docs/final/requisitos-base.md').read_text(encoding='utf-8')
 hu=None;criteria=[]
 for line in text.splitlines():
  if line.startswith('### HU-'):hu=re.search(r'HU-[A-Z0-9]+-\d+',line).group()
  m=re.match(r'- \*\*CA(\d+)\.',line)
  if m and hu and (hu.startswith('HU-N-')or hu.startswith('HU-G4-')):criteria.append((hu,int(m[1])))
 cases=read(ROOT/'data/casos.json');matrix=[]
 for hu,ca in criteria:
  linked=[c['id']for c in cases if c['hu']==hu and ca in c['ca']]
  matrix.append(dict(hu=hu,ca=ca,cases=linked))
 features={p.relative_to(ROOT).as_posix():p.read_text(encoding='utf-8')for p in (ROOT/'tests/api/features').glob('*.feature')}
 missing=[c['id']for c in cases if not any('@'+c['id']in s.split()for s in features.values())]
 web=read(ROOT/'features/e2e/catalogo.json');webids=[x['id']for x in web]
 issues=[]
 if len(set(webids))!=len(webids):issues.append('IDs web duplicados')
 common_hus={h for c in web for h in c['hu']if h.startswith('HU-N-')}
 missing_common={f'HU-N-{n:02}'for n in range(1,10)}-common_hus
 if missing_common:issues.append('Núcleo común sin escenario web: '+', '.join(sorted(missing_common)))
 for c in web:
  if not(ROOT/c['implementation']).exists():issues.append('Implementación ausente: '+c['id'])
  p=ROOT/c['feature']
  if not p.exists()or ('Escenario: '+c['id'])not in p.read_text(encoding='utf-8'):issues.append('Gherkin ausente: '+c['id'])
  for hu in c['hu']:
   if '@'+hu not in p.read_text(encoding='utf-8'):issues.append('HU ausente: '+c['id'])
 policy=read(ROOT/'data/quality-policy.json')
 by_id={c['id']:c for c in web}
 for ident,rule in policy['web_rules'].items():
  case=by_id.get(ident)
  if not case or case.get('defect')!=rule['defect']:issues.append('Defecto no trazado en Gherkin: '+ident)
  elif '@known_issue' not in next((line for line in (ROOT/case['feature']).read_text(encoding='utf-8').splitlines()if 'Escenario: '+ident+' 'in line),''):issues.append('Etiqueta perdida en resultado Gherkin: '+ident)
 for required in ['INFORME_FINAL.md','features/e2e','tests/api/features','tests/api/reportes','tests/e2e/specs','presentacion/Entrega_Final_Qolqe.pdf']:
  if not(ROOT/required).exists():issues.append('Entregable obligatorio ausente: '+required)
 if len(web)!=policy['expected_web_tests']:issues.append('Suite web esperada: '+str(policy['expected_web_tests']))
 if len(matrix)!=51 or any(not c['cases']for c in matrix):issues.append('Criterios API sin diseño')
 if missing:issues.append('Casos sin feature API: '+str(missing))
 technical=sorted({x for s in features.values()for x in re.findall(r'@(CT-\d+)',s)})
 result=dict(design_complete=not issues,scope='G4 y núcleo común; no se atribuye cobertura a otros módulos',criteria=matrix,criteria_count=len(matrix),base_api_case_count=len(cases),api_case_count=sum(c['layer']=='API'for c in catalogue()),technical_cases=technical,web_count=len(web),web=web,issues=issues,note='Vinculación de diseño; presencia de casos no equivale a aprobación ni garantiza cobertura de todos los caminos internos.')
 write(ROOT/'data/final-audit.json',result)
 print(json.dumps({k:v for k,v in result.items()if k not in ('criteria','web')},ensure_ascii=True,indent=2))
 return result

def repo_path(value):
 path=(ROOT/str(value).replace('\\','/')).resolve()
 if not path.is_relative_to(ROOT.resolve()):raise ValueError('Ruta de evidencia fuera del repositorio')
 return path

def performance():
 result=[]
 for profile in ['carga','campana','estres']:
  p=read(ROOT/f'tests/performance/resultados/latest-{profile}.json');folder=repo_path(p['dir']);r=read(folder/'resumen.json')
  assert r['profile']==profile and r['valid']and r['integrity']['approved'],profile
  assert r['meta']['reference_commit']=='8c7d2f0c939ede7765b7b80b98c10c3905693fda'
  for f in ['recursos.csv','operaciones.jsonl','integridad.json','procedencia.json','reporte.html','graficos/evolucion.png']:
   assert(folder/f).exists(),folder/f
  result.append(dict(profile=profile,run_id=r['meta']['run_id'],dir=folder.relative_to(ROOT).as_posix(),valid=r['valid'],approved=r['approved'],integrity=r['integrity'],windows=r['windows'],by_operation=r['by_operation'],resources=r['resources'],historical=True))
 write(ROOT/'data/final-performance.json',result)
 print('Tres experimentos históricos identificados. Carga/estrés conservan sus incumplimientos; no son corridas nuevas de CI.')
 return result

def catalogue():
 rows=[]
 for p in sorted((ROOT/'tests/api/features').glob('*.feature')):
  text=p.read_text(encoding='utf-8');feature_hus=re.findall(r'@(HU-[A-Z0-9-]+)',text.split('Background:')[0]);tags=[]
  for line in text.splitlines():
   if line.strip().startswith('@'):tags=line.split()
   m=re.match(r'\s*Scenario(?: Outline)?:\s*(.+)',line)
   if m:
    ids=[x[1:]for x in tags if re.fullmatch(r'@(G4|CF|CT)-\d+',x)]
    for ident in ids:rows.append(dict(id=ident,title=m[1],hu=sorted(set(feature_hus+[x[1:]for x in tags if x.startswith('@HU-')])),layer='API',file=p.relative_to(ROOT).as_posix(),tags=tags))
 for c in read(ROOT/'features/e2e/catalogo.json'):rows.append(dict(id=c['id'],title=c['title'],hu=c['hu'],layer='Web',file=c['feature'],tags=['@'+h for h in c['hu']]+['@TC-'+c['id']]))
 unique={c['id']:c for c in rows}
 for c in unique.values():c['version']=sha(ROOT/c['file'])
 return sorted(unique.values(),key=lambda c:(c['layer'],c['id']))

def collect():
 runs=[];issues=[];gates={}
 for tool in ['schemathesis','karate','web']:
  p=ROOT/f'reports/gate/{tool}.json'
  if p.exists():
   g=read(p)
   if g.get('policy_sha256')!=sha(ROOT/'data/quality-policy.json'):
    issues.append(tool+': gate de otra versión de política')
    gates[tool]={'tool':tool,'approved':False,'scenario':'SIN EVALUACIÓN ACTUAL','counts':{},'blockers':['Política distinta']}
   else:gates[tool]=g
  else:issues.append('Falta gate '+tool)
 revision=os.environ.get('GITHUB_SHA')or git('rev-parse','HEAD');run_url=(f'https://github.com/{os.environ["GITHUB_REPOSITORY"]}/actions/runs/{os.environ["GITHUB_RUN_ID"]}'if os.environ.get('GITHUB_RUN_ID')else None)
 for tool in ['schemathesis','karate']:
  p=ROOT/f'reports/latest-{tool}.json'
  if not p.exists():issues.append('Falta ejecución '+tool);continue
  m=read(p);folder=ROOT/m['report_dir']
  if not folder.exists():issues.append('Reporte ausente '+tool);continue
  try:
   from qa_provenance import validate
   validate(m)
   if run_url and(m.get('github_run_url')!=run_url or m.get('qa_revision')!=revision):raise ValueError('Ejecución de otro run o commit')
   expected_report='karate-summary.html'if tool=='karate'else'schemathesis-detallado.html'
   if not(folder/expected_report).is_file():issues.append('HTML ausente '+tool)
   if tool=='karate':
    tests=[];classified={r['case']:r for r in gates.get(tool,{}).get('tests',[])}
    for t in parse_karate(folder):
     for ident in t['cases']:
      g=classified.get(t['key'],{})
      tests.append(dict(case_id=ident,variant=t['key'],state=t['status'],classification=g.get('status','unclassified'),defect=g.get('defect'),error='; '.join(s['signature'].split('\n')[0]for s in t.get('failure_signatures',[]))))
   else:tests=[dict(case_id='SCHEMATHESIS',variant=t['case'],state='passed'if t['status']=='passed'else'failed',classification=t['status'],defect=t.get('defect'),error='Señal de contrato; no equivale a un caso funcional.')for t in gates.get(tool,{}).get('tests',[])]
   runs.append(dict(key=tool+':'+m['run_id'],layer=tool,started=m['started_at'],revision=m.get('qa_revision'),dirty=m.get('qa_worktree_dirty'),url=m.get('github_run_url'),report_dir=m['report_dir'],report_file='karate-summary.html'if tool=='karate'else'schemathesis-detallado.html',source_hash=hashlib.sha256(json.dumps(m['source_hashes'],sort_keys=True).encode()).hexdigest(),tests=tests))
  except (Exception,SystemExit)as e:issues.append(tool+': '+str(e))
 p=ROOT/'reports/cypress/latest-stability.json'
 if p.exists():
  try:
   pointer=read(p);m=read(ROOT/pointer['dir']/'stability.json');classified={r['case']:r for r in gates.get('web',{}).get('tests',[])}
   if m['completed']!=3 or len(m['runs'])!=3:issues.append('Web incompleta: '+str(m['completed'])+'/3 corridas completas; repetir secuencia')
   for f,digest in m['sourceFingerprint']['files'].items():assert sha(ROOT/f)==digest,'Fuentes modificadas: '+f
   for i,r in enumerate(m['runs'],1):
    if not(ROOT/r['runDir']/'html/index.html').is_file():issues.append('HTML web ausente: '+r['runDir'])
    if run_url:assert r.get('pipelineUrl')==run_url and r.get('revision')==revision,'Web de otro run'
    tests=[]
    for t in r['tests']:
     title=' '.join(t['title']);ident=re.search(r'E2E-G4-\d+',title)
     assert ident,'Caso web sin ID';g=classified.get(ident[0],{})
     tests.append(dict(case_id=ident[0],variant=t['spec']+'::'+ident[0],state=t['state'],classification=g.get('status','unclassified'),defect=g.get('defect'),error=(t.get('error')or'').split('\n')[0]))
    runs.append(dict(key='web:'+r['runDir'],layer='web',started=r['started'],revision=r.get('revision'),dirty=r.get('worktreeDirty'),url=r.get('pipelineUrl'),report_dir=r['runDir'],report_file='html/index.html',source_hash=r['sourceFingerprint']['hash'],repetition=i,tests=tests))
  except (Exception,SystemExit)as e:issues.append('web: '+str(e))
 else:issues.append('Falta secuencia web actual')
 for tool,g in list(gates.items()):
  if not any(r['layer']==tool for r in runs):
   issues.append(tool+': sin ejecución actual verificada')
   gates[tool]={'tool':tool,'approved':False,'scenario':'SIN EJECUCIÓN ACTUAL','counts':{},'blockers':['No hay ejecución verificada para este gate']}
  if not g.get('approved'):issues.append(tool+': gate rechazado')
  if g.get('policy_sha256')!=sha(ROOT/'data/quality-policy.json'):issues.append(tool+': política distinta')
  if run_url and(g.get('pipeline_url')!=run_url or g.get('qa_revision')!=revision):issues.append(tool+': gate de otro run')
 return runs,gates,sorted(set(issues))

def history(cases,runs,database=None):
 database=database or ROOT/'.tools/final-history.sqlite';database.parent.mkdir(parents=True,exist_ok=True)
 c=sqlite3.connect(database)
 try:
  c.executescript('CREATE TABLE IF NOT EXISTS cases(id TEXT,version TEXT,title TEXT,hu TEXT,layer TEXT,file TEXT,PRIMARY KEY(id,version)); CREATE TABLE IF NOT EXISTS runs(key TEXT PRIMARY KEY,layer TEXT,started TEXT,revision TEXT,source_hash TEXT,url TEXT); CREATE TABLE IF NOT EXISTS executions(run_key TEXT,case_id TEXT,variant TEXT,state TEXT,classification TEXT,defect TEXT,error TEXT,PRIMARY KEY(run_key,case_id,variant));')
  for row in cases:c.execute('INSERT OR IGNORE INTO cases VALUES(?,?,?,?,?,?)',(row['id'],row['version'],row['title'],json.dumps(row['hu']),row['layer'],row['file']))
  for r in runs:
   prior=c.execute('SELECT source_hash FROM runs WHERE key=?',(r['key'],)).fetchone()
   if prior and prior[0]!=r['source_hash']:raise ValueError('No se puede reescribir una corrida con otras fuentes')
   c.execute('INSERT OR IGNORE INTO runs VALUES(?,?,?,?,?,?)',(r['key'],r['layer'],r['started'],r['revision'],r['source_hash'],r['url']))
   for t in r['tests']:
    values=(r['key'],t['case_id'],t['variant'],t['state'],t['classification'],t.get('defect'),t.get('error',''))
    prev=c.execute('SELECT * FROM executions WHERE run_key=? AND case_id=? AND variant=?',values[:3]).fetchone()
    if prev and tuple(prev)!=values:raise ValueError('No se puede sobrescribir el resultado histórico de '+t['case_id'])
    c.execute('INSERT OR IGNORE INTO executions VALUES(?,?,?,?,?,?,?)',values)
  c.commit();c.row_factory=sqlite3.Row
  result=[dict(x)for x in c.execute('SELECT runs.*,count(executions.case_id) AS executions FROM runs LEFT JOIN executions ON runs.key=executions.run_key GROUP BY runs.key ORDER BY started DESC')]
  c.close();return result
 finally:c.close()

def ai_evidence():
 proof=read(ROOT/'data/final-ia.json')
 assert proof['executed']and proof['passed']and proof['historical_local'],'Prueba IA no verificada'
 assert proof['reference_commit']=='8c7d2f0c939ede7765b7b80b98c10c3905693fda','Referencia IA distinta'
 assert hashlib.sha256((ROOT/proof['execution']).read_text(encoding='utf-8').encode()).hexdigest()==proof['execution_sha256'],'Registro IA alterado'
 raw=read(ROOT/proof['execution'])
 assert raw['mode']=='ai'and raw['code']==0 and raw['counts']['passed']==raw['counts']['total']==1,'IA incompleta o fallida'
 assert(ROOT/proof['report']).is_file(),'Reporte IA ausente'
 for f,digest in proof['source_hashes'].items():assert hashlib.sha256((ROOT/f).read_text(encoding='utf-8').encode()).hexdigest()==digest,'Fuente IA distinta: '+f
 return proof

STYLE="""body{font:17px/1.6 Segoe UI,Arial;color:#172b29;background:#f5f7f4;margin:0}main{max-width:1250px;margin:auto;padding:28px}h1,h2{line-height:1.2}a{color:#136b5b}table{width:100%;border-collapse:collapse;font-size:14px}th,td{border:1px solid #d7dfda;padding:9px;text-align:left;vertical-align:top}th{background:#e1ece5}section{background:white;border:1px solid #d7dfda;padding:24px;border-radius:12px;margin:22px 0}.scroll{overflow:auto}.cards{display:flex;gap:14px;flex-wrap:wrap}.card{padding:18px;background:#e7eee7;flex:1;min-width:180px}.big{font-size:32px;font-weight:bold}.warning{border-left:5px solid #a45336;padding:12px;background:#fff4ec}input,select,button{font:inherit;padding:8px;margin:6px}img{max-width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}small{color:#4b6059}@media print{button,input,select{display:none}section{break-inside:avoid}}"""
def table(headers,rows):return '<div class="scroll"><table><tr>'+''.join('<th>'+safe(x)+'</th>'for x in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+str(v)+'</td>'for v in row)+'</tr>'for row in rows)+'</table></div>'
def report(evidence='none'):
 design=audit();cases=catalogue();runs,gates,issues=collect()
 try:perf=performance()
 except (Exception,SystemExit)as e:perf=[];issues.append('Evidencia de rendimiento inválida: '+str(e))
 try:ai=ai_evidence()
 except (Exception,SystemExit)as e:ai=None;issues.append('Evidencia IA inválida: '+str(e))
 jobs=json.loads(os.environ.get('QA_JOB_RESULTS','{}'))
 issues+=['Job '+k+': '+v.get('result','ausente')for k,v in jobs.items()if v.get('result')!='success']
 if not design['design_complete']:issues+=design['issues']
 historical=history(cases,runs)
 evidence_ids={t['case_id']for r in runs if r['layer']=='karate'for t in r['tests']}
 missing_api=[c['id']for c in cases if c['layer']=='API'and c['id']not in evidence_ids]
 if missing_api:issues.append('Casos API sin ejecución actual: '+', '.join(missing_api))
 current=dict(worktree_dirty=bool(git('status','--porcelain')),created=dt.datetime.now(dt.timezone.utc).isoformat(),revision=git('rev-parse','HEAD'),evidence=evidence,ai=ai,approved=not issues,blockers=sorted(set(issues)),cases=cases,runs=runs,gates=gates,history=historical,performance=perf,design_summary={'criteria':design['criteria_count'],'web':design['web_count']},remote_run=os.environ.get('GITHUB_RUN_ID'),run_attempt=os.environ.get('GITHUB_RUN_ATTEMPT'),note='El gate académico no certifica producción. Rendimiento conserva experimentos históricos y sus incumplimientos.')
 write(ROOT/'data/final-report.json',current);write(ROOT/'results/final/report.json',current)
 write(ROOT/'results/final/cases-kiwi.json',cases)
 base=ROOT/'results/final';base.mkdir(parents=True,exist_ok=True)
 with(base/'trazabilidad.csv').open('w',encoding='utf-8-sig',newline='')as f:
  w=csv.writer(f);w.writerow(['HU','TC','Version del diseño','Run','Repetición','Commit QA','Estado crudo','Clasificación','Defecto','URL pipeline','Archivo'])
  by={c['id']:c for c in cases}
  for r in runs:
   for t in r['tests']:
    case=by.get(t['case_id'],{});w.writerow([','.join(case.get('hu',[])),t['case_id'],case.get('version'),r['key'],r.get('repetition',''),r['revision'],t['state'],t['classification'],t.get('defect'),r.get('url'),case.get('file')])
 body='<h1>Qolqe · Reporte final consolidado</h1><p>Commit QA: <code>'+safe(current['revision'])+'</code> · Cambios locales: '+safe(current['worktree_dirty'])+' · Evidencia web: '+safe(evidence)+'</p>'
 body+='<p><a href="../../apidoc/final/index.html">Presentación</a> · <a href="trazabilidad.csv">Matriz por ejecución CSV</a> · <a href="report.json">Datos y procedencia</a> · <a href="../../docs/final/gestion-casos.md">Kiwi TCMS</a></p>'
 body+='<div class="cards"><div class="card">Gate académico<br><strong>'+('APROBADO'if current['approved']else'BLOQUEADO')+'</strong></div><div class="card">Criterios API diseñados<div class="big">'+safe(design['criteria_count'])+'</div></div><div class="card">Escenarios web<div class="big">'+safe(design['web_count'])+'</div></div></div>'
 if issues:body+='<section class="warning"><h2>Bloqueos reales</h2><ul>'+''.join('<li>'+safe(x)+'</li>'for x in sorted(set(issues)))+'</ul></section>'
 body+='<section><h2>Quality gates y resultados</h2>'+table(['Herramienta','Gate','PASS','Known issue','Desconocido','Flaky'],[[safe(k),safe(g.get('scenario')),*('—'if k=='schemathesis'and x=='passed'else safe(g.get('counts',{}).get(x,0))for x in ['passed','known_issue','unknown_failure','flaky'])]for k,g in gates.items()])+'<p>Las señales de Schemathesis no son casos funcionales. Los fallos conocidos permanecen FAIL; solo sus firmas admitidas pueden permitir Escenario A.</p></section>'
 body+='<section><h2>Corridas actuales</h2>'+table(['Capa','ID / repetición','Resultados crudos','Reporte'],[[safe(r['layer']),safe(r['key']),safe(dict(collections.Counter(t['state']for t in r['tests']))),f'<a href="../../{r["report_dir"]}/{r["report_file"]}">Abrir HTML</a>']for r in runs])+'</section>'
 body+='<section><h2>HU → caso → variante → ejecución</h2><input id="buscar" placeholder="Buscar HU, TC, estado o defecto" aria-label="Filtrar trazabilidad"><p>Una misma prueba conserva resultados separados por corrida y repetición.</p>'
 matrix=[];by={c['id']:c for c in cases}
 for r in runs:
  for t in r['tests']:
   c=by.get(t['case_id'],{});matrix.append([safe(', '.join(c.get('hu',[]))),safe(t['case_id']),safe(t['variant']),safe(r.get('repetition')or r['key']),safe(t['state']),safe(t['classification']),safe(t.get('defect')or'—')])
 body+=table(['HU','TC','Variante','Ejecución','Crudo','Gate','Defecto'],matrix)+'</section>'
 body+='<section><h2>Historial de múltiples ejecuciones</h2>'+table(['Run','Fecha','Commit','Variantes o firmas únicas'],[[safe(r['key']),safe(r['started']),safe(r['revision']),safe(r['executions'])]for r in historical])+'<p>Historial local SQLite y caché por rama en CI. Para contrato agrupamos firmas iguales en el historial; las ocurrencias completas permanecen en el reporte de Schemathesis y en la matriz. La caché no reemplaza un servicio duradero de gestión. Kiwi TCMS se configura por separado y recibe cada corrida sin sobrescribir anteriores.</p></section>'
 if ai:body+='<section><h2>IA: ejecución local real documentada</h2><p>cy.prompt: 1/1 aprobada. POST 201 y persistencia verificados con aserciones explícitas. Run '+safe(ai['run_id'])+'. No es una nueva ejecución IA de este pipeline.</p><a href="../../'+safe(ai['report'])+'">Abrir reporte IA</a></section>'
 kiwi_file=base/'kiwi-status.json'
 if kiwi_file.exists():
  from kiwi_sync import digest,payload
  kiwi=read(kiwi_file);verified=kiwi.get('remote_verified')is True and kiwi.get('readback_verified')is True and kiwi.get('payload_sha256')==digest(payload(current))
  body+='<section><h2>Kiwi TCMS: gestión de casos</h2><p>'+('Sincronización real verificada para estas ejecuciones.'if verified else'Sin sincronización verificada para estas ejecuciones; revisar configuración o volver a sincronizar.')+'</p>'
  if verified:body+='<a href="'+safe(kiwi['plan_url'])+'">Abrir plan de casos en Kiwi</a>'+table(['Run local','ID en Kiwi','Estado'],[[safe(x['key']),safe(x['id']),safe(x['status'])]for x in kiwi['runs']])
  body+='<p>Kiwi agrupa variantes por caso. La matriz mantiene las variantes por separado y los comentarios conservan su detalle; un FAIL no se transforma en PASS por admitirlo en el gate.</p></section>'
 body+='<section><h2>Rendimiento: experimentos históricos, no nueva ejecución CI</h2>'+table(['Perfil','Run','Volumen','p95 movimientos','Integridad','Reporte'],[[safe({'campana':'Campaña','estres':'Estrés','carga':'Carga'}.get(p['profile'],p['profile'])),safe(p['run_id']),safe(round(p['windows'][0]['ops_s'],2))if p['profile']!='estres'else'Por escalón',safe(round(p['by_operation']['movimientos']['p95'],2)),safe(p['integrity']['approved']),f'<a href="../../{p["dir"]}/reporte.html">Abrir reporte</a>']for p in perf])+'<p>Carga: 5.47 operaciones correctas/s y movimientos 914.80 ms > 800 ms. Campaña: integridad conforme; no tiene nuevo SLA temporal. Estrés: incumplimiento temporal desde 100, degradación severa en 450 y cero operaciones exitosas/s en 600 durante su ventana.</p></section>'
 body+='<section><h2>Evidencia de imágenes</h2>'
 if evidence=='images':
  images=[p for r in runs if r['layer']=='web'for p in (ROOT/r['report_dir']/'screenshots').rglob('*.png')]
  body+=''.join(f'<details><summary>{safe(p.name)}</summary><img loading="lazy" src="../../{p.relative_to(ROOT).as_posix()}" alt="{safe(p.name)}"></details>'for p in images)
  if not images:body+='<p>No se recibieron capturas; no se inventa evidencia visual.</p>'
 else:body+='<p>Modo sin capturas: conservamos resultados, errores, matriz y procedencia. Los gráficos de rendimiento son mediciones y se conservan en ambos modos.</p>'
 body+='</section>'
 page='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Qolqe · Reporte final</title><style>'+STYLE+'</style><main>'+body+'</main><script>document.querySelector("#buscar").oninput=e=>{const t=e.target.closest("section").querySelector("table");[...t.rows].slice(1).forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(e.target.value.toLowerCase()))}</script></html>'
 (base/'index.html').write_text(page,encoding='utf-8')
 # Self-contained site keeps repository-relative links, copies only selected current evidence.
 site=base/'site'
 if site.exists():
  assert site.resolve().parent==base.resolve(),'Destino de sitio fuera del reporte'
  shutil.rmtree(site)
 site.mkdir(exist_ok=True)
 paths=['apidoc/final','docs/final','docs/parte3','features','tests/e2e','tests/api','.github','INFORME_FINAL.md','presentacion/Entrega_Final_Qolqe.pdf']+[p['dir']for p in perf]+[r['report_dir']for r in runs]
 for rel in paths:
  source=ROOT/rel
  if source.exists():
   target=site/rel;target.parent.mkdir(parents=True,exist_ok=True)

   if source.is_dir():shutil.copytree(source,target,dirs_exist_ok=True,ignore=shutil.ignore_patterns('screenshots','videos')if evidence=='none'and rel.startswith('reports/')else None)
   else:shutil.copy2(source,target)
 for source in list((ROOT/'tests/performance/resultados').glob('diagnostico*'))+[ROOT/'data/quality-policy.json']:
  if source.is_file():
   target=site/source.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,target)
 target=site/'results/final';target.mkdir(parents=True,exist_ok=True)
 for name in ['index.html','report.json','trazabilidad.csv','cases-kiwi.json']+(['kiwi-status.json']if(base/'kiwi-status.json').exists()else[]):shutil.copy2(base/name,target/name)
 (site/'index.html').write_text('<!doctype html><meta http-equiv="refresh" content="0;url=results/final/index.html"><a href="results/final/index.html">Reporte final</a>',encoding='utf-8')

 api_out=ROOT/'tests/api/reportes';api_out.mkdir(parents=True,exist_ok=True)
 write(api_out/'resumen.json',{'revision':current['revision'],'remote_run':current['remote_run'],'gates':{k:v for k,v in gates.items()if k in ('karate','schemathesis')},'runs':[r for r in runs if r['layer']in ('karate','schemathesis')]})
 (api_out/'index.html').write_text('<!doctype html><meta charset="utf-8"><h1>Reportes API de esta ejecución</h1><p>Los resultados conservan sus PASS/FAIL. <a href="../../../results/final/index.html">Abrir consolidado, matriz y reportes crudos</a></p>',encoding='utf8')
 dest_api=site/'tests/api/reportes';dest_api.mkdir(parents=True,exist_ok=True)
 for file in ['index.html','resumen.json']:shutil.copy2(api_out/file,dest_api/file)
 print('Reporte generado:',base/'index.html','Gate:',current['approved'])
 return current

def summary():
 p=ROOT/'data/final-report.json'
 if not p.exists():raise SystemExit('No se generó el reporte final')
 r=read(p);lines=['# Qolqe · Resultado final','',f'**Gate académico: {"APROBADO"if r["approved"]else"BLOQUEADO"}** · Commit `{r["revision"]}` · intento `{r.get("run_attempt")}`.', '', '| Suite | Gate | PASS | Conocidos | Desconocidos | Flaky |','|---|---|---:|---:|---:|---:|']
 for k,g in r['gates'].items():lines.append('| '+' | '.join([k,g.get('scenario','ausente')]+['—'if k=='schemathesis'and x=='passed'else str(g.get('counts',{}).get(x,0))for x in ['passed','known_issue','unknown_failure','flaky']])+' |')
 lines+=['','## Tres corridas web','', '| Corrida | Aprobados crudos | Fallidos crudos | Omitidos |','|---|---:|---:|---:|']
 for run in r['runs']:
  if run['layer']=='web':
   c=collections.Counter(t['state']for t in run['tests']);lines.append(f'| {run.get("repetition")} | {c["passed"]} | {c["failed"]} | {c["pending"]+c["skipped"]} |')
 lines+=['','## Bloqueos',*['- '+x for x in r['blockers']], '', '## Rendimiento documentado','Carga: 5.47 operaciones correctas/s; movimientos p95 914.80 ms frente a 800 ms. Campaña: integridad conforme y latencia degradada. Estrés: degradación severa desde el escalón 450. Son experimentos históricos identificados, no nuevas corridas de este pipeline.', '', '## Entregable navegable',f'[Descargar sitio HTML, matriz y evidencias]({os.environ.get("QA_ARTIFACT","")}). Extraer y abrir `results/final/site/index.html`. La tabla de resultados anterior es visible directamente al finalizar el job.','', '## Trazabilidad (una fila por caso, variante y repetición)','| HU | TC | Corrida | Crudo | Clasificación | Defecto |','|---|---|---|---|---|---|']
 by={c['id']:c for c in r['cases']}
 for run in r['runs']:
  for t in run['tests']:
   c=by.get(t['case_id'],{});lines.append('| '+' | '.join([','.join(c.get('hu',[])),t['case_id'],str(run.get('repetition')or run['layer']),t['state'],t['classification'],str(t.get('defect')or'—')])+' |')
 kiwi=ROOT/'results/final/kiwi-status.json'
 if kiwi.exists():
  state=read(kiwi);lines+=['','## Gestión de casos', 'Kiwi TCMS: **'+state['status']+'**. Sin configuración no se afirma sincronización remota.']
 text='\n'.join(lines)
 dest=os.environ.get('GITHUB_STEP_SUMMARY')
 if dest:
  with open(dest,'a',encoding='utf-8')as f:f.write(text+'\n')
 (ROOT/'results/final/resumen-actions.md').write_text(text,encoding='utf-8');print(text[:500])

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('action',choices=['audit','performance','report','summary','gate']);p.add_argument('--evidence',choices=['none','images'],default='none');a=p.parse_args()
 if a.action=='audit':raise SystemExit(0 if audit()['design_complete']else 1)
 if a.action=='performance':performance()
 if a.action=='report':report(a.evidence)
 if a.action=='summary':summary()
 if a.action=='gate':
  result=read(ROOT/'data/final-report.json');print('Gate final:',result['approved']);raise SystemExit(0 if result['approved']else 1)
