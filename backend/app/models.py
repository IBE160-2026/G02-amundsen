"""Pydantic-modeller for analyseresultatet fra Career Transition Assistant.

Samme struktur brukes i demomodus og normal modus (jf. architecture.md,
avsnitt "Demo Mode" og "Structured Output"), slik at frontend kan bygges mot
én og samme respons-kontrakt uavhengig av hvilken modus som er aktiv.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

Priority = Literal["sentral", "ønskelig"]
"""Hvor viktig et krav i stillingsannonsen er for analysen (FR3, Story 2.3)."""

# Rimelige øvre grenser for inputlengde til normalmodus (presisering i
# oppgaven: "Legg inn rimelige grenser for inputlengde"). Grensene er satt
# romslig nok til en reell CV/stillingsannonse, men bounder likevel
# token-kostnad og unngår urimelig store forespørsler til språkmodellen.
MAX_CV_LENGTH = 20_000
MAX_JOB_AD_LENGTH = 10_000


class SourceReference(BaseModel):
    """Sporbarhet: hvilken del av CV-en og/eller stillingsannonsen et
    funn eller forslag bygger på (FR7, NFR8, Story 3.2).

    Begge feltene er valgfrie fordi et kompetansegap typisk kun kan
    forankres i stillingsannonsen (informasjonen finnes per definisjon
    ikke i CV-en), mens en styrke eller et CV-forslag normalt forankres
    i begge deler.
    """

    cv_excerpt: str | None = Field(
        default=None,
        description="Utdrag fra CV-en som funnet/forslaget bygger på.",
    )
    job_ad_excerpt: str | None = Field(
        default=None,
        description="Utdrag fra stillingsannonsen som funnet/forslaget bygger på.",
    )


class JobRequirement(BaseModel):
    """Et sentralt krav identifisert i stillingsannonsen (FR3, Story 2.3)."""

    id: str
    description: str
    priority: Priority = "sentral"


class Strength(BaseModel):
    """En relevant styrke hos brukeren, sporbar til CV-en (FR4, Story 2.1)."""

    id: str
    description: str
    related_requirement_ids: list[str] = Field(default_factory=list)
    source: SourceReference


class CompetencyGap(BaseModel):
    """Et kompetansegap mellom CV og stillingskrav (FR5, Story 2.2)."""

    id: str
    description: str
    related_requirement_ids: list[str] = Field(default_factory=list)
    source: SourceReference


class CvSuggestion(BaseModel):
    """Et konkret forslag til hvordan CV-en kan tilpasses stillingen
    (FR6, FR7, Story 3.1, Story 3.2)."""

    id: str
    suggestion: str
    related_requirement_ids: list[str] = Field(default_factory=list)
    source: SourceReference


class AnalysisResult(BaseModel):
    """Det samlede, strukturerte analyseresultatet (architecture.md,
    avsnitt "Structured Output").

    Dekker: sentrale krav i stillingsannonsen, relevante styrker,
    kompetansegap, CV-forslag med sporbarhet, og et førsteutkast til
    søknadsbrev.
    """

    job_requirements: list[JobRequirement]
    strengths: list[Strength]
    competency_gaps: list[CompetencyGap]
    cv_suggestions: list[CvSuggestion]
    application_draft: str = Field(
        description="Førsteutkast til søknadsbrev basert på CV og stillingsannonse (FR8)."
    )


class AnalyzeRequest(BaseModel):
    """Forespørsel til normalmodus (FR1, FR2): brukerens CV og den aktuelle
    stillingsannonsen som ren tekst.

    Lengdegrensene er en enkel beskyttelse mot urimelig store forespørsler
    til språkmodellen (kostnad/token-bruk), ikke en antagelse om at ekte
    CV-er eller stillingsannonser normalt er så lange.
    """

    cv_text: str = Field(min_length=1, max_length=MAX_CV_LENGTH)
    job_ad_text: str = Field(min_length=1, max_length=MAX_JOB_AD_LENGTH)

    @field_validator("cv_text", "job_ad_text")
    @classmethod
    def _not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Feltet kan ikke være tomt eller bare bestå av mellomrom.")
        return value


class AnalyzeResponse(BaseModel):
    """Responsen fra analyseendepunktet, både i demomodus og normal modus.

    `cv_text` og `job_ad_text` ekkoes tilbake slik at frontend kan vise
    hva analysen faktisk bygger på, uten at applikasjonen lagrer noe
    utover den aktive forespørselen (FR11, NFR3).
    """

    mode: Literal["demo", "normal"]
    cv_text: str
    job_ad_text: str
    result: AnalysisResult
