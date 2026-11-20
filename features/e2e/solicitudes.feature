# language: es
@web
Característica: Solicitudes verificable en Qolqe
  Como cliente de Qolqe
  Quiero que la interfaz respete las reglas y conserve los datos
  Para operar de forma segura

  @HU-G4-06 @TC-E2E-G4-301 @WEB-G4-06-CA1-01 @WEB-G4-06-CA2-01
  Escenario: E2E-G4-301 @HU-G4-06 @TC-E2E-G4-301 | WEB-G4-06-CA1-01 WEB-G4-06-CA2-01 | Crear solicitud por UI; 48 horas, SMS y ambas vistas
    Dado un contexto aislado para "E2E-G4-301"
    Cuando realizo "Crear solicitud por UI; 48 horas, SMS y ambas vistas" en "E2E-G4-301"
    Entonces verifico las reglas y la persistencia de "E2E-G4-301"

  @HU-G4-06 @TC-E2E-G4-302 @WEB-G4-06-CA1-01
  Escenario: E2E-G4-302 @HU-G4-06 @TC-E2E-G4-302 | WEB-G4-06-CA1-01 | Límites válidos: 0.01, motivo 3
    Dado un contexto aislado para "E2E-G4-302"
    Cuando realizo "Límites válidos: 0.01, motivo 3" en "E2E-G4-302"
    Entonces verifico las reglas y la persistencia de "E2E-G4-302"

  @HU-G4-06 @TC-E2E-G4-303 @WEB-G4-06-CA1-01
  Escenario: E2E-G4-303 @HU-G4-06 @TC-E2E-G4-303 | WEB-G4-06-CA1-01 | Límites válidos: 500.00, motivo 60
    Dado un contexto aislado para "E2E-G4-303"
    Cuando realizo "Límites válidos: 500.00, motivo 60" en "E2E-G4-303"
    Entonces verifico las reglas y la persistencia de "E2E-G4-303"

  @HU-G4-06 @TC-E2E-G4-304 @WEB-G4-06-CA1-01 @WEB-G4-06-CA1-02
  Escenario: E2E-G4-304 @HU-G4-06 @TC-E2E-G4-304 | WEB-G4-06-CA1-01 WEB-G4-06-CA1-02 | Montos y motivos inválidos no crean solicitudes
    Dado un contexto aislado para "E2E-G4-304"
    Cuando realizo "Montos y motivos inválidos no crean solicitudes" en "E2E-G4-304"
    Entonces verifico las reglas y la persistencia de "E2E-G4-304"

  @HU-G4-06 @TC-E2E-G4-305 @WEB-G4-06-CA1-02
  Escenario: E2E-G4-305 @HU-G4-06 @TC-E2E-G4-305 | WEB-G4-06-CA1-02 | Sin contacto el formulario explica el error
    Dado un contexto aislado para "E2E-G4-305"
    Cuando realizo "Sin contacto el formulario explica el error" en "E2E-G4-305"
    Entonces verifico las reglas y la persistencia de "E2E-G4-305"

  @HU-G4-06 @TC-E2E-G4-306 @WEB-G4-06-CA1-03
  Escenario: E2E-G4-306 @HU-G4-06 @TC-E2E-G4-306 | WEB-G4-06-CA1-03 | Pendiente 10 permitida, 11 rechazada sin alterar el total
    Dado un contexto aislado para "E2E-G4-306"
    Cuando realizo "Pendiente 10 permitida, 11 rechazada sin alterar el total" en "E2E-G4-306"
    Entonces verifico las reglas y la persistencia de "E2E-G4-306"

  @HU-G4-07 @TC-E2E-G4-307 @WEB-G4-07-CA1-01 @WEB-G4-07-CA1-02
  Escenario: E2E-G4-307 @HU-G4-07 @TC-E2E-G4-307 | WEB-G4-07-CA1-01 WEB-G4-07-CA1-02 | Vistas separadas y filtros de los cinco estados
    Dado un contexto aislado para "E2E-G4-307"
    Cuando realizo "Vistas separadas y filtros de los cinco estados" en "E2E-G4-307"
    Entonces verifico las reglas y la persistencia de "E2E-G4-307"

  @HU-G4-07 @HU-G4-08 @TC-E2E-G4-308 @WEB-G4-07-CA2-01 @WEB-G4-08-CA4-02
  Escenario: E2E-G4-308 @HU-G4-07 @HU-G4-08 @TC-E2E-G4-308 | WEB-G4-07-CA2-01 WEB-G4-08-CA4-02 | Frontera 2879 minutos sin esperas reales
    Dado un contexto aislado para "E2E-G4-308"
    Cuando realizo "Frontera 2879 minutos sin esperas reales" en "E2E-G4-308"
    Entonces verifico las reglas y la persistencia de "E2E-G4-308"

  @HU-G4-07 @HU-G4-08 @TC-E2E-G4-309 @WEB-G4-07-CA2-01 @WEB-G4-08-CA4-02
  Escenario: E2E-G4-309 @HU-G4-07 @HU-G4-08 @TC-E2E-G4-309 | WEB-G4-07-CA2-01 WEB-G4-08-CA4-02 | Frontera 2880 minutos sin esperas reales
    Dado un contexto aislado para "E2E-G4-309"
    Cuando realizo "Frontera 2880 minutos sin esperas reales" en "E2E-G4-309"
    Entonces verifico las reglas y la persistencia de "E2E-G4-309"

  @HU-G4-07 @HU-G4-08 @TC-E2E-G4-310 @WEB-G4-07-CA2-01 @WEB-G4-08-CA4-02
  Escenario: E2E-G4-310 @HU-G4-07 @HU-G4-08 @TC-E2E-G4-310 | WEB-G4-07-CA2-01 WEB-G4-08-CA4-02 | Frontera 2881 minutos sin esperas reales
    Dado un contexto aislado para "E2E-G4-310"
    Cuando realizo "Frontera 2881 minutos sin esperas reales" en "E2E-G4-310"
    Entonces verifico las reglas y la persistencia de "E2E-G4-310"

  @HU-G4-08 @TC-E2E-G4-311 @WEB-G4-08-CA1-01 @WEB-G4-08-CA3-01
  Escenario: E2E-G4-311 @HU-G4-08 @TC-E2E-G4-311 | WEB-G4-08-CA1-01 WEB-G4-08-CA3-01 | Aceptar: dinero, operación, SMS y persistencia
    Dado un contexto aislado para "E2E-G4-311"
    Cuando realizo "Aceptar: dinero, operación, SMS y persistencia" en "E2E-G4-311"
    Entonces verifico las reglas y la persistencia de "E2E-G4-311"

  @HU-G4-08 @TC-E2E-G4-312 @WEB-G4-08-CA2-01
  Escenario: E2E-G4-312 @HU-G4-08 @TC-E2E-G4-312 | WEB-G4-08-CA2-01 | Aceptar con error de saldo: conserva pendiente y dinero
    Dado un contexto aislado para "E2E-G4-312"
    Cuando realizo "Aceptar con error de saldo: conserva pendiente y dinero" en "E2E-G4-312"
    Entonces verifico las reglas y la persistencia de "E2E-G4-312"

  @HU-G4-08 @TC-E2E-G4-313 @WEB-G4-08-CA2-01
  Escenario: E2E-G4-313 @HU-G4-08 @TC-E2E-G4-313 | WEB-G4-08-CA2-01 | Aceptar con error de limite: conserva pendiente y dinero
    Dado un contexto aislado para "E2E-G4-313"
    Cuando realizo "Aceptar con error de limite: conserva pendiente y dinero" en "E2E-G4-313"
    Entonces verifico las reglas y la persistencia de "E2E-G4-313"

  @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-314 @WEB-G4-08-CA4-01 @WEB-G4-09-CA1-02 @WEB-G4-10-CA1-02
  Escenario: E2E-G4-314 @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-314 | WEB-G4-08-CA4-01 WEB-G4-09-CA1-02 WEB-G4-10-CA1-02 | Acciones visibles solo para el actor correcto
    Dado un contexto aislado para "E2E-G4-314"
    Cuando realizo "Acciones visibles solo para el actor correcto" en "E2E-G4-314"
    Entonces verifico las reglas y la persistencia de "E2E-G4-314"

  @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-315 @WEB-G4-08-CA4-02 @WEB-G4-09-CA1-02 @WEB-G4-10-CA1-02
  Escenario: E2E-G4-315 @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-315 | WEB-G4-08-CA4-02 WEB-G4-09-CA1-02 WEB-G4-10-CA1-02 | Solicitud resuelta (aceptar) no ofrece otra transición
    Dado un contexto aislado para "E2E-G4-315"
    Cuando realizo "Solicitud resuelta (aceptar) no ofrece otra transición" en "E2E-G4-315"
    Entonces verifico las reglas y la persistencia de "E2E-G4-315"

  @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-316 @WEB-G4-08-CA4-02 @WEB-G4-09-CA1-02 @WEB-G4-10-CA1-02
  Escenario: E2E-G4-316 @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-316 | WEB-G4-08-CA4-02 WEB-G4-09-CA1-02 WEB-G4-10-CA1-02 | Solicitud resuelta (rechazar) no ofrece otra transición
    Dado un contexto aislado para "E2E-G4-316"
    Cuando realizo "Solicitud resuelta (rechazar) no ofrece otra transición" en "E2E-G4-316"
    Entonces verifico las reglas y la persistencia de "E2E-G4-316"

  @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-317 @WEB-G4-08-CA4-02 @WEB-G4-09-CA1-02 @WEB-G4-10-CA1-02
  Escenario: E2E-G4-317 @HU-G4-08 @HU-G4-09 @HU-G4-10 @TC-E2E-G4-317 | WEB-G4-08-CA4-02 WEB-G4-09-CA1-02 WEB-G4-10-CA1-02 | Solicitud resuelta (cancelar) no ofrece otra transición
    Dado un contexto aislado para "E2E-G4-317"
    Cuando realizo "Solicitud resuelta (cancelar) no ofrece otra transición" en "E2E-G4-317"
    Entonces verifico las reglas y la persistencia de "E2E-G4-317"

  @HU-G4-09 @TC-E2E-G4-318 @WEB-G4-09-CA1-01
  Escenario: E2E-G4-318 @HU-G4-09 @TC-E2E-G4-318 | WEB-G4-09-CA1-01 | Rechazar con motivo de longitud 0, SMS y persistencia
    Dado un contexto aislado para "E2E-G4-318"
    Cuando realizo "Rechazar con motivo de longitud 0, SMS y persistencia" en "E2E-G4-318"
    Entonces verifico las reglas y la persistencia de "E2E-G4-318"

  @HU-G4-09 @TC-E2E-G4-319 @WEB-G4-09-CA1-01
  Escenario: E2E-G4-319 @HU-G4-09 @TC-E2E-G4-319 | WEB-G4-09-CA1-01 | Rechazar con motivo de longitud 60, SMS y persistencia
    Dado un contexto aislado para "E2E-G4-319"
    Cuando realizo "Rechazar con motivo de longitud 60, SMS y persistencia" en "E2E-G4-319"
    Entonces verifico las reglas y la persistencia de "E2E-G4-319"

  @HU-G4-09 @TC-E2E-G4-320 @WEB-G4-09-CA1-02
  Escenario: E2E-G4-320 @HU-G4-09 @TC-E2E-G4-320 | WEB-G4-09-CA1-02 | Motivo de rechazo de 61 caracteres conserva pendiente
    Dado un contexto aislado para "E2E-G4-320"
    Cuando realizo "Motivo de rechazo de 61 caracteres conserva pendiente" en "E2E-G4-320"
    Entonces verifico las reglas y la persistencia de "E2E-G4-320"

  @HU-G4-10 @TC-E2E-G4-321 @WEB-G4-10-CA1-01
  Escenario: E2E-G4-321 @HU-G4-10 @TC-E2E-G4-321 | WEB-G4-10-CA1-01 | Solicitante cancela por UI y persiste CANCELADA
    Dado un contexto aislado para "E2E-G4-321"
    Cuando realizo "Solicitante cancela por UI y persiste CANCELADA" en "E2E-G4-321"
    Entonces verifico las reglas y la persistencia de "E2E-G4-321"

  @HU-G4-09 @TC-E2E-G4-322 @WEB-G4-09-CA1-02
  Escenario: E2E-G4-322 @HU-G4-09 @TC-E2E-G4-322 | WEB-G4-09-CA1-02 | Formulario cargado antes de vencer: rechazar debe responder 409 al vencer
    Dado un contexto aislado para "E2E-G4-322"
    Cuando realizo "Formulario cargado antes de vencer: rechazar debe responder 409 al vencer" en "E2E-G4-322"
    Entonces verifico las reglas y la persistencia de "E2E-G4-322"

  @HU-G4-10 @TC-E2E-G4-323 @WEB-G4-10-CA1-02
  Escenario: E2E-G4-323 @HU-G4-10 @TC-E2E-G4-323 | WEB-G4-10-CA1-02 | Formulario cargado antes de vencer: cancelar debe responder 409 al vencer
    Dado un contexto aislado para "E2E-G4-323"
    Cuando realizo "Formulario cargado antes de vencer: cancelar debe responder 409 al vencer" en "E2E-G4-323"
    Entonces verifico las reglas y la persistencia de "E2E-G4-323"

  @HU-G4-08 @TC-E2E-G4-324 @WEB-G4-08-CA4-02 @known_issue @D-03
  Escenario: E2E-G4-324 @HU-G4-08 @TC-E2E-G4-324 @known_issue @D-03 | WEB-G4-08-CA4-02 | [D-03] Formulario cargado antes de vencer: aceptar debe responder 409 al vencer
    Dado un contexto aislado para "E2E-G4-324"
    Cuando realizo "[D-03] Formulario cargado antes de vencer: aceptar debe responder 409 al vencer" en "E2E-G4-324"
    Entonces verifico las reglas y la persistencia de "E2E-G4-324"
