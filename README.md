# Qolqe Wallet G4 · Entrega final

**Franco · Pruebas y Verificación de Software**

Presento el consolidado de API, web con CI/CD y rendimiento. Evalúo **10 HU de G4 y 9 del núcleo común**, con 51 criterios API, 136 IDs API que producen 187 escenarios/variantes y 65 escenarios web ejecutables en Gherkin. Conservo Qolqe sin modificar, fijado en el commit `8c7d2f0c939ede7765b7b80b98c10c3905693fda`, con datos ficticios y bases aisladas.

## 1. Revisar la entrega sin instalar

| Material | Entrada |
|---|---|
| Informe completo en la raíz | [INFORME_FINAL.md](INFORME_FINAL.md) |
| Diapositivas para descargar | [PDF · 24 páginas](presentacion/Entrega_Final_Qolqe.pdf) |
| Presentación navegable | [HTML · 24 diapositivas](apidoc/final/index.html), servido localmente según la sección 3 |
| Pipeline, resultados y matriz visibles | [GitHub Actions → Entrega final](https://github.com/granitespinoza/qolqe-g4-qa/actions/workflows/pruebas.yml) |
| Procedencia de las cifras de las diapositivas | [Snapshot de la ejecución de referencia](data/presentacion-final-resultados.json) |
| Informe de rendimiento según plantilla | [Informe Word](docs/parte3/Informe_Rendimiento_Qolqe.docx) |
| Resultados completos de rendimiento | [Índice de perfiles](tests/performance/resultados/index.html), disponible en la copia local |
| Versión etiquetada | [Tag final](https://github.com/granitespinoza/qolqe-g4-qa/tree/final) |

Para revisar la reportería, abrir un run **completado** y comprobar su commit e intento. El **Summary** del último job muestra los gates, las tres corridas y la matriz sin descargar un ZIP. En **Artifacts**, descargar `entrega-final-RUN-INTENTO`, extraerlo completo y abrir `results/final/site/index.html`. También puede servirse esa carpeta con un servidor HTTP local. El sitio conserva reportes crudos, matriz, gráficos y, si se eligieron, capturas.

GitHub muestra el código de los archivos HTML; para navegar por ellos hay que descargarlos con sus carpetas o usar el sitio del artefacto. `results/final/` y los reportes crudos son salidas generadas, no enlaces a páginas desplegadas en GitHub. Pages es opcional y no es necesario para revisar el Summary y los artefactos.

## 2. Estructura ejecutable

```text
INFORME_FINAL.md                       Informe consolidado
.github/workflows/pruebas.yml          Pipeline principal
features/e2e/                         65 escenarios Gherkin de regresión y catálogo
features/smoke/                       Happy path breve
tests/api/features/                   Karate funcional y técnico
tests/api/openapi.json                Contrato capturado
tests/api/reportes/                   Entrada y resumen API generados por el job final
tests/e2e/specs/                      Implementación de escenarios Cypress
tests/e2e/steps/                      Enlace entre Gherkin y Cypress
tests/e2e/pages/                      Page Object Model
tests/e2e/support/                    Datos y comandos de preparación
tests/e2e/demos/                      IA y demostraciones separadas
tests/performance/                   k6, escenarios, configuración y soporte Python
tests/performance/resultados/        HTML, CSV de recursos, gráficos e integridad
scripts/                             Lanzadores, gates, reportería y sincronización
integrations/kiwi/                   Docker Compose e integración Kiwi TCMS
docs/final/                          Arquitectura, decisiones y guías de ejecución
apidoc/final/index.html               Presentación HTML
presentacion/Entrega_Final_Qolqe.pdf  Presentación PDF
results/final/                       Consolidado y matriz generados
reports/raw/                         Reportes API crudos generados
reports/cypress/                     Reportes web por corrida generados
```

Los reportes API completos se conservan en `reports/raw/` dentro del artefacto, enlazados desde el consolidado. `tests/api/reportes/` recibe además una entrada y resumen de la ejecución. Los resultados generados se identifican por corrida; no sustituyo evidencias antiguas por un archivo que parezca una nueva ejecución.

## 3. Preparar una copia nueva en Windows

Requisitos: **Python 3.13, Node.js 24 LTS, npm, Git y Chrome**, acceso a Internet para las dependencias. Bootstrap prepara la referencia y las dependencias API; utiliza Java 17 disponible o descarga su runtime cuando es necesario. Docker Desktop con motor Linux se necesita para Kiwi, no para el smoke web.

```powershell
git clone https://github.com/granitespinoza/qolqe-g4-qa.git
Set-Location qolqe-g4-qa
py -3.13 -m venv .venv
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
npm ci --no-audit --no-fund
npx cypress install
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 typecheck
.venv/Scripts/python.exe scripts/final_delivery.py audit
```

Para abrir la presentación y los reportes existentes, dejar esta terminal funcionando:

```powershell
.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

- Presentación: `http://localhost:8765/apidoc/final/`
- Rendimiento: `http://localhost:8765/tests/performance/resultados/`
- Consolidado, después de generarlo o importar su artefacto: `http://localhost:8765/results/final/`

El servidor HTTP sirve archivos; pulsar un enlace de la presentación no ejecuta pruebas. Una copia nueva no contiene `results/final/index.html`: primero hay que generar el consolidado o abrir el sitio completo descargado de Actions.

## 4. Demo web breve

En otra terminal desde la raíz:

```powershell
$env:QA_EVIDENCE = 'images' # cambiar a 'none' para no capturar imágenes
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report
```

El smoke ejecuta `features/smoke/contactos.feature`: prepara actores, inicia sesión, agrega un contacto, comprueba POST 201, los datos en la UI y su persistencia al recargar. El lanzador inicia su servidor y base exclusivos en el puerto 8011. No es necesario levantar manualmente otra instancia para esta demo. El puerto debe estar libre; cerrar una ejecución Cypress anterior antes de iniciar otra.

Para el runner interactivo: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 open`. Seleccionar una feature concreta. El smoke de un caso no sustituye la regresión de 65 ni sus tres repeticiones.

## 5. IA con Cypress Cloud

La demo real y su validación se documentan en [IA](docs/final/ia.md), con [reporte de una ejecución verificada](docs/final/evidencias/ia/reporte.html). Para repetirla se requiere sesión personal de Cypress Cloud y acceso al proyecto configurado:

```powershell
$env:CYPRESS_PROJECT_ID = 'ID_DEL_PROYECTO_CLOUD_CON_ACCESO'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 ai-open
```

Iniciar sesión y seleccionar `contactos-ia.cy.ts`. `cy.prompt` realiza acciones naturales; aserciones independientes verifican POST 201, datos y persistencia. El servicio puede reutilizar código generado. No se afirma que cada pipeline ejecute una nueva llamada a IA. No se guardan credenciales Cloud en Git.

## 6. Demo breve de rendimiento

Preparar k6 y las dependencias una vez, antes de la exposición:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 install
```

Ejecutar la demo con dashboard:

```powershell
$env:K6_WEB_DASHBOARD = 'true'
$env:K6_WEB_DASHBOARD_OPEN = 'true'
$env:K6_WEB_DASHBOARD_PORT = '5665'
$env:K6_WEB_DASHBOARD_PERIOD = '10s'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 demo
```

Abrir `http://127.0.0.1:5665` si no se abre automáticamente. La demo tiene cinco VUs, 15 s de subida, 90 s estables y 15 s de descenso, más finalización de sesiones. Cuando termine la carga, cerrar la pestaña del dashboard para permitir la salida de k6; esperar la conciliación y el regreso del prompt, sin interrumpir el proceso.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 open
Remove-Item Env:K6_WEB_DASHBOARD,Env:K6_WEB_DASHBOARD_OPEN,Env:K6_WEB_DASHBOARD_PORT,Env:K6_WEB_DASHBOARD_PERIOD -ErrorAction SilentlyContinue
```

El dashboard informa métricas HTTP; el reporte añade operaciones de negocio e integridad. La demo no acredita capacidad completa. Los experimentos de carga, campaña y estrés guardados conservan sus fechas e incumplimientos. El modelo y los comandos completos están en [tests/performance/README.md](tests/performance/README.md). Pico abrupto y resistencia de 18 h no fueron ejecutados y su exclusión se justifica; no se atribuyen resultados a esas pruebas.

## 7. Ejecutar las suites completas y generar un reporte nuevo

Ejecutar secuencialmente, sin mezclar suites sobre la misma instancia:

```powershell
$env:QA_EVIDENCE = 'none' # usar 'images' desde el inicio para obtener capturas
.venv/Scripts/python.exe scripts/ci_run.py api
.venv/Scripts/python.exe scripts/ci_run.py web
.venv/Scripts/python.exe scripts/build_web_coverage.py
.venv/Scripts/python.exe scripts/final_delivery.py report --evidence none
.venv/Scripts/python.exe scripts/final_delivery.py summary
.venv/Scripts/python.exe scripts/final_delivery.py gate
```

En ejecución local, `ci_run.py api` ejecuta Schemathesis y Karate; `ci_run.py web` realiza las tres corridas. Con `images`, usar también `report --evidence images`. Seleccionar imágenes al generar el HTML no crea capturas retroactivamente. Reporter/gate rechazan evidencia ausente, incompleta o de otras fuentes. Una suite bloqueada debe investigarse y aun así conservar su diagnóstico; no se cambian expectativas para conseguir verde.

## 8. Pipeline y lectura de los resultados

El workflow [pruebas.yml](.github/workflows/pruebas.yml) se activa por push a `main`/`codex/**`, PR a `main` y ejecución manual:

**Contrato (Schemathesis) → API (Karate) → Web Gherkin ×3 → Coherencia de rendimiento → Reportería y gate final.**

En Actions → Run workflow, `evidence=none` o `images` controla capturas. `performance_demo` añade una ejecución breve, no todos los experimentos largos. `publish_pages` es opcional y requiere configurar Pages. Sin Pages, Summary y artefactos siguen disponibles. No iniciar otra corrida de la misma rama mientras se revisa una: la concurrencia puede cancelar la anterior.

El **Escenario A académico** conserva los FAIL y admite solo firmas conocidas y documentadas en datos aislados. Fallos nuevos, causas distintas, flakiness, omisiones y errores de preparación bloquean. Conocido no significa inocuo; los defectos críticos conservan su severidad y no se certifica producción.

Referencia de las diapositivas: 175 PASS / 12 fallos conocidos entre 187 variantes API; tres corridas web de 55 PASS / 10 conocidos entre 65 casos; 562 interacciones de contrato con 27 señales conocidas. El [snapshot](data/presentacion-final-resultados.json) identifica commit y run. Las señales de contrato no equivalen a defectos únicos ni se suman como casos funcionales. Consultar el run del commit entregado para su resultado vigente.

SonarCloud es una integración externa que no forma parte de este workflow de entrega. Su estado se distingue del resultado de los cinco jobs anteriores.

## 9. Kiwi TCMS e historial

Con Docker iniciado:

```powershell
.venv/Scripts/python.exe -m pip install -r requirements-kiwi.txt
.venv/Scripts/python.exe scripts/kiwi_local.py start
.venv/Scripts/python.exe scripts/kiwi_local.py status
```

La instancia local se abre en `https://localhost:8443/plan/1/` para esta instalación; el lanzador informa el ID. Credenciales propias: `integrations/kiwi/.local/account.json`, ignorado por Git. Preparar la confianza del certificado local y el inicio de sesión antes de exponer, según [gestión de casos](docs/final/gestion-casos.md). No proyectar ni publicar las credenciales.

Después de generar un consolidado, importar con `.venv/Scripts/python.exe scripts/kiwi_local.py sync` y volver a generar el HTML para incorporar la confirmación. Para importar un artefacto de GitHub ya extraído:

```powershell
.venv/Scripts/python.exe scripts/kiwi_local.py sync --report 'RUTA_EXTRAIDA/results/final/report.json'
```

Cada caso conserva versión y cada corrida identidad, commit y estados. Las variantes API quedan agrupadas por caso con detalle en comentarios y matriz; un FAIL conocido permanece FAILED. La sincronización verifica los estados por lectura posterior. Los volúmenes conservan el historial; `scripts/kiwi_local.py stop` detiene sin eliminarlo.

Un runner hospedado de GitHub no puede conectarse al localhost de esta laptop. El pipeline exporta historial y payload. La sincronización remota requiere instancia accesible y secretos configurados; `not_configured` no afirma una importación real. La instancia local permite demostrar el uso efectivo de Kiwi.

## 10. Evidencias por criterio docente

| Criterio | Evidencia |
|---|---|
| Arquitectura y herramientas | [Arquitectura y alternativas](docs/final/arquitectura-y-patrones.md) |
| API funcional y técnica | [Features API](tests/api/features/) · [análisis del alcance](docs/final/requerimientos-y-umbrales.md) |
| Web Gherkin y núcleo | [Features E2E](features/e2e/) · [implementación](tests/e2e/specs/) |
| Patrón y escalabilidad | [POM y comparación](docs/final/arquitectura-y-patrones.md) · [Page Objects](tests/e2e/pages/) |
| Contrato inicial y gates | [Workflow](.github/workflows/pruebas.yml) · [política](data/quality-policy.json) |
| Reportería seleccionable | [Publicación y modos](docs/final/pipeline.md) · Summary/artefacto de Actions |
| Múltiples ejecuciones y gestión | [Kiwi e identidad de casos](docs/final/gestion-casos.md) · matriz por ejecución |
| IA y validación | [Capacidad IA](docs/final/ia.md) · [implementación](tests/e2e/demos/contactos-ia.cy.ts) |
| Exposición y demo | [Presentación](apidoc/final/index.html) · [preparación y comandos](docs/final/ejecucion.md) |

La exposición es una condición de evaluación que no sustituye un pipeline aprobado. Las limitaciones de resistencia, campaña y entorno local están documentadas. Conservo las entregas anteriores como antecedentes en `docs/`, `apidoc/parte2/` y `apidoc/parte3/`, con sus fechas y resultados; no se confunden con una corrida nueva.
