# Aporte de Franco: pytest + httpx (registro, login y usuario)

## Alcance y motivación
Complemento independiente de **Karate** (Granit), con otra tecnología de automatización:
**pytest** para ejecutar/assertar y **httpx** para peticiones HTTP.

Basado en el README y `docs/requisitos.md` del sistema Qolqe fijado en el proyecto.
No modifica `qolqe/`, no reemplaza los archivos `.feature` ni altera resultados previos.

- **HU-N-01**: registro correcto, DNI/PIN inválidos, celular duplicado.
- **HU-N-02**: login exitoso, credenciales inválidas y bloqueo por tres intentos.
- **HU-N-04**: perfil, saldo inicial, seguridad sin token, DNI enmascarado.
- **HU-N-05**: edición del nombre y persistencia.
- **Integración con G4**: un token obtenido por login permite acceder a GET /api/contactos;
  sin token se rechaza el acceso.

**Limitación honesta:** esta suite no cubre todos los criterios de esas HU ni las diez HU de G4.
El docente debe confirmar si espera todo G4 con cada herramienta. No equiparar
"tasa de aprobados" de pytest con "tasa de aprobados" de Karate: los escenarios no
son idénticos.

## Preparación en Windows (PowerShell)
Desde la raíz del repositorio de Granit:

```powershell
./scripts/bootstrap.ps1
./.venv/Scripts/python.exe -m pip install -r tests/pytest_franco/requirements.txt
```

En una terminal independiente, levantar la aplicación:

```powershell
./.venv/Scripts/python.exe scripts/serve_api.py
```

En otra terminal, ejecutar **todos los escenarios de Franco**:

```powershell
./.venv/Scripts/python.exe -m pytest tests/pytest_franco -v --tb=short
```

Para guardar salida legible para la exposición:

```powershell
./.venv/Scripts/python.exe -m pytest tests/pytest_franco -v --tb=short | Tee-Object -FilePath reporte-franco.txt
```

La API debe responder en http://127.0.0.1:8000/docs. Se puede cambiar
el servidor con `QOLQE_BASE_URL`.

## Demostración sugerida
1. Presentar **pytest + httpx** frente a Karate.
2. Explicar HU-N-02 y sus criterios CA1, CA2, CA3, CA4 como ejemplo principal.
3. Enseñar `test_login_correcto_devuelve_token_y_sesion` y
   `test_login_bloqueo_tercer_intento`.
4. Ejecutar toda esta suite con el comando anterior y analizar resultados reales.
5. Comparar tiempos, legibilidad, alcance y defectos **solo en casos equivalentes**.

Las cuentas usadas son ficticias y únicas para cada escenario. Existe un sondeo
acotado al **preparar** usuarios/sesiones para mitigar la incidencia de visibilidad
de datos que ya documentó Granit. No se reintenta la acción funcional cuyo
resultado se verifica. El entorno y las respuestas deben corroborarse en la
ejecución real; aquí no se inventan números de aprobados o fallidos.
