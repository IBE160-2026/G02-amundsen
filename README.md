# G02 — Gruppe 222

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon **Career Transition Assistant** og dokumentasjon av utvikling, testing og kvalitetssikring med KI. Se [`prd.md`](prd.md), [`architecture.md`](architecture.md) og [`epics-and-stories.md`](epics-and-stories.md) for produkt- og arkitekturbeskrivelse.

## Medlemmer

- Sondre Tveit Amundsen

## Kjøre applikasjonen lokalt

Applikasjonen består av en React/Vite-frontend (`frontend/`) og en FastAPI-backend (`backend/`), som kjøres som to separate prosesser. I v1 finnes kun **demomodus**, som bruker en fast, fiktiv CV og stillingsannonse fra [`test-data/`](test-data/) og krever ingen API-nøkkel.

### 1. Start backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Backenden kjører da på `http://127.0.0.1:8000`. `GET /api/analyze/demo` returnerer demoresultatet, og `http://127.0.0.1:8000/docs` viser API-dokumentasjonen.

### 2. Start frontend

I et nytt terminalvindu:

```bash
cd frontend
npm install
npm run dev
```

Frontenden kjører da på `http://localhost:5173` og er satt opp til å kalle backenden på `http://127.0.0.1:8000` (se `frontend/.env.example`). Skal backenden kjøre på en annen adresse, kopier `.env.example` til `.env` i `frontend/` og endre `VITE_API_BASE_URL`.

Backenden tillater CORS-forespørsler fra `http://localhost:5173` og `http://127.0.0.1:5173` i lokal utvikling, slik at frontend og backend kan kjøre som separate prosesser uten CORS-feil.

### 3. Bruk demomodus

Åpne `http://localhost:5173` i nettleseren, velg **Demomodus** (normalmodus er foreløpig ikke implementert) og trykk **«Kjør demoanalyse»**. Resultatet viser den fiktive CV-en og stillingsannonsen, sentrale krav, relevante styrker, kompetansegap, CV-forslag med sporbarhet til CV og stillingsannonse, og et redigerbart søknadsutkast.

### Kjøre tester

```bash
cd backend && uv run pytest

cd frontend && npm test
```
