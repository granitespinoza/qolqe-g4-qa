# language: en
@HU-G4-08 @api
Feature: HU-G4-08 — comportamiento verificable
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

  @G4-049 @CA1 @CA3 @CA4
  Scenario: Aceptar genera transferencia, código y SMS
    # HU-N-07 / R-G4-05 | Transición de estados | Destinatario vigente con saldo; vincular operación y solicitud.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 200
    * match r.result.estado == 'ACEPTADA'
    * match r.result.codigo_operacion == "#string"
    * def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
    * match r.result.saldo == '90.00'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result.saldo == '10.00'
    * def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
    * assert r.result.length >= 2

  @G4-050 @CA2
  Scenario: Saldo insuficiente conserva PENDIENTE
    # RN-08 / R-G4-05 | Transición de estados | Error financiero no resuelve solicitud.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'SALDO_INSUFICIENTE'
    * def r = req('/api/solicitudes', 'GET', null, a.token, {})
    * match r.result.enviadas[0].estado == 'PENDIENTE'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
    * match r.result.saldo == '0.00'

  @G4-051 @CA4
  Scenario: Tercero no puede aceptar
    # Propiedad de datos | Tabla de decisiones | Token válido con rol ajeno devuelve 404.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, c.token, {})
    * match r.statusCode == 404
    * match r.result.codigo == 'SOLICITUD_NO_ENCONTRADA'

  @G4-052 @CA4
  Scenario: Aceptar a los 2879 minutos
    # R-G4-05 | Valores límite (3 puntos) | Vigencia se decide en la acción, no solo al listar.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2879}, null, {})
    * set b.token = login(b)
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 200

  @G4-053 @CA4
  Scenario: Aceptar a los 2880 minutos
    # R-G4-05 | Valores límite (3 puntos) | Vigencia se decide en la acción, no solo al listar.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
    * set b.token = login(b)
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-054 @CA4
  Scenario: Aceptar a los 2881 minutos
    # R-G4-05 | Valores límite (3 puntos) | Vigencia se decide en la acción, no solo al listar.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2881}, null, {})
    * set b.token = login(b)
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-055 @CA4
  Scenario: No aceptar dos veces
    # R-G4-05 | Transición de estados | La segunda aceptación no duplica dinero.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
    * match r.result.saldo == '90.00'

  @G4-096 @CA1 @CA2
  Scenario: Límite diario agotado impide operación
    # RN-06 | Tabla de decisiones | Saldo suficiente pero límite agotado: aislar rechazo diario.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(b.cell)',saldo:'1000.00'}, null, {})
    * def r = req('/api/limites', 'PUT', {limite_diario:'100.00'}, b.token, {})
    * match r.statusCode == 200
    * def r = req('/api/transferencias', 'POST', {celular_destino:'#(a.cell)',monto:'100.00'}, b.token, {})
    * match r.statusCode == 201
    * def beforePayer = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
    * def beforeTarget = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * def beforeLimits = req('/api/limites', 'GET', null, b.token, {})
    * def beforeMovements = req('/api/movimientos', 'GET', null, b.token, {})
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'LIMITE_DIARIO_EXCEDIDO'
    * def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
    * match r.result == beforePayer.result
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result == beforeTarget.result
    * def r = req('/api/limites', 'GET', null, b.token, {})
    * match r.result.usado_hoy == beforeLimits.result.usado_hoy
    * def r = req('/api/movimientos', 'GET', null, b.token, {})
    * match r.result.total == beforeMovements.result.total
    * def r = req('/api/solicitudes', 'GET', null, a.token, {})
    * match r.result.enviadas[0].id == s.result.id
    * match r.result.enviadas[0].estado == 'PENDIENTE'
    * match r.result.enviadas[0].codigo_operacion == null

  @G4-097 @CA4
  Scenario: No aceptar desde ACEPTADA
    # R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-100 @CA4
  Scenario: No aceptar desde RECHAZADA
    # R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'

  @G4-103 @CA4
  Scenario: No aceptar desde CANCELADA
    # R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
    * match fund.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
    * match r.statusCode == 200
    * def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ESTADO_INVALIDO'
