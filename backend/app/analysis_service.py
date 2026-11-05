"""Orkestrerer normalmodus-analysen: bygger prompten, kaller OpenAI med
strukturert output, og kjører grunnlagskontrollen før resultatet returneres.

All kommunikasjon med språkmodellen skjer herfra og ingen andre steder
(architecture.md, avsnitt "Backend Integration"). Ingen retries gjøres her
eller i `llm_client.py` (`max_retries=0`), slik oppgaven ber om, for å
unngå uventet kostnad og lange ventetider ved feil.

Feil logges uten å inkludere CV-tekst, stillingsannonse eller API-nøkkelen
(personvern/NFR3 og sikkerhet/NFR4) – kun feiltype og en kort, ufarlig
feilmelding fra SDK-et. Det samme gjelder logging av grunnlagskontrollen
(se `_log_grounding_effect`): kun antall funn før/etter, aldri selve
innholdet. Dette ble lagt til etter en konkret erfaring (05.11.2026) der det
var umulig å fastslå om et manglende funn i et ekte svar skyldtes
språkmodellen selv eller `grounding.py`, siden ingenting ble logget.
"""

from __future__ import annotations

import logging

from openai import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    AuthenticationError,
    ContentFilterFinishReasonError,
    LengthFinishReasonError,
)

from .config import get_settings
from .grounding import enforce_grounding
from .llm_client import MissingApiKeyError, get_openai_client
from .models import AnalysisResult
from .prompts import build_messages

logger = logging.getLogger(__name__)


class NormalModeError(RuntimeError):
    """Basisklasse for feil som kan oppstå under normalmodus-analysen."""


class ApiKeyMissingError(NormalModeError):
    """OPENAI_API_KEY er ikke konfigurert, eller ble avvist som ugyldig."""


class LlmTimeoutError(NormalModeError):
    """Språkmodellen svarte ikke innen tidsfristen."""


class LlmRequestError(NormalModeError):
    """Selve kallet til språkmodell-API-et mislyktes."""


class LlmResponseInvalidError(NormalModeError):
    """Språkmodellen svarte, men uten et gyldig strukturert resultat."""


def _log_grounding_effect(raw: AnalysisResult, cleaned: AnalysisResult) -> None:
    """Logger kun antall funn før/etter grunnlagskontrollen – aldri
    innholdet – slik at et fremtidig "forsvant funnet pga. språkmodellen
    eller grounding.py?"-spørsmål kan besvares direkte i loggen, i stedet
    for å måtte undersøkes i etterkant uten data."""

    counts = (
        ("styrker", len(raw.strengths), len(cleaned.strengths)),
        ("kompetansegap", len(raw.competency_gaps), len(cleaned.competency_gaps)),
        ("cv-forslag", len(raw.cv_suggestions), len(cleaned.cv_suggestions)),
    )
    if any(before != after for _, before, after in counts):
        summary = ", ".join(f"{label} {before}->{after}" for label, before, after in counts)
        logger.info("Normalmodus: grunnlagskontroll endret antall funn (%s).", summary)


def run_normal_mode_analysis(cv_text: str, job_ad_text: str) -> AnalysisResult:
    """Kjører normalmodus-analysen for en gitt CV og stillingsannonse.

    Hever en av `NormalModeError`-underklassene over ved feil, slik at
    API-laget (`main.py`) kan oversette dem til forståelige HTTP-svar.
    """

    try:
        client = get_openai_client()
    except MissingApiKeyError as exc:
        raise ApiKeyMissingError(str(exc)) from exc

    settings = get_settings()
    messages = build_messages(cv_text=cv_text, job_ad_text=job_ad_text)

    try:
        completion = client.chat.completions.parse(
            model=settings.openai_model,
            messages=messages,
            response_format=AnalysisResult,
        )
    except APITimeoutError as exc:
        logger.warning("Normalmodus: tidsavbrudd mot språkmodell-API-et.")
        raise LlmTimeoutError("Språkmodellen svarte ikke innen tidsfristen.") from exc
    except AuthenticationError as exc:
        logger.warning("Normalmodus: API-nøkkelen ble avvist av språkmodell-leverandøren.")
        raise ApiKeyMissingError(
            "API-nøkkelen ble avvist av språkmodell-leverandøren."
        ) from exc
    except (LengthFinishReasonError, ContentFilterFinishReasonError) as exc:
        logger.warning("Normalmodus: ugyldig/avvist svar fra språkmodellen (%s).", type(exc).__name__)
        raise LlmResponseInvalidError(
            "Språkmodellen kunne ikke returnere et gyldig, fullstendig resultat."
        ) from exc
    except (APIConnectionError, APIStatusError) as exc:
        logger.warning("Normalmodus: feil fra språkmodell-API-et (%s).", type(exc).__name__)
        raise LlmRequestError("Kunne ikke hente svar fra språkmodellen.") from exc

    choice = completion.choices[0]

    if choice.message.refusal:
        logger.warning("Normalmodus: språkmodellen avviste forespørselen.")
        raise LlmResponseInvalidError(
            "Språkmodellen avviste forespørselen og kunne ikke levere et resultat."
        )

    result = choice.message.parsed
    if result is None:
        logger.warning("Normalmodus: språkmodellen returnerte ikke et strukturert resultat.")
        raise LlmResponseInvalidError(
            "Språkmodellen returnerte ikke et strukturert resultat."
        )

    cleaned_result = enforce_grounding(result, cv_text=cv_text, job_ad_text=job_ad_text)
    _log_grounding_effect(result, cleaned_result)
    return cleaned_result
