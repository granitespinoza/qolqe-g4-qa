"""Ejecuta suites, conserva su salida real y aplica el gate; nunca ignora fallos a ciegas."""
import argparse
import hashlib
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from quality_gate import aggregate
from export_results import export

ROOT=Path(__file__).resolve().parents[1]
git_bundle=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd'
if os.name=='nt' and git_bundle.exists():os.environ['PATH']=str(git_bundle)+os.pathsep+os.environ.get('PATH','')

def node():
    bundled=Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node.exe'
    return str(bundled) if os.name=='nt' and bundled.exists() else shutil.which('node') or 'node'

def run(tool):
    os.chdir(ROOT)
    started=dt.datetime.now(dt.timezone.utc)
    command=[node(),'scripts/cypress/stability.mjs'] if tool=='web' else [sys.executable,'scripts/run_qa.py',tool,'--start-api']
    code=subprocess.run(command).returncode
    try:
        if tool=='web':
            pointer=json.loads((ROOT/'reports/cypress/latest-stability.json').read_text())
            evidence=json.loads((ROOT/pointer['dir']/'stability.json').read_text())
            timestamp=evidence['runs'][0]['started']
        else:
            evidence=json.loads((ROOT/f'reports/latest-{tool}.json').read_text())
            timestamp=evidence['started_at']
            if evidence['exit_code']!=code:raise ValueError('Salida cruda y manifiesto diferentes')
        if dt.datetime.fromisoformat(timestamp.replace('Z','+00:00'))<started-dt.timedelta(seconds=2):raise ValueError('No hay evidencia nueva de esta ejecución')
    except Exception as e:
        result=aggregate([],['Error de ejecución/preparación: '+str(e)]);result['raw_process_exit']=code;result['tool']=tool
        output=ROOT/'reports/gate';output.mkdir(parents=True,exist_ok=True)
        (output/(tool+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
        return 1
    return subprocess.run([sys.executable,'scripts/quality_gate.py',tool]).returncode

def overall():
    outputs=[];blockers=[]
    policy_hash=hashlib.sha256((ROOT/'data/quality-policy.json').read_bytes()).hexdigest()
    current=(os.environ.get('GITHUB_SERVER_URL','https://github.com')+'/'+os.environ['GITHUB_REPOSITORY']+'/actions/runs/'+os.environ['GITHUB_RUN_ID']) if os.environ.get('GITHUB_RUN_ID') else None
    for tool in ('karate','schemathesis','web'):
        path=ROOT/f'reports/gate/{tool}.json'
        if not path.exists():blockers.append('Falta gate '+tool);continue
        result=json.loads(path.read_text(encoding='utf-8'));outputs.append(result)
        if result.get('policy_sha256')!=policy_hash:blockers.append('Política distinta: '+tool)
        if current and result.get('qa_revision')!=os.environ.get('GITHUB_SHA'):blockers.append('Commit distinto: '+tool)
        if not result.get('approved'):blockers.append(tool+': '+str(result.get('blockers')))
        if current and result.get('pipeline_url')!=current:blockers.append('Gate de otro run: '+tool)
    for kind in ('api','web'):
        try:export(kind)
        except (Exception,SystemExit) as e:blockers.append('Reportería JUnit '+kind+': '+str(e))
    result=dict(approved=not blockers,scenario='A' if not blockers and any(r.get('scenario')=='A' for r in outputs) else '100% exitoso' if not blockers else 'BLOQUEADO',pipeline_url=current,blockers=blockers,tools=outputs)
    output=ROOT/'reports/gate';output.mkdir(parents=True,exist_ok=True)
    (output/'overall.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    text=['# Quality Gate — Entrega 2','',f"Decisión: **{result['scenario']}**. Aprobado: **{result['approved']}**.",'',
          'Las pruebas conservan sus PASS/FAIL originales. Escenario A admite únicamente firmas conocidas para la instancia académica aislada; no certifica el producto para producción.','',
          '| Herramienta | Gate | PASS | Known issue | Desconocido | Flaky |','|---|---|---:|---:|---:|---:|']
    for r in outputs:
        c=r.get('counts',{});passed='—' if r['tool']=='schemathesis' else c.get('passed',0);text.append(f"| {r['tool']} | {r['scenario']} | {passed} | {c.get('known_issue',0)} | {c.get('unknown_failure',0)} | {c.get('flaky',0)} |")
    text+=['','En Schemathesis se clasifican ocurrencias de checks fallidos; no representan el total de interacciones ni casos funcionales únicos.','', 'Bloqueos: '+('; '.join(blockers) or 'ninguno'),'']
    (output/'resumen.md').write_text('\n'.join(text),encoding='utf-8')
    if os.environ.get('GITHUB_STEP_SUMMARY'):
        with open(os.environ['GITHUB_STEP_SUMMARY'],'a',encoding='utf-8') as f:f.write('\n'.join(text))
    print('\n'.join(text))
    return 0 if result['approved'] else 1

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['api','web','reporting']);a=p.parse_args()
    if a.mode=='api':
        codes=[run(t) for t in ('karate','schemathesis')]
        export('api')
        raise SystemExit(0 if all(c==0 for c in codes) else 1)
    if a.mode=='web':
        code=run('web');export('web');raise SystemExit(code)
    raise SystemExit(overall())
