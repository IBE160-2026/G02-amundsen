"""Grunnlagskontroll (grounding) for normalmodus.

Kontrollerer at kildesitatene i et KI-generert AnalysisResult faktisk finnes
i brukerens CV og/eller stillingsannonse, med forsiktig normalisering av
mellomrom og store/små bokstaver (FR10, NFR8, architecture.md avsnitt
"Grounding and Hallucination Control").

Manuell kvalitetssikring av et ekte svar fra språkmodellen (05.11.2026) viste
at et sitat kan være ordrett korrekt uten at *koblingen* det brukes til er
riktig:

1. En styrke ble knyttet til et stillingskrav (via `related_requirement_ids`)
   som gjaldt en helt annen kompetanse enn det styrkens eget sitat dokumenterte.
2. Et kompetansegap ble knyttet til feil stillingskrav på samme måte.
3. Et CV-forslag hadde et `cv_excerpt` som var et reelt utdrag fra CV-en, men
   som ikke hadde noe å gjøre med det forslaget faktisk handlet om.

En påfølgende ekte test (05.11.2026) viste at den første versjonen av fiksen
var for streng: et reelt, korrekt SQL-kompetansegap forsvant helt, og en
styrke om kundeservice/opplæring mistet koblingen til et relevant krav om
kommunikasjonsevner. Undersøkelse av koden (ikke gjetting) viste den
konkrete årsaken: nøkkelord-heuristikken krevde minst 4 bokstaver for at et
ord skulle telle som "betydningsfullt" – noe som utelukket korte, men
presise fagord som "SQL" (3 bokstaver) fra sammenligningen i BÅDE
gap-beskrivelsen og kravsitatet, slik at de ikke lenger delte noe nøkkelord
og gapet ble oppfattet som "ikke forankret i et relevant krav" og fjernet.
Dette kunne bekreftes direkte ved å kjøre `_shares_relevant_keyword` på
representativ tekst, uavhengig av hva språkmodellen faktisk svarte i den
aktuelle sesjonen (som ikke logges, se under).

Det er derfor ikke mulig å fastslå med 100 % sikkerhet om språkmodellen i
den konkrete, virkelige forespørselen aldri genererte SQL-gapet, siden
rå-svaret fra modellen ikke lagres eller logges noe sted (bevisst, for å
unngå å lagre CV-/annonseinnhold, jf. NFR3). Det som derimot ER bevist ved
kjøring av koden: slik `grounding.py` var skrevet, ville den garantert ha
fjernet et slikt gap selv om modellen leverte det helt korrekt. Siden dette
i seg selv er en fullt tilstrekkelig forklaring, og effekten er eksakt den
observerte, er den mest sannsynlige konklusjonen at `grounding.py` var
(hoved-)årsaken. `analysis_service.py` logger nå antall funn før/etter
grunnlagskontrollen (uten noe CV-/annonseinnhold), slik at dette kan
bekreftes direkte i fremtidige ekte kall.

Denne modulen gjør derfor to ting, ikke bare én:
- `_excerpt_is_grounded`: finnes sitatet ordrett i riktig kildetekst? Dette
  er den eneste kontrollen som avgjør om et PÅKREVD kildesitat beholdes, og
  dermed om funnet i det hele tatt vises (se begrunnelse under).
- `_shares_relevant_keyword`: handler sitatet/kravet faktisk om samme tema
  som funnets egen påstand? (en enkel, deterministisk nøkkelord-heuristikk)

Nøkkelord-heuristikken brukes bevisst BEGRENSET, ikke som en generell
relevans-dommer, etter erfaringen over:
- Den avgjør ALDRI om et påkrevd kildesitat (`job_ad_excerpt` for gap/forslag)
  beholdes – der er et ekte, ordrett sitat alltid tilstrekkelig. Å også
  kreve nøkkelord-overlapp her var nettopp det som slettet SQL-gapet.
- Den brukes til å luke `related_requirement_ids` (lav kostnad å ta feil:
  funnet vises fortsatt, bare uten den ene krav-koblingen) og til å nulle ut
  et VALGFRITT `cv_excerpt` på CV-forslag (samme lave kostnad).
- Den brukes fortsatt til å avgjøre om styrkers PÅKREVDE `cv_excerpt`
  beholdes, siden det er det eneste feltet en styrke har – uten det er det
  ingen dokumentert styrke å vise.

For å gjøre det tydelig skille mellom dokumentert kompetanse, manglende
kompetansedokumentasjon og betingede forslag – uten å endre skjemaet – brukes
feltene slik:
- Styrke (`Strength`): `cv_excerpt` er obligatorisk og må faktisk dokumentere
  påstanden (ordrett OG relevant). Uten det er det ikke en dokumentert
  styrke, og funnet fjernes.
- Kompetansegap (`CompetencyGap`): `cv_excerpt` settes alltid til `None`,
  siden et gap per definisjon er noe CV-en IKKE dokumenterer. `job_ad_excerpt`
  er obligatorisk og må finnes ordrett i annonsen (ikke lenger krevd å dele
  nøkkelord med beskrivelsen – se begrunnelse over).
- CV-forslag (`CvSuggestion`): `job_ad_excerpt` er obligatorisk på samme vis
  (kun ordrett kontroll). `cv_excerpt` er valgfritt – det brukes bare når
  forslaget handler om å omformulere/fremheve noe som allerede står i
  CV-en, og fjernes (settes til `None`) hvis det ikke er reelt relevant for
  forslaget. Dette representerer et "betinget forslag" (noe stillingen
  ønsker, som ikke er dokumentert i CV-en) uten å late som kompetansen finnes.

Begrensning som fortsatt gjelder, og som er en bevisst, akseptert avveining
(ikke noe vi kan løse uten en vesentlig mer komplisert løsning, f.eks.
semantisk/embedding-basert sammenligning eller en synonymordbok): en ren
nøkkelord-heuristikk kan ikke skille perfekt mellom "åpenbart feilkoblet"
(bacheloroppgave koblet til Power BI) og "reelt relatert, men med andre ord"
(kundeservice/opplæring koblet til kommunikasjonsevner) – begge mangler delt
ordforråd. Derfor vil `related_requirement_ids`-filteret fortsatt i noen
tilfeller fjerne en riktig kobling som er formulert med andre ord enn kravet.
Dette er dokumentert og testet som kjent, akseptert oppførsel (se
`test_grounding.py`), ikke en feil – kostnaden ved det er lav (funnet vises
fortsatt, bare uten den ene krav-koblingen), mens den opprinnelige feilen
(bacheloroppgave->Power BI) var en synlig, misvisende påstand om relevans.

En tredje runde med manuell kvalitetssikring (06.11.2026, testsett 4
"Thomas Berg" i `backend/test-data/manual-qa/`) viste en ny, konkret feil av
samme familie: en vag styrke om "digitale verktøy" ble koblet via
`related_requirement_ids` til et spesifikt krav om "prosjektstyringsverktøy
som Jira eller Trello". Årsaken (igjen undersøkt i koden, ikke gjettet):
`_filter_related_requirement_ids` sammenlignet kravets beskrivelse mot
funnets egen påstand OG BÅDE `cv_excerpt` OG `job_ad_excerpt` samlet. Siden
språkmodellen hadde satt `job_ad_excerpt` til nøyaktig kravets egen
beskrivelsestekst, "delte" kravet nøkkelord med seg selv – helt uavhengig av
om `cv_excerpt` ("digitale verktøy") faktisk hadde noe å gjøre med kravet
("Jira eller Trello"). Fiksen fjerner `job_ad_excerpt` fra dette
sammenligningsgrunnlaget: kun funnets egen påstand og dets faktiske
CV-dokumentasjon kan nå bekrefte en krav-kobling. Dette er bevisst en minimal
endring – kun denne ene sammenligningen er justert – og er verifisert mot at
legitime koblinger (bl.a. et kort fagord som "SQL", og overførbar erfaring
fra en deltidsjobb) fortsatt fungerer, se `test_grounding.py`.
"""

from __future__ import annotations

import re

from .models import AnalysisResult, CompetencyGap, CvSuggestion, JobRequirement, SourceReference, Strength

# Ord som er for generiske i en jobbsøknadskontekst til å telle som et reelt
# tematisk treff mellom et funn og et krav – de dukker opp nesten overalt
# ("erfaring", "kompetanse", ...), og ville gjort koblingskontrollen
# virkningsløs hvis de fikk telle som bevis på at to tekster handler om det
# samme. Inneholder også korte, grammatiske fyllord, siden minstelengden
# under er satt lav nok til at korte fagord som "SQL" skal telle.
_GENERIC_WORDS = {
    "erfaring", "erfaringer", "kompetanse", "kompetansen", "kunnskap",
    "kunnskaper", "ferdighet", "ferdigheter", "arbeid", "arbeidet",
    "arbeide", "arbeidsoppgaver", "jobb", "jobber", "stilling", "stillingen",
    "krav", "kravene", "evne", "evner", "relevant", "relevante",
    "dokumentert", "dokumentere", "oppgave", "oppgaven", "oppgaver",
    "prosjekt", "prosjektet", "prosjekter", "student", "studiet", "studier",
    "viktig", "viktige", "sentral", "sentrale", "ønskelig", "innen",
    # Korte, grammatiske fyllord (bare relevant nå når minstelengden er 3,
    # ikke 4 – uten disse ville de telt som "betydningsfulle" nøkkelord).
    "som", "for", "med", "har", "kan", "vil", "ved", "fra", "det", "den",
    "den", "din", "min", "sin", "god", "gode", "godt", "noe", "noen", "alle",
    "all", "men", "når", "hva", "hvem", "hvor", "samt", "også", "under",
    "over", "etter",
}


def _normalize(text: str) -> str:
    """Mellomrom og store/små bokstaver normaliseres bort, slik at små
    formateringsforskjeller ikke gir falske negativer."""

    return re.sub(r"\s+", " ", text).strip().casefold()


def _excerpt_is_grounded(excerpt: str, source_text: str) -> bool:
    if not excerpt.strip():
        return False
    return _normalize(excerpt) in _normalize(source_text)


def _significant_words(text: str) -> set[str]:
    """Ord på minst 3 bokstaver, utenom generiske fyllord.

    Minstelengden var tidligere 4, noe som utelukket korte, men presise
    fagord/forkortelser som "SQL" fra å telle som et treff mellom to tekster
    – se modulens docstring for hvordan dette ble oppdaget og bekreftet.
    """

    words = re.findall(r"[a-zæøå]+", text.casefold())
    return {w for w in words if len(w) >= 3 and w not in _GENERIC_WORDS}


def _shares_relevant_keyword(a: str, b: str) -> bool:
    """Enkel, deterministisk heuristikk for tematisk overlapp: deler de to
    tekstene minst ett ord som ikke er et generisk fyllord? Se modulens
    docstring for begrunnelse og begrensning."""

    return bool(_significant_words(a) & _significant_words(b))


def _own_claim_text(item: Strength | CompetencyGap | CvSuggestion) -> str:
    return getattr(item, "description", None) or getattr(item, "suggestion", "")


def _clean_source(
    item: Strength | CompetencyGap | CvSuggestion,
    *,
    cv_text: str,
    job_ad_text: str,
    force_cv_excerpt_none: bool = False,
) -> SourceReference:
    """Nuller ut kildesitater som ikke bør vises.

    `job_ad_excerpt` avgjøres UTELUKKENDE av om sitatet er ordrett ekte – se
    modulens docstring for hvorfor nøkkelord-relevans ble fjernet fra denne
    kontrollen (det var nettopp det som slettet et korrekt SQL-gap).
    `job_ad_excerpt` er obligatorisk for gap/forslag, så denne kontrollen er
    den eneste bremsen på om hele funnet vises – derfor skal den ikke kunne
    si nei på grunn av en nøkkelord-heuristikk.

    `cv_excerpt` kontrolleres både for at det er ordrett ekte OG at det
    tematisk handler om samme sak som funnets egen påstand (`own_text`).
    Samme regel gjelder for styrker og CV-forslag – forskjellen i hvor streng
    konsekvensen blir ligger hos den kallende funksjonen: for en styrke er
    `cv_excerpt` det eneste, obligatoriske sitatet (ingen `cv_excerpt` ⇒
    styrken fjernes), mens det for et CV-forslag er valgfritt (ingen
    `cv_excerpt` ⇒ forslaget vises likevel, motivert av `job_ad_excerpt`).
    """

    own_text = _own_claim_text(item)
    source = item.source

    if force_cv_excerpt_none:
        cv_excerpt = None
    else:
        cv_excerpt = source.cv_excerpt
        if cv_excerpt is not None and not (
            _excerpt_is_grounded(cv_excerpt, cv_text) and _shares_relevant_keyword(cv_excerpt, own_text)
        ):
            cv_excerpt = None

    job_ad_excerpt = source.job_ad_excerpt
    if job_ad_excerpt is not None and not _excerpt_is_grounded(job_ad_excerpt, job_ad_text):
        job_ad_excerpt = None

    return SourceReference(cv_excerpt=cv_excerpt, job_ad_excerpt=job_ad_excerpt)


def _filter_related_requirement_ids(
    item: Strength | CompetencyGap | CvSuggestion,
    cleaned_source: SourceReference,
    requirements_by_id: dict[str, JobRequirement],
) -> list[str]:
    """Beholder kun krav-ID-er der selve kravteksten faktisk handler om
    samme tema som funnet – dette er den direkte fiksen for at f.eks. en
    styrke om en bacheloroppgave ble koblet til et krav om Power BI.

    `job_ad_excerpt` er BEVISST IKKE med i sammenligningsgrunnlaget her.
    Et `job_ad_excerpt` er nesten alltid hentet fra stillingsannonsen, og
    kan derfor lett overlappe med SELVE kravet det er festet til – helt
    uavhengig av om CV-en faktisk dokumenterer noe relevant. Manuell
    kvalitetssikring (06.11.2026, testsett 4 "Thomas Berg") viste nøyaktig
    dette: en vag styrke om "digitale verktøy" ble koblet til et spesifikt
    Jira/Trello-krav fordi styrkens `job_ad_excerpt` var satt til nøyaktig
    kravets egen beskrivelsestekst – kravet "delte nøkkelord" med seg selv.
    Det er derfor kun funnets egen påstand og dets faktiske CV-dokumentasjon
    (`cv_excerpt`) som avgjør om en krav-kobling er reell."""

    own_text = " ".join(
        part
        for part in (_own_claim_text(item), cleaned_source.cv_excerpt or "")
        if part
    )

    return [
        req_id
        for req_id in item.related_requirement_ids
        if (requirement := requirements_by_id.get(req_id)) is not None
        and _shares_relevant_keyword(requirement.description, own_text)
    ]


def _clean_strength(
    item: Strength, *, cv_text: str, job_ad_text: str, requirements_by_id: dict[str, JobRequirement]
) -> Strength | None:
    cleaned_source = _clean_source(item, cv_text=cv_text, job_ad_text=job_ad_text)
    if cleaned_source.cv_excerpt is None:
        return None  # En styrke uten et reelt, relevant CV-sitat er ikke dokumentert.

    related_ids = _filter_related_requirement_ids(item, cleaned_source, requirements_by_id)
    return item.model_copy(update={"source": cleaned_source, "related_requirement_ids": related_ids})


def _clean_gap(
    item: CompetencyGap, *, cv_text: str, job_ad_text: str, requirements_by_id: dict[str, JobRequirement]
) -> CompetencyGap | None:
    cleaned_source = _clean_source(
        item, cv_text=cv_text, job_ad_text=job_ad_text, force_cv_excerpt_none=True
    )
    if cleaned_source.job_ad_excerpt is None:
        return None  # Et kompetansegap må kunne spores til et faktisk, relevant krav.

    related_ids = _filter_related_requirement_ids(item, cleaned_source, requirements_by_id)
    return item.model_copy(update={"source": cleaned_source, "related_requirement_ids": related_ids})


def _clean_suggestion(
    item: CvSuggestion, *, cv_text: str, job_ad_text: str, requirements_by_id: dict[str, JobRequirement]
) -> CvSuggestion | None:
    cleaned_source = _clean_source(item, cv_text=cv_text, job_ad_text=job_ad_text)
    if cleaned_source.job_ad_excerpt is None:
        return None  # Et CV-forslag må være motivert av et faktisk, relevant krav.

    related_ids = _filter_related_requirement_ids(item, cleaned_source, requirements_by_id)
    return item.model_copy(update={"source": cleaned_source, "related_requirement_ids": related_ids})


def enforce_grounding(result: AnalysisResult, *, cv_text: str, job_ad_text: str) -> AnalysisResult:
    """Returnerer en kopi av `result` der:
    - styrker uten et reelt, relevant CV-sitat er fjernet,
    - kompetansegap aldri har et `cv_excerpt` og er fjernet hvis de mangler
      et reelt (ordrett) `job_ad_excerpt`,
    - CV-forslag er fjernet hvis de mangler et reelt (ordrett) `job_ad_excerpt`
      (et valgfritt `cv_excerpt` beholdes kun hvis det også er relevant),
    - `related_requirement_ids` er luket for krav som ikke tematisk handler
      om det samme som funnet.

    `job_requirements` og `application_draft` kontrolleres ikke her, siden de
    ikke har et eget `source`-felt i skjemaet.
    """

    requirements_by_id = {req.id: req for req in result.job_requirements}

    strengths = [
        cleaned
        for item in result.strengths
        if (
            cleaned := _clean_strength(
                item, cv_text=cv_text, job_ad_text=job_ad_text, requirements_by_id=requirements_by_id
            )
        )
        is not None
    ]
    competency_gaps = [
        cleaned
        for item in result.competency_gaps
        if (
            cleaned := _clean_gap(
                item, cv_text=cv_text, job_ad_text=job_ad_text, requirements_by_id=requirements_by_id
            )
        )
        is not None
    ]
    cv_suggestions = [
        cleaned
        for item in result.cv_suggestions
        if (
            cleaned := _clean_suggestion(
                item, cv_text=cv_text, job_ad_text=job_ad_text, requirements_by_id=requirements_by_id
            )
        )
        is not None
    ]

    return result.model_copy(
        update={
            "strengths": strengths,
            "competency_gaps": competency_gaps,
            "cv_suggestions": cv_suggestions,
        }
    )
