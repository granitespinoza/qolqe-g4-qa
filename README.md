# Qolqe G4 · Pruebas de API, Web y rendimiento

## Entrega final consolidada

[Estado de verificación local y pendientes](docs/final/verificacion.md). La verificación local completó las tres corridas web y la importación real en Kiwi; cada revisión publicada conserva su propia validación en Actions.

Corregimos Gherkin web ejecutable, núcleo común, contrato al inicio del workflow, reportería visible en Actions, selección de capturas e historial por ejecución. Conservamos los resultados reales y los defectos del producto.

- [Presentación final](apidoc/final/index.html) · [Reporte actual](results/final/index.html) (generado localmente o en el artefacto).
- [Arquitectura y comparación de patrones](docs/final/arquitectura-y-patrones.md).
- [Requerimientos, umbrales y coherencia](docs/final/requerimientos-y-umbrales.md).
- [Jobs y reportería con/sin imágenes](docs/final/pipeline.md).
- [Gestión de casos y preparación de Kiwi TCMS](docs/final/gestion-casos.md) · [Capacidad de IA](docs/final/ia.md).
- Gherkin: `Web/features/`; pasos: `Web/cypress/steps/`; cuerpos de escenarios: `Web/cypress/e2e/`; POM: `Web/cypress/pages/`.

### Preparación y reproducción en Windows

Necesitamos Python 3.13, Node 24 LTS, Git, Chrome y Java 17. Con una copia nueva:

```powershell
git clone https://github.com/granitespinoza/qolqe-g4-qa.git
Set-Location qolqe-g4-qa
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/bootstrap.ps1
npm ci --no-audit --no-fund
npx cypress install
npm run cy:typecheck
.venv/Scripts/python.exe scripts/final_delivery.py audit
```

Para una demo breve, sin ejecutar las tres suites completas:

```powershell
$env:QA_EVIDENCE = 'images' # o 'none'
npm run cy:smoke
npm run cy:report
```

Para una verificación completa y reporte nuevo:

```powershell
.venv/Scripts/python.exe scripts/ci_run.py api
.venv/Scripts/python.exe scripts/ci_run.py web
.venv/Scripts/python.exe scripts/build_web_coverage.py
.venv/Scripts/python.exe scripts/final_delivery.py report --evidence none
.venv/Scripts/python.exe -m pip install -r requirements-kiwi.txt
.venv/Scripts/python.exe scripts/kiwi_local.py start
.venv/Scripts/python.exe scripts/kiwi_local.py sync
.venv/Scripts/python.exe scripts/final_delivery.py report --evidence none
.venv/Scripts/python.exe scripts/final_delivery.py summary
.venv/Scripts/python.exe scripts/final_delivery.py gate
```

No ejecutamos suites simultáneas sobre la misma instancia. El gate conserva fallos de producto; un rechazo no se corrige cambiando expectativas para ocultarlos. Ejecutamos reportería después de suites fallidas para conservar el diagnóstico. La presentación no inicia pruebas al pulsar enlaces.

```powershell
.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

Abrimos `http://localhost:8765/apidoc/final/` y `http://localhost:8765/results/final/`. En GitHub: Actions → **Entrega final - Contrato, API, Web y reportes** → Run workflow; elegir `none` o `images`. El Summary muestra resultados directamente; el artefacto incluye el sitio completo con rutas conservadas. Pages es opcional y requiere configuración del repositorio.

Kiwi TCMS dispone de un lanzador local con TLS, datos persistentes y sincronización por corrida. Para iniciarlo: `.venv/Scripts/python.exe -m pip install -r requirements-kiwi.txt` y `.venv/Scripts/python.exe scripts/kiwi_local.py start`. Después de generar el reporte usamos `.venv/Scripts/python.exe scripts/kiwi_local.py sync`. Las credenciales locales están ignoradas por Git; ver [gestión de casos](docs/final/gestion-casos.md). En Actions, `not_configured` indica que falta una instancia accesible desde el runner. La IA usa cy.prompt y requiere sesión personal Cypress Cloud. Los experimentos de rendimiento conservan sus fechas e incumplimientos y no se presentan como recién ejecutados por CI.



Granit Espinoza y Franco · Pruebas y Verificación de Software.

En este repositorio reunimos las pruebas de API (Karate y Schemathesis), los recorridos web (Cypress) y las pruebas de rendimiento (k6) de Qolqe Wallet. Conservamos la aplicación original y ejecutamos las pruebas con datos sintéticos y bases independientes.

## Parte 3 · Pruebas de rendimiento

Elegimos **k6 como único generador de carga**: definimos los escenarios HTTP en JavaScript, un lenguaje conocido por el equipo, y mantenemos las etapas, etiquetas y umbrales bajo control de versiones. Evaluamos Locust y JMeter como alternativas; no los utilizamos en las ejecuciones. Con Python preparamos los datos, registramos recursos mediante psutil y conciliamos las operaciones monetarias.

### Material de entrega

| Material | Ubicación |
|---|---|
| Presentación navegable | [apidoc/parte3/index.html](apidoc/parte3/index.html) |
| Informe Word según plantilla | [docs/parte3/Informe_Rendimiento_Qolqe.docx](docs/parte3/Informe_Rendimiento_Qolqe.docx) |
| Índice de reportes de rendimiento | [tests/performance/resultados/index.html](tests/performance/resultados/index.html) |
| Modelo, umbrales y escenarios | [tests/performance/configuracion/modelo.json](tests/performance/configuracion/modelo.json) |
| Operaciones HTTP ejecutadas por k6 | [tests/performance/escenarios/carga.js](tests/performance/escenarios/carga.js) |
| Justificación detallada y evidencias | [tests/performance/README.md](tests/performance/README.md) |

Incluimos el HTML y el Word en GitHub. Para visualizar la presentación con sus enlaces y gráficos descargamos o clonamos el repositorio completo; la vista de archivos de GitHub muestra el código HTML. Para entregar diapositivas como archivo, abrimos la presentación, usamos **Ctrl+P → Guardar como PDF** y seleccionamos todas las páginas. El estilo de impresión incluye las diapositivas completas. Adjuntamos ese PDF y el Word en la plataforma de entrega, junto con el enlace al repositorio.

### Organización

```text
scripts/performance.ps1                  Lanzador de instalación y ejecución
apidoc/parte3/index.html                  Presentación HTML
docs/parte3/Informe_Rendimiento_Qolqe.docx Informe de resultados
tests/performance/
   README.md                             Modelo y decisiones experimentales
   requirements.txt                      Dependencias de rendimiento
   configuracion/modelo.json             VUs, etapas, pausas y ponderaciones
   escenarios/carga.js                    Sesión y operaciones HTTP de k6
   scripts/performance.py                Preparación, servidor, monitor y conciliación
   scripts/server.py                     Inicio de Qolqe para cada corrida
   scripts/generar_reportes.py            Reportes HTML y gráficos
   scripts/crear_informe.py               Generación del informe Word
   scripts/crear_presentacion.py          Generación de la presentación
   resultados/index.html                 Índice de evidencias
   resultados/<run_id>/                  Archivos de una ejecución concreta
referencias/qolqe-wallet/                 Aplicación original descargada al preparar
.venv/                                   Entorno Python local, no versionado
.tools/performance/                      k6 y archivos temporales locales
```

### Preparación desde cero en otra computadora

Documentamos y validamos este procedimiento para **Windows x64 con PowerShell y Python 3.13**. Necesitamos Git y Python instalados, acceso a internet durante la instalación y espacio para dependencias y resultados. Podemos usar una sola computadora: Qolqe y k6 corren localmente. No necesitamos Cypress, Node, Java, Docker, cuentas de Grafana ni credenciales externas para esta demo de rendimiento. El lanzador `.ps1` y la descarga de k6 están preparados para Windows; no presentamos estos comandos como una instalación validada para macOS o Linux.

Primero comprobamos los requisitos:

```powershell
git --version
py -3.13 --version
```

En una computadora sin una copia del repositorio:

```powershell
Set-Location $env:USERPROFILE
git clone --branch main https://github.com/granitespinoza/qolqe-g4-qa.git
Set-Location qolqe-g4-qa
```

Si ya tenemos la copia, entramos en su carpeta, revisamos los cambios locales y actualizamos `main`. No borramos archivos para resolver una actualización:

```powershell
Set-Location "$env:USERPROFILE\qolqe-g4-qa"
git status
git switch main
git pull --ff-only origin main
```

Desde la raíz del repositorio, en una instalación nueva, creamos el entorno e instalamos las dependencias:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Descargamos Qolqe en la revisión original utilizada en los experimentos. Ejecutamos el `clone` únicamente si aún no existe `referencias/qolqe-wallet`:

```powershell
git clone https://github.com/cjudihtroj/qolqe-wallet.git referencias/qolqe-wallet
git -C referencias/qolqe-wallet checkout 8c7d2f0c939ede7765b7b80b98c10c3905693fda
```

Instalamos las dependencias de rendimiento y k6 2.4.0:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 install
.\.venv\Scripts\python.exe -m pip check
git -C referencias/qolqe-wallet rev-parse HEAD
git -C referencias/qolqe-wallet status --short
```

Comprobamos que `pip check` no indique incompatibilidades, que la revisión sea `8c7d2f0c939ede7765b7b80b98c10c3905693fda` y que el último comando no muestre cambios en Qolqe. Si un comando falla, resolvemos su mensaje antes de continuar. La instalación se hace una vez; no la repetimos antes de cada demo. El lanzador usa directamente `.venv`, sin activar el entorno ni cambiar permanentemente la política de PowerShell.

### Abrir la presentación y los reportes

En una primera terminal, desde la raíz, iniciamos el servidor de archivos y dejamos esa ventana abierta:

```powershell
.\.venv\Scripts\python.exe -m http.server 8765 --bind 127.0.0.1
```

En el navegador abrimos:

- [Presentación local](http://localhost:8765/apidoc/parte3/)
- [Índice de reportes](http://localhost:8765/tests/performance/resultados/)

Este servidor permite consultar archivos; no inicia pruebas. Los enlaces locales funcionan mientras esté abierto. Los reportes versionados ya se pueden consultar sin repetir los experimentos. Para detener únicamente este servidor usamos `Ctrl+C` en su terminal.

### Ejecutar la demo en vivo

En una **segunda terminal**, entramos en la misma carpeta del repositorio y ejecutamos:

```powershell
Set-Location "$env:USERPROFILE\qolqe-g4-qa"
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 demo
```

Si clonamos en otra ubicación, usamos esa carpeta en `Set-Location`. Mantenemos libre el puerto **8021** y ejecutamos un solo perfil a la vez. El lanzador prepara datos exclusivos, inicia Qolqe, ejecuta k6, registra CPU/memoria y concilia saldos y movimientos; no iniciamos Qolqe manualmente.

La demo sube a **5 VUs en 15 s**, mantiene ese nivel **90 s** y desciende en **15 s**. Esos 120 segundos no incluyen preparación, generación de reportes ni la finalización de sesiones, que puede prolongarse. Conservamos pausas de 10–25 s: las pausas sin mensajes en la terminal forman parte del modelo. Esperamos a que termine y vuelva el indicador de PowerShell.

Durante la ejecución mostramos una línea como `VU 1 | movimientos | HTTP [200] | ... ms | correcto=True`. El VU identifica al usuario virtual, HTTP muestra la respuesta recibida, los milisegundos expresan la duración de la operación y `correcto` indica si coincide con el estado HTTP esperado. Esa línea no sustituye la conciliación monetaria posterior.

Al terminar abrimos el índice:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 open
```

Seleccionamos **demo** y comprobamos su fecha y `run_id`. También podemos abrir directamente el reporte de la última demo:

```powershell
$demoActual = Get-Content tests/performance/resultados/latest-demo.json -Raw | ConvertFrom-Json
Start-Process (Join-Path (Get-Location).Path (Join-Path $demoActual.dir 'reporte.html'))
```

### Leer los resultados

Distinguimos tres estados:

- **Ejecución válida:** contamos con datos y recursos medidos, ejecución completa y controles del generador. No significa que el producto cumpla todos los umbrales.
- **Cumplimiento del perfil:** compara los resultados con los criterios del experimento. En referencia/demo se muestra `None` porque no emiten una decisión de aceptación de carga completa.
- **Integridad monetaria:** verifica registros, movimientos y saldos; esperamos `True` y una lista `issues` vacía. Un timeout puede haber dejado una operación persistida y requiere conciliación; no reintentamos escrituras automáticamente.

Revisamos las ventanas estables y la tabla **Resultados por operación**. El p95 es el tiempo en el que finaliza el 95% de las muestras: lo comparamos con **800 ms para consultas/login** y **1500 ms para operaciones monetarias**. El throughput cuenta operaciones de negocio correctas por segundo, no todas las peticiones HTTP. Los gráficos temporales usan intervalos de 15 s; las zonas sombreadas señalan ventanas estables. Las curvas agregadas de consultas no sustituyen el p95 de cada operación. El gráfico de errores temporales incluye login, mientras las tablas separan sus errores de los de negocio.

La demo breve muestra el procedimiento, no sustituye carga, campaña ni estrés. En nuestras ejecuciones completas la carga llegó a 5.47 operaciones correctas/s, pero movimientos obtuvo p95 de 914.80 ms y superó los 800 ms. La campaña conservó integridad monetaria. En estrés observamos degradación y fallos del servicio en niveles altos; conservamos los incumplimientos en los reportes.

### Repetir los experimentos completos

Desde la raíz ejecutamos **un comando por vez**, después de que termine el anterior:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 referencia
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 carga
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 campana
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 estres
```

Carga y campaña programan 16 minutos cada una, más preparación y cierre de sesiones. Estrés programa 22 minutos, más preparación y cierre. La acción `all` ejecuta referencia y los tres perfiles completos; no la utilizamos como demo breve. Cada corrida nueva conserva su propia carpeta y actualiza el puntero `latest-<perfil>.json`. Otra computadora producirá mediciones distintas; no esperamos que repita exactamente los valores del informe.

Para regenerar los reportes a partir de diarios y CSV existentes, sin producir carga:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 report
```

Esta acción actualiza reportes y el resumen integrado; no reemplaza por sí sola el informe Word ni la presentación de los experimentos documentados. Los incumplimientos de SLA permanecen visibles. La salida del lanzador no se interpreta por sí sola como aprobación del SLA: revisamos el reporte y la integridad.

### Archivos de cada reporte

Dentro de `tests/performance/resultados/<run_id>/` conservamos:

| Archivo | Evidencia |
|---|---|
| `reporte.html` | Tablas, gráficos y resultado de esa corrida |
| `graficos/evolucion.png`, `graficos/p95-operacion.png` | Evolución temporal y comparación por operación |
| `recursos.csv` | CPU y memoria por segundo de Qolqe y k6 |
| `integridad.json`, `saldos.csv`, `operaciones_monetarias.json` | Conciliación y posibles anomalías |
| `operaciones.jsonl` | Operaciones medidas y respuestas |
| `procedencia.json`, `configuracion.json`, `datos.json` | Entorno, versión, parámetros y datos sintéticos |
| `k6-summary.json`, `k6.log`, `servidor.log` | Salida nativa y registros de diagnóstico |

Si el puerto 8021 está ocupado, detenemos la instancia anterior que iniciamos antes de repetir. Si falta `.venv`, preparamos Python; si falta k6, repetimos `install` y revisamos su salida. Si falta un reporte, comprobamos el directorio indicado por la ejecución y sus registros. No cambiamos el producto ni borramos resultados para convertir un incumplimiento en aprobación.

## Partes 1 y 2 · API y Web

## Revisar la entrega

| Necesito… | Entrada |
|---|---|
| Entender componentes y recorrido | [Arquitectura](docs/arquitectura.md) |
| Preparar el entorno y ejecutar | [Guía de ejecución](docs/ejecucion.md) |
| Seguir el recorrido por clics y abrir matriz y reportes | [Portal de la entrega](apidoc/parte2/index.html) |
| Ver alcance y trazabilidad | [Alcance](docs/parte2/alcance-y-matriz.md) · [Matriz](docs/parte2/trazabilidad.md) |
| Ver pruebas y datos web | [API](API/README.md) · [Web](Web/README.md) · [Datos preparados](Web/cypress/support/fixtures.ts) |
| Revisar automatización y criterios | [Pipeline](docs/parte2/pipeline.md) · [Política del gate](docs/parte2/quality-gate.md) |
| Investigar diferencias | [Defectos conocidos](docs/parte2/defectos-conocidos.md) · [Revisión del contrato](docs/revision-contrato.md) |
| Encontrar sustento adicional | [Índice técnico](docs/README.md) |
| Comprobar materiales y acceso | [Lista de entrega](docs/parte2/entrega.md) · [PowerPoint](presentacion/Entrega2-Qolqe-Cypress.pptx) |

## Ejecutar un recorrido breve

En Windows con el entorno preparado, desde la raíz:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report
```

El lanzador administra su servidor en el puerto 8011. Esta prueba breve no sustituye la regresión completa. Para una instalación nueva, seguir primero la [guía de ejecución](docs/ejecucion.md).

## Interpretar los resultados

- Un test fallido conserva su resultado. El Quality Gate aplica una política distinta y puede admitir firmas conocidas bajo el Escenario A documentado; su aceptación académica debe contrastarse con la consigna.
- El HTML y la documentación versionados contienen evidencia de ejecuciones identificadas. No acreditan una ejecución nueva del código actual. Los reportes crudos no están incluidos en esta copia: recuperar el artefacto correspondiente o generar una nueva ejecución.
- Verificar commit, intento y artefactos en [GitHub Actions](https://github.com/granitespinoza/qolqe-g4-qa/actions) antes de declarar comprobada una entrega remota.
- Schemathesis produce señales que requieren revisión; no se cuentan automáticamente como defectos únicos ni como criterios funcionales cubiertos.

## Referencia

Aplicación: [Qolqe Wallet](https://github.com/cjudihtroj/qolqe-wallet), revisión `8c7d2f0c939ede7765b7b80b98c10c3905693fda`. Los ejecutores verifican la referencia y usan datos de prueba. No se realizan operaciones bancarias reales.

La preparación está documentada para Windows; CI configura Linux. La equivalencia de entornos se verifica con sus ejecuciones. El alcance y los límites se mantienen en los documentos enlazados, sin prometer cobertura total.
