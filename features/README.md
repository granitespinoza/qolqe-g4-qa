# Escenarios E2E ejecutables

`e2e/` contiene los 65 escenarios de regresión y su catálogo HU/TC. `smoke/` contiene el happy path breve. Cypress ejecuta estos archivos mediante Cucumber y `tests/e2e/steps/web.ts`; los escenarios y aserciones no se duplican. API mantiene su Gherkin en `tests/api/features/`.
