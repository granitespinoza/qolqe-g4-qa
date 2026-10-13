"""Ejecuta Karate o Schemathesis y conserva códigos de salida reales."""
from pathlib import Path
import argparse, json, os, shutil, subprocess, sys, time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
def api(route, body=None):
    request=urllib.request.Request('http://127.0.0.1:8000'+route,data=json.dumps(body).encode() if body is not None else None,headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(request, timeout=15) as r: return json.load(r)
def run(mode):
    if mode=='karate':
        java=shutil.which('java') or next((str(p) for p in (ROOT/'.tools/java').rglob('java.exe')),None)
        if not java: raise SystemExit('Falta Java 17: ejecutar scripts/bootstrap.ps1')
        args=[java,'-DqaPython='+sys.executable,'-cp',str(ROOT/'.tools/karate.jar')+os.pathsep+str(ROOT),'com.intuit.karate.Main','-T','1','-f','cucumber:json,junit:xml','-r','reports/raw/karate','features']
    else:
        # Usuario dedicado: no se imprimen ni guardan sus credenciales de sesión.
        n=str(time.time_ns()%90000000+10000000)
        api('/api/usuarios',{'dni':n,'celular':'9'+n,'nombres':'Contrato Prueba','pin':'4826'})
        token=api('/api/auth/login',{'celular':'9'+n,'pin':'4826'})['access_token']
        args=[str(Path(sys.executable).parent/('schemathesis.exe' if os.name=='nt' else 'schemathesis')),'run','http://127.0.0.1:8000/openapi.json','--include-path-regex','^/api/(contactos|solicitudes)(/|$)','--header','Authorization: Bearer '+token,'--phases','examples,coverage,fuzzing','--max-examples','20','--seed','20261013','--workers','1','--report','junit,ndjson','--report-dir','reports/raw/schemathesis']
    log=ROOT/'.tools'/f'{mode}.log'
    log.parent.mkdir(exist_ok=True)
    with log.open('w',encoding='utf-8') as f:
        env=os.environ.copy();env['PYTHONIOENCODING']='utf-8';env['PYTHONUTF8']='1'
        result=subprocess.run(args,cwd=ROOT,stdout=f,stderr=subprocess.STDOUT,env=env)
    print(f'{mode}: salida {result.returncode}; registro local {log}')
    return result.returncode
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['karate','schemathesis']);p.add_argument('--start-api',action='store_true');a=p.parse_args()
    proc=None
    try:
        if a.start_api:
            proc=subprocess.Popen([sys.executable,str(ROOT/'scripts/serve_api.py')],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            for _ in range(180):
                try: api('/openapi.json');break
                except Exception: time.sleep(1)
            else: raise SystemExit('La API no estuvo disponible en 180 segundos')
        sys.exit(run(a.mode))
    finally:
        if proc: proc.terminate();proc.wait(timeout=15)
