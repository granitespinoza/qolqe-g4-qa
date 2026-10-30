# language: en
@HU-G4-10 @api
Feature: HU-G4-10 — comportamiento verificable
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

  @G4-060 @CA1 @TC-G4-060
  Scenario: Cancelar solicitud pendiente
    # R-G4-05 | Transición de estados | Acción del rol correcto cambia el estado sin mover dinero.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 200
    * match r.result.estado == 'CANCELADA'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result.saldo == '0.00'

  @G4-061 @CA1 @TC-G4-061
  Scenario: Rechazar acción de tercero
    # Propiedad de datos | Tabla de decisiones | Un usuario ajeno no puede resolver solicitudes.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, c.token, {})
    * match r.statusCode == 404
    * match r.result.codigo == 'SOLICITUD_NO_ENCONTRADA'

  @G4-062 @CA1 @TC-G4-062
  Scenario: No resolver solicitud vencida
    # R-G4-05 | Transición de estados | A las 48 h la acción debe ser rechazada.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
    * set a.token = login(a)
    * set b.token = login(b)
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-063 @CA1 @TC-G4-063
  Scenario: No repetir resolución
    # R-G4-05 | Transición de estados | Estado terminal no admite otra resolución.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-099 @CA1 @TC-G4-099
  Scenario: No cancelar desde ACEPTADA
    # R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-102 @CA1 @TC-G4-102
  Scenario: No cancelar desde RECHAZADA
    # R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-105 @CA1 @TC-G4-105
  Scenario: No cancelar desde CANCELADA
    # R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'
