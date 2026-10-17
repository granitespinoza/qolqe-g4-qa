# Diseño de pruebas

## Método
Para cada caso mantenemos las demás entradas válidas. Los valores límite de dos puntos se aplican a alias; tres puntos a vencimiento. Vacío y espacios se comprueban por separado.

| Caso | HU / CA | Regla | Técnica | Por qué | Resultado |
|---|---|---|---|---|---|
| G4-001 | HU-G4-01 CA1 | R-G4-01/02/03 | Valores límite (2 puntos) | Alias permitido; celular activo, ajeno y lista vacía. | APROBADO |
| G4-002 | HU-G4-01 CA1 | R-G4-01/02/03 | Valores límite (2 puntos) | Alias permitido; celular activo, ajeno y lista vacía. | APROBADO |
| G4-003 | HU-G4-01 CA1 | R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía. | APROBADO |
| G4-004 | HU-G4-01 CA1 | R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía. | FALLÓ |
| G4-005 | HU-G4-01 CA1 | R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía. | APROBADO |
| G4-006 | HU-G4-01 CA1 | R-G4-01/02/03 | Particiones de equivalencia | Alias permitido; celular activo, ajeno y lista vacía. | APROBADO |
| G4-007 | HU-G4-01 CA1 | R-G4-02 | Valores límite (2 puntos) | Frontera o clase inválida, restantes condiciones válidas. | APROBADO |
| G4-008 | HU-G4-01 CA1 | R-G4-02 | Valores límite (2 puntos) | Frontera o clase inválida, restantes condiciones válidas. | APROBADO |
| G4-009 | HU-G4-01 CA1 | R-G4-02 | Particiones de equivalencia | Frontera o clase inválida, restantes condiciones válidas. | APROBADO |
| G4-010 | HU-G4-01 CA1 | R-G4-02 | Particiones de equivalencia | Frontera o clase inválida, restantes condiciones válidas. | APROBADO |
| G4-011 | HU-G4-01 CA1 | R-G4-02 | Particiones de equivalencia | Frontera o clase inválida, restantes condiciones válidas. | APROBADO |
| G4-012 | HU-G4-01 CA1 | R-G4-01 | Particiones de equivalencia | Representante de una condición distinta de negocio. | APROBADO |
| G4-013 | HU-G4-01 CA1 | R-G4-01 | Particiones de equivalencia | Representante de una condición distinta de negocio. | APROBADO |
| G4-014 | HU-G4-01 CA1 | R-G4-01 | Particiones de equivalencia | Representante de una condición distinta de negocio. | APROBADO |
| G4-015 | HU-G4-01 CA1 | R-G4-01 | Particiones de equivalencia | Cerrar una cuenta propia de contexto no reutiliza datos ajenos. | FALLÓ |
| G4-016 | HU-G4-01 CA1 | R-G4-01 | Particiones de equivalencia | Mismo celular con otro alias. | APROBADO |
| G4-017 | HU-G4-01 CA1 | R-G4-02 | Particiones de equivalencia | Unicidad se comprueba sin mayúsculas y tras recortar espacios. | APROBADO |
| G4-018 | HU-G4-01 CA1 | R-G4-02 | Particiones de equivalencia | Unicidad se comprueba sin mayúsculas y tras recortar espacios. | FALLÓ |
| G4-019 | HU-G4-01 CA1 | R-G4-03 | Valores límite (2 puntos) | Contexto con 14; comprobar frontera y ausencia de efecto al superar 15. | APROBADO |
| G4-020 | HU-G4-02 CA2, CA3 | HU-G4-02 CA2/3 | Particiones de equivalencia | José debe coincidir con JOSE; se verifica máscara, teléfono y favorito. | APROBADO |
| G4-021 | HU-G4-02 CA1 | HU-G4-02 CA1 | Particiones de equivalencia | Favorito con alias Z debe preceder a alias A no favorito. | APROBADO |
| G4-022 | HU-G4-02 CA1 | HU-G4-02 CA1 | Valores límite (2 puntos) | 10/11 distingue primera y segunda página. | APROBADO |
| G4-023 | HU-G4-02 CA2 | HU-G4-02 CA2 | Particiones de equivalencia | Consulta válida sin coincidencias devuelve lista vacía. | APROBADO |
| G4-024 | HU-G4-03 CA1 | R-G4-02 | Particiones de equivalencia | Mantener el mismo alias no debe ser duplicado; celular se conserva. | APROBADO |
| G4-025 | HU-G4-03 CA1 | R-G4-03 | Transición de estados | Ambas acciones conservan alias y celular. | APROBADO |
| G4-026 | HU-G4-03 CA1 | R-G4-03 | Valores límite (2 puntos) | Verificar 5/6 y que el sexto conserve estado no favorito. | APROBADO |
| G4-027 | HU-G4-03 CA1 | Propiedad de datos | Particiones de equivalencia | Un tercero no puede editar un recurso ajeno. | APROBADO |
| G4-028 | HU-G4-04 CA1 | RN-11 | Comprobación de efectos | Transferir, eliminar y consultar movimiento por código. | APROBADO |
| G4-029 | HU-G4-04 CA2 | R-G4-05 | Tabla de decisiones | Contacto propio y solicitud pendiente vigente. | APROBADO |
| G4-030 | HU-G4-04 CA2 | R-G4-05 | Tabla de decisiones | Comprobar dirección recibida, no solo enviada. | APROBADO |
| G4-031 | HU-G4-04 CA2 | R-G4-05 | Transición de estados | Vencida no bloquea eliminación. | APROBADO |
| G4-032 | HU-G4-05 CA1 | HU-N-07 | Comprobación de efectos | Cuenta origen 100, destino 0; transferencia 10 y SMS. | APROBADO |
| G4-033 | HU-G4-05 CA1 | RN-08 | Particiones de equivalencia | Saldo cero y monto válido; no confundir con monto inválido. | APROBADO |
| G4-034 | HU-G4-06 CA1, CA2 | R-G4-04/05 | Comprobación de efectos | El monto pedido no debita saldo antes de aceptar. | APROBADO |
| G4-035 | HU-G4-06 CA1 | RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales. | APROBADO |
| G4-036 | HU-G4-06 CA1 | RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales. | APROBADO |
| G4-037 | HU-G4-06 CA1 | RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales. | APROBADO |
| G4-038 | HU-G4-06 CA1 | RN-05 / R-G4-04 | Valores límite (2 puntos) | Fronteras monetarias y clase con demasiados decimales. | APROBADO |
| G4-039 | HU-G4-06 CA1 | RN-05 / R-G4-04 | Particiones de equivalencia | Fronteras monetarias y clase con demasiados decimales. | APROBADO |
| G4-040 | HU-G4-06 CA1 | R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos. | APROBADO |
| G4-041 | HU-G4-06 CA1 | R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos. | APROBADO |
| G4-042 | HU-G4-06 CA1 | R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos. | APROBADO |
| G4-043 | HU-G4-06 CA1 | R-G4-04 | Valores límite (2 puntos) | Fronteras 3/60 con monto y contacto válidos. | APROBADO |
| G4-044 | HU-G4-06 CA1 | R-G4-04 | Valores límite (2 puntos) | Límite independiente del número de contactos. | APROBADO |
| G4-045 | HU-G4-07 CA1 | HU-G4-07 CA1 | Particiones de equivalencia | Mismo recurso aparece según rol; filtro sin coincidencias. | APROBADO |
| G4-046 | HU-G4-07 CA2 | R-G4-05 | Valores límite (3 puntos) | Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min. | APROBADO |
| G4-047 | HU-G4-07 CA2 | R-G4-05 | Valores límite (3 puntos) | Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min. | APROBADO |
| G4-048 | HU-G4-07 CA2 | R-G4-05 | Valores límite (3 puntos) | Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min. | APROBADO |
| G4-049 | HU-G4-08 CA1, CA3, CA4 | HU-N-07 / R-G4-05 | Transición de estados | Destinatario vigente con saldo; vincular operación y solicitud. | APROBADO |
| G4-050 | HU-G4-08 CA2 | RN-08 / R-G4-05 | Transición de estados | Error financiero no resuelve solicitud. | APROBADO |
| G4-051 | HU-G4-08 CA4 | Propiedad de datos | Tabla de decisiones | Token válido con rol ajeno devuelve 404. | APROBADO |
| G4-052 | HU-G4-08 CA4 | R-G4-05 | Valores límite (3 puntos) | Vigencia se decide en la acción, no solo al listar. | APROBADO |
| G4-053 | HU-G4-08 CA4 | R-G4-05 | Valores límite (3 puntos) | Vigencia se decide en la acción, no solo al listar. | FALLÓ |
| G4-054 | HU-G4-08 CA4 | R-G4-05 | Valores límite (3 puntos) | Vigencia se decide en la acción, no solo al listar. | FALLÓ |
| G4-055 | HU-G4-08 CA4 | R-G4-05 | Transición de estados | La segunda aceptación no duplica dinero. | APROBADO |
| G4-056 | HU-G4-09 CA1 | R-G4-05 | Transición de estados | Acción del rol correcto cambia el estado sin mover dinero. | APROBADO |
| G4-057 | HU-G4-09 CA1 | Propiedad de datos | Tabla de decisiones | Un usuario ajeno no puede resolver solicitudes. | APROBADO |
| G4-058 | HU-G4-09 CA1 | R-G4-05 | Transición de estados | A las 48 h la acción debe ser rechazada. | APROBADO |
| G4-059 | HU-G4-09 CA1 | R-G4-05 | Transición de estados | Estado terminal no admite otra resolución. | APROBADO |
| G4-060 | HU-G4-10 CA1 | R-G4-05 | Transición de estados | Acción del rol correcto cambia el estado sin mover dinero. | APROBADO |
| G4-061 | HU-G4-10 CA1 | Propiedad de datos | Tabla de decisiones | Un usuario ajeno no puede resolver solicitudes. | APROBADO |
| G4-062 | HU-G4-10 CA1 | R-G4-05 | Transición de estados | A las 48 h la acción debe ser rechazada. | APROBADO |
| G4-063 | HU-G4-10 CA1 | R-G4-05 | Transición de estados | Estado terminal no admite otra resolución. | APROBADO |
| G4-064 | HU-G4-09 CA1 | HU-G4-09 CA1 | Particiones de equivalencia | Omitir motivo debe estar permitido; SMS verificable. | APROBADO |
| G4-065 | HU-G4-09 CA1 | HU-G4-09 CA1 | Valores límite (2 puntos) | Extremo permitido y vecino inválido. | APROBADO |
| G4-066 | HU-G4-09 CA1 | HU-G4-09 CA1 | Valores límite (2 puntos) | Extremo permitido y vecino inválido. | APROBADO |
| G4-067 | HU-N-01 CA1, CA6 | RN-01/02/03 | Comprobación de efectos | Usuarios creados por API; se verifican consecuencias del registro. | APROBADO |
| G4-068 | HU-N-01 CA2 | RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso. | APROBADO |
| G4-069 | HU-N-01 CA3 | RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso. | APROBADO |
| G4-070 | HU-N-01 CA4 | RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso. | APROBADO |
| G4-071 | HU-N-01 CA5 | RN-01/02/03 | Particiones de equivalencia | Una entrada inválida por caso. | APROBADO |
| G4-072 | HU-N-02 CA1 | HU-N-02 CA1 | Comprobación de efectos | La autenticación de contexto se vuelve a verificar explícitamente. | APROBADO |
| G4-073 | HU-N-02 CA2, CA3, CA4 | RN-04 | Transición de estados | Secuencia de intentos y frontera temporal. | APROBADO |
| G4-074 | HU-N-03 CA1, CA2 | HU-N-03 | Transición de estados | Dos sesiones; revocación de una no afecta la otra. | FALLÓ |
| G4-075 | HU-N-04 CA1, CA2 | HU-N-04 | Comprobación de efectos | No revelar DNI completo. | APROBADO |
| G4-076 | HU-N-04 CA3 | HU-N-04 CA3 | Particiones de equivalencia | Ausente e inválido son clases diferentes. | APROBADO |
| G4-077 | HU-N-04 CA3 | HU-N-04 CA3 | Particiones de equivalencia | Ausente e inválido son clases diferentes. | APROBADO |
| G4-078 | HU-N-04 CA3 | HU-N-04 CA3 | Valores límite (2 puntos) | A los 30 min debe rechazarse. | APROBADO |
| G4-079 | HU-N-05 CA1, CA2, CA3 | HU-N-05 | Comprobación de efectos | Actualizar permitidos sin cambiar identidad. | APROBADO |
| G4-080 | HU-N-06 CA1, CA2, CA4 | HU-N-06 | Transición de estados | Cierre válido y posterior login prohibido. | FALLÓ |
| G4-081 | HU-N-06 CA3 | HU-N-06 CA3 | Tabla de decisiones | Saldo cero pero solicitud pendiente: rechazo de cierre. | APROBADO |
| G4-082 | HU-N-07 CA1, CA2 | RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos. | APROBADO |
| G4-083 | HU-N-07 CA1, CA2 | RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos. | APROBADO |
| G4-084 | HU-N-07 CA1, CA2 | RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos. | APROBADO |
| G4-085 | HU-N-07 CA1, CA2 | RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos. | APROBADO |
| G4-086 | HU-N-07 CA1, CA2 | RN-05 | Valores límite (2 puntos) | Probar rango financiero con saldo y destinatario válidos. | APROBADO |
| G4-087 | HU-N-07 CA3, CA4 | RN-10 | Comprobación de efectos | Verificar transferencia en ambas cuentas. | APROBADO |
| G4-088 | HU-N-08 CA1, CA2, CA3 | RN-09 | Comprobación de efectos | Monto 100: comisión 1.50; verificar CCI en movimiento. | APROBADO |
| G4-089 | HU-N-09 CA1 | RN-09 | Particiones de equivalencia | Mínimo, proporcional y máximo; saldo no cambia. | APROBADO |
| G4-090 | HU-N-09 CA1 | RN-09 | Particiones de equivalencia | Mínimo, proporcional y máximo; saldo no cambia. | APROBADO |
| G4-091 | HU-N-09 CA1 | RN-09 | Particiones de equivalencia | Mínimo, proporcional y máximo; saldo no cambia. | APROBADO |
| G4-092 | HU-N-02 CA5 | HU-N-02 CA5 | Transición de estados | Cerrar cuenta con saldo cero antes de intentar ingresar. | APROBADO |
| G4-093 | HU-N-02 CA6 | HU-N-02 CA6 | Comprobación de efectos | Identificador no registrado no bloquea login, pero avisa. | FALLÓ |
| G4-094 | HU-N-03 CA2 | HU-N-03 CA2 | Transición de estados | Separado del caso de revocación para que su fallo no oculte este criterio. | APROBADO |
| G4-095 | HU-G4-05 CA1 | RN-06 | Tabla de decisiones | Saldo suficiente pero límite agotado: aislar rechazo diario. | APROBADO |
| G4-096 | HU-G4-08 CA1, CA2 | RN-06 | Tabla de decisiones | Saldo suficiente pero límite agotado: aislar rechazo diario. | APROBADO |
| G4-097 | HU-G4-08 CA4 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-098 | HU-G4-09 CA1 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-099 | HU-G4-10 CA1 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-100 | HU-G4-08 CA4 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-101 | HU-G4-09 CA1 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-102 | HU-G4-10 CA1 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-103 | HU-G4-08 CA4 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-104 | HU-G4-09 CA1 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-105 | HU-G4-10 CA1 | R-G4-05 | Transición de estados | Cubrir transición inválida desde estado terminal con rol correcto. | APROBADO |
| G4-106 | HU-G4-01 CA1 | R-G4-01 | Particiones de equivalencia | Crear valor nuevo sin registrar; separado de cuenta cerrada. | APROBADO |
| G4-107 | HU-G4-02 CA1 | HU-G4-02 CA1 | Particiones de equivalencia | Cuatro alias comprueban ambos grupos y prioridad de favoritos. | APROBADO |
| G4-108 | HU-G4-03 CA1 | HU-G4-03 CA1 | Comprobación de efectos | No basta verificar el campo cambiado. | APROBADO |
| G4-109 | HU-G4-06 CA1 | Propiedad de datos | Particiones de equivalencia | Un id válido ajeno debe ser tratado como inexistente. | APROBADO |
| G4-110 | HU-N-01 CA3 | RN-02 | Particiones de equivalencia | Registro con celular existente y restantes datos válidos. | APROBADO |
| G4-111 | HU-N-01 CA5 | HU-N-01 CA5 | Particiones de equivalencia | Primera cuenta fija correo; segunda intenta su versión en mayúsculas. | APROBADO |
| G4-112 | HU-N-06 CA1 | HU-N-06 CA1 | Particiones de equivalencia | Saldo cero, PIN incorrecto; conservar cuenta activa. | APROBADO |
| G4-113 | HU-N-06 CA2 | HU-N-06 CA2 | Particiones de equivalencia | PIN correcto y saldo positivo. | APROBADO |
| G4-114 | HU-N-07 CA2 | RN-07 | Particiones de equivalencia | Monto válido y saldo suficiente; aislar destino. | APROBADO |
| G4-115 | HU-N-08 CA1 | HU-N-08 CA1 | Particiones de equivalencia | CCI corto con monto válido. | APROBADO |
| G4-116 | HU-N-07 CA5 | RN-06/08 | Tabla de decisiones y concurrencia | Dos peticiones HTTP sincronizadas; comprobar límite y saldo por separado. Los reintentos de preparación, si ocurren, quedan en la evidencia. | FALLÓ |

## HU-N-01 — Registrarme · Prioridad Alta

**Como** visitante **quiero** crear una cuenta con mi DNI y celular **para** usar la billetera.
- **CA1.** Con DNI, nombres (2 a 80 caracteres), celular, PIN y correo opcional válidos, la cuenta se crea con saldo S/ 0.00 y límite diario de S/ 2,000.00.
- **CA2.** DNI que no cumple RN-01 *(error `DNI_INVALIDO`)*.
- **CA3.** Celular que no cumple RN-02 *(error `CELULAR_INVALIDO`)*, o que ya está registrado *(error `CELULAR_REGISTRADO`, 409)*.
- **CA4.** PIN que no cumple RN-03 *(error `PIN_INVALIDO`)*.
- **CA5.** Correo con formato inválido *(error `CORREO_INVALIDO`)* o ya usado por otra cuenta activa, sin distinguir mayúsculas *(error `CORREO_REGISTRADO`, 409)*.
- **CA6.** Se envía un SMS de bienvenida al celular registrado.

### G4-067 — Registro crea saldo cero, límite y bienvenida
**Técnica:** Comprobación de efectos. **Justificación:** Usuarios creados por API; se verifican consecuencias del registro.
**Regla:** RN-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-n-01.feature) · [Evidencia](../evidencias/G4-067.html)
```gherkin
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.statusCode == 200
* match r.result.saldo == '0.00'
* def r = req('/api/limites', 'GET', null, a.token, {})
* match r.result.limite_diario == '2000.00'
* def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
* assert r.result.length >= 1
```

### G4-068 — Rechazar dni inválido
**Técnica:** Particiones de equivalencia. **Justificación:** Una entrada inválida por caso.
**Regla:** RN-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-n-01.feature) · [Evidencia](../evidencias/G4-068.html)
```gherkin
* def n = random()
* def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
* set payload.dni = '123'
* def r = req('/api/usuarios', 'POST', payload, null, {})
* match r.statusCode == 422
* match r.result.codigo == 'DNI_INVALIDO'
```

### G4-069 — Rechazar celular inválido
**Técnica:** Particiones de equivalencia. **Justificación:** Una entrada inválida por caso.
**Regla:** RN-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-n-01.feature) · [Evidencia](../evidencias/G4-069.html)
```gherkin
* def n = random()
* def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
* set payload.celular = '123'
* def r = req('/api/usuarios', 'POST', payload, null, {})
* match r.statusCode == 422
* match r.result.codigo == 'CELULAR_INVALIDO'
```

### G4-070 — Rechazar pin inválido
**Técnica:** Particiones de equivalencia. **Justificación:** Una entrada inválida por caso.
**Regla:** RN-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-n-01.feature) · [Evidencia](../evidencias/G4-070.html)
```gherkin
* def n = random()
* def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
* set payload.pin = '1111'
* def r = req('/api/usuarios', 'POST', payload, null, {})
* match r.statusCode == 422
* match r.result.codigo == 'PIN_INVALIDO'
```

### G4-071 — Rechazar correo inválido
**Técnica:** Particiones de equivalencia. **Justificación:** Una entrada inválida por caso.
**Regla:** RN-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-n-01.feature) · [Evidencia](../evidencias/G4-071.html)
```gherkin
* def n = random()
* def payload = {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9" + n)',pin:'4826'}
* set payload.correo = 'invalid'
* def r = req('/api/usuarios', 'POST', payload, null, {})
* match r.statusCode == 422
* match r.result.codigo == 'CORREO_INVALIDO'
```

### G4-110 — Celular duplicado responde conflicto
**Técnica:** Particiones de equivalencia. **Justificación:** Registro con celular existente y restantes datos válidos.
**Regla:** RN-02. **Resultado:** APROBADO.
[Escenario](../features/hu-n-01.feature) · [Evidencia](../evidencias/G4-110.html)
```gherkin
* def r = req('/api/usuarios', 'POST', {dni:'12345678',nombres:'Nuevo Usuario',celular:'#(a.cell)',pin:'4826'}, null, {})
* match r.statusCode == 409
* match r.result.codigo == 'CELULAR_REGISTRADO'
```

### G4-111 — Correo duplicado ignora mayúsculas
**Técnica:** Particiones de equivalencia. **Justificación:** Primera cuenta fija correo; segunda intenta su versión en mayúsculas.
**Regla:** HU-N-01 CA5. **Resultado:** APROBADO.
[Escenario](../features/hu-n-01.feature) · [Evidencia](../evidencias/G4-111.html)
```gherkin
* def email = a.cell + '@example.com'
* def r = req('/api/cuentas/me', 'PUT', {correo:email}, a.token, {})
* match r.statusCode == 200
* def n = random()
* def r = req('/api/usuarios', 'POST', {dni:'#(n)',nombres:'Nuevo Usuario',celular:'#("9"+n)',pin:'4826',correo:'#(email.toUpperCase())'}, null, {})
* match r.statusCode == 409
* match r.result.codigo == 'CORREO_REGISTRADO'
```


## HU-N-02 — Iniciar sesión · Prioridad Alta

**Como** cliente **quiero** ingresar con mi celular y PIN **para** acceder a mi cuenta de forma segura.
- **CA1.** Con credenciales correctas recibo un token válido por 30 minutos y se crea una **sesión activa**.
- **CA2.** Con celular inexistente o PIN incorrecto recibo un mensaje genérico, sin revelar cuál dato falló *(error `CREDENCIALES_INVALIDAS`, 401)*.
- **CA3.** Se aplica RN-04. Al tercer intento fallido consecutivo la respuesta es *(error `CUENTA_BLOQUEADA`, 423)* y se envía un SMS de aviso.
- **CA4.** Durante el bloqueo, ni siquiera el PIN correcto permite ingresar (423). Pasados los 15 minutos puedo ingresar normalmente.
- **CA5.** Una cuenta cerrada no puede iniciar sesión *(error `CUENTA_CERRADA`, 401)*.
- **CA6.** Si envío el identificador de un dispositivo que **no** está en mis dispositivos de confianza (HU-G6-05), puedo ingresar, pero recibo un SMS de alerta de "nuevo dispositivo".

### G4-072 — Login crea sesión con vigencia de 30 minutos
**Técnica:** Comprobación de efectos. **Justificación:** La autenticación de contexto se vuelve a verificar explícitamente.
**Regla:** HU-N-02 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-n-02.feature) · [Evidencia](../evidencias/G4-072.html)
```gherkin
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
* match r.statusCode == 200
* match r.result.expires_in == 1800
* match r.result.sesion_id == "#number"
```

### G4-073 — Bloqueo tras tres intentos y acceso después de 15 min
**Técnica:** Transición de estados. **Justificación:** Secuencia de intentos y frontera temporal.
**Regla:** RN-04. **Resultado:** APROBADO.
[Escenario](../features/hu-n-02.feature) · [Evidencia](../evidencias/G4-073.html)
```gherkin
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'0000'}, null, {})
* match r.statusCode == 401
* match r.result.codigo == 'CREDENCIALES_INVALIDAS'
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'0000'}, null, {})
* match r.statusCode == 401
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'0000'}, null, {})
* match r.statusCode == 423
* match r.result.codigo == 'CUENTA_BLOQUEADA'
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
* match r.statusCode == 423
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:15}, null, {})
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
* match r.statusCode == 200
```

### G4-092 — Cuenta cerrada no puede ingresar
**Técnica:** Transición de estados. **Justificación:** Cerrar cuenta con saldo cero antes de intentar ingresar.
**Regla:** HU-N-02 CA5. **Resultado:** APROBADO.
[Escenario](../features/hu-n-02.feature) · [Evidencia](../evidencias/G4-092.html)
```gherkin
* def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
* match r.statusCode == 204
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
* match r.statusCode == 401
* match r.result.codigo == 'CUENTA_CERRADA'
```

### G4-093 — Nuevo dispositivo permite login y genera alerta
**Técnica:** Comprobación de efectos. **Justificación:** Identificador no registrado no bloquea login, pero avisa.
**Regla:** HU-N-02 CA6. **Resultado:** FALLÓ.
[Escenario](../features/hu-n-02.feature) · [Evidencia](../evidencias/G4-093.html)
```gherkin
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826',dispositivo_id:'dispositivo-no-registrado'}, null, {})
* match r.statusCode == 200
* def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
* assert JSON.stringify(r.result).toLowerCase().indexOf('nuevo dispositivo') >= 0
```


## HU-N-03 — Cerrar sesión · Prioridad Alta

**Como** cliente **quiero** cerrar mi sesión **para** que nadie use mi cuenta desde este equipo.
- **CA1.** Al cerrar sesión, el token deja de ser válido: cualquier uso posterior responde 401.
- **CA2.** Cerrar sesión no afecta mis otras sesiones activas.

### G4-074 — Cerrar sesión revoca solo ese token
**Técnica:** Transición de estados. **Justificación:** Dos sesiones; revocación de una no afecta la otra.
**Regla:** HU-N-03. **Resultado:** FALLÓ.
[Escenario](../features/hu-n-03.feature) · [Evidencia](../evidencias/G4-074.html)
```gherkin
* def second = login(a)
* def r = req('/api/auth/logout', 'POST', null, a.token, {})
* match r.statusCode == 204
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.statusCode == 401
* match r.result.codigo == 'NO_AUTENTICADO'
* def r = req('/api/cuentas/me/saldo', 'GET', null, second, {})
* match r.statusCode == 200
```

### G4-094 — Cerrar una sesión no afecta otra
**Técnica:** Transición de estados. **Justificación:** Separado del caso de revocación para que su fallo no oculte este criterio.
**Regla:** HU-N-03 CA2. **Resultado:** APROBADO.
[Escenario](../features/hu-n-03.feature) · [Evidencia](../evidencias/G4-094.html)
```gherkin
* def second = login(a)
* def r = req('/api/auth/logout', 'POST', null, a.token, {})
* match r.statusCode == 204
* def r = req('/api/cuentas/me/saldo', 'GET', null, second, {})
* match r.statusCode == 200
```


## HU-N-04 — Consultar mi saldo y perfil · Prioridad Alta

- **CA1.** Veo mi saldo disponible, la moneda (PEN) y la fecha de la última actualización.
- **CA2.** Veo mi perfil: nombres, celular, correo y DNI **enmascarado** (solo los últimos 4 dígitos).
- **CA3.** Sin token o con token vencido o inválido *(error `NO_AUTENTICADO`, 401)*.

### G4-075 — Saldo PEN y perfil enmascarado
**Técnica:** Comprobación de efectos. **Justificación:** No revelar DNI completo.
**Regla:** HU-N-04. **Resultado:** APROBADO.
[Escenario](../features/hu-n-04.feature) · [Evidencia](../evidencias/G4-075.html)
```gherkin
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.statusCode == 200
* match r.result.moneda == 'PEN'
* match r.result.actualizado_en == "#string"
* def r = req('/api/cuentas/me', 'GET', null, a.token, {})
* match r.statusCode == 200
* assert r.result.dni.startsWith('****')
* match r.result.celular == a.cell
```

### G4-076 — Acceso sin autenticación null
**Técnica:** Particiones de equivalencia. **Justificación:** Ausente e inválido son clases diferentes.
**Regla:** HU-N-04 CA3. **Resultado:** APROBADO.
[Escenario](../features/hu-n-04.feature) · [Evidencia](../evidencias/G4-076.html)
```gherkin
* def r = req('/api/cuentas/me/saldo', 'GET', null, null, {})
* match r.statusCode == 401
* match r.result.codigo == 'NO_AUTENTICADO'
```

### G4-077 — Acceso sin autenticación 'invalid'
**Técnica:** Particiones de equivalencia. **Justificación:** Ausente e inválido son clases diferentes.
**Regla:** HU-N-04 CA3. **Resultado:** APROBADO.
[Escenario](../features/hu-n-04.feature) · [Evidencia](../evidencias/G4-077.html)
```gherkin
* def r = req('/api/cuentas/me/saldo', 'GET', null, 'invalid', {})
* match r.statusCode == 401
* match r.result.codigo == 'NO_AUTENTICADO'
```

### G4-078 — Token vencido
**Técnica:** Valores límite (2 puntos). **Justificación:** A los 30 min debe rechazarse.
**Regla:** HU-N-04 CA3. **Resultado:** APROBADO.
[Escenario](../features/hu-n-04.feature) · [Evidencia](../evidencias/G4-078.html)
```gherkin
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:30}, null, {})
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.statusCode == 401
* match r.result.codigo == 'NO_AUTENTICADO'
```


## HU-N-05 — Editar mi perfil · Prioridad Media

**Como** cliente **quiero** actualizar mis nombres y mi correo **para** mantener mis datos al día.
- **CA1.** Puedo modificar nombres (2 a 80 caracteres) y correo (formato válido, único entre cuentas activas sin distinguir mayúsculas) *(errores `PERFIL_INVALIDO`, `CORREO_INVALIDO`, `CORREO_REGISTRADO` 409)*.
- **CA2.** El DNI y el celular **no** se pueden modificar: si se envían, se ignoran.
- **CA3.** Al cambiar el correo se envía un SMS de aviso.

### G4-079 — Editar perfil ignora DNI y celular y envía SMS
**Técnica:** Comprobación de efectos. **Justificación:** Actualizar permitidos sin cambiar identidad.
**Regla:** HU-N-05. **Resultado:** APROBADO.
[Escenario](../features/hu-n-05.feature) · [Evidencia](../evidencias/G4-079.html)
```gherkin
* def r = req('/api/cuentas/me', 'PUT', {nombres:'Granit Actualizado',correo:'#(a.cell + "@example.com")',dni:'11111111',celular:'999999999'}, a.token, {})
* match r.statusCode == 200
* match r.result.nombres == 'Granit Actualizado'
* match r.result.celular == a.cell
* def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
* assert r.result.length >= 2
```


## HU-N-06 — Cerrar mi cuenta · Prioridad Media

**Como** cliente **quiero** cerrar mi cuenta **para** dejar de usar Qolqe.
- **CA1.** Debo confirmar con mi PIN *(error `PIN_INCORRECTO`)*.
- **CA2.** Solo puedo cerrarla con saldo exactamente S/ 0.00 *(error `SALDO_PENDIENTE`)*.
- **CA3.** No puedo cerrarla si tengo solicitudes de dinero pendientes (no vencidas), enviadas o recibidas *(error `SOLICITUDES_PENDIENTES`, 409)*.
- **CA4.** Al cerrarla, todas mis sesiones se cierran, no puedo volver a ingresar y nadie puede transferirme (RN-07).

### G4-080 — Cerrar cuenta con saldo cero revoca acceso
**Técnica:** Transición de estados. **Justificación:** Cierre válido y posterior login prohibido.
**Regla:** HU-N-06. **Resultado:** FALLÓ.
[Escenario](../features/hu-n-06.feature) · [Evidencia](../evidencias/G4-080.html)
```gherkin
* def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
* match r.statusCode == 204
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.statusCode == 401
* def r = req('/api/auth/login', 'POST', {celular:'#(a.cell)',pin:'4826'}, null, {})
* match r.statusCode == 401
* match r.result.codigo == 'CUENTA_CERRADA'
```

### G4-081 — Solicitud pendiente impide cerrar cuenta
**Técnica:** Tabla de decisiones. **Justificación:** Saldo cero pero solicitud pendiente: rechazo de cierre.
**Regla:** HU-N-06 CA3. **Resultado:** APROBADO.
[Escenario](../features/hu-n-06.feature) · [Evidencia](../evidencias/G4-081.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'SOLICITUDES_PENDIENTES'
```

### G4-112 — PIN incorrecto impide cierre
**Técnica:** Particiones de equivalencia. **Justificación:** Saldo cero, PIN incorrecto; conservar cuenta activa.
**Regla:** HU-N-06 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-n-06.feature) · [Evidencia](../evidencias/G4-112.html)
```gherkin
* def r = req('/api/cuentas/me/cierre', 'POST', {pin:'0000'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'PIN_INCORRECTO'
* def r = req('/api/cuentas/me', 'GET', null, a.token, {})
* match r.statusCode == 200
```

### G4-113 — Saldo pendiente impide cierre
**Técnica:** Particiones de equivalencia. **Justificación:** PIN correcto y saldo positivo.
**Regla:** HU-N-06 CA2. **Resultado:** APROBADO.
[Escenario](../features/hu-n-06.feature) · [Evidencia](../evidencias/G4-113.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'0.01'}, null, {})
* def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'SALDO_PENDIENTE'
```


## HU-N-07 — Transferir a otro usuario Qolqe · Prioridad Alta

**Como** cliente **quiero** enviar dinero a otro celular de Qolqe **para** pagarle de inmediato.
- **CA1.** Indico el celular de destino (o un contacto) y el monto; opcionalmente una descripción de hasta 60 caracteres.
- **CA2.** Se validan RN-05, RN-06, RN-07 y RN-08 *(errores `MONTO_INVALIDO`, `LIMITE_DIARIO_EXCEDIDO`, `TRANSFERENCIA_A_SI_MISMO`, `DESTINO_NO_REGISTRADO` 404, `DESTINO_INACTIVO`, `SALDO_INSUFICIENTE`)*.
- **CA3.** Si es exitosa: se debita mi saldo, se acredita al destinatario, ambos vemos el movimiento con el mismo código (RN-10) y el destinatario recibe un SMS.
- **CA4.** El comprobante muestra el código de operación, el destinatario (nombre enmascarado y celular), el monto, la comisión, el total, mi nuevo saldo y la fecha.
- **CA5.** Las reglas se cumplen **también bajo concurrencia**: varias transferencias simultáneas no pueden superar el límite diario ni dejar el saldo negativo.

### G4-082 — Transferencia monto 0.00
**Técnica:** Valores límite (2 puntos). **Justificación:** Probar rango financiero con saldo y destinatario válidos.
**Regla:** RN-05. **Resultado:** APROBADO.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-082.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'0.00'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'MONTO_INVALIDO'
```

### G4-083 — Transferencia monto 0.01
**Técnica:** Valores límite (2 puntos). **Justificación:** Probar rango financiero con saldo y destinatario válidos.
**Regla:** RN-05. **Resultado:** APROBADO.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-083.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'0.01'}, a.token, {})
* match r.statusCode == 201
```

### G4-084 — Transferencia monto 500.00
**Técnica:** Valores límite (2 puntos). **Justificación:** Probar rango financiero con saldo y destinatario válidos.
**Regla:** RN-05. **Resultado:** APROBADO.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-084.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'500.00'}, a.token, {})
* match r.statusCode == 201
```

### G4-085 — Transferencia monto 500.01
**Técnica:** Valores límite (2 puntos). **Justificación:** Probar rango financiero con saldo y destinatario válidos.
**Regla:** RN-05. **Resultado:** APROBADO.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-085.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'500.01'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'MONTO_INVALIDO'
```

### G4-086 — Transferencia monto 10.005
**Técnica:** Valores límite (2 puntos). **Justificación:** Probar rango financiero con saldo y destinatario válidos.
**Regla:** RN-05. **Resultado:** APROBADO.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-086.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'10.005'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'MONTO_INVALIDO'
```

### G4-087 — Comprobante y movimientos con mismo código
**Técnica:** Comprobación de efectos. **Justificación:** Verificar transferencia en ambas cuentas.
**Regla:** RN-10. **Resultado:** APROBADO.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-087.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'100.00'}, null, {})
* def tx = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'10.00',descripcion:'Almuerzo'}, a.token, {})
* match tx.statusCode == 201
* match tx.result.total == '10.00'
* match tx.result.saldo == '90.00'
* def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, a.token, {})
* match r.statusCode == 200
* def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, b.token, {})
* match r.statusCode == 200
```

### G4-114 — Transferencia a sí mismo rechazada
**Técnica:** Particiones de equivalencia. **Justificación:** Monto válido y saldo suficiente; aislar destino.
**Regla:** RN-07. **Resultado:** APROBADO.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-114.html)
```gherkin
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(a.cell)',monto:'10.00'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'TRANSFERENCIA_A_SI_MISMO'
```

### G4-116 — Concurrencia conserva saldo y límite diario
**Técnica:** Tabla de decisiones y concurrencia. **Justificación:** Dos peticiones HTTP sincronizadas; comprobar límite y saldo por separado. Los reintentos de preparación, si ocurren, quedan en la evidencia.
**Regla:** RN-06/08. **Resultado:** FALLÓ.
[Escenario](../features/hu-n-07.feature) · [Evidencia](../evidencias/G4-116.html)
```gherkin
* def command = ['#(qaPython)', 'scripts/concurrency_probe.py']
* def runProbe = function(args){var P=Java.type('java.lang.ProcessBuilder');var S=Java.type('java.util.Scanner');var p=new P(Java.to(args,'java.lang.String[]')).redirectErrorStream(true).start();var scan=new S(p.getInputStream()).useDelimiter('\\A');var out=scan.hasNext()?scan.next():'';var code=p.waitFor();if(code!=0) throw new Error('Preparación de concurrencia: '+out);return JSON.parse(out);}
* def probe = runProbe(command)
* eval karate.embed(probe, 'application/json')
* match probe.ok == true
```


## HU-N-08 — Transferir a otro banco · Prioridad Alta

- **CA1.** Indico un CCI de 20 dígitos *(error `CCI_INVALIDO`)* y el monto.
- **CA2.** Se cobra la comisión de RN-09 y se aplican RN-05, RN-06 y RN-08.
- **CA3.** El movimiento muestra el CCI enmascarado (solo los últimos 4 dígitos).

### G4-088 — Transferencia interbancaria cobra comisión y enmascara CCI
**Técnica:** Comprobación de efectos. **Justificación:** Monto 100: comisión 1.50; verificar CCI en movimiento.
**Regla:** RN-09. **Resultado:** APROBADO.
[Escenario](../features/hu-n-08.feature) · [Evidencia](../evidencias/G4-088.html)
```gherkin
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'200.00'}, null, {})
* def tx = req('/api/transferencias', 'POST', {tipo:'INTERBANCARIA',cci:'12345678901234567890',monto:'100.00'}, a.token, {})
* match tx.statusCode == 201
* match tx.result.comision == '1.50'
* match tx.result.saldo == '98.50'
* def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, a.token, {})
* match r.statusCode == 200
* match r.result.contraparte == '****************7890'
```

### G4-115 — CCI inválido rechazado
**Técnica:** Particiones de equivalencia. **Justificación:** CCI corto con monto válido.
**Regla:** HU-N-08 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-n-08.feature) · [Evidencia](../evidencias/G4-115.html)
```gherkin
* def r = req('/api/transferencias', 'POST', {tipo:'INTERBANCARIA',cci:'123',monto:'10.00'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'CCI_INVALIDO'
```


## HU-N-09 — Simular la comisión · Prioridad Media

- **CA1.** Antes de transferir puedo ver el monto, la comisión y el total según el tipo de transferencia, sin que se realice ninguna operación.

### G4-089 — Simular comisión para 1.00 sin debitar
**Técnica:** Particiones de equivalencia. **Justificación:** Mínimo, proporcional y máximo; saldo no cambia.
**Regla:** RN-09. **Resultado:** APROBADO.
[Escenario](../features/hu-n-09.feature) · [Evidencia](../evidencias/G4-089.html)
```gherkin
* def r = req('/api/transferencias/comision', 'GET', null, a.token, {monto:'1.00',tipo:'INTERBANCARIA'})
* match r.statusCode == 200
* match r.result.comision == '1.00'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '0.00'
```

### G4-090 — Simular comisión para 100.00 sin debitar
**Técnica:** Particiones de equivalencia. **Justificación:** Mínimo, proporcional y máximo; saldo no cambia.
**Regla:** RN-09. **Resultado:** APROBADO.
[Escenario](../features/hu-n-09.feature) · [Evidencia](../evidencias/G4-090.html)
```gherkin
* def r = req('/api/transferencias/comision', 'GET', null, a.token, {monto:'100.00',tipo:'INTERBANCARIA'})
* match r.statusCode == 200
* match r.result.comision == '1.50'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '0.00'
```

### G4-091 — Simular comisión para 500.00 sin debitar
**Técnica:** Particiones de equivalencia. **Justificación:** Mínimo, proporcional y máximo; saldo no cambia.
**Regla:** RN-09. **Resultado:** APROBADO.
[Escenario](../features/hu-n-09.feature) · [Evidencia](../evidencias/G4-091.html)
```gherkin
* def r = req('/api/transferencias/comision', 'GET', null, a.token, {monto:'500.00',tipo:'INTERBANCARIA'})
* match r.statusCode == 200
* match r.result.comision == '5.00'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '0.00'
```


## HU-G4-01 — Agregar un contacto · Prioridad Alta

- **CA1.** Indico el celular y un alias. Se aplican R-G4-01 a R-G4-03 *(errores `CELULAR_INVALIDO`, `CONTACTO_PROPIO`, `CELULAR_NO_REGISTRADO` 404, `CONTACTO_EXISTENTE` 409, `ALIAS_INVALIDO`, `ALIAS_DUPLICADO` 409, `LIMITE_CONTACTOS`)*. Un celular de una cuenta cerrada se trata como no registrado.

### G4-001 — Crear contacto con alias 'Ana'
**Técnica:** Valores límite (2 puntos). **Justificación:** Alias permitido; celular activo, ajeno y lista vacía.
**Regla:** R-G4-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-001.html)
```gherkin
* def r = add(b.cell, "Ana", a.token)
* match r.statusCode == 201
* match r.result.alias == "Ana"
* match r.result.favorito == false
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-002 — Crear contacto con alias 'AAAAAAAAAAAAAAAAAAAA'
**Técnica:** Valores límite (2 puntos). **Justificación:** Alias permitido; celular activo, ajeno y lista vacía.
**Regla:** R-G4-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-002.html)
```gherkin
* def r = add(b.cell, "AAAAAAAAAAAAAAAAAAAA", a.token)
* match r.statusCode == 201
* match r.result.alias == "AAAAAAAAAAAAAAAAAAAA"
* match r.result.favorito == false
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-003 — Crear contacto con alias 'José'
**Técnica:** Particiones de equivalencia. **Justificación:** Alias permitido; celular activo, ajeno y lista vacía.
**Regla:** R-G4-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-003.html)
```gherkin
* def r = add(b.cell, "José", a.token)
* match r.statusCode == 201
* match r.result.alias == "José"
* match r.result.favorito == false
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-004 — Crear contacto con alias 'Niño'
**Técnica:** Particiones de equivalencia. **Justificación:** Alias permitido; celular activo, ajeno y lista vacía.
**Regla:** R-G4-01/02/03. **Resultado:** FALLÓ.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-004.html)
```gherkin
* def r = add(b.cell, "Niño", a.token)
* match r.statusCode == 201
* match r.result.alias == "Niño"
* match r.result.favorito == false
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-005 — Crear contacto con alias 'A1 B'
**Técnica:** Particiones de equivalencia. **Justificación:** Alias permitido; celular activo, ajeno y lista vacía.
**Regla:** R-G4-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-005.html)
```gherkin
* def r = add(b.cell, "A1 B", a.token)
* match r.statusCode == 201
* match r.result.alias == "A1 B"
* match r.result.favorito == false
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-006 — Crear contacto con alias ' Ana '
**Técnica:** Particiones de equivalencia. **Justificación:** Alias permitido; celular activo, ajeno y lista vacía.
**Regla:** R-G4-01/02/03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-006.html)
```gherkin
* def r = add(b.cell, " Ana ", a.token)
* match r.statusCode == 201
* match r.result.alias == "Ana"
* match r.result.favorito == false
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-007 — Rechazar alias 'Lu'
**Técnica:** Valores límite (2 puntos). **Justificación:** Frontera o clase inválida, restantes condiciones válidas.
**Regla:** R-G4-02. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-007.html)
```gherkin
* def r = add(b.cell, "Lu", a.token)
* match r.statusCode == 422
* match r.result.codigo == 'ALIAS_INVALIDO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-008 — Rechazar alias 'AAAAAAAAAAAAAAAAAAAAA'
**Técnica:** Valores límite (2 puntos). **Justificación:** Frontera o clase inválida, restantes condiciones válidas.
**Regla:** R-G4-02. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-008.html)
```gherkin
* def r = add(b.cell, "AAAAAAAAAAAAAAAAAAAAA", a.token)
* match r.statusCode == 422
* match r.result.codigo == 'ALIAS_INVALIDO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-009 — Rechazar alias ''
**Técnica:** Particiones de equivalencia. **Justificación:** Frontera o clase inválida, restantes condiciones válidas.
**Regla:** R-G4-02. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-009.html)
```gherkin
* def r = add(b.cell, "", a.token)
* match r.statusCode == 422
* match r.result.codigo == 'ALIAS_INVALIDO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-010 — Rechazar alias '   '
**Técnica:** Particiones de equivalencia. **Justificación:** Frontera o clase inválida, restantes condiciones válidas.
**Regla:** R-G4-02. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-010.html)
```gherkin
* def r = add(b.cell, "   ", a.token)
* match r.statusCode == 422
* match r.result.codigo == 'ALIAS_INVALIDO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-011 — Rechazar alias 'Ana@'
**Técnica:** Particiones de equivalencia. **Justificación:** Frontera o clase inválida, restantes condiciones válidas.
**Regla:** R-G4-02. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-011.html)
```gherkin
* def r = add(b.cell, "Ana@", a.token)
* match r.statusCode == 422
* match r.result.codigo == 'ALIAS_INVALIDO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-012 — Rechazar celular: CONTACTO_PROPIO
**Técnica:** Particiones de equivalencia. **Justificación:** Representante de una condición distinta de negocio.
**Regla:** R-G4-01. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-012.html)
```gherkin
* def r = add(a.cell, 'Ana', a.token)
* match r.statusCode == 422
* match r.result.codigo == 'CONTACTO_PROPIO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-013 — Rechazar celular: CELULAR_INVALIDO
**Técnica:** Particiones de equivalencia. **Justificación:** Representante de una condición distinta de negocio.
**Regla:** R-G4-01. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-013.html)
```gherkin
* def r = add('123', 'Ana', a.token)
* match r.statusCode == 422
* match r.result.codigo == 'CELULAR_INVALIDO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-014 — Rechazar celular: CELULAR_NO_REGISTRADO
**Técnica:** Particiones de equivalencia. **Justificación:** Representante de una condición distinta de negocio.
**Regla:** R-G4-01. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-014.html)
```gherkin
* def r = add('934567812', 'Ana', a.token)
* match r.statusCode == 404
* match r.result.codigo == 'CELULAR_NO_REGISTRADO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-015 — Celular válido sin registro
**Técnica:** Particiones de equivalencia. **Justificación:** Cerrar una cuenta propia de contexto no reutiliza datos ajenos.
**Regla:** R-G4-01. **Resultado:** FALLÓ.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-015.html)
```gherkin
* def r = req('/api/cuentas/me/cierre', 'POST', {pin:'4826'}, b.token, {})
* match r.statusCode == 204
* def r = add(b.cell, 'Ana', a.token)
* match r.statusCode == 404
* match r.result.codigo == 'CELULAR_NO_REGISTRADO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```

### G4-016 — Contacto duplicado
**Técnica:** Particiones de equivalencia. **Justificación:** Mismo celular con otro alias.
**Regla:** R-G4-01. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-016.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = add(b.cell, 'Otro', a.token)
* match r.statusCode == 409
* match r.result.codigo == 'CONTACTO_EXISTENTE'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-017 — Alias duplicado tras normalizar 'ANA'
**Técnica:** Particiones de equivalencia. **Justificación:** Unicidad se comprueba sin mayúsculas y tras recortar espacios.
**Regla:** R-G4-02. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-017.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = add(c.cell, "ANA", a.token)
* match r.statusCode == 409
* match r.result.codigo == 'ALIAS_DUPLICADO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-018 — Alias duplicado tras normalizar ' Ana '
**Técnica:** Particiones de equivalencia. **Justificación:** Unicidad se comprueba sin mayúsculas y tras recortar espacios.
**Regla:** R-G4-02. **Resultado:** FALLÓ.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-018.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = add(c.cell, " Ana ", a.token)
* match r.statusCode == 409
* match r.result.codigo == 'ALIAS_DUPLICADO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-019 — Permitir contacto 15 y rechazar contacto 16
**Técnica:** Valores límite (2 puntos). **Justificación:** Contexto con 14; comprobar frontera y ausencia de efecto al superar 15.
**Regla:** R-G4-03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-019.html)
```gherkin
* def fill = function(n){ for(var i=0;i<n;i++){ var u=create('Contacto ' + i); var x=add(u.cell,'Contacto ' + i,a.token); if(x.statusCode!=201) karate.fail('Contexto capacidad: '+JSON.stringify(x.result)); } }
* eval fill(14)
* def r = add(b.cell, 'Ana', a.token)
* match r.statusCode == 201
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 15
* def r = add(c.cell, 'Franco', a.token)
* match r.statusCode == 422
* match r.result.codigo == 'LIMITE_CONTACTOS'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 15
```

### G4-106 — Celular válido aún no registrado
**Técnica:** Particiones de equivalencia. **Justificación:** Crear valor nuevo sin registrar; separado de cuenta cerrada.
**Regla:** R-G4-01. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-01.feature) · [Evidencia](../evidencias/G4-106.html)
```gherkin
* def unknown = '9' + random()
* def r = add(unknown, 'Ana', a.token)
* match r.statusCode == 404
* match r.result.codigo == 'CELULAR_NO_REGISTRADO'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```


## HU-G4-02 — Ver y buscar mis contactos · Prioridad Media

- **CA1.** Veo mis contactos: primero los favoritos y luego el resto, ordenados por alias. 10 por página, indicando el total.
- **CA2.** Puedo buscar por parte del alias, sin distinguir mayúsculas ni tildes ("jose" encuentra "José").
- **CA3.** Cada contacto muestra alias, nombre enmascarado, celular y si es favorito.

### G4-020 — Buscar ignorando mayúsculas y tildes
**Técnica:** Particiones de equivalencia. **Justificación:** José debe coincidir con JOSE; se verifica máscara, teléfono y favorito.
**Regla:** HU-G4-02 CA2/3. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-02.feature) · [Evidencia](../evidencias/G4-020.html)
```gherkin
* def r = add(b.cell, 'José', a.token)
* def r = req('/api/contactos', 'GET', null, a.token, {buscar:'JOSE'})
* match r.statusCode == 200
* match r.result.total == 1
* match r.result.contactos[0].alias == 'José'
* match r.result.contactos[0].celular == b.cell
* match r.result.contactos[0].favorito == false
* match r.result.contactos[0].nombre == 'Franco P.'
```

### G4-021 — Ordenar favoritos antes del resto
**Técnica:** Particiones de equivalencia. **Justificación:** Favorito con alias Z debe preceder a alias A no favorito.
**Regla:** HU-G4-02 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-02.feature) · [Evidencia](../evidencias/G4-021.html)
```gherkin
* def z = add(b.cell, 'Zeta', a.token)
* def r = add(c.cell, 'Alfa', a.token)
* def r = req('/api/contactos/' + z.result.id + '', 'PUT', {favorito:true}, a.token, {})
* match r.statusCode == 200
* def r = req('/api/contactos', 'GET', null, a.token, {})
* match r.result.contactos[*].alias == ['Zeta','Alfa']
```

### G4-022 — Paginación con 11 contactos
**Técnica:** Valores límite (2 puntos). **Justificación:** 10/11 distingue primera y segunda página.
**Regla:** HU-G4-02 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-02.feature) · [Evidencia](../evidencias/G4-022.html)
```gherkin
* def fill = function(n){ for(var i=0;i<n;i++){ var u=create('Contacto ' + i); var x=add(u.cell,'Contacto ' + i,a.token); if(x.statusCode!=201) karate.fail('Contexto capacidad: '+JSON.stringify(x.result)); } }
* eval fill(11)
* def r = req('/api/contactos', 'GET', null, a.token, {})
* match r.statusCode == 200
* match r.result.total == 11
* match r.result.total_paginas == 2
* match r.result.contactos == "#[10]"
* def r = req('/api/contactos', 'GET', null, a.token, {pagina:2})
* match r.statusCode == 200
* match r.result.contactos == "#[1]"
```

### G4-023 — Búsqueda sin coincidencias
**Técnica:** Particiones de equivalencia. **Justificación:** Consulta válida sin coincidencias devuelve lista vacía.
**Regla:** HU-G4-02 CA2. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-02.feature) · [Evidencia](../evidencias/G4-023.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/contactos', 'GET', null, a.token, {buscar:'Inexistente'})
* match r.statusCode == 200
* match r.result.contactos == []
```

### G4-107 — Orden alfabético dentro de cada grupo
**Técnica:** Particiones de equivalencia. **Justificación:** Cuatro alias comprueban ambos grupos y prioridad de favoritos.
**Regla:** HU-G4-02 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-02.feature) · [Evidencia](../evidencias/G4-107.html)
```gherkin
* def u = create('Cuarto Usuario')
* def z = add(b.cell, 'Zeta', a.token)
* def x = add(c.cell, 'Alfa', a.token)
* def r = add(u.cell, 'Beta', a.token)
* def v = create('Quinto Usuario')
* def r = add(v.cell, 'Gamma', a.token)
* def r = req('/api/contactos/' + z.result.id + '', 'PUT', {favorito:true}, a.token, {})
* def r = req('/api/contactos/' + x.result.id + '', 'PUT', {favorito:true}, a.token, {})
* def r = req('/api/contactos', 'GET', null, a.token, {})
* match r.result.contactos[*].alias == ['Alfa','Zeta','Beta','Gamma']
```


## HU-G4-03 — Editar un contacto · Prioridad Media

- **CA1.** Puedo cambiar el alias (R-G4-02, sin compararlo consigo mismo) y marcarlo o desmarcarlo como favorito (R-G4-03 *(error `LIMITE_FAVORITOS`)*).

### G4-024 — Editar alias sin compararlo consigo mismo
**Técnica:** Particiones de equivalencia. **Justificación:** Mantener el mismo alias no debe ser duplicado; celular se conserva.
**Regla:** R-G4-02. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-03.feature) · [Evidencia](../evidencias/G4-024.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {alias:'Ana'}, a.token, {})
* match r.statusCode == 200
* match r.result.alias == 'Ana'
* match r.result.celular == b.cell
```

### G4-025 — Marcar y desmarcar favorito
**Técnica:** Transición de estados. **Justificación:** Ambas acciones conservan alias y celular.
**Regla:** R-G4-03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-03.feature) · [Evidencia](../evidencias/G4-025.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {favorito:true}, a.token, {})
* match r.statusCode == 200
* match r.result.favorito == true
* def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {favorito:false}, a.token, {})
* match r.statusCode == 200
* match r.result.favorito == false
* match r.result.alias == 'Ana'
```

### G4-026 — Quinto favorito permitido; sexto rechazado
**Técnica:** Valores límite (2 puntos). **Justificación:** Verificar 5/6 y que el sexto conserve estado no favorito.
**Regla:** R-G4-03. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-03.feature) · [Evidencia](../evidencias/G4-026.html)
```gherkin
* def ids = []
* def populate = function(){for(var i=0;i<6;i++){var u=create('Favorito '+i); var x=add(u.cell,'Favorito '+i,a.token); karate.appendTo(ids,x.result.id);}}
* eval populate()
* def mark = function(){for(var i=0;i<5;i++){var x=req('/api/contactos/'+ids[i],'PUT',{favorito:true},a.token,{}); if(x.statusCode!=200) karate.fail('Contexto favorito');}}
* eval mark()
* def r = req('/api/contactos/' + ids[5] + '', 'PUT', {favorito:true}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'LIMITE_FAVORITOS'
* def r = req('/api/contactos', 'GET', null, a.token, {})
* match r.result.contactos[5].favorito == false
```

### G4-027 — Rechazar edición de contacto ajeno
**Técnica:** Particiones de equivalencia. **Justificación:** Un tercero no puede editar un recurso ajeno.
**Regla:** Propiedad de datos. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-03.feature) · [Evidencia](../evidencias/G4-027.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {alias:'Otro'}, c.token, {})
* match r.statusCode == 404
* match r.result.codigo == 'CONTACTO_NO_ENCONTRADO'
```

### G4-108 — Editar solo alias conserva favorito
**Técnica:** Comprobación de efectos. **Justificación:** No basta verificar el campo cambiado.
**Regla:** HU-G4-03 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-03.feature) · [Evidencia](../evidencias/G4-108.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {favorito:true}, a.token, {})
* match r.statusCode == 200
* def r = req('/api/contactos/' + contact.result.id + '', 'PUT', {alias:'Nuevo Alias'}, a.token, {})
* match r.statusCode == 200
* match r.result.favorito == true
* match r.result.celular == b.cell
```


## HU-G4-04 — Eliminar un contacto · Prioridad Baja

- **CA1.** El contacto se elimina de mi lista. Las transferencias realizadas se conservan.
- **CA2.** No puedo eliminar un contacto con el que tengo solicitudes PENDIENTES (no vencidas), enviadas o recibidas *(error `SOLICITUDES_PENDIENTES`, 409)*.

### G4-028 — Eliminar contacto conserva transferencia
**Técnica:** Comprobación de efectos. **Justificación:** Transferir, eliminar y consultar movimiento por código.
**Regla:** RN-11. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-04.feature) · [Evidencia](../evidencias/G4-028.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'100.00'}, null, {})
* def tx = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
* match tx.statusCode == 201
* def r = req('/api/contactos/' + contact.result.id + '', 'DELETE', null, a.token, {})
* match r.statusCode == 204
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
* def r = req('/api/movimientos/' + tx.result.codigo_operacion + '', 'GET', null, a.token, {})
* match r.statusCode == 200
```

### G4-029 — Solicitud pendiente enviada impide eliminar
**Técnica:** Tabla de decisiones. **Justificación:** Contacto propio y solicitud pendiente vigente.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-04.feature) · [Evidencia](../evidencias/G4-029.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/contactos/' + contact.result.id + '', 'DELETE', null, a.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'SOLICITUDES_PENDIENTES'
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 1
```

### G4-030 — Solicitud pendiente recibida impide eliminar
**Técnica:** Tabla de decisiones. **Justificación:** Comprobar dirección recibida, no solo enviada.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-04.feature) · [Evidencia](../evidencias/G4-030.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def cb = add(a.cell,'Granit',b.token)
* def r = req('/api/contactos/' + cb.result.id + '', 'DELETE', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'SOLICITUDES_PENDIENTES'
```

### G4-031 — Solicitud vencida permite eliminar
**Técnica:** Transición de estados. **Justificación:** Vencida no bloquea eliminación.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-04.feature) · [Evidencia](../evidencias/G4-031.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
* set a.token = login(a)
* def r = req('/api/contactos/' + contact.result.id + '', 'DELETE', null, a.token, {})
* match r.statusCode == 204
* def list = req('/api/contactos', 'GET', null, a.token, {})
* match list.result.total == 0
```


## HU-G4-05 — Transferir a un contacto · Prioridad Alta

- **CA1.** Puedo transferir eligiendo un contacto en lugar de escribir el celular. Aplican todas las reglas de HU-N-07.

### G4-032 — Transferir por contacto acredita ambos saldos
**Técnica:** Comprobación de efectos. **Justificación:** Cuenta origen 100, destino 0; transferencia 10 y SMS.
**Regla:** HU-N-07. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-05.feature) · [Evidencia](../evidencias/G4-032.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'100.00'}, null, {})
* def r = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
* match r.statusCode == 201
* match r.result.saldo == '90.00'
* match r.result.comision == '0.00'
* def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* match r.result.saldo == '10.00'
* def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:b.cell})
* assert r.result.length >= 2
```

### G4-033 — Saldo insuficiente no produce transferencia
**Técnica:** Particiones de equivalencia. **Justificación:** Saldo cero y monto válido; no confundir con monto inválido.
**Regla:** RN-08. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-05.feature) · [Evidencia](../evidencias/G4-033.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'SALDO_INSUFICIENTE'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '0.00'
```

### G4-095 — Límite diario agotado impide operación
**Técnica:** Tabla de decisiones. **Justificación:** Saldo suficiente pero límite agotado: aislar rechazo diario.
**Regla:** RN-06. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-05.feature) · [Evidencia](../evidencias/G4-095.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(a.cell)',saldo:'1000.00'}, null, {})
* def r = req('/api/limites', 'PUT', {limite_diario:'100.00'}, a.token, {})
* match r.statusCode == 200
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(b.cell)',monto:'100.00'}, a.token, {})
* match r.statusCode == 201
* def beforePayer = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* def beforeTarget = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* def beforeLimits = req('/api/limites', 'GET', null, a.token, {})
* def beforeMovements = req('/api/movimientos', 'GET', null, a.token, {})
* def r = req('/api/transferencias', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00'}, a.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'LIMITE_DIARIO_EXCEDIDO'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result == beforePayer.result
* def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* match r.result == beforeTarget.result
* def r = req('/api/limites', 'GET', null, a.token, {})
* match r.result.usado_hoy == beforeLimits.result.usado_hoy
* def r = req('/api/movimientos', 'GET', null, a.token, {})
* match r.result.total == beforeMovements.result.total
```


## HU-G4-06 — Solicitar dinero a un contacto · Prioridad Alta

**Como** cliente **quiero** pedirle dinero a un contacto **para** cobrarle una deuda sin tener que recordárselo.
- **CA1.** Indico el contacto, el monto y el motivo (R-G4-04) *(errores `SOLICITUD_INVALIDA`, `LIMITE_SOLICITUDES`)*.
- **CA2.** La solicitud se crea en estado PENDIENTE, con fecha de vencimiento a las 48 horas, y el destinatario recibe un SMS.

### G4-034 — Crear solicitud pendiente con vigencia 48 h y SMS
**Técnica:** Comprobación de efectos. **Justificación:** El monto pedido no debita saldo antes de aceptar.
**Regla:** R-G4-04/05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-034.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* match s.result.estado == 'PENDIENTE'
* assert (new Date(s.result.vence_en+'-05:00') - new Date(s.result.creada_en+'-05:00')) == 172800000
* def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:b.cell})
* assert r.result.length >= 2
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '0.00'
```

### G4-035 — Monto solicitado 0.00
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras monetarias y clase con demasiados decimales.
**Regla:** RN-05 / R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-035.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '0.00', 'Almuerzo')
* match r.statusCode == 422
* match r.result.codigo == 'SOLICITUD_INVALIDA'
```

### G4-036 — Monto solicitado 0.01
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras monetarias y clase con demasiados decimales.
**Regla:** RN-05 / R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-036.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '0.01', 'Almuerzo')
* match r.statusCode == 201
```

### G4-037 — Monto solicitado 500.00
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras monetarias y clase con demasiados decimales.
**Regla:** RN-05 / R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-037.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '500.00', 'Almuerzo')
* match r.statusCode == 201
```

### G4-038 — Monto solicitado 500.01
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras monetarias y clase con demasiados decimales.
**Regla:** RN-05 / R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-038.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '500.01', 'Almuerzo')
* match r.statusCode == 422
* match r.result.codigo == 'SOLICITUD_INVALIDA'
```

### G4-039 — Monto solicitado 10.005
**Técnica:** Particiones de equivalencia. **Justificación:** Fronteras monetarias y clase con demasiados decimales.
**Regla:** RN-05 / R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-039.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '10.005', 'Almuerzo')
* match r.statusCode == 422
* match r.result.codigo == 'SOLICITUD_INVALIDA'
```

### G4-040 — Motivo de 2 caracteres
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras 3/60 con monto y contacto válidos.
**Regla:** R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-040.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '10.00', 'AA')
* match r.statusCode == 422
* match r.result.codigo == 'SOLICITUD_INVALIDA'
```

### G4-041 — Motivo de 3 caracteres
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras 3/60 con monto y contacto válidos.
**Regla:** R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-041.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '10.00', 'AAA')
* match r.statusCode == 201
```

### G4-042 — Motivo de 60 caracteres
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras 3/60 con monto y contacto válidos.
**Regla:** R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-042.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '10.00', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
* match r.statusCode == 201
```

### G4-043 — Motivo de 61 caracteres
**Técnica:** Valores límite (2 puntos). **Justificación:** Fronteras 3/60 con monto y contacto válidos.
**Regla:** R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-043.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = requestMoney(contact.result.id, '10.00', 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
* match r.statusCode == 422
* match r.result.codigo == 'SOLICITUD_INVALIDA'
```

### G4-044 — Décima pendiente permitida y undécima rechazada
**Técnica:** Valores límite (2 puntos). **Justificación:** Límite independiente del número de contactos.
**Regla:** R-G4-04. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-044.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def fillRequests = function(){for(var i=0;i<9;i++){var x=requestMoney(contact.result.id,'10.00','Almuerzo'); if(x.statusCode!=201) karate.fail('Contexto solicitudes');}}
* eval fillRequests()
* def r = requestMoney(contact.result.id,'10.00','Almuerzo')
* match r.statusCode == 201
* def r = requestMoney(contact.result.id,'10.00','Almuerzo')
* match r.statusCode == 422
* match r.result.codigo == 'LIMITE_SOLICITUDES'
```

### G4-109 — Contacto de otro usuario no permite solicitar
**Técnica:** Particiones de equivalencia. **Justificación:** Un id válido ajeno debe ser tratado como inexistente.
**Regla:** Propiedad de datos. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-06.feature) · [Evidencia](../evidencias/G4-109.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def r = req('/api/solicitudes', 'POST', {contacto_id:'#(contact.result.id)',monto:'10.00',motivo:'Almuerzo'}, c.token, {})
* match r.statusCode == 404
* match r.result.codigo == 'CONTACTO_NO_ENCONTRADO'
```


## HU-G4-07 — Ver mis solicitudes · Prioridad Media

- **CA1.** Veo las solicitudes **enviadas** y las **recibidas** por separado, y puedo filtrarlas por estado.
- **CA2.** Una solicitud PENDIENTE cuyo plazo ya pasó se muestra como **VENCIDA**.

### G4-045 — Separar solicitudes enviadas y recibidas y filtrar
**Técnica:** Particiones de equivalencia. **Justificación:** Mismo recurso aparece según rol; filtro sin coincidencias.
**Regla:** HU-G4-07 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-07.feature) · [Evidencia](../evidencias/G4-045.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes', 'GET', null, a.token, {})
* match r.result.enviadas == "#[1]"
* match r.result.recibidas == []
* def r = req('/api/solicitudes', 'GET', null, b.token, {})
* match r.result.recibidas == "#[1]"
* match r.result.enviadas == []
* def r = req('/api/solicitudes', 'GET', null, a.token, {estado:'ACEPTADA'})
* match r.result.enviadas == []
```

### G4-046 — Estado al transcurrir 2879 minutos
**Técnica:** Valores límite (3 puntos). **Justificación:** Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-07.feature) · [Evidencia](../evidencias/G4-046.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2879}, null, {})
* set a.token = login(a)
* def r = req('/api/solicitudes', 'GET', null, a.token, {})
* match r.result.enviadas[0].estado == 'PENDIENTE'
```

### G4-047 — Estado al transcurrir 2880 minutos
**Técnica:** Valores límite (3 puntos). **Justificación:** Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-07.feature) · [Evidencia](../evidencias/G4-047.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
* set a.token = login(a)
* def r = req('/api/solicitudes', 'GET', null, a.token, {})
* match r.result.enviadas[0].estado == 'VENCIDA'
```

### G4-048 — Estado al transcurrir 2881 minutos
**Técnica:** Valores límite (3 puntos). **Justificación:** Antes, exactamente y después de 48 h; renovar token porque expira a los 30 min.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-07.feature) · [Evidencia](../evidencias/G4-048.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2881}, null, {})
* set a.token = login(a)
* def r = req('/api/solicitudes', 'GET', null, a.token, {})
* match r.result.enviadas[0].estado == 'VENCIDA'
```


## HU-G4-08 — Aceptar una solicitud recibida · Prioridad Alta

- **CA1.** Al aceptar, se realiza una transferencia de mi cuenta al solicitante por el monto pedido, con **todas** las reglas de HU-N-07 (saldo, límite diario, etc.).
- **CA2.** Si la transferencia no se puede realizar, la solicitud sigue PENDIENTE y recibo el error de la transferencia.
- **CA3.** Si se realiza, la solicitud pasa a ACEPTADA, queda asociada al código de operación y el solicitante recibe un SMS.
- **CA4.** Solo el destinatario puede aceptarla (para cualquier otro usuario responde 404), y solo si está PENDIENTE y no vencida *(error `ESTADO_INVALIDO`, 409)*.

### G4-049 — Aceptar genera transferencia, código y SMS
**Técnica:** Transición de estados. **Justificación:** Destinatario vigente con saldo; vincular operación y solicitud.
**Regla:** HU-N-07 / R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-049.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 200
* match r.result.estado == 'ACEPTADA'
* match r.result.codigo_operacion == "#string"
* def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* match r.result.saldo == '90.00'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '10.00'
* def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
* assert r.result.length >= 2
```

### G4-050 — Saldo insuficiente conserva PENDIENTE
**Técnica:** Transición de estados. **Justificación:** Error financiero no resuelve solicitud.
**Regla:** RN-08 / R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-050.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'SALDO_INSUFICIENTE'
* def r = req('/api/solicitudes', 'GET', null, a.token, {})
* match r.result.enviadas[0].estado == 'PENDIENTE'
* def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* match r.result.saldo == '0.00'
```

### G4-051 — Tercero no puede aceptar
**Técnica:** Tabla de decisiones. **Justificación:** Token válido con rol ajeno devuelve 404.
**Regla:** Propiedad de datos. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-051.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, c.token, {})
* match r.statusCode == 404
* match r.result.codigo == 'SOLICITUD_NO_ENCONTRADA'
```

### G4-052 — Aceptar a los 2879 minutos
**Técnica:** Valores límite (3 puntos). **Justificación:** Vigencia se decide en la acción, no solo al listar.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-052.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2879}, null, {})
* set b.token = login(b)
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 200
```

### G4-053 — Aceptar a los 2880 minutos
**Técnica:** Valores límite (3 puntos). **Justificación:** Vigencia se decide en la acción, no solo al listar.
**Regla:** R-G4-05. **Resultado:** FALLÓ.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-053.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
* set b.token = login(b)
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-054 — Aceptar a los 2881 minutos
**Técnica:** Valores límite (3 puntos). **Justificación:** Vigencia se decide en la acción, no solo al listar.
**Regla:** R-G4-05. **Resultado:** FALLÓ.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-054.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2881}, null, {})
* set b.token = login(b)
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-055 — No aceptar dos veces
**Técnica:** Transición de estados. **Justificación:** La segunda aceptación no duplica dinero.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-055.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
* def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* match r.result.saldo == '90.00'
```

### G4-096 — Límite diario agotado impide operación
**Técnica:** Tabla de decisiones. **Justificación:** Saldo suficiente pero límite agotado: aislar rechazo diario.
**Regla:** RN-06. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-096.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/pruebas/saldo', 'PUT', {celular:'#(b.cell)',saldo:'1000.00'}, null, {})
* def r = req('/api/limites', 'PUT', {limite_diario:'100.00'}, b.token, {})
* match r.statusCode == 200
* def r = req('/api/transferencias', 'POST', {celular_destino:'#(a.cell)',monto:'100.00'}, b.token, {})
* match r.statusCode == 201
* def beforePayer = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* def beforeTarget = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* def beforeLimits = req('/api/limites', 'GET', null, b.token, {})
* def beforeMovements = req('/api/movimientos', 'GET', null, b.token, {})
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'LIMITE_DIARIO_EXCEDIDO'
* def r = req('/api/cuentas/me/saldo', 'GET', null, b.token, {})
* match r.result == beforePayer.result
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result == beforeTarget.result
* def r = req('/api/limites', 'GET', null, b.token, {})
* match r.result.usado_hoy == beforeLimits.result.usado_hoy
* def r = req('/api/movimientos', 'GET', null, b.token, {})
* match r.result.total == beforeMovements.result.total
* def r = req('/api/solicitudes', 'GET', null, a.token, {})
* match r.result.enviadas[0].id == s.result.id
* match r.result.enviadas[0].estado == 'PENDIENTE'
* match r.result.enviadas[0].codigo_operacion == null
```

### G4-097 — No aceptar desde ACEPTADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-097.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-100 — No aceptar desde RECHAZADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-100.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-103 — No aceptar desde CANCELADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-08.feature) · [Evidencia](../evidencias/G4-103.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```


## HU-G4-09 — Rechazar una solicitud recibida · Prioridad Media

- **CA1.** Puedo rechazarla con un motivo opcional de hasta 60 caracteres. Pasa a RECHAZADA y el solicitante recibe un SMS. Aplica la restricción de estado de HU-G4-08 CA4.

### G4-056 — Rechazar solicitud pendiente
**Técnica:** Transición de estados. **Justificación:** Acción del rol correcto cambia el estado sin mover dinero.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-056.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', {motivo:'No corresponde'}, b.token, {})
* match r.statusCode == 200
* match r.result.estado == 'RECHAZADA'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '0.00'
```

### G4-057 — Rechazar acción de tercero
**Técnica:** Tabla de decisiones. **Justificación:** Un usuario ajeno no puede resolver solicitudes.
**Regla:** Propiedad de datos. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-057.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', {motivo:'No corresponde'}, c.token, {})
* match r.statusCode == 404
* match r.result.codigo == 'SOLICITUD_NO_ENCONTRADA'
```

### G4-058 — No resolver solicitud vencida
**Técnica:** Transición de estados. **Justificación:** A las 48 h la acción debe ser rechazada.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-058.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
* set a.token = login(a)
* set b.token = login(b)
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', {motivo:'No corresponde'}, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-059 — No repetir resolución
**Técnica:** Transición de estados. **Justificación:** Estado terminal no admite otra resolución.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-059.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', {motivo:'No corresponde'}, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', {motivo:'No corresponde'}, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-064 — Motivo opcional y aviso al solicitante
**Técnica:** Particiones de equivalencia. **Justificación:** Omitir motivo debe estar permitido; SMS verificable.
**Regla:** HU-G4-09 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-064.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
* match r.statusCode == 200
* match r.result.motivo_rechazo == null
* def r = req('/api/pruebas/notificaciones', 'GET', null, null, {celular:a.cell})
* assert r.result.length >= 2
```

### G4-065 — Motivo de rechazo longitud 60
**Técnica:** Valores límite (2 puntos). **Justificación:** Extremo permitido y vecino inválido.
**Regla:** HU-G4-09 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-065.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', {motivo:'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'}, b.token, {})
* match r.statusCode == 200
```

### G4-066 — Motivo de rechazo longitud 61
**Técnica:** Valores límite (2 puntos). **Justificación:** Extremo permitido y vecino inválido.
**Regla:** HU-G4-09 CA1. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-066.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', {motivo:'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'}, b.token, {})
* match r.statusCode == 422
* match r.result.codigo == 'SOLICITUD_INVALIDA'
```

### G4-098 — No rechazar desde ACEPTADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-098.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-101 — No rechazar desde RECHAZADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-101.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-104 — No rechazar desde CANCELADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-09.feature) · [Evidencia](../evidencias/G4-104.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```


## HU-G4-10 — Cancelar una solicitud enviada · Prioridad Media

- **CA1.** Solo el solicitante puede cancelarla (para cualquier otro usuario responde 404), y solo si está PENDIENTE y no vencida *(error `ESTADO_INVALIDO`, 409)*. Pasa a CANCELADA.

### G4-060 — Cancelar solicitud pendiente
**Técnica:** Transición de estados. **Justificación:** Acción del rol correcto cambia el estado sin mover dinero.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-10.feature) · [Evidencia](../evidencias/G4-060.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 200
* match r.result.estado == 'CANCELADA'
* def r = req('/api/cuentas/me/saldo', 'GET', null, a.token, {})
* match r.result.saldo == '0.00'
```

### G4-061 — Rechazar acción de tercero
**Técnica:** Tabla de decisiones. **Justificación:** Un usuario ajeno no puede resolver solicitudes.
**Regla:** Propiedad de datos. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-10.feature) · [Evidencia](../evidencias/G4-061.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, c.token, {})
* match r.statusCode == 404
* match r.result.codigo == 'SOLICITUD_NO_ENCONTRADA'
```

### G4-062 — No resolver solicitud vencida
**Técnica:** Transición de estados. **Justificación:** A las 48 h la acción debe ser rechazada.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-10.feature) · [Evidencia](../evidencias/G4-062.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/pruebas/reloj', 'PUT', {avanzar_minutos:2880}, null, {})
* set a.token = login(a)
* set b.token = login(b)
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-063 — No repetir resolución
**Técnica:** Transición de estados. **Justificación:** Estado terminal no admite otra resolución.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-10.feature) · [Evidencia](../evidencias/G4-063.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-099 — No cancelar desde ACEPTADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-10.feature) · [Evidencia](../evidencias/G4-099.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/aceptar', 'POST', null, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-102 — No cancelar desde RECHAZADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-10.feature) · [Evidencia](../evidencias/G4-102.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/rechazar', 'POST', null, b.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```

### G4-105 — No cancelar desde CANCELADA
**Técnica:** Transición de estados. **Justificación:** Cubrir transición inválida desde estado terminal con rol correcto.
**Regla:** R-G4-05. **Resultado:** APROBADO.
[Escenario](../features/hu-g4-10.feature) · [Evidencia](../evidencias/G4-105.html)
```gherkin
* def contact = add(b.cell, 'Ana', a.token)
* match contact.statusCode == 201
* def s = requestMoney(contact.result.id, '10.00', 'Almuerzo')
* match s.statusCode == 201
* def fund = req('/api/pruebas/saldo', 'PUT', {celular: '#(b.cell)', saldo:'100.00'}, null, {})
* match fund.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 200
* def r = req('/api/solicitudes/' + s.result.id + '/cancelar', 'POST', null, a.token, {})
* match r.statusCode == 409
* match r.result.codigo == 'ESTADO_INVALIDO'
```
