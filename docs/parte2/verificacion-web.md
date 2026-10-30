# Pasos 3 y 4 — cobertura y verificación web

Resultado local, generado desde tres ejecuciones reales. No acredita un pipeline de GitHub ni una entrega completa.

Implementados: **54 tests**, **36 grupos de variantes**, **18 CA G4**.

Un grupo puede tener varios tests y un test varias aserciones. Si falla una aserción, las siguientes no se ejecutan; por eso presencia de código no implica aprobación del criterio.

Tres corridas sin fallos crudos: **NO**. Quality Gate: **A**, aprobado: **True**.

| Corrida | Aprobados | Fallidos | Omitidos/pendientes | Reporte local |
|---|---:|---:|---:|---|
| 1 | 45 | 9 | 0 | [HTML](../../reports/cypress/2026-10-30T16-45-13-067Z-regression/html/index.html) |
| 2 | 45 | 9 | 0 | [HTML](../../reports/cypress/2026-10-30T16-48-55-110Z-regression/html/index.html) |
| 3 | 45 | 9 | 0 | [HTML](../../reports/cypress/2026-10-30T16-53-17-738Z-regression/html/index.html) |

Huella común: `05d3d87a0498357dc839a020515f07935a9148937750cce7478ee02818c81a96`.

SUT: `8c7d2f0c939ede7765b7b80b98c10c3905693fda`. Base de datos independiente por corrida (eliminada al terminar para ahorrar disco), navegador `chrome`, reintentos de tests: 0.

Las fuentes aún pueden estar sin commit; el manifiesto registra `worktreeDirty` y hashes SHA-256 por archivo. Esta evidencia no debe atribuirse únicamente al commit HEAD.

[Manifiesto detallado local](../../reports/cypress/stability-2026-10-30T16-45-12-153Z/stability.json) · [Resumen versionable](../../data/parte2-web-verificacion.json). Los reportes y vídeos están ignorados por Git; compartirlos requiere adjuntarlos o publicarlos en el paso de CI.

## Criterios

| Criterio | Tests relacionados | Resultado |
|---|---|---|
| HU-G4-01-CA1 | E2E-G4-101, E2E-G4-102, E2E-G4-103, E2E-G4-104, E2E-G4-105, E2E-G4-106, E2E-G4-107, E2E-G4-108 | Escenario A: fallo conocido |
| HU-G4-02-CA1 | E2E-G4-108, E2E-G4-109, E2E-G4-110 | aprobado en 3 corridas |
| HU-G4-02-CA2 | E2E-G4-111 | aprobado en 3 corridas |
| HU-G4-02-CA3 | E2E-G4-110 | aprobado en 3 corridas |
| HU-G4-03-CA1 | E2E-G4-112, E2E-G4-113, E2E-G4-114, E2E-G4-115, E2E-G4-116 | Escenario A: fallo conocido |
| HU-G4-04-CA1 | E2E-G4-117 | Escenario A: fallo conocido |
| HU-G4-04-CA2 | E2E-G4-118, E2E-G4-119, E2E-G4-120, E2E-G4-121 | aprobado en 3 corridas |
| HU-G4-05-CA1 | E2E-G4-201, E2E-G4-202, E2E-G4-203, E2E-G4-204, E2E-G4-205, E2E-G4-206 | Escenario A: fallo conocido |
| HU-G4-06-CA1 | E2E-G4-301, E2E-G4-302, E2E-G4-303, E2E-G4-304, E2E-G4-305, E2E-G4-306 | aprobado en 3 corridas |
| HU-G4-06-CA2 | E2E-G4-301 | aprobado en 3 corridas |
| HU-G4-07-CA1 | E2E-G4-307 | aprobado en 3 corridas |
| HU-G4-07-CA2 | E2E-G4-308, E2E-G4-309, E2E-G4-310 | aprobado en 3 corridas |
| HU-G4-08-CA1 | E2E-G4-311 | aprobado en 3 corridas |
| HU-G4-08-CA2 | E2E-G4-312, E2E-G4-313 | aprobado en 3 corridas |
| HU-G4-08-CA3 | E2E-G4-311 | aprobado en 3 corridas |
| HU-G4-08-CA4 | E2E-G4-308, E2E-G4-309, E2E-G4-310, E2E-G4-314, E2E-G4-315, E2E-G4-316, E2E-G4-317, E2E-G4-324 | Escenario A: fallo conocido |
| HU-G4-09-CA1 | E2E-G4-314, E2E-G4-315, E2E-G4-316, E2E-G4-317, E2E-G4-318, E2E-G4-319, E2E-G4-320, E2E-G4-322 | aprobado en 3 corridas |
| HU-G4-10-CA1 | E2E-G4-314, E2E-G4-315, E2E-G4-316, E2E-G4-317, E2E-G4-321, E2E-G4-323 | aprobado en 3 corridas |

## Resultados por prueba

| ID | Corrida 1 / 2 / 3 | Archivo |
|---|---|---|
| E2E-G4-101 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-102 | failed / failed / failed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-103 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-104 | failed / failed / failed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-105 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-106 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-107 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-108 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-109 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-110 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-111 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-112 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-113 | failed / failed / failed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-114 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-115 | failed / failed / failed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-116 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-117 | failed / failed / failed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-118 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-119 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-120 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-121 | passed / passed / passed | [contactos-completo.cy.ts](../../Web/cypress/e2e/contactos-completo.cy.ts) |
| E2E-G4-001 | passed / passed / passed | [contactos-happy-path.cy.ts](../../Web/cypress/e2e/contactos-happy-path.cy.ts) |
| E2E-G4-002 | passed / passed / passed | [contactos-validaciones.cy.ts](../../Web/cypress/e2e/contactos-validaciones.cy.ts) |
| E2E-G4-003 | passed / passed / passed | [contactos-validaciones.cy.ts](../../Web/cypress/e2e/contactos-validaciones.cy.ts) |
| E2E-G4-301 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-302 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-303 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-304 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-305 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-306 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-307 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-308 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-309 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-310 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-311 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-312 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-313 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-314 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-315 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-316 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-317 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-318 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-319 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-320 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-321 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-322 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-323 | passed / passed / passed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-324 | failed / failed / failed | [solicitudes-completo.cy.ts](../../Web/cypress/e2e/solicitudes-completo.cy.ts) |
| E2E-G4-201 | failed / failed / failed | [transferencias-contactos.cy.ts](../../Web/cypress/e2e/transferencias-contactos.cy.ts) |
| E2E-G4-202 | failed / failed / failed | [transferencias-contactos.cy.ts](../../Web/cypress/e2e/transferencias-contactos.cy.ts) |
| E2E-G4-203 | passed / passed / passed | [transferencias-contactos.cy.ts](../../Web/cypress/e2e/transferencias-contactos.cy.ts) |
| E2E-G4-204 | passed / passed / passed | [transferencias-contactos.cy.ts](../../Web/cypress/e2e/transferencias-contactos.cy.ts) |
| E2E-G4-205 | passed / passed / passed | [transferencias-contactos.cy.ts](../../Web/cypress/e2e/transferencias-contactos.cy.ts) |
| E2E-G4-206 | failed / failed / failed | [transferencias-contactos.cy.ts](../../Web/cypress/e2e/transferencias-contactos.cy.ts) |

## Fallos observados

- **E2E-G4-102**: AssertionError: expected 422 to equal 201
- **E2E-G4-104**: AssertionError: expected 201 to equal 409
- **E2E-G4-113**: AssertionError: expected 422 to equal 200
- **E2E-G4-115**: AssertionError: expected 200 to equal 409
- **E2E-G4-117**: AssertionError: Timed out retrying after 4000ms: expected '<table>' to contain text '10.00', but the text was '\n        FechaTipoDescripciónCategoríaImporte\n        No hay movimientos en el rango seleccionado\n      '
- **E2E-G4-324**: AssertionError: expected 200 to equal 409
- **E2E-G4-201**: AssertionError: Timed out retrying after 4000ms: expected '<table>' to contain text '0.01', but the text was '\n        FechaTipoDescripciónCategoríaImporte\n        No hay movimientos en el rango seleccionado\n      '
- **E2E-G4-202**: AssertionError: Timed out retrying after 4000ms: expected '<table>' to contain text '500.00', but the text was '\n        FechaTipoDescripciónCategoríaImporte\n        No hay movimientos en el rango seleccionado\n      '
- **E2E-G4-206**: AssertionError: expected 201 to equal 422

## Reproducir

Desde la raíz del repositorio, PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 typecheck
$env:CY_BROWSER = "chrome"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 regression
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 stability
.venv/Scripts/python.exe scripts/build_web_coverage.py
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report
```

El servidor y las bases de pruebas se preparan automáticamente; deja libre el puerto 8011. `stability` ejecuta la regresión tres veces y devuelve código 1 si alguna falla. No editar fuentes durante la secuencia. La demo IA y el fallo didáctico están fuera de la regresión.

[Diagnóstico y justificación de los fallos](diagnostico-web.md).

## Mantenibilidad y límites

- Page Object Model: ContactosPage, SolicitudesPage, TransferenciasPage y LoginPage encapsulan selectores y acciones. Las especificaciones conservan resultados esperados de negocio.
- Se esperan respuestas reales con interceptores sin stubs, elementos visibles y estados DOM. No hay `cy.wait(ms)` ni reintentos de pruebas para forzar aprobaciones.
- Las fixtures crean actores independientes por prueba; solo la disponibilidad de los datos y sesiones de preparación admite sondeos acotados. Las operaciones funcionales y financieras no se reintentan.
- Las fronteras temporales usan el reloj de pruebas del servidor; cada test lo restablece. La suite debe seguir secuencial porque comparte ese reloj.
- El veredicto crudo exige cero fallos. El Quality Gate independiente exige mismas fuentes, suite completa, sin omisiones, sin inestabilidad y únicamente fallos conocidos admitidos para el contexto académico.
- Se mantiene la referencia original sin modificar. Los defectos del producto se conservan como FAIL. La aprobación académica se comunica como Escenario A; nunca como 100% de pruebas aprobadas.
- Pipeline y matriz consolidada implementados. Ver [guía de ejecución](entrega.md) y [política del Quality Gate](quality-gate.md). La ejecución remota debe comprobarse después de publicar los cambios.
