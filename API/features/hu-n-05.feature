# language: en
@HU-N-05 @api
Feature: HU-N-05 — comportamiento verificable
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

  @G4-079 @CA1 @CA2 @CA3 @TC-G4-079
  Scenario: Editar perfil ignora DNI y celular y envía SMS
    # HU-N-05 | Comprobación de efectos | Actualizar permitidos sin cambiar identidad.
    * def r = req('/api/cuentas/me', 'PUT', {nombres:'Granit Actualizado',correo:'#(a.cell + "@example.com")',dni:'11111111',celular:'999999999'}, a.token, {})
    * match r.statusCode == 200
    * match r.result.nombres == 'Granit Actualizado'
    * match r.result.celular == a.cell
    * def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
    * assert r.result.length >= 2
