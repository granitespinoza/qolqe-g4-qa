# language: en
@HU-N-04 @api
Feature: HU-N-04 — comportamiento verificable
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

  @G4-075 @CA1 @CA2
  Scenario: Saldo PEN y perfil enmascarado
    # HU-N-04 | Comprobación de efectos | No revelar DNI completo.
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.statusCode == 200
    * match r.result.moneda == 'PEN'
    * match r.result.actualizado_en == "#string"
    * def r = req('/api/cuentas/me', 'GET', null, a.token, {})
    * match r.statusCode == 200
    * assert r.result.dni.startsWith('****')
    * match r.result.celular == a.cell

  @G4-076 @CA3
  Scenario: Acceso sin autenticación null
    # HU-N-04 CA3 | Particiones de equivalencia | Ausente e inválido son clases diferentes.
    * def r = req('/api/cuentas/me/saldo', 'GET', null, null, {})
    * match r.statusCode == 401
    * match r.result.codigo == 'NO_AUTENTICADO'

  @G4-077 @CA3
  Scenario: Acceso sin autenticación 'invalid'
    # HU-N-04 CA3 | Particiones de equivalencia | Ausente e inválido son clases diferentes.
    * def r = req('/api/cuentas/me/saldo', 'GET', null, 'invalid', {})
    * match r.statusCode == 401
    * match r.result.codigo == 'NO_AUTENTICADO'

  @G4-078 @CA3
  Scenario: Token vencido
    # HU-N-04 CA3 | Valores límite (2 puntos) | A los 30 min debe rechazarse.
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:30}, null, {})
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.statusCode == 401
    * match r.result.codigo == 'NO_AUTENTICADO'
