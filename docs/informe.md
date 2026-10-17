# Informe — Parte 1 · G4 Contactos
Granit Espinoza y Franco · CS5383

## 1. Alcance y decisiones
10 HU de G4 y 9 del núcleo. La suite inicial tiene 116 escenarios. No se declara cobertura total: consultar [cobertura por CA](cobertura.md).
Referencia: https://github.com/cjudihtroj/qolqe-wallet · commit `8c7d2f0c939ede7765b7b80b98c10c3905693fda`.
Karate verifica negocio, estados y efectos; Schemathesis explora el contrato. [Decisiones y alternativas](decisiones.md).
Nivel: pruebas HTTP contra la aplicación FastAPI real con SQLite, sin mocks. No representa integración con bancos reales.
[Usabilidad complementaria](usabilidad.md): plan de inspección heurística para la entrega web; no se declara evaluación de interfaz realizada.

## 2. Pruebas de API
[Diseño detallado por HU](diseno-pruebas.md). [Contrato original](../data/openapi-original.json).
Usuarios nuevos por escenario. Reloj global restablecido al comenzar. Ejecución secuencial porque cambiar el reloj afecta toda la aplicación; no se promete paralelismo seguro.
**Última generación de evidencia:** 2026-10-16T21:02:13-05:00.
**Karate, catálogo funcional inicial:** 116 ejecutados; 103 aprobados; 13 fallaron.
Las validaciones CT y variantes CF se presentan por separado en [resultados complementarios](resultados-complementarios.md) y [matriz revisada de Contactos](cobertura-tecnica-contactos.md). La suite completa incluye ambos conjuntos.
El contraste entre requisitos, OpenAPI e implementación se conserva en [documentación frente a código](contraste-documentacion-codigo.md).
Reporte bruto de esta ejecución: `reports/raw/karate/20261017T015949Z-a4941f/karate-summary.html`. Registros redactados: [evidencias](../evidencias/).
El número de escenarios aprobados no mide cobertura de criterios ni ausencia de defectos. Cada reporte queda vinculado con commit, huellas de fuentes e inicio/fin de su ejecución; se rechazan resultados desactualizados.
[Schemathesis y límites de la ejecución](revision-contrato.md).

## 3. Pruebas web y CI/CD
Workflow preparado en `.github/workflows/api.yml`, con jobs separados para Karate y contrato. Conserva los reportes aunque una prueba falle. El pipeline debe informar fallos reales.
E2E web pendiente de Parte 2.

## 4. Rendimiento
Pendiente de Parte 3; no se realizó prueba de carga contra servicios públicos.

## 5. Defectos encontrados
5 hallazgos funcionales con escenario y evidencia enlazados. [Reproducción](defectos.md).
No se modificó Qolqe ni se ocultaron errores con expectativas ajustadas a su comportamiento.

## 6. Conclusiones y recomendaciones
La suite inicial permite defender técnicas y reproducir fallos. Completar los pendientes por CA antes de afirmar cobertura total o crear el tag de entrega `parte-1`.
La documentación HTML ayuda a localizar pruebas; el análisis se conserva en este informe y el diseño.
