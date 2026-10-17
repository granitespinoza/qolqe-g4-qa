# Incidencia de consistencia observada al ejecutar la suite completa

## Evidencia de la ejecución

Ejecución `20261017T015949Z-a4941f` (16 de octubre en Lima), entorno local
FastAPI **0.143.0**. El proyecto original permite `fastapi>=0.115,<1.0`.
No se modificó el código de la aplicación original para investigar esta señal.

Seis escenarios fallaron durante la preparación, al autenticar un usuario recién
creado: G4-029, G4-034, G4-098, G4-110, G4-111 y G4-072.
Esto impide evaluar la regla funcional de esos seis casos en esta ejecución;
no deben contarse como seis defectos de sus respectivas HU.

Ejemplo de `features.hu-g4-04.karate-json.txt` en el directorio raw de la ejecución:

| Momento local | Petición | Resultado |
|---|---|---|
| 21:01:17.974 → 21:01:18.054 | Registro de usuario sintético propio con PIN 4826 | 201, devuelve id3559 |
| 21:01:18.054 → 21:01:18.067 | Login del mismo celular con el mismo PIN | 401 CREDENCIALES_INVALIDAS |

Otra manifestación aparece en **G4-035** (monto 0.00, no G4-036):

| Momento local | Petición | Resultado |
|---|---|---|
| 21:01:22.360 → 21:01:22.366 | Crear contacto propio | 201, devuelve id886 |
| 21:01:22.367 → 21:01:22.367 | Crear solicitud para contacto886 con monto0.00 | 404 CONTACTO_NO_ENCONTRADO |

El esperado funcional de G4-035 sigue siendo 422 SOLICITUD_INVALIDA. El 404
indica que la API aún no encuentra el contacto que acaba de confirmar; no
demuestra que la regla monetaria acepte un monto inválido.

## Explicación respaldada por el código local

1. `qolqe/bd.py`, función `obtener_bd`, abre una conexión y hace `yield`; el
   `commit()` se ejecuta al finalizar la dependencia, después del `yield`.
2. Los endpoints de registro y contactos utilizan `Depends(obtener_bd)` sin
   especificar alcance de función. Devuelven sus objetos antes del commit.
3. En FastAPI0.143.0 instalado, `dependencies/models.py`, función
   `_get_computed_scope`, asigna alcance `request` a dependencias generadoras
   sin alcance explícito.
4. En `fastapi/routing.py`, `request_response`, la llamada
   `await response(scope, receive, send)` queda dentro de `request_stack`.
   La salida y limpieza de ese stack ocurren después de enviar la respuesta.
5. El cliente puede por tanto recibir 201 y emitir la siguiente petición antes
   de que la transacción anterior se haya confirmado. Una conexión SQLite
   distinta todavía no ve el usuario/contacto.

Es una **explicación causal fuertemente respaldada por trazas y código**, no un
experimento aislado adicional: durante la investigación no se ejecutaron nuevas
peticiones para evitar interferir con otra herramienta usando el entorno.

## Cómo tratarlo sin maquillar la ejecución

- Conservar el resultado original y separar fallos de preparación, discrepancias
  funcionales y discrepancias técnicas de contrato.
- No cambiar el esperado del caso monetario a 404 ni añadir esperas o reintentos
  ocultos para presentar una suite más verde.
- Si se modifica el entorno para estabilizar la demostración (por ejemplo,
  fijando una versión compatible de dependencias), registrar versión exacta,
  motivo y una ejecución nueva; comparar sin borrar esta evidencia.
- Una corrección permanente corresponde a confirmar los cambios antes de
  reconocerlos como exitosos. Debe proponerse al proyecto original y verificarse
  aparte; esta revisión no aplica esa corrección sobre el código ajeno.
