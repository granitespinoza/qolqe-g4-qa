# Capacidad de IA y validación independiente

Incorporamos `cy.prompt` en `tests/e2e/demos/contactos-ia.cy.ts`. La IA interpreta instrucciones de interacción: completar celular/alias y agregar un contacto. Aporta generación de acciones sobre la UI a partir de lenguaje natural. No decide el criterio de aceptación, no cambia el producto y no clasifica automáticamente defectos para permitir el gate.

Validamos su resultado con oráculos deterministas: POST real responde 201; tras recargar hay un único contacto; coinciden alias y celular. Eso comprueba persistencia, no solamente que la IA hizo clic. Datos y actores son sintéticos y exclusivos.

La demo es independiente de la regresión y requiere sesión personal Cypress Cloud, proyecto válido y conectividad. No se presenta como ejecutada en cada pipeline ni como un respaldo determinista cuando el servicio no está disponible.

```powershell
$env:CYPRESS_PROJECT_ID = 'ID_REAL_DE_CYPRESS_CLOUD'
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/cypress.ps1 ai-open
```

Seleccionar el spec IA e iniciar sesión personalmente. Conservar reporte/resultado de esa ejecución. Si cy.prompt solicita aclaraciones o falla, mostrar el resultado real; no sustituirlo por un script manual afirmando que fue IA. Se documentan tanto sus beneficios como la dependencia externa, variabilidad y revisión necesaria.

## Asistencia de IA en el diseño de casos

Los seis casos nuevos de núcleo se prepararon con asistencia de Codex y se verificaron contra la aplicación real: 6/6 aprobados en la ejecución local `2026-11-19T18-02-30-052Z-smoke`, con seis capturas. Esto valida esos escenarios concretos; no demuestra que cy.prompt se haya ejecutado en esa corrida. La capacidad cy.prompt y la asistencia de diseño se distinguen explícitamente.

## Ejecución real comprobada

El run `2026-11-20T02-18-03-994Z-ai` ejecutó cy.prompt en Chrome con el proyecto Cloud del equipo: 1/1 aprobada, POST 201 y persistencia tras recargar. El [reporte](evidencias/ia/reporte.html), [captura](evidencias/ia/contacto-ia.png) y registro de ejecución se conservan junto al resumen `data/final-ia.json`. No es una ejecución IA del pipeline hospedado ni se afirma que haya una llamada nueva al modelo en cada corrida: Cypress puede reutilizar el código generado en caché.
