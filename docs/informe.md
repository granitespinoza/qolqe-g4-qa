# Informe — Parte 2 · G4 Contactos y solicitudes
Granit Espinoza y Franco · CS5383

Este informe cubre la Entrega 2 (secciones 1, 3 y 5). La sección 2 conserva el resultado de la Parte 1. Mapa de todo el repositorio: [mapa-del-repo.md](parte2/mapa-del-repo.md).

## 1. Alcance y decisiones
10 HU de G4 (18 criterios de aceptación) y el núcleo común solo como dependencia de esos flujos. Fuente de requisitos: https://github.com/cjudihtroj/qolqe-wallet, commit `8c7d2f0c939ede7765b7b80b98c10c3905693fda`. Qolqe no se modifica.
Herramientas: Karate (negocio, estados y efectos en la API), Schemathesis (contrato OpenAPI) y Cypress con TypeScript (E2E web). Cada herramienta aporta una capa distinta; ver [decisiones](decisiones.md).
Cobertura: **54 tests web** en 36 grupos de variantes para los 18 CA de G4, y **130 casos de API únicos** que producen 181 ejecuciones. La matriz [HU → CA → TC → resultado](../data/trazabilidad-parte2.csv) enlaza cada criterio con sus casos; un caso puede aparecer en varios criterios. No se declara cobertura total: el número de pruebas no mide por sí solo la cobertura de criterios.
Quality Gate **Escenario A**: aprueba solo si todo fallo es una firma conocida y documentada, sin causas nuevas ni intermitencia, en un entorno académico aislado con datos ficticios. No certifica la aplicación para producción. [Política](parte2/quality-gate.md).
Nivel: pruebas contra la aplicación FastAPI real con SQLite, sin mocks. FastAPI queda fijado en 0.117.1 y Starlette en 0.48.0: las versiones nuevas confirman el commit después de enviar la respuesta y producían lecturas inconsistentes.

## 2. Pruebas de API (resultado de la Parte 1, conservado)
[Diseño detallado por HU](diseno-pruebas.md). [Contrato original](../data/openapi-original.json).
Usuarios nuevos por escenario. Reloj global restablecido al comenzar. Ejecución secuencial porque cambiar el reloj afecta toda la aplicación; no se promete paralelismo seguro.
**Última generación de evidencia:** 2026-10-16T21:26:08-05:00.
**Karate, catálogo funcional inicial:** 116 ejecutados; 107 aprobados; 9 fallaron.
Las validaciones CT y variantes CF se presentan por separado en [resultados complementarios](resultados-complementarios.md) y [matriz revisada de Contactos](cobertura-tecnica-contactos.md). La suite completa incluye ambos conjuntos.
El contraste entre requisitos, OpenAPI e implementación se conserva en [documentación frente a código](contraste-documentacion-codigo.md).
Los fallos adicionales de efectos inmediatos y la preparación se analizan con fecha y evidencia en [incidencia de consistencia](incidencia-consistencia.md). No se convierten automáticamente en defectos independientes.
Reporte bruto de esta ejecución: `reports/raw/karate/20261017T022208Z-161b94/karate-summary.html`. Registros redactados: [evidencias](../evidencias/).
El número de escenarios aprobados no mide cobertura de criterios ni ausencia de defectos. Cada reporte queda vinculado con commit, huellas de fuentes e inicio/fin de su ejecución; se rechazan resultados desactualizados.
[Schemathesis y límites de la ejecución](revision-contrato.md).

## 3. Pruebas web y CI/CD
**Diseño web.** Cypress con Page Object y comandos propios: los selectores `data-testid` viven en `Web/cypress/pages/`, la preparación de usuarios ficticios en `support/` y las aserciones del negocio en cada test. No hay esperas fijas: se usan los reintentos de consultas y aserciones de Cypress. Cada escenario crea sus propios usuarios y corre sobre una base SQLite exclusiva (puerto 8011). `cy.intercept` solo observa las peticiones reales. Ver [`tests/e2e/README.md`](../tests/e2e/README.md).
**Estabilidad.** La suite se ejecutó tres veces con el mismo resultado: 45 aprobados y 9 fallos conocidos, sin omitidos ni intermitencia. [Verificación web](parte2/verificacion-web.md).
**Pipeline.** `.github/workflows/pruebas.yml` ejecuta API (Karate y Schemathesis), luego Web (tres corridas) y luego Reportería, en push o PR a `main` y manualmente. No usa `continue-on-error` ni omite pruebas; los reportes crudos conservan los FAIL y los artefactos duran siete días. [Pipeline](parte2/pipeline.md).
**Estado del pipeline.** El último run remoto de `main` revisado (41131622090, 30 de octubre) terminó en fallo; la causa y su tratamiento están en [pipeline](parte2/pipeline.md) y [defectos conocidos](parte2/defectos-conocidos.md). Los workflows anteriores (`api.yml`, `cypress.yml`) siguen en el repositorio y corresponden al flujo previo a la política del gate.
**Gestión de casos.** La trazabilidad HU → caso → ejecución se registra en [`data/trazabilidad-parte2.csv`](../data/trazabilidad-parte2.csv) y [`data/trazabilidad-parte2.json`](../data/trazabilidad-parte2.json), con estado en el pipeline y defecto asociado por caso. Vista legible: [trazabilidad](parte2/trazabilidad.md) y [presentación web](../apidoc/parte2/index.html).

## 4. Rendimiento
Pendiente de Parte 3; no se realizó prueba de carga contra servicios públicos.

## 5. Defectos encontrados
Ocho defectos conocidos, cada uno con casos, esperado y observado, y su severidad en el producto. Detalle y reproducción en [defectos-conocidos.md](parte2/defectos-conocidos.md).

| ID | Defecto | Severidad | Casos |
|---|---|---|---|
| D-01 | Alias con ñ rechazado: esperado 201/200, obtenido 422 | Media | G4-004, CF-01, E2E-G4-102, E2E-G4-113 |
| D-02 | Alias duplicado por espacios permitido: esperado 409 | Media | G4-018, CF-03, E2E-G4-104, E2E-G4-115 |
| D-03 | Se acepta una solicitud vencida: esperado 409, obtenido 200 | Alta | G4-053, G4-054, E2E-G4-324 |
| D-04 | Token válido después de cerrar sesión: esperado 401 | Crítica | G4-074 |
| D-05 | Transferencias simultáneas superan saldo o límite diario | Crítica | G4-116 |
| D-06 | Favorito acepta texto o entero: esperado 422 | Media | CT-02 |
| D-07 | El historial omite el último día | Alta | E2E-G4-117, E2E-G4-201, E2E-G4-202 |
| D-08 | Transferencia a una cuenta cerrada permitida | Alta | E2E-G4-206 |

No se modificó Qolqe ni se ajustaron expectativas para ocultar fallos. La admisión de estos fallos en el gate se limita a esta evaluación académica aislada y no resta severidad al producto.

## 6. Conclusiones y recomendaciones
La suite inicial permite defender técnicas y reproducir fallos. Completar los pendientes por CA antes de afirmar cobertura total o crear el tag de entrega `parte-1`.
La documentación HTML ayuda a localizar pruebas; el análisis se conserva en este informe y el diseño.
