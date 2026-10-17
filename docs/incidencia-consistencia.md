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

## Preparación explícita para la demostración, autorizada posteriormente

Se conserva la API original, la versión del entorno y la ejecución fallida.
`features/support/setup.feature` incorpora una comprobación de disponibilidad
acotada; no presenta una transacción tardía como si hubiera sido inmediata:

- Registro: se hace **un solo POST** de creación. Si el login inmediato responde
  401 CREDENCIALES_INVALIDAS, se consulta otra vez con las mismas credenciales,
  hasta 20 intentos y con plazo de sondeo de 2segundos. Cualquier otro error
  corta la preparación inmediatamente.
- Contacto: se hace **un solo POST** y se conserva su respuesta original. Solo
  tras un 201 se consulta GET hasta que el id aparezca, revisando ambas páginas
  si procede. Nunca se repite el POST. Un error de consulta corta la preparación.
- Cada sondeo fallido registra `READINESS` en el reporte. Hay un intervalo
  explícito de 25ms entre sondeos cuando aún no está disponible; no se espera
  después de un éxito. No se inicia otro sondeo tras 20 observaciones o tras
  cumplir 2segundos, lo que ocurra primero; una petición ya iniciada conserva
  su tiempo de espera HTTP. El resumen de intentos se adjunta como JSON cuando hay
  más de uno o se agota el límite, sin registrar tokens.
- Al agotar el límite, la ejecución falla con `READINESS agotado`; no continúa
  con un contexto inválido. Las acciones funcionales bajo prueba (solicitar,
  aceptar, rechazar, cancelar, transferir, editar y eliminar) no se reintentan.
- Crear contacto también es una acción bajo prueba: el sondeo posterior no
  cambia su estado HTTP ni su JSON, ni sustituye las aserciones sobre ese retorno.
  La disponibilidad eventual queda visible y no se acredita como consistencia
  inmediata. Para medir la carrera original se conserva la evidencia anterior.

Este ajuste estabiliza las precondiciones de la demostración sin corregir el
defecto transaccional ni convertir la demora en un resultado funcional aprobado.
Una ejecución nueva debe distinguirse de la corrida previa, manteniendo todos
los fallos y adjuntos originales. No se modifican los esperados de ñ, duplicados,
vencimiento, revocación de token, concurrencia ni tipos de dato del contrato.

### Comprobación acotada del ajuste

Reporte local `reports/raw/readiness-contactos-20261016`: selección
`@G4-029,@G4-035,@CT-08,@CT-09`, **7 escenarios ejecutados, 7 aprobados**.
Incluye los casos de solicitud pendiente y monto0.00 que permiten comprobar
la secuencia de preparación, cuatro operaciones con JWT malformado y el alias
con símbolo al editar. En esta corrida los recursos estuvieron disponibles en
el primer sondeo: no se reprodujo la carrera ni se ejercitó un segundo intento.
Por tanto esta comprobación acredita el recorrido normal del ajuste, sin afirmar
que resuelve permanentemente la incidencia ni sustituir la ejecución completa.

### Segunda manifestación: token emitido con sesión aún no visible

La ejecución completa `20261017T021711Z-b99f4a` conservó **181 escenarios,
165 aprobados y16 fallidos**. En G4-046, después de avanzar el reloj, el login
de renovación devolvió200 y sesión4174 a las21:19:07.923. La consulta de
solicitudes a las21:19:07.932 devolvió401 NO_AUTENTICADO, con detalle «La sesión
fue cerrada». La aserción de estado encontró `#notpresent` porque el cuerpo era
un error de autenticación, no una lista de solicitudes vacía.

`usuario_actual`, en `qolqe/dependencias.py`, busca la sesión por `jti` y devuelve
ese401 si aún no existe. La secuencia es consistente con el mismo commit tardío,
esta vez en la inserción de una sesión recién emitida. No demuestra una regla
incorrecta de vencimiento de solicitudes.

Se añadió `features/support/session-ready.feature`, llamado tras el primer
login exitoso de `create` y después del único login de renovación del helper
`login(user)`. Consulta GET de saldo con **el token original**, sin volver a
emitirlo. Solo se repite ante401 NO_AUTENTICADO con el detalle exacto «La sesión
fue cerrada». Cualquier otro error detiene la preparación. Conserva el máximo
de20observaciones, plazo de2segundos, intervalos explícitos de25ms, mensajes
READINESS y adjuntoJSON si se necesitan varios intentos o se agota el plazo.

Este sondeo usa únicamente el estadoHTTP como comprobación de autenticación;
**no verifica ni espera un saldo concreto**. Las comprobaciones de saldo después
de una transferencia/aceptación, y de estado después de aceptar/cancelar, siguen
siendo aserciones directas. Los resultados inesperados de G4-049 o G4-102 no se
ocultan con una espera genérica: deben conservarse e investigarse como señales
de comportamiento/consistencia después de acciones reales.

Comprobación del soporte de sesión: `reports/raw/readiness-sesion-20261016`,
selección HU-G4-04 yHU-G4-07, **8 ejecutados, 8 aprobados**. En esta ejecución
se observaron dos situaciones de usuario recién registrado no autenticable en
el primer login: se registró un sondeo adicional y la preparación continuó al
obtener200. Las sesiones estuvieron disponibles en su primerGET protegido.
El resumen sin tokens queda en `reports/verificacion-readiness-sesion.json`.
Esta selección no sustituye la nueva suite completa ni acredita corregida la
consistencia transaccional de la aplicación.

## Última ejecución completa con preparación explícita

Ejecución `20261017T022208Z-161b94`: **181 escenarios, 166 aprobados, 15 fallidos y cero fallos de Background**. Se conserva la ejecución previa de 176 casos con seis fallos de preparación; no se reemplaza su evidencia raw. [Resumen y sondeos registrados](../reports/verificacion-final.json).

Los 15 fallos no equivalen a 15 defectos. Doce reproducen los fallos conocidos (incluidas variantes de edición y cuatro entradas para una discrepancia de booleanos). Otros tres comprueban efectos inmediatamente posteriores:

| Caso | Esperado | Observado en esta ejecución |
|---|---|---|
| [G4-015](../evidencias/G4-015.html) | Después de cerrar la cuenta con204, agregar ese destinatario debe devolver404 | El alta inmediata devolvió201 |
| [G4-093](../evidencias/G4-093.html) | Login desde dispositivo nuevo devuelve200 y genera aviso | La consulta inmediata de notificaciones no contenía el aviso |
| [G4-080](../evidencias/G4-080.html) | Tras cerrar la cuenta con204, el token no permite consultar saldo | La consulta inmediata devolvió200 |

Son fallos de aserción observados, compatibles con la incidencia de commit tardío explicada arriba. La causa compartida sigue siendo una inferencia respaldada por código y trazas, no tres defectos independientes confirmados. No se añadieron esperas para hacer aprobar esos efectos ni se cambiaron sus esperados. Requieren reproducción aislada y comparación temporal para cerrar el diagnóstico. No confundir que las precondiciones estén listas con haber corregido la implementación.
