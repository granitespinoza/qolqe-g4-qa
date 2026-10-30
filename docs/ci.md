> Entrega actual: `.github/workflows/pruebas.yml`, API → Web → Reportería y Quality Gate Escenario A. Ver [guía vigente](parte2/quality-gate.md). Lo siguiente conserva contexto anterior.

> Actualización Parte 2: [pipeline API + web + Schemathesis](parte2/pipeline.md). La descripción siguiente conserva el contexto anterior.

# GitHub Actions — estado y archivo histórico

## Auditoría de Parte 2 — 29 de octubre de 2026

El [run de main 40909689674](https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/40909689674) terminó en fallo: Karate informó 169 aprobados y 12 fallidos; Schemathesis también falló. No se ha ejecutado en GitHub la rama de esta implementación.

Se fijaron dependencias compartidas y se añadieron aislamiento y diagnóstico local. Ver [análisis actual](parte2/diagnostico-api.md) y [verificación](parte2/verificacion.md). La integración del pipeline completo corresponde al paso 5. No confundir los conteos históricos siguientes con los actuales.

## Archivo histórico — 13 de octubre

Ejecución: https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/38351731828

Ambos jobs terminaron y conservaron artefactos. Su estado es fallo, no una aprobación de la suite.

| Ejecución | Resultado |
|---|---|
| Karate local | 116 escenarios: 110 aprobados, 6 fallos; 5 defectos funcionales reproducidos |
| Karate en GitHub Actions | 116 escenarios: 108 aprobados, 8 fallos |
| Schemathesis | Job ejecutado; fallos de conformidad y advertencias conservados en su artefacto |

## Diferencias pendientes de investigar
Además de los 6 fallos de aserción reproducidos localmente, CI presenta 2 fallos de preparación de usuarios: tras registrar una cuenta con 201, su login inmediato devolvió 401 CREDENCIALES_INVALIDAS. Aparecen en el contexto de HU-G4-06 y HU-N-04. No se cuentan automáticamente como dos nuevos defectos de esas HU.

Hipótesis a verificar: visibilidad de la escritura tras respuesta, porque la dependencia de base de datos confirma la transacción al finalizar. Es una hipótesis de análisis, no una causa raíz demostrada.

Los escenarios que fallan en preparación no prueban su comportamiento de negocio. No ocultamos esta diferencia ni reemplazamos expectativas para obtener un pipeline verde.

Los artefactos se retienen 7 días y su acceso depende de la visibilidad del repositorio. La evidencia local redactada y el resumen quedan versionados.
