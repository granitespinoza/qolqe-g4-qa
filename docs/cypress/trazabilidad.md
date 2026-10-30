# Alcance y trazabilidad de Cypress

> Parte 2: [matriz G4 actual y backlog web](../parte2/alcance-y-matriz.md). Esta página conserva el alcance anterior. [Implementación y resultados actuales de pasos 3–4](../parte2/verificacion-web.md); presencia de pruebas no implica aprobación.

Fuente normativa: `referencias/qolqe-wallet/docs/requisitos.md`, revisión `8c7d2f0c939ede7765b7b80b98c10c3905693fda`.

| Caso | Requisito | Datos y técnica | Oráculo | Prioridad |
|---|---|---|---|---|
| E2E-G4-001 | HU-G4-01 CA1, R-G4-01/02/03; visualización parcial HU-G4-02 CA3 | Dos usuarios activos propios, alias Ana Cypress, lista inicialmente vacía. Partición válida. | POST 201, alias y celular correctos, favorito false, una fila persistente tras recargar. | Smoke alta |
| E2E-G4-002 | HU-G4-01 CA1, R-G4-02 | Alias Lu, longitud 2, justo debajo del mínimo 3. | 422 ALIAS_INVALIDO, error visible, cero contactos después de recargar. | Regresión |
| E2E-G4-003 | HU-G4-01 CA1, R-G4-01 | Mismo celular registrado dos veces con distinto alias. | 409 CONTACTO_EXISTENTE, error visible, una sola fila y alias original persistente. | Regresión |

El caso E2E-G4-001 complementa G4-001 de Karate: comprueba también botones, formulario, mensajes y persistencia observable. No sustituye las pruebas de API.

No se declara cobertura completa de CA1: quedan fuera celular propio/inactivo, límite 15, todos los límites del alias, unicidad del alias y otras particiones. Tampoco se cubre todo HU-G4-02 (orden, paginación, búsqueda ni nombre enmascarado).

La preparación por API registra datos ficticios propios. El login y la creación evaluada ocurren en la UI. `cy.intercept` solo observa y no devuelve respuestas simuladas. Cada prueba puede ejecutarse sola. No hay reintentos de tests ni `wait(ms)` para sincronizar la interfaz.

Las demos de IA y fallo didáctico están fuera de la regresión. Una captura de fallo provocada no representa un defecto de Qolqe.
