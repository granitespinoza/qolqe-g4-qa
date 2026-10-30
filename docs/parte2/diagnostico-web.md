> Registro histórico de etapas previas. Estado y criterio actuales: [Quality Gate Escenario A](quality-gate.md) y [guía final](entrega.md). La aplicación permanece intacta.

# Diagnóstico web — pasos 3 y 4

Los tests comparan la aplicación original con sus requisitos, sin modificar la referencia. Un fallo conocido sigue fallando y no equivale a una aprobación. Los resultados definitivos por corrida están en [verificacion-web.md](verificacion-web.md).

| Hallazgo | Pruebas | Regla y resultado esperado | Comportamiento observado |
|---|---|---|---|
| D-01: alias ñ | E2E-G4-102, 113 | R-G4-02 permite ñ; crear 201 y editar 200 | Respuesta 422. Reproduce el hallazgo API. |
| D-02: duplicados normalizados | E2E-G4-104, 115 | R-G4-03: duplicado tras recortar espacios debe responder 409 | Crear devuelve 201 y editar 200. Reproduce el hallazgo API. |
| D-03: aceptación vencida | E2E-G4-324 | HU-G4-08 CA4: una solicitud vencida no se acepta; 409 | El formulario se carga antes del vencimiento y se envía después: devuelve 200. Reproduce el hallazgo API. |
| D-07: historial del día | E2E-G4-117, 201, 202 | Transferir y conservar su movimiento visible; eliminar el contacto no elimina el historial | Los movimientos existen por código, pero el historial web del día queda vacío. |
| D-08: transferencia a cuenta cerrada | E2E-G4-206 | RN-07 / HU-N-07 CA2, dependencia de HU-G4-05: rechazar destino inactivo | Una cuenta cerrada recibe la transferencia (201). |

## Sustento técnico de los hallazgos nuevos

- **D-07:** `referencias/qolqe-wallet/qolqe/api/movimientos.py`, `_filtrar`, usa `m.fecha BETWEEN desde.isoformat() AND hasta.isoformat()`. La fecha superior es solo `AAAA-MM-DD`; los movimientos incluyen hora, por lo que los del último día quedan fuera. Los tests comprueban primero el movimiento por su código y luego la tabla web. No se amplía artificialmente la fecha a mañana para obtener verde.
- **D-08:** `referencias/qolqe-wallet/qolqe/api/transferencias.py`, `_resolver_destino_qolqe`, busca el usuario por celular sin comprobar su estado. `realizar_transferencia` tampoco rechaza una cuenta cerrada. La preparación cierra una cuenta con saldo cero y sin solicitudes pendientes; el test hace la transferencia desde el contacto por UI.

Las ubicaciones son del commit fijo `8c7d2f0c939ede7765b7b80b98c10c3905693fda`. D-07 y D-08 son hallazgos adicionales; no se suman automáticamente a los conteos del diagnóstico API anterior.

## Ajustes del arnés durante la validación

- Esperar que la lista de solicitudes esté cargada antes de pulsar una pestaña tras recargar. Un botón visible todavía puede no tener su controlador de eventos registrado.
- Construir las cabeceras de autenticación cuando se ejecuta el comando de Cypress, después de renovar el token al avanzar el reloj; evitar capturar el token antiguo al encolar comandos.
- Sondeos acotados de lectura y autenticación exclusivamente para disponibilidad de fixtures; no repetir altas, transferencias ni transiciones de negocio.
- Corregir el celular inexistente del caso 106: `900000001` pertenece a los datos semilla. Se usa `909999999`, fuera de la semilla y del rango de generación de actores.
- Corregir la expectativa del aviso de favoritos: el texto real es «5 contactos favoritos».

Estas correcciones no cambian las reglas esperadas de negocio. Las corridas preliminares de depuración no cuentan entre las tres ejecuciones finales de estabilidad.

## Qué significa para la entrega

El código implementa los grupos de variantes del alcance web G4. El requisito de tres ejecuciones completamente verdes sigue pendiente mientras los defectos se reproduzcan. Corregir la aplicación exigiría una versión autorizada distinta de la referencia original; cambiar los tests para aceptar estos defectos falsearía la evaluación. La integración y publicación de resultados en CI corresponde a los siguientes pasos del plan.

## Observaciones de consistencia en las corridas finales

Los casos E2E-G4-109 (contador tras agregar el contacto 11), E2E-G4-116 (estrella tras desmarcar favorito) , E2E-G4-319 (estado tras rechazar una solicitud) y E2E-G4-302 (solicitud recién creada ausente en la lista) pueden fallar después de una respuesta funcional exitosa: la interfaz conserva el estado anterior. Se registran por separado de los cinco defectos funcionales reproducidos; ver los resultados de cada corrida para saber cuándo ocurrieron. No se atribuyen automáticamente a falta de tiempo de espera: las aserciones ya esperan el estado DOM y la aplicación puede no volver a consultar los datos. Deben investigarse el orden de commit y la recarga de datos antes de declarar una causa definitiva. No se repite la escritura ni se recarga artificialmente la pantalla para ocultar este resultado.
