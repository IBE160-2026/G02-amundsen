from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from .analysis_service import (
    ApiKeyMissingError,
    LlmRequestError,
    LlmResponseInvalidError,
    LlmTimeoutError,
    run_normal_mode_analysis,
)
from .demo_data import load_demo_response
from .models import AnalyzeRequest, AnalyzeResponse

app = FastAPI(title="Career Transition Assistant API")

# Frontenden kjører som en separat utviklingsserver (Vite). Standardporten
# er 5173, men Vite velger automatisk 5174 (eller høyere) hvis 5173 allerede
# er i bruk (f.eks. en annen kjørende dev-server) – begge porter må derfor
# tillates for at lokal utvikling skal fungere uavhengig av hvilken port
# Vite faktisk endte opp med (architecture.md, avsnitt "Kommunikasjon" og
# "Local Development"). Listen er bevisst eksplisitt og begrenset til disse
# lokale origins – CORS skal IKKE åpnes for alle domener (`allow_origins`
# skal aldri settes til `["*"]`).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_methods=["GET", "POST"],
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


@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Kjører normalmodus (FR1-FR10): sender brukerens CV og stillingsannonse
    til en ekstern språkmodell (OpenAI) og returnerer et strukturert,
    sporbart resultat med samme form som demomodus.

    Krever at `OPENAI_API_KEY` er konfigurert i `backend/.env` – se
    `backend/.env.example`.
    """

    try:
        result = run_normal_mode_analysis(request.cv_text, request.job_ad_text)
    except ApiKeyMissingError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=(
                "Normalmodus er ikke tilgjengelig: ingen gyldig API-nøkkel er "
                "konfigurert på serveren. Bruk demomodus i mellomtiden."
            ),
        ) from exc
    except LlmTimeoutError as exc:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Språkmodellen svarte ikke innen tidsfristen. Prøv igjen.",
        ) from exc
    except (LlmRequestError, LlmResponseInvalidError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Kunne ikke hente et gyldig svar fra språkmodellen. Prøv igjen senere.",
        ) from exc

    return AnalyzeResponse(
        mode="normal",
        cv_text=request.cv_text,
        job_ad_text=request.job_ad_text,
        result=result,
    )
