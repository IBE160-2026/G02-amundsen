from fastapi import FastAPI, HTTPException

from .demo_data import load_demo_response
from .models import AnalyzeResponse

app = FastAPI(title="Career Transition Assistant API")


@app.get("/")
def read_root():
    return {"message": "Career Transition Assistant backend is running"}


@app.get("/api/analyze/demo", response_model=AnalyzeResponse)
def analyze_demo() -> AnalyzeResponse:
    """Kjører demomodus (FR12, Story 1.3, Story 5.1).

    Bruker en fast, fiktiv CV og stillingsannonse og returnerer et fast
    eksempelresultat med samme struktur som normal modus skal returnere.
    Gjør ingen kall til en ekstern språkmodell.
    """

    try:
        return load_demo_response()
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="Kunne ikke laste demodata. Kontroller at test-data-filene finnes.",
        ) from exc
