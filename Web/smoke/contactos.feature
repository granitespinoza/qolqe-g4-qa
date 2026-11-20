# language: es
@smoke
Característica: Alta de contacto y persistencia
  @HU-G4-01 @TC-E2E-G4-001
  Escenario: E2E-G4-001 @HU-G4-01 @TC-E2E-G4-001 |  | Contactos reales E2E-G4-001 @HU-G4-01 @TC-E2E-G4-001 agrega un contacto y conserva sus datos al recargar
    Dado un contexto aislado para "E2E-G4-001"
    Cuando realizo "Contactos reales E2E-G4-001 @HU-G4-01 @TC-E2E-G4-001 agrega un contacto y conserva sus datos al recargar" en "E2E-G4-001"
    Entonces verifico las reglas y la persistencia de "E2E-G4-001"
