from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .demo_data import load_demo_response
from .models import AnalyzeResponse

app = FastAPI(title="Career Transition Assistant API")

# Frontenden kjører som en separat utviklingsserver (Vite, typisk port 5173)
# og må derfor få lov til å kalle backend-API-et over CORS i lokal utvikling
# (architecture.md, avsnitt "Kommunikasjon" og "Local Development").
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)


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
