"""Valida integridad del paquete de evidencias; no convierte fallos del producto en PASS."""
from pathlib import Path
from html.parser import HTMLParser
from zipfile import ZipFile
import json,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[3];PERF=ROOT/'tests/performance'
class Links(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.slides=0
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t in ['a','img']:
   ref=a.get('href')or a.get('src')
   if ref and not ref.startswith(('http:','https:','#','data:')):self.refs.append(ref.split('#')[0])
  if t=='section'and a.get('class')=='slide':self.slides+=1
def main():
 checks=[];runs=[]
 for profile in ['carga','campana','estres']:
  pointer=PERF/'resultados'/f'latest-{profile}.json';assert pointer.exists(),pointer
  run=ROOT/json.loads(pointer.read_text(encoding='utf-8'))['dir'];r=json.loads((run/'resumen.json').read_text(encoding='utf-8'))
  assert r['profile']==profile and r['valid'],f'Ejecución inválida de {profile}: revisar antes de cerrar'
  assert r['meta']['reference_commit']=='8c7d2f0c939ede7765b7b80b98c10c3905693fda'
  assert r['meta']['k6_completed']and r['resources']['samples']>10
  assert set(['login','saldo_perfil','movimientos','transferencias','contactos','recargas','deudas','pagos','otros'])<=set(r['by_operation'])
  assert r['resources']['generator_cpu_host_max']<80
  for n in ['configuracion.json','procedencia.json','datos.json','operaciones.jsonl','recursos.csv','integridad.json','saldos.csv','k6-summary.json','reporte.html','graficos/evolucion.png','graficos/rendimiento-doc.png','graficos/recursos-doc.png']:
   assert(run/n).is_file(),run/n
  checks.append(f'{profile}: evidencia completa y ejecución válida; cumplimiento e integridad se informan por separado')
  runs.append(dict(profile=profile,run_id=run.name,valid=r['valid'],sla_or_profile_approved=r['approved'],integrity=r['integrity']['approved']))
 htmls=[ROOT/'apidoc/parte3/index.html',PERF/'resultados/index.html']+[ROOT/'tests/performance/resultados'/r['run_id']/'reporte.html'for r in runs]
 for file in htmls:
  parser=Links();parser.feed(file.read_text(encoding='utf-8'))
  for link in parser.refs:assert(file.parent/link).resolve().is_file()or(file.parent/link).resolve().is_dir(),f'Enlace roto: {file}: {link}'
 checks.append('HTML: enlaces locales y gráficos existentes')
 doc=ROOT/'docs/parte3/Informe_Rendimiento_Qolqe.docx'
 with ZipFile(doc)as z:
  root=ET.fromstring(z.read('word/document.xml'));ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
  text='\n'.join(t.text or ''for t in root.findall('.//w:t',ns))
  for title in ['1. Alcance','2. Herramienta','3. Tipos','4. Modelo','5. Criterios','6. Restricciones','7. Resultados','8. Análisis']:assert title in text,title
  assert '________________'not in text,'Campos sin completar'
 checks.append('Informe: ocho secciones de plantilla presentes y sin campos de relleno')
 main_report=(ROOT/'docs/informe.md').read_text(encoding='utf-8');assert'## 4. Rendimiento'in main_report and'Informe_Rendimiento_Qolqe.docx'in main_report
 assert(PERF/'resultados/diagnostico-sql.json').exists()
 checks.append('Informe del proyecto: sección 4 integrada; diagnóstico SQL presente')
 result=dict(package_complete=True,product_compliance_is_separate=True,runs=runs,checks=checks)
 (PERF/'resultados/verificacion-entrega.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
