"""Lasting av demodata for Career Transition Assistant.

Demomodus skal bruke en fast, fiktiv CV, en fast, fiktiv stillingsannonse og
et fast eksempelresultat med samme struktur som et ekte KI-svar, og skal ikke
gjøre noen kall til en ekstern språkmodell (architecture.md, avsnitt
"Demo Mode"; PRD FR12).

Demodataene lagres som egne prosjektfiler i `test-data/` på rot-nivå i
repoet, slik arkitekturdokumentet beskriver, i stedet for å være hardkodet i
Python-koden.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .models import AnalysisResult, AnalyzeResponse

# backend/app/demo_data.py -> parents[1] er "backend/", parents[2] er repo-roten.
TEST_DATA_DIR = Path(__file__).resolve().parents[2] / "test-data"

DEMO_CV_PATH = TEST_DATA_DIR / "demo-cv.txt"
DEMO_JOB_AD_PATH = TEST_DATA_DIR / "demo-job-ad.txt"
DEMO_RESULT_PATH = TEST_DATA_DIR / "demo-result.json"


@lru_cache(maxsize=1)
def load_demo_response() -> AnalyzeResponse:
    """Leser demofilene fra disk og bygger en validert AnalyzeResponse.

    Resultatet caches siden demodataene er statiske prosjektfiler som ikke
    endrer seg mellom forespørsler i en kjørende prosess.
    """

    cv_text = DEMO_CV_PATH.read_text(encoding="utf-8").strip()
    job_ad_text = DEMO_JOB_AD_PATH.read_text(encoding="utf-8").strip()
    result_data = json.loads(DEMO_RESULT_PATH.read_text(encoding="utf-8"))

    return AnalyzeResponse(
        mode="demo",
        cv_text=cv_text,
        job_ad_text=job_ad_text,
        result=AnalysisResult.model_validate(result_data),
    )
