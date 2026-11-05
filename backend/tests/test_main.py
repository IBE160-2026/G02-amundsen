"""Tester for FastAPI-endepunktene i Career Transition Assistant.

Dekker:
- at det eksisterende GET /-endepunktet fortsatt fungerer
- at demomodus-endepunktet svarer uten noen ekstern språkmodell
- at responsen fra demomodus følger den strukturen architecture.md og
  prd.md krever: sentrale krav, styrker, kompetansegap, CV-forslag med
  sporbarhet og et søknadsutkast (FR3-FR8, NFR8)
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_root_still_works():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Career Transition Assistant backend is running"
    }


def test_demo_endpoint_returns_200():
    response = client.get("/api/analyze/demo")

    assert response.status_code == 200


def test_demo_endpoint_uses_demo_mode_and_fixed_input():
    response = client.get("/api/analyze/demo")
    data = response.json()

    assert data["mode"] == "demo"
    # Demomodus skal bruke en fast, fiktiv CV og stillingsannonse (FR12).
    assert "Kari Nordmann" in data["cv_text"]
    assert "Fjord Digital AS" in data["job_ad_text"]


def test_demo_result_has_required_top_level_sections():
    response = client.get("/api/analyze/demo")
    result = response.json()["result"]

    # Resultatet skal minst inneholde: sentrale krav, styrker,
    # kompetansegap, CV-forslag og søknadsutkast (architecture.md,
    # avsnitt "Structured Output").
    for key in (
        "job_requirements",
        "strengths",
        "competency_gaps",
        "cv_suggestions",
        "application_draft",
    ):
        assert key in result

    assert len(result["job_requirements"]) > 0
    assert len(result["strengths"]) > 0
    assert len(result["competency_gaps"]) > 0
    assert len(result["cv_suggestions"]) > 0
    assert isinstance(result["application_draft"], str)
    assert result["application_draft"].strip() != ""


def test_demo_requirements_have_valid_priority():
    response = client.get("/api/analyze/demo")
    requirements = response.json()["result"]["job_requirements"]

    for requirement in requirements:
        assert requirement["priority"] in ("sentral", "ønskelig")
        assert requirement["id"]
        assert requirement["description"]


def test_demo_strengths_are_traceable_to_cv_and_job_ad():
    response = client.get("/api/analyze/demo")
    strengths = response.json()["result"]["strengths"]

    assert len(strengths) > 0
    for strength in strengths:
        source = strength["source"]
        # Styrker skal kunne spores tilbake til CV-en (FR4, FR7).
        assert source["cv_excerpt"]
        assert source["job_ad_excerpt"]


def test_demo_competency_gaps_reference_job_requirements():
    response = client.get("/api/analyze/demo")
    gaps = response.json()["result"]["competency_gaps"]

    assert len(gaps) > 0
    for gap in gaps:
        # Kompetansegap skal spores tilbake til krav i stillingsannonsen (FR5).
        assert gap["source"]["job_ad_excerpt"]
        assert len(gap["related_requirement_ids"]) > 0


def test_demo_cv_suggestions_are_traceable():
    response = client.get("/api/analyze/demo")
    suggestions = response.json()["result"]["cv_suggestions"]

    assert len(suggestions) > 0
    for suggestion in suggestions:
        assert suggestion["suggestion"]
        source = suggestion["source"]
        # CV-forslag skal vise hvilken del av CV og stillingsannonse de
        # bygger på (FR6, FR7, Story 3.2).
        assert source["cv_excerpt"]
        assert source["job_ad_excerpt"]


def test_demo_requirement_ids_referenced_by_strengths_exist():
    response = client.get("/api/analyze/demo")
    result = response.json()["result"]

    requirement_ids = {req["id"] for req in result["job_requirements"]}

    for strength in result["strengths"]:
        for req_id in strength["related_requirement_ids"]:
            assert req_id in requirement_ids

    for gap in result["competency_gaps"]:
        for req_id in gap["related_requirement_ids"]:
            assert req_id in requirement_ids


def test_demo_endpoint_is_idempotent_and_stable():
    """Demomodus skal gi et stabilt, fast eksempelresultat (FR12, NFR6),
    i motsetning til et ekte språkmodellsvar som kan variere."""

    first = client.get("/api/analyze/demo").json()
    second = client.get("/api/analyze/demo").json()

    assert first == second
