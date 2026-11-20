# language: en
@api @technical
Feature: Contratos técnicos del núcleo y solicitudes
Background:
  * def ctx = call read('classpath:tests/api/features/support/setup.feature')
  * def a = ctx.a
  * def req = function(route, method, body, token){ return karate.call('classpath:tests/api/features/support/http.feature', {route:route,method:method,body:body,token:token,query:{}}); }

  @CT-10 @TC-CT-10 @HU-G4-07
  Scenario: Consultar solicitudes sin token responde 401 con error estructurado
    * def r = req('/api/solicitudes','GET',null,null)
    * match r.statusCode == 401
    * match r.result contains {codigo:'NO_AUTENTICADO',detail:'#string'}

  @CT-11 @TC-CT-11 @HU-G4-07
  Scenario: Token malformado no permite consultar solicitudes
    * def r = req('/api/solicitudes','GET',null,'token-invalido')
    * match r.statusCode == 401
    * match r.result contains {codigo:'NO_AUTENTICADO',detail:'#string'}

  @CT-12 @TC-CT-12 @HU-N-04
  Scenario: Saldo devuelve moneda y monto serializado con dos decimales
    * def r = req('/api/cuentas/me/saldo','GET',null,a.token)
    * match r.statusCode == 200
    * match r.result contains {saldo:'#regex [0-9]+[.][0-9]{2}',moneda:'PEN'}

  @CT-13 @TC-CT-13 @HU-N-04
  Scenario: Perfil conserva tipos públicos y no expone el hash del PIN
    * def r = req('/api/cuentas/me','GET',null,a.token)
    * match r.statusCode == 200
    * match r.result contains {nombres:'#string',celular:'#string',dni:'#string'}
    * match r.result !contains {pin_hash:'#present'}

  @CT-14 @TC-CT-14 @HU-N-05
  Scenario: Perfil inválido responde 422 sin modificar el nombre
    * def before = req('/api/cuentas/me','GET',null,a.token)
    * def r = req('/api/cuentas/me','PUT',{nombres:'A'},a.token)
    * match r.statusCode == 422
    * match r.result contains {codigo:'PERFIL_INVALIDO',detail:'#string'}
    * def after = req('/api/cuentas/me','GET',null,a.token)
    * match after.result.nombres == before.result.nombres

  @CT-15 @TC-CT-15 @HU-N-04
  Scenario: Método no permitido no se interpreta como actualización de perfil
    * def r = req('/api/cuentas/me','POST',{},a.token)
    * match r.statusCode == 405
