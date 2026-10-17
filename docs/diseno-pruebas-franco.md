# Aporte de Franco — Diseño y trazabilidad de pruebas HTTP

## Alcance
Herramienta **pytest + httpx**. Pruebas automatizadas HTTP contra el Qolqe original de la referencia, sin mocks y sin modificar `qolqe/`. Módulo común (registro, login, usuario) como soporte a **G4 Contactos**, no equivalente a probar todas las HU propias de G4.

**Fuentes de resultados esperados:** `docs/requisitos.md` del repositorio oficial de Qolqe, su contrato `/openapi.json` y las convenciones de errores del README del enunciado.

## Justificación de herramienta
- **Karate** (Granit): escenarios legibles estilo Gherkin, HTTP y aserciones integradas, útil para casos funcionales trazables.
- **pytest + httpx** (Franco): control y parametrización directamente en Python, integración natural con fixtures, aserciones y salida JUnit. Permite comparar enfoques sin alterar pruebas Karate.
- Limitación: pytest + httpx requiere escribir código para preparación, solicitudes y verificaciones, y no produce por sí solo un informe HTML funcional equivalente al portal Karate.

## Diseño y trazabilidad

| Técnica | HU / CA | Datos o partición | Esperado | Prueba |
|---|---|---|---|---|
| Partición positiva | HU-N-01 CA1 | DNI 8 dígitos, celular 9 dígitos, PIN válido | HTTP 201, usuario registrado | test_registro_valido_crea_usuario |
| Partición negativa | HU-N-01 CA2 | DNI demasiado corto o alfabético | HTTP 422, DNI_INVALIDO | test_registro_dni_invalido |
| Partición negativa | HU-N-01 CA4 | PIN de 2 cifras | HTTP 422, PIN_INVALIDO | test_registro_pin_invalido |
| Estado preexistente | HU-N-01 CA3 | Celular registrado | HTTP 409, CELULAR_REGISTRADO | test_registro_duplicado |
| Partición positiva / contrato | HU-N-02 CA1 | Login con celular/PIN correctos | 200, JWT, tipo bearer, 1800s, sesion_id | test_login_correcto_devuelve_token_y_sesion |
| Partición negativa | HU-N-02 CA2 | PIN incorrecto | 401, CREDENCIALES_INVALIDAS | test_login_pin_incorrecto |
| Partición negativa | HU-N-02 CA2 | Celular inexistente | 401, CREDENCIALES_INVALIDAS | test_login_celular_inexistente |
| Transición de estado | HU-N-02 CA3, CA4 | Tres intentos errados y luego PIN correcto | 401/401/423/423, CUENTA_BLOQUEADA | test_login_bloqueo_tercer_intento |
| Datos de salida | HU-N-04 CA2 | Perfil con JWT | DNI enmascarado, celular propio | test_perfil_autenticado_muestra_dni_enmascarado |
| Datos de salida | HU-N-01 CA1, HU-N-04 CA1 | Cuenta nueva | Saldo 0.00 PEN | test_saldo_inicial_y_moneda |
| Seguridad / particiones | HU-N-04 CA3 / G4 | Sin token en perfil, saldo, contactos | HTTP 401 | test_endpoint_protegido_sin_token |
| Estado y persistencia | HU-N-05 CA1 | Editar nombre y leer perfil | HTTP 200, nombre actualizado | test_editar_nombre_del_usuario |
| Integración HTTP | Núcleo → G4 | Login y GET /api/contactos | HTTP 200, lista inicialmente vacía | test_contactos_g4_disponible_con_login |

**Advertencia:** registrar estados 201/200/401/422/423 como esperados no implica que hayan sido observados. Solo el reporte de ejecución confirma los obtenidos.

## Funcionales vs técnicas
- **Funcionales:** alta, acceso, bloqueo, actualización de perfil y habilitación de contactos para usuario autenticado.
- **Técnicas:** códigos HTTP, tipos de datos, campos de respuesta, obligatoriedad del JWT, verificación de serialización.

## Preparación y reproducibilidad
Los escenarios crean usuarios nuevos con identificadores sintéticos. Hay un sondeo acotado para la visibilidad inicial de registro y sesión porque el proyecto ya documentó una incidencia de commits tardíos. **No se reintentan altas, cambios de perfil ni la acción de negocio bajo prueba.** La última lectura inmediatamente posterior a editar perfil puede fallar por consistencia transaccional: debe documentarse sin añadir esperas ocultas.

## Resultados, defectos y evidencias
- **Estado actual del diseño:** se han escrito pruebas y una ejecución específica en GitHub Actions; revisar el reporte asociado a la ejecución antes de registrar totales.
- **No atribuir defectos nuevos** solo por un exit code distinto de cero. Inspeccionar escenario, petición/respuesta y momento del fallo.
- **Evidencias:** workflow `.github/workflows/pytest-franco.yml`, artefacto `evidencias-pytest-franco` con `reports/pytest-franco.xml` y `reports/pytest-franco.txt` (conservación temporal).
- **Pendientes de cobertura:** correo, SMS, DNI/celular inmutables, cuenta cerrada, vencimiento de token, desbloqueo tras 15 min, reglas de G4 diferentes del acceso a contactos.

## Para la primera presentación
1. Explicar la selección de pytest + httpx comparada con Karate.
2. Contextualizar la autenticación/usuario como núcleo que protege G4.
3. Exponer **HU-N-02 (Login)**; justificar equivalencia de credenciales y transiciones tras 3 intentos.
4. Mostrar `test_login_correcto_devuelve_token_y_sesion` y `test_login_bloqueo_tercer_intento`.
5. Ejecutar toda la suite `python -m pytest tests/pytest_franco -v --tb=short`, enseñar el XML/log de ejecución y contrastar con las pruebas equivalentes de Karate. Si se requiere exponer una HU propia de G4, ampliar específicamente el alcance antes de afirmar cumplimiento.

## Uso de IA
Desarrollo asistido por ChatGPT (estructura inicial, automatización, README y matriz); revisar con los integrantes, contrastar con ejecuciones y completar el `IA.md` de la entrega final con lo realmente aceptado/modificado.
