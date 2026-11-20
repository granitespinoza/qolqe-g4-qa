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
