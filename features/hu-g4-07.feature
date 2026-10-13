# language: en
@HU-G4-07 @api
Feature: HU-G4-07 — comportamiento verificable
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

  @G4-045 @CA1
  Scenario: Separar solicitudes enviadas y recibidas y filtrar
    # HU-G4-07 CA1 | Particiones de equivalencia | Mismo recurso aparece según rol; filtro sin coincidencias.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/solicitudes', 'GET', null, a.token, {})
    * match r.result.enviadas == "#[1]"
    * match r.result.recibidas == []
    * def r = req('/api/solicitudes', 'GET', null, b.token, {})
    * match r.result.recibidas == "#[1]"
    * match r.result.enviadas == []
    * def r = req('/api/solicitudes', 'GET', null, a.token, {estado:'ACEPTADA'})
    * match r.result.enviadas == []

  @G4-046 @CA2
  Scenario: Estado al transcurrir 2879 minutos
    # R-G4-05 | Valores límite (3 puntos) | Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2879}, null, {})
    * set a.token = login(a)
    * def r = req('/api/solicitudes', 'GET', null, a.token, {})
    * match r.result.enviadas[0].estado == 'PENDIENTE'

  @G4-047 @CA2
  Scenario: Estado al transcurrir 2880 minutos
    # R-G4-05 | Valores límite (3 puntos) | Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
    * set a.token = login(a)
    * def r = req('/api/solicitudes', 'GET', null, a.token, {})
    * match r.result.enviadas[0].estado == 'VENCIDA'

  @G4-048 @CA2
  Scenario: Estado al transcurrir 2881 minutos
    # R-G4-05 | Valores límite (3 puntos) | Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2881}, null, {})
    * set a.token = login(a)
    * def r = req('/api/solicitudes', 'GET', null, a.token, {})
    * match r.result.enviadas[0].estado == 'VENCIDA'
