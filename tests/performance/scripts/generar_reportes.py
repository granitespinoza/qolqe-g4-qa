"""Reportes por ejecución y presentación HTML basados en evidencia real."""
import csv,json,math,statistics,sys
from collections import defaultdict,Counter
from pathlib import Path
from html import escape
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[3];PERF=ROOT/'tests/performance'
sys.path.insert(0,str(Path(__file__).parent))
from performance import percentile,analyze
STYLE='''body{font:18px/1.65 Segoe UI,Arial,sans-serif;color:#22251f;background:#fafbf9;max-width:1120px;margin:35px auto;padding:0 25px}h1,h2{font-family:Georgia,serif;font-weight:500}h1{font-size:42px}h2{font-size:30px}table{width:100%;border-collapse:collapse;font-size:15px;margin:20px 0}td,th{border:1px solid #dce2d9;padding:10px;text-align:left;vertical-align:top}th{background:#ecd9a7}img{max-width:100%}a{color:#285e52}pre{white-space:pre-wrap;background:#edf5f1;padding:18px;overflow-wrap:anywhere}aside{background:#eef4fa;border-left:4px solid #476f98;padding:20px}button,select{padding:8px 12px;background:white;border:1px solid #22251f;border-radius:7px;font:inherit;font-size:15px;cursor:pointer}.muted{color:#626861}.fail{color:#a13f30}.pass{color:#285e52}'''
def table(headers,rows):
 return '<table><tr>'+''.join('<th>'+escape(str(v))+'</th>'for v in headers)+'</tr>'+''.join('<tr>'+''.join('<td>'+escape(str(v))+'</td>'for v in row)+'</tr>'for row in rows)+'</table>'
def nombre_perfil(profile):
 return {'campana':'campaña','estres':'estrés'}.get(profile,profile)

def fmt(v,d=1):return 'sin muestra'if v is None else f'{v:.{d}f}'
def graph(run,res):
 ev=[json.loads(s)for s in(run/'operaciones.jsonl').read_text(encoding='utf-8').splitlines()if s.strip()]
 with(run/'recursos.csv').open(encoding='utf-8')as f:rr=[{k:float(v)for k,v in r.items()}for r in csv.DictReader(f)]
 if not ev:return
 start=res['meta'].get('measurement_epoch',res['meta']['k6_started_epoch']);buckets=defaultdict(list)
 for e in ev:buckets[int((e['at']/1000-start)//15)*15].append(e)
 x=sorted(buckets);fig,axes=plt.subplots(4,1,figsize=(11,12),sharex=True)
 for cls,color in [('consulta','#476f98'),('dinero','#a95746')]:
  vals=[percentile([e['ms']for e in buckets[t]if e['clase']==cls],95)for t in x]
  axes[0].plot(x,[float('nan')if v is None else v for v in vals],label=f'p95 {cls}',color=color)
 axes[0].axhline(800,color='#476f98',ls='--',lw=.8,label='800 ms');axes[0].axhline(1500,color='#a95746',ls='--',lw=.8,label='1500 ms');axes[0].set_ylabel('Respuesta (ms)');axes[0].legend(fontsize=8,ncol=4)
 axes[1].plot(x,[100*sum(not e['ok']for e in buckets[t])/len(buckets[t])for t in x],color='#a95746',label='Errores (%; incluye login)');axes[1].axhline(1,ls='--',color='gray');axes[1].set_ylabel('Errores (%)');axes[1].legend(fontsize=8)
 axes[2].plot(x,[sum(e['op']!='login'and e['ok']for e in buckets[t])/15 for t in x],color='#497a6a',label='Operaciones exitosas/s');axes[2].set_ylabel('Operaciones exitosas/s');ax=axes[2].twinx();ax.plot(x,[max(e.get('active_vus',0)for e in buckets[t])for t in x],color='#8068a6',alpha=.6,label='VUs activos');ax.set_ylabel('VUs activos');axes[2].legend(loc='upper left',fontsize=8);ax.legend(loc='upper right',fontsize=8)
 rx=[r['epoch']-start for r in rr];axes[3].plot(rx,[r['app_cpu_host_pct']for r in rr],color='#476f98',label='CPU Qolqe (% host)');axes[3].plot(rx,[r['generator_cpu_host_pct']for r in rr],color='#a95746',label='CPU k6 (% host)');axes[3].set_ylabel('CPU (%)');am=axes[3].twinx();am.plot(rx,[r['app_rss_mb']for r in rr],color='#497a6a',alpha=.5,label='RSS Qolqe');am.plot(rx,[r['generator_rss_mb']for r in rr],color='#8068a6',alpha=.5,label='RSS k6');am.set_ylabel('RSS MB');axes[3].legend(loc='upper left',fontsize=7);am.legend(loc='upper right',fontsize=7)
 for a in axes:
  a.grid(alpha=.2)
  for w in res['windows']:a.axvspan(w['start_s'],w['end_s'],color='#c9ded5',alpha=.15)
 axes[-1].set_xlabel('Segundos desde el inicio efectivo de k6');fig.suptitle(f"{nombre_perfil(res['profile']).upper()} · {res['meta']['run_id']}\nVentanas estables sombreadas; percentiles de intervalos de 15 s",fontsize=12);fig.tight_layout(rect=(0,0,1,.95));g=run/'graficos';g.mkdir(exist_ok=True);fig.savefig(g/'evolucion.png',dpi=130);plt.close(fig)
 fig,ax=plt.subplots(figsize=(10,4));names=list(res['by_operation']);vals=[res['by_operation'][k]['p95']for k in names];ax.barh(names,vals,color=['#a95746'if k in ['transferencias','recargas','pagos']else'#497a6a'for k in names]);ax.scatter([1500 if k in ['transferencias','recargas','pagos']else 800 for k in names],range(len(names)),marker='|',s=180,color='black',label='Umbral por operación');ax.legend(fontsize=8);ax.set_xlabel('p95 de la operación en ventanas estables (ms)');ax.grid(axis='x',alpha=.2);fig.tight_layout();fig.savefig(g/'p95-operacion.png',dpi=120);plt.close(fig)
 # Separate figures retain readable labels when embedded at 6 inches in the report.
 fig,axs=plt.subplots(3,1,figsize=(6.4,5.6),sharex=True)
 for cls,col in [('consulta','#476f98'),('dinero','#a95746')]:
  vals=[percentile([e['ms']for e in buckets[t]if e['clase']==cls],95)for t in x]
  axs[0].plot(x,[float('nan')if v is None else v for v in vals],color=col,label=cls)
 axs[0].axhline(800,color='#476f98',ls='--',lw=.7);axs[0].axhline(1500,color='#a95746',ls='--',lw=.7);axs[0].set_ylabel('p95 (ms)');axs[0].legend(fontsize=8,ncol=2)
 axs[1].plot(x,[100*sum(not e['ok']for e in buckets[t])/len(buckets[t])for t in x],color='#a95746');axs[1].axhline(1,ls='--',color='gray');axs[1].set_ylabel('Error (%)')
 axs[2].plot(x,[sum(e['op']!='login'and e['ok']for e in buckets[t])/15 for t in x],color='#497a6a');axs[2].set_ylabel('Operaciones exitosas/s');axs[2].set_xlabel('Segundos de prueba')
 for a in axs:
  a.tick_params(labelsize=8);a.grid(alpha=.2)
  for w in res['windows']:a.axvspan(w['start_s'],w['end_s'],color='#c9ded5',alpha=.2)
 fig.suptitle(nombre_perfil(res['profile']).upper()+' · rendimiento',fontsize=12);fig.tight_layout(rect=(0,0,1,.96));fig.savefig(g/'rendimiento-doc.png',dpi=160);plt.close(fig)
 fig,axs=plt.subplots(2,1,figsize=(6.4,3.5),sharex=True)
 for field,col,label in [('app_cpu_host_pct','#476f98','Qolqe'),('generator_cpu_host_pct','#a95746','k6')]:axs[0].plot(rx,[r[field]for r in rr],color=col,label=label)
 axs[0].set_ylabel('CPU % host');axs[0].legend(fontsize=8,ncol=2)
 for field,col,label in [('app_rss_mb','#497a6a','Qolqe'),('generator_rss_mb','#8068a6','k6')]:axs[1].plot(rx,[r[field]for r in rr],color=col,label=label)
 axs[1].set_ylabel('RSS MB');axs[1].legend(fontsize=8,ncol=2);axs[1].set_xlabel('Segundos de prueba')
 for a in axs:a.tick_params(labelsize=8);a.grid(alpha=.2)
 fig.suptitle(nombre_perfil(res['profile']).upper()+' · recursos',fontsize=12);fig.tight_layout(rect=(0,0,1,.95));fig.savefig(g/'recursos-doc.png',dpi=160);plt.close(fig)
 with(run/'series-15s.csv').open('w',newline='',encoding='utf-8')as f:
  w=csv.writer(f);w.writerow(['elapsed_s','operations_s','p95_consulta_ms','p95_dinero_ms','error_rate_including_login','active_vus'])
  for t in x:
   a=buckets[t];w.writerow([t,sum(e['op']!='login'and e['ok']for e in a)/15,percentile([e['ms']for e in a if e['clase']=='consulta'],95),percentile([e['ms']for e in a if e['clase']=='dinero'],95),sum(not e['ok']for e in a)/len(a),max(e.get('active_vus',0)for e in a)])
def report(run,res):
 graph(run,res)
 rows=[[k,v['count'],v['errors'],fmt(v['p50']),fmt(v['p95']),fmt(v['p99']),fmt(v['share'])]for k,v in res['by_operation'].items()]
 windows=[[f"{w['start_s']}–{w['end_s']}",w['operations'],fmt(w['ops_s'],3),fmt(w['p95_consulta']),fmt(w['p95_dinero']),fmt(100*w['error_rate'])if w['error_rate']is not None else'—',w['latency_ok'],w['error_ok'],w.get('per_operation_ok')]for w in res['windows']]
 body=f"<h1>{escape(nombre_perfil(res['profile']).title())} · Pruebas de rendimiento</h1><p>{escape(run.name)}</p><p><strong>Ejecución válida: {res['valid']} · Cumplimiento del perfil: {res['approved']} · Integridad monetaria: {res['integrity']['approved']}</strong></p>"
 body+='<aside>Los incumplimientos del producto se conservan. Una ejecución válida puede no cumplir el SLA. La campaña tiene requisito obligatorio de integridad; sus tiempos se comparan descriptivamente con los umbrales normales porque el enunciado no fija una degradación numérica.</aside>'
 body+='<h2>Ventanas de medición</h2>'+table(['Segundos','Operaciones','Ops/s','p95 consulta','p95 dinero','Error %','Latencia agregada','Error normal','SLA por operación'],windows)
 body+='<h2>Resultados por operación</h2>'+table(['Operación','Muestras','Errores','p50 ms','p95 ms','p99 ms','Distribución %'],rows)
 body+='<p>El throughput de negocio cuenta únicamente operaciones correctas; all_ops_s conserva las finalizadas incluyendo fallos y req_s las peticiones totales. El contador nativo operaciones_negocio de k6 cuenta finalizaciones y no se utiliza como throughput exitoso. Saldo y perfil representa una operación de negocio con dos peticiones secuenciales. Login se mide por separado. Las métricas operacion_ms usan tiempo de pared de la operación completa; los percentiles se calculan con interpolación lineal. Las peticiones de preparación están fuera de la medición.</p>'
 body+='<h2>Evolución temporal</h2><img alt="Latencia, errores, throughput y recursos en el tiempo" src="graficos/evolucion.png"><img alt="p95 por operación" src="graficos/p95-operacion.png">'
 body+='<h2>Recursos</h2>'+table(['Métrica','Valor'],[[k,fmt(v)]for k,v in res['resources'].items()])+'<p>CPU host = CPU del proceso y sus hijos / procesadores lógicos. El CSV conserva también CPU en equivalentes de núcleo. RSS de Qolqe incluye el proceso hijo de Python. Las columnas de CPU y memoria del host reflejan competencia de otras aplicaciones.</p>'
 body+='<p>El resumen nativo de k6 incluye toda la ejecución; este análisis utiliza las ventanas estables especificadas y percentiles por operación.</p>'
 body+='<h2>Integridad y errores</h2><pre>'+escape(json.dumps(res['integrity'],ensure_ascii=False,indent=2))+'</pre>'
 body+='<p>La conciliación relaciona intentos, códigos, registros monetarios, movimientos y saldos de propietarios y destinatarios. Una respuesta HTTP perdida se investiga en la base y no se reintenta automáticamente.</p>'
 body+='<p><a href="integridad.json">Conciliación JSON</a> · <a href="saldos.csv">Saldos iniciales/esperados/finales</a> · <a href="operaciones_monetarias.json">Diario monetario conciliado</a> · <a href="recursos.csv">CSV recursos</a> · <a href="series-15s.csv">Series</a> · <a href="operaciones.jsonl">Diario de operaciones</a> · <a href="procedencia.json">Versión y entorno</a> · <a href="k6-summary.json">Resumen k6</a> · <a href="servidor.log">Log servidor</a></p>'
 counts=Counter((e['op'],str(e['statuses']),str(e['codigos']))for e in res['errors']);body+=table(['Operación','HTTP','Código','Ocurrencias'],[[*k,v]for k,v in counts.items()])
 (run/'reporte.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+escape(run.name)+'</title><style>'+STYLE+'</style>'+body+'</html>',encoding='utf-8')
def main():
 results=[]
 for profile in ['referencia','demo','carga','campana','estres']:
  latest=PERF/'resultados'/f'latest-{profile}.json'
  if not latest.exists():continue
  run=ROOT/json.loads(latest.read_text(encoding='utf-8'))['dir'];res=json.loads((run/'resumen.json').read_text(encoding='utf-8'))
  ev=[json.loads(line)for line in(run/'operaciones.jsonl').read_text(encoding='utf-8').splitlines()if line.strip()]
  with(run/'recursos.csv').open(encoding='utf-8')as f:resources=[{k:float(v)for k,v in row.items()}for row in csv.DictReader(f)]
  res=analyze(ev,resources,profile,res['meta'],res['integrity'],run)
  res['analysis_note']='Análisis regenerado desde diario y CSV de esta ejecución; procedencia conserva hashes del ejecutor medido.'
  if profile in ['referencia','demo']:res['approved']=None;res['criteria']='Perfil de referencia/demostración; no sustituye un experimento completo ni emite gate del SLA.'
  (run/'resumen.json').write_text(json.dumps(res,ensure_ascii=False,indent=2),encoding='utf-8')
  report(run,res);results.append(res)
 write=PERF/'resultados/resumen-entrega.json';write.write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
 rows=[]
 for r in results:
  run=r['meta']['run_id'];rows.append([f'<a href="{run}/reporte.html">{nombre_perfil(r["profile"])}</a>',str(r['valid']),str(r['approved']),str(r['integrity']['approved'])])
 index='<h1>Parte 3 · Quincena Qolqe</h1><p>Reportes generados desde las evidencias de ejecución.</p><table><tr><th>Perfil</th><th>Válida</th><th>Cumple perfil</th><th>Integridad</th></tr>'+''.join('<tr>'+''.join('<td>'+c+'</td>'for c in row)+'</tr>'for row in rows)+'</table><p><a href="../../../apidoc/parte3/index.html">Presentación de exposición</a></p>'
 if (PERF/'resultados/diagnostico-sql.json').exists():index+='<p><a href="diagnostico-sql.json">Diagnóstico SQL del historial</a> · <a href="diagnostico-sql.csv">Mediciones de consultas</a></p>'
 (PERF/'resultados/index.html').write_text('<!doctype html><html lang="es"><meta charset="utf-8"><title>Resultados Parte 3</title><style>'+STYLE+'</style>'+index+'</html>',encoding='utf-8')
 # Integrate into section 4 of the existing project report, preserving the other parts.
 project=ROOT/'docs/informe.md'
 if project.exists()and all(k in {r['profile']for r in results}for k in ['carga','campana','estres']):
  import re
  section='## 4. Rendimiento\n\nParte 3: campaña Quincena Qolqe, probada por API con k6 y Qolqe original. [Informe según plantilla](parte3/Informe_Rendimiento_Qolqe.docx), [resultados](../tests/performance/resultados/index.html), [modelo y ejecución](../tests/performance/README.md) y [presentación](../apidoc/parte3/index.html).\n\n'
  section+='| Perfil | Ejecución válida | Cumple perfil | Integridad | Evidencia |\n|---|---|---|---|---|\n'
  for r in results:
   if r['profile']in ['carga','campana','estres']:section+=f"| {nombre_perfil(r['profile'])} | {r['valid']} | {r['approved']} | {r['integrity']['approved']} | [Reporte](../tests/performance/resultados/{r['meta']['run_id']}/reporte.html) |\n"
  section+='\nCarga normal: aproximadamente 100 VUs y 5 operaciones/s; campaña: 300 VUs. Consultas/login p95 <800 ms, dinero p95 <1500 ms y error normal <=1%. El detalle incluye p95 por operación, CPU y memoria de aplicación/generador, gráficos y conciliación de saldos y movimientos. Resistencia de 18 h no ejecutada: limitación explícita del experimento. Los resultados son una línea base local y no certifican producción.\n\n'
  text=project.read_text(encoding='utf-8-sig');text=text.replace('# Informe — Parte 2 · G4 Contactos y solicitudes','# Informe del proyecto Qolqe Wallet',1).replace('Este informe cubre la Entrega 2 (secciones 1, 3 y 5). La sección 2 conserva el resultado de la Parte 1.','Este informe reúne las entregas del Proyecto 2. La sección 2 conserva la Parte 1; las secciones 1, 3 y 5 describen la Parte 2; la sección 4 incorpora las pruebas de rendimiento de la Parte 3.');text=re.sub(r'## 4\. Rendimiento\n.*?(?=## 5\.)',lambda _:section,text,flags=re.S)
  project.write_text(text,encoding='utf-8')
 print('Reportes actualizados:',len(results))
if __name__=='__main__':main()
