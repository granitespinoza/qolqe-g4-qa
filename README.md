# Qolqe G4 · Contactos y solicitudes de dinero

**Granit y Franco · CS5383 — Pruebas y Verificación de Software**

Trabajo de QA asistido con IA: decisiones justificadas, pruebas reproducibles y evidencia real. La aplicación original se conserva sin modificaciones.

## Recorrido para la docente
0. [Levantar y probar paso a paso](docs/levantar-y-probar.md): API, HTML, selección por HU/caso y ejecución completa.
1. [Informe](docs/informe.md).
2. [Decisiones y alternativas](docs/decisiones.md).
3. [Diseño por historia](docs/diseno-pruebas.md) y [pendientes por criterio](docs/cobertura.md).
4. [Defectos reproducidos](docs/defectos.md).
5. [Documentación HTML](apidoc/index.html): endpoints, búsqueda, escenarios y resultados.
6. Presentación principal en el HTML; [PPT de respaldo](presentacion/G4-contactos.pptx).
7. [Estado verificado del pipeline](docs/ci.md).
8. [Evaluación de usabilidad propuesta](docs/usabilidad.md): complemento para la Parte 2.

## Preparar en Windows
Requisitos: Git y Python 3.12. Java 17 se descarga localmente si falta.
```powershell
./scripts/bootstrap.ps1
```
Terminal 1:
```powershell
./.venv/Scripts/python.exe scripts/serve_api.py
```
Terminal 2:
```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate
./.venv/Scripts/python.exe scripts/run_qa.py schemathesis
./.venv/Scripts/python.exe scripts/build_docs.py
```
Para abrir el portal con sus documentos y evidencias:
```powershell
./.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```
Visitar http://localhost:8765/apidoc/. También abre `apidoc/index.html` directamente: los datos están incorporados y no dependen de un CDN.

## Reproducir un caso
El lanzador localiza Java y configura el intérprete de los auxiliares:
```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@G4-004'
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@HU-G4-01'
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@CONTRATO-CONTACTOS'
```
Los tags se escriben entre comillas en PowerShell. Cada selección conserva un reporte independiente y no reemplaza el manifiesto de la suite completa.
Karate devuelve salida no cero cuando fallan pruebas. No se desactivan los casos que detectan defectos.

## Referencia y alcance
Fuente: https://github.com/cjudihtroj/qolqe-wallet
Commit: `8c7d2f0c939ede7765b7b80b98c10c3905693fda`.
La carpeta `referencias/` se clona con bootstrap, está ignorada y no forma un repositorio embebido en nuestro historial.
Restful Booker se usa como referencia didáctica; no se incorporaron sus reglas o código a Qolqe.
API: http://localhost:8000/docs · OpenAPI: http://localhost:8000/openapi.json.

## Evidencias y límites
`reports/raw/` contiene reportes locales completos; puede incluir tokens de prueba y no se versiona. `evidencias/` contiene registros HTML con tokens ocultos. GitHub Actions conserva reportes de prueba como artefactos privados por 7 días.
La suite es secuencial por el reloj compartido. No se declara cobertura total mientras existan pendientes en `docs/cobertura.md`. No se crea `parte-1` hasta completar y revisar la entrega.
Cada ejecución nueva conserva un directorio propio y `reports/latest-karate.json`, con commit, huellas de fuentes e inicio/fin. La documentación rechaza resultados de otro diseño y usa el OpenAPI capturado en esa ejecución. `--start-api` rechaza un puerto ocupado para evitar probar otra instancia por accidente.

## Sustentación en vivo (última indicación de la docente)
Explicar una HU con sus CA y diseño; ejecutar toda la automatización; revisar el reporte; defender otra HU por tag. Ensayar 10 minutos y reservar 5 de preguntas, cerrando con conclusiones. Las capturas son archivo de estudio.

Schemathesis dispone de [peticiones y checks detallados](reports/schemathesis-detallado.html), con filtros basados en metadatos y credenciales ocultas. Los casos CT explícitos y la matriz complementan las condiciones no demostradas por la exploración. El detalle se genera al ejecutar Schemathesis; también puede reconstruirse desde su evidencia local con `scripts/build_schemathesis_report.py`.

La preparación de usuarios, contactos y sesiones comprueba disponibilidad mediante sondeos acotados y registrados. No se reintentan operaciones financieras ni se cambian sus aserciones. [Incidencia y comparación de ejecuciones](docs/incidencia-consistencia.md).
