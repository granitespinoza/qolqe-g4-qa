"""Pruebas independientes del núcleo: registro, login y usuario, con integración G4.

FUENTES: HU-N-01 (CA1/2/4), HU-N-02 (CA1/2/3), HU-N-04 (CA1/2/3),
HU-N-05 (CA1), y protección de GET /api/contactos (G4).
"""
import pytest
from conftest import new_user_data, login_when_ready


def auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_registro_valido_crea_usuario(client):
    """HU-N-01 CA1: alta de usuario nuevo."""
    body = new_user_data()
    response = client.post("/api/usuarios", json=body)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["celular"] == body["celular"]
    assert data["nombres"] == body["nombres"]
    assert isinstance(data["id"], int)


@pytest.mark.parametrize("dni", ["123", "abcdefgh"])
def test_registro_dni_invalido(client, dni):
    """HU-N-01 CA2: particiones inválidas del DNI."""
    body = new_user_data()
    body["dni"] = dni
    response = client.post("/api/usuarios", json=body)
    assert response.status_code == 422, response.text
    assert response.json()["codigo"] == "DNI_INVALIDO"


def test_registro_pin_invalido(client):
    """HU-N-01 CA4: PIN no permitido."""
    body = new_user_data()
    body["pin"] = "12"
    response = client.post("/api/usuarios", json=body)
    assert response.status_code == 422, response.text
    assert response.json()["codigo"] == "PIN_INVALIDO"


def test_registro_duplicado(client, user):
    """HU-N-01 CA3: no permite duplicar un celular."""
    other = new_user_data()
    other["celular"] = user["celular"]
    response = client.post("/api/usuarios", json=other)
    assert response.status_code == 409, response.text
    assert response.json()["codigo"] == "CELULAR_REGISTRADO"


def test_login_correcto_devuelve_token_y_sesion(client, user):
    """HU-N-02 CA1: autenticación correcta y contrato básico."""
    response = login_when_ready(client, user)
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] == 1800
    assert isinstance(body["access_token"], str) and body["access_token"]
    assert isinstance(body["sesion_id"], int)
    assert body["usuario"]["celular"] == user["celular"]


def test_login_pin_incorrecto(client, user):
    """HU-N-02 CA2: respuesta genérica sin identificar qué dato es incorrecto."""
    response = client.post("/api/auth/login", json={"celular": user["celular"], "pin": "0000"})
    assert response.status_code == 401, response.text
    assert response.json()["codigo"] == "CREDENCIALES_INVALIDAS"


def test_login_celular_inexistente(client):
    """HU-N-02 CA2: mismo error que PIN equivocado."""
    body = new_user_data()
    response = client.post("/api/auth/login", json={"celular": body["celular"], "pin": body["pin"]})
    assert response.status_code == 401, response.text
    assert response.json()["codigo"] == "CREDENCIALES_INVALIDAS"


def test_login_bloqueo_tercer_intento(client, user):
    """HU-N-02 CA3/4: tres intentos incorrectos bloquean incluso el PIN correcto."""
    # Un registro 201 puede necesitar un intervalo breve para ser visible; se valida
    # la precondición con login correcto antes de probar el bloqueo.
    ready = login_when_ready(client, user)
    assert ready.status_code == 200, ready.text
    for number in (1, 2, 3):
        result = client.post("/api/auth/login", json={"celular": user["celular"], "pin": "0000"})
        expected = 423 if number == 3 else 401
        assert result.status_code == expected, f"Intento {number}: {result.text}"
    response = client.post("/api/auth/login", json={"celular": user["celular"], "pin": user["pin"]})
    assert response.status_code == 423, response.text
    assert response.json()["codigo"] == "CUENTA_BLOQUEADA"


def test_perfil_autenticado_muestra_dni_enmascarado(client, user, token):
    """HU-N-04 CA2: autenticación y visibilidad del perfil."""
    response = client.get("/api/cuentas/me", headers=auth(token))
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["celular"] == user["celular"]
    assert data["dni"].endswith(user["dni"][-4:])
    assert data["dni"] != user["dni"]


def test_saldo_inicial_y_moneda(client, token):
    """HU-N-01 CA1 y HU-N-04 CA1: saldo S/ 0, moneda PEN."""
    response = client.get("/api/cuentas/me/saldo", headers=auth(token))
    assert response.status_code == 200, response.text
    assert response.json()["saldo"] == "0.00"
    assert response.json()["moneda"] == "PEN"


@pytest.mark.parametrize("path", ["/api/cuentas/me", "/api/cuentas/me/saldo", "/api/contactos"])
def test_endpoint_protegido_sin_token(client, path):
    """HU-N-04 CA3 y comprobación técnica G4: autenticación obligatoria."""
    response = client.get(path)
    assert response.status_code == 401, response.text


def test_editar_nombre_del_usuario(client, user, token):
    """HU-N-05 CA1: editar el perfil y comprobar persistencia."""
    updated = client.put("/api/cuentas/me", json={"nombres": "Franco QA Prueba"}, headers=auth(token))
    assert updated.status_code == 200, updated.text
    assert updated.json()["nombres"] == "Franco QA Prueba"
    check = client.get("/api/cuentas/me", headers=auth(token))
    assert check.status_code == 200, check.text
    assert check.json()["nombres"] == "Franco QA Prueba"


def test_contactos_g4_disponible_con_login(client, token):
    """Integración: token del núcleo permite consultar contactos G4."""
    response = client.get("/api/contactos", headers=auth(token))
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data["total"], int)
    assert data["total"] == 0
