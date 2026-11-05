# G02 — Gruppe 222

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon **Career Transition Assistant** og dokumentasjon av utvikling, testing og kvalitetssikring med KI. Se [`prd.md`](prd.md), [`architecture.md`](architecture.md) og [`epics-and-stories.md`](epics-and-stories.md) for produkt- og arkitekturbeskrivelse.

## Medlemmer

- Sondre Tveit Amundsen

## Kjøre applikasjonen lokalt

Applikasjonen består av en React/Vite-frontend (`frontend/`) og en FastAPI-backend (`backend/`), som under lokal utvikling kjøres som to separate prosesser. **Demomodus** bruker en fast, fiktiv CV og stillingsannonse fra [`backend/test-data/`](backend/test-data/) og krever ingen API-nøkkel. **Normalmodus** sender din egen CV og stillingsannonse til en ekte språkmodell (OpenAI, `gpt-5.4-mini`) via backenden, og krever en API-nøkkel (se under).

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

### 3. Bruk demo- eller normalmodus i grensesnittet

Åpne `http://localhost:5173` i nettleseren. Velg **Demomodus** og trykk **«Kjør demoanalyse»** for å se hovedflyten med fiktiv CV og stillingsannonse uten API-nøkkel, eller velg **Normalmodus**, lim inn din egen CV og stillingsannonse, og trykk **«Kjør analyse»**. Resultatet viser i begge tilfeller sentrale krav, relevante styrker, kompetansegap, CV-forslag med sporbarhet til CV og stillingsannonse, og et redigerbart søknadsutkast.

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

## Publisering på Vercel

IBE160 bruker Vercel som offisiell publiseringsløsning. Repoet er forberedt for
publisering med én **Vercel Services**-konfigurasjon i [`vercel.json`](vercel.json) i
repo-roten, som lar frontend (`frontend/`) og backend (`backend/`) kjøre som to
tjenester i **ett** Vercel-prosjekt, på samme domene: alt under `/api/*` rutes til
FastAPI-backenden, resten rutes til React/Vite-frontenden. Se `architecture.md`
avsnitt 10 for begrunnelse og alternativ løsning.

Dette er foreløpig kun forberedt, ikke publisert – ingen Vercel-prosjekt er opprettet.

### Manuelt i Vercel (når prosjektet opprettes)

1. Koble repoet til Vercel via GitHub-integrasjonen (gjøres i Vercel-dashbordet).
2. Sett miljøvariabelen `OPENAI_API_KEY` for **Production**-miljøet i Vercel sitt
   dashbord (eller med `vercel env add`) – **aldri** i en fil som committes.
   `OPENAI_MODEL` og `OPENAI_TIMEOUT_SECONDS` er valgfrie (har standardverdier i koden).
3. Sett **ikke** `OPENAI_API_KEY` på Preview-miljøet – da fungerer demomodus på alle
   forhåndsvisninger, mens normalmodus der gir en ren 503-feilmelding i stedet for å
   kunne bruke API-kreditter.
4. Sett et forbrukstak/budsjettgrense for API-nøkkelen direkte i OpenAI sin
   plattform, før lenken deles med andre – dette er det viktigste forsvaret mot at
   uvedkommende bruker opp kredittene, siden v1 ikke har innlogging.
5. `VITE_API_BASE_URL` skal **ikke** settes i produksjon – frontend velger automatisk
   en relativ adresse der.
