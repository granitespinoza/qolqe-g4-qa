# language: en
@HU-N-08 @api
Feature: HU-N-08 — comportamiento verificable
  Como cliente de Qolqe
  Quiero operaciones que respeten las reglas
  Para conservar mis datos y mi dinero

Background:
  * def ctx = call read('classpath:features/support/setup.feature')
  * def http = ctx.http
  * def a = ctx.a
  * def b = ctx.b
  * def c = ctx.c
  * def add = ctx.add
  * def create = ctx.create
  * def random = ctx.random
  * def login = ctx.login
  * def requestMoney = ctx.requestMoney
  * def req = function(route, method, body, token, query){return karate.call('classpath:features/support/http.feature',{route:route,method:method,body:JSON.parse(JSON.stringify(body),function(k,v){return typeof v === 'string' && v.startsWith('#(') && v.endsWith(')') ? karate.eval(v.substring(2,v.length-1)) : v;}),token:token,query:query});}

  @G4-088 @CA1 @CA2 @CA3
  Scenario: Transferencia interbancaria cobra comisión y enmascara CCI
    # RN-09 | Comprobación de efectos | Monto 100: comisión 1.50; verificar CCI en movimiento.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'200.00'}, null, {})
    * def tx = req('/api/transferencias', 'POST', {tipo:'INTERBANCARIA',cci:'12345678901234567890',monto:'100.00'}, a.token, {})
    * match tx.statusCode == 201
    * match tx.result.comision == '1.50'
    * match tx.result.saldo == '98.50'
    * def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, a.token, {})
    * match r.statusCode == 200
    * match r.result.contraparte == '****************7890'

  @G4-115 @CA1
  Scenario: CCI inválido rechazado
    # HU-N-08 CA1 | Particiones de equivalencia | CCI corto con monto válido.
    * def r = req('/api/transferencias', 'POST', {tipo:'INTERBANCARIA',cci:'123',monto:'10.00'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'CCI_INVALIDO'
