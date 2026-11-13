"""Diagnóstico posterior a la carga; instrumenta una conexión de prueba, no modifica Qolqe."""
import csv,hashlib,json,sqlite3,statistics,time
from pathlib import Path
from performance import ROOT,PERF,prepare
def main():
    runtime=ROOT/'.tools/performance/diagnostico-sql';runtime.mkdir(parents=True,exist_ok=True)
    db=runtime/'qolqe.db'
    if db.exists():raise RuntimeError('El diagnóstico ya tiene base: conservar o usar una carpeta nueva antes de repetir')
    fixture=prepare(db,1)
    from qolqe.api.movimientos import listar
    from qolqe.dependencias import UsuarioActual
    c=sqlite3.connect(db);c.row_factory=sqlite3.Row
    owner=UsuarioActual(10001,'910000001','Carga 1','diagnostico',0,1)
    original=c.execute('SELECT * FROM movimientos WHERE usuario_id=10001').fetchall()
    columns=list(original[0].keys());rows=[]
    for n in [100,1000]:
        c.execute('DELETE FROM movimientos WHERE usuario_id=10001')
        c.executemany('INSERT INTO movimientos('+','.join(columns)+') VALUES('+','.join('?'for _ in columns)+')',[tuple(r)for r in original[:n]]);c.commit()
        # Warm-up excluded from measurements.
        listar(desde=None,hasta=None,tipo=None,categoria_id=None,pagina=1,usuario=owner,bd=c)
        for rep in range(3):
            statements=[];c.set_trace_callback(statements.append);start=time.perf_counter()
            answer=listar(desde=None,hasta=None,tipo=None,categoria_id=None,pagina=1,usuario=owner,bd=c)
            elapsed=(time.perf_counter()-start)*1000;c.set_trace_callback(None)
            rows.append(dict(historial=n,repeticion=rep+1,total_select=sum(s.lstrip().upper().startswith('SELECT')for s in statements),sumas_por_movimiento=sum('SUM(importe_cent)'in s for s in statements),filas_respuesta=len(answer.movimientos),ms=elapsed))
    c.close()
    source=ROOT/'referencias/qolqe-wallet/qolqe/api/movimientos.py';s=source.read_text(encoding='utf-8')
    result=dict(method='Llamada directa a listar() original en una base exclusiva; mismo código y datos sintéticos. Una conexión instrumentada con set_trace_callback; calentamiento excluido y tres repeticiones. No es una segunda prueba HTTP ni demuestra por sí sola la causa total del estrés.',source='qolqe/api/movimientos.py',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
      observed='El endpoint obtiene el historial completo, ejecuta una consulta SUM por fila y pagina después. Patrón N+1 confirmado en este diagnóstico; contribución al límite bajo carga es una hipótesis respaldada por latencias por endpoint.',rows=rows,summary=[dict(historial=n,mediana_ms=statistics.median(r['ms']for r in rows if r['historial']==n),selects=next(r['total_select']for r in rows if r['historial']==n),sumas=next(r['sumas_por_movimiento']for r in rows if r['historial']==n))for n in [100,1000]],recommendation='Proponer paginación en SQL y cálculo de saldos acumulados sin una consulta por movimiento. Validar después con el mismo modelo. No se implementa cambio en Qolqe.')
    out=PERF/'resultados';(out/'diagnostico-sql.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    with(out/'diagnostico-sql.csv').open('w',newline='',encoding='utf-8')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    for name in ['qolqe.db','qolqe.db-wal','qolqe.db-shm']:(runtime/name).unlink(missing_ok=True)
    print(json.dumps(result['summary'],ensure_ascii=False,indent=2))
if __name__=='__main__':main()
