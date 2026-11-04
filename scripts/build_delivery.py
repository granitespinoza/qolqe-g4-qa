"""Genera trazabilidad y una presentación ligera desde evidencia real; nunca fabrica runs."""
import argparse
import csv
import io
from collections import Counter
import json
import os
import re
from pathlib import Path
from delivery_portal import render
from diagnose_api import parse_karate, diagnose_schemathesis
from qa_provenance import validate

ROOT=Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


def build():
    matrix=load(ROOT/'data/matriz-parte2.json')
    web_path=ROOT/'data/parte2-web-verificacion.json'
    web=load(web_path) if web_path.exists() else None
    current=(os.environ.get('GITHUB_SERVER_URL','https://github.com')+'/'+os.environ['GITHUB_REPOSITORY']+'/actions/runs/'+os.environ['GITHUB_RUN_ID']) if os.environ.get('GITHUB_RUN_ID') else None
    manifests={}
    missing=[]
    api_rows=[]
    contract=None
    for tool in ('karate','schemathesis'):
        path=ROOT/f'reports/latest-{tool}.json'
        if not path.exists():
            missing.append(tool);continue
        m=load(path)
        if current and (m.get('github_run_url')!=current or m.get('qa_revision')!=os.environ.get('GITHUB_SHA')):
            missing.append(f'{tool}: evidencia ajena a este run');continue
        folder=validate(m)
        manifests[tool]={k:m.get(k) for k in ('run_id','started_at','finished_at','exit_code','qa_revision','qa_worktree_dirty','github_run_url','report_dir','reference_commit')}
        if tool=='karate':
            if m.get('tag') or m.get('scope')!='all': raise ValueError('Se requiere Karate completo')
            api_rows=parse_karate(folder)
        else:
            contract=diagnose_schemathesis(path)
    if web and current and any(r.get('pipelineUrl')!=current or r.get('revision')!=os.environ.get('GITHUB_SHA') for r in web['runs']):
        missing.append('cypress: evidencia ajena a este run');web=None
    if web:
        raw=load(ROOT/web['evidence'])
        if web['source_hash']!=raw['sourceFingerprint']['hash']:raise ValueError('Huella web inconsistente')
        if len(raw['runs'])!=3 or not raw['verdict']['sameTests'] or not raw['verdict']['sameSources'] or not raw['verdict']['completeSuite']:
            raise ValueError('La evidencia no corresponde a tres suites completas de las mismas fuentes')
    else: missing.append('cypress')
    tests={t['id']:t for t in web['tests']} if web else {}
    gate_api=load(ROOT/'reports/gate/karate.json') if (ROOT/'reports/gate/karate.json').exists() else {}
    gate_web=load(ROOT/'reports/gate/web.json') if (ROOT/'reports/gate/web.json').exists() else {}
    gate_overall=load(ROOT/'reports/gate/overall.json') if (ROOT/'reports/gate/overall.json').exists() else {}
    api_gate={t['case']:t for t in gate_api.get('tests',[])}
    web_gate={t['case']:t for t in gate_web.get('tests',[])}
    flat=[]
    criteria=[]
    for c in matrix['criteria']:
        api_cases=[]
        for case in c['api_cases']+c['api_supplemental_cases']:
            rows=[r for r in api_rows if case['id'] in r['cases']]
            api_cases.append(dict(**case,results=[{k:r[k] for k in ('key','name','status')} for r in rows],
                                  status='sin ejecución' if not rows else 'failed' if any(r['status']=='failed' for r in rows) else 'passed' if all(r['status']=='passed' for r in rows) else 'skipped'))
        groups={g['id'] for g in c['planned_web_cases']}
        linked=[t for t in tests.values() if groups.intersection(t['groups']) or t['id'] in c['existing_web_cases']]
        for case in api_cases:
            actual=[r for r in api_rows if case['id'] in r['cases']]
            classified=[api_gate.get(r['key'],{}) for r in actual]
            defects=sorted({r['defect'] for r in classified if r.get('defect')})
            status='PASA' if case['status']=='passed' else 'FALLA / KNOWN ISSUE' if classified and all(r.get('status') in ('passed','known_issue') for r in classified) else 'FALLA DESCONOCIDA' if actual else 'SIN EJECUCIÓN'
            flat.append(dict(hu=c['hu'],tc='TC-'+case['id'],scenario=actual[0]['name'] if actual else case['id'],layer='API',tags=sorted({t for r in actual for t in r.get('tags',[])}),state=status,defects=defects,file=case['file']))
        for test in linked:
            g=web_gate.get(test['id'],{})
            states=[r['state'] for r in test['results']]
            status='PASA' if all(x=='passed' for x in states) else 'FLAKY' if g.get('status')=='flaky' else 'FALLA / KNOWN ISSUE' if g.get('status')=='known_issue' else 'FALLA DESCONOCIDA'
            flat.append(dict(hu=c['hu'],tc='TC-'+test['id'],scenario=test['title'].split('|')[-1].strip(),layer='Web',tags=sorted(set(re.findall(r'@[A-Za-z0-9_-]+',test['title']))),state=status,defects=[g['defect']] if g.get('defect') else [],file=test['file']))
        criteria.append(dict(id=c['id'],title=c['title'],api=api_cases,web=linked,
                             web_status='sin ejecución' if not linked else 'passed' if all(r['state']=='passed' for t in linked for r in t['results']) else 'failed'))
    # También se trazan las pruebas del núcleo ejecutadas como dependencias compartidas.
    present={r['tc'] for r in flat if r['layer']=='API'}
    for ident in sorted({case for r in api_rows for case in r['cases']}):
        if 'TC-'+ident in present:continue
        actual=[r for r in api_rows if ident in r['cases']]
        classified=[api_gate.get(r['key'],{}) for r in actual]
        tags=sorted({t for r in actual for t in r.get('tags',[])})
        hus=[t[1:] for t in tags if t.startswith('@HU-')]
        defects=sorted({r['defect'] for r in classified if r.get('defect')})
        state='PASA' if all(r['status']=='passed' for r in actual) else 'FALLA / KNOWN ISSUE' if all(r.get('status') in ('passed','known_issue') for r in classified) else 'FALLA DESCONOCIDA'
        flat.append(dict(hu=', '.join(hus),tc='TC-'+ident,scenario=actual[0]['name'],layer='API',tags=tags,state=state,defects=defects,file=actual[0]['file'],selection='núcleo compartido',variants=[{'key':r['key'],'status':r['status'],'gate_status':api_gate.get(r['key'],{}).get('status')} for r in actual]))
    result=dict(scope=matrix['scope'],pipeline_url=current,missing=missing,api_runs=manifests,
                api_counts=dict(Counter(r['status'] for r in api_rows)),web_runs=web['runs'] if web else [],
                web_verdict=web['verdict'] if web else None,contract=contract,criteria=criteria,
                matrix=flat,gate=gate_overall,note='La evidencia local combina fechas distintas y no representa un pipeline remoto. Schemathesis es complemento de contrato; sus peticiones aleatorias no se asignan a CA como casos diseñados.')
    lines=['# Trazabilidad de la entrega — Parte 2','',result['scope'],'',
           f"Ejecución de GitHub: {current or '**pendiente; evidencia local**'}.",'',result['note'],'',
           '## HU → CA → casos → ejecución','', '| Criterio | API (caso: resultado) | Web (caso: corridas 1/2/3) |','|---|---|---|']
    for c in criteria:
        a='; '.join(f"{x['id']}: {x['status']}" for x in c['api']) or 'sin casos'
        w='; '.join(f"{t['id']}: {'/'.join(r['state'] for r in t['results'])}" for t in c['web']) or 'sin ejecución'
        lines.append(f"| {c['id']} | {a} | {w} |")
    lines+=['','## Reportes y procedencia','']
    for tool,m in manifests.items():
        target=f"{m['report_dir']}/"+('karate-summary.html' if tool=='karate' else 'schemathesis-detallado.html')
        lines.append(f"- {tool}: `{m['run_id']}`, salida `{m['exit_code']}`. [Reporte](../../{target}). Run remoto: {m['github_run_url'] or 'no existe para esta ejecución local'}.")
    if web:
        for i,r in enumerate(web['runs'],1):lines.append(f"- Cypress {i}: `{r['started']}`, `{r['counts']}`. [Reporte](../../{r['runDir']}/html/index.html). Run remoto: {r.get('pipelineUrl') or 'local'}.")
    lines+=['','Los resultados API de un escenario parametrizado conservan sus variantes en el JSON. Un caso solo figura passed cuando todas sus variantes ejecutadas pasan. La tabla por criterio se limita a 18 CA G4. La matriz exigida también incluye todos los casos API del núcleo compartido y sus variantes ejecutadas.','',
            'Regenerar: `python scripts/build_delivery.py`. En CI se descargan y combinan los artefactos de los tres trabajos de esta misma ejecución. Una evidencia de otro run se informa como ausente.','',
            f"Evidencia ausente: {', '.join(missing) or 'ninguna herramienta; los resultados locales no sustituyen al run remoto'}. Horas y revisiones están en el [JSON](../../data/trazabilidad-parte2.json).",'']
    lines += ['', '## Matriz exigida por la docente', '', '| HU | TC | Escenario | Capa | Tags en código | Estado de prueba en pipeline | Defecto asociado |', '|---|---|---|---|---|---|---|']
    for row in flat:
        lines.append('| '+' | '.join([row['hu'],row['tc'],row['scenario'].replace('|','/'),row['layer'],' '.join(row['tags']),row['state'],', '.join(row['defects']) or 'N/A'])+' |')
    lines += ['', f"Quality Gate: **{gate_overall.get('scenario','pendiente')}**, aprobado: **{gate_overall.get('approved',False)}**. Los FAIL crudos no se cambian a PASS.", '', '[Defectos y riesgos](defectos-conocidos.md) · [Política del gate](quality-gate.md)', '']
    return result,'\n'.join(lines)


if __name__=='__main__':
    p=argparse.ArgumentParser()
    modes=p.add_mutually_exclusive_group()
    modes.add_argument('--check',action='store_true')
    modes.add_argument('--snapshot',action='store_true',help='Regenerar solo el portal desde la matriz histórica versionada')
    a=p.parse_args()
    if a.snapshot:
        (ROOT/'apidoc/parte2/index.html').write_text(
            render(load(ROOT/'data/trazabilidad-parte2.json'), snapshot=True), encoding='utf-8')
        raise SystemExit(0)
    data,md=build()
    outputs={'data/trazabilidad-parte2.json':json.dumps(data,ensure_ascii=False,indent=2)+'\n','docs/parte2/trazabilidad.md':md,'apidoc/parte2/index.html':render(data)}
    csv_buffer=io.StringIO(newline='');writer=csv.writer(csv_buffer,lineterminator="\n")
    writer.writerow(['HU','TC','Escenario','Capa','Tags en código','Estado en pipeline','Defecto asociado'])
    for row in data['matrix']:writer.writerow([row['hu'],row['tc'],row['scenario'],row['layer'],' '.join(row['tags']),row['state'],', '.join(row['defects']) or 'N/A'])
    outputs['data/trazabilidad-parte2.csv']=csv_buffer.getvalue()
    outputs['results/reporte-final.html']=outputs['apidoc/parte2/index.html'].replace('<title>', '<base href="../apidoc/parte2/"><title>',1)
    for name,content in outputs.items():
        path=ROOT/name
        if a.check:
            if not path.exists() or path.read_text(encoding='utf-8')!=content:raise SystemExit('Desactualizado: '+name)
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content,encoding='utf-8')
    print('Trazabilidad generada; evidencia ausente:',data['missing'])
    if data['missing']:raise SystemExit(2)
