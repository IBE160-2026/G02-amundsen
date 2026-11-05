"""Tester for POST /api/analyze (normalmodus).

`run_normal_mode_analysis` mockes på modulnivå i `app.main` – ingen ekte,
betalte API-kall gjøres. Dekker inputvalidering (manglende/tomt/for langt
input), den vellykkede flyten, og at feil fra `analysis_service` oversettes
til forståelige HTTP-feilsvar uten å lekke interne detaljer.
"""

from fastapi.testclient import TestClient

from app import main
from app.main import app
from app.models import AnalysisResult, MAX_CV_LENGTH, MAX_JOB_AD_LENGTH

client = TestClient(app)

VALID_PAYLOAD = {
    "cv_text": "Kari Nordmann. Master i informatikk.",
    "job_ad_text": "Søker utvikler med kjennskap til Python.",
}


def _valid_result() -> AnalysisResult:
    return AnalysisResult(
        job_requirements=[],
        strengths=[],
        competency_gaps=[],
        cv_suggestions=[],
        application_draft="Utkast til søknad.",
    )


def test_missing_fields_returns_422():
    response = client.post("/api/analyze", json={})

    assert response.status_code == 422


def test_blank_cv_text_returns_422():
    response = client.post(
        "/api/analyze", json={"cv_text": "   ", "job_ad_text": "Noe tekst"}
    )

    assert response.status_code == 422


def test_cv_text_too_long_returns_422():
    response = client.post(
        "/api/analyze",
        json={"cv_text": "a" * (MAX_CV_LENGTH + 1), "job_ad_text": "Noe tekst"},
    )

    assert response.status_code == 422


def test_job_ad_text_too_long_returns_422():
    response = client.post(
        "/api/analyze",
        json={"cv_text": "Noe tekst", "job_ad_text": "a" * (MAX_JOB_AD_LENGTH + 1)},
    )

    assert response.status_code == 422


def test_successful_normal_mode_returns_200(monkeypatch):
    monkeypatch.setattr(main, "run_normal_mode_analysis", lambda cv, job_ad: _valid_result())

    response = client.post("/api/analyze", json=VALID_PAYLOAD)
    data = response.json()

    assert response.status_code == 200
    assert data["mode"] == "normal"
    assert data["cv_text"] == VALID_PAYLOAD["cv_text"]
    assert data["job_ad_text"] == VALID_PAYLOAD["job_ad_text"]
    assert data["result"]["application_draft"] == "Utkast til søknad."


def test_missing_api_key_returns_503(monkeypatch):
    def _raise(cv, job_ad):
        raise main.ApiKeyMissingError("ingen nøkkel konfigurert")

    monkeypatch.setattr(main, "run_normal_mode_analysis", _raise)

    response = client.post("/api/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 503
    assert "demomodus" in response.json()["detail"].lower()


def test_timeout_returns_504(monkeypatch):
    def _raise(cv, job_ad):
        raise main.LlmTimeoutError("tidsavbrudd")

    monkeypatch.setattr(main, "run_normal_mode_analysis", _raise)

    response = client.post("/api/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 504


def test_llm_request_error_returns_502(monkeypatch):
    def _raise(cv, job_ad):
        raise main.LlmRequestError("noe gikk feil mot API-et")

    monkeypatch.setattr(main, "run_normal_mode_analysis", _raise)

    response = client.post("/api/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 502


def test_llm_response_invalid_returns_502(monkeypatch):
    def _raise(cv, job_ad):
        raise main.LlmResponseInvalidError("ugyldig svar")

    monkeypatch.setattr(main, "run_normal_mode_analysis", _raise)

    response = client.post("/api/analyze", json=VALID_PAYLOAD)

    assert response.status_code == 502


def test_error_responses_do_not_leak_exception_details(monkeypatch):
    secret_detail = "Bearer sk-super-secret-key-should-not-leak"

    def _raise(cv, job_ad):
        raise main.LlmRequestError(secret_detail)

    monkeypatch.setattr(main, "run_normal_mode_analysis", _raise)

    response = client.post("/api/analyze", json=VALID_PAYLOAD)

    assert secret_detail not in response.text
