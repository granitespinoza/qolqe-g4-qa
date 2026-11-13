# Parte 3 Pruebas de rendimiento de Qolqe

Esta entrega evalúa por HTTP la campaña Quincena Qolqe. Se conserva el código original en `referencias/qolqe-wallet`, con una base exclusiva por corrida. Los resultados describen esta laptop y no certifican capacidad de producción.

## Preparación en Windows

Desde la raíz del repositorio, con Python del proyecto ya preparado:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 install
```

Se instala k6 2.4.0 oficial en `.tools/performance`, psutil y las dependencias de gráficos. No se requiere Grafana Cloud, Docker ni credenciales externas. Las credenciales generadas son sintéticas; no se registran JWT en los diarios.

## Ejecución

Cerrar cualquier otra ejecución de Qolqe en el puerto 8021. Cerrar aplicaciones que compitan por CPU y memoria. Ejecutar un perfil por vez:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 referencia
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 carga
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 campana
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 estres
```

También existe `all`, que ejecuta referencia, carga, campaña y estrés. Cada prueba necesita minutos reales: carga y campaña tienen 300 s de subida, 600 s estables y 60 s de descenso, más finalización de sesiones. Estrés aumenta 25→50→100→200→300→450→600 VUs con 150 s estables por escalón y rampas de 30 s. La finalización de sesiones puede prolongar la duración; sus ventanas se documentan.

La demo corta dura alrededor de dos minutos más finalización de sesiones. Conserva think time real, pero no sustituye el experimento completo:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 demo
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 open
```

Para regenerar reportes existentes sin repetir la carga:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/performance.ps1 report
```

## Requerimiento y decisiones

- 3000 sesiones/h × 2 min / 60 = aproximadamente 100 usuarios simultáneos normales; campaña triple = 300.
- 3000 × 6 / 3600 = 5 operaciones de negocio/s normales, sin contar login. Saldo/perfil tiene dos peticiones secuenciales y una operación de negocio.
- Una iteración representa una sesión: login y seis operaciones con pausas triangulares de 10 a 25 s y moda 19 s (media 18 s). Se hacen seis pausas entre login y las seis operaciones. No se fuerza artificialmente la sesión a exactamente 120 s; se reporta la diferencia observada.
- Mezcla ponderada 30/15/15/10/10/6/4/10. Son probabilidades; el reporte muestra la mezcla lograda y los tamaños de muestra. Login se mide aparte.
- Consultas/login p95 <800 ms; dinero p95 <1500 ms; error normal <=1%. Umbrales evaluados por operación, además de gráficos agregados.
- Campaña exige cero duplicados o operaciones parciales. No tiene SLA numérico de degradación: se compara con la referencia normal sin inventar aprobación temporal de campaña.
- El pico de negocio se modela con concentración durante cinco minutos, no con un salto arbitrario de un segundo. Es un perfil de campaña; un spike abrupto adicional se descarta porque no está cuantificado en el requerimiento.
- Resistencia sí es relevante por las 18 horas diarias sin reinicio. No se ejecuta una validación de 18 horas por la ventana de trabajo y el equipo local compartido. Por tanto no se concluye ausencia de fugas ni estabilidad de jornada completa. Se propone una prueba dedicada posterior.
- Las duraciones de estabilización y escalones de estrés son decisiones experimentales, no cifras del negocio. Las ventanas estables se analizan separadamente de rampas y recuperación. El último escalón no certifica el límite absoluto.

## Datos y protección de resultados

Los endpoints de soporte reinician una base exclusiva. La preparación extiende los datos con el esquema original: propietario y destinatario exclusivos, 1000 movimientos sintéticos por propietario, contacto y 64 deudas pagables independientes. Otra deuda queda reservada para consultas. Saldos iniciales de S/10000, transferencias/pagos de S/1 y recargas de S/5 evitan límites ajenos al objetivo. Cada recarga utiliza un número distinto. No se modifica ninguna función del producto ni se ajustan saldos durante la medición.

Tras ejecutar se concilian intentos y respuestas contra transferencias, recargas, pagos, movimientos y saldos. No se reintentan operaciones monetarias. Un timeout se investiga por su identificador en la base. Si hay anomalías se conserva la base exclusiva en `.tools/performance/<run>/`; si la conciliación es correcta se eliminan únicamente los archivos de esa base y quedan las evidencias exportadas.

## Evidencias

Cada carpeta de `resultados/<fecha-UTC>-<perfil>/` contiene:

- `procedencia.json`, `configuracion.json`, `datos.json`: versión, entorno, parámetros y datos sintéticos.
- `operaciones.jsonl`: operaciones de negocio medidas, estado HTTP, causa y referencias monetarias.
- `k6-summary.json`, `k6.log`, `servidor.log`: evidencia de herramienta y aplicación.
- `recursos.csv`: CPU/RSS de Qolqe y k6, y estado del host por segundo. CPU de proceso se presenta en equivalentes de núcleo y normalizada por CPU lógicos.
- `integridad.json`, `operaciones_monetarias.json`, `saldos.csv`: conciliación.
- `resumen.json`, `series-15s.csv`, `graficos/`, `reporte.html`: análisis derivado.

`latest-*.json` apunta a la última corrida de cada perfil; el índice no mezcla reportes de otra ejecución. Los intentos iniciales de preparación no válidos no constituyen resultados del producto.

## Verificación de los analizadores

```powershell
.venv/Scripts/python.exe tests/performance/scripts/test_performance.py
```

Las comprobaciones verifican percentiles, ponderaciones y detección de duplicados, movimientos incompletos y saldos incorrectos. Una ejecución válida puede incumplir el SLA: se reporta el fallo real. La admisión de defectos conocidos de Parte 2 no convierte una anomalía monetaria en éxito.

## Exposición

Presentación local: `apidoc/parte3/index.html`. Reportes: `tests/performance/resultados/index.html`. Informe según plantilla: `docs/parte3/Informe_Rendimiento_Qolqe.docx`.

```powershell
.venv/Scripts/python.exe -m http.server 8765 --bind 127.0.0.1
```

Abrir `http://localhost:8765/apidoc/parte3/`. El guion personal se entrega en el chat, fuera del repositorio.

## Fuentes

Enunciado P2 Parte 3 y clases de semanas 12, 13 y 14. Documentación oficial de k6: https://grafana.com/docs/k6/latest/using-k6/scenarios/ y https://grafana.com/docs/k6/latest/using-k6/thresholds/. Alternativas: https://docs.locust.io/ y https://jmeter.apache.org/usermanual/best-practices.html.
