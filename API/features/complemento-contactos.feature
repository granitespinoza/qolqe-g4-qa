# language: en
@COMPLEMENTO-CONTACTOS @funcional @api
Feature: Variantes funcionales faltantes de Contactos después de revisión docente
  Fuente: requisitos.md, HU-G4-02 CA2, HU-G4-03 CA1, R-G4-02 y propiedad de datos.
  Separado de los 116 escenarios históricos; no implica cobertura exhaustiva.

Background:
  * def ctx = call read('classpath:API/features/support/setup.feature')
  * def http = ctx.http
  * def a = ctx.a
  * def b = ctx.b
  * def c = ctx.c
  * def req = function(route, method, body, token, query){ return karate.call('classpath:API/features/support/http.feature',{route:route,method:method,body:body,token:token,query:query}); }

  @CF-01 @HU-G4-03 @CA1 @TC-CF-01 @known_issue @D-01
  Scenario Outline: Editar alias válido en límites y clases permitidas
    # Valores límite 3/20 y particiones de caracteres; celular y favorito se conservan.
    * def contact = ctx.add(b.cell, 'Inicial', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id, 'PUT', {alias:alias}, a.token, {})
    * match r.statusCode == 200
    * match r.result.alias == expected
    * match r.result.celular == b.cell
    * match r.result.favorito == false
    Examples:
      | alias                | expected             |
      | Ana                  | Ana                  |
      | AAAAAAAAAAAAAAAAAAAA | AAAAAAAAAAAAAAAAAAAA |
      | José                 | José                 |
      | Niño                 | Niño                 |
      | A1 B                 | A1 B                 |

  @CF-02 @HU-G4-03 @CA1 @TC-CF-02
  Scenario Outline: Editar alias inválido conserva el contacto original
    # Particiones inválidas, no basta ensayar estos valores solamente al crear.
    * def contact = ctx.add(b.cell, 'Inicial', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id, 'PUT', {alias:alias}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'ALIAS_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.contactos == [ '#(contact.result)' ]
    Examples:
      | alias! |
      | ''     |
      | '   '  |
      | 'Ana@' |

  @CF-03 @HU-G4-03 @CA1 @TC-CF-03 @known_issue @D-02
  Scenario Outline: Editar alias duplicado tras normalizar
    # Partición por mayúsculas y espacios: unicidad también al editar.
    * def first = ctx.add(b.cell, 'Ana', a.token)
    * def second = ctx.add(c.cell, 'Otro', a.token)
    * match first.statusCode == 201
    * match second.statusCode == 201
    * def r = req('/api/contactos/' + second.result.id, 'PUT', {alias:alias}, a.token, {})
    * match r.statusCode == 409
    * match r.result.codigo == 'ALIAS_DUPLICADO'
    Examples:
      | alias!  |
      | 'ANA'   |
      | ' Ana ' |

  @CF-04 @HU-G4-02 @CA2 @TC-CF-04
  Scenario: Buscar por fragmento del alias
    # Partición de coincidencia parcial: una igualdad completa no demuestra este CA.
    * def contact = ctx.add(b.cell, 'José oficina', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos', 'GET', null, a.token, {buscar:'OFIC'})
    * match r.statusCode == 200
    * match r.result.total == 1
    * match r.result.contactos[0].id == contact.result.id

  @CF-05 @HU-G4-04 @CA1 @TC-CF-05
  Scenario: Eliminar contacto ajeno responde 404 y conserva el recurso
    # Partición de permisos; propiedad general aplicable a eliminación.
    * def contact = ctx.add(b.cell, 'Ana', a.token)
    * match contact.statusCode == 201
    * def r = req('/api/contactos/' + contact.result.id, 'DELETE', null, c.token, {})
    * match r.statusCode == 404
    * match r.result.codigo == 'CONTACTO_NO_ENCONTRADO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.contactos == [ '#(contact.result)' ]
