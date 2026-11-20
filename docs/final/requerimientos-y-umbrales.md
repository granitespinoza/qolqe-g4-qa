# Análisis del requerimiento y coherencia de resultados

## Contrato de alcance

La cobertura funcional API abarca los 51 CA de las HU del núcleo y G4, con 116 casos base, cinco complementarios y 15 identificadores técnicos: 136 IDs API que producen 187 escenarios/variantes al expandir los outlines. El auditor verifica enlaces, no cuenta cada interacción de Schemathesis como un caso. El resultado se considera completo solo si cada caso diseñado tiene ejecución actual; cualquier ausencia bloquea. No afirmamos cobertura de todas las ramas del código ni de otros módulos.

La web tiene 65 escenarios: 54 de G4 y 11 del núcleo, vinculados a las nueve HU comunes. Incluyen registro, acceso, logout, saldo/perfil, edición, cierre de cuenta, transferencia directa e interbancaria y simulación sin efectos monetarios. Los datos de frontera y variantes técnicas siguen cubiertos también por API; no se afirma que un happy path web cubra todas esas variantes.

## Derivación del modelo de rendimiento

| Dato | Cálculo / decisión | Limitación |
|---|---|---|
| 3000 sesiones/h y duración media 2 min | Ley de Little: 3000/60 × 2 ≈ 100 sesiones concurrentes | Aproximación estable; un modelo cerrado no mantiene una tasa fija de llegadas cuando aumenta la latencia |
| Triple de concurrencia en campaña | 300 VUs | VUs activos incluyen operaciones y pausas, no 300 peticiones instantáneas |
| 6 operaciones/sesión | 3000 × 6 / 3600 = 5 operaciones de negocio/s | Login aparte; saldo/perfil reúne dos peticiones HTTP |
| Pausas 10–25 s, media 18 s | Distribución triangular con moda 19 s | Elección de distribución; no fuerza cada sesión a exactamente 120 s |
| Mayoría de inicios en primeros 5 min de campaña | Rampa de 300 s, aproximación mediante VUs | No se reproduce una distribución exacta de llegadas; se repiten sesiones para sostener carga |
| Ventana de campaña de 15 min | 300 s subida + 600 s estable; 60 s de descenso adicional | Cierre de sesiones hasta 150 s; tiempo total no equivale a ventana estable |
| Estrés | 25/50/100/200/300/450/600; rampas 30 s, estables 150 s | Niveles y duración son decisiones experimentales; no fueron datos prescritos por negocio |
| Operación 6:00–24:00 | Resistencia relevante de 18 h | No ejecutada; una prueba breve no acredita estabilidad diaria ni ausencia de fugas |

## Criterios y controles

| Criterio | Métrica y límite | Carga / interpretación |
|---|---|---|
| Consultas y login | p95 de cada operación <800 ms | Hora punta; referencia descriptiva en campaña |
| Transferencias, recargas, pagos | p95 por operación <1500 ms | Hora punta; referencia descriptiva en campaña |
| Error | ≤1% operaciones de negocio; login separado | Hora punta |
| Volumen | ≥5 operaciones de negocio correctas/s | 100 VUs, ventana estable; no peticiones HTTP/s |
| Integridad | 0 duplicados y 0 parciales detectados; saldos/movimientos conciliados | Todas las corridas; obligatorio en campaña |
| Validez del generador | CPU k6 inferior a aproximadamente 80% del host | Control del experimento, no SLA de Qolqe |

No fijamos un límite de CPU o memoria del producto que el requerimiento no define. Las métricas de recursos sirven para diagnosticar. Los datos de dinero son sintéticos y los saldos suficientes evitan falsos fallos por reglas de negocio.

## Lectura coherente

1. Separar diseño, ejecución válida, resultado crudo y gate académico.
2. El p95 de la ventana completa no es el promedio de los p95 de intervalos de 15 s.
3. Un agregado de consultas puede cumplir aunque movimientos incumpla; decidir por operación.
4. El gráfico de error temporal incluye login; las tablas separan errores de negocio/login.
5. La conciliación comprende toda la corrida, mientras throughput y percentiles se evalúan en ventanas estables.
6. Descenso programado de VUs no es colapso. En estrés se observa degradación con demanda alta, errores y caída de operaciones exitosas.
7. Capacidad observada: 50 cumple; siguiente nivel 100 incumple. No equivale a máximo exacto de producción.
8. Campaña puede conservar integridad y superar la latencia normal: su True de perfil no es aprobación de un SLA temporal nuevo.

## Hallazgos y recomendaciones

Carga: 5.47 operaciones correctas/s y 0% de error; movimientos p95 914.80 ms >800. Campaña: 16.38 operaciones correctas/s, 0% de error, 3988 operaciones monetarias conciliadas; movimientos p95 1453.80 ms. Estrés: degradación temporal desde 100, severa en 450 y 0 operaciones exitosas/s en 600 durante su ventana. Son ejecuciones locales históricas identificadas; no se atribuyen a un pipeline nuevo.

Se confirmó N+1 antes de paginar (102 SELECT para 100 registros y 1002 para 1000). Se observaron bloqueos de SQLite durante escrituras. No se aisló su contribución exacta. Recomendamos optimizar consultas, instrumentar esperas/transacciones y repetir con servidor/generador separados. Ocho operaciones persistieron pese a error o respuesta perdida: no prueba duplicados, sí riesgo de repetición manual. Recomendamos consulta de estado e idempotencia. No modificamos Qolqe.
