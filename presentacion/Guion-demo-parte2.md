# Guion de la demo en vivo · Entrega 2 · Qolqe G4

Granit y Franco · 15 min de exposición + 5 de preguntas. Las indicaciones entre [corchetes] son acciones y no se leen. Los resultados se anuncian después de verlos en pantalla, nunca se prometen. Este archivo es personal: Git lo ignora (`presentacion/[Gg]uion*`).

Base: rama `main`, commit `8d8208b`. Lo que se dice sale de ese código, de `docs/parte2/` y del run 41131622090.

---

## 0. Estado real (30 oct, 17:45 Lima): leer antes de empezar

| Tema | Estado | Qué hacer |
|---|---|---|
| Demo local | Presentación en `http://localhost:8765/apidoc/parte2/#presentacion`. Cypress abierto en la pestaña «Cypress demo» de la Terminal | El clic sobre el spec es manual |
| Run remoto de `main` ([run 41131622090](https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/41131622090), 16:31) | **Rojo.** Karate gate A (169 PASS, 12 known) · Web gate A (45 PASS, 9 known) · Schemathesis **BLOQUEADO** (25 known + **2 firmas desconocidas**) | Elegir opción A o B del apartado 4 antes de empezar |
| Causa del rojo | Las 2 firmas son variantes de K-C03 (celular con dígitos Unicode, 422 `CELULAR_INVALIDO`). Con la misma semilla, Linux generó 2 cuerpos distintos a los registrados, y la firma incluye el cuerpo. Salen iguales en los 2 runs de CI | Respuesta lista en 5.1 |
| Arreglo | Agrupar K-C03 por causa, como ya se hace con K-C02. Probado fuera de línea contra los datos del run de Linux: 27 de 27 known, gate A. Está en un `git stash` local, **sin subir** | Subirlo exige PR, merge y ~9 min de run. Decisión de ustedes |
| Reportes en esta Mac | En `8765` los enlaces de «Reportes» dan **404**: Git ignora `reports/raw` y `reports/cypress`. El artefacto del run **ya está descargado** en `tmp/entrega-run` y servido en `http://localhost:8766/apidoc/parte2/`: 34 de sus 35 enlaces locales responden | Usar `8766` para los reportes y `8765` para el resto |
| Artefactos del run | `entrega-parte2-41131622090-1` vence el 6 nov | |
| Workflow viejo | `Cypress contactos E2E` sigue activo y en rojo: corre la misma suite sin clasificar los 9 known | Si preguntan: es del flujo anterior; el gate vigente es `pruebas.yml` |

---

## 1. Antes de entrar (10 min antes)

- [ ] Presentación web abierta en `#presentacion`. Si el servidor se cayó:

```bash
cd "/Users/granitespinozasalazar/Documents/pruebas y verificcion de soft/qolqe-g4-qa" && .venv/bin/python -m http.server 8765 --bind 127.0.0.1
```

- [ ] Cypress interactivo, desde la Terminal de la app (no desde Claude: ahí Chrome no conectó). Cerrar antes cualquier Cypress anterior (Ctrl-C), porque el puerto 8011 debe estar libre:

```bash
cd "/Users/granitespinozasalazar/Documents/pruebas y verificcion de soft/qolqe-g4-qa" && CYPRESS_CACHE_FOLDER="$PWD/.tools/cypress-binary" CY_VIDEO=0 CY_KEEP_DB=0 QA_PYTHON="$PWD/.venv/bin/python" npm run cy:open
```

- [x] Artefacto del run: **ya descargado** en `tmp/entrega-run` (Git ignora `tmp/`) y servido en `http://localhost:8766/apidoc/parte2/`. Si el servidor se cae, desde la raíz del repo:

```bash
cd "/Users/granitespinozasalazar/Documents/pruebas y verificcion de soft/qolqe-g4-qa" && python3 -I -m http.server 8766 --bind 127.0.0.1 --directory tmp/entrega-run
```

En esa página, 34 de 35 enlaces locales responden. Solo «Demo Cypress anterior» (menú de arriba) da 404, porque el artefacto no incluye esa carpeta: no usarlo ahí. Para descargarlo de nuevo (vence el 6 nov), en otra carpeta:

```bash
cd "/Users/granitespinozasalazar/Documents/pruebas y verificcion de soft/qolqe-g4-qa" && gh run download 41131622090 -R granitespinoza/qolqe-g4-qa -n entrega-parte2-41131622090-1 -D tmp/entrega-run-2
```

- [ ] Pestañas listas: Actions del run · `Web/cypress/support/fixtures.ts` (líneas 92-97) · `API/features/hu-g4-01.feature` (línea 51) · `Web/cypress/pages/ContactosPage.ts` · `.github/workflows/pruebas.yml` · `docs/parte2/defectos-conocidos.md`.
- [ ] Notificaciones apagadas. Zoom del navegador al 125 %.
- [ ] Decidida la opción A o B del run (apartado 4).
- [ ] Cronómetro visible.

---

## 2. Hoja de ruta

| Min | PPT | Qué se muestra |
|---|---|---|
| 0:00-2:30 | 1-3 | Alcance (específicos: contactos, transferencias desde contactos, solicitudes; compartidos: login, saldo, movimientos) y técnicas |
| 2:30-4:15 | 4-5 | Por qué Cypress; arquitectura y Page Object Model |
| 4:15-6:00 | 6-7 | **Bloque 1** trazabilidad y **Bloque 4** pipeline |
| 6:00-8:00 | 8-9 | Gate y defectos |
| 8:00-11:00 | 10 | **Bloques 2 y 3** Cypress en vivo |
| 11:00-12:00 | 11 | **Bloque 5** el run y el reporte |
| 12:00-14:00 | 12 | **Bloque 6** Schemathesis y conclusiones |
| 14:00-15:00 | 13 | Anexo / Referencias |
| 15:00-20:00 | — | Preguntas (apartado 5) |

Si van a disparar un run nuevo, hacerlo en el minuto 0: tarda ~9 min (el último fue 8 min 46 s).

```bash
gh workflow run pruebas.yml -R granitespinoza/qolqe-g4-qa --ref main
```

---

## 3. Guion por bloques

### Bloque 1 · Trazabilidad en el código (4:15-5:15 · PPT 6)

[Abrir `Web/cypress/support/fixtures.ts`, líneas 92-97, función `caso`]

"Cada prueba lleva su historia y su caso en el nombre: `@HU-G4-01` y `@TC-E2E-G4-102`. Si es un defecto conocido, el mismo nombre añade `@known_issue` y `@D-01`."

[Abrir `API/features/hu-g4-01.feature`, línea 51]

"En API es igual, en el Gherkin: `@TC-G4-004 @known_issue @D-01`."

[Presentación web → `#matriz` → buscar `E2E-G4-102`]

"El mismo identificador aparece en el código, en la matriz y en el resultado. Columnas: HU, TC, escenario, capa, tags en código, estado de prueba y defecto asociado. Aquí: Web, FALLA / KNOWN ISSUE, defecto D-01."

[Filtro «Known issues»]

"En esta matriz son 18 filas: 9 TC de Web y 9 de API."

### Bloque 2 · Cypress en vivo (8:00-9:30 · PPT 10)

[Ventana de Chrome de Cypress → clic en `contactos-happy-path.cy.ts`; dura unos 2 s]

"Este es el smoke de HU-G4-01, criterio 1, `E2E-G4-001`. Los datos se preparan por API en una base aislada. La prueba entra por la interfaz y agrega un contacto."

[Señalar en el log: la petición `POST /api/contactos` con 201, la fila «Ana Cypress», el recargado y el contador «1 de 15». Si el log se ve distinto, no importa: lo que se defiende es el 201 y el «1 de 15» tras recargar]

"Observamos la respuesta real del servidor: 201 y el cuerpo con alias, celular y favorito falso. Recargamos y sigue ahí: 1 de 15."

[Abrir `Web/cypress/pages/ContactosPage.ts`]

"El test no tiene selectores: usa `agregar`, `filas` y `contador`. Los `data-testid` viven en un solo Page Object; si cambia un selector, se corrige ahí."

### Bloque 3 · Un fallo conocido (9:30-11:00 · PPT 10)

[Volver a la lista de specs → clic en `contactos-completo.cy.ts`. Corre sus 21 casos, ~40 s; 5 fallan]

Mientras corre: "Este archivo tiene 21 casos. Cinco fallan por defectos conocidos. El gate lo permite solo si cada fallo coincide con una firma registrada."

[Al terminar: ubicar en rojo `E2E-G4-102 @HU-G4-01 @TC-E2E-G4-102 @known_issue @D-01 | WEB-G4-01-CA1-01 | [D-01] ñ debe ser válida al crear` y abrir el detalle: `AssertionError: expected 422 to equal 201`]

"Esta prueba falla y debe fallar. Crear un contacto con alias «Niño» devuelve 422 y debería devolver 201. Es el defecto D-01, severidad media. El FAIL se conserva en el reporte. El gate lo admite porque coincide exacto: mismo archivo, mismo ID, mismo mensaje y etiqueta `@known_issue`. Con otro mensaje, bloquea."

Si falta tiempo: no esperar la corrida; mostrar el mismo caso en el reporte del artefacto.

### Bloque 4 · Pipeline y gate (4:15-8:00 · PPT 7-9)

[GitHub → Actions → «Pipeline CI/CD - Entrega 2» → el run → commit e intento]

"Tres trabajos en orden. API, con Karate y Schemathesis. Web, con tres corridas de Cypress, que corre aunque API falle. Y Reportería, que consolida el mismo run e intento. Se activa con push o PR a main, y a mano."

[`.github/workflows/pruebas.yml`: mostrar `on:`, `needs` e `if: always()`]

"No usamos `continue-on-error`: los FAIL quedan en los reportes y el gate decide."

[PPT 8]

"Aprueba si todo pasa o si los únicos fallos son defectos conocidos admitidos para la instancia académica aislada. Bloquea: fallo nuevo, causa distinta, preparación inválida, reporte ausente, omisiones e intermitencia."

[PPT 9]

"Admitimos el riesgo solo para esta instancia aislada, con datos y dinero ficticios. No es una aprobación para producción. D-04, token válido tras logout, y D-05, invariantes monetarias concurrentes, conservan su severidad crítica."

### Bloque 5 · El run y el reporte (11:00-12:00 · PPT 11)

[Abrir `http://localhost:8766/apidoc/parte2/#reportes`: la matriz y los enlaces a los reportes crudos de ese run (Karate, Schemathesis y las 3 corridas de Cypress). El resumen del gate está en `http://localhost:8766/reports/gate/resumen.md`]

Ver apartado 4 para el discurso de la opción A o B. Después:

"Tres corridas web: 45 PASS, 9 FAIL crudos que son 9 known issues, cero flaky y cero omitidas. API: 169 PASS y 12 known issues. No lo presentamos como 54 pruebas en verde."

### Bloque 6 · Schemathesis y cierre (12:00-15:00 · PPT 12-13)

"562 interacciones y 27 ocurrencias de contrato. No son 27 defectos: son señales revisadas por causa, K-C01 a K-C04. Qolqe permanece intacto: está fijado al commit `8c7d2f0` y el gate comprueba que no se modificó."

[PPT 13]

"Anexo: repositorio en main, matriz de trazabilidad, política y defectos conocidos, y el run en Actions."

---

## 4. El run: decidir antes de empezar

### Opción A · Mostrar el run real que existe (rojo) y explicarlo

[Actions → run 41131622090 → job «Reportería, matriz y decisión final» → paso «Aplicar decisión consolidada sin esconder fallos»: se ve la tabla Herramienta | Gate | PASS | Known issue | Desconocido | Flaky]

"Este es el run real de `main`, commit `8d8208b`, del 30 de octubre a las 16:31. Karate y Web pasan el gate en Escenario A. Schemathesis bloqueó: aparecieron dos firmas que la política no conoce. No las aceptamos automáticamente.

Las analizamos. Son variantes del señal K-C03, celular con dígitos Unicode que el esquema acepta y Qolqe rechaza con 422. Con la misma semilla, en Linux se generaron dos cuerpos distintos a los registrados. El problema está en nuestra firma, que incluía el cuerpo aleatorio. La corrección es agruparla por causa, como ya hacemos con K-C02, y documentarlo. No se toca Qolqe ni se quita el check."

Si dice «entonces el pipeline no pasa»: "Correcto: hoy el gate de main está bloqueado y lo mostramos. Es la razón de correrlo en CI: en el entorno local de Windows aprobaba. Una señal nueva bloquea, sin excepciones automáticas."

### Opción B · Hay un run verde del commit final

[Actions → el run verde → comprobar que el commit es el entregado]

"Este es el run del commit entregado, con los tres trabajos aprobados. Un job verde no significa que cada test pase: los FAIL conocidos siguen en los reportes crudos, y el gate los admite por Escenario A."

Nunca presentar un run viejo de otro código como ejecución actual.

---

## 5. Si interrumpe: respuestas de 20 segundos

1. **¿Por qué el pipeline está bloqueado?** Dos firmas de Schemathesis sin registrar, variantes de K-C03. Es nuestra firma, que incluía el cuerpo aleatorio. Se corrige agrupando por causa. Evidencia: log del paso «Aplicar decisión consolidada».
2. **¿Por qué esa prueba falló y el gate aprueba?** Porque es D-01: mismo archivo, mismo ID, mismo mensaje y `@known_issue`, y el riesgo está admitido en `data/quality-policy.json` solo para la instancia aislada. Con otro mensaje bloquea.
3. **¿Dónde está la etiqueta en el código?** Web: `fixtures.ts`, función `caso`, líneas 92-97. API: `hu-g4-01.feature`, línea 51.
4. **¿Cómo garantizan la trazabilidad sin Kiwi TCMS?** Con etiquetas en el código y una matriz HU → CA → caso → ejecución que se regenera en cada run. `build_scope.py --check` comprueba que la matriz coincide con los requisitos y que los casos tienen archivos reales.
5. **¿Qué diferencia hay entre known issue y flaky?** Known issue falla siempre, con la misma causa registrada. Flaky es el mismo caso cambiando de resultado entre corridas sin cambiar fuentes: bloquea. Corremos Web tres veces y cualquier cambio PASS ↔ FAIL bloquea. Ejemplo real: FastAPI desde 0.118 cierra las dependencias con `yield` después de enviar la respuesta, y Qolqe confirma ahí su commit; se fijó 0.117.1 y las tres corridas salieron iguales.
6. **¿Por qué Cypress y no Playwright?** Corre en el navegador con log de comandos y snapshots, reintenta aserciones, observa la red real con `cy.intercept`, y el equipo trabaja en TypeScript sobre un solo dominio. Playwright es una alternativa válida; no la comparamos con pruebas propias.
7. **¿Por qué Page Object?** Los tests guardan escenarios y aserciones; los selectores viven en `ContactosPage.ts`. Si cambia uno, se corrige en un lugar.
8. **¿Usan esperas o reintentos?** No hay esperas fijas. Solo hay sondeos acotados, de máximo 10, para preparar datos tras un commit, y quedan en el log como «preparación: sondeo n/10». Las operaciones de negocio se ejecutan una vez.
9. **¿Por qué no hay pruebas de seguridad o carga en cada push?** Quedaron fuera del alcance de esta entrega y no están implementadas. Sí corremos contrato con Schemathesis, con semilla 20261013 y máximo 20 ejemplos. Carga y DAST irían programadas fuera del push; es una propuesta, no algo hecho.
10. **¿No aceptaron defectos críticos?** D-04 y D-05 conservan severidad crítica. La admisión es solo para la evaluación aislada, con datos ficticios. No certifica producción ni es una aprobación de la docente.
11. **¿Cuántas pruebas son?** 130 TC de API únicos, que dan 181 ejecuciones por los Scenario Outline, y 54 TC de Web. Un TC puede aparecer en varios criterios; las filas de la matriz no son tests independientes.
12. **¿Pueden agregar excepciones para pasar?** Cada excepción es exacta (archivo, ID, mensaje, defecto admitido) y está versionada en `data/quality-policy.json`. La etiqueta sola no basta. Si cambia una fuente aprobada, el gate falla con «Cambió una fuente aprobada».
13. **¿Modificaron Qolqe?** No. Commit fijo `8c7d2f0`, y el gate verifica que la referencia esté limpia.
14. **¿Por qué Web corre aunque API falle?** Para conservar toda la evidencia. La decisión final se consolida en el tercer trabajo.

Si no saben una cifra: "No la tenemos medida; la verificamos y la agregamos". No improvisar números.

---

## 6. Plan B

- **Cypress no abre o Chrome no conecta:** en la Terminal, `npm run cy:smoke` con las mismas variables del apartado 1, y abrir el reporte ya generado: `reports/cypress/2026-10-30T22-24-55-185Z-smoke/html/index.html` (1 passing).
- **Puerto 8011 ocupado:** Ctrl-C en la pestaña anterior de Cypress y repetir.
- **Sin internet o sin GitHub:** matriz local en `localhost:8765` y el artefacto descargado en `localhost:8766`.
- **`contactos-completo` tarda demasiado:** mostrar `E2E-G4-102` desde el reporte de CI: `http://localhost:8766/reports/cypress/2026-10-30T21-33-22-238Z-regression/html/index.html`.
- **Un enlace de «Reportes» da 404 en `8765`:** es normal, esos enlaces apuntan a corridas locales anteriores. Usar la página de `8766` (artefacto), cuyos enlaces apuntan a los reportes de ese run.

---

## 7. Si te sale una palabra que no es de este repo

| No decir | Decir |
|---|---|
| Playwright | Cypress 16.2.0 con Page Objects |
| Allure | Reporte HTML consolidado (`apidoc/parte2`), mochawesome, y los HTML de Karate y Schemathesis |
| Cucumber | Karate (Gherkin, archivos `.feature`) |
| `@HU-01`, `@TC-001`, `DEF-101` | `@HU-G4-01`, `@TC-G4-004`, `@TC-E2E-G4-102`, `D-01` |
| 54 PASS | 45 PASS y 9 known issues |
| Pipeline en verde | Solo si lo están viendo en pantalla |
| Nightly implementado | Propuesta, no implementado |
| Un run viejo como actual | Nunca |

---

## 8. Cifras para memorizar

- **Alcance:** 18 criterios G4 · 36 grupos de variantes · 54 pruebas web · 130 TC API únicos (181 ejecuciones).
- **Web, 3 corridas:** 45 PASS · 9 FAIL crudos = 9 known · 0 flaky · 0 omitidas.
- **API:** 169 PASS · 12 known · 0 fallos de Background.
- **Schemathesis:** 562 interacciones · 27 ocurrencias · 9 controles contextuales exitosos · semilla 20261013 · máximo 20 ejemplos. En el run de CI: 25 known + 2 desconocidas.
- **Defectos:** D-01 alias con ñ (media) · D-02 duplicados normalizados (media) · D-03 solicitud vencida aceptada (alta) · D-04 token válido tras logout (crítica) · D-05 invariantes monetarias concurrentes (crítica) · D-06 coerción de favorito (media) · D-07 historial omite el último día (alta) · D-08 transferencia a cuenta cerrada (alta). Señales de contrato: K-C01 a K-C04.
- **Versiones:** Cypress 16.2.0 · Node 24 en CI · FastAPI 0.117.1 y Starlette 0.48.0 fijados · Karate 1.5.2 · Schemathesis 4.17.0 · Python 3.13 en CI · Qolqe `8c7d2f0`.
- **Run:** «Pipeline CI/CD - Entrega 2» · ~9 min · artefactos 7 días.
