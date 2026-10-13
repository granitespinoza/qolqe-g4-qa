"""Dos transferencias simultáneas: saldo y límite deben mantenerse bajo concurrencia."""
import concurrent.futures, json, threading, time, urllib.request, urllib.error
def request(route,method='GET',body=None,token=None):
    headers={'Content-Type':'application/json'}
    if token:headers['Authorization']='Bearer '+token
    r=urllib.request.Request('http://127.0.0.1:8000'+route,method=method,data=json.dumps(body).encode() if body is not None else None,headers=headers)
    try:
        with urllib.request.urlopen(r,timeout=20) as resp:return resp.status,json.load(resp)
    except urllib.error.HTTPError as e:return e.code,json.load(e)
def user():
    n=str(time.time_ns()%90000000+10000000)
    cell='9'+n
    status,r=request('/api/usuarios','POST',{'dni':n,'nombres':'Concurrencia Prueba','celular':cell,'pin':'4826'})
    assert status==201,(status,r)
    status,r=request('/api/auth/login','POST',{'celular':cell,'pin':'4826'})
    assert status==200,(status,r)
    return cell,r['access_token']
def probe(balance,limit):
    cell,token=user();dst,_=user()
    status,r=request('/api/pruebas/saldo','PUT',{'celular':cell,'saldo':balance});assert status==200,(status,r)
    status,r=request('/api/limites','PUT',{'limite_diario':limit},token);assert status==200,(status,r)
    barrier=threading.Barrier(2)
    def transfer(_):
        barrier.wait(timeout=10)
        return request('/api/transferencias','POST',{'celular_destino':dst,'monto':'400.00'},token)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(transfer,range(2)))
    status,saldo=request('/api/cuentas/me/saldo',token=token)
    status,limits=request('/api/limites',token=token)
    successes=sum(s==201 for s,r in results)
    ok=successes==1 and float(saldo['saldo'])>=0 and float(limits['usado_hoy'])<=float(limit)
    return dict(initial_balance=balance,limit=limit,responses=results,successes=successes,saldo=saldo,limits=limits,ok=ok)
if __name__=='__main__':
    result={'saldo':probe('500.00','2000.00'),'limite':probe('2000.00','500.00')}
    result['ok']=all(v['ok'] for v in result.values())
    print(json.dumps(result,ensure_ascii=True))
