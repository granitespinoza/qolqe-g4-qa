# language: en
@CONTRATO-CONTACTOS @tecnica @api
Feature: Contrato técnico explícito de Contactos, separado de la cobertura funcional
  Fuente: data/openapi-original.json, SolicitudContacto, CambioContacto,
  Contacto, PaginaContactos y parámetros de las cuatro operaciones CRUD.
  El esperado procede del contrato; una coerción del servidor no cambia el esperado.

Background:
  * def ctx = call read('classpath:features/support/setup.feature')
  * def http = ctx.http
  * def a = ctx.a
  * def b = ctx.b
  * def req = function(route, method, body, token, query){ return karate.call('classpath:features/support/http.feature',{route:route,method:method,body:body,token:token,query:query}); }
  * def contactSchema = { id: '#? Number.isInteger(_) ', alias: '#string', celular: '#regex ^9[0-9]{8}$', nombre: '#string', favorito: '#boolean' }
  * def errorSchema = { codigo: '#string', detail: '#string' }

  @CT-01 @HU-G4-01
  Scenario Outline: POST rechaza <caso> sin crear contacto
    * def body = { celular: '#(b.cell)', alias: 'Ana' }
    * eval if (campo === '$body') body = valor; else if (omitir) delete body[campo]; else body[campo] = valor
    * def r = req('/api/contactos', 'POST', body, a.token, {})
    * match r.statusCode == 422
    * match r.result contains errorSchema
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.statusCode == 200
    * match list.result.total == 0
    Examples:
      | caso                 | campo   | omitir! | valor! |
      | alias omitido        | alias   | true    | null   |
      | celular omitido      | celular | true    | null   |
      | alias nulo           | alias   | false   | null   |
      | celular nulo         | celular | false   | null   |
      | alias numerico       | alias   | false   | 123    |
      | alias booleano       | alias   | false   | true   |
      | alias objeto         | alias   | false   | {}     |
      | alias arreglo        | alias   | false   | []     |
      | celular numerico     | celular | false   | 912345678 |
      | celular booleano     | celular | false   | true   |
      | celular objeto       | celular | false   | {}     |
      | celular arreglo      | celular | false   | []     |
      | cuerpo ausente       | $body   | false   | null   |
      | cuerpo arreglo       | $body   | false   | []     |
      | cuerpo objeto vacio  | $body   | false   | {}     |
      | celular ocho digitos | celular | false   | '91234567' |
      | celular diez digitos | celular | false   | '9123456789' |
      | celular inicia en 8  | celular | false   | '812345678' |
      | celular con letras   | celular | false   | '9abcdefgh' |

  @CT-02 @HU-G4-03
  Scenario Outline: PUT rechaza <caso> sin modificar contacto
    * def created = ctx.add(b.cell, 'Ana', a.token)
    * match created.statusCode == 201
    * def r = req('/api/contactos/' + created.result.id, 'PUT', body, a.token, {})
    * match r.statusCode == 422
    * match r.result contains errorSchema
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.statusCode == 200
    * match list.result.contactos == [ '#(created.result)' ]
    Examples:
      | caso                 | body!                 |
      | alias numerico       | {alias:123}           |
      | alias booleano       | {alias:true}          |
      | alias objeto         | {alias:{}}            |
      | alias arreglo        | {alias:[]}            |
      | alias menor a 3      | {alias:'Lu'}          |
      | alias mayor a 20     | {alias:'AAAAAAAAAAAAAAAAAAAAA'} |
      | favorito texto true  | {favorito:'true'}      |
      | favorito texto false | {favorito:'false'}     |
      | favorito entero uno  | {favorito:1}           |
      | favorito entero cero | {favorito:0}           |
      | favorito objeto      | {favorito:{}}          |
      | favorito arreglo     | {favorito:[]}          |
      | cuerpo ausente       | null                  |
      | cuerpo arreglo       | []                    |

  @CT-03 @HU-G4-03
  Scenario Outline: PUT permite campos opcionales y nulos expresamente admitidos
    * def created = ctx.add(b.cell, 'Ana', a.token)
    * match created.statusCode == 201
    * def r = req('/api/contactos/' + created.result.id, 'PUT', body, a.token, {})
    * match r.statusCode == 200
    * match r.result == created.result
    Examples:
      | body!                          |
      | {}                             |
      | {alias:null}                   |
      | {favorito:null}                |
      | {alias:null, favorito:null}    |

  @CT-04 @HU-G4-02
  Scenario Outline: GET rechaza pagina fuera del contrato
    * def r = req('/api/contactos', 'GET', null, a.token, {pagina:pagina})
    * match r.statusCode == 422
    * match r.result contains errorSchema
    Examples:
      | pagina |
      | 0      |
      | -1     |
      | 1.5    |
      | abc    |

  @CT-05 @HU-G4-03 @HU-G4-04
  Scenario Outline: Identificador de ruta debe ser entero
    * def r = req('/api/contactos/no-entero', method, body, a.token, {})
    * match r.statusCode == 422
    * match r.result contains errorSchema
    Examples:
      | method | body!          |
      | PUT    | {alias:'Ana'}  |
      | DELETE | null           |

  @CT-06 @HU-G4-01 @HU-G4-02 @HU-G4-03 @HU-G4-04
  Scenario: Contrato de respuestas en recorrido CRUD válido
    * def created = ctx.add(b.cell, 'Ana', a.token)
    * match created.statusCode == 201
    * match created.result == contactSchema
    * def listed = req('/api/contactos', 'GET', null, a.token, {})
    * match listed.statusCode == 200
    * match listed.result == { buscar: '#null', pagina: '#? Number.isInteger(_) && _ >= 1', por_pagina: 10, total: '#? Number.isInteger(_) && _ >= 0', total_paginas: '#? Number.isInteger(_) && _ >= 1', contactos: '#array' }
    * match listed.result.contactos == '#[1]'
    * match each listed.result.contactos == contactSchema
    * def updated = req('/api/contactos/' + created.result.id, 'PUT', {alias:'Nuevo', favorito:true}, a.token, {})
    * match updated.statusCode == 200
    * match updated.result == contactSchema
    * match updated.result contains {alias:'Nuevo', favorito:true}
    * def deleted = req('/api/contactos/' + created.result.id, 'DELETE', null, a.token, {})
    * match deleted.statusCode == 204
    * match deleted.result == ''
    * def listed = req('/api/contactos', 'GET', null, a.token, {})
    * match listed.result.total == 0

  @CT-07 @HU-G4-01 @HU-G4-02 @HU-G4-03 @HU-G4-04
  Scenario Outline: Operaciones protegidas rechazan peticiones sin token
    * def created = ctx.add(b.cell, 'Ana', a.token)
    * match created.statusCode == 201
    * def route = '/api/contactos' + (member ? '/' + created.result.id : '')
    * def r = req(route, method, body, null, {})
    * match r.statusCode == 401
    * match r.result contains {codigo:'NO_AUTENTICADO', detail:'#string'}
    Examples:
      | method | member! | body!                          |
      | GET    | false   | null                           |
      | POST   | false   | {celular:b.cell, alias:'Otro'} |
      | PUT    | true    | {alias:'Nuevo'}                 |
      | DELETE | true    | null                           |

  @CT-08 @HU-G4-01 @HU-G4-02 @HU-G4-03 @HU-G4-04
  Scenario Outline: Bearer con token malformado no autentica operaciones protegidas
    # HTTPBearer declarado en OpenAPI; no se inventan otras cabeceras obligatorias.
    * def created = ctx.add(b.cell, 'Ana', a.token)
    * match created.statusCode == 201
    * def route = '/api/contactos' + (member ? '/' + created.result.id : '')
    * def r = req(route, method, body, 'no-es-un-jwt', {})
    * match r.statusCode == 401
    * match r.result contains {codigo:'NO_AUTENTICADO', detail:'#string'}
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.statusCode == 200
    * match list.result.contactos == [ '#(created.result)' ]
    Examples:
      | method | member! | body!                          |
      | GET    | false   | null                           |
      | POST   | false   | {celular:b.cell, alias:'Otro'} |
      | PUT    | true    | {alias:'Nuevo'}                 |
      | DELETE | true    | null                           |

  @CT-09 @HU-G4-03
  Scenario: Editar alias con símbolo prohibido conserva el contacto
    # CambioContacto.alias describe mismas reglas que al agregar (R-G4-02).
    * def created = ctx.add(b.cell, 'Ana', a.token)
    * match created.statusCode == 201
    * def r = req('/api/contactos/' + created.result.id, 'PUT', {alias:'Ana@'}, a.token, {})
    * match r.statusCode == 422
    * match r.result.codigo == 'ALIAS_INVALIDO'
    * def list = req('/api/contactos', 'GET', null, a.token, {})
    * match list.result.contactos == [ '#(created.result)' ]
