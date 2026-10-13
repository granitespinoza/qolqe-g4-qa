# language: en
@HU-G4-06 @api
Feature: HU-G4-06 — comportamiento verificable
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

  @G4-034 @CA1 @CA2
  Scenario: Crear solicitud pendiente con vigencia 48 h y SMS
    # R-G4-04/05 | Comprobación de efectos | El monto pedido no debita saldo antes de aceptar.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * match s.result.estado == 'PENDIENTE'
    * assert (new Date(s.result.vence_en+'-05:00') - new Date(s.result.creada_en+'-05:00')) == 172800000
    * def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:b.cell})
    * assert r.result.length >= 2
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.result.saldo == '0.00'

  @G4-035 @CA1
  Scenario: Monto solicitado 0.00
    # RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '0.00', 'Almuerzo')
    * match r.statusCode == 422
    * match r.result.codigo == 'SOLICITUD_INVALIDA'

  @G4-036 @CA1
  Scenario: Monto solicitado 0.01
    # RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '0.01', 'Almuerzo')
    * match r.statusCode == 201

  @G4-037 @CA1
  Scenario: Monto solicitado 500.00
    # RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '500.00', 'Almuerzo')
    * match r.statusCode == 201

  @G4-038 @CA1
  Scenario: Monto solicitado 500.01
    # RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '500.01', 'Almuerzo')
    * match r.statusCode == 422
    * match r.result.codigo == 'SOLICITUD_INVALIDA'

  @G4-039 @CA1
  Scenario: Monto solicitado 10.005
    # RN-05 / R-G4-04 | Particiones de equivalencia | Fronteras monetarias y clase con demasiados decimales.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '10.005', 'Almuerzo')
    * match r.statusCode == 422
    * match r.result.codigo == 'SOLICITUD_INVALIDA'

  @G4-040 @CA1
  Scenario: Motivo de 2 caracteres
    # R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '10.00', 'AA')
    * match r.statusCode == 422
    * match r.result.codigo == 'SOLICITUD_INVALIDA'

  @G4-041 @CA1
  Scenario: Motivo de 3 caracteres
    # R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '10.00', 'AAA')
    * match r.statusCode == 201

  @G4-042 @CA1
  Scenario: Motivo de 60 caracteres
    # R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '10.00', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    * match r.statusCode == 201

  @G4-043 @CA1
  Scenario: Motivo de 61 caracteres
    # R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = requestMoney(contact.result.id, '10.00', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
    * match r.statusCode == 422
    * match r.result.codigo == 'SOLICITUD_INVALIDA'

  @G4-044 @CA1
  Scenario: Décima pendiente permitida y undécima rechazada
    # R-G4-04 | Valores límite (2 puntos) | Límite independiente del número de contactos.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def fillRequests = function(){for(var i=0;i<9;i++){var x=requestMoney(contact.result.id,'10.00','Almuerzo'); if(x.statusCode!=201) karate.fail('Contexto solicitudes');}}
    * eval fillRequests()
    * def r = requestMoney(contact.result.id,'10.00','Almuerzo')
    * match r.statusCode == 201
    * def r = requestMoney(contact.result.id,'10.00','Almuerzo')
    * match r.statusCode == 422
    * match r.result.codigo == 'LIMITE_SOLICITUDES'

  @G4-109 @CA1
  Scenario: Contacto de otro usuario no permite solicitar
    # Propiedad de datos | Particiones de equivalencia | Un id válido ajeno debe ser tratado como inexistente.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/solicitudes', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00',motivo:'Almuerzo'}, c.token, {})
    * match r.statusCode == 404
    * match r.result.codigo == 'CONTACTO_NO_ENCONTRADO'
