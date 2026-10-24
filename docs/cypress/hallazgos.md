# Hallazgos de implementación y verificación

Fecha de comprobación: 24 de octubre de 2026. Entorno local Windows, Node 24.22.1, Cypress 16.2.0 y Chrome 156. Qolqe fijado en 8c7d2f0c939ede7765b7b80b98c10c3905693fda.

## Verificado

- TypeScript sin errores.
- Smoke: 1 caso aprobado.
- Regresión: 3 casos aprobados (happy path, alias inválido y celular duplicado).
- Happy path ejecutado en smoke y nuevamente en regresión, con datos independientes.
- Fallo didáctico: 1 fallo esperado, por encontrar 1 contacto cuando se exigen 2. Generó captura PNG, video MP4 y reporte HTML. Salida 1 conservada.
- Preparador de Python ejecutado satisfactoriamente en el entorno existente.
- Demo IA aprobada en modo interactivo por el usuario. Evidencia visual aportada: un test verde, POST 201 y comprobaciones de alias, celular y una fila después de recargar. Captura en `evidencias/cypress-ia-aprobada.png`.

Los resultados locales están en `reports/cypress/` y se excluyen de Git. `verificacion-local.json` registra las ejecuciones revisadas sin credenciales. Los resultados no constituyen cobertura total de la HU.

## Dificultades reales

1. Node habitual del equipo era 20.17.0, incompatible con Cypress 16. El lanzador PowerShell selecciona el runtime Node 24 ya disponible, sin cambiar la instalación global.
2. PowerShell 5 elimina ciertas comillas al pasar expresiones a Node. Se simplificó la detección de versión para funcionar en esa consola.
3. Una ejecución exitosa de validaciones avisó `Insufficient frames captured to create video`. Los tres casos pasaron. La captura de video sí funcionó en la demo fallida. Un test verde no garantiza que toda herramienta de evidencia funcionó; hay que revisar los artefactos.
4. El primer intento real de cy.prompt llegó al comando IA, pero falló al descargar su módulo Cloud. Después se completaron el acceso Cloud y el projectId. La instrucción de verificación con {{alias}} requirió aclaración: se reemplazó por el texto explícito Contacto IA. El usuario ejecutó el escenario y aportó una captura con resultado aprobado.

## Límites

- Esta suite comprueba un flujo de Contactos y dos rechazos, no toda Qolqe.
- Cypress Cloud no es necesario para la regresión; cy.prompt sí agrega autenticación, conectividad y cuota.
- Las consultas/aserciones reintentan, pero no garantizan ausencia de flakiness. No se usan retries de tests para ocultar resultados.
- Cypress no es la elección para pruebas de carga, apps móviles nativas o varios navegadores independientes controlados simultáneamente por un test.
- CI está configurado, pero su resultado remoto requiere push y ejecución en GitHub Actions.

Fuentes para límites: https://docs.cypress.io/app/references/trade-offs y https://docs.cypress.io/api/commands/prompt.
