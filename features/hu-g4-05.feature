# language: en
@HU-G4-05 @api
Feature: HU-G4-05 — comportamiento verificable
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

  @G4-032 @CA1
  Scenario: Transferir por contacto acredita ambos saldos
    # HU-N-07 | Comprobación de efectos | Cuenta origen 100, destino 0; transferencia 10 y SMS.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'100.00'}, null, {})
    * def r = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
    * match r.statusCode == 201
    * match r.result.saldo == '90.00'
    * match r.result.comision == '0.00'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
    * match r.result.saldo == '10.00'
    * def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:b.cell})
    * assert r.result.length >= 2

  @G4-033 @CA1
  Scenario: Saldo insuficiente no produce transferencia
    # RN-08 | Particiones de equivalencia | Saldo cero y monto válido; no confundir con monto inválido.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'SALDO_INSUFICIENTE'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result.saldo == '0.00'

  @G4-095 @CA1
  Scenario: Límite diario agotado impide operación
    # RN-06 | Tabla de decisiones | Saldo suficiente pero límite agotado: aislar rechazo diario.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
    * def r = req('/api/limites', 'PUT', {limite_diario:'100.00'}, a.token, {})
    * match r.statusCode == 200
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'100.00'}, a.token, {})
    * match r.statusCode == 201
    * def r = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'LIMITE_DIARIO_EXCEDIDO'
