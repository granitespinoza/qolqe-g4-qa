# language: en
@HU-N-03 @api
Feature: HU-N-03 — comportamiento verificable
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

  @G4-074 @CA1 @CA2 @TC-G4-074 @known_issue @D-04
  Scenario: Cerrar sesión revoca solo ese token
    # HU-N-03 | Transición de estados | Dos sesiones; revocación de una no afecta la otra.
    * def second = login(a)
    * def r = req('/api/auth/logout', 'POST', null, a.token, {})
    * match r.statusCode == 204
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.statusCode == 401
    * match r.result.codigo == 'NO_AUTENTICADO'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, second, {})
    * match r.statusCode == 200

  @G4-094 @CA2 @TC-G4-094
  Scenario: Cerrar una sesión no afecta otra
    # HU-N-03 CA2 | Transición de estados | Separado del caso de revocación para que su fallo no oculte este criterio.
    * def second = login(a)
    * def r = req('/api/auth/logout', 'POST', null, a.token, {})
    * match r.statusCode == 204
    * def r = req('/api/cuentas/me/saldo', 'GET', null, second, {})
    * match r.statusCode == 200
