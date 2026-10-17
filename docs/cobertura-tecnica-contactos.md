# Cobertura revisada de Contactos: qué demostramos y qué falta

La docente distingue cobertura funcional (CA y reglas) y técnica (OpenAPI).
Esta revisión no equivale a una declaración de cobertura del 100 %.
Fuentes: `referencias/qolqe-wallet/docs/requisitos.md` y `data/openapi-original.json`,
sin alterar el contrato para hacer aprobar pruebas.

## Funcional: requisito → técnica → caso verificable

| Requisito | Qué se comprueba / por qué | Casos |
|---|---|---|
| HU-G4-01 CA1 / R-G4-01 | Celular propio, mal formado, inexistente, cerrado y duplicado son clases distintas | G4-012 a G4-016, G4-106 |
| HU-G4-01 CA1 / R-G4-02 | Longitudes 2/3/20/21: ambos extremos inclusivos; clases de letras, tildes, ñ, números, espacios y símbolo inválido | G4-001 a G4-011 |
| HU-G4-01 CA1 / R-G4-02 | Unicidad sin mayúsculas y recorte: cambiar un solo factor permite explicar el defecto | G4-017, G4-018 |
| HU-G4-01 CA1 / R-G4-03 | Capacidad 15/16 con contexto de 14; límite superior y ausencia de creación al rechazar | G4-019 |
| HU-G4-02 CA1 | Orden de favoritos y alias en ambos grupos; 10/11 separa páginas | G4-021, G4-022, G4-107 |
| HU-G4-02 CA2 | Igualdad sin mayúsculas/tildes no demuestra coincidencia parcial: se añade fragmento OFIC de José oficina | G4-020, G4-023, CF-04 |
| HU-G4-02 CA3 | Alias, máscara exacta del nombre, celular y favorito; presencia y tipos no sustituyen el contenido correcto | G4-020, CT-06 |
| HU-G4-03 CA1 / R-G4-02 | La validación al crear no demuestra la validación al editar: repetir fronteras y clases válidas/ inválidas | G4-024, CF-01, CF-02, CT-02 |
| HU-G4-03 CA1 / R-G4-02 | Alias propio permitido; alias ajeno duplicado tras normalizar rechazado | G4-024, CF-03 |
| HU-G4-03 CA1 / R-G4-03 | Marcar/desmarcar: transición de estado; 5/6: límite de favoritos; editar alias conserva otros campos | G4-025, G4-026, G4-108 |
| HU-G4-04 CA1 | Eliminar sin borrar transferencia; permiso de usuario distinto mantiene el recurso | G4-028, CF-05 |
| HU-G4-04 CA2 | Tabla de decisión: pendiente vigente enviada/recibida impide eliminar; vencida permite | G4-029, G4-030, G4-031 |

`CF-*` están en `features/complemento-contactos.feature` y conservan tags de HU.
Son variantes añadidas tras la revisión; no se adjudican retroactivamente a la
ejecución histórica de 116 casos del 13 de octubre.

## Técnica: restricciones explícitas del CRUD

| Contrato / restricción | Ejemplos y aserciones | Tag |
|---|---|---|
| POST SolicitudContacto.required | Omitir alias; omitir celular; cuerpo vacío o ausente: 422 y ningún contacto creado | CT-01 |
| POST alias/celular son string, no nullable | null, número, booleano, objeto y arreglo: 422; verificar lista vacía | CT-01 |
| POST celular minLength/maxLength/pattern | 8/10 caracteres, primer dígito 8 y letras: 422 | CT-01 |
| POST alias minLength/maxLength/pattern | 2/3/20/21 y caracteres permitidos/prohibidos ya están en casos funcionales | G4-001 a G4-011 |
| PUT CambioContacto.alias | Tipos inválidos y longitudes 2/21: 422, contacto original conservado | CT-02 |
| PUT CambioContacto.favorito boolean | Texto 'true'/'false', 1/0, objeto y arreglo deben rechazarse según esquema; no aceptar coerción por conveniencia | CT-02 |
| PUT campos opcionales y nullable | Objeto vacío, alias null y favorito null admitidos; estado conservado | CT-03 |
| GET pagina integer, mínimo 1 | 0, -1, 1.5 y texto: 422; página 1 válida en CT-06 | CT-04, CT-06 |
| PUT/DELETE contacto_id integer | Ruta no-entero: 422 | CT-05 |
| Respuestas Contacto y PaginaContactos | Campos requeridos, tipos, patrón celular, página ≥1, tamaño10 y lista de Contacto; CRUD con 201/200/204 sin cuerpo | CT-06 |
| Security HTTPBearer en las cuatro operaciones | Sin token: 401 NO_AUTENTICADO; no basta comprobarlo solo en GET | CT-07 |
| Authorization Bearer con JWT malformado en las cuatro operaciones | 401 NO_AUTENTICADO; verificar que el contacto original se conserva | CT-08 |
| PUT alias con símbolo prohibido | R-G4-02 y descripción CambioContacto (mismas reglas al agregar): 422 ALIAS_INVALIDO y sin modificación | CT-09 |

`CT-*` están en `features/contrato-contactos.feature` y llevan tags de sus HU.
Los casos técnicos aplican partición de equivalencia por tipo/ausencia/nulo y
valores límite por longitud/página. No se exige un campo opcional ni se prohíbe
null donde OpenAPI lo admite. Los campos adicionales no se rechazan: el contrato
no declara `additionalProperties:false`.

La única cabecera de autenticación exigida aquí se deriva de HTTPBearer:
`Authorization: Bearer <token>`. No se inventan cabeceras obligatorias ajenas al
contrato. CT-07 comprueba ausencia y CT-08 token malformado. Los cuerpos de estas
pruebas usan JSON; el alcance actual no demuestra todas las variantes de tipo
de contenido ni JSON sintácticamente mal formado.

## Ejecución y lectura del resultado

Primera verificación, anterior a CT-08/CT-09: **60 escenarios ejecutados,
54 aprobados y 6 fallidos**, con usuarios propios por escenario y sin mocks.
El diseño actual contiene 53 filas CT y 12 CF (65 complementarias).
CT-08/CT-09 se verificaron posteriormente junto con dos casos funcionales:
7 seleccionados, 7 aprobados; [detalle y límites](incidencia-consistencia.md).
Los seis fallos de la primera revisión se
agrupan en tres comportamientos; no son seis defectos independientes:

- CF-01, alias «Niño» al editar: esperado 200, obtenido 422; amplía la
  reproducción del defecto funcional de ñ ya observado al crear.
- CF-03, duplicado « Ana » al editar: esperado 409, obtenido 200; amplía la
  reproducción del defecto de unicidad tras recortar espacios.
- CT-02, cuatro variantes de favorito (`"true"`, `"false"`, `1`, `0`): esperado
  422 según el tipo boolean del contrato, obtenido 200. Es una discrepancia
  técnica entre esquema y coerción del servidor, separada del comportamiento
  funcional de marcar favorito. Revisar con la docente si corresponde endurecer
  implementación o documentar esa entrada; no modificar silenciosamente OpenAPI.

Los resultados de esta revisión se guardan aparte en
`reports/revision-contactos-20261016.json`. El reporte nativo local contiene
las peticiones y aserciones; incluye credenciales sintéticas y no debe publicarse
sin redactar tokens. Los resúmenes compartidos no incluyen esos valores.

Un fallo de preparación no demuestra un defecto del producto. Un fallo de
aserción requiere revisar petición, respuesta y fuente del esperado. Si el
servidor acepta un booleano representado como string o número, registrar la
diferencia respecto de OpenAPI como hallazgo técnico, separado del defecto
funcional del alias ñ. No alterar el esperado para que coincida con la respuesta.

## Límites y pendientes que debemos reconocer

- La corrida completa posterior reveló una incidencia de disponibilidad de
  registros recién creados. Se documentan los fallos originales y la política
  explícita de sondeo de preparación en [incidencia de consistencia](incidencia-consistencia.md).

- La auditoría detallada de esta tabla cubre HU-G4-01 a HU-G4-04. HU-G4-05 a
  HU-G4-10 y núcleo siguen en `docs/cobertura.md`, con pendientes propios.
- Schemathesis exploró 9 operaciones, con problemas de contexto documentados en
  `docs/revision-contrato.md`; sus 400 casos no acreditan por sí solos cobertura
  técnica completa ni sustituyen los CT explícitos.
- Falta completar una matriz técnica equivalente para solicitudes y operaciones
  comunes: obligatorio, tipo, null, enum, longitudes y respuestas por operación.
- Siguen pendientes dígitos Unicode, patrones con espacios de extremos y su
  interacción con longitudes, parámetros repetidos y pruebas de cuerpo JSON mal
  formado / tipo de contenido. No afirmar que esta revisión agota OpenAPI.
- En los flujos financieros faltan variantes de destino cerrado, detalle exacto
  de SMS, filtros por cada estado y aceptación simultánea; se mantienen visibles.
