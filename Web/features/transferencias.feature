# language: es
@web
Característica: Transferencias verificable en Qolqe
  Como cliente de Qolqe
  Quiero que la interfaz respete las reglas y conserve los datos
  Para operar de forma segura

  @HU-G4-05 @TC-E2E-G4-201 @WEB-G4-05-CA1-01 @WEB-G4-05-CA1-02 @known_issue @D-07
  Escenario: E2E-G4-201 @HU-G4-05 @TC-E2E-G4-201 @known_issue @D-07 | WEB-G4-05-CA1-01 WEB-G4-05-CA1-02 | Transferir 0.01, comprobante y movimientos persistentes
    Dado un contexto aislado para "E2E-G4-201"
    Cuando realizo "Transferir 0.01, comprobante y movimientos persistentes" en "E2E-G4-201"
    Entonces verifico las reglas y la persistencia de "E2E-G4-201"

  @HU-G4-05 @TC-E2E-G4-202 @WEB-G4-05-CA1-01 @WEB-G4-05-CA1-02 @known_issue @D-07
  Escenario: E2E-G4-202 @HU-G4-05 @TC-E2E-G4-202 @known_issue @D-07 | WEB-G4-05-CA1-01 WEB-G4-05-CA1-02 | Transferir 500.00, comprobante y movimientos persistentes
    Dado un contexto aislado para "E2E-G4-202"
    Cuando realizo "Transferir 500.00, comprobante y movimientos persistentes" en "E2E-G4-202"
    Entonces verifico las reglas y la persistencia de "E2E-G4-202"

  @HU-G4-05 @TC-E2E-G4-203 @WEB-G4-05-CA1-02
  Escenario: E2E-G4-203 @HU-G4-05 @TC-E2E-G4-203 | WEB-G4-05-CA1-02 | Montos 0, negativo, 500.01 y tres decimales: sin transferencia
    Dado un contexto aislado para "E2E-G4-203"
    Cuando realizo "Montos 0, negativo, 500.01 y tres decimales: sin transferencia" en "E2E-G4-203"
    Entonces verifico las reglas y la persistencia de "E2E-G4-203"

  @HU-G4-05 @TC-E2E-G4-204 @WEB-G4-05-CA1-03
  Escenario: E2E-G4-204 @HU-G4-05 @TC-E2E-G4-204 | WEB-G4-05-CA1-03 | Error saldo conserva el dinero
    Dado un contexto aislado para "E2E-G4-204"
    Cuando realizo "Error saldo conserva el dinero" en "E2E-G4-204"
    Entonces verifico las reglas y la persistencia de "E2E-G4-204"

  @HU-G4-05 @TC-E2E-G4-205 @WEB-G4-05-CA1-03
  Escenario: E2E-G4-205 @HU-G4-05 @TC-E2E-G4-205 | WEB-G4-05-CA1-03 | Error limite conserva el dinero
    Dado un contexto aislado para "E2E-G4-205"
    Cuando realizo "Error limite conserva el dinero" en "E2E-G4-205"
    Entonces verifico las reglas y la persistencia de "E2E-G4-205"

  @HU-G4-05 @TC-E2E-G4-206 @WEB-G4-05-CA1-03 @known_issue @D-08
  Escenario: E2E-G4-206 @HU-G4-05 @TC-E2E-G4-206 @known_issue @D-08 | WEB-G4-05-CA1-03 | Error cerrado conserva el dinero
    Dado un contexto aislado para "E2E-G4-206"
    Cuando realizo "Error cerrado conserva el dinero" en "E2E-G4-206"
    Entonces verifico las reglas y la persistencia de "E2E-G4-206"
