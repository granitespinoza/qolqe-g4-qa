> Registro histórico de etapas previas. Estado y criterio actuales: [Quality Gate Escenario A](quality-gate.md) y [guía final](entrega.md). La aplicación permanece intacta.

# Verificación de pasos 1 y 2

Verificado: 2026-10-29T22:32:46.571427+00:00. Rama: `codex/parte2-alcance-api`. No se realizó commit ni push.

## Paso 1 — listo

- 18 criterios G4 contrastados con la fuente: 2 parciales y 16 pendientes en web.
- 3 tests web existentes referenciados, sin contarlos como cobertura completa.
- 36 grupos de variantes web diseñados, aún sin implementar (paso 3).
- Matriz JSON y Markdown regenerables, referencias a casos/API/archivos verificadas.

## Paso 2 — implementación y diagnóstico verificados

- Entorno nuevo instalado desde el lock; `pip freeze` coincide y `pip check` pasa.
- API y Cypress comparten dependencias fijadas. El workflow API instala ese mismo lock.
- Base y plantilla exclusivas por cada ejecución con `--start-api`; referencia original intacta.
- Manifiestos con versión QA/SUT, entorno, dependencias y hashes.
- Clasificación estricta de fallos, sin exclusiones ni cambio de expectativas.
- Ocho pruebas del diagnóstico aprobadas; matriz verificada y sintaxis de scripts revisada.

| Evidencia | Resultado |
|---|---|
| Karate inicial, entorno previo | 181: 169 aprobados, 12 fallidos |
| Karate final, entorno limpio y base aislada | 181: 169 aprobados, 12 fallidos |
| Fallos conocidos / nuevos sin clasificar | 12 / 0 |
| Fallos de preparación Background | 0 |
| Schemathesis | 562 interacciones; 4 fallos JUnit; 0 errores JUnit |
| Controles contextuales Schemathesis | 9/9 con respuesta 2xx |

Karate final: `20261029T221847Z-373ae7`. Schemathesis final: `20261029T223124Z-2fed46`. Ambos conservaron código de salida 1 y 1, respectivamente.

## Fallos de Karate en la verificación final

| Caso / variante | Problema | Escenario |
|---|---|---|
| CF-01 (línea 30) | D-01 | Editar alias válido en límites y clases permitidas |
| CF-03 (línea 62) | D-02 | Editar alias duplicado tras normalizar |
| CT-02 (línea 67) | D-06 | PUT rechaza favorito texto true sin modificar contacto |
| CT-02 (línea 68) | D-06 | PUT rechaza favorito texto false sin modificar contacto |
| CT-02 (línea 69) | D-06 | PUT rechaza favorito entero uno sin modificar contacto |
| CT-02 (línea 70) | D-06 | PUT rechaza favorito entero cero sin modificar contacto |
| G4-004 (línea 52) | D-01 | Crear contacto con alias 'Niño' |
| G4-018 (línea 187) | D-02 | Alias duplicado tras normalizar ' Ana ' |
| G4-053 (línea 82) | D-03 | Aceptar a los 2880 minutos |
| G4-054 (línea 97) | D-03 | Aceptar a los 2881 minutos |
| G4-074 (línea 22) | D-04 | Cerrar sesión revoca solo ese token |
| G4-116 (línea 80) | D-05 | Concurrencia conserva saldo y límite diario |

Los detalles y causas están en [diagnóstico API](diagnostico-api.md). Schemathesis produce señales de contrato/generación; no se cuentan automáticamente como cuatro defectos funcionales.

## Abrir la evidencia local

Desde la raíz del repositorio:

```powershell
./.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

- [Karate final](http://localhost:8765/reports/raw/karate/20261029T221847Z-373ae7/karate-summary.html).
- [Schemathesis final](http://localhost:8765/reports/raw/schemathesis/20261029T223124Z-2fed46/schemathesis-detallado.html).
- [Matriz de alcance](alcance-y-matriz.md).
- [Resumen versionable](../../data/parte2-verificacion.json), sin tokens ni cuerpos HTTP brutos.

Los reportes completos están en `reports/raw/` y no se suben a Git. El resumen sí conserva los resultados y sus identificadores. Los informes HTML históricos versionados se mantienen como archivo; no sustituyen los enlaces de esta ejecución.

## Qué sigue pendiente

La API **no está en verde**: quedan defectos del SUT y señales de contrato documentadas. La instalación limpia no los corrige. No hay nueva validación Linux/GitHub de esta rama. Las ejecuciones locales tienen cambios sin commit registrados en el manifiesto.

El siguiente trabajo aprobado por separado será el paso 3 (ampliar Cypress); después, tres ejecuciones de estabilidad web, pipeline integrado, trazabilidad a resultados y exposición. No se adelantaron esos pasos ni se modificó Qolqe para forzar un aprobado.
