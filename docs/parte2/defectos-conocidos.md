# Defectos conocidos — Escenario A

Aplicación del criterio docente solicitada por el equipo en esta conversación. Admisión limitada a ejecución académica aislada; no es aprobación individual de la docente ni aceptación para producción.

Escenario A académico: aceptar solo firmas exactas documentadas en datos ficticios aislados. No certifica aptitud productiva. Flakiness, preparación, omisiones y causas nuevas bloquean.

No se afirma que los defectos financieros o de seguridad sean inocuos: conservan su severidad. La excepción se limita al riesgo de ejecutar pruebas con datos ficticios en una instancia aislada; no habilita despliegues ni uso productivo.

## D-01 — Alias con ñ rechazado

Severidad del producto: **Media**. Impacto: Impide altas o ediciones válidas.

Casos: G4-004, CF-01, E2E-G4-102, E2E-G4-113.

Reproducción y esperado/observado: Usar Niño en crear/editar; esperado 201/200, observado 422.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Media. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## D-02 — Duplicados normalizados permitidos

Severidad del producto: **Media**. Impacto: Permite alias duplicados con espacios.

Casos: G4-018, CF-03, E2E-G4-104, E2E-G4-115.

Reproducción y esperado/observado: Crear Ana y luego otro contacto con alias espacio-Ana-espacio; esperado 409, observado 201/200.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Media. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## D-03 — Aceptación de solicitud vencida

Severidad del producto: **Alta**. Impacto: Una solicitud fuera de vigencia puede mover dinero.

Casos: G4-053, G4-054, E2E-G4-324.

Reproducción y esperado/observado: Cargar pendiente, avanzar a 2880 minutos y aceptar; esperado 409, observado 200.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Alta. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## D-04 — Token válido después de logout

Severidad del producto: **Crítica**. Impacto: Revocación de autenticación inefectiva.

Casos: G4-074.

Reproducción y esperado/observado: Logout y reutilizar token; esperado 401, observado 200.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Crítica. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## D-05 — Invariantes monetarias concurrentes

Severidad del producto: **Crítica**. Impacto: Saldo o límite no protegido bajo concurrencia.

Casos: G4-116.

Reproducción y esperado/observado: Dos peticiones sincronizadas, comprobar probe.ok; esperado true, observado false.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Crítica. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## D-06 — Coerción de favorito fuera de contrato

Severidad del producto: **Media**. Impacto: Acepta texto o números donde el contrato declara booleano.

Casos: CT-02.

Reproducción y esperado/observado: PUT favorito con texto true/false o entero 0/1; esperado 422, observado 200.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Media. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## D-07 — Historial omite el último día

Severidad del producto: **Alta**. Impacto: Movimientos existentes no aparecen en el historial del día.

Casos: E2E-G4-117, E2E-G4-201, E2E-G4-202.

Reproducción y esperado/observado: Transferir y consultar historial hoy; esperado movimiento, observado tabla vacía.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Alta. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## D-08 — Transferencia a cuenta cerrada

Severidad del producto: **Alta**. Impacto: Permite enviar fondos a un destinatario inactivo.

Casos: E2E-G4-206.

Reproducción y esperado/observado: Cerrar cuenta destino sin saldo, transferir desde contacto; esperado rechazo 422, observado 201.

Admisión académica: Entorno local/CI de pruebas, datos y dinero ficticios, base exclusiva; sin despliegue ni acceso a cuentas reales. La severidad del producto permanece Alta. Fuera de este contexto no se admite la excepción.

Evidencia: matriz por caso, reporte crudo API/web y `reports/gate/` del mismo run. La política registra fuente y firma exacta; un fallo diferente del mismo caso bloquea.

## Observaciones de contrato revisadas

No se corrige Qolqe ni se retiran checks. Las 27 ocurrencias de Schemathesis se revisaron por perfil y quedan limitadas a huellas exactas de petición, respuesta y check, con contrato fijado. Una nueva huella bloquea.

- **K-C01**: Ejemplos incompletos y restricciones de monto no expresadas completamente en OpenAPI.
- **K-C02**: Prioridad de validación: contacto existente devuelve rechazo 409 antes del alias inválido.
- **K-C03**: Patrón de celular con dígitos Unicode frente a validación ASCII.
- **K-C04**: Null de query representado por el generador como texto estado=null.
