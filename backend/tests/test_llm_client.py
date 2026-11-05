"""Tester for app.llm_client / app.config.

Kontrollerer at normalmodus gir en tydelig, egen feiltype når
`OPENAI_API_KEY` ikke er konfigurert – uten at dette påvirker demomodus
eller krever en ekte API-nøkkel (NFR6).

`get_settings` mockes direkte (med `_env_file=None`) i stedet for å
sette/fjerne miljøvariabler, slik at testen er uavhengig av om det faktisk
finnes en lokal `backend/.env`-fil med en ekte nøkkel på utviklermaskinen
som kjører testene.
"""

import pytest

from app import llm_client
from app.config import Settings
from app.llm_client import MissingApiKeyError, get_openai_client


def test_get_openai_client_raises_when_api_key_missing(monkeypatch):
    monkeypatch.setattr(
        llm_client, "get_settings", lambda: Settings(openai_api_key=None, _env_file=None)
    )

    with pytest.raises(MissingApiKeyError):
        get_openai_client()


def test_get_openai_client_succeeds_when_api_key_present(monkeypatch):
    monkeypatch.setattr(
        llm_client,
        "get_settings",
        lambda: Settings(openai_api_key="sk-test-dummy-key", _env_file=None),
    )

    client = get_openai_client()

    assert client.api_key == "sk-test-dummy-key"
    # Ingen automatiske retries skal gjøres ved feil (presisering i oppgaven).
    assert client.max_retries == 0
