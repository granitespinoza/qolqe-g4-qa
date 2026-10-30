"""Publica peticiones reales y checks correlacionados, con secretos ocultos.

No consume la API ni modifica los resultados. Soporta reportes NDJSON/HAR de
Schemathesis 4.17.0. Las categorías proceden de metadatos, no de nombres de tests.
"""
import argparse
import base64
from collections import Counter, defaultdict
import html
import json
import os
from pathlib import Path
import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
JWT = re.compile(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+')
SECRET = re.compile(r'authorization|cookie|password|contrase|(^|[_-])pin($|[_-])|token|api[_-]?key', re.I)


def redact(value):
    if isinstance(value, dict):
        return {str(k): '[OCULTO]' if SECRET.search(str(k)) else redact(v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact(v) for v in value]
    if isinstance(value, str):
        return JWT.sub('[JWT OCULTO]', value)
    return value


def body(value):
    if isinstance(value, dict) and '$base64' in value:
        decoded = base64.b64decode(value['$base64']).decode('utf-8', errors='replace')
        try:
            return redact(json.loads(decoded))
        except (ValueError, TypeError):
            return redact(decoded)
    return redact(value)


def url(value):
    parts = urlsplit(value)
    query = [(k, '[OCULTO]' if SECRET.search(k) else redact(v)) for k, v in parse_qsl(parts.query, keep_blank_values=True)]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))


def category(value, parent):
    # Una sonda de autenticación puede heredar los metadatos del caso padre.
    # Priorizar el cambio de credencial evita atribuir esa sonda al campo del padre.
    if parent:
        original_auth = parent.get('headers', {}).get('Authorization')
        child_auth = value.get('headers', {}).get('Authorization')
        if original_auth and (child_auth is None or child_auth == 'SCHEMATHESIS-INVALID-VALUE'):
            return 'auth', 'Relación padre-hijo y credencial retirada o inválida'
    meta = value.get('meta', {})
    data = meta.get('phase', {}).get('data', {})
    location = data.get('location', '')
    scenario = data.get('scenario', '')
    if data.get('parameter', '').lower() == 'authorization' or '/properties/Authorization' in location:
        return 'auth', 'Metadatos: parámetro Authorization'
    if scenario == 'incorrect_type' or location.endswith('/type'):
        return 'type', 'Metadatos: incorrect_type o puntero /type'
    if scenario in ('string_above_max_length', 'string_below_min_length') or location.endswith(('/maxLength', '/minLength')):
        return 'length', 'Metadatos: límite de longitud'
    if scenario == 'invalid_pattern' or location.endswith('/pattern'):
        return 'pattern', 'Metadatos: patrón'
    if scenario in ('near_boundary_number', 'value_below_minimum', 'value_above_maximum') or location.endswith(('/minimum', '/maximum', '/exclusiveMinimum', '/exclusiveMaximum')):
        return 'range', 'Metadatos: frontera numérica o restricción de mínimo/máximo'
    if scenario in ('enum_value', 'invalid_enum_value') or location.endswith('/enum'):
        return 'enum', 'Metadatos: valor permitido o excluido de una enumeración'
    if scenario in ('object_missing_required_property', 'missing_parameter') or location.endswith('/required'):
        return 'required', 'Metadatos: propiedad o parámetro obligatorio omitido'
    return 'sin categoría demostrada', 'Sin metadatos suficientes para atribuir una validación concreta'


def build(manifest_path, output_dir):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    directory = (ROOT / manifest['report_dir']).resolve()
    if not directory.is_relative_to((ROOT/'reports/raw').resolve()):
        raise SystemExit('El reporte fuente debe estar dentro de reports/raw.')
    ndjson_path = next(directory.glob('ndjson*.ndjson'))
    har_path = next(directory.glob('har*.json'))
    events = [json.loads(line) for line in ndjson_path.read_text(encoding='utf-8').splitlines()]
    entries = json.loads(har_path.read_text(encoding='utf-8'))['log']['entries']
    by_id = defaultdict(list)
    for number, entry in enumerate(entries):
        for header in entry['request']['headers']:
            if header['name'].lower() == 'x-schemathesis-testcaseid':
                by_id[header['value']].append((number, entry))
    controls = {c['case_id'] for c in json.loads((directory/'controles-contexto.json').read_text(encoding='utf-8'))} if (directory/'controles-contexto.json').exists() else set()
    rows = []
    matched = set()
    cases_without_interaction = 0
    for event in events:
        if 'ScenarioFinished' not in event:
            continue
        execution = event['ScenarioFinished']
        recorder = execution['recorder']
        cases = recorder.get('cases', {})
        cases_without_interaction += len(set(cases)-set(recorder.get('interactions', {})))
        for case_id, interaction in recorder.get('interactions', {}).items():
            case = cases.get(case_id, {})
            value = case.get('value', {})
            parent_id = case.get('parent_id')
            parent = cases.get(parent_id, {}).get('value', {})
            request = interaction['request']
            response = interaction.get('response')
            har_candidates = by_id.get(case_id, [])
            # Igual ID + método + URL + estado: correlación verificable.
            candidates = [(n, e) for n, e in har_candidates if e['request']['method'] == request['method'] and e['request']['url'] == request['uri'] and e['response']['status'] == (response or {}).get('status_code')]
            correlation = 'NDJSON: interacción y checks por mismo case_id'
            if len(candidates) == 1:
                matched.add(candidates[0][0])
                correlation += '; HAR: mismo ID, método, URL y estado'
            else:
                correlation += '; HAR sin coincidencia única completa'
            checks = recorder.get('checks', {}).get(case_id, [])
            outcome = 'fallo de check' if any(c['status'] == 'failure' for c in checks) else 'checks registrados sin fallo' if checks else 'sin checks propios registrados'
            group, reason = category(value, parent)
            rows.append({'case_id': case_id, 'parent_id': parent_id, 'phase': execution['phase'],
                'origin': 'control de contexto' if case_id in controls else 'petición auxiliar vinculada' if parent_id else 'caso de Schemathesis',
                'operation': recorder['label'], 'method': request['method'], 'url': url(request['uri']),
                'path_template': value.get('path'), 'category': group, 'category_evidence': reason,
                'metadata': redact(value.get('meta')), 'request_headers': redact(request.get('headers', {})),
                'request_body': body(request.get('body')), 'status': response.get('status_code') if response else None,
                'response_headers': redact(response.get('headers', {})) if response else {},
                'response_body': body(response.get('content')) if response else None,
                'elapsed_seconds': response.get('elapsed') if response else None,
                'checks': redact(checks), 'outcome': outcome, 'correlation': correlation})
    summary = {'run_id': manifest['run_id'], 'started_at': manifest['started_at'],
        'finished_at': manifest.get('finished_at'), 'ndjson_interactions': len(rows),
        'har_entries': len(entries), 'har_correlated': len(matched),
        'har_not_correlated': len(entries)-len(matched),
        'cases_without_recorded_interaction': cases_without_interaction,
        'check_failure_occurrences': sum(c['status']=='failure' for row in rows for c in row['checks']),
        'requests_with_check_failure': sum(row['outcome']=='fallo de check' for row in rows),
        'requests_without_own_checks': sum(not row['checks'] for row in rows),
        'categories': dict(Counter(row['category'] for row in rows)),
        'limitations': ['Los totales describen peticiones y checks registrados; no acreditan cobertura completa de requisitos.',
            'Una respuesta 4xx puede ser correcta. Un check sin fallo no demuestra todos los criterios del endpoint.',
            'Las peticiones auxiliares pueden evaluarse en los checks del padre y no tener checks propios.',
            'Las categorías solo se asignan con metadatos o relación de autenticación registrada; sin evidencia se indica sin categoría demostrada.',
            'Los fallos de checks repetidos no equivalen al número de señales únicas ni a defectos confirmados.']}
    result = {'summary': summary, 'requests': rows}
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir/'schemathesis-detallado.json'
    serialized = json.dumps(result, ensure_ascii=True, indent=2)
    # Verificación de publicación: no debe sobrevivir ningún JWT reconocible.
    if JWT.search(serialized):
        raise SystemExit('Se detectó un JWT en el resultado; no se publica.')
    output_json.write_text(serialized, encoding='utf-8')
    template = Path(__file__).with_name('schemathesis_report_template.html').read_text(encoding='utf-8')
    interpretation_link = os.path.relpath(ROOT/'docs/revision-contrato.md', output_dir).replace('\\', '/')
    template = template.replace('../docs/revision-contrato.md', interpretation_link)
    embedded = serialized.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    (output_dir/'schemathesis-detallado.html').write_text(template.replace('/*DATA*/null', embedded), encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', default='reports/latest-schemathesis.json')
    parser.add_argument('--output-dir', default='reports')
    arguments = parser.parse_args()
    build((ROOT/arguments.manifest).resolve(), (ROOT/arguments.output_dir).resolve())
