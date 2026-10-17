window.QA_PRESENTATION = [
  {
    "title": "Por qué Karate",
    "subtitle": "1 · Herramienta",
    "body": "Peticiones, preparación y aserciones en archivos .feature.",
    "items": [
      "Ejecutamos por HU o caso mediante tags.",
      "Menos código HTTP que con pytest-bdd; requiere Java."
    ],
    "why": "Concentramos las pruebas versionadas en un solo formato. Postman también permite automatizar.",
    "show": "Ver decisiones",
    "link": "#decisiones"
  },
  {
    "title": "Alcance G4",
    "subtitle": "2 · Funcionalidad",
    "body": "Contactos y solicitudes de dinero.",
    "items": [
      "Contactos: agregar, buscar, editar, eliminar y transferir.",
      "Solicitudes: crear, consultar, aceptar, rechazar y cancelar.",
      "Incluimos el núcleo común: usuarios, autenticación, cuenta y transferencias."
    ],
    "why": "Los flujos de G4 dependen del núcleo común.",
    "show": "Ver historias",
    "link": "#historias"
  },
  {
    "title": "HU-G4-01 · Agregar un contacto",
    "subtitle": "3 · Criterio de aceptación CA1",
    "body": "Ingresar celular y alias; aplicar R-G4-01 a R-G4-03.",
    "items": [
      "Celular registrado, activo, ajeno y no repetido; cerrado equivale a no registrado.",
      "Alias: recortar espacios; 3–20 caracteres; letras, tildes, ñ, números y espacios; único sin distinguir mayúsculas.",
      "Máximo 15 contactos y 5 favoritos; favoritos se evalúa al editar."
    ],
    "why": "CA1 reúne varias condiciones: cada una necesita casos.",
    "show": "Ver CA1, reglas y errores originales",
    "link": "../referencias/qolqe-wallet/docs/requisitos.md"
  },
  {
    "title": "Regla → técnica → casos",
    "subtitle": "4 · Diseño de HU-G4-01",
    "body": "Variamos una condición y mantenemos válidas las demás.",
    "rows": [
      [
        "Condición",
        "Técnica / datos",
        "Casos"
      ],
      [
        "Longitud del alias",
        "Valores límite: 2, 3, 20, 21",
        "G4-001, 002, 007, 008"
      ],
      [
        "Caracteres y espacios",
        "Particiones: José, Niño, vacío, @",
        "G4-003 a 011"
      ],
      [
        "Celular",
        "Particiones: propio, cerrado, inválido, duplicado",
        "G4-012 a 016, 106"
      ],
      [
        "Unicidad del alias",
        "Particiones: ANA y « Ana »",
        "G4-017, 018"
      ],
      [
        "Capacidad",
        "Valores límite: contactos 15 y 16",
        "G4-019"
      ]
    ],
    "why": "Probamos fronteras y clases con comportamientos distintos.",
    "show": "Ver casos y aserciones",
    "link": "#historias"
  },
  {
    "title": "Validaciones técnicas",
    "subtitle": "5 · Fuente: OpenAPI",
    "body": "Obligatoriedad, headers, tipos, longitudes, rangos y formatos.",
    "items": [
      "Schemathesis: mostrar petición, respuesta, metadatos y checks.",
      "Karate: casos CT explícitos para complementar la exploración."
    ],
    "why": "Un total de pruebas no demuestra qué restricción se validó.",
    "links": [
      {
        "label": "Ver detalle de Schemathesis",
        "href": "../reports/schemathesis-detallado.html"
      },
      {
        "label": "Ver matriz técnica",
        "href": "../docs/cobertura-tecnica-contactos.md"
      }
    ]
  },
  {
    "title": "Ejecutar toda la suite",
    "subtitle": "6 · Demo en vivo",
    "body": "Ejecutar → abrir el reporte nuevo → explicar los fallos.",
    "items": [
      "G4 + núcleo común + escenarios complementarios.",
      "Distinguir fallos de preparación y de aserción."
    ],
    "why": "El reporte debe corresponder a la ejecución de esta sesión.",
    "show": "Ver comandos",
    "link": "#ejecucion-vivo"
  },
  {
    "title": "G4-004 · Alias Niño",
    "subtitle": "7 · Resultado y fundamento",
    "case": "G4-004",
    "body": "Usuario autenticado, destinatario válido y lista con capacidad.",
    "expected": "201 · Contacto creado",
    "obtained": "Registro guardado: 422 · ALIAS_INVALIDO",
    "code": "* def r = add(b.cell, \"Niño\", a.token)\n* match r.statusCode == 201",
    "why": "R-G4-02 y OpenAPI permiten ñ. El rechazo contradice ambas fuentes.",
    "links": [
      {
        "label": "Ver petición y respuesta",
        "href": "../evidencias/G4-004.html"
      },
      {
        "label": "Ver contrato del alias",
        "href": "#post-api-contactos"
      }
    ]
  },
  {
    "title": "Otra HU por tag",
    "subtitle": "8 · Pregunta al azar",
    "body": "Ubicar CA y casos → justificar técnica → ejecutar el tag.",
    "items": [
      "HU: @HU-G4-02 · Caso: @G4-020.",
      "Abrir el reporte nuevo y revisar lo ejecutado."
    ],
    "why": "La etiqueta selecciona los escenarios asociados a la HU o al caso.",
    "show": "Elegir HU y copiar comando",
    "link": "#ejecucion-vivo"
  },
  {
    "title": "De 116 a 181 escenarios",
    "subtitle": "9 · Alcance y conteo",
    "body": "Catálogo inicial: 81 casos G4 + 35 del núcleo común = 116.",
    "rows": [
      [
        "Conjunto inicial",
        "Casos"
      ],
      [
        "Contactos y transferencia por contacto",
        "37"
      ],
      [
        "Solicitudes de dinero",
        "44"
      ],
      [
        "Núcleo común",
        "35"
      ]
    ],
    "items": [
      "65 añadidos = 53 técnicos + 12 funcionales.",
      "Karate: 116 + 65 = 181. Schemathesis se cuenta aparte."
    ],
    "why": "Cada HU requiere varias pruebas; cantidad no equivale a cobertura completa.",
    "links": [
      {
        "label": "Ver los 116 iniciales",
        "href": "#historias",
        "allCases": true
      },
      {
        "label": "Ver los 65 añadidos",
        "href": "#supplementary-results"
      },
      {
        "label": "Ver reporte total: 181",
        "report": true
      }
    ]
  },
  {
    "title": "Conclusiones",
    "subtitle": "10 · Lecciones aprendidas",
    "body": "El esperado sale de requisitos y contrato.",
    "items": [
      "Conservar y explicar los fallos; no cambiar aserciones para obtener verde.",
      "Registrar la preparación y reconocer los pendientes."
    ],
    "why": "Cada conclusión necesita una regla y evidencia.",
    "show": "Ver documentación frente a código",
    "link": "../docs/contraste-documentacion-codigo.md"
  }
];
