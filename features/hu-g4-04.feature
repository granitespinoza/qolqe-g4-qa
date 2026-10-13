# language: en
@HU-G4-04 @api
Feature: HU-G4-04 — comportamiento verificable
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

  @G4-028 @CA1
  Scenario: Eliminar contacto conserva transferencia
    # RN-11 | Comprobación de efectos | Transferir, eliminar y consultar movimiento por código.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'100.00'}, null, {})
    * def tx = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
    * match tx.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id + '', 'DELETE', null, a.token, {})
    * match r.statusCode == 204
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0
    * def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, a.token, {})
    * match r.statusCode == 200

  @G4-029 @CA2
  Scenario: Solicitud pendiente enviada impide eliminar
    # R-G4-05 | Tabla de decisiones | Contacto propio y solicitud pendiente vigente.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id + '', 'DELETE', null, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'SOLICITUDES_PENDIENTES'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-030 @CA2
  Scenario: Solicitud pendiente recibida impide eliminar
    # R-G4-05 | Tabla de decisiones | Comprobar dirección recibida, no solo enviada.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def cb = add(a.cell,'Granit',b.token)
    * def r = req('/api/contactos/' + cb.result.id + '', 'DELETE', null, b.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'SOLICITUDES_PENDIENTES'

  @G4-031 @CA2
  Scenario: Solicitud vencida permite eliminar
    # R-G4-05 | Transición de estados | Vencida no bloquea eliminación.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
    * match s.statusCode == 201
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
    * set a.token = login(a)
    * def r = req('/api/contactos/' + contact.result.id + '', 'DELETE', null, a.token, {})
    * match r.statusCode == 204
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0
