"""Relaciona el diseño web con tres ejecuciones reales, sin convertir fallos en aprobaciones."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def build():
    matrix = json.loads((ROOT / 'data/matriz-parte2.json').read_text(encoding='utf-8'))
    latest = json.loads((ROOT / 'reports/cypress/latest-stability.json').read_text())
    evidence_path = ROOT / latest['dir'] / 'stability.json'
    evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
    runs = evidence['runs']
    for name, expected in evidence['sourceFingerprint']['files'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, f'Fuente modificada desde la evidencia: {name}'
    assert len(runs) == 3, 'Se necesitan tres ejecuciones completas'
    planned = {g['id'] for c in matrix['criteria'] for g in c['planned_web_cases']}
    gate_path=ROOT/'reports/gate/web.json'
    gate=json.loads(gate_path.read_text(encoding='utf-8')) if gate_path.exists() else {}
    if gate.get('report_dir')!=latest['dir']:gate={}
    gate_by_id={t['case']:t for t in gate.get('tests',[])}
    tests = {}
    for n, run in enumerate(runs):
        seen = set()
        for test in run['tests']:
            title = ' '.join(test['title'])
            match = re.search(r'E2E-G4-\d+', title)
            assert match, f'Caso sin ID: {title}'
            key = match.group()
            assert key not in seen, f'ID repetido: {key}'
            seen.add(key)
            groups = sorted(set(re.findall(r'WEB-G4-\d+-CA\d+-\d+', title)))
            assert set(groups) <= planned, f'Grupo desconocido: {groups}'
            entry = tests.setdefault(key, dict(id=key, title=title, file=test['spec'], groups=groups, results=[]))
            assert entry['title'] == title and entry['file'] == test['spec'], 'Cambió la selección entre corridas'
            error = test.get('error') or ''
            entry['results'].append(dict(run=n+1, state=test['state'], error=error.split('\n')[0]))
    assert all(len(t['results']) == 3 for t in tests.values()), 'Selecciones incompletas'
    covered = {g for t in tests.values() for g in t['groups']}
    assert covered == planned, f'Grupos sin pruebas: {planned-covered}'
    criteria = []
    for c in matrix['criteria']:
        group_ids = {g['id'] for g in c['planned_web_cases']}
        linked = sorted(t['id'] for t in tests.values() if group_ids.intersection(t['groups']))
        passed = all(r['state'] == 'passed' for key in linked for r in tests[key]['results'])
        criteria.append(dict(id=c['id'], groups=sorted(group_ids), tests=linked,
                             status='aprobado en 3 corridas' if passed else 'Escenario A: fallo conocido' if linked and all(gate_by_id.get(k,{}).get('status') in ('passed','known_issue') for k in linked) else 'bloqueado por fallos'))
    result = dict(scope='G4 aprobado: 18 CA y 36 grupos de variantes; no todos los módulos Qolqe',
                  evidence=evidence_path.relative_to(ROOT).as_posix(),
                  evidence_sha256=hashlib.sha256(evidence_path.read_bytes()).hexdigest(),
                  source_hash=evidence['sourceFingerprint']['hash'], verdict=evidence['verdict'],
                  criteria=criteria, tests=list(tests.values()),gate=gate,
                  runs=[{k:r[k] for k in ('runDir','started','ended','code','counts','sutRevision','browser','revision','worktreeDirty','pipelineUrl')} for r in runs])
    lines = ['# Pasos 3 y 4 — cobertura y verificación web', '',
             'Resultado local, generado desde tres ejecuciones reales. No acredita un pipeline de GitHub ni una entrega completa.', '',
             f"Implementados: **{len(tests)} tests**, **{len(planned)} grupos de variantes**, **{len(criteria)} CA G4**.", '',
             'Un grupo puede tener varios tests y un test varias aserciones. Si falla una aserción, las siguientes no se ejecutan; por eso presencia de código no implica aprobación del criterio.', '',
             f"Tres corridas sin fallos crudos: **{'SÍ' if evidence['verdict']['achieved'] else 'NO'}**. Quality Gate: **{gate.get('scenario','pendiente')}**, aprobado: **{gate.get('approved',False)}**.", '',
             '| Corrida | Aprobados | Fallidos | Omitidos/pendientes | Reporte local |', '|---|---:|---:|---:|---|']
    for n,r in enumerate(runs,1):
        c=r['counts']
        lines.append(f"| {n} | {c['passed']} | {c['failed']} | {c['skipped']+c['pending']} | [HTML](../../{r['runDir']}/html/index.html) |")
    lines += ['', f"Huella común: `{result['source_hash']}`.", '',
              f"SUT: `{runs[0]['sutRevision']}`. Base de datos independiente por corrida (eliminada al terminar para ahorrar disco), navegador `{runs[0]['browser']}`, reintentos de tests: 0.", '',
              'Las fuentes aún pueden estar sin commit; el manifiesto registra `worktreeDirty` y hashes SHA-256 por archivo. Esta evidencia no debe atribuirse únicamente al commit HEAD.', '',
              f"[Manifiesto detallado local](../../{result['evidence']}) · [Resumen versionable](../../data/parte2-web-verificacion.json). Los reportes y vídeos están ignorados por Git; compartirlos requiere adjuntarlos o publicarlos en el paso de CI.", '',
              '## Criterios', '', '| Criterio | Tests relacionados | Resultado |', '|---|---|---|']
    for c in criteria:
        lines.append(f"| {c['id']} | {', '.join(c['tests'])} | {c['status']} |")
    lines += ['', '## Resultados por prueba', '', '| ID | Corrida 1 / 2 / 3 | Archivo |', '|---|---|---|']
    for t in tests.values():
        lines.append(f"| {t['id']} | {' / '.join(r['state'] for r in t['results'])} | [{Path(t['file']).name}](../../{t['file']}) |")
    lines += ['', '## Fallos observados', '']
    for t in tests.values():
        errors = sorted({r['error'] for r in t['results'] if r['state'] != 'passed'})
        if errors:
            lines.append(f"- **{t['id']}**: " + '; '.join(e.replace('`', "'") for e in errors))
    lines += ['', '## Reproducir', '', 'Desde la raíz del repositorio, PowerShell:', '', '```powershell',
              'powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 typecheck',
              '$env:CY_BROWSER = "chrome"',
              'powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 regression',
              'powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 stability',
              '.venv/Scripts/python.exe scripts/build_web_coverage.py',
              'powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report',
              '```', '',
              'El servidor y las bases de pruebas se preparan automáticamente; deja libre el puerto 8011. `stability` ejecuta la regresión tres veces y devuelve código 1 si alguna falla. No editar fuentes durante la secuencia. La demo IA y el fallo didáctico están fuera de la regresión.', '',
              '[Diagnóstico y justificación de los fallos](diagnostico-web.md).', '', '## Mantenibilidad y límites', '',
              '- Page Object Model: ContactosPage, SolicitudesPage, TransferenciasPage y LoginPage encapsulan selectores y acciones. Las especificaciones conservan resultados esperados de negocio.',
              '- Se esperan respuestas reales con interceptores sin stubs, elementos visibles y estados DOM. No hay `cy.wait(ms)` ni reintentos de pruebas para forzar aprobaciones.',
              '- Las fixtures crean actores independientes por prueba; solo la disponibilidad de los datos y sesiones de preparación admite sondeos acotados. Las operaciones funcionales y financieras no se reintentan.',
              '- Las fronteras temporales usan el reloj de pruebas del servidor; cada test lo restablece. La suite debe seguir secuencial porque comparte ese reloj.',
              '- El veredicto crudo exige cero fallos. El Quality Gate independiente exige mismas fuentes, suite completa, sin omisiones, sin inestabilidad y únicamente fallos conocidos admitidos para el contexto académico.',
              '- Se mantiene la referencia original sin modificar. Los defectos del producto se conservan como FAIL. La aprobación académica se comunica como Escenario A; nunca como 100% de pruebas aprobadas.',
              '- Pipeline y matriz consolidada implementados. Ver [guía de ejecución](entrega.md) y [política del Quality Gate](quality-gate.md). La ejecución remota debe comprobarse después de publicar los cambios.', '']
    return {'data/parte2-web-verificacion.json':json.dumps(result,ensure_ascii=False,indent=2)+'\n',
            'docs/parte2/verificacion-web.md':'\n'.join(lines)}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    for name,content in build().items():
        path=ROOT/name
        if args.check:
            assert path.read_text(encoding='utf-8')==content, f'Desactualizado: {name}'
        else:
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text(content,encoding='utf-8')
    print('Cobertura: 18 CA, 36 grupos y resultados de tres ejecuciones vinculados.')
