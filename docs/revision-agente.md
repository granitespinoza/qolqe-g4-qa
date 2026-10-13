# Revisión independiente y mejoras

Un agente adicional revisó el proyecto estáticamente por petición de Granit. No se atribuye a esta revisión una ejecución de pruebas ni una evaluación de usuarios.

| Hallazgo | Mejora aplicada |
|---|---|
| Resultados antiguos mezclados con fuentes actuales | Directorio y manifiesto por ejecución; huellas de features, datos y referencia; snapshot OpenAPI con hash; generación rechazada si cambian las fuentes |
| Fallo de preparación clasificado como defecto | Registro revisado en data/defectos-confirmados.json; la reproducción actual exige la aserción causante, no cualquier fallo del escenario |
| Rechazo por límite sin comprobar ausencia de efectos | Consultar ambos saldos, movimientos, consumo diario y estado/código de la solicitud después del rechazo |
| Máscaras comprobadas débilmente | Comprobar el nombre enmascarado esperado y CCI con exactamente los últimos cuatro dígitos |
| Inicio de API confundido con una instancia existente | Rechazar puerto ocupado y comprobar supervivencia del proceso creado |

La segunda revisión encontró un enlace que aún apuntaba al reporte anterior; se corrigió para usar el directorio del manifiesto.

## Incidencias de preparación
El auxiliar de concurrencia espera a que el login de sus cuentas recién creadas esté disponible, con máximo cinco intentos y registro de cada reintento. Esto se aplica al contexto de concurrencia, no a los escenarios que verifican el comportamiento de login. No se reintentan las transferencias ni se ajustan sus resultados esperados.
Un fallo del auxiliar se informa como preparación; no se presenta como prueba de saldo o límite. Su salida completa queda adjunta al escenario.

## Usabilidad
Se añadió un plan complementario para Parte 2 en docs/usabilidad.md. No sustituye las técnicas funcionales ni afirma que la docente haya exigido esa evaluación.
