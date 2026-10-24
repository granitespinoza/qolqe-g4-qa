# Guion de exposición: Cypress

Granit expone la presentación principal (`presentacion/cypress/Cypress-Principal.pptx`, 10 diapositivas, unos 7 a 8 minutos). Franco expone «Cypress en Qolqe» (`presentacion/cypress/Cypress-Qolqe.pptx`, 11 diapositivas, unos 6 a 7 minutos). Las indicaciones entre corchetes son acciones y no se leen. Los resultados se anuncian después de ejecutar, nunca se prometen.

**Verificar antes de exponer:** las comparaciones con Playwright, Selenium, Robot Framework y WebdriverIO salen de conocimiento general, no de la documentación de Cypress ni del repo. Contrastarlas con la comparativa que presentó la docente.

---

## Parte 1: Granit, Cypress (presentación principal)

**[Diapositiva 1: portada] Gancho (30 s)**

"Buenos días, profesora. Imaginen que ayer una prueba falló y hoy pasa, sin que nadie haya cambiado una línea de código. ¿Fue un defecto o fue la prueba? Esa duda cuesta tiempo y confianza.

Hoy presentamos Cypress. Vamos a explicar qué es, cómo funciona y cuándo conviene usarlo. También vamos a compararlo con otras alternativas, y al final Franco mostrará cómo lo aplicamos en el módulo de contactos de Qolqe."

**[Diapositiva 2: el dolor] (45 s)**

"El problema de automatizar pruebas web es conocido: esperas fijas para que cargue la página, fallos intermitentes que no se reproducen, comandos que viajan por la red hacia el navegador, y depurar casi a ciegas, con solo un mensaje de error.

Cypress propone lo contrario: esperar automáticamente a la interfaz, correr junto a la aplicación y dejar ver qué pasó en cada paso. El resultado esperado es menos falsos negativos y menos tiempo buscando por qué falló una prueba."

**[Diapositiva 3: qué es y evolución] (45 s)**

"Cypress es un framework de pruebas end-to-end en JavaScript y TypeScript. En 2017 salió su beta pública como código abierto. En 2022, con Cypress 10, incorporó pruebas de componentes. Más recientemente apareció `cy.prompt`, en la versión 15.4, y pasó a beta en la 15.13. Nosotros usamos la 16.2.0.

Además de E2E, prueba componentes y hace solicitudes API."

**[Diapositiva 4: arquitectura] (1 min)**

"La diferencia de fondo es la arquitectura. Con un enfoque tipo Selenium, el script manda comandos a un driver y este al navegador, por la red. Cypress se ejecuta dentro del navegador, en el mismo bucle de ejecución que la aplicación. Detrás hay un proceso Node.js que se encarga de lo que el navegador no puede hacer: capturas, video, archivos y red.

Por eso no hay latencia de red entre el comando y el navegador, y además puede observar o modificar el tráfico. Mocha organiza los `describe` e `it`, y Chai aporta las aserciones."

**[Diapositiva 5: por qué nos ayuda] (1 min)**

"Cuatro capacidades nos importan. Una: espera automática. Cypress espera a que el elemento sea visible, esté habilitado y no esté cubierto antes de actuar, y reintenta las aserciones. Dos: viaje en el tiempo, con snapshots del DOM por cada comando. Tres: control de red con `cy.intercept`, que permite observar o simular respuestas. Y cuatro: evidencia, con capturas al fallar y video.

Esto reduce los fallos intermitentes, pero no los elimina por completo."

**[Comparación: decirla aquí o en la diapositiva 9] (1 min)**

"Hay otras alternativas muy válidas. Frente a Selenium y WebdriverIO, que se basan en el protocolo WebDriver y envían comandos al navegador desde fuera, Cypress gana en depuración visual y en que corre dentro del navegador, lo que reduce la latencia. En cambio Selenium soporta más lenguajes y navegadores.

Frente a Playwright, que es muy potente y cubre varios navegadores y pestañas, Cypress es más simple de empezar para quien ya trabaja con JavaScript y su interfaz de depuración es muy didáctica. Playwright sería mejor si necesitáramos varios navegadores o pestañas en un mismo test.

Frente a Robot Framework, que es de palabras clave y muy legible para equipos no técnicos, Cypress se escribe directamente en código y no necesita librerías adicionales.

No decimos que Cypress sea mejor en todo. Para nuestro caso, un flujo continuo dentro de un solo dominio, escrito en TypeScript, y con la necesidad de depurar rápido, es la mejor opción."

**[Diapositiva 6: IA] (1 min)**

"Sobre inteligencia artificial: Cypress incluye `cy.prompt`, que convierte pasos en lenguaje natural en comandos de Cypress. Está en beta desde la 15.13, requiere Cypress Cloud y navegador Chromium, y permite ver el código generado con el botón Code. Según su documentación incluye también self-healing: si cambia un selector o su texto, vuelve a resolver el paso. Tiene límites: no admite `cy.request`, iframes ni canvas, y funciona mejor en inglés.

Nosotros demostramos la generación y ejecución de pasos, y revisamos el código generado. El self-healing es de la herramienta, pero no lo probamos."

**[Diapositiva 7: patrón de diseño] (1 min)**

"Para estructurar las pruebas usamos Page Object con Custom Commands, en tres capas. Los tests guardan los escenarios y las aserciones del negocio. Los Page Objects guardan los selectores y acciones de cada pantalla. Y los Custom Commands reúnen la preparación reutilizable, como `cy.prepararContactos`.

¿Por qué es el adecuado para contactos? Porque el módulo se reduce a una pantalla con un formulario y una lista, con varias reglas que se prueban sobre los mismos elementos. Si cambia el selector del botón Agregar, se actualiza en un solo Page Object y no en todos los tests. Además, permite que cada integrante trabaje una página distinta sin chocar. Es una decisión de diseño, no una regla de Cypress: cuidamos que los Page Objects no guarden estado compartido."

**[Diapositiva 8: evidencias] (45 s)**

"Sobre evidencias: `cypress open` es la interfaz interactiva para desarrollo, y `cypress run` es para CI. Ahí Cypress toma capturas automáticas al fallar. El video se graba durante la ejecución y un hook lo elimina cuando el spec pasó, así solo conservamos el video de lo que falla. Eso ahorra almacenamiento y los artefactos de CI se retienen siete días."

**[Diapositiva 9: cuándo sí y cuándo no] (45 s)**

"Cuándo sí: aplicaciones web modernas, flujos continuos en un dominio, equipos con JavaScript o TypeScript, y cuando conviene observar o simular la red. Cuándo no: aplicaciones móviles nativas o de escritorio, pruebas de carga, tests que necesiten varios navegadores o pestañas a la vez, o equipos que exigen Java, Python o C#."

**[Diapositiva 10: cierre] (20 s)**

"En resumen: Cypress nos da espera automática, depuración visual, control de red y evidencia de fallos; sus límites son un navegador a la vez y un dominio por prueba. Nuestra decisión fue aplicarlo con Page Objects sobre HU-G4-01. Franco muestra ahora cómo se ve eso en Qolqe."

---

## Parte 2: Franco, Cypress en Qolqe

**[Diapositiva 1: portada] (20 s)**

"Gracias. Ahora vemos Cypress aplicado al registro de contactos de Qolqe: 3 escenarios de la historia HU-G4-01, criterio de aceptación 1. Los escenarios corren sobre la interfaz, la API y la base reales."

**[Diapositiva 2: arquitectura de ejecución] (40 s)**

"Un lanzador Node inicia un solo servidor con la aplicación original en el puerto 8011 y su propia base SQLite. No modificamos Qolqe ni usamos la base de Karate. Cypress corre en el navegador y el proceso Node genera reportes y videos. Cypress Cloud solo interviene en la demo de IA."

**[Diapositiva 3: trazabilidad] (1 min)**

"Los escenarios nacen de HU-G4-01 CA1. El primero es el smoke: alta válida con alias 'Ana Cypress', donde esperamos 201 y que el contacto siga allí al recargar. Dos de regresión: alias 'Lu', de 2 caracteres, justo debajo del mínimo de 3, que debe devolver 422 sin crear nada; y celular duplicado, que devuelve 409 y deja una sola fila.

Los elegimos porque son el camino principal y los dos rechazos más relevantes. No cubren todas las reglas: celular propio o inactivo, límite 15, todas las fronteras del alias y HU-G4-02 se prueban a nivel API."

**[Diapositiva 4: patrón] (30 s)**

"Aquí se ve el patrón en el repo: `LoginPage` y `ContactosPage` centralizan los selectores `data-testid`, los tests conservan las aserciones, y `cy.prepararContactos` crea dos usuarios ficticios por escenario."

**[Diapositiva 5: demo happy path] (2 min)**

[Abrir con `scripts/cypress.ps1 open` y elegir `contactos-happy-path.cy.ts`.]

"Preparamos los usuarios por API, ingresamos por la interfaz, agregamos el contacto y esperamos la respuesta del POST. `cy.intercept` solo observa la petición real, no la simula. Luego comprobamos la fila y recargamos para confirmar la persistencia."

[Cuando termine:] "En esta ejecución obtuvimos ___." [Anunciar solo lo que muestre la pantalla.]

**[Diapositiva 6: IA] (1 min 30 s)**

[Con `ai-open`, ya con sesión Cloud iniciada, ejecutar `contactos-ia.cy.ts`.]

"La IA recibe pasos en lenguaje natural, completa Celular y Alias y pulsa Agregar. Con la opción Code revisamos los comandos generados. Las aserciones de 201 y persistencia son explícitas, no generadas. Si algo falla por Cloud o conexión, mostramos esta captura de la ejecución aprobada del 24/10 y lo decimos como respaldo."

**[Diapositiva 7: evidencia] (40 s)**

"Con `cypress run` guardamos reporte HTML, capturas al fallar, y el video solo de los specs fallidos. Un dato real: una ejecución verde avisó que no capturó suficientes cuadros para el video. Un test verde no garantiza que la evidencia se generó, así que revisamos los artefactos."

**[Diapositiva 8: fallo didáctico] (45 s)**

[`scripts/cypress.ps1 failure`, luego `report`.]

"Aquí exigimos a propósito dos contactos cuando hay uno. Cypress informa la diferencia y conserva captura, video y reporte. La salida 1 es esperada y no es un defecto de Qolqe: está fuera de la regresión y de CI."

**[Diapositiva 9: resultados] (40 s)**

"Los resultados que verificamos: [actualizar con los de la ejecución de hoy] smoke, regresión y fallo esperado, con sus duraciones. El workflow de CI en GitHub Actions también corrió la regresión." [Confirmar en Actions antes de decirlo.]

**[Diapositiva 10: dificultades] (40 s)**

"Dificultades reales: el Node 20 del equipo era incompatible con Cypress 16, las comillas de PowerShell 5 se perdían, y `cy.prompt` falló la primera vez al descargar su módulo de Cloud. Límites: son 3 escenarios, no toda Qolqe."

**[Diapositiva 11: entrega] (30 s)**

"El repositorio tiene el README con los comandos, la trazabilidad y los workflows, y se reproduce con `install`, `setup`, `typecheck` y `smoke`. Gracias."

---

## Preparación antes de exponer (Windows, Node 24 LTS)

- `scripts/cypress.ps1 install`, `setup`, `typecheck` y `smoke`, una vez y con tiempo.
- Puerto 8011 libre; un solo modo a la vez.
- Para la IA, usar `ai-open` (el modo `ai` headless falló el 24/10) e iniciar sesión en Cypress Cloud antes; si pide proyecto, definir `$env:CYPRESS_PROJECT_ID`.
- Actualizar la diapositiva 9 de «Cypress en Qolqe» con los números de la ejecución propia.

## Preguntas probables

| Pregunta | Respuesta corta |
|---|---|
| ¿Por qué Cypress y no Playwright? | Para un flujo en un dominio y equipo JS/TS, Cypress es más simple y su depuración es muy didáctica. Playwright sería mejor con varios navegadores o pestañas. |
| ¿Por qué Page Object? | Separa selectores de aserciones y facilita el mantenimiento; es una decisión de diseño, no obligatoria. |
| ¿La IA hace self-healing? | `cy.prompt` lo incluye según su documentación, pero no lo probamos. |
| ¿Por qué solo 3 escenarios? | Es el camino principal y dos rechazos clave de HU-G4-01 CA1. El resto está en las pruebas de API. |
| ¿El fallo de la demo es un bug? | No, es una expectativa falsa a propósito. |
| ¿Cobertura completa? | No se declara; ver límites en `docs/cypress/trazabilidad.md`. |
