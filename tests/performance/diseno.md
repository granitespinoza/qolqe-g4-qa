# Diseño y trazabilidad del experimento

## Objetivo y capa

Se evalúan los flujos de Quincena Qolqe por API HTTP. Criterio de selección: frecuencia (saldo/perfil e historial), impacto monetario (transferencia, recarga y pago) y operaciones de apoyo presentes en el perfil. Se incluyen más de tres flujos, manteniendo la distribución completa del enunciado. No se mide renderizado del frontend.

## Parámetros y fuente

| Parámetro | Valor | Origen o supuesto explícito |
|---|---|---|
| Llegada normal | 50 sesiones/min | Enunciado §4: 3000 sesiones/h |
| Concurrencia normal estimada | 100 VUs | 50 sesiones/min × 2 min de duración media |
| Concurrencia de campaña estimada | 300 VUs | Triple del nivel normal |
| Volumen de negocio normal | 5 operaciones/s | 3000 sesiones/h × 6 / 3600 |
| Login normal esperado | 0,83/s | 3000 / 3600; no se incluye en los porcentajes de las seis operaciones |
| Operaciones por sesión | 6 | Enunciado §4 |
| Think time | 10–25 s, triangular con moda 19 s | Enunciado: rango 10–25 y media 18; (10+19+25)/3 = 18 |
| Pausas por iteración | 6 | Interpretación: una pausa desde login hasta la primera operación y entre operaciones sucesivas |
| Pesos | 30/15/15/10/10/6/4/10 | Tabla del requerimiento; consulta y pago separados |
| Rampa de campaña | 300 s | Concentración de primeros ingresos en los primeros 5 min |
| Campaña estable | 600 s | Resto de la ventana de 15 min después de la subida |
| Descenso | 60 s | Decisión operativa para retirar usuarios progresivamente |
| Rampa de carga normal | 300 s | Decisión experimental: misma subida gradual, evitando lanzamiento simultáneo artificial |
| Carga estable | 600 s | Decisión experimental: aproximadamente 3000 operaciones normales para analizar percentiles y errores |
| Escalones de estrés | 25, 50, 100, 200, 300, 450, 600 | 100 y 300 vienen del negocio; niveles menores añadidos porque 100 incumplió; niveles superiores exploran el límite |
| Rampas y mesetas de estrés | 30 s y 150 s | Decisión experimental: progresión escalonada y periodo de aproximadamente una sesión completa por nivel |
| Finalización de sesiones | Hasta 150 s adicionales | Decisión del ejecutor; se registra tiempo efectivo, no se oculta dentro de la ventana estable |
| Datos por VU | Cuenta y destinatario exclusivos | Enunciado §3–5: usuario distinto por VU y saldo suficiente |
| Historial | 1000 movimientos/propietario | Volumen de los usuarios de carga de la semilla original; se asume incluido en el rango consultado |
| Saldos | S/10000 iniciales | Monto sintético suficiente, consistente con usuarios de carga originales |
| Dinero por operación | Transferencia/pago S/1; recarga S/5 | Elección de datos válidos para controlar límites; no es una distribución real de importes |
| Deudas | 64 por propietario y una reservada a consultas | Previsión del número de pagos según peso 4% y duración; el ejecutor rechaza agotamiento, no recicla pagos |

El modelo es cerrado por VUs y usa sesiones repetidas. Los dos minutos son una media de negocio: el script conserva pausas, no añade una espera artificial para forzar exactamente 120 s. El volumen logrado puede diferir de 5 operaciones/s; esa diferencia se presenta. En campaña, la concentración de primeros ingresos se interpreta por usuario distinto; las sesiones se repiten después para sostener la carga. No se reproduce una tasa de llegada abierta ni se mide directamente la longitud de una cola.

## Criterios

- Consultas e inicio de sesión: p95 <800 ms.
- Transferencias, recargas y pagos: p95 <1500 ms.
- Error normal: <=1%; se informa también login y cada operación.
- Throughput normal: >=5 operaciones de negocio/s, además de login. Saldo/perfil agrupa dos peticiones HTTP y una operación de negocio.
- Campaña: cero duplicados y operaciones parciales, con conciliación de intentos, registros, movimientos y saldos. El enunciado no proporciona umbral temporal numérico de campaña; se compara con la referencia normal de forma descriptiva.
- Estrés: aplicar referencia normal por nivel y volumen proporcional para estimar el mayor nivel observado que cumple; no confundirlo con capacidad máxima de producción.

Se informa el número de muestras por operación. Los percentiles calculados desde el diario usan interpolación lineal. Los valores de k6 de toda la corrida pueden diferir de los reportados en ventanas estables.

## Tipos y restricciones

Carga y estrés se ejecutan. La campaña de 300 VUs representa el pico de negocio de cinco minutos; no se inventa un salto de un segundo. Resistencia es relevante por las 18 h sin reinicios, pero no se ejecuta completa por ventana experimental y equipo compartido. Su descarte de ejecución es una limitación y no evidencia de estabilidad prolongada.

Se mide CPU y RSS de aplicación/generador y estado del host. Qolqe usa su SQLite original y un worker. No se cambian consultas ni reglas para obtener cumplimiento. Si el generador se satura, la corrida se declara inválida. Errores de datos se separan; no se suprimen del diario. Una pérdida de respuesta de dinero se investiga en la base, sin repetir la escritura.

El historial sintético está concentrado en una fecha anterior; no representa la distribución temporal de producción. CPU, RAM y disco son compartidos con otras aplicaciones. Los experimentos no proporcionan por sí solos causalidad completa: los recursos y el diagnóstico SQL deben interpretarse conjuntamente. No se añaden excepciones del Quality Gate de Parte 2 para aprobar integridad monetaria.
