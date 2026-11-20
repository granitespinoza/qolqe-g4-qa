# language: es
@web
Característica: Contactos verificable en Qolqe
  Como cliente de Qolqe
  Quiero que la interfaz respete las reglas y conserve los datos
  Para operar de forma segura

  @HU-G4-01 @TC-E2E-G4-101 @WEB-G4-01-CA1-01
  Escenario: E2E-G4-101 @HU-G4-01 @TC-E2E-G4-101 | WEB-G4-01-CA1-01 | Alta en límites 3/20, tildes, números y persistencia
    Dado un contexto aislado para "E2E-G4-101"
    Cuando realizo "Alta en límites 3/20, tildes, números y persistencia" en "E2E-G4-101"
    Entonces verifico las reglas y la persistencia de "E2E-G4-101"

  @HU-G4-01 @TC-E2E-G4-102 @WEB-G4-01-CA1-01 @known_issue @D-01
  Escenario: E2E-G4-102 @HU-G4-01 @TC-E2E-G4-102 @known_issue @D-01 | WEB-G4-01-CA1-01 | [D-01] ñ debe ser válida al crear
    Dado un contexto aislado para "E2E-G4-102"
    Cuando realizo "[D-01] ñ debe ser válida al crear" en "E2E-G4-102"
    Entonces verifico las reglas y la persistencia de "E2E-G4-102"

  @HU-G4-01 @TC-E2E-G4-103 @WEB-G4-01-CA1-02
  Escenario: E2E-G4-103 @HU-G4-01 @TC-E2E-G4-103 | WEB-G4-01-CA1-02 | Recorta espacios y rechaza duplicado por mayúsculas
    Dado un contexto aislado para "E2E-G4-103"
    Cuando realizo "Recorta espacios y rechaza duplicado por mayúsculas" en "E2E-G4-103"
    Entonces verifico las reglas y la persistencia de "E2E-G4-103"

  @HU-G4-01 @TC-E2E-G4-104 @WEB-G4-01-CA1-02 @known_issue @D-02
  Escenario: E2E-G4-104 @HU-G4-01 @TC-E2E-G4-104 @known_issue @D-02 | WEB-G4-01-CA1-02 | [D-02] duplicado con espacios debe rechazarse
    Dado un contexto aislado para "E2E-G4-104"
    Cuando realizo "[D-02] duplicado con espacios debe rechazarse" en "E2E-G4-104"
    Entonces verifico las reglas y la persistencia de "E2E-G4-104"

  @HU-G4-01 @TC-E2E-G4-105 @WEB-G4-01-CA1-03
  Escenario: E2E-G4-105 @HU-G4-01 @TC-E2E-G4-105 | WEB-G4-01-CA1-03 | Alias vacío, espacios, 2/21 caracteres y símbolos no crean datos
    Dado un contexto aislado para "E2E-G4-105"
    Cuando realizo "Alias vacío, espacios, 2/21 caracteres y símbolos no crean datos" en "E2E-G4-105"
    Entonces verifico las reglas y la persistencia de "E2E-G4-105"

  @HU-G4-01 @TC-E2E-G4-106 @WEB-G4-01-CA1-04
  Escenario: E2E-G4-106 @HU-G4-01 @TC-E2E-G4-106 | WEB-G4-01-CA1-04 | Celular inválido, propio e inexistente; límite de longitud UI
    Dado un contexto aislado para "E2E-G4-106"
    Cuando realizo "Celular inválido, propio e inexistente; límite de longitud UI" en "E2E-G4-106"
    Entonces verifico las reglas y la persistencia de "E2E-G4-106"

  @HU-G4-01 @TC-E2E-G4-107 @WEB-G4-01-CA1-04
  Escenario: E2E-G4-107 @HU-G4-01 @TC-E2E-G4-107 | WEB-G4-01-CA1-04 | Cuenta cerrada se trata como celular no registrado
    Dado un contexto aislado para "E2E-G4-107"
    Cuando realizo "Cuenta cerrada se trata como celular no registrado" en "E2E-G4-107"
    Entonces verifico las reglas y la persistencia de "E2E-G4-107"

  @HU-G4-01 @HU-G4-02 @TC-E2E-G4-108 @WEB-G4-01-CA1-05 @WEB-G4-02-CA1-02
  Escenario: E2E-G4-108 @HU-G4-01 @HU-G4-02 @TC-E2E-G4-108 | WEB-G4-01-CA1-05 WEB-G4-02-CA1-02 | Contacto 15 permitido, 16 rechazado; paginación 10+5
    Dado un contexto aislado para "E2E-G4-108"
    Cuando realizo "Contacto 15 permitido, 16 rechazado; paginación 10+5" en "E2E-G4-108"
    Entonces verifico las reglas y la persistencia de "E2E-G4-108"

  @HU-G4-02 @TC-E2E-G4-109 @WEB-G4-02-CA1-01 @WEB-G4-02-CA1-02
  Escenario: E2E-G4-109 @HU-G4-02 @TC-E2E-G4-109 | WEB-G4-02-CA1-01 WEB-G4-02-CA1-02 | Lista vacía y frontera de páginas 10/11
    Dado un contexto aislado para "E2E-G4-109"
    Cuando realizo "Lista vacía y frontera de páginas 10/11" en "E2E-G4-109"
    Entonces verifico las reglas y la persistencia de "E2E-G4-109"

  @HU-G4-02 @TC-E2E-G4-110 @WEB-G4-02-CA1-01 @WEB-G4-02-CA3-01
  Escenario: E2E-G4-110 @HU-G4-02 @TC-E2E-G4-110 | WEB-G4-02-CA1-01 WEB-G4-02-CA3-01 | Favoritos primero, orden y nombre enmascarado
    Dado un contexto aislado para "E2E-G4-110"
    Cuando realizo "Favoritos primero, orden y nombre enmascarado" en "E2E-G4-110"
    Entonces verifico las reglas y la persistencia de "E2E-G4-110"

  @HU-G4-02 @TC-E2E-G4-111 @WEB-G4-02-CA2-01 @WEB-G4-02-CA2-02
  Escenario: E2E-G4-111 @HU-G4-02 @TC-E2E-G4-111 | WEB-G4-02-CA2-01 WEB-G4-02-CA2-02 | Búsqueda parcial sin mayúsculas/tildes, vacío y limpiar
    Dado un contexto aislado para "E2E-G4-111"
    Cuando realizo "Búsqueda parcial sin mayúsculas/tildes, vacío y limpiar" en "E2E-G4-111"
    Entonces verifico las reglas y la persistencia de "E2E-G4-111"

  @HU-G4-03 @TC-E2E-G4-112 @WEB-G4-03-CA1-01 @WEB-G4-03-CA1-02
  Escenario: E2E-G4-112 @HU-G4-03 @TC-E2E-G4-112 | WEB-G4-03-CA1-01 WEB-G4-03-CA1-02 | Editar sin duplicarse a sí mismo; límites, tilde y persistencia
    Dado un contexto aislado para "E2E-G4-112"
    Cuando realizo "Editar sin duplicarse a sí mismo; límites, tilde y persistencia" en "E2E-G4-112"
    Entonces verifico las reglas y la persistencia de "E2E-G4-112"

  @HU-G4-03 @TC-E2E-G4-113 @WEB-G4-03-CA1-02 @known_issue @D-01
  Escenario: E2E-G4-113 @HU-G4-03 @TC-E2E-G4-113 @known_issue @D-01 | WEB-G4-03-CA1-02 | [D-01] ñ debe ser válida al editar
    Dado un contexto aislado para "E2E-G4-113"
    Cuando realizo "[D-01] ñ debe ser válida al editar" en "E2E-G4-113"
    Entonces verifico las reglas y la persistencia de "E2E-G4-113"

  @HU-G4-03 @TC-E2E-G4-114 @WEB-G4-03-CA1-02
  Escenario: E2E-G4-114 @HU-G4-03 @TC-E2E-G4-114 | WEB-G4-03-CA1-02 | Edición inválida y duplicado por mayúsculas conservan datos
    Dado un contexto aislado para "E2E-G4-114"
    Cuando realizo "Edición inválida y duplicado por mayúsculas conservan datos" en "E2E-G4-114"
    Entonces verifico las reglas y la persistencia de "E2E-G4-114"

  @HU-G4-03 @TC-E2E-G4-115 @WEB-G4-03-CA1-02 @known_issue @D-02
  Escenario: E2E-G4-115 @HU-G4-03 @TC-E2E-G4-115 @known_issue @D-02 | WEB-G4-03-CA1-02 | [D-02] alias duplicado con espacios al editar debe rechazarse
    Dado un contexto aislado para "E2E-G4-115"
    Cuando realizo "[D-02] alias duplicado con espacios al editar debe rechazarse" en "E2E-G4-115"
    Entonces verifico las reglas y la persistencia de "E2E-G4-115"

  @HU-G4-03 @TC-E2E-G4-116 @WEB-G4-03-CA1-03
  Escenario: E2E-G4-116 @HU-G4-03 @TC-E2E-G4-116 | WEB-G4-03-CA1-03 | Favoritos 5/6, desmarcar y persistencia
    Dado un contexto aislado para "E2E-G4-116"
    Cuando realizo "Favoritos 5/6, desmarcar y persistencia" en "E2E-G4-116"
    Entonces verifico las reglas y la persistencia de "E2E-G4-116"

  @HU-G4-04 @TC-E2E-G4-117 @WEB-G4-04-CA1-01 @WEB-G4-04-CA1-02 @known_issue @D-07
  Escenario: E2E-G4-117 @HU-G4-04 @TC-E2E-G4-117 @known_issue @D-07 | WEB-G4-04-CA1-01 WEB-G4-04-CA1-02 | Eliminar conserva la transferencia y su movimiento
    Dado un contexto aislado para "E2E-G4-117"
    Cuando realizo "Eliminar conserva la transferencia y su movimiento" en "E2E-G4-117"
    Entonces verifico las reglas y la persistencia de "E2E-G4-117"

  @HU-G4-04 @TC-E2E-G4-118 @WEB-G4-04-CA2-01
  Escenario: E2E-G4-118 @HU-G4-04 @TC-E2E-G4-118 | WEB-G4-04-CA2-01 | Bloquear eliminación con solicitud enviada
    Dado un contexto aislado para "E2E-G4-118"
    Cuando realizo "Bloquear eliminación con solicitud enviada" en "E2E-G4-118"
    Entonces verifico las reglas y la persistencia de "E2E-G4-118"

  @HU-G4-04 @TC-E2E-G4-119 @WEB-G4-04-CA2-01
  Escenario: E2E-G4-119 @HU-G4-04 @TC-E2E-G4-119 | WEB-G4-04-CA2-01 | Bloquear eliminación con solicitud recibida
    Dado un contexto aislado para "E2E-G4-119"
    Cuando realizo "Bloquear eliminación con solicitud recibida" en "E2E-G4-119"
    Entonces verifico las reglas y la persistencia de "E2E-G4-119"

  @HU-G4-04 @TC-E2E-G4-120 @WEB-G4-04-CA2-02
  Escenario: E2E-G4-120 @HU-G4-04 @TC-E2E-G4-120 | WEB-G4-04-CA2-02 | Eliminar con solicitud resuelta
    Dado un contexto aislado para "E2E-G4-120"
    Cuando realizo "Eliminar con solicitud resuelta" en "E2E-G4-120"
    Entonces verifico las reglas y la persistencia de "E2E-G4-120"

  @HU-G4-04 @TC-E2E-G4-121 @WEB-G4-04-CA2-02
  Escenario: E2E-G4-121 @HU-G4-04 @TC-E2E-G4-121 | WEB-G4-04-CA2-02 | Eliminar con solicitud vencida
    Dado un contexto aislado para "E2E-G4-121"
    Cuando realizo "Eliminar con solicitud vencida" en "E2E-G4-121"
    Entonces verifico las reglas y la persistencia de "E2E-G4-121"

  @HU-G4-01 @TC-E2E-G4-001
  Escenario: E2E-G4-001 @HU-G4-01 @TC-E2E-G4-001 |  | Contactos reales E2E-G4-001 @HU-G4-01 @TC-E2E-G4-001 agrega un contacto y conserva sus datos al recargar
    Dado un contexto aislado para "E2E-G4-001"
    Cuando realizo "Contactos reales E2E-G4-001 @HU-G4-01 @TC-E2E-G4-001 agrega un contacto y conserva sus datos al recargar" en "E2E-G4-001"
    Entonces verifico las reglas y la persistencia de "E2E-G4-001"

  @HU-G4-01 @TC-E2E-G4-002
  Escenario: E2E-G4-002 @HU-G4-01 @TC-E2E-G4-002 |  | HU-G4-01 CA1 E2E-G4-002 @HU-G4-01 @TC-E2E-G4-002 rechaza alias de 2 caracteres sin crear un contacto
    Dado un contexto aislado para "E2E-G4-002"
    Cuando realizo "HU-G4-01 CA1 E2E-G4-002 @HU-G4-01 @TC-E2E-G4-002 rechaza alias de 2 caracteres sin crear un contacto" en "E2E-G4-002"
    Entonces verifico las reglas y la persistencia de "E2E-G4-002"

  @HU-G4-01 @TC-E2E-G4-003
  Escenario: E2E-G4-003 @HU-G4-01 @TC-E2E-G4-003 |  | HU-G4-01 CA1 E2E-G4-003 @HU-G4-01 @TC-E2E-G4-003 rechaza celular duplicado y conserva un único contacto
    Dado un contexto aislado para "E2E-G4-003"
    Cuando realizo "HU-G4-01 CA1 E2E-G4-003 @HU-G4-01 @TC-E2E-G4-003 rechaza celular duplicado y conserva un único contacto" en "E2E-G4-003"
    Entonces verifico las reglas y la persistencia de "E2E-G4-003"
