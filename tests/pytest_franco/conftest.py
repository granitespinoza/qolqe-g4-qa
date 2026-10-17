"""Fixtures HTTP para la contribución de Franco (no modifican Qolqe)."""
import os
import time
import uuid

import httpx
import pytest


BASE_URL = os.getenv("QOLQE_BASE_URL", "http://127.0.0.1:8000")


@pytest.fixture
def client():
    with httpx.Client(base_url=BASE_URL, timeout=12.0) as session:
        try:
            response = session.get("/openapi.json")
            response.raise_for_status()
        except httpx.HTTPError as error:
            pytest.fail(f"API Qolqe no disponible en {BASE_URL}: {error}")
        yield session


def new_user_data():
    # Identificadores sintéticos aislados del conjunto semilla.
    value = uuid.uuid4().int % 80000000 + 10000000
    return {
        "dni": str(value),
        "nombres": "Usuario Prueba Franco",
        "celular": "9" + str(value),
        "pin": "4826",
        "correo": None,
    }


@pytest.fixture
def user(client):
    payload = new_user_data()
    result = client.post("/api/usuarios", json=payload)
    assert result.status_code == 201, result.text
    return payload


def login_when_ready(client, user, seconds=2.0):
    """Espera solamente la visibilidad inicial del registro, no reintenta operaciones financieras."""
    end = time.monotonic() + seconds
    while True:
        response = client.post("/api/auth/login", json={"celular": user["celular"], "pin": user["pin"]})
        if response.status_code == 200:
            return response
        if not (response.status_code == 401 and response.json().get("codigo") == "CREDENCIALES_INVALIDAS"):
            return response
        if time.monotonic() >= end:
            return response
        time.sleep(0.05)


@pytest.fixture
def token(client, user):
    response = login_when_ready(client, user)
    assert response.status_code == 200, response.text
    access_token = response.json()["access_token"]
    # La aplicación puede emitir una sesión aún no visible para la siguiente petición.
    end = time.monotonic() + 2
    while True:
        probe = client.get("/api/cuentas/me/saldo", headers={"Authorization": f"Bearer {access_token}"})
        if probe.status_code == 200:
            break
        if time.monotonic() >= end:
            pytest.fail(f"Sesión recién creada no disponible: {probe.status_code} {probe.text}")
        assert probe.status_code == 401 and probe.json().get("codigo") == "NO_AUTENTICADO", probe.text
        time.sleep(0.05)
    return access_token
