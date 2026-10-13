"""Documentación y resultados se generan desde fuentes reales, sin completar huecos."""
from pathlib import Path
import datetime, hashlib, html, json, re, subprocess
from zoneinfo import ZoneInfo
from qa_provenance import validate

ROOT=Path(__file__).resolve().parents[1]
def write(p,s):
    p=ROOT/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def redact(s):
    return re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+','<TOKEN_OCULTO>',s)
def build():
    manifest=json.loads((ROOT/'reports/latest-karate.json').read_text(encoding='utf-8'))
    report_dir=validate(manifest)
    commit=subprocess.check_output(['git','-C',str(ROOT/'referencias/qolqe-wallet'),'rev-parse','HEAD'],text=True).strip()
    source=(ROOT/'referencias/qolqe-wallet/docs/requisitos.md').read_text(encoding='utf-8')
    cases=json.loads((ROOT/'data/casos.json').read_text(encoding='utf-8'))
    if not (report_dir/'openapi.json').is_file():raise SystemExit('Falta el reporte local de esa ejecución. Ejecuta scripts/run_qa.py karate antes de regenerar documentación.')
    schema_bytes=(report_dir/'openapi.json').read_bytes()
    if hashlib.sha256(schema_bytes).hexdigest()!=manifest['openapi_sha256']:raise SystemExit('El snapshot OpenAPI cambió después de la ejecución')
    schema=json.loads(schema_bytes)
    write('data/openapi-original.json',json.dumps(schema,ensure_ascii=False,indent=2))
    results={}
    for p in report_dir.glob('features.*.json'):
        features=json.loads(p.read_text(encoding='utf-8'))
        # Los adjuntos JSON de Karate (por ejemplo concurrencia) no son reportes Cucumber.
        if not isinstance(features,list): continue
        for feature in features:
            if not isinstance(feature,dict) or feature.get('keyword')!='Feature':continue
            for e in feature.get('elements',[]):
                tags=[t['name'].lstrip('@') for t in e.get('tags',[])]
                case_id=next((t for t in tags if re.fullmatch('G4-\\d+',t)),None)
                if not case_id: continue
                steps=e.get('steps',[])
                failed=[s for s in steps if s.get('result',{}).get('status')=='failed']
                skipped=any(s.get('result',{}).get('status')=='skipped' for s in steps)
                status='FALLÓ' if failed else ('PENDIENTE' if skipped else 'APROBADO')
                error=redact(failed[0]['result'].get('error_message','')) if failed else ''
                design=next((c for c in cases if c['id']==case_id),None)
                first=next((i for i,s in enumerate(steps) if design and s.get('name')==design['steps'][0]),0)
                logs='\n'.join(redact(s.get('doc_string',{}).get('value','')) for s in steps[first:])
                results[case_id]={'status':status,'error':error,'feature':feature['uri'],'name':e.get('name',''),'failed_step':failed[0]['name'] if failed else '', 'failure_phase':'preparacion' if failed and steps.index(failed[0])<first else ('asercion' if failed else None)}
                evidence=f'<html lang="es"><meta charset="utf-8"><title>{case_id}</title><style>body{{font:15px Segoe UI;margin:40px;background:#faf9f5;color:#172b29}}pre{{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf0e8;padding:20px}}</style><h1>{case_id} · {html.escape(e.get("name",""))}</h1><p>Resultado: {status} · Karate 1.5.2 · referencia {commit[:12]}</p><p>Registro real de ejecución; tokens ocultos.</p><pre>{html.escape(error)}</pre><pre>{html.escape(logs)}</pre></html>'
                write(f'evidencias/{case_id}.html',evidence)
    stats={'executed':sum(r['status']!='PENDIENTE' for r in results.values()),'passed':sum(r['status']=='APROBADO' for r in results.values()),'failed':sum(r['status']=='FALLÓ' for r in results.values())}
    findings=[]
    registry=json.loads((ROOT/'data/defectos-confirmados.json').read_text(encoding='utf-8'))
    for reviewed in registry:
        r=results.get(reviewed['case'],{})
        reproduced=(r.get('status')=='FALLÓ' and r.get('failure_phase')=='asercion' and r.get('failed_step')==reviewed['expected_failed_step'] and 'match failed' in r.get('error',''))
        if reproduced:
            findings.append({**reviewed,'classification':'Defecto revisado; reproducido en esta ejecución'})
    operations=[]
    paths=['/api/contactos','/api/solicitudes','/api/transferencias','/api/auth','/api/cuentas','/api/usuarios']
    for path,methods in schema['paths'].items():
        if not any(path.startswith(p) for p in paths):continue
        for method,op in methods.items():
            if method not in ['get','post','put','delete','patch']:continue
            id=re.sub('[^a-z0-9]+','-',method+'-'+path.lower()).strip('-')
            curl=f"curl -X {method.upper()} 'http://localhost:8000{path}'"
            if op.get('security'):curl+=" \\\n  -H 'Authorization: Bearer <TOKEN>'"
            body=op.get('requestBody',{}).get('content',{}).get('application/json')
            if body:
                sample=body.get('example') or next((x['value'] for x in body.get('examples',{}).values() if 'value' in x),{})
                curl+=" \\\n  -H 'Content-Type: application/json' \\\n  --data '"+json.dumps(sample,ensure_ascii=False)+"'"
            operations.append(dict(id=id,path=path,method=method,operation=op,curl=curl))
    stamp=datetime.datetime.fromisoformat(manifest['finished_at']).astimezone(ZoneInfo('America/Lima')).isoformat(timespec='seconds')
    data=dict(commit=commit,timestamp=stamp,cases=cases,results=results,stats=stats,findings=findings,operations=operations,openapi=schema)
    write('apidoc/data.js','window.QA_DATA = '+json.dumps(data,ensure_ascii=False)+';\n')
    write('reports/resultados.json',json.dumps(dict(timestamp=stamp,commit=commit,stats=stats,results=results,findings=findings),ensure_ascii=False,indent=2))
    # Cada CA permanece visible, incluidos los que solo tienen cobertura parcial.
    hu_blocks=re.findall(r'### (HU-(?:G4|N)-\d+) · ([^\n]+)\n(.*?)(?=\n### |\n---|\Z)',source,re.S)
    lines=['# Cobertura por criterio','', 'Los casos asociados demuestran presencia de pruebas, no cobertura exhaustiva. Un CA compuesto puede requerir variantes adicionales.','', '| HU / CA | Pruebas asociadas | Estado de diseño |','|---|---|---|']
    for hu,title,body in hu_blocks:
        for num in re.findall(r'\*\*CA(\d+)\.',body):
            matches=[c['id'] for c in cases if c['hu']==hu and int(num) in c['ca']]
            lines.append(f'| {hu} CA{num} | {", ".join(matches) or "—"} | {"Pruebas presentes; revisar variantes" if matches else "PENDIENTE: sin escenario específico"} |')
    lines+=['','## Pendientes transversales','- Ampliar concurrencia a aceptación simultánea de solicitudes.','- Completar variantes de destino cerrado y permisos en cada flujo financiero.','- Ampliar filtros de solicitudes a cada estado y verificar su contenido.','- Validar contenido exacto de todos los SMS, no solo su presencia.','- CI: revisar resultados del workflow; la ejecución local no sustituye el pipeline.','- Web y rendimiento corresponden a entregas posteriores.']
    write('docs/cobertura.md','\n'.join(lines)+'\n')
    lines=['# Diseño de pruebas','', '## Método','Para cada caso mantenemos las demás entradas válidas. Los valores límite de dos puntos se aplican a alias; tres puntos a vencimiento. Vacío y espacios se comprueban por separado.','', '| Caso | HU / CA | Regla | Técnica | Por qué | Resultado |','|---|---|---|---|---|---|']
    for c in cases:lines.append(f'| {c["id"]} | {c["hu"]} CA{", CA".join(map(str,c["ca"]))} | {c["rule"]} | {c["technique"]} | {c["why"]} | {results.get(c["id"],{}).get("status","PENDIENTE")} |')
    for hu,title,body in hu_blocks:
        lines+=['',f'## {hu} — {title}','',body.strip(),'']
        for c in [c for c in cases if c['hu']==hu]:
            lines += [f'### {c["id"]} — {c["title"]}',f'**Técnica:** {c["technique"]}. **Justificación:** {c["why"]}',f'**Regla:** {c["rule"]}. **Resultado:** {results.get(c["id"],{}).get("status","PENDIENTE")}.',f'[Escenario](../features/{hu.lower()}.feature) · [Evidencia](../evidencias/{c["id"]}.html)','```gherkin']+['* '+s for s in c['steps']]+['```','']
    write('docs/diseno-pruebas.md','\n'.join(lines))
    lines=['# Defectos reproducidos','',f'Aplicación original: `{commit}`. No se modificó su código.','']
    for f in findings:
        c=next(c for c in cases if c['id']==f['case'])
        lines += [f'## {f["id"]} — {f["title"]}',f'**Clasificación:** {f["classification"]}. **Requisito:** {c["hu"]}, {c["rule"]}.',f'**Descripción:** {f["description"]}',f'**Reproducción automatizada:** ejecutar Karate con etiqueta `@{c["id"]}`. El escenario prepara sus propios usuarios.',f'**Esperado y pasos:** [feature](../features/{c["hu"].lower()}.feature).',f'**Obtenido:** [registro HTTP real](../evidencias/{c["id"]}.html).','```text',results[c['id']]['error'],'```','']
    lines+=['## Clasificación pendiente','Los demás fallos se investigan por separado: no se atribuyen automáticamente a la aplicación. La implementación puede confirmar una hipótesis de causa, pero no reemplaza la reproducción HTTP.']
    write('docs/defectos.md','\n'.join(lines))
    write('docs/informe.md',f'''# Informe — Parte 1 · G4 Contactos
Granit Espinoza y Franco · CS5383

## 1. Alcance y decisiones
10 HU de G4 y 9 del núcleo. La suite inicial tiene {len(cases)} escenarios. No se declara cobertura total: consultar [cobertura por CA](cobertura.md).
Referencia: https://github.com/cjudihtroj/qolqe-wallet · commit `{commit}`.
Karate verifica negocio, estados y efectos; Schemathesis explora el contrato. [Decisiones y alternativas](decisiones.md).
Nivel: pruebas HTTP contra la aplicación FastAPI real con SQLite, sin mocks. No representa integración con bancos reales.
[Usabilidad complementaria](usabilidad.md): plan de inspección heurística para la entrega web; no se declara evaluación de interfaz realizada.

## 2. Pruebas de API
[Diseño detallado por HU](diseno-pruebas.md). [Contrato original](../data/openapi-original.json).
Usuarios nuevos por escenario. Reloj global restablecido al comenzar. Ejecución secuencial porque cambiar el reloj afecta toda la aplicación; no se promete paralelismo seguro.
**Última generación de evidencia:** {stamp}.
**Karate:** {stats['executed']} ejecutados; {stats['passed']} aprobados; {stats['failed']} fallaron.
Reporte bruto de esta ejecución: `{manifest['report_dir']}/karate-summary.html`. Registros redactados: [evidencias](../evidencias/).
El número de escenarios aprobados no mide cobertura de criterios ni ausencia de defectos. Cada reporte queda vinculado con commit, huellas de fuentes e inicio/fin de su ejecución; se rechazan resultados desactualizados.
[Schemathesis y límites de la ejecución](revision-contrato.md).

## 3. Pruebas web y CI/CD
Workflow preparado en `.github/workflows/api.yml`, con jobs separados para Karate y contrato. Conserva los reportes aunque una prueba falle. El pipeline debe informar fallos reales.
E2E web pendiente de Parte 2.

## 4. Rendimiento
Pendiente de Parte 3; no se realizó prueba de carga contra servicios públicos.

## 5. Defectos encontrados
{len(findings)} hallazgos funcionales con escenario y evidencia enlazados. [Reproducción](defectos.md).
No se modificó Qolqe ni se ocultaron errores con expectativas ajustadas a su comportamiento.

## 6. Conclusiones y recomendaciones
La suite inicial permite defender técnicas y reproducir fallos. Completar los pendientes por CA antes de afirmar cobertura total o crear el tag de entrega `parte-1`.
La documentación HTML ayuda a localizar pruebas; el análisis se conserva en este informe y el diseño.
''')
    print(json.dumps(stats),f'{len(findings)} hallazgos confirmados registrados')
if __name__=='__main__':build()
