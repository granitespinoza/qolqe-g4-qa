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


def cobertura():
    import re
    items = []
    for line in open(ROOT / 'docs' / 'parte2' / 'verificacion-web.md', encoding='utf8'):
        m = re.match(r'\| (HU-G4-\d+-CA\d+) \| (.+?) \| (.+?) \|', line)
        if m:
            tests = [t for t in m.group(2).split(', ') if t.strip()]
            items.append((m.group(1), len(tests), 'conocido' in m.group(3)))
    scale = 38.0
    left = 150
    b = text(24, 34, 'Cobertura web por criterio de aceptación', 18, INK, 'bold')
    b += text(24, 54, f'{len(items)} criterios de G4, cada uno con al menos un test web. Un test puede cubrir varios criterios (54 tests únicos).', 12, MUTED)
    for i, (ca, n, known) in enumerate(items):
        y = 76 + i * 25
        b += text(24, y + 15, ca, 12, INK)
        color = AMBER if known else GREEN
        b += f'<rect x="{left}" y="{y}" width="{n * scale}" height="18" rx="2" fill="{color}"/>\n'
        b += text(left + n * scale + 8, y + 14, f'{n} {"test" if n == 1 else "tests"}', 12, MUTED)
    ly = 76 + len(items) * 25 + 8
    b += f'<rect x="24" y="{ly}" width="14" height="14" rx="2" fill="{GREEN}"/>' + text(44, ly + 12, 'aprobado en las tres corridas', 12, MUTED)
    b += f'<rect x="250" y="{ly}" width="14" height="14" rx="2" fill="{AMBER}"/>' + text(270, ly + 12, 'incluye un fallo conocido y documentado', 12, MUTED)
    return svg(760, ly + 34, b, 'Cobertura web por criterio', 'Tests web por criterio de aceptación de G4, con su resultado en tres corridas')


def flujo_trazabilidad():
    b = text(24, 34, 'De la historia de usuario al resultado, con dos casos reales', 18, INK, 'bold')
    b += text(24, 54, 'Cada paso es verificable: la etiqueta del código une el test con la matriz y con el defecto.', 12, MUTED)
    heads = ['Historia', 'Criterio', 'Caso de prueba', 'Etiquetas en el código', 'Resultado en el pipeline']
    xs = [24, 200, 376, 590, 838]
    ws = [160, 160, 198, 232, 238]
    for x, w, h in zip(xs, ws, heads):
        b += text(x + w / 2, 84, h, 12, MUTED, 'bold', 'middle')
    rows = [
        (['HU-G4-01', 'Agregar un contacto'], ['CA1 · R-G4-02', 'la ñ está permitida'], ['TC-E2E-G4-102', 'alias Niño al crear'],
         ['@HU-G4-01 @TC-E2E-G4-102', '@known_issue @D-01'], ['Fallo conocido D-01', 'esperado 201, obtenido 422'], '#fff7e6', '#f3d9a4'),
        (['HU-G4-01', 'Agregar un contacto'], ['CA1 · R-G4-01/02/03', 'alta válida y persistente'], ['TC-E2E-G4-001', 'alias Ana Cypress'],
         ['@HU-G4-01 @TC-E2E-G4-001'], ['Pasa', 'POST 201 y persiste al recargar'], '#e7f6ee', '#b7e1c9'),
    ]
    for r, (a, c, t, g, res, fill, stroke) in enumerate(rows):
        y = 98 + r * 112
        for i, content in enumerate([a, c, t, g]):
            b += box(xs[i], y, ws[i], 84, content, '#f1f5f9')
            if i < 3:
                b += arrow(xs[i] + ws[i] + 2, y + 42, xs[i + 1] - 2)
        b += arrow(xs[3] + ws[3] + 2, y + 42, xs[4] - 2)
        b += box(xs[4], y, ws[4], 84, res, fill, stroke)
    return svg(1100, 336, b, 'Flujo de trazabilidad', 'De historia de usuario a criterio, caso, etiquetas y resultado, con dos casos reales')


def page_object():
    b = text(24, 34, 'Page Object y su quiebre: qué pasa cuando cambia un selector', 18, INK, 'bold')
    b += text(24, 54, 'Ejemplo: cambia el botón «Agregar contacto». agregar() se invoca 15 veces en 4 specs.', 12, MUTED)
    def grid(x0, y0, color):
        out = ''
        for i in range(15):
            cx = x0 + (i % 5) * 34
            cy = y0 + (i // 5) * 34
            out += f'<rect x="{cx}" y="{cy}" width="28" height="28" rx="4" fill="{color}" stroke="{LINE}"/>\n'
        return out
    # Sin Page Object
    b += f'<rect x="24" y="78" width="500" height="280" rx="8" fill="#fff5f5" stroke="#f0c4c4"/>\n'
    b += text(274, 104, 'Sin Page Object (hipótesis)', 14, '#9b2c2c', 'bold', 'middle')
    b += grid(48, 128, '#ffffff')
    b += text(133, 245, '15 llamadas repetirían el selector', 12, MUTED, anchor='middle')
    b += arrow(228, 168, 300)
    b += box(304, 130, 196, 76, ['selector del botón', 'escrito 15 veces'], '#fde8e8', '#f0a8a8')
    b += box(48, 270, 452, 64, ['Cambia el botón: hay que corregir 15 sitios', 'y un olvido deja un test roto por motivos ajenos al negocio'], '#ffffff', '#f0c4c4', '#9b2c2c')
    # Con Page Object
    b += f'<rect x="556" y="78" width="520" height="280" rx="8" fill="#f0fbf5" stroke="#b7e1c9"/>\n'
    b += text(816, 104, 'Con Page Object (lo que hicimos)', 14, '#1f6b46', 'bold', 'middle')
    b += grid(580, 128, '#ffffff')
    b += text(665, 245, '15 llamadas a agregar()', 12, MUTED, anchor='middle')
    b += arrow(758, 168, 800)
    b += box(804, 128, 120, 80, ['ContactosPage', '.agregar()'], '#e7f6ee', '#b7e1c9')
    b += arrow(926, 168, 950)
    b += box(954, 140, 108, 56, ['selector', 'definido 1 vez'], '#e7f6ee', '#b7e1c9')
    b += box(580, 270, 482, 64, ['Cambia el botón: se corrige 1 línea en ContactosPage.ts', 'los tests y sus aserciones de negocio no se tocan'], '#ffffff', '#b7e1c9', '#1f6b46')
    b += text(24, 388, 'Límite real: 13 selectores están centralizados en pages/, pero 15 usos de data-testid siguen directos en los tests (por ejemplo boton-favorito).', 12, MUTED)
    b += text(24, 408, 'Por eso el patrón reduce el quiebre en los flujos más repetidos, y no lo elimina por completo.', 12, MUTED)
    return svg(1100, 436, b, 'Page Object y su quiebre', 'Comparación entre repetir el selector en 15 tests y centralizarlo en un Page Object')


def estabilidad():
    b = text(24, 34, 'Estabilidad: tres corridas completas, mismo resultado', 18, INK, 'bold')
    b += text(24, 54, 'Reintentos de tests: 0. Esperas fijas: 0. Las consultas y aserciones de Cypress reintentan hasta 4000 ms.', 12, MUTED)
    scale = 7.0
    for i in range(3):
        y = 84 + i * 50
        b += text(24, y + 20, f'Corrida {i + 1}', 14, INK, 'bold')
        b += f'<rect x="120" y="{y}" width="{45 * scale}" height="30" rx="3" fill="{GREEN}"/>\n'
        b += text(120 + 45 * scale / 2, y + 20, '45 PASS', 13, '#ffffff', 'bold', 'middle')
        b += f'<rect x="{120 + 45 * scale}" y="{y}" width="{9 * scale}" height="30" rx="3" fill="{AMBER}"/>\n'
        b += text(120 + 45 * scale + 9 * scale / 2, y + 20, '9', 13, INK, 'bold', 'middle')
        b += text(120 + 54 * scale + 12, y + 20, 'sin omitidos ni intermitencia', 12, MUTED)
    b += text(24, 252, 'Qué encontró el pipeline remoto: Qolqe valida «hoy» en hora de Lima; un runner en UTC enviaba una fecha futura entre 00:00 y 05:00 UTC.', 12, MUTED)
    b += text(24, 272, 'Se fijó TZ: America/Lima en el job Web en lugar de cambiar tests o firmas del gate.', 12, MUTED)
    return svg(900, 300, b, 'Estabilidad de la suite web', 'Tres corridas con 45 aprobados y 9 fallos conocidos cada una')


def reporteria():
    b = text(24, 34, 'Dónde se muestra la reportería en la demo', 18, INK, 'bold')
    b += text(24, 54, 'Del run en Actions a los reportes por herramienta, en este orden.', 12, MUTED)
    steps = [
        ('1', 'Actions', ['el run con los', 'tres jobs en verde']),
        ('2', 'Resumen del run', ['enlace al artefacto', 'entrega-parte2']),
        ('3', 'Decisión del gate', ['reports/gate/', 'resumen.md']),
        ('4', 'Matriz navegable', ['apidoc/parte2/', 'index.html']),
        ('5', 'Reportes', ['Karate, Cypress y', 'Schemathesis']),
    ]
    w, gap, x = 188, 24, 24
    for i, (n, title, lines) in enumerate(steps):
        b += f'<rect x="{x}" y="84" width="{w}" height="120" rx="8" fill="#f1f5f9" stroke="{LINE}"/>\n'
        b += f'<circle cx="{x + 24}" cy="108" r="13" fill="{BLUE}"/>' + text(x + 24, 113, n, 13, '#ffffff', 'bold', 'middle')
        b += text(x + 44, 113, title, 13, INK, 'bold')
        for j, ln in enumerate(lines):
            b += text(x + w / 2, 148 + j * 18, ln, 12, MUTED, anchor='middle')
        if i < len(steps) - 1:
            b += arrow(x + w + 2, 144, x + w + gap - 2)
        x += w + gap
    b += text(24, 236, 'Los HTML hay que servirlos (python -m http.server); los enlaces a reports/ del repo no existen porque esas carpetas no se versionan.', 12, MUTED)
    b += text(24, 256, 'El artefacto caduca a los 7 días: descargarlo antes de la exposición. El resumen permanente está en docs/parte2/resultado-gate.md.', 12, MUTED)
    return svg(1120, 284, b, 'Reportería de la demo', 'Cinco pasos para mostrar la reportería, del run de Actions a los reportes por herramienta')


# Tiempos del run remoto 41152595167 (GitHub Actions y execution.json de cada herramienta), en segundos
PURPLE = '#7c5cbf'
TIEMPOS_RUN = [('Espera en cola', 393, '#cbd5e1'), ('job_api', 127, BLUE), ('job_web', 325, TEAL), ('job_reporting', 9, PURPLE)]
TIEMPOS_PASOS = [
    ('Preparar Qolqe y dependencias (API)', 16, BLUE), ('Karate', 75, BLUE), ('Schemathesis', 20, BLUE),
    ('Preparar Qolqe y Cypress (Web)', 20, TEAL), ('Cypress, corrida 1', 105, TEAL), ('Cypress, corrida 2', 94, TEAL),
    ('Cypress, corrida 3', 94, TEAL), ('Reportería y matriz', 9, PURPLE),
]


def fmt(sec):
    m, s = divmod(int(sec), 60)
    return f'{m} min {s:02d} s' if m else f'{s} s'


def tiempos():
    total = sum(v for _, v, _ in TIEMPOS_RUN)
    work = sum(v for n, v, _ in TIEMPOS_RUN if n != 'Espera en cola')
    b = text(24, 34, 'Cuánto tardó cada cosa', 18, INK, 'bold')
    b += text(24, 54, f'Run 41152595167 de main: 14 min 19 s de reloj ({fmt(work)} de ejecución real y {fmt(393)} de espera antes del primer job; el resto, pausas entre jobs).', 12, MUTED)
    width, x = 940.0, 24.0
    for name, v, color in TIEMPOS_RUN:
        w = width * v / total
        b += f'<rect x="{x:.1f}" y="82" width="{w:.1f}" height="34" fill="{color}"/>\n'
        if w >= 70:
            fill = INK if name == 'Espera en cola' else '#ffffff'
            b += text(x + w / 2, 104, f'{name} · {fmt(v)}', 12, fill, 'bold', 'middle')
        x += w
    b += text(24, 138, 'Los segmentos finos (reportería: 9 s) no caben con etiqueta; el detalle está abajo.', 11, MUTED)
    b += text(24, 170, 'Detalle por paso', 14, INK, 'bold')
    scale = 3.6
    for i, (name, v, color) in enumerate(TIEMPOS_PASOS):
        y = 184 + i * 30
        b += text(24, y + 16, name, 12, INK)
        b += f'<rect x="270" y="{y}" width="{v * scale:.1f}" height="20" rx="2" fill="{color}"/>\n'
        b += text(270 + v * scale + 8, y + 15, fmt(v), 12, MUTED)
    ly = 184 + len(TIEMPOS_PASOS) * 30 + 6
    b += text(24, ly + 14, 'Karate 75 s y Schemathesis 20 s salen del execution.json de cada herramienta; las tres corridas de Cypress, de su manifiesto de estabilidad.', 11, MUTED)
    b += text(24, ly + 32, 'El resto de cada job son el gate, la consolidación y la publicación de artefactos.', 11, MUTED)
    return svg(1000, ly + 54, b, 'Tiempos del pipeline', 'Línea de tiempo del run y duración de cada paso')


def resumen():
    tiles = [
        ('54', 'tests web', '18 criterios de G4'), ('181', 'ejecuciones de API', '130 casos · 169 PASS · 12 conocidos'),
        ('27', 'ocurrencias de contrato', 'todas conocidas · 9 controles'), ('3 de 3', 'corridas web iguales', '45 PASS · 9 conocidos'),
        ('8', 'defectos del producto', '2 críticos · 3 altos · 3 medios'), ('205', 'filas de trazabilidad', '135 API · 70 Web'),
        ('7 min 41 s', 'de ejecución real', 'tres jobs, sin contar la cola'), ('Gate A', 'aprobado', 'sin desconocidos ni intermitencia'),
    ]
    b = text(24, 34, 'Resumen de la Entrega 2', 18, INK, 'bold')
    b += text(24, 54, 'Cifras del run verde de main (41152595167) y de la matriz de trazabilidad.', 12, MUTED)
    w, h, gap = 224, 104, 14
    colors = [BLUE, GREEN, AMBER, TEAL, RED, BLUE, PURPLE, GREEN]
    for i, (big, label, sub) in enumerate(tiles):
        x = 24 + (i % 4) * (w + gap)
        y = 78 + (i // 4) * (h + gap)
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#f8fafc" stroke="{LINE}"/>\n'
        b += f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{colors[i]}"/>\n'
        b += text(x + 22, y + 44, big, 28 if len(big) < 8 else 24, INK, 'bold')
        b += text(x + 22, y + 66, label, 13, INK, 'bold')
        b += text(x + 22, y + 86, sub, 11, MUTED)
    return svg(1000, 78 + 2 * (h + gap) + 6, b, 'Resumen', 'Ocho cifras clave de la entrega')


def karate_schemathesis():
    b = text(24, 34, 'Karate y Schemathesis: qué prueba cada uno y dónde se ve', 18, INK, 'bold')
    b += text(24, 54, 'Cifras del run verde de main 41152595167. <run> es la carpeta del run dentro del artefacto entrega-parte2.', 12, MUTED)
    cards = [
        (24, BLUE, 'Karate · API', [
            ('Qué prueba', 'reglas de negocio, estados y efectos'),
            ('Cómo', 'casos diseñados, con esperado justificado'),
            ('Resultado', '169 PASS · 12 conocidos (181 ejecuciones)'),
            ('Duración en CI', '75 s'),
        ], ['reports/raw/karate/<run>/karate-summary.html', 'evidencias/G4-004.html (caso de la ñ, en el repo)']),
        (520, TEAL, 'Schemathesis · Contrato', [
            ('Qué prueba', 'que la API cumpla el contrato OpenAPI'),
            ('Cómo', 'datos generados automáticamente'),
            ('Resultado', '27 ocurrencias, todas conocidas'),
            ('Duración en CI', '20 s'),
        ], ['reports/raw/schemathesis/<run>/schemathesis-detallado.html', 'reports/schemathesis-detallado.html (copia en el repo)']),
    ]
    for x, color, title, rows, paths in cards:
        b += f'<rect x="{x}" y="76" width="456" height="262" rx="8" fill="#ffffff" stroke="{LINE}"/>\n'
        b += f'<rect x="{x}" y="76" width="456" height="36" rx="8" fill="{color}"/>\n'
        b += text(x + 18, 100, title, 15, '#ffffff', 'bold')
        for i, (k, v) in enumerate(rows):
            y = 138 + i * 26
            b += text(x + 18, y, k, 12, MUTED, 'bold') + text(x + 130, y, v, 13, INK)
        b += text(x + 18, 258, 'Dónde se ve', 12, MUTED, 'bold')
        for i, pth in enumerate(paths):
            b += f'<rect x="{x + 18}" y="{268 + i * 30}" width="420" height="24" rx="4" fill="#f1f5f9"/>\n'
            b += text(x + 28, 285 + i * 30, pth, 12, INK)
    b += f'<rect x="24" y="352" width="952" height="40" rx="8" fill="#eef2ff" stroke="#c7d2fe"/>\n'
    b += text(500, 377, 'Se complementan: Schemathesis descubre diferencias con el contrato; Karate las confirma con un esperado justificado.', 13, INK, 'bold', 'middle')
    return svg(1000, 416, b, 'Karate y Schemathesis', 'Qué prueba cada herramienta, su resultado, duración y dónde se ve la evidencia')


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in [('pipeline', pipeline), ('gate', gate), ('trazabilidad', trazabilidad), ('cobertura', cobertura), ('flujo-trazabilidad', flujo_trazabilidad), ('page-object', page_object), ('estabilidad', estabilidad), ('reporteria', reporteria), ('tiempos', tiempos), ('resumen', resumen), ('karate-schemathesis', karate_schemathesis)]:
        (OUT / f'{name}.svg').write_text(fn(), encoding='utf-8')
        print('escrito', OUT / f'{name}.svg')
