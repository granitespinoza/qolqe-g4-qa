# Qolqe G4 · Verificación de API y Web

Granit Espinoza y Franco · Pruebas y Verificación de Software.

Kit de pruebas para reproducir verificaciones de contactos y solicitudes de dinero en Qolqe. Schemathesis explora el contrato OpenAPI, Karate comprueba escenarios explícitos y Cypress verifica recorridos desde la interfaz. Los ejecutores preparan instancias de prueba y conservan evidencia; el ahorro de tiempo todavía no está medido.

## Revisar la entrega

| Necesito… | Entrada |
|---|---|
| Entender componentes y recorrido | [Arquitectura](docs/arquitectura.md) |
| Preparar el entorno y ejecutar | [Guía de ejecución](docs/ejecucion.md) |
| Revisar presentación, matriz y reportes | [Portal de la entrega](apidoc/parte2/index.html) |
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
