"""Tester for CORS-konfigurasjonen i app.main.

Bakgrunn: under manuell testing kjørte frontend på
`http://localhost:5174` (Vite valgte denne porten automatisk fordi 5173
allerede var i bruk), mens backendens `allow_origins` kun tillot port 5173.
Nettleseren blokkerte da `fetch()`-kall fra frontend med
"No 'Access-Control-Allow-Origin' header is present", selv om et direkte
`GET` i adressefeltet fungerte (CORS gjelder kun skript-initierte
forespørsler, ikke vanlig nettlesernavigasjon).

Testene kontrollerer at de fire tillatte lokale origins (localhost/127.0.0.1
på port 5173 og 5174) faktisk får CORS-tillatelse, og at et ukjent origin
IKKE får det – uten å åpne for alle domener.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

UNKNOWN_ORIGIN = "http://evil.example.com"


@pytest.mark.parametrize("origin", ALLOWED_ORIGINS)
def test_allowed_origin_gets_cors_header_on_demo_endpoint(origin):
    response = client.get("/api/analyze/demo", headers={"Origin": origin})

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == origin


def test_unknown_origin_does_not_get_cors_header_on_demo_endpoint():
    response = client.get("/api/analyze/demo", headers={"Origin": UNKNOWN_ORIGIN})

    # Selve forespørselen besvares fortsatt (backenden stopper den ikke),
    # men uten CORS-headeren vil nettleseren blokkere at JS-koden i et
    # ukjent origin faktisk får lese svaret.
    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers


@pytest.mark.parametrize("origin", ALLOWED_ORIGINS)
def test_preflight_for_allowed_origin_permits_post_to_analyze(origin):
    response = client.options(
        "/api/analyze",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == origin
    assert "POST" in response.headers.get("access-control-allow-methods", "")


def test_preflight_for_unknown_origin_is_rejected():
    response = client.options(
        "/api/analyze",
        headers={
            "Origin": UNKNOWN_ORIGIN,
            "Access-Control-Request-Method": "POST",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers


def test_cors_is_not_wildcarded_to_all_origins():
    """Regresjonsvern for presisering i oppgaven: CORS skal ikke åpnes for
    alle domener. Kontrollerer at middlewaren faktisk er konfigurert med en
    konkret liste, ikke `["*"]`."""

    cors_middleware = next(
        m for m in app.user_middleware if m.cls.__name__ == "CORSMiddleware"
    )
    configured_origins = cors_middleware.kwargs["allow_origins"]

    assert configured_origins == ALLOWED_ORIGINS
    assert "*" not in configured_origins
