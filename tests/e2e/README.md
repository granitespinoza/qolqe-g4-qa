# tests/e2e — pruebas E2E web

Las pruebas E2E de este proyecto son de **Cypress** y se mantienen en [`Web/cypress/`](../../Web/cypress/). Esta carpeta existe para que la ubicación pedida en la consigna sea fácil de encontrar; no duplica el código.

| Qué | Dónde |
|---|---|
| Tests (54) | `Web/cypress/e2e/*.cy.ts` |
| Page Objects (locators y acciones) | `Web/cypress/pages/` |
| Comandos propios y datos de prueba | `Web/cypress/support/` |
| Demos (IA y fallo didáctico), fuera de regresión | `Web/cypress/demos/` |
| Configuración | `cypress.config.ts` |
| Lanzadores | `scripts/cypress.ps1`, `scripts/cypress/run.mjs` |

## Diseño

- **Patrón:** Page Object más comandos personalizados.
- **Localizadores:** atributos `data-testid`.
- **Esperas:** las propias de Cypress (reintentos de consultas y aserciones); no hay esperas fijas.
- **Aislamiento:** usuarios ficticios nuevos por escenario y base SQLite exclusiva en el puerto 8011.
- **Trazabilidad:** cada test lleva etiquetas `@HU-…` y `@TC-…` y aparece en `data/trazabilidad-parte2.csv`.

## Ejecutar

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 setup
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
```

Suite completa con el Quality Gate: `.venv/Scripts/python.exe scripts/ci_run.py web`. Más detalle en [`docs/parte2/mapa-del-repo.md`](../../docs/parte2/mapa-del-repo.md).
