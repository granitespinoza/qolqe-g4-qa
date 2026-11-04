"""Presentación del kit a partir de una matriz de procedencia conocida."""
import html
import re
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path(__file__).with_suffix('.html')


def esc(value):
    return html.escape(str(value), quote=True)


def relative_link(path, label):
    path = PurePosixPath(path)
    if path.is_absolute() or '..' in path.parts or not (ROOT / path).is_file():
        return f'{esc(label)} · archivo no incluido en esta copia'
    return f'<a href="../../{esc(path)}">{esc(label)}</a>'


def render(data, *, snapshot=False):
    remote = data.get('pipeline_url') or ''
    match = re.fullmatch(r'https://github\.com/[\w.-]+/[\w.-]+/actions/runs/(\d+)', remote)
    source = ('Evidencia histórica versionada' if snapshot else
              'Evidencia de la ejecución asociada' if match else 'Evidencia local')
    provenance = f'{source} · <a href="{esc(remote)}">GitHub Actions #{match[1]}</a>' if match else source

    rows = []
    for row in data['matrix']:
        case = relative_link(row['file'], row['tc'])
        defect = ', '.join(row['defects'])
        defects = relative_link('docs/parte2/defectos-conocidos.md', defect) if defect else '—'
        cells = [esc(row['hu']), case, esc(row['scenario']), esc(row['layer']),
                 esc(' '.join(row['tags'])), esc(row['state']), defects]
        rows.append(f'<tr data-state="{esc(row["state"])}">' +
                    ''.join(f'<td>{cell}</td>' for cell in cells) + '</tr>')

    def report_link(path, label):
        if snapshot:
            return f'{esc(label)} · disponible si se conserva el artefacto del run'
        return relative_link(path, label)

    reports = []
    for tool, run in data['api_runs'].items():
        filename = 'karate-summary.html' if tool == 'karate' else 'schemathesis-detallado.html'
        link = report_link(f'{run["report_dir"]}/{filename}', tool.capitalize())
        reports.append(f'<li>{link} · {esc(run["run_id"])} · salida {esc(run["exit_code"])}</li>')

    runs, templates = [], []
    for i, run in enumerate(data['web_runs'], 1):
        counts = run['counts']
        passed = int(counts['passed'])
        failed = int(counts['failed'])
        pending = int(counts.get('pending', 0))
        skipped = int(counts.get('skipped', 0))
        other = pending + skipped
        report = report_link(f'{run["runDir"]}/html/index.html', f'Reporte Cypress {i}')
        reports.append(f'<li>{report}</li>')
        bars = ''.join(f'<span class="{kind}" style="--count:{count}"></span>'
                       for kind, count in (('passed', passed), ('failed', failed), ('other', other)) if count)
        runs.append(f'<button class="run" type="button" data-run="run-{i}"><strong>Corrida {i}</strong>'
                    f'<span class="bar" aria-hidden="true">{bars}</span>'
                    f'<span class="counts">{passed} aprobadas · {failed} fallidas · {other} pendientes u omitidas</span></button>')
        templates.append(f'<template id="run-{i}"><h3>Cypress · corrida {i}</h3>'
                         f'<p>Inicio: <time datetime="{esc(run["started"])}">{esc(run["started"])}</time></p>'
                         f'<ul class="run-detail-counts"><li>Aprobadas: {passed}</li><li>Fallidas: {failed}</li>'
                         f'<li>Pendientes: {pending}</li><li>Omitidas: {skipped}</li></ul>'
                         f'<p>{report}</p><p>{provenance}.</p></template>')

    gate = data.get('gate') or {}
    verdict = {True: 'aprobado', False: 'bloqueado'}.get(gate.get('approved'), 'sin decisión registrada')
    example = next((r for r in data['matrix'] if r['tc'] == 'TC-G4-004'), None)
    substitutions = dict(
        provenance=provenance,
        criterion_count=len(data['criteria']),
        case_state=esc(example['state'] if example else 'sin resultado disponible'),
        gate_note=f'Quality Gate: {esc(gate.get("scenario", "pendiente"))} · {verdict}.',
        rows='\n'.join(rows),
        report_links='\n'.join(reports) or '<li>No hay reportes asociados.</li>',
        runs='\n'.join(runs) or '<p>No hay corridas web asociadas.</p>',
        run_templates='\n'.join(templates),
    )
    return re.sub(r'\{\{(\w+)\}\}', lambda m: str(substitutions[m[1]]),
                  TEMPLATE.read_text(encoding='utf-8'))
