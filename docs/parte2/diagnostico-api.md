> Registro histórico de etapas previas. Estado y criterio actuales: [Quality Gate Escenario A](quality-gate.md) y [guía final](entrega.md). La aplicación permanece intacta.

# Diagnóstico API — Paso 2

La aplicación de referencia permanece en `8c7d2f0c939ede7765b7b80b98c10c3905693fda`, sin cambios. Los fallos siguen devolviendo código 1. Este trabajo mejora la reproducibilidad y clasifica evidencia; **no certifica un pipeline verde**.

## Reproducción y entorno

- Ejecución inicial completa: `20261029T163543Z-48b5c9`, 181 escenarios, 169 aprobados y 12 fallidos; cero fallos de Background.
- Coincide en cantidades con el [pipeline de main auditado](https://github.com/granitespinoza/qolqe-g4-qa/actions/runs/40909689674). La coincidencia de cantidades no prueba por sí sola identidad de todos los fallos remotos.
- El entorno nuevo `.tools/qa-step2-venv` se instaló desde cero con `requirements-lock.txt`; `pip check` pasó. Python local 3.13.3, Windows; GitHub está configurado con Python 3.12/Linux. Esa plataforma remota debe verificarse después de subir los cambios; no se declara equivalente solo por instalar el lock.
- API y Cypress utilizan el mismo lock: FastAPI 0.143.3, Starlette 1.8.0, Pydantic 2.14.1, Schemathesis 4.17.0, entre otras dependencias fijadas. La instalación previa de CI permitía actualizar FastAPI; no se atribuyen automáticamente a eso los fallos funcionales.
- `--start-api` crea base y plantilla nuevas en `.tools/api-runs/<id>/`, preserva el registro del servidor y rechaza un puerto 8000 ocupado. El servidor manual conserva su comportamiento previo.
- Nuevos manifiestos registran revisión QA, indicador de cambios sin commit, versiones instaladas, hashes del arnés, sistema operativo y URL de Actions cuando corresponda. Las ejecuciones locales de esta implementación indican árbol modificado: aún no son evidencia de un commit publicado.

## Karate: 12 fallos, seis problemas identificados

| ID | Casos / variantes | Esperado → observado | Diagnóstico |
|---|---|---|---|
| D-01 | G4-004, CF-01 fila Niño | Crear 201 / editar 200 → 422 | La expresión de alias en `qolqe/reglas/contactos.py` omite ñ/Ñ aunque R-G4-02 las permite. |
| D-02 | G4-018, CF-03 variante con espacios | 409 → 201 al crear / 200 al editar | La unicidad se comprueba antes de `strip()`, permitiendo duplicados normalizados. |
| D-03 | G4-053, G4-054 | 409 → 200 | Aceptar comprueba el estado almacenado y no el vencimiento calculado, a diferencia de rechazar/cancelar. |
| D-04 | G4-074 | 401 tras logout → 200 | Logout almacena el JTI; `usuario_actual` busca revocación usando el token completo. |
| D-05 | G4-116 | Invariantes monetarias verdaderas → falsas | La sonda concurrente detecta vulneración de saldo o límite. Revisar el adjunto `probe` para la variante concreta; no atribuir ambos fallos sin leerla. Las comprobaciones y escrituras no protegen conjuntamente el intervalo de concurrencia. |
| D-06 | CT-02: texto true/false y entero 1/0 | Rechazo de tipo 422 → 200 | El esquema anuncia booleano/null; Pydantic admite coerción de texto/número. Es una discrepancia de contrato técnico, separada de la regla funcional de favoritos. |

`data/api-known-failures.json` registra firmas revisadas: versión de referencia, hash del feature, escenario/fila y huella del error/paso. `scripts/diagnose_api.py` solo clasifica una coincidencia exacta. Un fallo distinto o de preparación permanece sin clasificar. **No elimina tests, no cambia aserciones y no convierte un defecto conocido en PASS.**

Un caso concurrente que pasa en otra ejecución no demuestra que el defecto esté corregido; se informa como no reproducido. Los fallos funcionales permanecen visibles.

## Schemathesis: señales, no cuatro defectos funcionales

Ejecución aislada `20261029T221607Z-81120f`: 9/69 operaciones seleccionadas (contactos y solicitudes), 562 interacciones, 27 ocurrencias de checks fallidos, agrupadas en 4 combinaciones operación/check y 4 fallos JUnit. Cero errores JUnit. Los nueve controles contextuales respondieron 2xx. Semilla 20261013, fases examples/coverage/fuzzing; stateful desactivado.

| Señal | Evidencia y conclusión |
|---|---|
| POST solicitudes / positive_data_acceptance | Mezcla causas: cuatro peticiones de Examples omitieron monto/motivo, aunque el esquema los declara obligatorios; una validación independiente de JSON Schema confirma que esos cuerpos son inválidos. Su 422 no demuestra un defecto funcional. Otras cuatro peticiones Fuzzing usan montos no numéricos, negativos o mayores al límite: el esquema admite string/number sin expresar todas las restricciones de negocio. Existe discrepancia entre generación/contrato y validación real. |
| POST contactos / negative_data_rejection | Alias demasiado largo con celular ya agregado devuelve 409 CONTACTO_EXISTENTE antes de validar alias. **409 es rechazo, no creación exitosa**; el nombre del check no debe interpretarse como que se guardó el dato inválido. Es una señal de prioridad de validaciones respecto de la expectativa del generador. |
| POST contactos / positive_data_acceptance | La generación interpreta el patrón `\d` con dígitos Unicode; la aplicación exige ASCII. Documentar la ambigüedad del patrón y del motor de regex. No confundirlo con el defecto de alias ñ. |
| GET solicitudes / positive_data_acceptance | El parámetro admite null en OpenAPI; el generador envía el texto `estado=null`, que la API rechaza con FILTRO_INVALIDO. Es una discrepancia de representación de null en query. |

Persisten dos advertencias del generador: datos inexistentes (404) y validación más restrictiva que los datos generados. Los controles reales complementan el fuzzing pero no hacen que cada petición aleatoria tenga un recurso válido. No se reescribieron datos aleatorios ni se retiraron checks para obtener verde.

## Política para el pipeline

En esta fase el criterio es estricto: cualquier suite fallida sigue en rojo. Las firmas conocidas son documentación y diagnóstico, no una lista de exclusiones. Para un futuro gate con defectos esperados se necesita acordar el tratamiento académico y hacerlo explícito; nunca usar `continue-on-error` global ni reemplazar 409 esperado por 200 observado. Si se exige ausencia absoluta de fallos, estos defectos del sistema/contrato deben corregirse en una versión autorizada de la referencia.

No se modificó el SUT, no se repitieron operaciones financieras para hacerlas pasar y no se presentó una ejecución local como un run remoto nuevo.

## Comandos

Desde PowerShell, dentro del repositorio; ejecutar las suites secuencialmente porque ambas usan el puerto 8000:

```powershell
./.venv/Scripts/python.exe -m pip install -r requirements-lock.txt
./.venv/Scripts/python.exe -m pip check
./.venv/Scripts/python.exe scripts/build_scope.py --check
./.venv/Scripts/python.exe scripts/run_qa.py karate --start-api
./.venv/Scripts/python.exe scripts/diagnose_api.py karate
./.venv/Scripts/python.exe scripts/run_qa.py schemathesis --start-api
./.venv/Scripts/python.exe scripts/diagnose_api.py schemathesis
./.venv/Scripts/python.exe -m unittest discover -s tests -p test_parte2_tools.py -v
```

Un código 1 del ejecutor/diagnóstico indica fallos reales conservados. No concatenar las suites con `&&` si se desea recopilar ambas evidencias. Los reportes HTML y el `diagnostico.json` se conservan dentro del directorio indicado por cada ejecución, bajo `reports/raw/` (ignorado por Git). El resumen redactado de esta revisión está en `data/parte2-verificacion.json`.
