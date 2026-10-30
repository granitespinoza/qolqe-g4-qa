# language: en
@HU-N-01 @api
Feature: HU-N-01 — comportamiento verificable
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

  @G4-067 @CA1 @CA6 @TC-G4-067
  Scenario: Registro crea saldo cero, límite y bienvenida
    # RN-01/02/03 | Comprobación de efectos | Usuarios creados por API; se verifican consecuencias del registro.
    * def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
    * match r.statusCode == 200
    * match r.result.saldo == '0.00'
    * def r = req('/api/limites', 'GET', null, a.token, {})
    * match r.result.limite_diario == '2000.00'
    * def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
    * assert r.result.length >= 1

  @G4-068 @CA2 @TC-G4-068
  Scenario: Rechazar dni inválido
    # RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso.
    * def n = random()
    * def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
    * set payload.dni = '123'
    * def r = req('/api/usuarios', 'POST', payload, null, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'DNI_INVALIDO'

  @G4-069 @CA3 @TC-G4-069
  Scenario: Rechazar celular inválido
    # RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso.
    * def n = random()
    * def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
    * set payload.celular = '123'
    * def r = req('/api/usuarios', 'POST', payload, null, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'CELULAR_INVALIDO'

  @G4-070 @CA4 @TC-G4-070
  Scenario: Rechazar pin inválido
    # RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso.
    * def n = random()
    * def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
    * set payload.pin = '1111'
    * def r = req('/api/usuarios', 'POST', payload, null, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'PIN_INVALIDO'

  @G4-071 @CA5 @TC-G4-071
  Scenario: Rechazar correo inválido
    # RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso.
    * def n = random()
    * def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
    * set payload.correo = 'invalid'
    * def r = req('/api/usuarios', 'POST', payload, null, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'CORREO_INVALIDO'

  @G4-110 @CA3 @TC-G4-110
  Scenario: Celular duplicado responde conflicto
    # RN-02 | Particiones de equivalencia | Registro con celular existente y restantes datos válidos.
    * def r = req('/api/usuarios', 'POST', {dni:'12345678',nombres:'Nuevo Usuario',celular:'#(a.cell)',pin:'4826'}, null, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'CELULAR_REGISTRADO'

  @G4-111 @CA5 @TC-G4-111
  Scenario: Correo duplicado ignora mayúsculas
    # HU-N-01 CA5 | Particiones de equivalencia | Primera cuenta fija correo; segunda intenta su versión en mayúsculas.
    * def email = a.cell + '@example.com'
    * def r = req('/api/cuentas/me', 'PUT', {correo:email}, a.token, {})
    * match r.statusCode == 200
    * def n = random()
    * def r = req('/api/usuarios', 'POST', {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9"+n)',pin:'4826',correo:'#(email.toUpperCase())'}, null, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'CORREO_REGISTRADO'
