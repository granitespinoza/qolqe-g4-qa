import http from 'k6/http';
import { sleep, check } from 'k6';
import { Counter, Rate, Trend } from 'k6/metrics';
import exec from 'k6/execution';
import { SharedArray } from 'k6/data';
const cfg=JSON.parse(open('../configuracion/modelo.json'));
const users=new SharedArray('usuarios',()=>JSON.parse(open(__ENV.PERF_DATA)).users);
const profile=cfg.perfiles[__ENV.PERF_PROFILE];
const duration=new Trend('operacion_ms',true), errors=new Rate('operacion_error'), count=new Counter('operaciones_negocio');
export const options={scenarios:{wallet:{executor:'ramping-vus',startVUs:__ENV.PERF_PROFILE==='referencia'?1:0,stages:profile.stages,gracefulRampDown:'150s',gracefulStop:'150s'}},
  thresholds:{'operacion_ms{clase:consulta}':['p(95)<800'],'operacion_ms{clase:dinero}':['p(95)<1500'],'operacion_error':['rate<=0.01']},
  summaryTrendStats:['avg','min','med','p(90)','p(95)','p(99)','max'],discardResponseBodies:false};
let rng=0;
function rand(){rng=(Math.imul(1664525,rng)+1013904223)>>>0;return rng/4294967296;}
function think(){const {min:a,mode:c,max:b}=cfg.think_time;const u=rand(),p=(c-a)/(b-a);return u<p?a+Math.sqrt(u*(b-a)*(c-a)):b-Math.sqrt((1-u)*(b-a)*(b-c));}
let token='',seq=0,paid=0,session=0;
function request(method,path,body,op,clase,expected,meta={}){
  const params={headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},timeout:'30s',tags:{name:op,clase}};
  const r=http.request(method,__ENV.PERF_URL+path,body===null?null:JSON.stringify(body),params);
  let j={};try{j=r.json();}catch(_){}
  const ok=r.status===expected;
  check(r,{[op+' status esperado']:()=>ok});
  return {r,j,ok};
}
function emit(op,clase,begin,results,meta={}){
  const ms=Date.now()-begin,ok=results.every(x=>x.ok);
  duration.add(ms,{op,clase});errors.add(!ok,{op,clase});if(op!=='login')count.add(1,{op});
  console.log('PERF '+JSON.stringify({at:Date.now(),elapsed_s:exec.instance.currentTestRunDuration/1000,active_vus:exec.instance.vusActive,vu:exec.vu.idInTest,session,seq,op,clase,ms,ok,
    statuses:results.map(x=>x.r.status),codigos:results.map(x=>x.j.codigo||null),
    codes:results.map(x=>x.j.codigo_operacion||null),...meta}));
  return ok;
}
const weights=Object.entries(cfg.distribucion);
function choose(){const r=rand()*100;let a=0;for(const [k,w]of weights){a+=w;if(r<a)return k;}return 'otros';}
export default function(){
  if(!rng)rng=cfg.seed+exec.vu.idInTest*7919;
  const u=users[exec.vu.idInTest-1];if(!u)throw Error('VU sin usuario exclusivo');
  session++;let t=Date.now();
  const login=request('POST','/api/auth/login',{celular:u.cell,pin:u.pin},'login','consulta',200);
  emit('login','consulta',t,[login]);token=login.j.access_token||'';
  if(!token){sleep(think());return;}
  for(let i=0;i<6;i++){
    sleep(think());seq++;let op=choose(),clase=['transferencias','recargas','pagos'].includes(op)?'dinero':'consulta';
    let r=[],meta={};t=Date.now();
    if(op==='saldo_perfil'){
      r=[request('GET','/api/cuentas/me/saldo',null,op,clase,200),request('GET','/api/cuentas/me',null,op,clase,200)];
    }else if(op==='movimientos')r=[request('GET','/api/movimientos?pagina=1',null,op,clase,200)];
    else if(op==='contactos')r=[request('GET','/api/contactos?buscar=Contacto',null,op,clase,200)];
    else if(op==='transferencias'){
      meta={amount_cent:100,recipient:u.dest_uid,description:`PERF-${exec.vu.idInTest}-${seq}`};
      r=[request('POST','/api/transferencias',{tipo:'QOLQE',celular_destino:u.dest_cell,monto:'1.00',descripcion:meta.description},op,clase,201)];
    }else if(op==='recargas'){
      meta={amount_cent:500,cell:String(940000000+exec.vu.idInTest*1000+seq)};
      r=[request('POST','/api/recargas',{celular:meta.cell,monto:'5.00'},op,clase,201)];
    }else if(op==='deudas')r=[request('GET',`/api/servicios/deudas?empresa=ELECTRO&suministro=${u.query_supply}`,null,op,clase,200)];
    else if(op==='pagos'){
      if(paid>=u.debts.length)throw Error('Datos de pago agotados');
      meta={amount_cent:100,debt_id:u.debts[paid++]};
      r=[request('POST','/api/servicios/pagos',{deuda_id:meta.debt_id},op,clase,201)];
    }else{
      const paths=['/api/limites','/api/limites/alertas','/api/solicitudes','/api/seguridad/dispositivos','/api/seguridad/sesiones'];
      const path=paths[Math.floor(rand()*paths.length)];meta={path};r=[request('GET',path,null,op,clase,200)];
    }
    emit(op,clase,t,r,meta);
  }
}
export function handleSummary(data){return {[__ENV.PERF_SUMMARY]:JSON.stringify(data,null,2)};}
