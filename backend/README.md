# Career Transition Assistant – backend

FastAPI-backend for Career Transition Assistant. Se [prosjektets README](../README.md) for fulle oppstartsinstruksjoner for frontend og backend sammen.

## Oppstart

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Backenden kjører da på `http://127.0.0.1:8000`. `GET /` bekrefter at tjeneren kjører, `GET /api/analyze/demo` kjører demomodus, `POST /api/analyze` kjører normalmodus (krever `OPENAI_API_KEY`), og `http://127.0.0.1:8000/docs` viser API-dokumentasjonen.

## Normalmodus (OpenAI)

Kopier `.env.example` til `.env` og fyll inn `OPENAI_API_KEY` for å bruke `POST /api/analyze`. `.env` skal aldri committes. Uten en nøkkel svarer endepunktet med HTTP 503 og en forklarende feilmelding, mens demomodus fortsatt fungerer uendret.

## Tester

```bash
uv run pytest
```
