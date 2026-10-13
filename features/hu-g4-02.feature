# language: en
@HU-G4-02 @api
Feature: HU-G4-02 — comportamiento verificable
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

  @G4-020 @CA2 @CA3
  Scenario: Buscar ignorando mayúsculas y tildes
    # HU-G4-02 CA2/3 | Particiones de equivalencia | José debe coincidir con JOSE; se verifica máscara, teléfono y favorito.
    * def r = add(b.cell, 'José', a.token)
    * def r = req('/api/contactos', 'GET', null, a.token, {buscar:'JOSE'})
    * match r.statusCode == 200
    * match r.result.total == 1
    * match r.result.contactos[0].alias == 'José'
    * match r.result.contactos[0].celular == b.cell
    * match r.result.contactos[0].favorito == false
    * match r.result.contactos[0].nombre != 'Franco Prueba'

  @G4-021 @CA1
  Scenario: Ordenar favoritos antes del resto
    # HU-G4-02 CA1 | Particiones de equivalencia | Favorito con alias Z debe preceder a alias A no favorito.
    * def z = add(b.cell, 'Zeta', a.token)
    * def r = add(c.cell, 'Alfa', a.token)
    * def r = req('/api/contactos/' + z.result.id + '', 'PUT', {favorito:true}, a.token, {})
    * match r.statusCode == 200
    * def r = req('/api/contactos', 'GET', null, a.token, {})
    * match r.result.contactos[*].alias == ['Zeta','Alfa']

  @G4-022 @CA1
  Scenario: Paginación con 11 contactos
    # HU-G4-02 CA1 | Valores límite (2 puntos) | 10/11 distingue primera y segunda página.
    * def fill = function(n){ for(var i=0;i<n;i++){ var u=create('Contacto ' + i); var x=add(u.cell,'Contacto ' + i,a.token); if(x.statusCode!=201) karate.fail('Contexto capacidad: '+JSON.stringify(x.result)); } }
    * eval fill(11)
    * def r = req('/api/contactos', 'GET', null, a.token, {})
    * match r.statusCode == 200
    * match r.result.total == 11
    * match r.result.total_paginas == 2
    * match r.result.contactos == "#[10]"
    * def r = req('/api/contactos', 'GET', null, a.token, {pagina:2})
    * match r.statusCode == 200
    * match r.result.contactos == "#[1]"

  @G4-023 @CA2
  Scenario: Búsqueda sin coincidencias
    # HU-G4-02 CA2 | Particiones de equivalencia | Consulta válida sin coincidencias devuelve lista vacía.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos', 'GET', null, a.token, {buscar:'Inexistente'})
    * match r.statusCode == 200
    * match r.result.contactos == []

  @G4-107 @CA1
  Scenario: Orden alfabético dentro de cada grupo
    # HU-G4-02 CA1 | Particiones de equivalencia | Cuatro alias comprueban ambos grupos y prioridad de favoritos.
    * def u = create('Cuarto Usuario')
    * def z = add(b.cell, 'Zeta', a.token)
    * def x = add(c.cell, 'Alfa', a.token)
    * def r = add(u.cell, 'Beta', a.token)
    * def v = create('Quinto Usuario')
    * def r = add(v.cell, 'Gamma', a.token)
    * def r = req('/api/contactos/' + z.result.id + '', 'PUT', {favorito:true}, a.token, {})
    * def r = req('/api/contactos/' + x.result.id + '', 'PUT', {favorito:true}, a.token, {})
    * def r = req('/api/contactos', 'GET', null, a.token, {})
    * match r.result.contactos[*].alias == ['Alfa','Zeta','Beta','Gamma']
