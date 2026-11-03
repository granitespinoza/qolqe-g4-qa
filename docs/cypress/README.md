# Modos de ejecución Cypress

La preparación y el recorrido de la entrega se mantienen en la [guía de ejecución](../ejecucion.md). El alcance vigente se describe en la [matriz integrada](../parte2/trazabilidad.md); la [trazabilidad inicial](trazabilidad.md) es un antecedente.

## Modos disponibles

Desde la raíz, usar `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 ACCION`:

| Acción | Equivalente npm | Función |
|---|---|---|
| open | npm run cy:open | Abre el runner; seleccionar spec y cerrar al terminar. |
| smoke | npm run cy:smoke | Ejecuta el alta válida y la persistencia de un contacto. |
| regression | npm run cy:regression | Ejecuta los specs de `Web/cypress/e2e/`. |
| stability | npm run cy:stability | Ejecuta tres regresiones para comparar resultados. |
| report | npm run cy:report | Abre el último reporte headless en Windows. |
| ai-open | npm run cy:ai:open | Demo IA interactiva; requiere acceso a Cypress Cloud. |
| ai | npm run cy:ai | Demo IA headless, sujeta a autenticación y servicio. |
| failure | npm run cy:demo-failure | Expectativa falsa intencional; fuera de regresión y CI. |

## Aislamiento y evidencia

El lanzador administra Qolqe en 8011. No ejecutar dos modos simultáneamente. Los escenarios preparan actores de prueba y usan respuestas reales. Las bases por ejecución se ubican en `.tools/cypress-runs/`; el lanzador intenta retirarlas al cerrar salvo `CY_KEEP_DB=1`.

Cada ejecución headless conserva `execution.json`, resultados y HTML en `reports/cypress/<fecha>-<modo>/`. `latest.json` identifica la última ejecución. El vídeo está desactivado por defecto; se activa con `CY_VIDEO=1`. Capturas y vídeos dependen del modo y de la configuración: comprobar que se generaron antes de anunciarlos.

La demo IA usa `cy.prompt` para acciones; las aserciones de resultado son explícitas. No declarar self-healing demostrado ni una llamada nueva al modelo por cada repetición. Ver [hallazgos históricos](hallazgos.md).

## Automatización

El [workflow principal](../../.github/workflows/pruebas.yml) consolida API, Web y Reportería. El [workflow específico de Cypress](../../.github/workflows/cypress.yml) se conserva como ejecución separada; no reemplaza la entrega integrada. El estado remoto se verifica en Actions para el commit correspondiente.
