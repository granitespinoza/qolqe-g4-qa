# Alcance y matriz de diseño — línea base del paso 1

18 CA de HU-G4-01 a HU-G4-10. Núcleo solo como dependencia de estos flujos. API histórica de núcleo se conserva.

Clasificación técnica del alcance G4 aprobada para el plan; no es una clasificación emitida por la docente.

Fuente: `referencias/qolqe-wallet/docs/requisitos.md`, commit `8c7d2f0c939ede7765b7b80b98c10c3905693fda`.

**Presencia de código no significa prueba aprobada ni cobertura completa.** Esta matriz es de diseño; los resultados API están en el diagnóstico. La trazabilidad automática al pipeline corresponde al paso 6.

Generar: `python scripts/build_scope.py`. Verificar sin escribir: `python scripts/build_scope.py --check`.

Estado posterior de implementación y ejecución: [verificación web de pasos 3–4](verificacion-web.md). Los estados parcial/pendiente siguientes describen la línea base, no el resultado actual.

## Criterios

| HU / CA | Nivel | Casos API existentes | Casos web existentes | Cobertura web |
|---|---|---|---|---|
| HU-G4-01-CA1 | web+api | G4-001, G4-002, G4-003, G4-004, G4-005, G4-006, G4-007, G4-008, G4-009, G4-010, G4-011, G4-012, G4-013, G4-014, G4-015, G4-016, G4-017, G4-018, G4-019, G4-106 | E2E-G4-001, E2E-G4-002, E2E-G4-003 | parcial |
| HU-G4-02-CA1 | web+api | G4-021, G4-022, G4-107 | — | pendiente |
| HU-G4-02-CA2 | web+api | G4-020, G4-023, CF-04 | — | pendiente |
| HU-G4-02-CA3 | web+api | G4-020 | E2E-G4-001 | parcial |
| HU-G4-03-CA1 | web+api | G4-024, G4-025, G4-026, G4-027, G4-108, CF-01, CF-02, CF-03 | — | pendiente |
| HU-G4-04-CA1 | web+api | G4-028, CF-05 | — | pendiente |
| HU-G4-04-CA2 | web+api | G4-029, G4-030, G4-031 | — | pendiente |
| HU-G4-05-CA1 | web+api | G4-032, G4-033, G4-095 | — | pendiente |
| HU-G4-06-CA1 | web+api | G4-034, G4-035, G4-036, G4-037, G4-038, G4-039, G4-040, G4-041, G4-042, G4-043, G4-044, G4-109 | — | pendiente |
| HU-G4-06-CA2 | web+api | G4-034 | — | pendiente |
| HU-G4-07-CA1 | web+api | G4-045 | — | pendiente |
| HU-G4-07-CA2 | web+api | G4-046, G4-047, G4-048 | — | pendiente |
| HU-G4-08-CA1 | web+api | G4-049, G4-096 | — | pendiente |
| HU-G4-08-CA2 | web+api | G4-050, G4-096 | — | pendiente |
| HU-G4-08-CA3 | web+api | G4-049 | — | pendiente |
| HU-G4-08-CA4 | web+api | G4-049, G4-051, G4-052, G4-053, G4-054, G4-055, G4-097, G4-100, G4-103 | — | pendiente |
| HU-G4-09-CA1 | web+api | G4-056, G4-057, G4-058, G4-059, G4-064, G4-065, G4-066, G4-098, G4-101, G4-104 | — | pendiente |
| HU-G4-10-CA1 | web+api | G4-060, G4-061, G4-062, G4-063, G4-099, G4-102, G4-105 | — | pendiente |

## Diseño web pendiente

En esta línea base, los identificadores WEB son grupos de variantes planificadas. Su implementación y ejecución posterior se documentan en verificacion-web.md. Cada grupo puede producir varios tests parametrizados. Los tres E2E existentes se reutilizan al implementarlos.

### HU-G4-01-CA1 — Alta de contactos

Ruta: `/contactos`. Complemento API: API complementa tipos JSON, autenticación y propiedad; R-G4-03 favoritos se ejerce en edición.

- **WEB-G4-01-CA1-01**: Alta válida y persistencia; alias de 3 y 20 caracteres, tildes, ñ, números y espacios.
- **WEB-G4-01-CA1-02**: Normalización de espacios; alias duplicado por mayúsculas y por espacios.
- **WEB-G4-01-CA1-03**: Alias vacío, 2 y 21 caracteres, símbolos no permitidos.
- **WEB-G4-01-CA1-04**: Celular inválido, propio, inexistente, cerrado y contacto duplicado.
- **WEB-G4-01-CA1-05**: Límite: crear el contacto 15 y rechazar el 16 sin alterar la lista.

### HU-G4-02-CA1 — Orden y paginación

Ruta: `/contactos`. Complemento API: API comprueba parámetros de paginación inválidos.

- **WEB-G4-02-CA1-01**: Lista vacía; favoritos primero y orden por alias dentro de cada grupo.
- **WEB-G4-02-CA1-02**: 10 por página: 10/11/15 contactos, navegación anterior/siguiente y total.

### HU-G4-02-CA2 — Búsqueda

Ruta: `/contactos`. Complemento API: API confirma la búsqueda sobre datos propios.

- **WEB-G4-02-CA2-01**: Fragmento, mayúsculas y tildes: jose encuentra José.
- **WEB-G4-02-CA2-02**: Sin coincidencias y limpiar búsqueda restaura la lista.

### HU-G4-02-CA3 — Datos visibles

Ruta: `/contactos`. Complemento API: No basta verificar solamente alias y celular.

- **WEB-G4-02-CA3-01**: Alias, nombre enmascarado, celular e indicador de favorito.

### HU-G4-03-CA1 — Edición y favoritos

Ruta: `/contactos`. Complemento API: API cubre tipos no representables en el formulario y acceso a recursos ajenos.

- **WEB-G4-03-CA1-01**: Editar alias válido y conservarlo sin considerarlo duplicado consigo mismo; persistencia.
- **WEB-G4-03-CA1-02**: Límites 2/3/20/21, ñ, símbolos y duplicados normalizados al editar.
- **WEB-G4-03-CA1-03**: Marcar y desmarcar; permitir favorito 5 y rechazar 6 sin modificar los demás.

### HU-G4-04-CA1 — Eliminación e historial

Ruta: `/contactos`. Complemento API: API verifica que los movimientos financieros no se borraron.

- **WEB-G4-04-CA1-01**: Eliminar y comprobar ausencia tras recargar.
- **WEB-G4-04-CA1-02**: Transferencias previas permanecen visibles en movimientos.

### HU-G4-04-CA2 — Bloqueo de eliminación

Ruta: `/contactos`. Complemento API: Preparar cada estado por API y reloj de pruebas, sin esperar 48 horas.

- **WEB-G4-04-CA2-01**: Bloquear eliminación con solicitud pendiente enviada y recibida.
- **WEB-G4-04-CA2-02**: Permitir cuando resuelta o vencida; verificar mensaje y conservación del contacto si falla.

### HU-G4-05-CA1 — Transferencia desde contacto

Ruta: `/contactos → /transferir`. Complemento API: HU-N-07 CA1–4; concurrencia CA5 y manipulación de destinatario ajeno/propio se verifican por API.

- **WEB-G4-05-CA1-01**: Seleccionar contacto y transferir: destinatario, comprobante y persistencia.
- **WEB-G4-05-CA1-02**: Monto 0/0.01/500/500.01 y más de 2 decimales; descripción hasta 60.
- **WEB-G4-05-CA1-03**: Saldo insuficiente, límite diario y destino cerrado: error sin débito.

### HU-G4-06-CA1 — Crear solicitud

Ruta: `/solicitudes`. Complemento API: API comprueba ID de contacto ajeno/inexistente y tipos no representables en UI.

- **WEB-G4-06-CA1-01**: Elegir contacto, monto y motivo válidos; límites de monto y motivo 2/3/60/61.
- **WEB-G4-06-CA1-02**: Sin contacto y datos inválidos: mensaje sin crear solicitud.
- **WEB-G4-06-CA1-03**: Permitir pendiente 10 y rechazar 11.

### HU-G4-06-CA2 — Estado, vencimiento y aviso

Ruta: `/solicitudes`. Complemento API: API verifica diferencia exacta de 48 horas y contenido/destinatario del SMS simulado.

- **WEB-G4-06-CA2-01**: Nueva solicitud en enviadas/recibidas: PENDIENTE y vencimiento mostrado.

### HU-G4-07-CA1 — Vistas y filtros

Ruta: `/solicitudes`. Complemento API: API cubre aislamiento entre usuarios y filtro inválido.

- **WEB-G4-07-CA1-01**: Separar enviadas y recibidas para dos actores.
- **WEB-G4-07-CA1-02**: Filtrar PENDIENTE/ACEPTADA/RECHAZADA/CANCELADA/VENCIDA y Todos; lista vacía.

### HU-G4-07-CA2 — Vencimiento visible

Ruta: `/solicitudes`. Complemento API: Preparar reloj controlado y renovar sesión; no esperar tiempo real.

- **WEB-G4-07-CA2-01**: Antes de 48h pendiente; a las 48h y después vencida al actualizar.

### HU-G4-08-CA1 — Aceptar y transferir

Ruta: `/solicitudes`. Complemento API: API complementa invariantes monetarias de HU-N-07 y concurrencia.

- **WEB-G4-08-CA1-01**: Destinatario acepta con saldo y límite disponibles; saldo y movimiento correctos.

### HU-G4-08-CA2 — Aceptación fallida

Ruta: `/solicitudes`. Complemento API: Comprobar ausencia de transferencia por API además del estado mostrado.

- **WEB-G4-08-CA2-01**: Saldo insuficiente y límite diario: error visible, conserva PENDIENTE y dinero.

### HU-G4-08-CA3 — Resultado de aceptación

Ruta: `/solicitudes`. Complemento API: API verifica SMS al solicitante y código compartido de movimientos.

- **WEB-G4-08-CA3-01**: Estado ACEPTADA, código de operación asociado y persistencia.

### HU-G4-08-CA4 — Permisos y transición

Ruta: `/solicitudes`. Complemento API: API verifica 404 ajeno y 409 al invocar directamente, incluida la frontera 48h sin listar antes.

- **WEB-G4-08-CA4-01**: Acción aceptar disponible solo al destinatario en solicitud pendiente vigente.
- **WEB-G4-08-CA4-02**: Solicitud resuelta o vencida no permite nueva aceptación desde UI.

### HU-G4-09-CA1 — Rechazo

Ruta: `/solicitudes`. Complemento API: API verifica SMS, permisos y transición directa sin depender de botones ocultos.

- **WEB-G4-09-CA1-01**: Rechazar sin motivo y con motivo de hasta 60; persistencia RECHAZADA.
- **WEB-G4-09-CA1-02**: Motivo 61 inválido; acciones según actor, estado y vencimiento.

### HU-G4-10-CA1 — Cancelación

Ruta: `/solicitudes`. Complemento API: API verifica 404 ajeno y 409 de transición directa.

- **WEB-G4-10-CA1-01**: Solicitante cancela pendiente vigente; persistencia CANCELADA.
- **WEB-G4-10-CA1-02**: Otros actores, resueltas y vencidas no ofrecen cancelación válida.

## Dependencias del núcleo

- **HU-N-02 CA1**: Login UI como precondición; no acredita todos los CA de autenticación.
- **HU-N-04 CA1**: Saldo observable tras operaciones; verificar precisión por API.
- **HU-N-07 CA1,2,3,4,5**: CA1–4 por web+API en transferencias G4; CA5 concurrencia por API.
- **HU-N-03 CA1,2**: API de revocación conservada; logout UI no reemplaza prueba de token.

## Límites y criterio de finalización

Otros módulos G1/G2/G3/G5/G6 independientes; IA y fallo didáctico no cuentan como cobertura de regresión.

El SMS se consulta por API de pruebas; no existe un teléfono real en la demo. Concurrencia y peticiones manipuladas se verifican por API. La web debe comprobar la visibilidad de acciones, mensajes, estados y persistencia. Un botón oculto no demuestra autorización del servidor.

No se declara ningún CA web completo en esta etapa. Solo se podrá cerrar un criterio tras implementar sus variantes, revisar sus aserciones y asociar resultados reales. La matriz de la docente, si existe una clasificación adicional, prevalece sobre este alcance técnico.
