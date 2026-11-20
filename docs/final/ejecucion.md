# Preparación y demo de la entrega final

## Antes de exponer

Usar Node 24 LTS, Python 3.13 y Chrome. Preparar el entorno una vez con el README; no instalar dependencias frente a la audiencia. No modificar archivos durante las tres corridas web. Abrir la presentación, un run real de Actions y su Summary/artefacto, el reporte final y la matriz. La nueva presentación tiene 18 diapositivas de apoyo, con enlaces a detalle.

```powershell
Set-Location "$env:USERPROFILE\qolqe-g4-qa"
.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

Dejar esa terminal abierta. Abrir `http://localhost:8765/apidoc/final/`. El servidor muestra archivos, no ejecuta pruebas.

## Pipeline real

En GitHub → Actions → Entrega final → Run workflow. Elegir `none` o `images`. Ver el commit y el intento, contrato primero y luego API/Web. Preparar un run completado del mismo commit, porque la suite completa tarda y no cabe en 15 minutos. Si se inicia otro en vivo, mostrar su progreso y distinguirlo del run completado; no presentar un run anterior como si acabara de terminar.

## Demo web breve con Gherkin

En otra terminal, desde la raíz:

```powershell
$env:QA_EVIDENCE='images'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report
```

El happy path usa `Web/smoke/contactos.feature`, conecta sus pasos con el escenario existente y valida POST, UI y persistencia. Un smoke no es la regresión de 65 casos ni sus tres repeticiones. Para ver el navegador, usar la acción `open` y seleccionar una feature. Mantener libre el puerto 8011.

## Capacidad de IA

```powershell
$env:CYPRESS_PROJECT_ID='ID_REAL_DEL_PROYECTO_CLOUD'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 ai-open
```

Iniciar sesión personalmente y seleccionar `contactos-ia.cy.ts`. Mostrar instrucciones, acciones generadas y aserciones explícitas. No ejecutar al mismo tiempo que otra suite en 8011. Si no hay sesión o el servicio falla, explicarlo y conservar el resultado; no afirmar que una prueba manual fue ejecutada por IA.

## Demo breve de rendimiento y dashboard

```powershell
$env:K6_WEB_DASHBOARD='true'
$env:K6_WEB_DASHBOARD_OPEN='true'
$env:K6_WEB_DASHBOARD_PORT='5665'
$env:K6_WEB_DASHBOARD_PERIOD='10s'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 demo
```

Abrir `http://127.0.0.1:5665` si no se abre automáticamente. Al acabar la carga y sesiones, cerrar la pestaña para permitir que k6 salga; no interrumpir la conciliación. Esperar a que vuelva PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 open
Remove-Item Env:K6_WEB_DASHBOARD,Env:K6_WEB_DASHBOARD_OPEN,Env:K6_WEB_DASHBOARD_PORT,Env:K6_WEB_DASHBOARD_PERIOD -ErrorAction SilentlyContinue
```

El dashboard muestra métricas HTTP en vivo; no sustituye el análisis de operaciones de negocio ni la integridad monetaria. La demo tiene 5 VUs y no acredita carga completa. No volver a ejecutar carga/campaña/estrés durante la exposición; abrir sus reportes identificados.

## Reporte consolidado y trazabilidad

```powershell
.venv/Scripts/python.exe scripts/final_delivery.py report --evidence none
.venv/Scripts/python.exe scripts/kiwi_local.py sync
.venv/Scripts/python.exe scripts/final_delivery.py report --evidence none
.venv/Scripts/python.exe scripts/final_delivery.py summary
```

Abrir `http://localhost:8765/results/final/`. Esa generación no ejecuta suites y rechazará evidencia ausente o desactualizada. Para las capturas, la suite debe haberse ejecutado con `QA_EVIDENCE=images`; pedir `report --evidence images` no crea imágenes retroactivamente. Kiwi TCMS local se inicia con `scripts/kiwi_local.py start` y recibe las corridas mediante `scripts/kiwi_local.py sync`; preparar certificado y acceso antes de la exposición.

## Cierre de la revisión

Antes de publicar: revisar `git status`, los bloqueos del reporte, el run remoto del commit final y el modo de evidencia. No mover los tags de entregas anteriores. No hay una ejecución remota comprobada hasta que se publique y termine el workflow del commit nuevo.

## Preparación de Kiwi antes de la exposición

Iniciar una vez con `.venv/Scripts/python.exe scripts/kiwi_local.py start`, preparar la confianza del certificado y abrir `https://localhost:8443/plan/1/`. Las credenciales se consultan en `integrations/kiwi/.local/account.json`, ignorado por Git. Mostrar las corridas identificadas por run/commit y abrir un caso con sus variantes. No reinstalar Docker ni repetir migraciones durante los 15 minutos.

## Importar una ejecución de GitHub en Kiwi local

Descargar y extraer el artefacto final en una carpeta independiente, conservando sus rutas. Después importar su `results/final/report.json`:

```powershell
.venv/Scripts/python.exe scripts/kiwi_local.py sync --report RUTA-EXTRAIDA/results/final/report.json
```

No se reemplaza el historial ni se confunde una corrida de Linux con una nueva ejecución local.
