# Verificación de la entrega final

## Alcance vigente

- API: 51 criterios del núcleo y G4; 136 IDs (116 base, cinco complementarios y 15 técnicos), expandidos en 187 escenarios/variantes.
- Web: 65 escenarios .feature; 54 de G4 y 11 del núcleo. Hay escenarios vinculados a las nueve HU comunes.
- El auditor rechaza un núcleo sin alguna de sus HU y los gates requieren tres corridas completas con la misma selección, fuentes y entorno.
- Qolqe permanece en su referencia original, sin modificaciones del producto.

## Evidencias y unidades

La ejecución vigente se consulta en el Summary y el artefacto del commit publicado en [Actions](https://github.com/granitespinoza/qolqe-g4-qa/actions). Allí se publican los estados crudos, defectos, repeticiones y variantes. No se atribuyen automáticamente a un commit nuevo las métricas de una corrida anterior.

Antes de ampliar el núcleo se verificaron tres corridas locales de 60 escenarios (51 PASS y nueve FAIL conocidos cada una), 180 capturas y una importación Kiwi de 196 casos y 316 ejecuciones. Se conservan como snapshot histórico en `data/final-verificacion.json`. La ampliación incorpora cierre de sesión/cuenta y transferencias/simulación; la estabilidad del alcance final de 65 se verifica en el workflow vigente.

El núcleo ampliado se ejecutó localmente: diez PASS y un FAIL por el defecto D-04 de revocación tras logout. La falla de sincronización inicial del formulario se corrigió en la automatización mediante una espera de red. No se convirtió en excepción del producto.

Karate publica variantes, mientras Kiwi agrega por ID/versión de caso. En el snapshot anterior, 12 variantes API fallidas correspondían a nueve casos; los comentarios conservaron todas sus variantes. Los casos de Schemathesis son señales de contrato y no se suman como defectos únicos.

## Condiciones de aprobación

El Escenario A admite solo firmas conocidas documentadas, con datos aislados; conserva los FAIL. Fallos nuevos, intermitencia, omisiones o preparación inválida bloquean. No certifica aptitud productiva ni significa que las 65 pruebas hayan pasado individualmente.

Kiwi local verifica TLS y lee de nuevo los estados importados. Un runner de GitHub requiere una instancia accesible para sincronizar directamente; el payload siempre puede importarse en la herramienta local. Su historial conserva las versiones y corridas previas.

La demo cy.prompt cuenta con evidencia real, validada mediante POST 201 y persistencia; requiere la sesión personal Cloud para repetirla. No se afirma ejecución IA nueva en cada pipeline.

[Guía de ejecución](ejecucion.md) · [Gestión de casos](gestion-casos.md) · [IA](ia.md)

## Organización final exigida

El informe principal está en `INFORME_FINAL.md`, los escenarios ejecutables en `features/e2e/`, Karate en `tests/api/features/`, Cypress en `tests/e2e/` y la exportación de 24 diapositivas en `presentacion/Entrega_Final_Qolqe.pdf`. La reorganización exige una nueva ejecución; los snapshots anteriores conservan su revisión y no se renombran como resultados nuevos. La demo IA se volvió a ejecutar después de mover las rutas: 1/1 aprobada.
