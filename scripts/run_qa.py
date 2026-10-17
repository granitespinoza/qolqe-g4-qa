"""Ejecuta Karate o Schemathesis y conserva códigos de salida reales."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shutil, socket, subprocess, sys, time, uuid
import urllib.request
from qa_provenance import snapshot

ROOT = Path(__file__).resolve().parents[1]
def api(route, body=None):
    request=urllib.request.Request('http://127.0.0.1:8000'+route,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request, timeout=15) as r: return json.load(r)
def run(mode, tag=None, scope='all'):
    started=datetime.datetime.now(datetime.timezone.utc)
    run_id=started.strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:6]
    report_dir='reports/raw/'+mode+'/'+run_id
    manifest={'run_id':run_id,'tool':mode,'scope':scope,'tag':tag,'started_at':started.isoformat(),'report_dir':report_dir,**snapshot()}
    schema_bytes=json.dumps(api('/openapi.json'),ensure_ascii=False,indent=2).encode('utf-8')
    manifest['openapi_sha256']=hashlib.sha256(schema_bytes).hexdigest()
    if mode=='karate':
        java=shutil.which('java') or next((str(p) for p in (ROOT/'.tools/java').rglob('java.exe')),None)
        if not java: raise SystemExit('Falta Java 17: ejecutar scripts/bootstrap.ps1')
        args=[java,'-DqaPython='+sys.executable,'-cp',str(ROOT/'.tools/karate.jar')+os.pathsep+str(ROOT),'com.intuit.karate.Main','-T','1','-f','cucumber:json,junit:xml','-r',report_dir,'features']
        if scope == 'g4':
            args[-1:] = [str(p.relative_to(ROOT)) for p in sorted((ROOT/'features').glob('hu-g4-*.feature'))]
        if tag:
            # Se pasa como argumento, sin ejecutar texto en un shell.
            args[args.index('-r'):args.index('-r')] = ['-t', tag]
    else:
        manifest['context_hooks_sha256']=hashlib.sha256((ROOT/'scripts/schemathesis_context.py').read_bytes()).hexdigest()
        manifest['phases']=['examples','coverage','fuzzing']
        manifest['context_policy']='Controles explícitos con recursos reales; generación aleatoria sin corregir; respuestas sin modificar.'
        # Usuario dedicado: no se imprimen ni guardan sus credenciales de sesión.
        n=str(time.time_ns()%90000000+10000000)
        api('/api/usuarios',{'dni':n,'celular':'9'+n,'nombres':'Contrato Prueba','pin':'4826'})
        preparation=[]
        for attempt in range(1,4):
            try:
                token=api('/api/auth/login',{'celular':'9'+n,'pin':'4826'})['access_token']
                break
            except urllib.error.HTTPError as error:
                if error.code != 401 or attempt == 3: raise
                failure=json.loads(error.read())
                preparation.append({'operation':'login de generador tras registro','attempt':attempt,
                    'response_status':error.code,'codigo':failure.get('codigo'), 'detail':failure.get('detail')})
                time.sleep(0.2)
        manifest['generator_preparation_retries']=preparation
        args=[str(Path(sys.executable).parent/('schemathesis.exe' if os.name=='nt' else 'schemathesis')),'run','http://127.0.0.1:8000/openapi.json','--include-path-regex','^/api/(contactos|solicitudes)(/|$)','--header','Authorization: Bearer '+token,'--phases','examples,coverage,fuzzing','--max-examples','20','--seed','20261013','--workers','1','--continue-on-failure','--report','junit,ndjson,har','--report-dir','reports/raw/schemathesis']
        auth_index=args.index('--header')
        del args[auth_index:auth_index+2]
    if mode=='schemathesis':args[args.index('--report-dir')+1]=report_dir
    log=ROOT/'.tools'/f'{mode}-{run_id}.log'
    log.parent.mkdir(exist_ok=True)
    with log.open('w',encoding='utf-8') as f:
        env=os.environ.copy();env['PYTHONIOENCODING']='utf-8';env['PYTHONUTF8']='1'
        if mode=='schemathesis':
            env['SCHEMATHESIS_HOOKS']='scripts.schemathesis_context'
            env['QA_SCHEMATHESIS_REPORT_DIR']=str(ROOT/report_dir)
            env['QA_SCHEMATHESIS_TOKEN']=token
        result=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,env=env)
    manifest.update(finished_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),exit_code=result.returncode)
    (ROOT/report_dir).mkdir(parents=True,exist_ok=True)
    (ROOT/report_dir/'openapi.json').write_bytes(schema_bytes)
    (ROOT/report_dir/'execution.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    # Una demostración parcial nunca reemplaza el resultado de la suite completa.
    pointer = f'latest-{mode}' if not tag and scope == 'all' else f'latest-{mode}-selection'
    (ROOT/'reports'/f'{pointer}.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(f'{mode}: salida {result.returncode}; alcance {scope}; tag {tag or "todos"}')
    print(f'Registro local: {log}')
    if mode == 'karate':
        summary=ROOT/report_dir/'karate-summary-json.txt'
        if summary.exists():
            counts=json.loads(summary.read_text(encoding='utf-8'))
            # Karate 1.5.2 escribe scenariosfailed con f minúscula.
            passed=counts.get('scenariosPassed', 0)
            failed=counts.get('scenariosfailed', counts.get('scenariosFailed', 0))
            print(f'Escenarios: {passed} aprobados; {failed} fallidos.')
        print(f'Reporte: http://localhost:8765/{report_dir}/karate-summary.html')
        print('Si hay fallos, revisa el paso rojo: una aserción funcional y un error de preparación se investigan de forma distinta.')
    return result.returncode
if __name__=='__main__':
    p=argparse.ArgumentParser(description='Ejecutar pruebas y conservar evidencia de cada ejecución.')
    p.add_argument('mode',choices=['karate','schemathesis'])
    p.add_argument('--start-api',action='store_true',help='Inicia una API temporal y la detiene al terminar; el puerto 8000 debe estar libre.')
    p.add_argument('--tag',help='Tag exacto de Karate, por ejemplo @HU-G4-01 o @G4-004.')
    p.add_argument('--list-tags',action='store_true',help='Muestra archivos y sus etiquetas, sin iniciar ni consultar la API.')
    p.add_argument('--scope',choices=['all','g4'],default='all',help='all incluye G4 y núcleo común; g4 selecciona solo features hu-g4-*.')
    a=p.parse_args()
    if a.mode != 'karate' and (a.tag or a.scope != 'all' or a.list_tags):
        p.error('--tag, --scope y --list-tags se utilizan solo con karate')
    if a.list_tags:
        selected=(ROOT/'features').glob('hu-g4-*.feature') if a.scope=='g4' else (ROOT/'features').rglob('*.feature')
        for path in sorted(selected):
            tags=sorted({tag for line in path.read_text(encoding='utf-8').splitlines() if line.lstrip().startswith('@') for tag in line.split() if tag.startswith('@')})
            if tags and tags != ['@ignore']:
                print(str(path.relative_to(ROOT))+': '+', '.join(tags))
        sys.exit(0)
    if a.tag and (not a.tag.startswith('@') or any(c.isspace() for c in a.tag) or ',' in a.tag or '~' in a.tag):
        p.error('--tag debe ser un único tag, por ejemplo @HU-G4-01')
    if a.tag:
        selected=(ROOT/'features').glob('hu-g4-*.feature') if a.scope=='g4' else (ROOT/'features').rglob('*.feature')
        if not any(a.tag in text.split() for path in selected for text in path.read_text(encoding='utf-8').splitlines() if text.lstrip().startswith('@')):
            p.error('El tag no existe en el alcance elegido. Revisa el encabezado de la HU o del escenario.')
    proc=None
    try:
        if a.start_api:
            with socket.socket() as sock:
                if sock.connect_ex(('127.0.0.1',8000))==0:
                    raise SystemExit('El puerto 8000 ya está ocupado. --start-api no reutiliza otra instancia; libera el puerto o ejecuta sin esa opción conscientemente.')
            proc=subprocess.Popen([sys.executable,str(ROOT/'scripts/serve_api.py')],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            for _ in range(180):
                if proc.poll() is not None:raise SystemExit('La API iniciada terminó antes de estar disponible')
                try: api('/openapi.json');break
                except Exception: time.sleep(1)
            else: raise SystemExit('La API no estuvo disponible en 180 segundos')
        sys.exit(run(a.mode,a.tag,a.scope))
    except (OSError, urllib.error.URLError) as error:
        raise SystemExit(f'No se pudo ejecutar la prueba: {error}. Comprueba el entorno y que la API esté disponible en http://127.0.0.1:8000/docs.')
    finally:
        if proc and proc.poll() is None: proc.terminate();proc.wait(timeout=15)
