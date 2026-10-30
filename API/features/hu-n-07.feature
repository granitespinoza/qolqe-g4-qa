# language: en
@HU-N-07 @api
Feature: HU-N-07 — comportamiento verificable
  Como cliente de Qolqe
  Quiero operaciones que respeten las reglas
  Para conservar mis datos y mi dinero

Background:
  * def ctx = call read('classpath:API/features/support/setup.feature')
  * def http = ctx.http
  * def a = ctx.a
  * def b = ctx.b
  * def c = ctx.c
  * def add = ctx.add
  * def create = ctx.create
  * def random = ctx.random
  * def login = ctx.login
  * def requestMoney = ctx.requestMoney
  * def req = function(route, method, body, token, query){return karate.call('classpath:API/features/support/http.feature',{route:route,method:method,body:JSON.parse(JSON.stringify(body),function(k,v){return typeof v === 'string' && v.startsWith('#(') && v.endsWith(')') ? karate.eval(v.substring(2,v.length-1)) : v;}),token:token,query:query});}

  @G4-082 @CA1 @CA2 @TC-G4-082
  Scenario: Transferencia monto 0.00
    # RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'0.00'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'MONTO_INVALIDO'

  @G4-083 @CA1 @CA2 @TC-G4-083
  Scenario: Transferencia monto 0.01
    # RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'0.01'}, a.token, {})
    * match r.statusCode == 201

  @G4-084 @CA1 @CA2 @TC-G4-084
  Scenario: Transferencia monto 500.00
    # RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'500.00'}, a.token, {})
    * match r.statusCode == 201

  @G4-085 @CA1 @CA2 @TC-G4-085
  Scenario: Transferencia monto 500.01
    # RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'500.01'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'MONTO_INVALIDO'

  @G4-086 @CA1 @CA2 @TC-G4-086
  Scenario: Transferencia monto 10.005
    # RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'10.005'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'MONTO_INVALIDO'

  @G4-087 @CA3 @CA4 @TC-G4-087
  Scenario: Comprobante y movimientos con mismo código
    # RN-10 | Comprobación de efectos | Verificar transferencia en ambas cuentas.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'100.00'}, null, {})
    * def tx = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'10.00',descripcion:'Almuerzo'}, a.token, {})
    * match tx.statusCode == 201
    * match tx.result.total == '10.00'
    * match tx.result.saldo == '90.00'
    * def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, a.token, {})
    * match r.statusCode == 200
    * def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, b.token, {})
    * match r.statusCode == 200

  @G4-114 @CA2 @TC-G4-114
  Scenario: Transferencia a sí mismo rechazada
    # RN-07 | Particiones de equivalencia | Monto válido y saldo suficiente; aislar destino.
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(a.cell)',monto:'10.00'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'TRANSFERENCIA_A_SI_MISMO'

  @G4-116 @CA5 @TC-G4-116 @known_issue @D-05
  Scenario: Concurrencia conserva saldo y límite diario
    # RN-06/08 | Tabla de decisiones y concurrencia | Dos peticiones HTTP sincronizadas; comprobar límite y saldo por separado. Los reintentos de preparación, si ocurren, quedan en la evidencia.
    * def command = ['#(qaPython)', 'scripts/concurrency_probe.py']
    * def runProbe = function(args){var P=Java.type('java.lang.ProcessBuilder');var S=Java.type('java.util.Scanner');var p=new P(Java.to(args,'java.lang.String[]')).redirectErrorStream(true).start();var scan=new S(p.getInputStream()).useDelimiter('\\A');var out=scan.hasNext()?scan.next():'';var code=p.waitFor();if(code!=0) throw new Error('Preparación de concurrencia: '+out);return JSON.parse(out);}
    * def probe = runProbe(command)
    * eval karate.embed(probe, 'application/json')
    * match probe.ok == true
