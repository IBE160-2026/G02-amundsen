"""Tester for innlasting av demodata (app.demo_data).

Kontrollerer at demofilene i backend/test-data/ faktisk finnes og kan lastes
inn til en gyldig AnalyzeResponse, uavhengig av HTTP-laget.

`test_test_data_dir_is_inside_backend_service_root` er lagt til etter en
konkret feil i produksjon: demodataene lå tidligere i en `test-data/`-mappe
på repo-roten, UTENFOR backend-tjenestens rot. Dette fungerte lokalt (hele
repoet ligger på disk), men Vercel Services bunter en Python-tjeneste kun
med filer inne i tjenestens egen rot-mappe (`backend/`), så filene fulgte
ikke med i produksjon – `GET /api/analyze/demo` svarte med
"Kunne ikke laste demodata". Denne testen fanger opp om noen flytter
datafilene ut av `backend/` igjen, noe de øvrige testene under IKKE ville
avdekket (de kjører alltid lokalt, der hele repoet er tilgjengelig).
"""

from pathlib import Path

from app.demo_data import (
    DEMO_CV_PATH,
    DEMO_JOB_AD_PATH,
    DEMO_RESULT_PATH,
    TEST_DATA_DIR,
    load_demo_response,
)
from app.models import AnalyzeResponse

BACKEND_ROOT = Path(__file__).resolve().parents[1]


def test_demo_data_files_exist():
    assert DEMO_CV_PATH.is_file()
    assert DEMO_JOB_AD_PATH.is_file()
    assert DEMO_RESULT_PATH.is_file()


def test_test_data_dir_is_inside_backend_service_root():
    """Demodata-mappen må ligge inne i `backend/` – ikke på repo-roten eller
    andre steder utenfor – for å bli bundlet med Vercel-tjenesten."""

    assert TEST_DATA_DIR.is_relative_to(BACKEND_ROOT)


def test_load_demo_response_returns_valid_model():
    response = load_demo_response()

    assert isinstance(response, AnalyzeResponse)
    assert response.mode == "demo"
    assert response.cv_text != ""
    assert response.job_ad_text != ""


def test_load_demo_response_is_cached_and_consistent():
    first = load_demo_response()
    second = load_demo_response()

    # lru_cache gjenbruker samme instans mellom kall i samme prosess.
    assert first is second
