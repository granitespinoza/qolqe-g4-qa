# Usabilidad complementaria — G4

## Decisión y alcance
Incorporar una evaluación heurística breve de la interfaz Qolqe para la Parte 2 (web). En Parte 1 solo describimos el método y los riesgos relacionados; una respuesta API no demuestra usabilidad.
No hay evidencia de que la docente haya exigido heurísticas o conceda puntos extra por ellas. Su utilidad es justificar decisiones y observaciones con capturas y consecuencias para el usuario.

## Heurísticas seleccionadas
| Heurística de Nielsen | Relación con G4 | Qué observar | Evidencia y clasificación |
|---|---|---|---|
| H1 Visibilidad del estado | HU-G4-01 y HU-G4-07 | Tras agregar, ¿se ve el contacto y el resultado? ¿Enviadas, recibidas y vencidas se distinguen claramente? | Captura antes/después y respuesta API. Incumplimiento de CA si falta el comportamiento exigido; observación UX si solo falta claridad |
| H5 Prevención de errores | HU-G4-01/03/06/08 | ¿Se muestran límites de alias/monto? ¿Una acción financiera informa destinatario e importe antes de ejecutarse? | Captura del formulario y flujo. La confirmación previa es recomendación UX si el requisito no la exige |
| H9 Reconocer y recuperarse de errores | HU-G4-01 y HU-G4-08 CA2 | ¿Un alias duplicado o saldo insuficiente produce un mensaje comprensible y permite corregir el intento? | Captura del mensaje y estado posterior. Error técnico exigido por API y calidad del mensaje UI se evalúan por separado |
| H6 Reconocer en vez de recordar | HU-G4-02/05/06 | ¿Alias, búsqueda y selección de contactos evitan memorizar celulares? | Captura de búsqueda/selector. Vincular a CA y probar el flujo web |

## Ficha por observación
ID · HU/CA · pantalla · tarea · heurística · condición observada · consecuencia para el usuario · captura · recomendación · clasificación · estado de verificación.
Priorizar por bloqueo de tarea, frecuencia y posibilidad de recuperación. No asignar gravedad únicamente por preferencia estética.

## Cómo entra a la exposición
Una observación concreta, si está verificada, dentro de la HU elegida: «Aplicamos H9 porque el usuario necesita corregir un alias duplicado. Aquí se observa el mensaje, la corrección y el contacto finalmente creado». No añadir una exposición teórica de las diez heurísticas.
Las heurísticas orientan la inspección; particiones, valores límite y transiciones siguen justificando los escenarios funcionales.

## Documentación HTML del equipo
Puede revisarse también con H6 (menú por módulos), H4 (métodos HTTP consistentes y rotulados, no solo colores) y H10 (ejemplos y ayuda). Es calidad de nuestro artefacto, no cobertura de la interfaz Qolqe.

## Estado
Plan de evaluación, todavía sin hallazgos de interfaz confirmados ni pruebas de usuarios. La revisión de código HTML por sí sola no demuestra el comportamiento visual.

Fuente: Jakob Nielsen, https://www.nngroup.com/articles/ten-usability-heuristics/
