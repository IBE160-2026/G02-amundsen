"""Konfigurasjon for normalmodus.

API-nøkkelen leses kun fra miljøvariabler/en lokal `.env`-fil i `backend/`,
og håndteres aldri i frontend eller logges (architecture.md, avsnitt
"Backend Integration" og "Secrets"; NFR4).
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = Field(default=None, alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5.4-mini", alias="OPENAI_MODEL")
    openai_timeout_seconds: float = Field(default=30.0, alias="OPENAI_TIMEOUT_SECONDS")


def get_settings() -> Settings:
    """Leser innstillingene på nytt for hvert kall.

    Instansieringen er billig, og å unngå caching gjør det enkelt å endre
    miljøvariabler mellom tester uten en egen cache-cache-invalidering.
    """

    return Settings()
