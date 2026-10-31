# Resultado del Quality Gate en CI

Decisión del run remoto de `main`: [run 41152595167](https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/41152595167), commit `8ee107e`. Los tres jobs terminaron en éxito: API y contratos, Web E2E con tres corridas, y Reportería.

![Quality Gate Escenario A](img/gate.svg)

**Decisión: Escenario A, aprobado.** Las pruebas conservan sus PASS y FAIL originales. El Escenario A admite únicamente firmas conocidas y documentadas, en una instancia académica aislada. No certifica el producto para producción.

| Herramienta | Gate | PASS | Known issue | Desconocido | Flaky |
|---|---|---:|---:|---:|---:|
| Karate | A | 169 | 12 | 0 | 0 |
| Schemathesis | A | — | 27 | 0 | 0 |
| Web (Cypress, tres corridas) | A | 45 | 9 | 0 | 0 |

Bloqueos: ninguno. En Schemathesis se clasifican ocurrencias de checks fallidos; no son el total de interacciones ni casos funcionales únicos. No debe leerse como 54 pruebas web aprobadas: 9 fallan por defectos conocidos del producto, que se conservan visibles.

## Qué se corrigió para llegar aquí

- **Firma de contrato K-C03:** el generador interpreta `\d` como dígito Unicode y Qolqe valida solo ASCII; el cuerpo aleatorio variaba entre plataformas con la misma semilla. Se agrupa por causa y se conservan operación, check, estado, respuesta y fase.
- **Zona horaria del navegador:** el job Web fija `TZ: America/Lima`, porque Qolqe valida con hora de Lima y un runner en UTC enviaba una fecha futura entre las 00:00 y las 05:00 UTC. Ver [pipeline](pipeline.md).

Política y reglas: [quality-gate.md](quality-gate.md). Defectos: [defectos-conocidos.md](defectos-conocidos.md). Trazabilidad con el run: [trazabilidad.md](trazabilidad.md). El artefacto del run vence a los 7 días; esta página conserva el resumen.
