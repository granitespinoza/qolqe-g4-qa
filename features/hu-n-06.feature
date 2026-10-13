# language: en
@HU-N-06 @api
Feature: HU-N-06 — comportamiento verificable
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

  @G4-080 @CA1 @CA2 @CA4
  Scenario: Cerrar cuenta con saldo cero revoca acceso
    # HU-N-06 | Transición de estados | Cierre válido y posterior login prohibido.
    * def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
    * match r.statusCode == 204
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.statusCode == 401
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
    * match r.statusCode == 401
    * match r.result.codigo == 'CUENTA_CERRADA'

  @G4-081 @CA3
  Scenario: Solicitud pendiente impide cerrar cuenta
    # HU-N-06 CA3 | Tabla de decisiones | Saldo cero pero solicitud pendiente: rechazo de cierre.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'SOLICITUDES_PENDIENTES'

  @G4-112 @CA1
  Scenario: PIN incorrecto impide cierre
    # HU-N-06 CA1 | Particiones de equivalencia | Saldo cero, PIN incorrecto; conservar cuenta activa.
    * def r = req('/api/cuentas/me/cierre', 'POST', {pin:'0000'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'PIN_INCORRECTO'
    * def r = req('/api/cuentas/me', 'GET', null, a.token, {})
    * match r.statusCode == 200

  @G4-113 @CA2
  Scenario: Saldo pendiente impide cierre
    # HU-N-06 CA2 | Particiones de equivalencia | PIN correcto y saldo positivo.
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'0.01'}, null, {})
    * def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'SALDO_PENDIENTE'
