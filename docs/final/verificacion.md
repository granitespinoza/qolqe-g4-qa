# Verificación de la entrega final

Ejecuciones locales identificadas por run y hashes de fuentes. Se realizaron antes del commit de consolidación y registran `worktree_dirty=true`; no se atribuyen falsamente al contenido limpio de su commit base. La validación de la revisión publicada se consulta en Actions.

| Comprobación | Resultado local |
|---|---|
| Diseño API G4 y núcleo | 51 criterios, 116 casos base + 5 complementarios + 15 técnicos: 136 IDs |
| Karate | 187 escenarios/variantes: 175 PASS y 12 FAIL conocidos; gate A aprobado |
| Schemathesis | 562 interacciones, 27 señales conocidas y 0 desconocidas; gate A aprobado |
| Web Gherkin | 60 escenarios × 3 corridas completas, con las mismas fuentes y entorno |
| Cada corrida web | 51 PASS / 9 FAIL conocidos, 0 omitidos, 0 intermitentes; gate A aprobado |
| Evidencia web | 180 capturas, vídeos desactivados |
| Kiwi TCMS local | 196 casos, cuatro corridas y 316 ejecuciones; estados leídos de nuevo y comparados con el payload |
| Rendimiento | Tres experimentos históricos verificados; se conservan incumplimientos de carga y estrés |
| Producto Qolqe | Referencia original sin modificar |

API: `20261119T181613Z-d95321`. Contrato: `20261119T181336Z-7b77c5`. Web: `stability-2026-11-20T01-14-36-285Z` (19 de noviembre en Lima). Las tres corridas completas reemplazan la secuencia interrumpida anterior como evidencia vigente; no se convirtió la interrupción en defecto tolerado.

## Diferencia entre escenarios y casos de gestión

Karate ejecuta 187 escenarios/variantes. Kiwi los agrupa en 136 casos: 127 PASSED y 9 FAILED. Las 12 variantes fallidas pertenecen a nueve casos; los comentarios conservan el detalle de cada variante. Web registra 60 casos por corrida: 51 PASSED y 9 FAILED. En total hay 196 casos distintos y 316 ejecuciones de casos, conservadas en cuatro corridas.

No hay contradicción entre esos recuentos: se cuentan unidades diferentes. Las 27 señales de Schemathesis se muestran por separado; no se convierten en 27 defectos únicos ni se suman como casos funcionales.

## Alcance de la aprobación

El gate académico aprueba el Escenario A con firmas conocidas exactas y datos aislados. Los fallos continúan siendo FAIL y no representan aptitud productiva. Las tres corridas son consistentes; no son tres ejecuciones 60/60 aprobadas.

Kiwi funciona en esta laptop con TLS verificado por el cliente. Un runner hospedado de GitHub necesita una instancia accesible para sincronizar automáticamente; la exportación del payload y el historial no dependen de esa conectividad. Antes de exponer se prepara la confianza del certificado local en el navegador y se abre el plan.

La demo cy.prompt pasó 1/1 en `2026-11-20T01-50-32-126Z-ai`; se mantiene separada de la regresión por su autenticación Cloud. La asistencia de IA en el diseño del núcleo cuenta con seis escenarios comprobados contra el producto real.

[Resumen verificable](../../data/final-verificacion.json) · [Guía de demo](ejecucion.md) · [Actions del repositorio](https://github.com/granitespinoza/qolqe-g4-qa/actions)
