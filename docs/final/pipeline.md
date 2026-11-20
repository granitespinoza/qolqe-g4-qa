# Workflow final y reportería visible

`pruebas.yml` se dispara en push a main o codex/**, pull request a main y ejecución manual.

| Job | Motivo | Gate |
|---|---|---|
| Contrato | Schemathesis al inicio, antes de pruebas funcionales; revisar diseño y esquema | Referencia/esquema/configuración, controles y firmas conocidas |
| API | Karate completo funcional y técnico de G4/núcleo | Cantidad, procedencia, defectos conocidos exactos; desconocidos bloquean |
| Web | Gherkin/Cypress completo tres veces, misma fuente y entorno | Sin omisiones, preparación inválida ni flakiness; FAIL conocido conserva resultado |
| Rendimiento | Comprobar integridad/coherencia de los tres experimentos históricos | No convertir datos antiguos en nuevas corridas ni exigir que el producto pase cuando la finalidad es detectar límites |
| Reportería | Construir HTML, historial y matriz aunque suites fallen | Consolidar errores de jobs y gates; publicar antes de devolver rechazo |
| Pages opcional | Publicar sitio navegable si se habilita la opción | Requiere Settings → Pages → GitHub Actions y permisos de despliegue |

Los jobs funcionales posteriores se intentan aunque uno anterior falle para obtener diagnóstico completo. Esto no anula el gate: cualquier job fallido o evidencia ausente bloquea la decisión final. El gate académico distingue PASS, firma conocida admitida, fallo nuevo, intermitencia y preparación incompleta. La excepción no autoriza uso productivo ni rebaja la severidad del defecto.

## Visible al finalizar

El último job de reportería escribe directamente en el Summary de Actions: gates, counts, tres corridas, bloqueos y matriz HU/TC/ejecución. Se ve sin descargar un ZIP. El artefacto contiene además un sitio navegable completo: extraer y abrir `results/final/site/index.html`. Opcionalmente Pages sirve ese sitio; no se afirma una URL desplegada hasta verificar un run real.

## Con imágenes o sin imágenes

En Actions → Run workflow seleccionar `evidence`: `images` captura éxitos y fallos; `none` desactiva screenshots y vídeos. Push/PR usan `none` por defecto. Se conservan resultados, errores y procedencia en ambos modos. Los gráficos de rendimiento son mediciones, no screenshots opcionales, y permanecen disponibles.

La demo IA es separada por su autenticación personal. La opción `performance_demo` ejecuta un perfil breve adicional; el pipeline siempre verifica los experimentos completos documentados, sin volver a lanzar una hora de carga en cada push.

## Revisiones sustituidas

Push y PR comparten el grupo de concurrencia de su rama. Una ejecución nueva puede cancelar la anterior para evitar pruebas duplicadas de la misma revisión. Una corrida cancelada no se presenta como evidencia completa ni aprobada; la demo utiliza un run finalizado del commit publicado.
