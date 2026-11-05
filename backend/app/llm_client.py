"""Oppretter OpenAI-klienten for normalmodus.

Klienten opprettes først når den faktisk trengs (ved et kall til
`/api/analyze`), ikke ved import av applikasjonen. Det betyr at demomodus
og `GET /` fortsatt fungerer uten noen API-nøkkel satt (NFR6), og at
applikasjonen ikke krasjer ved oppstart om nøkkelen mangler.

`max_retries=0` er satt bevisst: oppgaven ber om ingen automatiske retries
for API-kall, for å unngå uventet kostnad og lange ventetider ved feil.
"""

from __future__ import annotations

from openai import OpenAI

from .config import get_settings


class MissingApiKeyError(RuntimeError):
    """Hevet når OPENAI_API_KEY ikke er konfigurert på serveren."""


def get_openai_client() -> OpenAI:
    settings = get_settings()
    if not settings.openai_api_key:
        raise MissingApiKeyError(
            "OPENAI_API_KEY er ikke satt. Se backend/.env.example."
        )

    return OpenAI(
        api_key=settings.openai_api_key,
        timeout=settings.openai_timeout_seconds,
        max_retries=0,
    )
