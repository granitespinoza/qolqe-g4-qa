# Preparación y ejecución

Ejecutar desde la raíz del repositorio. Los comandos de esta guía son para Windows/PowerShell. CI tiene su propia preparación Linux en el [workflow](../.github/workflows/pruebas.yml); esta guía no acredita una validación de macOS.

## Preparar una copia nueva

Requisitos: Git, Python compatible con `requirements-lock.txt` (CI configura 3.13), Node.js 24 LTS recomendado, npm, Chrome e internet para instalar dependencias. API utiliza Java 17 y Karate 1.5.2. El preparador API descarga Java si falta.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 setup
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 typecheck
```

Ejecutar cada comando y comprobar su salida antes del siguiente. `bootstrap.ps1` crea `.venv`; el setup web reutiliza ese entorno. No reinstalar en cada ejecución. Cypress Cloud solo es necesario para la demo IA opcional.

## Recorrido breve web

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report
```

El lanzador inicia Qolqe en 8011, ejecuta el alta de un contacto y comprueba persistencia tras recargar. Conserva la evidencia e intenta retirar la base temporal al terminar. `report` abre el último reporte; leer su fecha y alcance.

Para ver el navegador de pruebas:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 open
```

Seleccionar `Web/cypress/e2e/contactos-happy-path.cy.ts`. Cerrar Cypress antes de iniciar otro modo. Ver [modos adicionales](cypress/README.md).

## Seleccionar un caso API

El ejecutor puede administrar una instancia nueva; mantener libre el puerto 8000:

```powershell
.venv/Scripts/python.exe scripts/run_qa.py karate --start-api --tag '@G4-001'
```

Para una HU, sustituir el tag por `@HU-G4-01`. Para contrato técnico usar `@CONTRATO-CONTACTOS`. Una selección no sustituye el manifiesto de la suite completa. El comando imprime el directorio de su reporte.

## Ejecución completa y consolidación

```powershell
.venv/Scripts/python.exe scripts/ci_run.py api
.venv/Scripts/python.exe scripts/ci_run.py web
.venv/Scripts/python.exe scripts/build_web_coverage.py
.venv/Scripts/python.exe scripts/ci_run.py reporting
.venv/Scripts/python.exe scripts/build_delivery.py
```

API ejecuta Karate y Schemathesis; Web realiza tres corridas completas. Revisar cada salida. Si una suite falla, conservar su evidencia y continuar con las demás para diagnosticar; no interpretar una salida fallida como aprobación del conjunto. No iniciar una API manual que compita con los lanzadores.

## Abrir presentación, matriz y reportes

En otra terminal:

```powershell
.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

Abrir [portal local](http://localhost:8765/apidoc/parte2/). El servidor sirve archivos, no inicia pruebas desde el navegador. Los reportes enlazados deben existir en la copia o en el artefacto extraído.

| Evidencia | Ubicación |
|---|---|
| Última suite API | `reports/latest-karate.json` y `reports/latest-schemathesis.json` |
| Última selección Karate | `reports/latest-karate-selection.json` |
| Última ejecución Web | `reports/cypress/latest.json` |
| Reporte consolidado generado | `results/reporte-final.html` |
| Decisión del gate | `reports/gate/resumen.md` |
| Matriz generada | `data/trazabilidad-parte2.csv` |

El gate puede admitir fallos conocidos bajo su política; no significa que todos los tests aprobaron. Si falta evidencia actual, el generador o evaluador puede bloquear la entrega. Consultar [política](parte2/quality-gate.md) y [defectos](parte2/defectos-conocidos.md).

## Problemas de preparación

- Puerto 8000/8011 ocupado: identificar y cerrar la instancia de pruebas anterior antes de continuar. El ejecutor rechaza reutilizar un servidor desconocido.
- Dependencias o navegador ausentes: resolver la preparación y revisar su salida; no atribuir ese error a Qolqe.
- Reporte inexistente: comprobar el manifiesto y su directorio o extraer el artefacto completo de Actions.
- Evidencia de otro código: ejecutar de nuevo; no editar resultados para hacerlos coincidir.
