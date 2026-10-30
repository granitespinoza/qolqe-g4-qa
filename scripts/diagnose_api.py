"""Summarize real API failures. Known defects remain failures (exit 1)."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import xml.etree.ElementTree as ET

from qa_provenance import validate

ROOT = Path(__file__).resolve().parents[1]


def parse_karate(directory):
    rows = []
    for path in sorted(directory.glob('*.json')):
        if path.name in {'execution.json', 'openapi.json'}:
            continue
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, list):
            continue
        for feature in data:
            background_failed = False
            for element in feature.get('elements', []):
                steps = element.get('steps', [])
                if element.get('type') == 'background':
                    background_failed = any(s.get('result', {}).get('status') == 'failed' for s in steps)
                    continue
                if element.get('type') != 'scenario':
                    continue
                failed = [s for s in steps if s.get('result', {}).get('status') == 'failed']
                skipped = any(s.get('result', {}).get('status') in {'skipped','undefined','pending'} for s in steps)
                state = 'failed' if failed or background_failed else 'skipped' if skipped else 'passed'
                uri = feature['uri'].replace('\\', '/')
                rows.append({'key':f"{uri}::{element['line']}", 'file':uri, 'line':element['line'],
                    'name':element['name'], 'cases':[t['name'][1:] for t in element.get('tags', []) if t['name'].startswith(('@G4-', '@CF-', '@CT-'))],
                    'status':state, 'background_failed':background_failed,
                    # Only fingerprints are published, never raw HTTP bodies or tokens.
                    'tags':[t['name'] for t in feature.get('tags',[])+element.get('tags',[])],
                    'failure_signatures':[{'step':s['name'],'signature':s['result'].get('error_message','').split('\n\n')[0].strip()} for s in failed],
                    'failed_steps':[{'step':s['name'], 'error_sha256':hashlib.sha256(s['result'].get('error_message','').encode()).hexdigest()} for s in failed]})
    if not rows or len({r['key'] for r in rows}) != len(rows):
        raise ValueError('Reporte vacío o identificadores de escenario duplicados')
    summary = json.loads((directory/'karate-summary-json.txt').read_text(encoding='utf-8'))
    passed = summary['scenariosPassed']
    failed = summary.get('scenariosfailed', summary.get('scenariosFailed'))
    if passed + failed != len(rows) or failed != sum(r['status']=='failed' for r in rows):
        raise ValueError('Resumen Karate y escenarios no coinciden; no publicar resultados parciales')
    return rows


def classify(row, manifest, catalog):
    if row['status'] != 'failed':
        return None
    active_path=ROOT/'data/quality-policy.json'
    if active_path.exists():
        active=json.loads(active_path.read_text(encoding='utf-8'))
        source=ROOT/row['file']
        source_ok=source.exists() and hashlib.sha256(source.read_text(encoding='utf-8').encode()).hexdigest()==active.get('source_hashes',{}).get(row['file'])
        if source_ok and manifest.get('reference_commit')==active.get('reference_commit') and not row['background_failed']:
            for rule in active.get('api_rules',[]):
                if rule['key']==row['key'] and rule['failures']==row.get('failure_signatures') and '@known_issue' in row.get('tags',[]):return rule['defect']
    for known in catalog['failures']:
        if (manifest['reference_commit'] == catalog['reference_commit']
            and known['key'] == row['key']
            and known['source_sha256'] == manifest['source_hashes'].get(row['file'])
            and known['failed_steps'] == row['failed_steps']
            and not row['background_failed']):
            return known['defect']
    return None


def diagnose_karate(manifest_path):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest['tool'] != 'karate' or manifest.get('scope') != 'all' or manifest.get('tag'):
        raise ValueError('El diagnóstico consolidado requiere suite Karate completa, sin selección')
    directory = validate(manifest)
    rows = parse_karate(directory)
    catalog = json.loads((ROOT/'data/api-known-failures.json').read_text(encoding='utf-8'))
    for row in rows:
        row['defect'] = classify(row, manifest, catalog)
        row['classification'] = ('defecto conocido reproducido' if row['defect'] else 'fallo sin clasificar') if row['status']=='failed' else row['status']
    active_path=ROOT/'data/quality-policy.json'
    active=json.loads(active_path.read_text(encoding='utf-8')) if active_path.exists() else {}
    known_keys = {f['key'] for f in active.get('api_rules',catalog['failures'])}
    return {'tool':'karate', 'run_id':manifest['run_id'], 'report_dir':manifest['report_dir'],
        'qa_revision':manifest.get('qa_revision'), 'qa_worktree_dirty':manifest.get('qa_worktree_dirty'),
        'reference_commit':manifest['reference_commit'], 'exit_code':manifest['exit_code'],
        'counts':dict(Counter(r['status'] for r in rows)),
        'known_failure_instances':sum(bool(r['defect']) for r in rows),
        'unknown_failures':sum(r['status']=='failed' and not r['defect'] for r in rows),
        'background_failures':sum(r['background_failed'] for r in rows),
        'known_cases_not_reproduced':[r['key'] for r in rows if r['key'] in known_keys and r['status']=='passed'],
        'policy':'Clasificación informativa. Ningún defecto conocido cambia FAIL a PASS.', 'cases':rows}


def diagnose_schemathesis(manifest_path):
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    if manifest['tool'] != 'schemathesis':
        raise ValueError('Manifiesto de herramienta incorrecta')
    directory = validate(manifest)
    detail = json.loads((directory/'schemathesis-detallado.json').read_text(encoding='utf-8'))
    if detail['summary']['run_id'] != manifest['run_id']:
        raise ValueError('Detalle Schemathesis de otra ejecución')
    failures = Counter()
    for row in detail['requests']:
        for check in row['checks']:
            if check['status'] == 'failure':
                failures[(row['operation'], check.get('name','sin nombre'))] += 1
    controls_path = directory/'controles-contexto.json'
    controls = json.loads(controls_path.read_text(encoding='utf-8')) if controls_path.exists() else []
    xmls = list(directory.glob('junit*.xml'))
    if len(xmls) != 1:
        raise ValueError('Falta JUnit único de Schemathesis')
    junit = ET.parse(xmls[0]).getroot()
    return {'tool':'schemathesis','run_id':manifest['run_id'],'report_dir':manifest['report_dir'],
        'qa_revision':manifest.get('qa_revision'), 'qa_worktree_dirty':manifest.get('qa_worktree_dirty'),
        'reference_commit':manifest['reference_commit'], 'exit_code':manifest['exit_code'],
        'interactions':detail['summary']['ndjson_interactions'],
        'failure_occurrences':sum(failures.values()),
        'failure_groups':[{'operation':op,'check':check,'occurrences':count} for (op,check),count in sorted(failures.items())],
        'junit_failures':len(junit.findall('.//failure')), 'junit_errors':len(junit.findall('.//error')),
        'context_controls':len(controls),
        'context_successful_controls':sum(200 <= c.get('response_status',0) < 300 for c in controls),
        'policy':'Señales de contrato; no equivalen a defectos únicos confirmados. No se suprimen checks.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('tool', choices=['karate','schemathesis'])
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    path = args.manifest or ROOT/f'reports/latest-{args.tool}.json'
    result = (diagnose_karate if args.tool=='karate' else diagnose_schemathesis)(path)
    output = ROOT/result['report_dir']/'diagnostico.json'
    output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=True,indent=2))
    print('Diagnóstico: '+str(output))
    raise SystemExit(1 if result['exit_code'] or result.get('unknown_failures') or result.get('counts',{}).get('skipped') else 0)
