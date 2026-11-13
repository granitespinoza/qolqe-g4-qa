"""Completa una copia de la plantilla docente con evidencia derivada de las corridas."""
import json,copy,hashlib
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
from docx import Document
from docx.shared import Inches,Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
ROOT=Path(__file__).resolve().parents[3];PERF=ROOT/'tests/performance';OUT=ROOT/'docs/parte3'
def txt(v):return 'sin muestra'if v is None else f'{v:.2f}'if isinstance(v,float)else str(v)
def after(p,text,style=None):
    el=OxmlElement('w:p');p._p.addnext(el)
    from docx.text.paragraph import Paragraph
    n=Paragraph(el,p._parent);n.style=style or p.style;n.add_run(text);return n
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    source=PERF/'plantilla/Template_Informe_Rendimiento.docx';d=Document(source);ps=list(d.paragraphs)
    d.core_properties.title='Informe de pruebas de rendimiento de Qolqe Wallet';d.core_properties.author='Granit y Franco';d.core_properties.subject='Proyecto 2 Parte 3 Quincena Qolqe'
    results=json.loads((PERF/'resultados/resumen-entrega.json').read_text(encoding='utf-8'));by={r['profile']:r for r in results}
    primary=[by[k]for k in ['carga','campana','estres']if k in by]
    if len(primary)!=3:raise RuntimeError('Se requieren resultados de carga, campaña y estrés para cerrar el informe')
    load=by['carga'];campaign=by['campana'];stress=by['estres'];meta=load['meta']
    env=json.loads((PERF/'resultados/entorno.json').read_text(encoding='utf-8-sig'))if(PERF/'resultados/entorno.json').exists()else{}
    ps[2].text='Grupo 4 · Granit y Franco     Fecha: '+datetime.now(ZoneInfo('America/Lima')).strftime('%d/%m/%Y')
    ps[3].text='Aplicación bajo prueba: Qolqe Wallet     Herramienta: '+meta['k6_version']
    ps[7].text='Se evalúa si Qolqe soporta la hora punta y el triple de concurrencia de Quincena Qolqe. Se miden tiempos, errores, volumen y recursos, y se verifica integridad monetaria en un entorno local.'
    ps[9].text='Consultas de saldo/perfil y movimientos: frecuencia y acceso a información del usuario. Transferencias, recargas y pagos: impacto directo en dinero y riesgo de inconsistencias. Contactos y operaciones auxiliares: representan el resto del perfil operacional. Se incluyen las ocho categorías del requerimiento con sus ponderaciones.'
    ps[11].text='☐ Web';ps[12].text='☒ API';ps[13].text='☐ Ambas'
    ps[15].text='Se genera carga HTTP sobre los flujos reales del backend, sin simular respuestas. Esta capa permite reproducir las operaciones ponderadas y la concurrencia sin añadir cientos de navegadores al mismo equipo. No mide renderizado ni experiencia visual del frontend; Cypress de la Parte 2 conserva esa cobertura funcional.'
    ps[19].text='Se seleccionó k6 por sus escenarios como código, usuarios virtuales, etiquetas por operación, métricas y umbrales. Los scripts usan JavaScript, cercano al TypeScript ya empleado por el equipo. Frente a Locust, se eligió un generador separado del runtime Python de Qolqe; Locust sería una alternativa adecuada por su programación en Python. Frente a JMeter, se priorizó una configuración versionable compacta; JMeter ofrece diseño visual y reportes, pero sus cargas deben ejecutarse por consola. Ninguna de estas herramientas mide por sí sola todos los recursos del servidor: se agregó psutil. No se realizaron benchmarks comparativos entre generadores.'
    ps[20].text='Fuentes de herramienta: grafana.com/docs/k6/latest/using-k6/scenarios/; grafana.com/docs/k6/latest/using-k6/thresholds/; docs.locust.io; jmeter.apache.org/usermanual/best-practices.html. Versión exacta, configuración y hashes figuran en procedencia.json de cada corrida.'
    tab=d.tables[0]
    vals=[['Carga','Sí, ejecutada','Valida la hora punta estimada de 100 usuarios y sus umbrales.'],['Estrés','Sí, ejecutada','Incrementos hasta 600 VUs para observar dónde se incumple; no equivale a capacidad de producción.'],['Pico / campaña','Sí, campaña ejecutada','Subida hasta 300 VUs en 300 s y mantenimiento hasta el fin de la ventana de campaña. No se añade un salto instantáneo no cuantificado por el negocio.'],['Resistencia','Relevante; no ejecutada','Las 18 h sin reinicios justifican una prueba dedicada. Se descarta su ejecución completa en esta entrega por ventana experimental y entorno local compartido. No se afirma estabilidad de 18 h ni ausencia de fugas.']]
    for row,values in zip(tab.rows[1:],vals):
        for c,t in zip(row.cells,values):c.text=t
    t=d.tables[1]
    rows=[['Parámetro','Carga normal','Estrés'],['VUs','100','25 → 50 → 100 → 200 → 300 → 450 → 600'],['Ramp-up (s)','300','30 por incremento'],['Duración (s)','960 programados + cierre de sesiones','1320 programados + cierre de sesiones'],['Think time (ms)','10000–25000, media 18000','Misma distribución'],['Distribución (%)','30/15/15/10/10/6/4/10','Misma mezcla ponderada']]
    for row,values in zip(t.rows,rows):
        for c,x in zip(row.cells,values):c.text=x
    ps[27].text='Origen: 3000 sesiones/h × 2 min / 60 = 100 usuarios simultáneos medios. Campaña: triple = 300. Volumen normal: 3000 × 6 / 3600 = 5 operaciones de negocio/s; login se mide aparte (0,83/s esperado). Campaña: 300 s de subida, 600 s estable y 60 s de descenso. Las duraciones estables y los escalones de estrés son decisiones experimentales. Se respeta el think time con distribución triangular mínimo 10, moda 19 y máximo 25 s, cuya media es 18 s. Se usan seis pausas entre login y seis operaciones; los dos minutos son una media de negocio, no una duración impuesta por el script. Se reporta la desviación real.'
    mix='Saldo/perfil 30%; movimientos 15%; transferencias 15%; contactos 10%; recargas 10%; consulta de deudas 6%; pagos 4%; otros 10%. La selección es ponderada con semilla 20261112 y la mezcla lograda se registra, sin prometer proporciones exactas en muestras pequeñas.'
    after(ps[27],mix)
    t=d.tables[2];accept=[['Tiempo de respuesta','Consultas/login p95 <800 ms; dinero p95 <1500 ms','Requerimiento de servicio; evaluación por operación.'],['Tasa de error máxima','<=1% en hora punta','No más del 1%; se separan errores de datos, HTTP y transporte.'],['Throughput mínimo','5 operaciones negocio/s en hora punta, más login','3000 sesiones/h × 6; peticiones HTTP no equivalen a operaciones.']]
    for row,values in zip(t.rows[1:],accept):
        for c,x in zip(row.cells,values):c.text=x
    ps[31].text='El requerimiento no cuantifica la degradación razonable durante campaña. Se informa latencia y error frente a la referencia normal sin inventar un SLA de campaña. Sí se exige integridad monetaria: cero operaciones duplicadas o parciales. Para estrés se informa el mayor escalón observado que cumple el criterio normal y el volumen equivalente, con incertidumbre por duración y entorno.'
    ps[34].text=f"Entorno local: {meta['platform']}. Procesador: {env.get('cpu','ver entorno.json')}. CPU: {meta['physical_cpus']} núcleos físicos / {meta['logical_cpus']} lógicos. RAM: {meta['memory_gb']} GB. Python {meta['python'].split()[0]}; un worker de Uvicorn. Qolqe original {meta['reference_commit']}. Configuración de dependencias: requirements-lock.txt del proyecto más requirements de performance."
    ps[35].text='Se midieron CPU y RSS cada segundo con psutil, tanto del proceso Qolqe como de sus hijos y de k6. El CSV registra hora, CPU en equivalentes de núcleo, CPU normalizada al total de procesadores y memoria MB. Se conserva también CPU y memoria del host para detectar competencia externa. Se cruzan las marcas de tiempo con el inicio efectivo de k6.'
    ps[36].text='Aplicación y generador compiten por CPU, RAM y disco; otros procesos del usuario pueden influir. No se ajustó el código del producto, número de workers ni SQLite para obtener mejores resultados. Si k6 supera 80% de CPU total del host, la corrida se invalida. Los resultados son una línea base relativa; no se extrapolan a producción ni establecen un límite universal. Se asumen 1000 movimientos por propietario, tomando como referencia el volumen de los usuarios de carga originales; se concentran en una fecha anterior para incluirlos en el rango consultado. No se afirma equivalencia con la distribución histórica real de producción.'
    ps[37].text='La referencia y preflight descubrieron errores iniciales del ejecutor (contexto de VU, arranque con cero usuarios y aislamiento entre perfiles), corregidos antes de las corridas completas. Esos intentos no se presentan como fallos de Qolqe. Los VUs se retiran con cierre de sesiones de hasta 150 s, por lo que el tiempo real puede superar el programado. Se agregaron 25 y 50 VUs al estrés después del incumplimiento a 100, para acotar el límite inferior. El primer ingreso de los usuarios de campaña se concentra en cinco minutos; se repiten sesiones para sostener la carga. No se ejecutó resistencia de 18 h. Se generaron datos adicionales fuera de la medición, sin alterar la aplicación.'
    rows=[]
    for r in primary:
        for w in r['windows']:
            rows.append([r['profile'],f"{w['start_s']}–{w['end_s']}",txt(w['ops_s']),txt(w['p95_consulta']),txt(w['p95_dinero']),txt(100*w['error_rate'])if w['error_rate']is not None else'—',str(r['integrity']['approved'])])
    def insert_table(anchor,headers,rows):
        table=d.add_table(rows=1,cols=len(headers))
        for child in d.tables[0]._tbl.tblPr:
            if child.tag in [qn('w:tblBorders'),qn('w:tblStyle'),qn('w:tblCellMar'),qn('w:tblLook')]:table._tbl.tblPr.append(copy.deepcopy(child))
        for c,x in zip(table.rows[0].cells,headers):
            c.text=x
            shade=OxmlElement('w:shd');shade.set(qn('w:fill'),'D9E2F3');c._tc.get_or_add_tcPr().append(shade)
            for run in c.paragraphs[0].runs:run.bold=True
        for vals in rows:
            for c,x in zip(table.add_row().cells,vals):c.text=str(x)
        anchor._p.addnext(table._tbl)
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    for run in para.runs:run.font.size=Pt(9)
        trpr=table.rows[0]._tr.get_or_add_trPr();rep=OxmlElement('w:tblHeader');trpr.append(rep)
        return table
    ps[40].text='Resumen de ejecuciones completas'
    insert_table(ps[40],['Perfil','Ventana s','Ops/s','p95 consulta ms','p95 dinero ms','Error %','Integridad'],rows)
    ps[41].text='El resumen agregado orienta la lectura. El cumplimiento temporal se comprueba también por cada operación para evitar que un endpoint lento quede oculto por consultas rápidas. Los reportes HTML incluyen muestras, percentiles, mezcla lograda y errores por causa. En carga, movimientos registra p95 '+txt(load['by_operation'].get('movimientos',{}).get('p95'))+' ms frente a 800 ms; ese endpoint determina el incumplimiento aunque el agregado de consultas sea menor.'
    ps[42].text='Se conservan CSV de recursos por segundo, diarios de operaciones sin tokens y saldos iniciales/esperados/observados. La conciliación verifica registros y movimientos de cada operación monetaria, incluyendo respuestas HTTP perdidas. No se reintentan escrituras.'
    ps[43].text='Evidencia gráfica de carga normal y campaña';ps[43].paragraph_format.keep_with_next=True
    tail=ps[43]
    for r in [load,campaign]:
        tail=after(tail,f"{r['profile'].upper()} · {r['meta']['run_id']}");tail.paragraph_format.keep_with_next=True
        run=ROOT/'tests/performance/resultados'/r['meta']['run_id'];tail=after(tail,'')
        tail.add_run().add_picture(str(run/'graficos/rendimiento-doc.png'),width=Inches(6.0))
        tail=after(tail,'');tail.add_run().add_picture(str(run/'graficos/recursos-doc.png'),width=Inches(6.0))
        tail=after(tail,f"Máximos: CPU Qolqe {txt(r['resources']['app_cpu_host_max'])}% del host; CPU k6 {txt(r['resources']['generator_cpu_host_max'])}%; RSS Qolqe {txt(r['resources']['app_rss_mb_max'])} MB. Ventanas estables sombreadas; puntos temporales de 15 s.")
    ps[45].text='Estrés y detalle por operación'
    ps[46].text='Las ventanas se analizan por escalón, no mezcladas en un único p95. El aumento de demanda permite observar saturación, caída de throughput o crecimiento de latencia; el diagnóstico necesita corroboración con recursos y logs.'
    ps[47].text=f"Estrés: CPU Qolqe máxima {txt(stress['resources']['app_cpu_host_max'])}% del host; CPU k6 máxima {txt(stress['resources']['generator_cpu_host_max'])}%; RSS Qolqe máximo {txt(stress['resources']['app_rss_mb_max'])} MB."
    ps[48].text='Evolución de estrés y p95 por operación en carga'
    tail=after(ps[48],'');tail.add_run().add_picture(str(PERF/'resultados'/stress['meta']['run_id']/'graficos/rendimiento-doc.png'),width=Inches(6))
    tail=after(tail,'');tail.add_run().add_picture(str(PERF/'resultados'/stress['meta']['run_id']/'graficos/recursos-doc.png'),width=Inches(6))
    tail=after(tail,'');tail.add_run().add_picture(str(PERF/'resultados'/load['meta']['run_id']/'graficos/p95-operacion.png'),width=Inches(6))
    outcomes='; '.join(f"{r['profile']}: válida={r['valid']}, cumple perfil={r['approved']}, integridad={r['integrity']['approved']}"for r in primary)
    ps[52].text='Cumplimiento observado: '+outcomes+'. Ver detalle por operación y ventana en los reportes enlazados; las respuestas fallidas no se convierten en éxitos por ser conocidas.'
    passing=[]
    levels=[25,50,100,200,300,450,600]
    for level,w in zip(levels,stress['windows']):
        if w.get('per_operation_ok',False)and w['error_ok']and w['ops_s']>=level*.05:passing.append(level)
    ps[54].text='Capacidad estimada: '+(f"el mayor escalón observado que satisface los criterios agregados y el volumen equivalente fue {max(passing)} VUs. Esto es una aproximación y debe contrastarse con percentiles por endpoint y con las limitaciones del entorno."if passing else 'ningún escalón de estrés cumplió simultáneamente latencia, error y volumen equivalente. No se establece una capacidad certificada.')
    ps[53].text='El diagnóstico se fundamenta en la forma de latencia/throughput y su coincidencia temporal con CPU, memoria y errores. El reporte no mide directamente espera de bloqueo de SQLite ni latencia de disco; por tanto una asociación con base de datos se reporta como hipótesis, no causa confirmada. Los logs se incluyen para comprobar excepciones y timeouts.'
    diagnosis=json.loads((PERF/'resultados/diagnostico-sql.json').read_text(encoding='utf-8'))
    diag=diagnosis['summary']
    after(ps[53],f"En estrés, el log registra sqlite3.OperationalError: database is locked durante escrituras. En el diagnóstico aislado del historial se observaron {diag[0]['selects']} SELECT para {diag[0]['historial']} movimientos y {diag[1]['selects']} para {diag[1]['historial']}; las sumas por fila fueron {diag[0]['sumas']} y {diag[1]['sumas']}. Esto confirma un patrón N+1 antes de paginar. Son dos evidencias complementarias: no se afirma que el N+1 sea por sí solo la causa de todos los bloqueos. Ver diagnostico-sql.json/CSV y servidor.log.")
    after(ps[54],f"En carga normal a 100 VUs se incumplió el p95 de movimientos; {max(passing) if passing else 'No hay un nivel válido'} VUs es una estimación conservadora observada en la ventana breve de estrés, no una certificación. En estrés se detectaron {stress['integrity']['committed_after_http_error']} operaciones persistidas pese a una respuesta HTTP fallida o perdida. Se conciliaron sin reintentar: no hubo duplicados ni operaciones parciales detectadas, pero existe riesgo de repetición por el usuario si desconoce el resultado.")
    ps[55].text='Riesgos: demoras o rechazos durante campaña; operaciones monetarias que el cliente perciba fallidas aunque se hayan aplicado; límites de una instancia local compartida. Cualquier inconsistencia monetaria detectada impide concluir cumplimiento del requisito de campaña.'
    ps[56].text='Recomendaciones: confirmar perfiles con registros de uso; aislar generador y servidor; instrumentar tiempos de consulta y espera de transacciones; proponer paginación SQL sin N+1 e idempotencia/consulta de estado para respuestas perdidas; repetir el nivel cercano al primer incumplimiento; ejecutar resistencia de 18 h en un entorno dedicado; acordar un umbral cuantitativo de degradación de campaña. Las optimizaciones o cambios al producto se proponen y no se implementan en esta entrega.'
    end=after(ps[42],'Trazabilidad de evidencia: tests/performance/resultados/index.html; cada carpeta incluye procedencia.json, configuración, reporte HTML, recursos.csv e integridad.json. Presentación: apidoc/parte3/index.html. Fuentes: enunciado P2 Parte 3 y clases semanas 13–14. Este informe corresponde a los run_id mostrados, no a ejecuciones remotas de Parte 2.')
    # Keep headings with content; allow tables to flow and repeat header rows.
    for p in d.paragraphs:
        if p.style.name.startswith('Heading'):p.paragraph_format.keep_with_next=True
    final=OUT/'Informe_Rendimiento_Qolqe.docx';d.save(final)
    (OUT/'procedencia-informe.json').write_text(json.dumps({'template_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runs':[r['meta']['run_id']for r in primary],'source':'Template_Informe_Rendimiento.docx','sections':8},indent=2),encoding='utf-8')
    print(final)
if __name__=='__main__':main()
