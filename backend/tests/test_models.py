"""Tester for Pydantic-modellene i app.models.

Dekker grunnleggende validering, slik at ugyldige analyseresultater
(f.eks. et krav med ugyldig prioritet eller manglende felt) avvises før
de når frontend, uavhengig av om de kommer fra demomodus eller en
ekstern språkmodell i normal modus.
"""

import pytest
from pydantic import ValidationError

from app.models import (
    AnalysisResult,
    AnalyzeResponse,
    CompetencyGap,
    CvSuggestion,
    JobRequirement,
    SourceReference,
    Strength,
)


def _minimal_result() -> dict:
    return {
        "job_requirements": [
            {"id": "r1", "description": "Krav A", "priority": "sentral"}
        ],
        "strengths": [
            {
                "id": "s1",
                "description": "Styrke A",
                "related_requirement_ids": ["r1"],
                "source": {"cv_excerpt": "CV-utdrag", "job_ad_excerpt": "Annonse-utdrag"},
            }
        ],
        "competency_gaps": [
            {
                "id": "g1",
                "description": "Gap A",
                "related_requirement_ids": ["r1"],
                "source": {"cv_excerpt": None, "job_ad_excerpt": "Annonse-utdrag"},
            }
        ],
        "cv_suggestions": [
            {
                "id": "c1",
                "suggestion": "Forslag A",
                "related_requirement_ids": ["r1"],
                "source": {"cv_excerpt": "CV-utdrag", "job_ad_excerpt": "Annonse-utdrag"},
            }
        ],
        "application_draft": "Kjære rekrutterer, ...",
    }


def test_analysis_result_accepts_valid_data():
    result = AnalysisResult.model_validate(_minimal_result())

    assert len(result.job_requirements) == 1
    assert result.job_requirements[0].priority == "sentral"
    assert result.strengths[0].source.cv_excerpt == "CV-utdrag"
    assert result.competency_gaps[0].source.cv_excerpt is None


def test_source_reference_allows_missing_cv_excerpt_for_gaps():
    # Et kompetansegap kan forankres kun i stillingsannonsen, siden
    # informasjonen per definisjon ikke finnes i CV-en.
    source = SourceReference(cv_excerpt=None, job_ad_excerpt="Krever Scrum-erfaring")

    assert source.cv_excerpt is None
    assert source.job_ad_excerpt == "Krever Scrum-erfaring"


def test_job_requirement_rejects_invalid_priority():
    with pytest.raises(ValidationError):
        JobRequirement(id="r1", description="Krav A", priority="kritisk")


def test_job_requirement_requires_description():
    with pytest.raises(ValidationError):
        JobRequirement(id="r1", priority="sentral")  # type: ignore[call-arg]


def test_strength_requires_source():
    with pytest.raises(ValidationError):
        Strength(id="s1", description="Styrke A")  # type: ignore[call-arg]


def test_analyze_response_requires_valid_mode():
    payload = {
        "mode": "normal",
        "cv_text": "CV-tekst",
        "job_ad_text": "Annonse-tekst",
        "result": _minimal_result(),
    }

    response = AnalyzeResponse.model_validate(payload)
    assert response.mode == "normal"

    with pytest.raises(ValidationError):
        AnalyzeResponse.model_validate({**payload, "mode": "ugyldig"})


def test_competency_gap_and_cv_suggestion_default_related_ids_to_empty_list():
    gap = CompetencyGap(
        id="g1", description="Gap A", source=SourceReference(job_ad_excerpt="X")
    )
    suggestion = CvSuggestion(
        id="c1", suggestion="Forslag A", source=SourceReference(job_ad_excerpt="X")
    )

    assert gap.related_requirement_ids == []
    assert suggestion.related_requirement_ids == []
