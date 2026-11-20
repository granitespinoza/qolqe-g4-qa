# tests/e2e — pruebas E2E web

Las pruebas E2E de este proyecto son de **Cypress** y se mantienen en [`tests/e2e/`](../../tests/e2e/). Esta es la ubicación ejecutable de Cypress. El Gherkin reside en `features/e2e/` y el smoke en `features/smoke/`.

| Qué | Dónde |
|---|---|
| Escenarios de regresión (65) | `tests/e2e/specs/*.cy.ts` |
| Page Objects (locators y acciones) | `tests/e2e/pages/` |
| Comandos propios y datos de prueba | `tests/e2e/support/` |
| Demos (IA y fallo didáctico), fuera de regresión | `tests/e2e/demos/` |
| Configuración | `cypress.config.ts` |
| Lanzadores | `scripts/cypress.ps1`, `scripts/cypress/run.mjs` |

## Diseño

- **Patrón:** Page Object más comandos personalizados.
- **Localizadores:** atributos `data-testid`.
- **Esperas:** las propias de Cypress (reintentos de consultas y aserciones); no hay esperas fijas.
- **Aislamiento:** usuarios ficticios nuevos por escenario y base SQLite exclusiva en el puerto 8011.
- **Trazabilidad:** cada test lleva etiquetas `@HU-…` y `@TC-…` y aparece en `results/final/trazabilidad.csv`.

## Ejecutar

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 setup
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
```

Suite completa con el Quality Gate: `.venv/Scripts/python.exe scripts/ci_run.py web`. Más detalle en [arquitectura](../../docs/arquitectura.md).
