"""Tester for normalmodus-orkestreringen (app.analysis_service).

Alle tester mocker OpenAI-klienten – ingen ekte, betalte API-kall gjøres.
Dekker både den vellykkede flyten (inkludert at grunnlagskontrollen faktisk
kjøres) og feilsituasjonene appen skal håndtere med forståelige
feilmeldinger: manglende/ugyldig API-nøkkel, tidsavbrudd, API-feil og et
ugyldig/avvist svar fra språkmodellen.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock

import httpx2
import openai
import pytest

from app import analysis_service
from app.llm_client import MissingApiKeyError
from app.models import AnalysisResult, SourceReference, Strength

CV_TEXT = "Kari Nordmann. Master i informatikk."
JOB_AD_TEXT = "Søker utvikler med kjennskap til Python."


def _fake_completion(*, parsed=None, refusal=None):
    message = SimpleNamespace(parsed=parsed, refusal=refusal)
    choice = SimpleNamespace(message=message)
    return SimpleNamespace(choices=[choice])


def _fake_client(parse_result=None, parse_side_effect=None):
    client = MagicMock()
    if parse_side_effect is not None:
        client.chat.completions.parse.side_effect = parse_side_effect
    else:
        client.chat.completions.parse.return_value = parse_result
    return client


def _valid_result() -> AnalysisResult:
    return AnalysisResult(
        job_requirements=[],
        strengths=[
            Strength(
                id="s1",
                description="Mastergrad i informatikk er relevant for stillingen",
                source=SourceReference(cv_excerpt="Master i informatikk", job_ad_excerpt="Python"),
            )
        ],
        competency_gaps=[],
        cv_suggestions=[],
        application_draft="Utkast til søknad.",
    )


def test_raises_api_key_missing_when_client_cannot_be_created(monkeypatch):
    def _raise_missing():
        raise MissingApiKeyError("ingen nøkkel")

    monkeypatch.setattr(analysis_service, "get_openai_client", _raise_missing)

    with pytest.raises(analysis_service.ApiKeyMissingError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_raises_timeout_error_on_api_timeout(monkeypatch):
    request = httpx2.Request("POST", "https://api.openai.com/v1/chat/completions")
    client = _fake_client(parse_side_effect=openai.APITimeoutError(request=request))
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with pytest.raises(analysis_service.LlmTimeoutError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_raises_api_key_missing_on_authentication_error(monkeypatch):
    request = httpx2.Request("POST", "https://api.openai.com/v1/chat/completions")
    response = httpx2.Response(status_code=401, request=request)
    error = openai.AuthenticationError("Invalid API key", response=response, body=None)
    client = _fake_client(parse_side_effect=error)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with pytest.raises(analysis_service.ApiKeyMissingError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_raises_request_error_on_connection_error(monkeypatch):
    request = httpx2.Request("POST", "https://api.openai.com/v1/chat/completions")
    error = openai.APIConnectionError(request=request)
    client = _fake_client(parse_side_effect=error)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with pytest.raises(analysis_service.LlmRequestError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_raises_request_error_on_rate_limit(monkeypatch):
    request = httpx2.Request("POST", "https://api.openai.com/v1/chat/completions")
    response = httpx2.Response(status_code=429, request=request)
    error = openai.RateLimitError("Too many requests", response=response, body=None)
    client = _fake_client(parse_side_effect=error)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with pytest.raises(analysis_service.LlmRequestError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_raises_response_invalid_on_length_finish_reason(monkeypatch):
    error = openai.LengthFinishReasonError(
        completion=SimpleNamespace(usage=SimpleNamespace(completion_tokens=10))
    )
    client = _fake_client(parse_side_effect=error)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with pytest.raises(analysis_service.LlmResponseInvalidError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_raises_response_invalid_on_refusal(monkeypatch):
    completion = _fake_completion(parsed=None, refusal="Kan ikke hjelpe med dette.")
    client = _fake_client(parse_result=completion)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with pytest.raises(analysis_service.LlmResponseInvalidError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_raises_response_invalid_when_parsed_is_none(monkeypatch):
    completion = _fake_completion(parsed=None, refusal=None)
    client = _fake_client(parse_result=completion)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with pytest.raises(analysis_service.LlmResponseInvalidError):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)


def test_successful_analysis_returns_parsed_result(monkeypatch):
    completion = _fake_completion(parsed=_valid_result(), refusal=None)
    client = _fake_client(parse_result=completion)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    result = analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)

    assert isinstance(result, AnalysisResult)
    assert len(result.strengths) == 1
    assert result.strengths[0].id == "s1"


def test_successful_analysis_applies_grounding_filter(monkeypatch):
    fabricated = AnalysisResult(
        job_requirements=[],
        strengths=[
            Strength(
                id="s1",
                description="Oppdiktet styrke",
                source=SourceReference(cv_excerpt="Ti års erfaring som pilot", job_ad_excerpt=None),
            )
        ],
        competency_gaps=[],
        cv_suggestions=[],
        application_draft="Utkast.",
    )
    completion = _fake_completion(parsed=fabricated, refusal=None)
    client = _fake_client(parse_result=completion)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    result = analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)

    # Sitatet finnes ikke i CV_TEXT, så grunnlagskontrollen skal luke bort funnet.
    assert result.strengths == []


def test_grounding_effect_is_logged_with_counts_only_not_content(monkeypatch, caplog):
    """Lagt til etter at det var umulig å fastslå om et manglende SQL-gap
    skyldtes språkmodellen eller `grounding.py`, siden ingenting ble logget.
    Loggen skal vise at noe ble fjernet, men ALDRI inneholde CV-/annonse-
    eller funninnhold (NFR3)."""

    fabricated = AnalysisResult(
        job_requirements=[],
        strengths=[
            Strength(
                id="s1",
                description="Oppdiktet styrke som ikke finnes i CV-en",
                source=SourceReference(cv_excerpt="Ti års erfaring som pilot", job_ad_excerpt=None),
            )
        ],
        competency_gaps=[],
        cv_suggestions=[],
        application_draft="Utkast.",
    )
    completion = _fake_completion(parsed=fabricated, refusal=None)
    client = _fake_client(parse_result=completion)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with caplog.at_level("INFO"):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)

    log_text = "\n".join(record.message for record in caplog.records)
    assert "styrker 1->0" in log_text
    assert "Ti års erfaring som pilot" not in log_text
    assert "Oppdiktet styrke" not in log_text
    assert CV_TEXT not in log_text


def test_grounding_effect_is_not_logged_when_nothing_changes(monkeypatch, caplog):
    completion = _fake_completion(parsed=_valid_result(), refusal=None)
    client = _fake_client(parse_result=completion)
    monkeypatch.setattr(analysis_service, "get_openai_client", lambda: client)

    with caplog.at_level("INFO"):
        analysis_service.run_normal_mode_analysis(CV_TEXT, JOB_AD_TEXT)

    assert not any("grunnlagskontroll" in record.message for record in caplog.records)
