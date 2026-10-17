"""Publica evidencia redactada de casos técnicos y funcionales complementarios."""
import html, json, re
from pathlib import Path
from qa_provenance import validate

ROOT = Path(__file__).resolve().parents[1]

def build():
    manifest = json.loads((ROOT/'reports/latest-karate.json').read_text(encoding='utf-8'))
    folder = validate(manifest)
    rows = []
    for path in sorted(folder.glob('features.*.json')):
        features = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(features, list): continue
        for feature in features:
            background = []
            for scenario in feature.get('elements', []):
                if scenario.get('type') == 'background':
                    background = scenario.get('steps', [])
                    continue
                if scenario.get('type') != 'scenario': continue
                tags = [t['name'].lstrip('@') for t in scenario.get('tags', [])]
                tag = next((t for t in tags if re.fullmatch(r'(CT|CF)-\d+', t)), None)
                if not tag: continue
                key = f"{tag}-{scenario.get('line', len(rows))}"
                steps = background + scenario.get('steps', [])
                statuses = [s.get('result', {}).get('status') for s in steps]
                status = 'FALLÓ' if 'failed' in statuses else ('PENDIENTE' if 'skipped' in statuses else 'APROBADO')
                logs = '\n'.join(s.get('doc_string', {}).get('value', '') + '\n' + s.get('result', {}).get('error_message', '') for s in steps)
                logs = re.sub(r'eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', '<TOKEN_OCULTO>', logs)
                title = scenario.get('name', tag)
                target = f'evidencias/{key}.html'
                (ROOT/target).write_text(f'<html lang="es"><meta charset="utf-8"><title>{html.escape(key)}</title><style>body{{font:16px Segoe UI;margin:35px}}pre{{white-space:pre-wrap;overflow-wrap:anywhere}}</style><h1>{html.escape(title)}</h1><p>{key} · {status} · ejecución {manifest["run_id"]}</p><p>Registro real; tokens ocultos. Cada fila de Examples se conserva por separado.</p><pre>{html.escape(logs)}</pre></html>', encoding='utf-8')
                rows.append(dict(id=key, tag=tag, name=title, status=status, evidence=target))
    stats = {state: sum(r['status']==state for r in rows) for state in ('APROBADO','FALLÓ','PENDIENTE')}
    (ROOT/'reports/complementarios.json').write_text(json.dumps(dict(run_id=manifest['run_id'], stats=stats, cases=rows),ensure_ascii=False,indent=2), encoding='utf-8')
    lines = ['# Resultados complementarios', '', f'Ejecución: `{manifest["run_id"]}`. Separados del catálogo inicial de 116 casos.', '', f'{len(rows)} escenarios: {stats["APROBADO"]} aprobados, {stats["FALLÓ"]} fallidos, {stats["PENDIENTE"]} pendientes.', '', '| Tag | Variante ejecutada | Resultado | Evidencia |', '|---|---|---|---|']
    for row in rows:
        lines.append(f'| {row["tag"]} | {row["name"].replace("|", "/")} | {row["status"]} | [HTTP real](../{row["evidence"]}) |')
    (ROOT/'docs/resultados-complementarios.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(f'Complementarios: {len(rows)}; {stats}')

if __name__=='__main__': build()
