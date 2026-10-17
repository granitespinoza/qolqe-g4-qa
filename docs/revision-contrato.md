# Revisión de contrato — Schemathesis

## Nueva ejecución con contexto real: 16 de octubre de 2026, 21:05 (Lima)

Ejecución `20261017T020510Z-9ea00f`, Schemathesis 4.17.0: **562 casos generados, 138 omitidos, 4 señales únicas, 0 errores de hooks y 2 advertencias**. Salida 1: no es una ejecución completamente aprobada. La fecha del identificador está en UTC. [Resumen público de esta ejecución](../reports/schemathesis-actual.json).

Se añadieron nueve ejemplos de control independientes de los datos aleatorios. Todos alcanzaron una respuesta de éxito con recursos propios y rol correcto:

| Operación | Respuesta del control |
|---|---|
| POST contactos | 201 |
| GET contactos | 200 |
| PUT contacto propio | 200 |
| DELETE contacto propio sin pendientes | 204 |
| POST solicitudes | 201 |
| GET solicitudes | 200 |
| Aceptar como destinatario con saldo | 200 |
| Rechazar como destinatario | 200 |
| Cancelar como solicitante | 200 |

La preparación verifica que el contacto y la solicitud creados sean visibles mediante consultas antes de enviar la operación bajo prueba. Hubo **dos reintentos de preparación de login** tras 401 `CREDENCIALES_INVALIDAS`, registrados en `preparacion-contexto.json` y en el resumen público. No se repitió una operación funcional fallida para convertirla en aprobada. La confirmación de BD después de responder en la dependencia de FastAPI es una causa posible de esa falta de visibilidad; requiere investigación separada, no se atribuye al comportamiento del CRUD evaluado.

Se conservaron las comprobaciones de autenticación: el HAR contiene también **177 respuestas 401**. Los controles manuales se declaran explícitamente autenticados en los metadatos de Schemathesis 4.17; de lo contrario el analizador los interpreta como tokens aleatorios aunque sean JWT reales. Esto no excluye `ignored_auth` ni reinyecta tokens en sus peticiones sin credenciales. El código del hook coincide con la huella SHA256 guardada al inicio de esta ejecución.

Las cuatro señales corresponden a las mismas categorías de interpretación de la tabla inferior. Siguen siendo señales por investigar, **no cuatro defectos confirmados**. Persisten advertencias por 404 en cinco operaciones y discrepancias de validación en cinco operaciones durante la generación automática; los nueve controles exitosos no borran esas limitaciones ni demuestran todos los CA.

Se mantienen sin modificar el esquema original, sus restricciones, las entradas generadas y las respuestas obtenidas. Los reportes completos JUnit/NDJSON/HAR son locales; el resumen público no contiene tokens. [Contraste con el código y los requisitos](contraste-documentacion-codigo.md).

## Complemento explícito tras la revisión docente

La exploración descrita abajo no prueba todos los tipos y campos obligatorios.
Se añadieron casos Karate verificables por campo para el CRUD de Contactos:
[matriz funcional y técnica](cobertura-tecnica-contactos.md),
`features/contrato-contactos.feature` y `features/complemento-contactos.feature`.
Sus ejecuciones y hallazgos se registran aparte de los 116 casos históricos.

## Ejecución exploratoria histórica
Schemathesis 4.17.0; fases examples, coverage y fuzzing. Stateful desactivado. Semilla 20261013, un worker, máximo 20 ejemplos de fuzzing por operación (no 20 peticiones totales).
9 operaciones G4 seleccionadas de 69; 400 casos generados, 72 omitidos, 4 fallos únicos señalados y 2 advertencias. [Salida redactada](../reports/schemathesis.txt).

## Interpretación de hallazgos
| Petición / respuesta | Interpretación | Próxima comprobación |
|---|---|---|
| POST solicitudes con solo contacto_id devuelve 422, pero se generó como válida | Señal automática pendiente: el snapshot sí declara obligatorios contacto_id, monto y motivo | Rechazar esa petición es correcto; investigar generación/clasificación de Schemathesis antes de atribuir un defecto |
| Alias largo devuelve 409 CONTACTO_EXISTENTE | La clasificación automática no implica que se haya creado un contacto inválido: intervino un duplicado | Repetir con celular propio de contexto que aún no sea contacto y verificar ausencia de creación |
| Celular con dígitos Unicode genera 422 | Posible diferencia entre regex del contrato y validación del código | Revisar la semántica de digit y definir con requisitos si se admiten solamente dígitos ASCII |
| GET solicitudes?estado=null devuelve 422 | Diferencia entre null del esquema y texto literal «null» en query | Reproducir omitiendo estado; no asumir que la cadena null equivale a ausencia |

## Límites que debemos explicar
6 operaciones devolvieron repetidamente 404 por falta de identificadores propios. Por ello esta ejecución NO acredita toda la lógica de esos endpoints.
5 operaciones generaron mayormente errores de validación. No se afirma cobertura técnica completa.
Los reportes originales están en reports/raw/schemathesis y el workflow los conserva. Los tokens están ocultos en la versión compartida.
Karate utiliza contactos y solicitudes existentes creados por cada escenario; complementa estos límites de contexto, pero no sustituye mejorar la configuración de Schemathesis.

## Qué es defecto y qué es observación
Incumplimiento de requisito o esquema: investigar como defecto de implementación o contrato. Apartarse de una convención manteniendo el contrato: registrar como observación justificada, según Clase 10.
No modificar el contrato original para eliminar fallos. Conservar su snapshot y anotar la discrepancia.
