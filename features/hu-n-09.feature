# language: en
@HU-N-09 @api
Feature: HU-N-09 — comportamiento verificable
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

  @G4-089 @CA1
  Scenario: Simular comisión para 1.00 sin debitar
    # RN-09 | Particiones de equivalencia | Mínimo, proporcional y máximo; saldo no cambia.
    * def r = req('/api/transferencias/comision', 'GET', null, a.token, {monto:'1.00',tipo:'INTERBANCARIA'})
    * match r.statusCode == 200
    * match r.result.comision == '1.00'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result.saldo == '0.00'

  @G4-090 @CA1
  Scenario: Simular comisión para 100.00 sin debitar
    # RN-09 | Particiones de equivalencia | Mínimo, proporcional y máximo; saldo no cambia.
    * def r = req('/api/transferencias/comision', 'GET', null, a.token, {monto:'100.00',tipo:'INTERBANCARIA'})
    * match r.statusCode == 200
    * match r.result.comision == '1.50'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result.saldo == '0.00'

  @G4-091 @CA1
  Scenario: Simular comisión para 500.00 sin debitar
    # RN-09 | Particiones de equivalencia | Mínimo, proporcional y máximo; saldo no cambia.
    * def r = req('/api/transferencias/comision', 'GET', null, a.token, {monto:'500.00',tipo:'INTERBANCARIA'})
    * match r.statusCode == 200
    * match r.result.comision == '5.00'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result.saldo == '0.00'
