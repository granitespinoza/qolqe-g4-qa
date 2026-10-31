# Entrega 2 — guía final de ensayo y publicación

La implementación local está verificada con **Quality Gate Escenario A aprobado**. Qolqe permanece intacto. Los FAIL conocidos conservan sus evidencias. Antes de entregar, publicar los cambios, integrarlos a `main` y comprobar un run real del workflow actualizado; la evidencia local no sustituye esa demostración.

## Materiales

- Canvas: `presentacion/Entrega2-Qolqe-Cypress.pptx`, 13 diapositivas, notas para 15 minutos y última diapositiva **Anexo / Referencias**.
- Presentación web y matriz: `apidoc/parte2/index.html`.
- Reporte final consolidado: `results/reporte-final.html`; XML crudos consolidados en `results/api-results.xml` y `results/web-results.xml`.
- Matriz en CSV: `data/trazabilidad-parte2.csv`; JSON con variantes y procedencia: `data/trazabilidad-parte2.json`.
- Defectos y riesgos: `docs/parte2/defectos-conocidos.md`.
- Política: `docs/parte2/quality-gate.md` y `data/quality-policy.json`.
- Comandos para Bloc de notas: `docs/parte2/comandos-demo.txt`.

La matriz contiene 130 TC API y 54 TC web únicos. Los Scenario Outline de API producen 181 ejecuciones. Un TC puede aparecer en varios criterios; no contar las filas de matriz como tests independientes.

## Ensayo rápido sin regenerar todas las suites

Terminal 1:

```powershell
Set-Location 'C:\Users\Franco\qolqe-g4-qa'
.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

Dejar abierta y visitar `http://localhost:8765/apidoc/parte2/#presentacion`. Si ese servidor ya está activo, utilizarlo.

Terminal 2:

```powershell
Set-Location 'C:\Users\Franco\qolqe-g4-qa'
$env:CY_VIDEO = '0'
$env:CY_KEEP_DB = '0'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 open
```

En Cypress: E2E → Chrome → `Web/cypress/e2e/contactos-happy-path.cy.ts`. Mostrar preparación por API, login UI, alta UI, POST 201 y persistencia tras recargar. Luego, si se desea enseñar un defecto, abrir `contactos-completo.cy.ts` y revisar `E2E-G4-102`, identificado como D-01. Ese archivo ejecuta sus 21 casos; no confundirlo con un único caso seleccionado.

Cerrar Cypress antes de otro modo. Alternativa breve sin runner visual:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 smoke
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report
```

Para explicar el gate a partir de la última secuencia completa ya verificada:

```powershell
.venv/Scripts/python.exe scripts/quality_gate.py web
.venv/Scripts/python.exe scripts/ci_run.py reporting
Get-Content reports/gate/resumen.md
```

Este gate lee las últimas tres corridas completas, no la ejecución interactiva que acaba de abrirse. Decirlo expresamente. Para evidencia nueva ejecutar la secuencia del apartado siguiente o disparar el workflow remoto.

## Ejecución completa nueva

No es necesario reinstalar dependencias en cada ensayo. Para una copia nueva, seguir la instalación del README. Con las dependencias instaladas:

```powershell
Set-Location 'C:\Users\Franco\qolqe-g4-qa'
.venv/Scripts/python.exe -m pip check
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 typecheck
.venv/Scripts/python.exe -m unittest discover -s tests -p test_quality_gate.py
$env:CY_BROWSER = 'chrome'
$env:CY_VIDEO = '0'
$env:CY_KEEP_DB = '0'
.venv/Scripts/python.exe scripts/ci_run.py api
.venv/Scripts/python.exe scripts/ci_run.py web
.venv/Scripts/python.exe scripts/build_web_coverage.py
.venv/Scripts/python.exe scripts/ci_run.py reporting
.venv/Scripts/python.exe scripts/build_delivery.py
```

Ejecutar en orden y revisar cada salida. `ci_run.py` devuelve 0 cuando el gate correspondiente aprueba; los manifiestos conservan la salida original de cada herramienta. Si un gate bloquea, abrir `reports/gate/<herramienta>.json`: no agregar una excepción automáticamente. Corregir scripts/preparación si corresponde o revisar y documentar una causa del producto. Nunca modificar Qolqe ni suprimir tests para pasar.

Las tres corridas web usan una base nueva cada una, no graban vídeo por defecto y retiran la base temporal al cerrar el servidor. API también retira las bases de su propia instancia y conserva server.log. Mantener libres los puertos 8000 y 8011 antes de que arranquen sus lanzadores. No mezclar una instancia manual con la instancia que estos comandos gestionan.

## Publicar y demostrar el pipeline real

Los cambios siguen en la rama `codex/parte2-alcance-api`. Revisar y publicar:

```powershell
git status --short
git diff --stat
git add -A
git diff --cached --stat
git commit -m "Completa entrega 2 con Quality Gate Escenario A y presentacion"
git push -u origin codex/parte2-alcance-api
```

Crear un pull request de esa rama hacia `main`. El workflow `.github/workflows/pruebas.yml` se activa en PR hacia main, push a main y ejecución manual. Son exactamente tres trabajos: API → Web → Reportería. Web y Reportería se ejecutan aunque el anterior falle para conservar evidencia.

En Actions abrir **Pipeline CI/CD - Entrega 2**, comprobar commit e intento y esperar los tres jobs. Si están aprobados por Escenario A, descargar `entrega-parte2-<run>-<intento>`, extraerlo y abrir `apidoc/parte2/index.html`. Revisar el enlace del run, la matriz, reportes crudos y `reports/gate/resumen.md`. Un job verde no significa que cada test tenga PASS.

Integrar el PR a main y verificar también su ejecución. Los enlaces del anexo del PPT apuntan a main; solo reflejarán estos archivos cuando la entrega esté integrada. Para repetir en vivo: Actions → workflow → Run workflow → main. El pipeline puede tardar más de 15 minutos; iniciarlo al comienzo y tener disponible un run anterior del mismo commit, identificado como tal. Nunca presentar un run viejo de otro código como ejecución actual.

## Exposición: 15 minutos + 5 de preguntas

| Tiempo | Diapositivas / pantalla | Qué demostrar |
|---|---|---|
| 0–2:30 | 1–3 | Alcance general, compartido y específico; selección, particiones, límites y estados. |
| 2:30–4:15 | 4–5 | Por qué Cypress, arquitectura y POM en `Web/cypress/pages/ContactosPage.ts`. |
| 4:15–6:00 | 6–7 + matriz/Actions | Mismo HU/TC en fuente y resultado; tres jobs del pipeline real. Dispararlo temprano. |
| 6:00–8:00 | 8–9 | Reglas del gate y defectos con riesgo declarado; admisión académica, no productiva. |
| 8:00–11:00 | 10 + Cypress | Happy path real, respuesta 201 y persistencia; un FAIL conocido si hay tiempo. |
| 11:00–12:00 | 11 + reporte | 45 PASS y 9 known issues en cada corrida; cero inestabilidad detectada. |
| 12:00–14:00 | 12 | Contrato: señales revisadas no equivalen a defectos únicos; conclusiones y límites. |
| 14:00–15:00 | 13 | Anexo / Referencias: repositorio main, matriz, política y Actions. |
| 15:00–20:00 | Preguntas | Defender un caso, una firma y el patrón. |

Explicación central: «La prueba sigue fallando porque el defecto existe. El gate aprueba el Escenario A porque la causa está registrada y admitida para esta instancia aislada, y no hay errores nuevos ni intermitencias».

Si se pregunta por la estabilidad: se fijó un entorno dentro del rango de dependencias original que confirma las escrituras antes de responder; no se modificó Qolqe. Ver la documentación oficial enlazada en `quality-gate.md`.

Si se pregunta por CI/CD: el workflow implementa CI de pruebas y publicación de evidencia; no despliega la aplicación a producción. La demo IA es complementaria y se conserva aparte; esta rúbrica exige pipeline, reporte, matriz y automatización.

## Canvas

Subir únicamente el archivo `presentacion/Entrega2-Qolqe-Cypress.pptx`, según las indicaciones docentes. Antes de subirlo comprobar que los enlaces de main abren la versión final y ensayar el acceso a los artefactos. La hora límite indicada en el material recibido es 19:00; confirmar que corresponde a la sesión de entrega.
