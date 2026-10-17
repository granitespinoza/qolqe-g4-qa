# Contraste entre requisitos, OpenAPI e implementación

Revisión del código original fijado en `8c7d2f0c939ede7765b7b80b98c10c3905693fda`. No se modifica la aplicación para conseguir pruebas verdes. Las líneas siguientes corresponden a esa referencia; se complementan con las evidencias HTTP ya conservadas.

## Qué demuestra cada fuente

- **Requisitos:** definen el comportamiento funcional esperado. `docs/requisitos.md` de la referencia, líneas 254–298, contiene reglas y HU de G4.
- **OpenAPI:** define entradas, salidas y restricciones técnicas. La API se documenta con los modelos de `qolqe/api/` y el enriquecimiento de `qolqe/contrato.py`; el snapshot recibido está en `data/openapi-original.json`.
- **Código:** explica cómo está implementado el comportamiento. Una lectura puede localizar una causa probable; no reemplaza la reproducción HTTP.
- **Karate/Schemathesis:** proporcionan resultados observados para datos, contexto y ejecución concretos. Un resultado verde no demuestra una regla que carece de escenario.

## Incumplimientos reproducidos y explicación en el código

| Hallazgo | Lo que exige la documentación | Lo que hace el código | Evidencia y clasificación |
|---|---|---|---|
| D-01: alias con ñ | R-G4-02, requisitos línea 256, permite ñ. El patrón OpenAPI, `qolqe/contrato.py:630`, también la incluye. | `qolqe/reglas/contactos.py:9` define un patrón que omite Ñ/ñ; se aplica en líneas 29 y 41. `qolqe/api/contactos.py:77` convierte el rechazo en `ALIAS_INVALIDO`. | [G4-004](../evidencias/G4-004.html): esperado 201, obtenido 422. Incumplimiento funcional y desacuerdo con el patrón técnico. La lectura explica el rechazo observado. |
| D-02: duplicado tras recortar | R-G4-02 exige recortar espacios y que el alias sea único sin distinguir mayúsculas. | `qolqe/reglas/contactos.py:24` compara el valor sin recortar; `strip()` ocurre después, en línea 26. La edición repite ese orden en líneas 36 y 38. | [G4-018](../evidencias/G4-018.html): agregar « Ana » después de Ana obtiene 201 en vez de 409. El caso reproducido corresponde al alta; no atribuir a edición una ejecución que no se haya realizado. |
| D-03: aceptar solicitud vencida | R-G4-05 y HU-G4-08 CA4, requisitos líneas 259 y 292, impiden aceptar después del vencimiento de 48 h. | `qolqe/reglas/contactos.py:72` calcula VENCIDA al llegar al plazo. Rechazar/cancelar llaman a `_exigir_pendiente` (`qolqe/api/solicitudes.py:175` y `:191`). Aceptar compara únicamente el estado guardado, línea 156, y omite esa comprobación temporal. | [G4-053](../evidencias/G4-053.html), [G4-054](../evidencias/G4-054.html): 200 en lugar de 409. El código explica por qué consulta y aceptación pueden discrepar en el estado. |
| D-04: token válido tras logout | HU-N-03 y R-G6-04 exigen invalidación inmediata de la sesión. | `qolqe/api/autenticacion.py:159` guarda el identificador jti en `tokens_revocados`; `qolqe/dependencias.py:47` consulta esa columna usando el token completo. Son valores distintos. | [G4-074](../evidencias/G4-074.html): después de logout se obtiene 200 en vez de 401. Pertenece al núcleo común; afecta al acceso protegido de G4. |
| D-05: saldo y límite bajo concurrencia | HU-N-07 exige conservar saldo y límite ante solicitudes simultáneas. | `qolqe/transacciones.py:62` comprueba saldo y `:67` comprueba límite antes de mover saldo en `:76`. Ese orden por sí solo no demuestra una carrera: hay que verificar además el manejo de transacciones y reproducir concurrencia. | [G4-116](../evidencias/G4-116.html) y `reports/concurrencia.json` conservan la prueba simultánea. La evidencia dinámica fundamenta el defecto; la lectura aislada solo señala la zona a investigar. |

Los enlaces de evidencia corresponden a las ejecuciones identificadas al generarlas. Para afirmar que un defecto persiste en una ejecución nueva, abrir su reporte actual y comprobar su resultado; no trasladar automáticamente la fecha de esta revisión a los registros históricos.

## Observación que requiere decisión y prueba específica

**H-01: longitud del alias antes o después de recortar.** La regla R-G4-02 y la implementación (`qolqe/reglas/contactos.py:26`) describen/realizan el recorte antes de comprobar la longitud. OpenAPI incorpora `maxLength:20` al valor recibido (`qolqe/contrato.py:630`). Un alias con 20 caracteres internos y espacios exteriores podría ser válido funcionalmente y quedar fuera del esquema de entrada por su longitud bruta. Esto es una discrepancia de interpretación del contrato: no es un nuevo defecto confirmado en esta revisión. Preparar el dato, contrastar ambas fuentes y consultar el criterio esperado; no alterar el esquema silenciosamente.

## Cómo usamos Schemathesis sin confundir contexto con defecto

El ejecutor mantiene las fases `examples,coverage,fuzzing` y añade **ejemplos de control** con recursos reales para las operaciones de contactos y solicitudes. `scripts/schemathesis_context.py` utiliza hooks de la versión instalada 4.17.0:

1. `before_add_examples` añade un ejemplo explícito por operación seleccionada.
2. `before_call` prepara usuarios propios, contacto o solicitud pendiente, rol correcto y saldo de prueba para aceptar. Solo lo hace para los ejemplos añadidos; no corrige los valores aleatorios generados.
3. `after_call` registra el estado HTTP de esos controles en `controles-contexto.json`. No cambia respuestas ni elimina fallos.

La ejecución `20261017T020510Z-9ea00f` confirmó los nueve controles con respuestas de éxito; hubo dos reintentos de login durante la preparación, que quedan registrados junto con las verificaciones de visibilidad. [Resultados y límites actuales](revision-contrato.md).

El OpenAPI original permanece intacto y se captura en la carpeta de ejecución. Los usuarios de control son nuevos para cada operación: no dependen de IDs de la semilla ni del estado dejado por un CRUD anterior. Los reportes HAR y NDJSON permiten revisar las peticiones reales; permanecen locales porque pueden contener datos de sesión de prueba.

La generación conserva también combinaciones cuyo contexto de negocio puede ser inválido. Por ejemplo, un número de contacto que cumple el tipo `integer` no garantiza que exista ni pertenezca al usuario: un 404 puede ser correcto. Igualmente, responder 422 a un cuerpo sin campos obligatorios es un rechazo esperado. Cada señal debe contrastarse con el cuerpo enviado, autenticación, propiedad del recurso, estado y restricción del esquema antes de registrar un defecto.

Los hooks están documentados oficialmente en [Hooks de Schemathesis](https://schemathesis.readthedocs.io/en/latest/reference/hooks/) y [Extender Schemathesis](https://schemathesis.readthedocs.io/en/stable/guides/extending/). La compatibilidad concreta se contrasta además con el código de la versión instalada. Estas herramientas complementan las pruebas funcionales; no sustituyen la matriz CA/regla → escenario → aserción → evidencia.
