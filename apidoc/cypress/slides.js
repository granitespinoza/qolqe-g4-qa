window.CYPRESS_SLIDES = [
  {
    "title": "Un contacto que permanece",
    "label": "01 / Demo de Qolqe",
    "body": "Automatización E2E de HU-G4-01: agregar un contacto y comprobarlo después de recargar.",
    "items": [
      "Granit y Franco · Grupo 4",
      "Cypress + TypeScript · Interfaz y API reales",
      "Happy path, IA en vivo y evidencia de ejecución"
    ],
    "why": "El éxito se comprueba con aserciones sobre la respuesta y la interfaz.",
    "link": "#ejecucion",
    "action": "Preparar la demo"
  },
  {
    "title": "Qué cubrimos",
    "label": "02 / Del requisito al caso",
    "body": "CA1 de HU-G4-01 guía los datos y los resultados esperados.",
    "rows": [
      [
        "Caso",
        "Dato / técnica",
        "Esperado"
      ],
      [
        "E2E-G4-001",
        "Ana Cypress · partición válida",
        "201; una fila persiste al recargar"
      ],
      [
        "E2E-G4-002",
        "Lu · valor 2, bajo el mínimo 3",
        "422 ALIAS_INVALIDO; cero contactos"
      ],
      [
        "E2E-G4-003",
        "Mismo celular dos veces · partición inválida",
        "409 CONTACTO_EXISTENTE; una sola fila"
      ]
    ],
    "why": "Estos tres casos cubren un camino válido y dos rechazos. No representan toda Qolqe ni todas las reglas de CA1.",
    "link": "../../docs/cypress/trazabilidad.md",
    "action": "Ver trazabilidad"
  },
  {
    "title": "El recorrido de la prueba",
    "label": "03 / Arquitectura de nuestra demo",
    "body": "El navegador usa la interfaz de Qolqe y esta se comunica con FastAPI y SQLite.",
    "items": [
      "Tests TypeScript y Page Objects ejecutan acciones sobre la UI.",
      "El lanzador inicia la aplicación en 127.0.0.1:8011 con una base exclusiva para Cypress.",
      "Node.js coordina la ejecución, los eventos y los reportes.",
      "Solo la demo de cy.prompt utiliza Cypress Cloud."
    ],
    "why": "La preparación por API crea usuarios ficticios. El flujo evaluado agrega el contacto desde la interfaz.",
    "link": "../../scripts/cypress/server.py",
    "action": "Ver servidor de pruebas"
  },
  {
    "title": "Dónde está el patrón",
    "label": "04 / Page Object y Custom Commands",
    "body": "Cada pantalla reúne sus selectores y acciones. El escenario declara los resultados de negocio.",
    "code": "const pagina = new ContactosPage()\nnew LoginPage().ingresar(propietario.celular, propietario.pin)\npagina.abrir()\npagina.agregar(contacto.celular, 'Ana Cypress')\npagina.filas().should('have.length', 1)",
    "items": [
      "LoginPage y ContactosPage reutilizan acciones y selectores data-testid.",
      "cy.prepararContactos crea dos usuarios para cada escenario.",
      "Las páginas también comprueban que terminaron de abrir o iniciar sesión."
    ],
    "why": "Un cambio de selector se concentra en el Page Object. El test conserva visibles las verificaciones del negocio.",
    "link": "#codigo",
    "action": "Abrir los archivos del patrón"
  },
  {
    "title": "Happy path en vivo",
    "label": "05 / Ejecutar el flujo",
    "body": "Agregar “Ana Cypress” y comprobar que el contacto permanece.",
    "items": [
      "Preparar usuarios e iniciar sesión desde la interfaz.",
      "Completar celular y alias. Pulsar Agregar.",
      "Observar el POST real: 201, alias y celular correctos.",
      "Ver una fila y favorito desactivado. Recargar: una fila y contador 1 de 15."
    ],
    "why": "cy.intercept observa la petición sin simular su respuesta. La recarga comprueba que la UI recupera el contacto guardado.",
    "command": "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 open",
    "link": "../../cypress/e2e/contactos-happy-path.cy.ts",
    "action": "Ver el test completo"
  },
  {
    "title": "IA aplicada al mismo flujo",
    "label": "06 / cy.prompt en vivo",
    "body": "Cuatro instrucciones en lenguaje natural guían la interacción con el formulario.",
    "code": "Type {{phone}} in the input labeled Celular inside Agregar contacto\nType {{alias}} in the input labeled Alias\nClick the button labeled Agregar\nVerify that the text \"Contacto IA\" is visible in the list under \"Mis contactos\"",
    "items": [
      "La demo necesita sesión de Cypress Cloud y projectId configurado.",
      "Después de cy.prompt, el test exige 201 y vuelve a comprobar los datos tras recargar."
    ],
    "why": "Mostramos generación y ejecución de acciones. No declaramos haber probado self-healing.",
    "command": "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 ai-open",
    "link": "../../cypress/demos/contactos-ia.cy.ts",
    "action": "Ver prueba con IA"
  },
  {
    "title": "Qué demuestra el verde",
    "label": "07 / Lectura del resultado",
    "body": "Una prueba aprobada significa que sus aserciones se cumplieron en esa ejecución.",
    "rows": [
      [
        "Lo que aparece",
        "Qué significa"
      ],
      [
        "expected 201 to equal 201",
        "La respuesta coincide con el código esperado"
      ],
      [
        "have a length 1",
        "La consulta devuelve exactamente una fila de contacto"
      ],
      [
        "contain text Contacto IA",
        "La fila contiene el alias esperado"
      ],
      [
        "reload y nuevas aserciones",
        "La aplicación vuelve a mostrar los datos guardados"
      ]
    ],
    "why": "Un test verde no acredita todos los módulos ni todos los datos posibles. Hay que explicar qué se verificó.",
    "link": "#evidencia",
    "action": "Ver captura anterior identificada"
  },
  {
    "title": "Regresión y reporte nuevo",
    "label": "08 / Evidencia de esta sesión",
    "body": "Ejecutar los tres casos y abrir el HTML de esa ejecución.",
    "items": [
      "El happy path espera creación. Las pruebas negativas esperan rechazo.",
      "422 y 409 pueden aprobar: son respuestas esperadas para datos inválidos.",
      "Revisar fecha, nombres de casos, cantidades y aserciones en el reporte."
    ],
    "why": "El modo run genera los reportes. La ventana interactiva sirve para observar los pasos y depurar.",
    "command": "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 regression\npowershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report",
    "link": "#reportes",
    "action": "Consultar el último reporte local"
  },
  {
    "title": "Un fallo intencional",
    "label": "09 / Diagnóstico y evidencia",
    "body": "Creamos un contacto, pero la demo exige dos a propósito.",
    "code": "pagina.filas().should('have.length', 1)\n// Expectativa deliberadamente incorrecta\npagina.filas().should('have.length', 2)",
    "items": [
      "Esperado por el test: 2. Observado: 1.",
      "El comando termina con salida 1: esta demo debe fallar.",
      "En modo run se generan reporte y captura al fallar; revisar también el video."
    ],
    "why": "Esta aserción falsa permite explicar el diagnóstico. No constituye un defecto de Qolqe y está fuera de regresión y CI.",
    "command": "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 failure\npowershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 report",
    "link": "../../cypress/demos/evidencia-fallo.cy.ts",
    "action": "Ver el fallo didáctico"
  },
  {
    "title": "Lo que aprendimos",
    "label": "10 / Hallazgos y límites",
    "body": "La automatización requiere preparar el entorno y revisar las evidencias.",
    "items": [
      "Cloud necesitó sesión y projectId. El error era de configuración, antes de completar la IA.",
      "El placeholder en la verificación requirió el texto explícito “Contacto IA”.",
      "Los videos de specs aprobados se eliminan mediante after:spec. El HTML se conserva.",
      "GitHub Actions ejecuta la regresión en Electron. La IA y el fallo didáctico están separados."
    ],
    "why": "La evidencia sostiene el alcance de estos casos. La exposición debe distinguir fallos de entorno, del test y del producto.",
    "link": "https://github.com/granitespinoza/qolqe-g4-qa/actions",
    "action": "Ver ejecuciones de CI"
  }
];
