# language: en
@HU-G4-01 @api
Feature: HU-G4-01 — comportamiento verificable
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

  @G4-001 @CA1
  Scenario: Crear contacto con alias 'Ana'
    # R-G4-01/02/03 | Valores límite (2 puntos) | Alias permitido; celular activo, ajeno y lista vacía.
    * def r = add(b.cell, "Ana", a.token)
    * match r.statusCode == 201
    * match r.result.alias == "Ana"
    * match r.result.favorito == false
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-002 @CA1
  Scenario: Crear contacto con alias 'AAAAAAAAAAAAAAAAAAAA'
    # R-G4-01/02/03 | Valores límite (2 puntos) | Alias permitido; celular activo, ajeno y lista vacía.
    * def r = add(b.cell, "AAAAAAAAAAAAAAAAAAAA", a.token)
    * match r.statusCode == 201
    * match r.result.alias == "AAAAAAAAAAAAAAAAAAAA"
    * match r.result.favorito == false
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-003 @CA1
  Scenario: Crear contacto con alias 'José'
    # R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía.
    * def r = add(b.cell, "José", a.token)
    * match r.statusCode == 201
    * match r.result.alias == "José"
    * match r.result.favorito == false
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-004 @CA1
  Scenario: Crear contacto con alias 'Niño'
    # R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía.
    * def r = add(b.cell, "Niño", a.token)
    * match r.statusCode == 201
    * match r.result.alias == "Niño"
    * match r.result.favorito == false
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-005 @CA1
  Scenario: Crear contacto con alias 'A1 B'
    # R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía.
    * def r = add(b.cell, "A1 B", a.token)
    * match r.statusCode == 201
    * match r.result.alias == "A1 B"
    * match r.result.favorito == false
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-006 @CA1
  Scenario: Crear contacto con alias ' Ana '
    # R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía.
    * def r = add(b.cell, " Ana ", a.token)
    * match r.statusCode == 201
    * match r.result.alias == "Ana"
    * match r.result.favorito == false
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-007 @CA1
  Scenario: Rechazar alias 'Lu'
    # R-G4-02 | Valores límite (2 puntos) | Frontera o clase inválida, restantes condiciones válidas.
    * def r = add(b.cell, "Lu", a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'ALIAS_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-008 @CA1
  Scenario: Rechazar alias 'AAAAAAAAAAAAAAAAAAAAA'
    # R-G4-02 | Valores límite (2 puntos) | Frontera o clase inválida, restantes condiciones válidas.
    * def r = add(b.cell, "AAAAAAAAAAAAAAAAAAAAA", a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'ALIAS_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-009 @CA1
  Scenario: Rechazar alias ''
    # R-G4-02 | Particiones de equivalencia | Frontera o clase inválida, restantes condiciones válidas.
    * def r = add(b.cell, "", a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'ALIAS_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-010 @CA1
  Scenario: Rechazar alias '   '
    # R-G4-02 | Particiones de equivalencia | Frontera o clase inválida, restantes condiciones válidas.
    * def r = add(b.cell, "   ", a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'ALIAS_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-011 @CA1
  Scenario: Rechazar alias 'Ana@'
    # R-G4-02 | Particiones de equivalencia | Frontera o clase inválida, restantes condiciones válidas.
    * def r = add(b.cell, "Ana@", a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'ALIAS_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-012 @CA1
  Scenario: Rechazar celular: CONTACTO_PROPIO
    # R-G4-01 | Particiones de equivalencia | Representante de una condición distinta de negocio.
    * def r = add(a.cell, 'Ana', a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'CONTACTO_PROPIO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-013 @CA1
  Scenario: Rechazar celular: CELULAR_INVALIDO
    # R-G4-01 | Particiones de equivalencia | Representante de una condición distinta de negocio.
    * def r = add('123', 'Ana', a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'CELULAR_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-014 @CA1
  Scenario: Rechazar celular: CELULAR_NO_REGISTRADO
    # R-G4-01 | Particiones de equivalencia | Representante de una condición distinta de negocio.
    * def r = add('934567812', 'Ana', a.token)
    * match r.statusCode == 404
    * match r.result.codigo == 'CELULAR_NO_REGISTRADO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-015 @CA1
  Scenario: Celular válido sin registro
    # R-G4-01 | Particiones de equivalencia | Cerrar una cuenta propia de contexto no reutiliza datos ajenos.
    * def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, b.token, {})
    * match r.statusCode == 204
    * def r = add(b.cell, 'Ana', a.token)
    * match r.statusCode == 404
    * match r.result.codigo == 'CELULAR_NO_REGISTRADO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0

  @G4-016 @CA1
  Scenario: Contacto duplicado
    # R-G4-01 | Particiones de equivalencia | Mismo celular con otro alias.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = add(b.cell, 'Otro', a.token)
    * match r.statusCode == 409
    * match r.result.codigo == 'CONTACTO_EXISTENTE'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-017 @CA1
  Scenario: Alias duplicado tras normalizar 'ANA'
    # R-G4-02 | Particiones de equivalencia | Unicidad se comprueba sin mayúsculas y tras recortar espacios.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = add(c.cell, "ANA", a.token)
    * match r.statusCode == 409
    * match r.result.codigo == 'ALIAS_DUPLICADO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-018 @CA1
  Scenario: Alias duplicado tras normalizar ' Ana '
    # R-G4-02 | Particiones de equivalencia | Unicidad se comprueba sin mayúsculas y tras recortar espacios.
    * def contact = add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = add(c.cell, " Ana ", a.token)
    * match r.statusCode == 409
    * match r.result.codigo == 'ALIAS_DUPLICADO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 1

  @G4-019 @CA1
  Scenario: Permitir contacto 15 y rechazar contacto 16
    # R-G4-03 | Valores límite (2 puntos) | Contexto con 14; comprobar frontera y ausencia de efecto al superar 15.
    * def fill = function(n){ for(var i=0;i<n;i++){ var u=create('Contacto ' + i); var x=add(u.cell,'Contacto ' + i,a.token); if(x.statusCode!=201) karate.fail('Contexto capacidad: '+JSON.stringify(x.result)); } }
    * eval fill(14)
    * def r = add(b.cell, 'Ana', a.token)
    * match r.statusCode == 201
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 15
    * def r = add(c.cell, 'Franco', a.token)
    * match r.statusCode == 422
    * match r.result.codigo == 'LIMITE_CONTACTOS'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 15

  @G4-106 @CA1
  Scenario: Celular válido aún no registrado
    # R-G4-01 | Particiones de equivalencia | Crear valor nuevo sin registrar; separado de cuenta cerrada.
    * def unknown = '9' + random()
    * def r = add(unknown, 'Ana', a.token)
    * match r.statusCode == 404
    * match r.result.codigo == 'CELULAR_NO_REGISTRADO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.total == 0
