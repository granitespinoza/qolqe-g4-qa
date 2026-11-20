# language: es
@web
Característica: Nucleo verificable en Qolqe
  Como cliente de Qolqe
  Quiero que la interfaz respete las reglas y conserve los datos
  Para operar de forma segura

  @HU-N-02 @TC-E2E-G4-401
  Escenario: E2E-G4-401 @HU-N-02 @TC-E2E-G4-401 |  | Login válido navega a inicio
    Dado un contexto aislado para "E2E-G4-401"
    Cuando realizo "Login válido navega a inicio" en "E2E-G4-401"
    Entonces verifico las reglas y la persistencia de "E2E-G4-401"

  @HU-N-02 @TC-E2E-G4-402
  Escenario: E2E-G4-402 @HU-N-02 @TC-E2E-G4-402 |  | Credenciales inválidas mantienen el login y muestran mensaje genérico
    Dado un contexto aislado para "E2E-G4-402"
    Cuando realizo "Credenciales inválidas mantienen el login y muestran mensaje genérico" en "E2E-G4-402"
    Entonces verifico las reglas y la persistencia de "E2E-G4-402"

  @HU-N-04 @TC-E2E-G4-403
  Escenario: E2E-G4-403 @HU-N-04 @TC-E2E-G4-403 |  | Saldo preparado visible y opción de ocultar
    Dado un contexto aislado para "E2E-G4-403"
    Cuando realizo "Saldo preparado visible y opción de ocultar" en "E2E-G4-403"
    Entonces verifico las reglas y la persistencia de "E2E-G4-403"

  @HU-N-04 @TC-E2E-G4-404
  Escenario: E2E-G4-404 @HU-N-04 @TC-E2E-G4-404 |  | Perfil conserva celular y enmascara DNI
    Dado un contexto aislado para "E2E-G4-404"
    Cuando realizo "Perfil conserva celular y enmascara DNI" en "E2E-G4-404"
    Entonces verifico las reglas y la persistencia de "E2E-G4-404"

  @HU-N-05 @TC-E2E-G4-405
  Escenario: E2E-G4-405 @HU-N-05 @TC-E2E-G4-405 |  | Edición de nombres persiste tras recargar
    Dado un contexto aislado para "E2E-G4-405"
    Cuando realizo "Edición de nombres persiste tras recargar" en "E2E-G4-405"
    Entonces verifico las reglas y la persistencia de "E2E-G4-405"

  @HU-N-01 @TC-E2E-G4-406
  Escenario: E2E-G4-406 @HU-N-01 @TC-E2E-G4-406 |  | Registro por UI crea cuenta y permite iniciar sesión
    Dado un contexto aislado para "E2E-G4-406"
    Cuando realizo "Registro por UI crea cuenta y permite iniciar sesión" en "E2E-G4-406"
    Entonces verifico las reglas y la persistencia de "E2E-G4-406"

  @HU-N-03 @TC-E2E-G4-407 @known_issue @D-04
  Escenario: E2E-G4-407 @HU-N-03 @TC-E2E-G4-407 @known_issue @D-04 | Cerrar sesión limpia la UI, revoca su token y conserva otra sesión
    Dado un contexto aislado para "E2E-G4-407"
    Cuando realizo "Cerrar sesión limpia la UI, revoca su token y conserva otra sesión" en "E2E-G4-407"
    Entonces verifico las reglas y la persistencia de "E2E-G4-407"

  @HU-N-06 @TC-E2E-G4-408
  Escenario: E2E-G4-408 @HU-N-06 @TC-E2E-G4-408 | Cerrar cuenta con saldo cero y PIN impide volver a ingresar
    Dado un contexto aislado para "E2E-G4-408"
    Cuando realizo "Cerrar cuenta con saldo cero y PIN impide volver a ingresar" en "E2E-G4-408"
    Entonces verifico las reglas y la persistencia de "E2E-G4-408"

  @HU-N-07 @TC-E2E-G4-409
  Escenario: E2E-G4-409 @HU-N-07 @TC-E2E-G4-409 | Transferencia directa por celular muestra comprobante y acredita al destinatario
    Dado un contexto aislado para "E2E-G4-409"
    Cuando realizo "Transferencia directa por celular muestra comprobante y acredita al destinatario" en "E2E-G4-409"
    Entonces verifico las reglas y la persistencia de "E2E-G4-409"

  @HU-N-08 @TC-E2E-G4-410
  Escenario: E2E-G4-410 @HU-N-08 @TC-E2E-G4-410 | Transferencia interbancaria cobra comisión y enmascara el CCI
    Dado un contexto aislado para "E2E-G4-410"
    Cuando realizo "Transferencia interbancaria cobra comisión y enmascara el CCI" en "E2E-G4-410"
    Entonces verifico las reglas y la persistencia de "E2E-G4-410"

  @HU-N-09 @TC-E2E-G4-411
  Escenario: E2E-G4-411 @HU-N-09 @TC-E2E-G4-411 | Simular comisión y cancelar conserva saldo y no crea movimientos
    Dado un contexto aislado para "E2E-G4-411"
    Cuando realizo "Simular comisión y cancelar conserva saldo y no crea movimientos" en "E2E-G4-411"
    Entonces verifico las reglas y la persistencia de "E2E-G4-411"
