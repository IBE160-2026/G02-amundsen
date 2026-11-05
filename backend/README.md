# Career Transition Assistant – backend

FastAPI-backend for Career Transition Assistant. Se [prosjektets README](../README.md) for fulle oppstartsinstruksjoner for frontend og backend sammen.

## Oppstart

```bash
uv sync
uv run uvicorn app.main:app --reload
```

Backenden kjører da på `http://127.0.0.1:8000`. `GET /` bekrefter at tjeneren kjører, `GET /api/analyze/demo` kjører demomodus, og `http://127.0.0.1:8000/docs` viser API-dokumentasjonen.

## Tester

```bash
uv run pytest
```
