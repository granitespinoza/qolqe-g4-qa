# language: en
@HU-N-02 @api
Feature: HU-N-02 — comportamiento verificable
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

  @G4-072 @CA1 @TC-G4-072
  Scenario: Login crea sesión con vigencia de 30 minutos
    # HU-N-02 CA1 | Comprobación de efectos | La autenticación de contexto se vuelve a verificar explícitamente.
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
    * match r.statusCode == 200
    * match r.result.expires_in == 1800
    * match r.result.sesion_id == "#number"

  @G4-073 @CA2 @CA3 @CA4 @TC-G4-073
  Scenario: Bloqueo tras tres intentos y acceso después de 15 min
    # RN-04 | Transición de estados | Secuencia de intentos y frontera temporal.
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'0000'}, null, {})
    * match r.statusCode == 401
    * match r.result.codigo == 'CREDENCIALES_INVALIDAS'
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'0000'}, null, {})
    * match r.statusCode == 401
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'0000'}, null, {})
    * match r.statusCode == 423
    * match r.result.codigo == 'CUENTA_BLOQUEADA'
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
    * match r.statusCode == 423
    * def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:15}, null, {})
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
    * match r.statusCode == 200

  @G4-092 @CA5 @TC-G4-092
  Scenario: Cuenta cerrada no puede ingresar
    # HU-N-02 CA5 | Transición de estados | Cerrar cuenta con saldo cero antes de intentar ingresar.
    * def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
    * match r.statusCode == 204
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
    * match r.statusCode == 401
    * match r.result.codigo == 'CUENTA_CERRADA'

  @G4-093 @CA6 @TC-G4-093
  Scenario: Nuevo dispositivo permite login y genera alerta
    # HU-N-02 CA6 | Comprobación de efectos | Identificador no registrado no bloquea login, pero avisa.
    * def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826',dispositivo_id:'dispositivo-no-registrado'}, null, {})
    * match r.statusCode == 200
    * def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
    * assert JSON.stringify(r.result).toLowerCase().indexOf('nuevo dispositivo') >= 0
