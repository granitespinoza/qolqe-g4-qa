"""Validate and render the Part 2 scope without claiming execution coverage."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def build(root=ROOT):
    scope = json.loads((root/'data/alcance-parte2.json').read_text(encoding='utf-8'))
    source = root/'referencias/qolqe-wallet/docs/requisitos.md'
    requirement_text = source.read_text(encoding='utf-8')
    expected = set()
    hu = None
    for line in requirement_text.splitlines():
        if line.startswith('### HU-'):
            hu = re.search(r'HU-[NG]\w*-\d+', line).group()
        if hu and hu.startswith('HU-G4-'):
            ca = re.match(r'- \*\*CA(\d+)\.', line)
            if ca:
                expected.add(f'{hu}-CA{ca[1]}')
    criteria = scope['criteria']
    ids = [c['id'] for c in criteria]
    if len(ids) != len(set(ids)) or set(ids) != expected:
        raise ValueError(f'Criterios duplicados, faltantes o ajenos: {set(ids) ^ expected}')
    cases = json.loads((root/'data/casos.json').read_text(encoding='utf-8'))
    web_files = {}
    for path in (root/'Web/cypress/e2e').glob('*.cy.ts'):
        for case in re.findall(r'E2E-G4-\d+', path.read_text(encoding='utf-8')):
            web_files[case] = path.relative_to(root).as_posix()
    features = {p.relative_to(root).as_posix(): p.read_text(encoding='utf-8') for p in (root/'API/features').glob('*.feature')}
    planned = set()
    for c in criteria:
        c['api_cases'] = []
        for case in cases:
            if case['hu'] == c['hu'] and c['ca'] in case['ca']:
                paths = [p for p, text in features.items() if re.search(r'@'+re.escape(case['id'])+r'\b', text)]
                if len(paths) != 1:
                    raise ValueError(f"Caso API sin archivo único: {case['id']}")
                c['api_cases'].append({'id':case['id'], 'file':paths[0]})
        c['api_supplemental_cases'] = []
        for path, text in features.items():
            for tags in re.findall(r'^\s*(@[^\n]+)\n\s*Scenario', text, flags=re.M):
                ids_extra = re.findall(r'@(CF-\d+)', tags)
                if ids_extra and '@'+c['hu'] in tags.split() and '@CA'+str(c['ca']) in tags.split():
                    c['api_supplemental_cases'].extend({'id':i,'file':path} for i in ids_extra)
        for case in c['existing_web_cases']:
            if case not in web_files:
                raise ValueError(f'Caso web declarado pero inexistente: {case}')
        c['web_files'] = {case:web_files[case] for case in c['existing_web_cases']}
        for case in c['planned_web_cases']:
            if case['id'] in planned:
                raise ValueError(f"ID de diseño duplicado: {case['id']}")
            planned.add(case['id'])
    scope['requirements_sha256'] = hashlib.sha256(requirement_text.encode('utf-8')).hexdigest()
    scope['requirements_hash_format'] = 'UTF-8 con saltos de linea LF'
    scope['summary'] = {'criteria':len(criteria), 'partial_web':sum(c['web_status']=='parcial' for c in criteria),
        'pending_web':sum(c['web_status']=='pendiente' for c in criteria), 'complete_web':0,
        'existing_web_tests':len({i for c in criteria for i in c['existing_web_cases']}), 'planned_web_groups':len(planned)}
    lines = ['# Alcance y matriz de diseño — línea base del paso 1', '', scope['scope'], '', scope['classification'], '',
        f"Fuente: `referencias/qolqe-wallet/docs/requisitos.md`, commit `{scope['reference_commit']}`.", '',
        '**Presencia de código no significa prueba aprobada ni cobertura completa.** Esta matriz es de diseño; los resultados API están en el diagnóstico. La trazabilidad automática al pipeline corresponde al paso 6.', '',
        'Generar: `python scripts/build_scope.py`. Verificar sin escribir: `python scripts/build_scope.py --check`.', '',
        'Estado posterior de implementación y ejecución: [verificación web de pasos 3–4](verificacion-web.md). Los estados parcial/pendiente siguientes describen la línea base, no el resultado actual.', '', '## Criterios', '', '| HU / CA | Nivel | Casos API existentes | Casos web existentes | Cobertura web |', '|---|---|---|---|---|']
    for c in criteria:
        api = ', '.join(x['id'] for x in c['api_cases']+c['api_supplemental_cases'])
        lines.append(f"| {c['id']} | {c['level']} | {api} | {', '.join(c['existing_web_cases']) or '—'} | {c['web_status']} |")
    lines += ['', '## Diseño web pendiente', '', 'En esta línea base, los identificadores WEB son grupos de variantes planificadas. Su implementación y ejecución posterior se documentan en verificacion-web.md. Cada grupo puede producir varios tests parametrizados. Los tres E2E existentes se reutilizan al implementarlos.', '']
    for c in criteria:
        lines += [f"### {c['id']} — {c['title']}", '', f"Ruta: `{c['route']}`. Complemento API: {c['api_complement']}", '']
        lines += [f"- **{x['id']}**: {x['objective']}." for x in c['planned_web_cases']]
        lines += ['']
    lines += ['## Dependencias del núcleo', '']
    lines += [f"- **{d['hu']} CA{','.join(map(str,d['ca']))}**: {d['role']}." for d in scope['shared_dependencies']]
    lines += ['', '## Límites y criterio de finalización', '', scope['excluded'], '',
        'El SMS se consulta por API de pruebas; no existe un teléfono real en la demo. Concurrencia y peticiones manipuladas se verifican por API. La web debe comprobar la visibilidad de acciones, mensajes, estados y persistencia. Un botón oculto no demuestra autorización del servidor.', '',
        'No se declara ningún CA web completo en esta etapa. Solo se podrá cerrar un criterio tras implementar sus variantes, revisar sus aserciones y asociar resultados reales. La matriz de la docente, si existe una clasificación adicional, prevalece sobre este alcance técnico.', '']
    return {'data/matriz-parte2.json':json.dumps(scope,ensure_ascii=False,indent=2)+'\n',
            'docs/parte2/alcance-y-matriz.md':'\n'.join(lines)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    outputs = build()
    for name, content in outputs.items():
        path = ROOT/name
        if args.check:
            if not path.exists() or path.read_text(encoding='utf-8') != content:
                raise SystemExit(f'Matriz desactualizada: {name}; ejecutar scripts/build_scope.py')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
    print('Alcance validado: 18 CA G4; referencias a casos y archivos verificadas.')
