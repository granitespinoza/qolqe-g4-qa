# Revisión de contrato — Schemathesis

## Ejecución exploratoria real
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
