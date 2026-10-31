"""Genera los gráficos SVG del README sin dependencias externas.

Lee la matriz de trazabilidad y escribe docs/parte2/img/*.svg. Las cifras del gate son las del run
remoto indicado en docs/parte2/resultado-gate.md.
"""
import csv
from collections import Counter, defaultdict
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs' / 'parte2' / 'img'
FONT = 'Helvetica, Arial, sans-serif'
INK, MUTED, LINE = '#1f2937', '#5b6b7a', '#cbd5e1'
GREEN, AMBER, BLUE, TEAL, RED, ORANGE = '#2f9e6b', '#e0a526', '#3b82c4', '#1f9aa6', '#d1495b', '#e8833a'

# Resultado del run remoto de main (docs/parte2/resultado-gate.md)
GATE = [('Karate', 169, 12), ('Schemathesis', 0, 27), ('Web (Cypress, 3 corridas)', 45, 9)]
GATE_RUN = '41152595167'


def svg(width, height, body, title, desc):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
            f'role="img" font-family="{FONT}">\n<title>{escape(title)}</title><desc>{escape(desc)}</desc>\n'
            f'<rect width="{width}" height="{height}" rx="10" fill="#ffffff" stroke="{LINE}"/>\n{body}</svg>\n')


def text(x, y, s, size=14, fill=INK, weight='normal', anchor='start'):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escape(s)}</text>\n'


def box(x, y, w, h, lines, fill='#f1f5f9', stroke=LINE, color=INK, bold_first=True):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}"/>\n'
    step = 17
    top = y + h / 2 - (len(lines) - 1) * step / 2 + 5
    for i, line in enumerate(lines):
        out += text(x + w / 2, top + i * step, line, 13, color, 'bold' if (i == 0 and bold_first) else 'normal', 'middle')
    return out


def arrow(x1, y, x2):
    return (f'<line x1="{x1}" y1="{y}" x2="{x2 - 6}" y2="{y}" stroke="{MUTED}" stroke-width="2"/>\n'
            f'<polygon points="{x2},{y} {x2 - 9},{y - 5} {x2 - 9},{y + 5}" fill="{MUTED}"/>\n')


def pipeline():
    b = text(24, 34, 'Pipeline de CI: pruebas.yml', 18, INK, 'bold')
    b += text(24, 54, 'Tres jobs en cadena. Web y reportería usan if: always(), así que la evidencia se conserva si algo falla.', 12, MUTED)
    y0 = 78
    b += box(24, y0 + 60, 140, 96, ['Disparadores', 'push o PR a main', 'ejecución manual'], '#eef2ff', '#c7d2fe')
    cols = [
        (196, 'job_api · API y contratos', [['Karate'], ['Schemathesis'], ['Quality Gate API', 'Escenario A']]),
        (452, 'job_web · Web E2E', [['Cypress', '3 corridas'], ['Quality Gate Web', 'Escenario A']]),
        (708, 'job_reporting · Reportería', [['Decisión final', 'del mismo run'], ['Matriz y reporte', 'consolidado']]),
    ]
    for x, title, items in cols:
        b += f'<rect x="{x}" y="{y0}" width="224" height="236" rx="8" fill="#ffffff" stroke="{LINE}" stroke-dasharray="5 4"/>\n'
        b += text(x + 112, y0 + 22, title, 13, INK, 'bold', 'middle')
        gap = 12
        h = 56 if len(items) == 3 else 76
        total = len(items) * h + (len(items) - 1) * gap
        top = y0 + 36 + (200 - total) / 2
        for i, it in enumerate(items):
            fill = '#e7f6ee' if 'Gate' in it[0] or 'Decisión' in it[0] else '#f1f5f9'
            b += box(x + 20, top + i * (h + gap), 184, h, it, fill, '#b7e1c9' if fill == '#e7f6ee' else LINE)
    b += arrow(164, y0 + 108, 196) + arrow(420, y0 + 118, 452) + arrow(676, y0 + 118, 708)
    b += box(960, y0 + 78, 120, 80, ['Artefactos', 'se conservan', '7 días'], '#fff7e6', '#f3d9a4')
    b += arrow(932, y0 + 118, 960)
    return svg(1104, 340, b, 'Pipeline de CI', 'Disparadores, job de API, job Web, job de reportería y artefactos')


def gate():
    scale = 2.6
    left = 210
    b = text(24, 34, 'Quality Gate, Escenario A: aprobado', 18, INK, 'bold')
    b += text(24, 54, f'Run remoto de main {GATE_RUN}. Sin fallos desconocidos ni intermitencia en ninguna herramienta.', 12, MUTED)
    for i, (name, ok, known) in enumerate(GATE):
        y = 86 + i * 62
        b += text(24, y + 20, name, 14, INK, 'bold')
        x = left
        if ok:
            b += f'<rect x="{x}" y="{y}" width="{ok * scale}" height="30" rx="3" fill="{GREEN}"/>\n'
            b += text(x + ok * scale / 2, y + 20, f'{ok} PASS', 13, '#ffffff', 'bold', 'middle')
            x += ok * scale
        b += f'<rect x="{x}" y="{y}" width="{known * scale}" height="30" rx="3" fill="{AMBER}"/>\n'
        label = f'{known} conocidos'
        if known * scale >= 90:
            b += text(x + known * scale / 2, y + 20, label, 13, INK, 'bold', 'middle')
        else:
            b += text(x + known * scale + 8, y + 20, label, 13, INK, 'bold')
        if not ok:
            b += text(x + known * scale + 8 + 96, y + 20, 'ocurrencias de contrato revisadas', 12, MUTED)
    ly = 86 + 3 * 62 + 4
    b += f'<rect x="24" y="{ly}" width="14" height="14" rx="2" fill="{GREEN}"/>' + text(44, ly + 12, 'PASS', 12, MUTED)
    b += f'<rect x="100" y="{ly}" width="14" height="14" rx="2" fill="{AMBER}"/>' + text(120, ly + 12, 'fallo conocido y documentado (defecto del producto)', 12, MUTED)
    b += text(24, ly + 40, 'No equivale a 54 pruebas web aprobadas ni certifica el producto para producción.', 12, MUTED)
    return svg(820, ly + 62, b, 'Resultado del Quality Gate', 'Barras de PASS y fallos conocidos de Karate, Schemathesis y Web')


def trazabilidad():
    rows = list(csv.DictReader(open(ROOT / 'data' / 'trazabilidad-parte2.csv', encoding='utf8')))
    groups = defaultdict(Counter)
    for r in rows:
        hu = r['HU']
        key = 'Varias HU' if ',' in hu else ('Núcleo común' if hu.startswith('HU-N') else hu)
        known = r['Estado en pipeline'].startswith('FALLA')
        groups[key][(r['Capa'], 'known' if known else 'pass')] += 1
    order = [f'HU-G4-{i:02d}' for i in range(1, 11)] + ['Varias HU', 'Núcleo común']
    order = [k for k in order if k in groups]
    scale = 13.0
    left = 150
    b = text(24, 34, 'Trazabilidad HU → caso → resultado en el pipeline', 18, INK, 'bold')
    b += text(24, 54, f'{len(rows)} filas de la matriz (data/trazabilidad-parte2.csv). Un caso puede aparecer en varias HU: no son pruebas independientes.', 12, MUTED)
    series = [('API', 'pass', BLUE, 'API: pasa'), ('API', 'known', RED, 'API: conocido'), ('Web', 'pass', TEAL, 'Web: pasa'), ('Web', 'known', ORANGE, 'Web: conocido')]
    for i, k in enumerate(order):
        y = 80 + i * 30
        b += text(24, y + 17, k, 13, INK, 'bold' if k.startswith('HU-G4') else 'normal')
        x = left
        total = 0
        for layer, state, color, _ in series:
            n = groups[k][(layer, state)]
            if not n:
                continue
            w = n * scale
            b += f'<rect x="{x}" y="{y}" width="{w}" height="22" fill="{color}"/>\n'
            if w >= 22:
                b += text(x + w / 2, y + 16, str(n), 12, '#ffffff', 'bold', 'middle')
            x += w
            total += n
        b += text(x + 8, y + 16, str(total), 12, MUTED)
    ly = 80 + len(order) * 30 + 10
    x = 24
    for _, _, color, label in series:
        b += f'<rect x="{x}" y="{ly}" width="14" height="14" rx="2" fill="{color}"/>' + text(x + 20, ly + 12, label, 12, MUTED)
        x += 150
    return svg(900, ly + 34, b, 'Trazabilidad por historia de usuario', 'Barras apiladas de casos de API y Web por historia, con su estado en el pipeline')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [('pipeline', pipeline), ('gate', gate), ('trazabilidad', trazabilidad)]:
        (OUT / f'{name}.svg').write_text(fn(), encoding='utf-8')
        print('escrito', OUT / f'{name}.svg')
