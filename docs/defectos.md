# Defectos reproducidos

Aplicación original: `8c7d2f0c939ede7765b7b80b98c10c3905693fda`. No se modificó su código.

## D-01 — Alias con ñ rechazado
**Clasificación:** Incumplimiento funcional reproducido. **Requisito:** HU-G4-01, R-G4-01/02/03.
**Descripción:** La regla R-G4-02 admite ñ. El alta con Niño devuelve ALIAS_INVALIDO en lugar de crear el contacto.
**Reproducción automatizada:** ejecutar Karate con etiqueta `@G4-004`. El escenario prepara sus propios usuarios.
**Esperado y pasos:** [feature](../features/hu-g4-01.feature).
**Obtenido:** [registro HTTP real](../evidencias/G4-004.html).
```text
match failed: EQUALS
  $ | not equal (NUMBER:NUMBER)
  422
  201

features/hu-g4-01.feature:55
```

## D-02 — Duplicado tras recortar espacios
**Clasificación:** Incumplimiento funcional reproducido. **Requisito:** HU-G4-01, R-G4-02.
**Descripción:** Después de guardar Ana, crear otro contacto con « Ana » debe ser ALIAS_DUPLICADO. Se observa creación de un segundo alias Ana.
**Reproducción automatizada:** ejecutar Karate con etiqueta `@G4-018`. El escenario prepara sus propios usuarios.
**Esperado y pasos:** [feature](../features/hu-g4-01.feature).
**Obtenido:** [registro HTTP real](../evidencias/G4-018.html).
```text
match failed: EQUALS
  $ | not equal (NUMBER:NUMBER)
  201
  409

features/hu-g4-01.feature:192
```

## D-03 — Aceptación de solicitud vencida
**Clasificación:** Incumplimiento funcional reproducido. **Requisito:** HU-G4-08, R-G4-05.
**Descripción:** A las 48 horas se espera ESTADO_INVALIDO, 409, sin transferencia. La aceptación realiza la transferencia.
**Reproducción automatizada:** ejecutar Karate con etiqueta `@G4-053`. El escenario prepara sus propios usuarios.
**Esperado y pasos:** [feature](../features/hu-g4-08.feature).
**Obtenido:** [registro HTTP real](../evidencias/G4-053.html).
```text
match failed: EQUALS
  $ | not equal (NUMBER:NUMBER)
  200
  409

features/hu-g4-08.feature:93
```

## D-04 — Token sigue válido después de logout
**Clasificación:** Incumplimiento funcional reproducido. **Requisito:** HU-N-03, HU-N-03.
**Descripción:** HU-N-03 exige revocación inmediata. Tras logout, la consulta de saldo con el mismo token sigue respondiendo 200.
**Reproducción automatizada:** ejecutar Karate con etiqueta `@G4-074`. El escenario prepara sus propios usuarios.
**Esperado y pasos:** [feature](../features/hu-n-03.feature).
**Obtenido:** [registro HTTP real](../evidencias/G4-074.html).
```text
match failed: EQUALS
  $ | not equal (NUMBER:NUMBER)
  200
  401

features/hu-n-03.feature:28
```

## D-05 — Concurrencia supera saldo y límite diario
**Clasificación:** Incumplimiento funcional reproducido. **Requisito:** HU-N-07, RN-06/08.
**Descripción:** Dos transferencias de 400 simultáneas: con saldo inicial 500 se observaron dos éxitos y saldo -300; con saldo 2000 y límite 500 se observaron 800 usados. Ver reports/concurrencia.json.
**Reproducción automatizada:** ejecutar Karate con etiqueta `@G4-116`. El escenario prepara sus propios usuarios.
**Esperado y pasos:** [feature](../features/hu-n-07.feature).
**Obtenido:** [registro HTTP real](../evidencias/G4-116.html).
```text
match failed: EQUALS
  $ | not equal (BOOLEAN:BOOLEAN)
  false
  true

features/hu-n-07.feature:85
```

## Clasificación pendiente
Los demás fallos se investigan por separado: no se atribuyen automáticamente a la aplicación. La implementación puede confirmar una hipótesis de causa, pero no reemplaza la reproducción HTTP.