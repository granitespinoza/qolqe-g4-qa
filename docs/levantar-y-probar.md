# Levantar Qolqe y mostrar las pruebas en vivo

Guía de Granit. Ejecuta los comandos en **PowerShell**, dentro de la carpeta del proyecto. No necesitas activar el entorno virtual: los comandos ya utilizan su Python.

## 1. Preparación inicial: una sola vez

Requisitos: Git, Python 3.12 e internet para descargar las dependencias. El preparador descarga Karate y Java 17 si hacen falta; conserva la aplicación original en `referencias/qolqe-wallet`.

```powershell
Set-Location 'C:\Users\LEGION\Documents\ChatGPT\proyecto de VyS'
./scripts/bootstrap.ps1
```

Si PowerShell indica que la ejecución de scripts está deshabilitada, ejecuta únicamente este preparador en un proceso con permiso temporal; no cambia la configuración permanente del equipo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ./scripts/bootstrap.ps1
```

Si ocurre un error de descarga o instalación, resuélvelo antes de continuar. No necesitas volver a generar los `.feature` para ejecutar las pruebas existentes.

## 2. Terminal 1: encender la API

```powershell
./.venv/Scripts/python.exe scripts/serve_api.py
```

Déjala abierta. Cuando indique que el servidor está disponible, abre **http://127.0.0.1:8000/docs**. Ahí ves Swagger y puedes consumir los endpoints. **http://127.0.0.1:8000/openapi.json** es el contrato que puedes guardar en JSON e importar en un cliente de API.

La aplicación usa una base local de pruebas en `.tools`; no es un servicio de producción. No ejecutes dos suites a la vez: comparten la API y el reloj de pruebas.

## 3. Terminal 2: encender el HTML y los reportes

Abre otra pestaña de PowerShell en la misma carpeta:

```powershell
./.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

Déjala abierta. Visita **http://localhost:8765/apidoc/#presentacion** para exponer; **http://localhost:8765/apidoc/#demostracion** contiene las capturas explicadas. El servidor de HTML permite abrir también los reportes recién generados por Karate.

## 4. Terminal 3: probar un caso y después una historia

Antes de la exposición, comprueba una ejecución pequeña:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@G4-001'
```

El comando debe ejecutar **un escenario**, no toda la suite. La consola muestra los aprobados, fallidos y un enlace al reporte. Abre ese enlace; entra al feature y despliega los pasos para enseñar la petición, respuesta y aserción. El reporte es la ejecución real; el HTML de presentación contiene evidencias de una ejecución identificada y no cambia automáticamente con cada demostración.

Para ejecutar una HU completa con todos los escenarios que tenemos asociados:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@HU-G4-01'
```

Si la docente elige la HU 5, cambia el tag:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@HU-G4-05'
```

Para mostrar el caso de alias «Niño», que reproduce un incumplimiento conocido:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@G4-004'
```

Esperamos creación `201` según el requisito. Si vuelve a obtener `422`, muestra el paso rojo y explica la diferencia; no cambies la aserción para obtener verde. Las etiquetas están escritas con `@` en los `.feature`: `@HU-G4-01` selecciona una historia y `@G4-004` un caso.

Para ver los tags disponibles por archivo, sin necesitar la API:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --list-tags
```

## 5. Separar funcionalidad y contrato técnico

Pruebas funcionales asignadas a G4, **contactos y solicitudes de dinero**:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --scope g4
```

Este alcance selecciona los archivos `hu-g4-*.feature`: no incluye las HU del núcleo común ni el feature técnico separado. `g4` no significa solamente el CRUD de contactos.

Validaciones explícitas del contrato de contactos (campos, tipos y restricciones), separadas de la técnica funcional:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@CONTRATO-CONTACTOS'
```

La evidencia de cada validación está en su escenario y aserciones. No digas «cubre todo OpenAPI» por el solo hecho de ejecutar este feature ni Schemathesis.

Suite completa del repositorio: G4, núcleo común y pruebas técnicas incluidas:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate
```

No mezcles estos tres totales: corresponden a alcances distintos. La cobertura se contrasta contra los criterios y reglas en `docs/cobertura.md`, no se calcula como porcentaje de escenarios verdes.

## 6. Encontrar el último reporte sin adivinar carpetas

Para explorar el contrato con Schemathesis, con la misma API levantada y sin Karate ejecutándose en paralelo:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py schemathesis
```

El ejecutor conserva generación por esquema y añade controles con recursos reales y roles correctos. Su reporte está en la carpeta indicada por `reports/latest-schemathesis.json`; `controles-contexto.json` separa los controles añadidos. Los archivos JUnit, NDJSON y HAR conservan los resultados. No interpretes automáticamente cada señal como un defecto: un ID inexistente, recurso ajeno o dato obligatorio omitido puede explicar un 404 o 422 correcto. Consulta `docs/contraste-documentacion-codigo.md` para contrastar documentación e implementación.

Cada ejecución tiene una carpeta nueva con fecha e identificador. Para la última ejecución **por tag o alcance**:

```powershell
$ultimaPrueba = Get-Content reports/latest-karate-selection.json -Raw | ConvertFrom-Json
"http://localhost:8765/$($ultimaPrueba.report_dir)/karate-summary.html"
```

Para la última **suite completa**, usa `reports/latest-karate.json`. Una ejecución parcial no sustituye ese registro. Cada carpeta conserva `execution.json` y el OpenAPI capturado al comenzar. Los reportes y logs originales son locales y pueden contener tokens de usuarios de prueba: no los publiques sin ocultarlos.

Para actualizar el HTML de resultados después de ejecutar **la suite completa** y revisar sus resultados:

```powershell
./.venv/Scripts/python.exe scripts/build_docs.py
```

Recarga la página del navegador. No necesitas regenerar el portal para abrir un reporte nuevo de Karate. Si se modifican las pruebas, un reporte anterior no representa el nuevo diseño; el generador verifica esa relación.

## 7. Interpretar lo que sale

| Lo que ves | Qué significa y qué hacer |
|---|---|
| Un escenario aprobado | Las aserciones ejecutadas en ese escenario se cumplieron. No demuestra por sí solo todos los CA de la HU. |
| Fallo en `match ...statusCode` o en el cuerpo | Compara esperado, obtenido y su regla. Puede revelar un defecto o un esperado incorrecto; revisa la fuente. |
| Fallo en `Background`, login o conexión | La preparación no terminó; no atribuyas a contactos una regla que ni siquiera llegó a probarse. |
| Salida distinta de cero | Hubo fallos o errores. Es intencional conservarlos; revisa el reporte y el log que imprime la consola. |
| «El tag no existe» | Copia la etiqueta exacta del `.feature`; no omitas `@` ni confundas HU con caso. |
| Conexión rechazada en 8000 | La API no está encendida. Revisa la Terminal 1. |
| Puerto ocupado | Puede haber otra instancia. Reutiliza conscientemente la que ya levantaste o detenla con Ctrl+C en su terminal. |

Si no deseas dejar una API levantada, puedes ejecutar un caso con `--start-api`; el puerto 8000 debe estar libre. Ese modo inicia la API, ejecuta y la detiene al terminar:

```powershell
./.venv/Scripts/python.exe scripts/run_qa.py karate --tag '@G4-001' --start-api
```

Para cerrar la sesión de trabajo, pulsa **Ctrl+C** en las terminales de API y HTML después de finalizar las pruebas.

## 8. Orden de demostración a la docente

1. Herramienta y motivo (breve), alcance asignado y HU elegida con **todos** sus CA.
2. Requisito → particiones/límites/estados o decisiones → casos resultantes. Explica por qué usaste esa técnica y qué datos elegiste.
3. Abre el `.feature`: preparación, petición y aserciones. Distingue reglas funcionales de restricciones del contrato.
4. Ejecuta toda la automatización del alcance en vivo, muestra su reporte y explica resultados concretos. Si hay un defecto, conserva el fallo y justifica el esperado.
5. Después ejecuta y explica la HU/caso elegida al azar usando su tag. Cierra con conclusiones y lecciones aprendidas. No prometas cobertura de un criterio sin su caso y evidencia.

## Incidencia observada al preparar datos

La ejecución integrada del 16/10 registró seis fallos de login en Background y una consulta prematura tras crear un contacto. Consulta [evidencia y causa probable](incidencia-consistencia.md). Un 201 seguido inmediatamente de 401/404 no demuestra que la regla funcional posterior haya sido evaluada. Conserva ambos registros; cualquier repetición produce un reporte nuevo, sin borrar el fallo anterior. Los controles de Schemathesis registran sus reintentos de preparación por separado.

## Tiempo de sustentación

Ensaya 10 minutos de exposición y reserva 5 para preguntas: herramienta y alcance 1 minuto; HU, técnicas y datos 3; validaciones técnicas y evidencia 2; ejecución completa y reporte 3; conclusiones 1. Las preguntas aleatorias se atienden con los tags ya preparados. No reemplaces la ejecución completa por una selección ni por capturas.

## Mostrar el detalle técnico de Schemathesis

Al ejecutar `scripts/run_qa.py schemathesis` se genera automáticamente el reporte navegable dentro de su directorio `reports/raw/schemathesis/<run_id>/`; la terminal imprime el enlace exacto. El [reporte versionado](../reports/schemathesis-detallado.html) es un archivo histórico. Filtra por categoría (required, type, length, pattern o auth), abre una petición y muestra su dato, respuesta y checks. Conserva los metadatos que explican la categoría. Sin metadatos suficientes se indica sin categoría demostrada; eso no cuenta como cobertura probada. Distingue checks propios de peticiones auxiliares evaluadas por un padre.

Para reconstruirlo desde la última ejecución guardada sin consumir la API:

```powershell
./.venv/Scripts/python.exe scripts/build_schemathesis_report.py
```

La reconstrucción lee evidencia histórica. Para la demo en vivo primero ejecuta la herramienta y luego abre el reporte de esa ejecución. El lanzador conserva además una copia del detalle en la carpeta propia de cada ejecución nueva.
