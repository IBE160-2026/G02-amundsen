# G02 — Gruppe 222

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon **Career Transition Assistant** og dokumentasjon av utvikling, testing og kvalitetssikring med KI. Se [`prd.md`](prd.md), [`architecture.md`](architecture.md) og [`epics-and-stories.md`](epics-and-stories.md) for produkt- og arkitekturbeskrivelse.

## Medlemmer

- Sondre Tveit Amundsen

## Kjøre applikasjonen lokalt

Applikasjonen består av en React/Vite-frontend (`frontend/`) og en FastAPI-backend (`backend/`), som kjøres som to separate prosesser. **Demomodus** bruker en fast, fiktiv CV og stillingsannonse fra [`test-data/`](test-data/) og krever ingen API-nøkkel. Backenden har nå også et **normalmodus**-endepunkt som bruker OpenAI (`gpt-5.4-mini`), men dette er foreløpig ikke koblet til frontend – det testes direkte mot backend-API-et (se under).

### 1. Start backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Backenden kjører da på `http://127.0.0.1:8000`. `GET /api/analyze/demo` returnerer demoresultatet, og `http://127.0.0.1:8000/docs` viser API-dokumentasjonen.

For å bruke normalmodus (`POST /api/analyze`) må du kopiere `backend/.env.example` til `backend/.env` og fylle inn en egen `OPENAI_API_KEY`. Denne filen skal **aldri** committes (den er dekket av `.gitignore`). Uten en nøkkel svarer `/api/analyze` med en tydelig feilmelding (HTTP 503), mens demomodus fortsatt fungerer som normalt.

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

### 4. Test normalmodus direkte mot backend (uten frontend)

Når `backend/.env` har en gyldig `OPENAI_API_KEY`:

```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"cv_text": "...", "job_ad_text": "..."}'
```

Du kan også bruke `http://127.0.0.1:8000/docs` ("Try it out" på `POST /api/analyze`). Svaret har samme struktur som demomodus, men `mode` er `"normal"` og innholdet er generert av språkmodellen – med kildesitater som er kontrollert mot din CV/stillingsannonse (se `app/grounding.py`).

### Kjøre tester

```bash
cd backend && uv run pytest

cd frontend && npm test
```
