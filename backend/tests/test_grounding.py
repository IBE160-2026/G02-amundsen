"""Tester for grunnlagskontrollen (app.grounding).

Rent deterministiske tester – ingen kall til OpenAI.

- Tre av testene (`test_*_mirrors_qa_report_*`) speiler de opprinnelige
  feilene fra manuell kvalitetssikring av et ekte svar (05.11.2026): en
  styrke feilkoblet til et urelatert krav, et kompetansegap feilkoblet til
  feil krav, og et CV-forslag med et irrelevant CV-sitat.
- Testene merket `*_followup_fix_*` speiler et påfølgende ekte funn samme
  dag: et korrekt SQL-kompetansegap forsvant helt fordi nøkkelord-
  heuristikken krevde minst 4 bokstaver (og dermed utelukket "SQL"), og en
  styrke mistet en reelt relevant krav-kobling. Se docstringen i
  `app/grounding.py` for hvordan dette ble bekreftet (ikke gjettet).
"""

from app.grounding import _shares_relevant_keyword, enforce_grounding
from app.models import (
    AnalysisResult,
    CompetencyGap,
    CvSuggestion,
    JobRequirement,
    SourceReference,
    Strength,
)

CV_TEXT = (
    "Kari Nordmann\nMaster i informatikk.\n"
    "Bacheloroppgave om kundetilfredshet i varehandelen.\n"
    "Erfaring med Python og JavaScript.\n"
    "Kundeservice og opplæring av nyansatte i deltidsjobb."
)
JOB_AD_TEXT = (
    "Vi søker en utvikler.\n"
    "Krever kjennskap til Python.\n"
    "Krever erfaring med Power BI for rapportering.\n"
    "Krever god kjennskap til SQL for rapportering.\n"
    "Gode kommunikasjonsevner er ønskelig."
)


def _result(
    strengths=None, gaps=None, suggestions=None, job_requirements=None
) -> AnalysisResult:
    return AnalysisResult(
        job_requirements=job_requirements or [],
        strengths=strengths or [],
        competency_gaps=gaps or [],
        cv_suggestions=suggestions or [],
        application_draft="Utkast.",
    )


# --- Grunnleggende sitat-kontroll (ordrett, normalisert) -------------------


def test_shares_relevant_keyword_true_for_real_overlap():
    assert _shares_relevant_keyword("Erfaring med Python", "Krever kjennskap til Python") is True


def test_shares_relevant_keyword_false_when_only_generic_words_overlap():
    # Begge nevner "kompetanse"/"erfaring"/"prosjekt", men handler ikke om samme tema.
    a = "God kompetanse innen prosjektarbeid og erfaring fra tidligere prosjekter"
    b = "Relevant erfaring og kompetanse er en fordel i dette prosjektet"

    assert _shares_relevant_keyword(a, b) is False


def test_enforce_grounding_strength_requires_grounded_and_relevant_cv_excerpt():
    grounded = Strength(
        id="s1",
        description="Relevant Python-erfaring",
        source=SourceReference(cv_excerpt="Erfaring med Python", job_ad_excerpt="Python"),
    )
    fabricated = Strength(
        id="s2",
        description="Oppdiktet styrke",
        source=SourceReference(cv_excerpt="Ti års ledererfaring", job_ad_excerpt="Python"),
    )
    result = _result(strengths=[grounded, fabricated])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert [s.id for s in cleaned.strengths] == ["s1"]


def test_enforce_grounding_does_not_mutate_original_result():
    fabricated = Strength(
        id="s2",
        description="Oppdiktet styrke",
        source=SourceReference(cv_excerpt="Ti års ledererfaring", job_ad_excerpt="Python"),
    )
    result = _result(strengths=[fabricated])

    enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert len(result.strengths) == 1  # originalen er uendret


# --- Kompetansegap: cv_excerpt skal alltid bli None ------------------------


def test_enforce_grounding_gap_cv_excerpt_is_always_removed_even_if_real():
    gap = CompetencyGap(
        id="g1",
        description="Mangler Power BI-erfaring",
        source=SourceReference(
            cv_excerpt="Erfaring med Python",  # ekte sitat, men skal likevel fjernes
            job_ad_excerpt="Krever erfaring med Power BI for rapportering",
        ),
    )
    result = _result(gaps=[gap])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert len(cleaned.competency_gaps) == 1
    assert cleaned.competency_gaps[0].source.cv_excerpt is None
    assert cleaned.competency_gaps[0].source.job_ad_excerpt is not None


def test_enforce_grounding_gap_without_grounded_job_ad_excerpt_is_dropped():
    # Sitatet finnes IKKE ordrett i annonsen – dette er fortsatt obligatorisk.
    gap = CompetencyGap(
        id="g1",
        description="Mangler Power BI-erfaring",
        source=SourceReference(cv_excerpt=None, job_ad_excerpt="Noe som ikke finnes i annonsen"),
    )
    result = _result(gaps=[gap])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert cleaned.competency_gaps == []


def test_enforce_grounding_gap_survives_even_without_keyword_overlap_in_description():
    """Dette er den generelle versjonen av SQL-fiksen: et `job_ad_excerpt`
    som er ordrett ekte skal IKKE også måtte dele nøkkelord med gapets egen
    beskrivelse for å overleve – den kontrollen var nettopp det som slettet
    et korrekt SQL-gap (se app/grounding.py sin docstring)."""

    gap = CompetencyGap(
        id="g2",
        description="Ikke dokumentert i CV-en",  # deler ingen ord med sitatet under
        source=SourceReference(cv_excerpt=None, job_ad_excerpt="Krever kjennskap til Python"),
    )
    result = _result(gaps=[gap])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert len(cleaned.competency_gaps) == 1


# --- CV-forslag: cv_excerpt må være relevant, job_ad_excerpt er obligatorisk


def test_enforce_grounding_suggestion_without_job_ad_excerpt_is_dropped():
    suggestion = CvSuggestion(
        id="c1",
        suggestion="Fremhev Python-ferdighetene tidligere i CV-en",
        source=SourceReference(cv_excerpt="Erfaring med Python", job_ad_excerpt=None),
    )
    result = _result(suggestions=[suggestion])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert cleaned.cv_suggestions == []


# --- De tre konkrete feilene fra manuell kvalitetssikring (05.11.2026) -----


def test_strength_mirrors_qa_report_case_1_unrelated_requirement_is_unlinked():
    """S5 (bacheloroppgave om kundetilfredshet) var koblet til JR5 (Power BI),
    som ikke har noe å gjøre med oppgaven. Koblingen skal fjernes, men
    styrken i seg selv er fortsatt gyldig (sitatet er ekte og relevant)."""

    power_bi_requirement = JobRequirement(
        id="jr5", description="Krever erfaring med Power BI for rapportering"
    )
    strength = Strength(
        id="s5",
        description="Bacheloroppgave om kundetilfredshet i varehandelen",
        related_requirement_ids=["jr5"],
        source=SourceReference(
            cv_excerpt="Bacheloroppgave om kundetilfredshet i varehandelen",
            job_ad_excerpt=None,
        ),
    )
    result = _result(strengths=[strength], job_requirements=[power_bi_requirement])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert len(cleaned.strengths) == 1
    assert cleaned.strengths[0].related_requirement_ids == []


def test_gap_mirrors_qa_report_case_2_unrelated_requirement_is_unlinked():
    """G3 (rapportering/presentasjon av innsikt) var koblet til JR4
    (kommunikasjonsevner) – et urelatert, mer generelt krav. Koblingen skal
    fjernes, men selve gapet er fortsatt gyldig."""

    communication_requirement = JobRequirement(id="jr4", description="Gode kommunikasjonsevner")
    gap = CompetencyGap(
        id="g3",
        description="Ingen dokumentert erfaring med rapportering og presentasjon av innsikt",
        related_requirement_ids=["jr4"],
        source=SourceReference(
            cv_excerpt=None,
            job_ad_excerpt="Krever erfaring med Power BI for rapportering",
        ),
    )
    result = _result(gaps=[gap], job_requirements=[communication_requirement])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert len(cleaned.competency_gaps) == 1
    assert cleaned.competency_gaps[0].related_requirement_ids == []


def test_shares_relevant_keyword_now_counts_short_acronyms_like_sql():
    """Direkte regresjonstest for selve rotårsaken: "SQL" er 3 bokstaver og
    ble tidligere utelukket av en minstelengde på 4, slik at identiske SQL-
    omtaler i to tekster ikke talte som et treff."""

    assert _shares_relevant_keyword("Ingen erfaring med SQL", "Krever kjennskap til SQL") is True


def test_shares_relevant_keyword_still_ignores_short_norwegian_stopwords():
    # Regresjonsvern for å senke minstelengden til 3: vanlige, korte
    # grammatiske ord skal fortsatt IKKE telle som et reelt treff.
    a = "Du som har erfaring med ledelse kan vise det her"
    b = "Vi som ser etter folk med gode ferdigheter har en stilling ledig"

    assert _shares_relevant_keyword(a, b) is False


def test_gap_followup_fix_sql_gap_is_no_longer_dropped():
    """Speiler det konkrete, påfølgende ekte funnet: et SQL-kompetansegap
    forsvant helt. `description` og `job_ad_excerpt` deler her bare det
    korte ordet "SQL" – som beviselig var nok til å slette gapet før
    fiksen (se `test_shares_relevant_keyword_now_counts_short_acronyms_like_sql`
    og docstringen i `app/grounding.py`)."""

    gap = CompetencyGap(
        id="g_sql",
        description="Ingen dokumentert erfaring med SQL i CV-en",
        related_requirement_ids=[],
        source=SourceReference(
            cv_excerpt=None,
            job_ad_excerpt="Krever god kjennskap til SQL for rapportering",
        ),
    )
    result = _result(gaps=[gap])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert len(cleaned.competency_gaps) == 1
    assert cleaned.competency_gaps[0].source.job_ad_excerpt is not None


def test_strength_followup_known_limitation_differently_worded_link_is_still_removed():
    """Speiler det andre konkrete funnet: en styrke om kundeservice/
    opplæring mistet koblingen til et relevant krav om kommunikasjonsevner.

    Dette er en KJENT, AKSEPTERT begrensning (se app/grounding.py), ikke en
    feil som fikses her: "kundeservice"/"opplæring" og "kommunikasjonsevner"
    deler ikke noe ord, og en ren nøkkelord-heuristikk kan derfor ikke se at
    de er relatert uten en vesentlig mer komplisert løsning (f.eks.
    semantisk sammenligning eller en synonymordbok). Testen dokumenterer
    bevisst dagens oppførsel, slik at den ikke overrasker senere."""

    communication_requirement = JobRequirement(id="jr4", description="Gode kommunikasjonsevner")
    strength = Strength(
        id="s4",
        description="Kundeservice og opplæring av nyansatte",
        related_requirement_ids=["jr4"],
        source=SourceReference(
            cv_excerpt="Kundeservice og opplæring av nyansatte i deltidsjobb",
            job_ad_excerpt=None,
        ),
    )
    result = _result(strengths=[strength], job_requirements=[communication_requirement])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    # Styrken vises fortsatt (sitatet er ekte og relevant for styrken selv) –
    # det er bare krav-koblingen som forsvinner.
    assert len(cleaned.strengths) == 1
    assert cleaned.strengths[0].related_requirement_ids == []


def test_suggestion_mirrors_qa_report_case_3_irrelevant_cv_excerpt_is_dropped():
    """C5 var et korrekt formulert, betinget forslag om å legge til Power BI,
    men `cv_excerpt` pekte på bacheloroppgaven – som ikke dokumenterer Power
    BI. `cv_excerpt` skal fjernes, mens forslaget selv (motivert av
    `job_ad_excerpt`) beholdes."""

    suggestion = CvSuggestion(
        id="c5",
        suggestion=(
            "Vurder å nevne Power BI i CV-en din dersom du har brukt det i et "
            "prosjekt, siden stillingen etterspør rapporteringserfaring."
        ),
        source=SourceReference(
            cv_excerpt="Bacheloroppgave om kundetilfredshet i varehandelen",
            job_ad_excerpt="Krever erfaring med Power BI for rapportering",
        ),
    )
    result = _result(suggestions=[suggestion])

    cleaned = enforce_grounding(result, cv_text=CV_TEXT, job_ad_text=JOB_AD_TEXT)

    assert len(cleaned.cv_suggestions) == 1
    assert cleaned.cv_suggestions[0].source.cv_excerpt is None
    assert cleaned.cv_suggestions[0].source.job_ad_excerpt is not None
