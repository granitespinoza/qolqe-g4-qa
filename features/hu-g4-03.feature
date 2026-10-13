# language: en
@HU-G4-03 @api
Feature: HU-G4-03 — comportamiento verificable
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

  @G4-024 @CA1
  Scenario: Editar alias sin compararlo consigo mismo
    # R-G4-02 | Particiones de equivalencia | Mantener el mismo alias no debe ser duplicado; celular se conserva.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {alias:'Ana'}, a.token, {})
    * match r.statusCode == 200
    * match r.result.alias == 'Ana'
    * match r.result.celular == b.cell

  @G4-025 @CA1
  Scenario: Marcar y desmarcar favorito
    # R-G4-03 | Transición de estados | Ambas acciones conservan alias y celular.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {favorito:true}, a.token, {})
    * match r.statusCode == 200
    * match r.result.favorito == true
    * def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {favorito:false}, a.token, {})
    * match r.statusCode == 200
    * match r.result.favorito == false
    * match r.result.alias == 'Ana'

  @G4-026 @CA1
  Scenario: Quinto favorito permitido; sexto rechazado
    # R-G4-03 | Valores límite (2 puntos) | Verificar 5/6 y que el sexto conserve estado no favorito.
    * def ids = []
    * def populate = function(){for(var i=0;i<6;i++){var u=create('Favorito '+i); var x=add(u.cell,'Favorito '+i,a.token); karate.appendTo(ids,x.result.id);}}
    * eval populate()
    * def mark = function(){for(var i=0;i<5;i++){var x=req('/api/contactos/'+ids[i],'PUT',{favorito:true},a.token,{}); if(x.statusCode!=200) karate.fail('Contexto favorito');}}
    * eval mark()
    * def r = req('/api/contactos/' + ids[5] + '', 'PUT', {favorito:true}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'LIMITE_FAVORITOS'
    * def r = req('/api/contactos', 'GET', null, a.token, {})
    * match r.result.contactos[5].favorito == false

  @G4-027 @CA1
  Scenario: Rechazar edición de contacto ajeno
    # Propiedad de datos | Particiones de equivalencia | Un tercero no puede editar un recurso ajeno.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {alias:'Otro'}, c.token, {})
    * match r.statusCode == 404
    * match r.result.codigo == 'CONTACTO_NO_ENCONTRADO'

  @G4-108 @CA1
  Scenario: Editar solo alias conserva favorito
    # HU-G4-03 CA1 | Comprobación de efectos | No basta verificar el campo cambiado.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {favorito:true}, a.token, {})
    * match r.statusCode == 200
    * def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {alias:'Nuevo Alias'}, a.token, {})
    * match r.statusCode == 200
    * match r.result.favorito == true
    * match r.result.celular == b.cell
