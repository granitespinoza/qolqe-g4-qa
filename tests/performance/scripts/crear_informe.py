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
    ps[3].text='Aplicación bajo prueba: Qolqe Wallet     Herramienta: k6 '+meta['k6_version'].split()[1].lstrip('v')
    ps[7].text='Se evalúa si Qolqe soporta la hora punta y el triple de concurrencia de Quincena Qolqe. Se miden tiempos, errores, volumen y recursos, y se verifica integridad monetaria en un entorno local.'
    ps[9].text='Consultas de saldo/perfil y movimientos: frecuencia y acceso a información del usuario. Transferencias, recargas y pagos: impacto directo en dinero y riesgo de inconsistencias. Contactos y operaciones auxiliares: representan el resto del perfil operacional. Se incluyen las ocho categorías del requerimiento con sus ponderaciones.'
    ps[11].text='☐ Web';ps[12].text='☒ API';ps[13].text='☐ Ambas'
    ps[15].text='Se genera carga HTTP sobre los flujos reales del backend, sin simular respuestas. Esta capa permite reproducir las operaciones ponderadas y la concurrencia sin añadir cientos de navegadores al mismo equipo. No mide renderizado ni experiencia visual del frontend; Cypress de la Parte 2 conserva esa cobertura funcional.'
    ps[19].text='La herramienta utilizada para generar carga fue k6. Los escenarios se implementaron en JavaScript y definieron usuarios virtuales, rampas, pausas y distribución de operaciones. Las etiquetas y los umbrales permitieron separar consultas y operaciones monetarias. El equipo ya trabajaba con JavaScript/TypeScript en la automatización web, por lo que esta elección permitió mantener el modelo de carga en un lenguaje conocido y revisar sus cambios en el repositorio.'
    ps[20].text='Locust permite modelar usuarios mediante Python y resulta conveniente cuando se necesita integrar el comportamiento de la carga con bibliotecas o componentes escritos en ese lenguaje. Para Qolqe se prefirió conservar los escenarios en JavaScript y utilizar Python en la preparación de datos, el monitoreo y el análisis. JMeter resulta conveniente para equipos que diseñan planes visuales y necesitan combinar HTTP con protocolos como JDBC. La evaluación de Qolqe se centró en HTTP y se optó por scripts JavaScript, sin incorporar un plan visual adicional. Locust y JMeter se consideraron como alternativas; no se utilizaron en las ejecuciones. La medición de CPU y memoria se realizó con psutil.'
    tab=d.tables[0]
    tab.rows[0].cells[2].text='Justificación'
    vals=[['Carga','Sí, ejecutada','Valida la hora punta estimada de 100 usuarios y sus umbrales.'],['Estrés','Sí, ejecutada','Incrementos hasta 600 VUs para observar dónde se incumple; no equivale a capacidad de producción.'],['Pico / campaña','Sí, campaña ejecutada','Subida hasta 300 VUs en 300 s y mantenimiento hasta el fin de la ventana de campaña. No se añade un salto instantáneo no cuantificado por el negocio.'],['Resistencia','Relevante; no ejecutada','Las 18 h sin reinicios justifican una prueba dedicada. Se descarta su ejecución completa en esta entrega por ventana experimental y entorno local compartido. No se afirma estabilidad de 18 h ni ausencia de fugas.']]
    for row,values in zip(tab.rows[1:],vals):
        for c,t in zip(row.cells,values):c.text=t
    t=d.tables[1]
    rows=[['Parámetro','Carga normal','Estrés'],['VUs','100','25 → 50 → 100 → 200 → 300 → 450 → 600'],['Ramp-up (s)','300','30 por incremento'],['Duración (s)','960 programados + cierre de sesiones','1320 programados + cierre de sesiones'],['Think time (ms)','10000–25000, media 18000','Misma distribución'],['Distribución (%)','30/15/15/10/10/6/4/10','Misma mezcla ponderada']]
    for row,values in zip(t.rows,rows):
        for c,x in zip(row.cells,values):c.text=x
    ps[27].text='La concurrencia normal estimada es de 100 usuarios: 3000 sesiones/h ÷ 60 × 2 minutos. La campaña triplica ese nivel hasta 300 usuarios. El volumen normal equivale a 5 operaciones de negocio/s, además de 0,83 inicios de sesión/s. La campaña tiene 300 s de subida, 600 s estables y 60 s de descenso. Para las pausas se utilizó una distribución triangular de 10 a 25 s, con moda de 19 s y media de 18 s. Cada sesión incluye un login y seis operaciones, con una pausa antes de cada operación. Las duraciones de estabilización y los escalones de estrés son decisiones experimentales; la duración efectiva de las sesiones depende también de las respuestas del sistema.'
    mix='Saldo/perfil 30%; movimientos 15%; transferencias 15%; contactos 10%; recargas 10%; consulta de deudas 6%; pagos 4%; otros 10%. La selección de operaciones fue aleatoria y ponderada, con semilla 20261112.'
    after(ps[27],mix)
    t=d.tables[2];accept=[['Tiempo de respuesta','Consultas/login p95 <800 ms; dinero p95 <1500 ms','Requerimiento de servicio; evaluación por operación.'],['Tasa de error máxima','<=1% en hora punta','No más del 1%; se separan errores de datos, HTTP y transporte.'],['Throughput mínimo','5 operaciones negocio/s en hora punta, más login','3000 sesiones/h × 6; peticiones HTTP no equivalen a operaciones.']]
    for row,values in zip(t.rows[1:],accept):
        for c,x in zip(row.cells,values):c.text=x
    ps[31].text='Durante la campaña se exige que ninguna operación monetaria quede incompleta ni se aplique dos veces. El requerimiento no establece un límite numérico para la degradación de tiempos o errores en ese periodo; los valores se compararon con la hora punta como referencia. La capacidad se estimó a partir del mayor escalón probado que cumplió los umbrales normales y el volumen proporcional a su concurrencia.'
    ps[34].text=f"Entorno local: Windows 11. Procesador: {env.get('cpu','Intel Core i5-11400H')}. CPU: {meta['physical_cpus']} núcleos físicos y {meta['logical_cpus']} lógicos; RAM: {meta['memory_gb']} GB. Python {meta['python'].split()[0]}, FastAPI 0.117.1 y Starlette 0.48.0, con un worker de Uvicorn y SQLite. Versión de Qolqe: {meta['reference_commit'][:8]}."
    ps[35].text='CPU y memoria RSS se registraron cada segundo mediante psutil para Qolqe y k6. La medición de Qolqe incluyó sus procesos hijos. La CPU se expresó tanto en equivalentes de núcleo como en porcentaje de la capacidad total del equipo. Las marcas de tiempo permitieron relacionar recursos, latencia, errores y throughput durante cada ejecución.'
    ps[36].text='La aplicación y el generador compartieron CPU, RAM y disco con otros procesos del equipo. Se mantuvieron el código original, SQLite y un worker de Uvicorn. El criterio de validez del generador fue una utilización inferior al 80% de CPU total. Los resultados corresponden a este entorno local. Se utilizaron 1000 movimientos por propietario, como en los usuarios de carga de la semilla original, concentrados en una fecha incluida en el rango consultado. Esta distribución sintética condiciona la estimación de capacidad.'
    ps[37].text='Después del incumplimiento observado con 100 usuarios se incorporaron los escalones de 25 y 50 para acotar el límite inferior. Se permitió hasta 150 s adicionales para finalizar sesiones, por lo que la duración efectiva pudo superar la programada. Los primeros ingresos de campaña se concentraron en cinco minutos y se repitieron sesiones para sostener la carga. No se ejecutó la resistencia de 18 horas por la duración del experimento y el uso compartido del equipo.'
    rows=[]
    for r in primary:
        for w in r['windows']:
            rows.append([r['profile'],f"{w['start_s']}–{w['end_s']}",txt(w['ops_s']),txt(w['p95_consulta']),txt(w['p95_dinero']),txt(100*w['error_rate'])if w['error_rate']is not None else'—','Conforme' if r['integrity']['approved'] else 'Incidencias'])
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
    ps[41].text=f'Con 100 usuarios, la carga sostuvo {txt(load["windows"][0]["ops_s"])} operaciones correctas/s y registró 0% de errores. Movimientos obtuvo un p95 de {txt(load["by_operation"]["movimientos"]["p95"])} ms, superior al umbral de 800 ms. En campaña, con 300 usuarios, se alcanzaron {txt(campaign["windows"][0]["ops_s"])} operaciones correctas/s sin errores; el p95 de movimientos fue de {txt(campaign["by_operation"]["movimientos"]["p95"])} ms. La carga normal incumplió el criterio temporal de ese endpoint.'
    ps[42].text=f'La conciliación registró {load["integrity"]["database_operations"]} operaciones monetarias persistidas en carga y {campaign["integrity"]["database_operations"]} en campaña. En estrés hubo {stress["integrity"]["attempts"]} intentos y {stress["integrity"]["database_operations"]} operaciones persistidas. Los saldos y movimientos fueron consistentes con los registros de las operaciones; no se detectaron duplicados ni operaciones parciales.'
    ps[43].text='Evidencia gráfica de carga normal y campaña';ps[43].paragraph_format.keep_with_next=True
    tail=ps[43]
    for r in [load,campaign]:
        tail=after(tail,f"{r['profile'].upper()} · {r['meta']['run_id']}");tail.paragraph_format.keep_with_next=True
        run=ROOT/'tests/performance/resultados'/r['meta']['run_id'];tail=after(tail,'')
        tail.add_run().add_picture(str(run/'graficos/rendimiento-doc.png'),width=Inches(6.0))
        tail=after(tail,'');tail.add_run().add_picture(str(run/'graficos/recursos-doc.png'),width=Inches(6.0))
        tail=after(tail,f"Máximos: CPU Qolqe {txt(r['resources']['app_cpu_host_max'])}% del host; CPU k6 {txt(r['resources']['generator_cpu_host_max'])}%; RSS Qolqe {txt(r['resources']['app_rss_mb_max'])} MB. Ventanas estables sombreadas; puntos temporales de 15 s.")
    ps[45].text='Estrés y detalle por operación'
    ps[46].text=f'En estrés, 25 y 50 usuarios cumplieron los umbrales y el volumen proporcional. Con 100 usuarios el p95 de movimientos fue de {txt(stress["windows"][2]["by_operation"]["movimientos"]["p95"])} ms. Con 450 usuarios la tasa de error de las operaciones de negocio alcanzó {txt(100*stress["windows"][5]["error_rate"])}%; con 600 fue de {txt(100*stress["windows"][6]["error_rate"])}% y el throughput exitoso cayó a cero.'
    ps[47].text=f"Estrés: CPU Qolqe máxima {txt(stress['resources']['app_cpu_host_max'])}% del host; CPU k6 máxima {txt(stress['resources']['generator_cpu_host_max'])}%; RSS Qolqe máximo {txt(stress['resources']['app_rss_mb_max'])} MB."
    ps[48].text='Evolución de estrés y p95 por operación en carga'
    tail=after(ps[48],'');tail.add_run().add_picture(str(PERF/'resultados'/stress['meta']['run_id']/'graficos/rendimiento-doc.png'),width=Inches(6))
    tail=after(tail,'');tail.add_run().add_picture(str(PERF/'resultados'/stress['meta']['run_id']/'graficos/recursos-doc.png'),width=Inches(6))
    tail=after(tail,'');tail.add_run().add_picture(str(PERF/'resultados'/load['meta']['run_id']/'graficos/p95-operacion.png'),width=Inches(6))
    outcomes='; '.join(f"{r['profile']}: válida={r['valid']}, cumple perfil={r['approved']}, integridad={r['integrity']['approved']}"for r in primary)
    ps[52].text='La hora punta no cumplió todos los requisitos: el volumen y la tasa de error estuvieron dentro de lo exigido, pero la consulta de movimientos superó el límite de latencia. La campaña mantuvo la integridad monetaria con tiempos superiores a la referencia normal. El estrés identificó incumplimientos temporales desde 100 usuarios y una caída marcada del servicio al llegar a 450 usuarios.'
    passing=[]
    levels=[25,50,100,200,300,450,600]
    for level,w in zip(levels,stress['windows']):
        if w.get('per_operation_ok',False)and w['error_ok']and w['ops_s']>=level*.05:passing.append(level)
    ps[54].text=f'El mayor escalón que cumplió los umbrales por operación y el volumen proporcional fue de {max(passing)} usuarios virtuales. El siguiente nivel probado, 100 usuarios, incumplió la latencia de movimientos. La capacidad observada queda acotada entre esos niveles para las ventanas y el entorno evaluados.' if passing else 'Ningún escalón cumplió simultáneamente los criterios de tiempo, error y volumen.'
    ps[53].text='Los errores HTTP 500 aparecidos durante el estrés coincidieron con excepciones sqlite3.OperationalError: database is locked en las escrituras de Qolqe. Los gráficos muestran el aumento de latencia y errores junto con la caída del throughput exitoso. Esto respalda la contención de escrituras como uno de los factores de degradación. No se aislaron los tiempos de bloqueo, acceso a disco y espera de ejecución para cuantificar la contribución de cada recurso.'
    diagnosis=json.loads((PERF/'resultados/diagnostico-sql.json').read_text(encoding='utf-8'))
    diag=diagnosis['summary']
    after(ps[53],f"El diagnóstico aislado del historial registró {diag[0]['selects']} SELECT para {diag[0]['historial']} movimientos y {diag[1]['selects']} para {diag[1]['historial']}; las sumas por fila fueron {diag[0]['sumas']} y {diag[1]['sumas']}. Esto confirma un patrón N+1 antes de paginar. El patrón N+1 incrementa el trabajo del historial; los bloqueos de escritura constituyen otro factor de degradación observado. ")
    after(ps[54],f"En estrés se detectaron {stress['integrity']['committed_after_http_error']} operaciones persistidas pese a una respuesta HTTP fallida o perdida. Se conciliaron sin reintentar: no hubo duplicados ni operaciones parciales detectadas, pero existe riesgo de repetición por el usuario si desconoce el resultado.")
    ps[55].text='Los principales riesgos son la lentitud del historial durante la hora punta, los rechazos y timeouts bajo sobrecarga y la repetición de operaciones cuyo resultado el cliente desconoce. La ejecución local y las ventanas breves de estrés limitan la extrapolación de estos resultados a producción.'
    ps[56].text='Se recomienda priorizar la paginación en SQL y el cálculo de saldos sin consultas por cada movimiento; instrumentar la duración y espera de las transacciones SQLite; incorporar consulta de estado e idempotencia para operaciones monetarias; repetir el intervalo de 50 a 100 usuarios con servidor y generador separados; ejecutar resistencia durante 18 horas y acordar un límite cuantitativo de degradación para la campaña.'
    editorial_remove={'Completar para cada tipo de prueba que van a ejecutar:', 'Por qué eligieron su herramienta y cómo se compara con otras alternativas: ventajas y limitaciones.', 'Para cada tipo, marquen si aplica y expliquen por qué (vinculen con una necesidad del requerimiento):'}
    editorial_rename={'Contexto de negocio (2-3 líneas):': 'Contexto de negocio', 'Origen de los valores (dato de negocio y cálculos):': 'Derivación de los parámetros', 'Partes del requerimiento que no se podían convertir en umbral y supuesto tomado deben estar también indicados': 'Supuestos de aceptación'}
    for paragraph in list(d.paragraphs):
        if paragraph.text in editorial_remove:paragraph._element.getparent().remove(paragraph._element)
        elif paragraph.text in editorial_rename:paragraph.text=editorial_rename[paragraph.text]
    # Keep headings with content; allow tables to flow and repeat header rows.
    for p in d.paragraphs:
        if p.style.name.startswith('Heading'):p.paragraph_format.keep_with_next=True
    final=OUT/'Informe_Rendimiento_Qolqe.docx';d.save(final)
    (OUT/'procedencia-informe.json').write_text(json.dumps({'template_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'runs':[r['meta']['run_id']for r in primary],'source':'Template_Informe_Rendimiento.docx','sections':8},indent=2),encoding='utf-8')
    print(final)
if __name__=='__main__':main()
