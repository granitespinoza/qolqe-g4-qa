# Cypress: ejecución reproducible

Granit y Franco. Suite web del módulo Contactos. Leer `trazabilidad.md` para alcance y `arquitectura.md` para diseño. Presentación en `presentacion/cypress/`.

## Requisitos

Git, Node.js 24 LTS (también compatibles 22 y >=26), Python 3.12 recomendado, Chrome e internet para instalar. Cypress está fijado en 16.2.0. El runtime de pruebas puede funcionar sin Cypress Cloud; solamente la demo IA lo necesita.

## Windows

En la raíz del repositorio:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 setup
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 typecheck
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
```

El lanzador usa Node compatible del PATH o el runtime local de Codex si está disponible. No cambia la instalación global. Con Node 24 en PATH se pueden usar directamente `npm ci`, `npm run cy:setup`, `npm run cy:smoke`.

Si Python 3.12 no está en `py`, establece `QA_PYTHON` con la ruta de un Python >=3.11 antes de `setup`. Si ya existe `.venv`, se reutiliza. No hacen falta Karate ni Java para esta suite.

## Modos

| Acción de cypress.ps1 | Comando npm equivalente | Resultado |
|---|---|---|
| open | npm run cy:open | Cypress App. Seleccionar el spec y cerrar la aplicación al terminar. |
| smoke | npm run cy:smoke | Happy path en Chrome headless. |
| regression | npm run cy:regression | Los tres casos de negocio. |
| ai-open | npm run cy:ai:open | Cypress App, solo demo IA, iniciar sesión Cloud. |
| ai | npm run cy:ai | Demo IA headless con autenticación Cloud ya resuelta. |
| failure | npm run cy:demo-failure | Fallo intencional, salida 1 esperada. |
| report | npm run cy:report | Abre el HTML de la última ejecución run en Windows. |

Cada modo inicia y detiene su servidor en 8011. Si el puerto está ocupado, se detiene sin reutilizar servidores ajenos. La aplicación está en http://127.0.0.1:8011 mientras la ejecución siga abierta. No iniciar dos modos simultáneamente. Chrome se puede sustituir con `CY_BROWSER=electron` para regresión, no para la demo IA.

## Datos y aislamiento

Cada escenario registra dos usuarios ficticios distintos. PIN de prueba: 4826. No hay credenciales de producción. Datos separados en `.tools/cypress/`, no se reinicia ninguna base compartida. El directorio puede crecer por registros de prueba; su limpieza manual solo se debe realizar con el servidor detenido y exclusivamente en esa carpeta.

## IA

1. Ejecutar `ai-open`, seleccionar Chrome y completar inicio de sesión en Cypress Cloud.
2. Si Cloud solicita asociar el proyecto, configurar su ID con `$env:CYPRESS_PROJECT_ID='ID_REAL'` y volver a abrir. No versionar claves.
3. Ejecutar `contactos-ia.cy.ts`, mostrar pasos `cy.prompt` y la opción Code del Command Log.
4. La IA completa el formulario. Aserciones convencionales comprueban 201 y persistencia tras recargar.

No requiere simular respuestas. No declarar la IA validada si la cuenta, permisos, conectividad o cuota impiden ejecutarla. El servicio puede reutilizar comandos en caché: una repetición no demuestra necesariamente una nueva llamada al modelo. La demo demuestra generación/ejecución de pasos, no self-healing.

Contingencia externa (identificarla como tal): entregar el HTML de Contactos y el CA a un asistente IA, pedir un test Cypress con selectores presentes y aserciones de persistencia, revisar el código y ejecutarlo en vivo. Un video es respaldo, no reemplaza la IA en vivo.

## Evidencia

`reports/cypress/<fecha>-<modo>/html/index.html`, `execution.json`, capturas y videos. `latest.json` indica la última ejecución. Se conservan videos de specs con intentos fallidos; los demás se eliminan después de grabar. Capturas automáticas y video aplican a `run`, no a `open`. No se suben reportes locales a Git; CI guarda artefactos 7 días. Revisar datos antes de compartir un reporte.

`failure` espera incorrectamente 2 contactos cuando existe 1. Está excluido de regresión y CI. Su salida de error es intencional y no debe presentarse como defecto del producto.

## CI

`.github/workflows/cypress.yml` instala, prepara Qolqe fijado, comprueba TypeScript y ejecuta regresión en Electron sobre Ubuntu. La demo IA no bloquea CI. El resultado remoto solo se conoce después del push; ver Actions.

Fuentes: https://docs.cypress.io/app/guides/screenshots-and-videos · https://docs.cypress.io/api/commands/prompt
