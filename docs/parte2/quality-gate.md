# Quality Gate — Escenario A

Se aplica la indicación docente: Qolqe original no se corrige; los fallos funcionales se ejecutan y se reportan. Una excepción conocida puede aprobar el gate de la evaluación académica si está documentada, admitida y no hay causas nuevas ni inestabilidad. Esto no certifica la aplicación para producción.

## Decisión

| Resultado | Gate |
|---|---|
| Pruebas completas sin fallos | Aprueba, 100% exitoso |
| Solo firmas conocidas admitidas en instancia académica aislada | Aprueba, Escenario A |
| Mismo TC con una causa o respuesta diferente | Bloquea |
| Selector, autenticación, preparación, proceso o reporte inválido | Bloquea |
| Omisiones, suite incompleta, fuentes diferentes o intermitencia | Bloquea |

Los HTML y XML mantienen sus FAIL. El ejecutor conserva los códigos originales en `execution.json`; `scripts/ci_run.py` evalúa después la evidencia y devuelve el código del gate. No usa `continue-on-error`, `|| echo`, cambios de esperado ni tests desactivados.

## Firmas y controles

- API: referencia, fuentes normalizadas, escenario/fila, paso fallido, esperado/observado y tag `@known_issue`. No se tolera un fallo de Background.
- Web: spec, ID, tag, primera línea del error y fuentes; solo se normaliza el número de milisegundos que Cypress imprime al agotar sus sondeos, sin modificar selector, esperado ni observado. Tres corridas completas con los mismos tests y entorno; cualquier cambio PASS ↔ known issue/FAIL bloquea.
- Contrato: OpenAPI fijado, operación, método, ruta/query, check, estado, respuesta, fase y datos relevantes. Se revisaron 27 ocurrencias. Únicamente el texto aleatorio de un alias inválido se agrupa por clase en el perfil de prioridad `CONTACTO_EXISTENTE` 409; un alias válido, otro estado o respuesta no coincide. El resto conserva huellas de petición/respuesta concretas. Una firma nueva bloquea.
- Reportería: gates del mismo run, commit y política. La evidencia vieja no se acepta como nueva. Un resultado de prueba exitoso no se convierte artificialmente en fallo conocido.
- Contexto: base exclusiva, Qolqe en modo prueba y referencia sin cambios. Los tests no apuntan a cuentas o fondos reales.

Catálogo versionado: `data/quality-policy.json`. Riesgos, pasos, casos y justificación: [defectos-conocidos.md](defectos-conocidos.md). Los riesgos del producto conservan su severidad alta o crítica cuando corresponde. La admisión del equipo se limita a esta evaluación aislada y no pretende una aprobación individual adicional de la docente.

## Estabilidad y dependencias

El rango original admite FastAPI `>=0.115,<1.0`. Se fija FastAPI **0.117.1** y Starlette **0.48.0** en el lock común. No se modifica ninguna línea de Qolqe.

FastAPI cambió desde 0.118 el momento en que ejecuta el cierre de dependencias con `yield`: en la configuración por defecto actual ocurre después de enviar la respuesta. Qolqe confirma el commit al cerrar esa dependencia. Por tanto, la actualización automática de FastAPI podía hacer que el cliente leyera antes del commit. La versión fijada mantiene el cierre antes de responder y eliminó las intermitencias observadas en las tres nuevas corridas. [Explicación oficial](https://fastapi.tiangolo.com/advanced/advanced-dependencies/).

Se validaron tres corridas con **45 PASS y 9 FAIL conocidos en cada una**, cero omitidas y cero flakiness detectada. La API completa dio **169 PASS y 12 fallos conocidos**, con cero fallos de Background. Schemathesis conservó **562 interacciones, 27 ocurrencias revisadas y 9 controles contextuales exitosos**. Una segunda ejecución independiente comprobó la clasificación del contrato.

`stability` sigue devolviendo fallo por los FAIL crudos. `quality_gate.py web` aprueba únicamente cuando cumplen Escenario A. No se presenta esto como 54 pruebas PASS.

## Comandos

Desde la raíz, con `.venv` y Node 24 ya disponibles:

```powershell
.venv/Scripts/python.exe scripts/ci_run.py api
.venv/Scripts/python.exe scripts/ci_run.py web
.venv/Scripts/python.exe scripts/build_web_coverage.py
.venv/Scripts/python.exe scripts/ci_run.py reporting
.venv/Scripts/python.exe scripts/build_delivery.py
```

Para revisar solo la evidencia existente, sin volver a ejecutar suites:

```powershell
.venv/Scripts/python.exe scripts/quality_gate.py karate
.venv/Scripts/python.exe scripts/quality_gate.py schemathesis
.venv/Scripts/python.exe scripts/quality_gate.py web
.venv/Scripts/python.exe scripts/ci_run.py reporting
```

La decisión se guarda en `reports/gate/overall.json` y `reports/gate/resumen.md`. Los reportes crudos y los gates se publican en el artefacto de la misma ejecución de GitHub. La matriz muestra tanto el estado de prueba como el defecto asociado.

Resultado del run remoto de `main`: [resultado-gate.md](resultado-gate.md).
