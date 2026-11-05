"""Tester for innlasting av demodata (app.demo_data).

Kontrollerer at demofilene i test-data/ faktisk finnes og kan lastes inn
til en gyldig AnalyzeResponse, uavhengig av HTTP-laget.
"""

from app.demo_data import (
    DEMO_CV_PATH,
    DEMO_JOB_AD_PATH,
    DEMO_RESULT_PATH,
    load_demo_response,
)
from app.models import AnalyzeResponse


def test_demo_data_files_exist():
    assert DEMO_CV_PATH.is_file()
    assert DEMO_JOB_AD_PATH.is_file()
    assert DEMO_RESULT_PATH.is_file()


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
