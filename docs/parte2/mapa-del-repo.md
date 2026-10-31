# Mapa del repositorio — Entrega 2

Qué hay y dónde está, siguiendo el orden de la exposición y de la rúbrica. Qolqe original no se modifica: se clona fijado en el commit `8c7d2f0` y se prueba tal cual.

## De requisito a reporte

```
Requisitos (referencias/qolqe-wallet/docs/requisitos.md)  +  Contrato (API/openapi.json)
        │ 10 HU de G4 · 18 criterios de aceptación (CA)
        ▼
Casos de prueba (TC) ── API: Karate + Schemathesis ── Web: Cypress
        │
        ▼
Matriz HU → CA → TC → resultado (data/trazabilidad-parte2.csv)
        │
        ▼
Quality Gate (Escenario A) → CI (pruebas.yml) → reportes publicados
```

## Dónde está cada cosa

| Quiero ver… | Ruta |
|---|---|
| Pruebas de API (Karate), una `.feature` por HU | `API/features/` y contrato en `API/openapi.json` |
| Pruebas web (Cypress + TypeScript) | `Web/cypress/e2e/` (tests), `pages/` (Page Objects), `support/` (comandos y datos de prueba) |
| Demos separadas de la regresión (IA y fallo didáctico) | `Web/cypress/demos/` |
| Exploración del contrato (Schemathesis) | `scripts/run_qa.py schemathesis`, `scripts/schemathesis_context.py` |
| Pipeline de CI | `.github/workflows/pruebas.yml` (API → Web → Reportería) |
| Política del Quality Gate | `docs/parte2/quality-gate.md` y `data/quality-policy.json` |
| Trazabilidad HU → caso → ejecución | `data/trazabilidad-parte2.csv`, `docs/parte2/trazabilidad.md` |
| Defectos y riesgos | `docs/parte2/defectos-conocidos.md` |
| Cobertura web por criterio | `docs/parte2/verificacion-web.md` |
| Presentación web y matriz navegable | `apidoc/parte2/index.html` |
| Informe | `docs/informe.md` |
| Guía de ensayo y publicación | `docs/parte2/entrega.md` |

Los E2E de la consigna (`tests/e2e/`) viven en `Web/cypress/`; ver [`tests/e2e/README.md`](../../tests/e2e/README.md).

## Cifras de la evidencia local

| Suite | Resultado |
|---|---|
| Web (Cypress) | 54 tests, 36 grupos de variantes, 18 CA. Tres corridas: 45 aprobados y 9 fallos conocidos en cada una, sin intermitencia |
| API (Karate) | 130 TC únicos; 181 ejecuciones por los Scenario Outline: 169 aprobados y 12 fallos conocidos |
| Contrato (Schemathesis) | 562 interacciones, 27 ocurrencias revisadas, 9 controles con contexto real exitosos |

El Quality Gate aprueba por **Escenario A**: solo pasan firmas conocidas y documentadas, en un entorno académico aislado. No equivale a 54 pruebas aprobadas ni certifica la aplicación para producción.

## Comandos

Desde la raíz, con el entorno preparado (`scripts/bootstrap.ps1` y Node 24 LTS):

```powershell
.venv/Scripts/python.exe scripts/ci_run.py api
.venv/Scripts/python.exe scripts/ci_run.py web
.venv/Scripts/python.exe scripts/build_web_coverage.py
.venv/Scripts/python.exe scripts/ci_run.py reporting
.venv/Scripts/python.exe scripts/build_delivery.py
```

Cypress interactivo: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 open`.

## Glosario mínimo

- **HU / CA:** historia de usuario y su criterio de aceptación.
- **TC:** *test case*, caso de prueba. Aparece en etiquetas como `@TC-E2E-G4-001`.
- **Smoke / regresión:** prueba mínima del camino principal / conjunto que detecta que un cambio rompió algo.
- **Firma conocida:** fallo documentado con su esperado y observado exactos; el gate solo admite estas.

Los gráficos del README se generan con `python scripts/build_graphics.py` (sin dependencias) y se guardan en `docs/parte2/img/`.
