"""Lasting av demodata for Career Transition Assistant.

Demomodus skal bruke en fast, fiktiv CV, en fast, fiktiv stillingsannonse og
et fast eksempelresultat med samme struktur som et ekte KI-svar, og skal ikke
gjøre noen kall til en ekstern språkmodell (architecture.md, avsnitt
"Demo Mode"; PRD FR12).

Demodataene lagres som egne prosjektfiler i `backend/test-data/`, i stedet
for å være hardkodet i Python-koden. Filene ligger bevisst INNE i
`backend/`, ikke på repo-roten: i produksjon kjører backenden som en egen
Vercel Service med `backend/` som tjenestens rot (se `vercel.json`), og en
slik Python-tjeneste bunter kun filer som faktisk ligger inne i rot-mappen.
Filer utenfor (f.eks. en `test-data/` på repo-roten) følger ikke med i
funksjonen som kjører i produksjon, og ga opphav til feilen "Kunne ikke
laste demodata" etter publisering – demodata fungerte lokalt, men fantes
ikke i det produksjonsbyggede funksjonen.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from .models import AnalysisResult, AnalyzeResponse

# backend/app/demo_data.py -> parents[0] er "app/", parents[1] er "backend/".
# Må IKKE gå lenger ut (f.eks. parents[2] til repo-roten) – se docstringen
# over for hvorfor.
TEST_DATA_DIR = Path(__file__).resolve().parents[1] / "test-data"

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
