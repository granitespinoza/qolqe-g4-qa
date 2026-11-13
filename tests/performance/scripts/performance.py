"""Ejecución reproducible de Parte 3. Sin modificar Qolqe ni reutilizar sus bases locales."""
from __future__ import annotations
import argparse,csv,hashlib,json,os,platform,random,shutil,socket,sqlite3,subprocess,sys,threading,time
from datetime import datetime,timedelta,timezone
from pathlib import Path
import psutil,requests
ROOT=Path(__file__).resolve().parents[3]
PERF=ROOT/'tests/performance'
CFG=json.loads((PERF/'configuracion/modelo.json').read_text(encoding='utf-8'))
GIT=shutil.which('git') or str(Path.home()/'.cache/codex-runtimes/codex-primary-runtime/dependencies/native/git/cmd/git.exe')
def git(*args,cwd=ROOT):
    return subprocess.check_output([GIT,'-C',str(cwd),*args],text=True).strip()
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def percentile(a,p):
    if not a:return None
    a=sorted(a);i=(len(a)-1)*p/100;lo=int(i);hi=min(lo+1,len(a)-1)
    return a[lo]+(a[hi]-a[lo])*(i-lo)
def configure(db):
    os.environ['QOLQE_BD']=str(db);os.environ['QOLQE_BD_PLANTILLA']=str(ROOT/'.tools/performance/plantilla.db');os.environ['QOLQE_MODO_PRUEBA']='1'
    sys.path.insert(0,str(ROOT/'referencias/qolqe-wallet'))
    from qolqe import config
    config.RUTA_BD=Path(db);config.RUTA_PLANTILLA=ROOT/'.tools/performance/plantilla.db'
def prepare(db,n):
    configure(db)
    from qolqe import reloj
    from qolqe.semilla import reiniciar_datos
    from qolqe.credenciales import hash_pin
    reiniciar_datos()
    c=sqlite3.connect(db);c.row_factory=sqlite3.Row
    now=reloj.a_texto(reloj.ahora());date=(reloj.hoy()+timedelta(days=30)).isoformat();pin_hash=hash_pin('2580');users=[]
    for v in range(1,n+1):
        uid=10000+v;dest=20000+v;cell=str(910000000+v);destcell=str(930000000+v)
        for ident,phone,name in [(uid,cell,f'Carga {v}'),(dest,destcell,f'Destino {v}')]:
            c.execute('INSERT INTO usuarios(id,dni,nombres,celular,pin_hash,creado_en) VALUES(?,?,?,?,?,?)',(ident,str(80000000+ident),name,phone,pin_hash,now))
            c.execute('INSERT INTO cuentas VALUES(?,?,?)',(ident,CFG['saldo_centimos'],now))
            c.execute('INSERT INTO limites(usuario_id,limite_diario_cent) VALUES(?,200000)',(ident,))
        c.execute('INSERT INTO contactos(usuario_id,contacto_usuario_id,alias,favorito,creado_en) VALUES(?,?,?,0,?)',(uid,dest,f'Contacto {v}',now))
        supply=str(80000000+v);q_supply=str(85000000+v);debts=[]
        for k in range(CFG['deudas_por_usuario']+1):
            q=q_supply if k==CFG['deudas_por_usuario'] else supply
            cur=c.execute('INSERT INTO deudas(empresa,suministro,titular,periodo,monto_cent,vencimiento) VALUES(?,?,?,?,?,?)',('ELECTRO',q,f'Carga {v}','2026-12',100,date))
            if q==supply:debts.append(cur.lastrowid)
        old=reloj.a_texto(reloj.ahora()-timedelta(days=2))
        c.executemany('INSERT INTO movimientos(usuario_id,codigo_operacion,tipo,descripcion,monto_cent,importe_cent,fecha) VALUES(?,?,?,?,?,?,?)',
            [(uid,f'HIST-{v}-{j}','TRANSFERENCIA_RECIBIDA','Historial sintético',100,100,old)for j in range(CFG['historial_por_usuario'])])
        users.append(dict(vu=v,uid=uid,cell=cell,pin='2580',dest_uid=dest,dest_cell=destcell,debts=debts,query_supply=q_supply,initial_cent=CFG['saldo_centimos']))
    c.commit();c.close();return dict(users=users,created_at=now,history_per_user=CFG['historial_por_usuario'],debts_per_user=CFG['deudas_por_usuario'])
def reconcile(db,fixture,events,out):
    c=sqlite3.connect(db);c.row_factory=sqlite3.Row
    money=[e for e in events if e.get('clase')=='dinero'];issues=[];details=[]
    expected={u['uid']:u['initial_cent']for u in fixture['users']};expected.update({u['dest_uid']:u['initial_cent']for u in fixture['users']})
    seen_codes=set();confirmed=0;after_error=0
    for e in money:
        u=fixture['users'][e['vu']-1];op=e['op'];uid=u['uid']
        if op=='transferencias':rows=c.execute('SELECT * FROM transferencias WHERE origen_id=? AND descripcion=?',(uid,e['description'])).fetchall()
        elif op=='recargas':rows=c.execute('SELECT * FROM recargas WHERE usuario_id=? AND celular=?',(uid,e['cell'])).fetchall()
        else:rows=c.execute('SELECT * FROM pagos_servicio WHERE usuario_id=? AND deuda_id=?',(uid,e['debt_id'])).fetchall()
        item=dict(vu=e['vu'],seq=e['seq'],op=op,http_ok=e['ok'],records=len(rows),codes=[r['codigo_operacion']for r in rows])
        if len(rows)>1:issues.append(dict(kind='duplicated_operation',**item))
        if e['ok'] and len(rows)!=1:issues.append(dict(kind='confirmed_without_single_record',**item))
        if not e['ok'] and rows:after_error+=1
        if len(rows)==1:
            r=rows[0];cod=r['codigo_operacion'];confirmed+=1
            if cod in seen_codes:issues.append(dict(kind='duplicate_code',**item))
            seen_codes.add(cod)
            if e['ok'] and cod not in e.get('codes',[]):issues.append(dict(kind='response_code_mismatch',**item))
            movements=c.execute('SELECT usuario_id,importe_cent FROM movimientos WHERE codigo_operacion=?',(cod,)).fetchall()
            if op=='transferencias':
                amount=r['monto_cent'];cost=amount+r['comision_cent'];expected[uid]-=cost;expected[u['dest_uid']]+=amount
                want=sorted([(uid,-cost),(u['dest_uid'],amount)])
                if r['destino_id']!=u['dest_uid'] or amount!=e['amount_cent']:issues.append(dict(kind='wrong_transfer',**item))
            else:
                cost=r['monto_cent'] if op=='recargas' else r['total_cent'];expected[uid]-=cost;want=[(uid,-cost)]
                if cost!=e['amount_cent']:issues.append(dict(kind='wrong_amount',**item))
                if op=='pagos' and c.execute('SELECT estado FROM deudas WHERE id=?',(e['debt_id'],)).fetchone()[0]!='PAGADA':issues.append(dict(kind='debt_not_paid',**item))
            if sorted((r['usuario_id'],r['importe_cent'])for r in movements)!=want:issues.append(dict(kind='partial_movements',**item))
        elif op=='pagos':
            if c.execute('SELECT estado FROM deudas WHERE id=?',(e['debt_id'],)).fetchone()[0]!='PENDIENTE':issues.append(dict(kind='debt_changed_without_payment',**item))
        details.append(item)
    with (out/'saldos.csv').open('w',newline='',encoding='utf-8')as f:
        w=csv.writer(f);w.writerow(['usuario_id','inicial_cent','esperado_cent','observado_cent','coincide'])
        for uid,val in expected.items():
            actual=c.execute('SELECT saldo_cent FROM cuentas WHERE usuario_id=?',(uid,)).fetchone()[0]
            w.writerow([uid,CFG['saldo_centimos'],val,actual,val==actual])
            if actual!=val:issues.append(dict(kind='balance_mismatch',uid=uid,expected=val,actual=actual))
    # Also detect rows created without an event journal entry.
    actual_total=sum(c.execute(f'SELECT count(*) FROM {t} WHERE {field} BETWEEN 10001 AND 10600').fetchone()[0]for t,field in [('transferencias','origen_id'),('recargas','usuario_id'),('pagos_servicio','usuario_id')])
    if actual_total!=sum(d['records']for d in details):issues.append(dict(kind='unjournaled_monetary_records',database_records=actual_total,journal_matched=sum(d['records']for d in details)))
    movement_codes={r[0]for r in c.execute("SELECT DISTINCT codigo_operacion FROM movimientos WHERE (usuario_id BETWEEN 10001 AND 10600 OR usuario_id BETWEEN 20001 AND 20600) AND codigo_operacion NOT LIKE 'HIST-%'")}
    for code in sorted(movement_codes-seen_codes):issues.append(dict(kind='orphan_movement',code=code))
    c.close()
    write(out/'operaciones_monetarias.json',details)
    result=dict(approved=not issues,attempts=len(money),database_operations=actual_total,confirmed_records=confirmed,committed_after_http_error=after_error,issues=issues)
    write(out/'integridad.json',result);return result
def analyze(events,resources,profile,meta,integrity,out):
    conf=CFG['perfiles'][profile];start=meta.get('measurement_epoch',meta['k6_started_epoch']);windows=conf['steady'];groups={};window_results=[]
    def stats(es,seconds):
        ops=[e for e in es if e['op']!='login'];req=sum(len(e['statuses'])for e in es)
        return dict(operations=len(ops),requests=req,login=sum(e['op']=='login'for e in es),ops_s=sum(e['ok']for e in ops)/seconds,all_ops_s=len(ops)/seconds,req_s=req/seconds,
          error_rate=sum(not e['ok']for e in ops)/len(ops)if ops else None,login_error_rate=sum(not e['ok']for e in es if e['op']=='login')/max(1,sum(e['op']=='login'for e in es)),
          p95_consulta=percentile([e['ms']for e in es if e['clase']=='consulta'],95),p95_dinero=percentile([e['ms']for e in es if e['clase']=='dinero'],95))
    for a,b in windows:
        es=[e for e in events if a<=e['at']/1000-start<b]
        st=stats(es,b-a);st.update(start_s=a,end_s=b)
        st['latency_ok']=st['p95_consulta']is not None and st['p95_dinero']is not None and st['p95_consulta']<800 and st['p95_dinero']<1500
        st['error_ok']=st['error_rate']is not None and st['error_rate']<=.01 and st['login_error_rate']<=.01
        st['by_operation']={op:dict(count=len(a),p95=percentile([e['ms']for e in a],95),error_rate=sum(not e['ok']for e in a)/len(a))for op in sorted({e['op']for e in es})if(a:=[e for e in es if e['op']==op])}
        st['per_operation_ok']=all(v['p95']<(1500 if op in ['transferencias','recargas','pagos']else 800) and v['error_rate']<=.01 for op,v in st['by_operation'].items()) and all(k in st['by_operation']for k in CFG['distribucion']) and 'login'in st['by_operation']
        window_results.append(st)
    selected=[e for e in events if any(a<=e['at']/1000-start<b for a,b in windows)]
    for op in sorted({e['op']for e in selected}):
        es=[e for e in selected if e['op']==op];dur=[e['ms']for e in es]
        groups[op]=dict(count=len(es),errors=sum(not e['ok']for e in es),p50=percentile(dur,50),p95=percentile(dur,95),p99=percentile(dur,99),max=max(dur),share=sum(e['op']==op for e in selected)/max(1,sum(e['op']!='login'for e in selected))*100 if op!='login'else None)
    sample=[r for r in resources if any(a<=r['epoch']-start<b for a,b in windows)]
    valid=bool(events)and meta['k6_completed']and bool(sample)and max([r['generator_cpu_host_pct']for r in resources]or[100])<80
    if any(any(code in [401,403,404,409,422,423]for code in e['statuses'])for e in selected):valid=False
    # Every critical group must have samples. Per-operation SLAs, not an aggregate that hides endpoints.
    per_op_ok=all(v['p95']<(1500 if op in ['transferencias','recargas','pagos']else 800)for op,v in groups.items())and all(k in groups for k in CFG['distribucion'])and 'login'in groups
    approx_volume=window_results[0]['ops_s']>=5 if conf['expected_ops_s'] else None
    approved=valid and per_op_ok and all(w['error_ok']for w in window_results)and integrity['approved']and (approx_volume is not False)
    result=dict(profile=profile,valid=valid,approved=approved,criteria='campaña: integridad obligatoria; latencia/error comparados con referencia normal, sin SLA numérico de campaña'if profile=='campana'else 'p95 por operación, error <=1%; carga normal >=5 operaciones/s',
        meta=meta,windows=window_results,by_operation=groups,integrity=integrity,throughput_normal_ok=approx_volume,
        resources=dict(samples=len(resources),app_cpu_host_max=max([r['app_cpu_host_pct']for r in resources]or[0]),generator_cpu_host_max=max([r['generator_cpu_host_pct']for r in resources]or[0]),app_rss_mb_max=max([r['app_rss_mb']for r in resources]or[0])),
        errors=[e for e in events if not e['ok']])
    if profile=='campana':result['approved']=valid and integrity['approved'];result['normal_reference_met']=per_op_ok and all(w['error_ok']for w in window_results)
    write(out/'resumen.json',result);return result
def run(profile):
    ref=ROOT/'referencias/qolqe-wallet'
    with socket.socket()as probe:
        probe.settimeout(.5)
        if probe.connect_ex(('127.0.0.1',8021))==0:raise RuntimeError('Puerto 8021 ocupado: cerrar la instancia anterior antes de ejecutar')
    if git('status','--porcelain',cwd=ref):raise RuntimeError('Qolqe original tiene cambios: no ejecutar hasta aclararlos')
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ');out=PERF/'resultados'/f'{stamp}-{profile}';out.mkdir(parents=True,exist_ok=False)
    runtime=ROOT/'.tools/performance'/out.name;runtime.mkdir(parents=True,exist_ok=False);db=runtime/'qolqe.db'
    n=max(s['target']for s in CFG['perfiles'][profile]['stages'])
    print(f'[{profile}] preparando {n} usuarios exclusivos...',flush=True)
    fixture=prepare(db,n);write(out/'datos.json',fixture)
    write(out/'configuracion.json',dict(profile=CFG['perfiles'][profile],model=CFG))
    k6s=list((ROOT/'.tools/performance').rglob('k6.exe'))
    k6=shutil.which('k6')or(str(k6s[0])if k6s else None)
    if not k6:raise RuntimeError('Instalar k6 o ejecutar scripts/performance.ps1 install')
    env=os.environ.copy();env.update(PERF_PORT='8021',PERF_URL='http://127.0.0.1:8021',PERF_PROFILE=profile,PERF_DATA=str(out/'datos.json'),PERF_SUMMARY=str(out/'k6-summary.json'),K6_NO_USAGE_REPORT='true')
    log=(out/'servidor.log').open('w',encoding='utf-8');server=subprocess.Popen([sys.executable,str(PERF/'scripts/server.py')],env=env,stdout=log,stderr=log)
    runner=None;resources=[];events=[];stop=threading.Event()
    try:
        for _ in range(120):
            if server.poll()is not None:raise RuntimeError('Servidor no inicia; ver servidor.log')
            try:
                if requests.get(env['PERF_URL']+'/openapi.json',timeout=1).ok:break
            except requests.RequestException:pass
            time.sleep(.5)
        else:raise RuntimeError('Servidor no disponible')
        # Verify all workload paths with one user, outside the measured phase.
        u=fixture['users'][0];rr=requests.post(env['PERF_URL']+'/api/auth/login',json={'celular':u['cell'],'pin':u['pin']},timeout=10);rr.raise_for_status()
        hdr={'Authorization':'Bearer '+rr.json()['access_token']}
        paths=['/api/cuentas/me/saldo','/api/cuentas/me','/api/movimientos?pagina=1','/api/contactos?buscar=Contacto','/api/servicios/deudas?empresa=ELECTRO&suministro='+u['query_supply'],'/api/limites','/api/limites/alertas','/api/solicitudes','/api/seguridad/dispositivos','/api/seguridad/sesiones']
        preflight=[]
        for path in paths:
            r=requests.get(env['PERF_URL']+path,headers=hdr,timeout=10);preflight.append({'path':path,'status':r.status_code})
            if r.status_code!=200:raise RuntimeError(f'Precondición inválida: {path} {r.status_code}: {r.text}')
        write(out/'preflight.json',preflight)
        meta=dict(profile=profile,run_id=out.name,qa_revision=git('rev-parse','HEAD'),qa_dirty=bool(git('status','--porcelain')),reference_commit=git('rev-parse','HEAD',cwd=ref),
          platform=platform.platform(),python=sys.version,server_pid=server.pid,logical_cpus=psutil.cpu_count(),physical_cpus=psutil.cpu_count(logical=False),memory_gb=round(psutil.virtual_memory().total/1e9,2),
          k6_version=subprocess.check_output([k6,'version'],text=True).strip(),target_vus=n,server_workers=1,source_hashes={str(p.relative_to(ROOT)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest()for p in PERF.rglob('*')if p.is_file()and 'resultados'not in p.parts and p.suffix in ['.py','.js','.json']},k6_started_epoch=time.time())
        runner=subprocess.Popen([k6,'run','--quiet','--log-format','raw',str(PERF/'escenarios/carga.js')],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',bufsize=1)
        app=psutil.Process(server.pid);gen=psutil.Process(runner.pid);app.cpu_percent();gen.cpu_percent();cpus=psutil.cpu_count()
        def monitor():
            with(out/'recursos.csv').open('w',newline='',encoding='utf-8')as f:
                w=csv.DictWriter(f,fieldnames=['epoch','elapsed_s','app_cpu_host_pct','app_cpu_core_pct','app_rss_mb','generator_cpu_host_pct','generator_cpu_core_pct','generator_rss_mb','host_cpu_pct','host_memory_pct']);w.writeheader()
                while not stop.wait(1):
                    try:
                        children=app.children(recursive=True)
                        for proc in children:
                            if proc.pid not in tracked:
                                proc.cpu_percent();tracked[proc.pid]=proc
                        ac=sum(proc.cpu_percent()for proc in tracked.values()if proc.is_running());gc=gen.cpu_percent();row=dict(epoch=time.time(),elapsed_s=time.time()-meta['k6_started_epoch'],app_cpu_host_pct=ac/cpus,app_cpu_core_pct=ac,app_rss_mb=sum(proc.memory_info().rss for proc in tracked.values()if proc.is_running())/1e6,generator_cpu_host_pct=gc/cpus,generator_cpu_core_pct=gc,generator_rss_mb=gen.memory_info().rss/1e6,host_cpu_pct=psutil.cpu_percent(),host_memory_pct=psutil.virtual_memory().percent)
                        resources.append(row);w.writerow(row);f.flush()
                    except psutil.Error:break
        tracked={app.pid:app};thread=threading.Thread(target=monitor,daemon=True);thread.start()
        print(f'[{profile}] ejecutando k6. Reportes: {out.relative_to(ROOT)}',flush=True)
        with(out/'k6.log').open('w',encoding='utf-8')as f,(out/'operaciones.jsonl').open('w',encoding='utf-8')as journal:
            for line in runner.stdout:
                if 'PERF 'in line:
                    try:
                        event=json.loads(line.split('PERF ',1)[1]);events.append(event);
                        if profile=='demo':print(f"VU {event['vu']} | {event['op']} | HTTP {event['statuses']} | {event['ms']} ms | correcto={event['ok']}",flush=True)
                        journal.write(json.dumps(event,ensure_ascii=False)+'\n');journal.flush()
                    except json.JSONDecodeError:f.write(line)
                else:f.write(line)
        code=runner.wait();stop.set();thread.join(timeout=3)
        meta.update(measurement_epoch=(events[0]['at']/1000-events[0]['elapsed_s'])if events else meta['k6_started_epoch'],k6_exit_code=code,k6_completed=code in [0,99]and(out/'k6-summary.json').exists(),finished_epoch=time.time())
        write(out/'procedencia.json',meta)
    finally:
        stop.set()
        if runner is not None and runner.poll()is None:runner.terminate();runner.wait(timeout=15)
        try:
            descendants=psutil.Process(server.pid).children(recursive=True)
        except psutil.Error:descendants=[]
        for child in descendants:
            try:child.terminate()
            except psutil.Error:pass
        server.terminate()
        try:server.wait(timeout=15)
        except subprocess.TimeoutExpired:server.kill();server.wait()
        psutil.wait_procs(descendants,timeout=10)
        log.close()
    integrity=reconcile(db,fixture,events,out)
    result=analyze(events,resources,profile,meta,integrity,out)
    # Keep databases only for anomalies; remove only the newly created owned files after reconciliation.
    if integrity['approved']:
        for name in ['qolqe.db','qolqe.db-wal','qolqe.db-shm']:
            file=runtime/name
            if file.parent.resolve()==runtime.resolve():file.unlink(missing_ok=True)
    else:result['database_evidence']=str(db.relative_to(ROOT));write(out/'resumen.json',result)
    write(PERF/'resultados'/f'latest-{profile}.json',{'dir':str(out.relative_to(ROOT))})
    print(json.dumps({'profile':profile,'valid':result['valid'],'approved':result['approved'],'integrity':integrity['approved'],'events':len(events),'dir':str(out.relative_to(ROOT))},ensure_ascii=False),flush=True)
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('profile',choices=list(CFG['perfiles'])+['all']);args=ap.parse_args()
    invalid=False
    for p in (['referencia','carga','campana','estres']if args.profile=='all'else[args.profile]):
        result=run(p);invalid=invalid or not result['valid']
    sys.exit(2 if invalid else 0)
