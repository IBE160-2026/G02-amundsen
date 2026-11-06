# G02 — Gruppe 222

Gruppeprosjekt i **IBE160 Programmering med KI** ved Høgskolen i Molde, høsten 2026 (15 studiepoeng).

Repoet inneholder gruppens applikasjon **Career Transition Assistant** og dokumentasjon av utvikling, testing og kvalitetssikring med KI.

**Publisert applikasjon:** **https://g02-amundsen.vercel.app/** – demomodus fungerer direkte, uten noen API-nøkkel (se avsnittet «Publisering på Vercel» under for status på normalmodus i produksjon).

## Medlemmer

- Sondre Tveit Amundsen

## Dokumentasjon

| Dokument | Innhold |
|---|---|
| [`product-brief.md`](product-brief.md) | Opprinnelig produktidé og avgrensning |
| [`tilbakemelding-product-brief.md`](tilbakemelding-product-brief.md) | Faglærers tilbakemelding på product brief, inkl. sensorveiledningens kriterier |
| [`prd.md`](prd.md) | Funksjonelle/ikke-funksjonelle krav og akseptansekriterier |
| [`architecture.md`](architecture.md) | Teknologivalg, systemarkitektur og publiseringsoppsett |
| [`epics-and-stories.md`](epics-and-stories.md) | Epics og brukerhistorier |
| [`process-log.md`](process-log.md) | Løpende prosess- og KI-logg: beslutninger, feil som ble funnet, hvordan de ble rettet, og testresultater |
| [`backend/test-data/manual-qa/`](backend/test-data/manual-qa/) | Fire fiktive testsett (CV + stillingsannonse) med forhåndsdefinerte forventede resultater, brukt til manuell kvalitetssikring av normalmodus mot ekte OpenAI-svar – se `TESTPLAN.md` i samme mappe for metodikken |
| [`.logs/sondre-tveit-amundsen/issues.md`](.logs/sondre-tveit-amundsen/issues.md) | Samlet, løpende liste over åpne punkter og kjente begrensninger |
| [`.logs/sondre-tveit-amundsen/`](.logs/sondre-tveit-amundsen/) | Detaljerte sesjonslogger (oppgave, plan, resultat) fra arbeidet med Claude Code |

## Forutsetninger

For å kjøre applikasjonen lokalt på en ren maskin må følgende være installert:

- **Python 3.12 eller nyere** – `backend/.python-version` og `backend/pyproject.toml` krever `>=3.12`.
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** – Pythons pakke- og prosjektverktøy, brukt til alt i `backend/` (installer- og oppstartskommandoer, lockfile).
- **Node.js** `^20.19.0` eller `>=22.12.0`, med **npm** – krevd av Vite 8 (se `frontend/package.json`).

Utviklet og testet med Python 3.12, uv 0.12.7, Node.js v26.7.0 og npm 11.19.0. Andre versjoner innenfor kravene over bør også fungere.

Ingen database, Docker eller andre eksterne tjenester er nødvendig. **Demomodus krever ingen API-nøkkel og ingen betalt tjeneste** – se punkt 3 under.

## Kjøre applikasjonen lokalt

```bash
git clone https://github.com/IBE160-2026/G02-amundsen.git
cd G02-amundsen
```

Applikasjonen består av en React/Vite-frontend (`frontend/`) og en FastAPI-backend (`backend/`), som under lokal utvikling kjøres som to separate prosesser.

### 1. Start backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Backenden kjører da på `http://127.0.0.1:8000`. `GET /api/analyze/demo` returnerer demoresultatet uten API-nøkkel, og `http://127.0.0.1:8000/docs` viser API-dokumentasjonen.

**For normalmodus** (`POST /api/analyze`) med egen OpenAI-nøkkel: kopier `backend/.env.example` til `backend/.env` og fyll inn din egen `OPENAI_API_KEY`. Denne filen skal **aldri** committes (den er dekket av `.gitignore`). Uten en nøkkel svarer `/api/analyze` med en tydelig feilmelding (HTTP 503) – demomodus fungerer uendret uansett.

### 2. Start frontend

I et nytt terminalvindu:

```bash
cd frontend
npm install
npm run dev
```

Frontenden kjører da på `http://localhost:5173` og er satt opp til å kalle backenden på `http://127.0.0.1:8000` (se `frontend/.env.example`). Skal backenden kjøre på en annen adresse, kopier `.env.example` til `.env` i `frontend/` og endre `VITE_API_BASE_URL`.

Backenden tillater CORS-forespørsler fra `http://localhost:5173` og `http://127.0.0.1:5173` i lokal utvikling, slik at frontend og backend kan kjøre som separate prosesser uten CORS-feil.

### 3. Bruk demomodus (ingen API-nøkkel, ingen kostnad)

Åpne `http://localhost:5173` i nettleseren, velg **Demomodus** og trykk **«Kjør demoanalyse»**. Dette er hvordan sensor kan teste hele hovedflyten uten egen API-nøkkel eller betalt tilgang til en språkmodell (jf. PRD NFR6). Resultatet viser en fast, fiktiv CV og stillingsannonse, sentrale krav, relevante styrker, kompetansegap, CV-forslag med sporbarhet til CV og stillingsannonse, og et redigerbart søknadsutkast.

### 4. Bruk normalmodus med egen OpenAI API-nøkkel

Når `backend/.env` har en gyldig `OPENAI_API_KEY` (se punkt 1): velg **Normalmodus** i grensesnittet, lim inn en egen CV og stillingsannonse, og trykk **«Kjør analyse»**. Resultatet har samme struktur som demomodus, men innholdet er generert av en ekte språkmodell.

Normalmodus kan også kalles direkte mot backenden, uten frontend:

```bash
curl -X POST http://127.0.0.1:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"cv_text": "...", "job_ad_text": "..."}'
```

Du kan også bruke `http://127.0.0.1:8000/docs` ("Try it out" på `POST /api/analyze`). Kildesitater i svaret er kontrollert mot CV-en/stillingsannonsen som faktisk ble sendt inn (se `backend/app/grounding.py`).

### Kjøre automatiserte tester

```bash
cd backend && uv run pytest

cd frontend && npm test
```

## Publisering på Vercel

IBE160 bruker Vercel som offisiell publiseringsløsning. Applikasjonen er publisert på
**https://g02-amundsen.vercel.app/**, med én **Vercel Services**-konfigurasjon i
[`vercel.json`](vercel.json) i repo-roten: frontend (`frontend/`) og backend
(`backend/`) kjører som to tjenester i **ett** Vercel-prosjekt, på samme domene – alt
under `/api/*` rutes til FastAPI-backenden, resten rutes til React/Vite-frontenden. Se
`architecture.md` avsnitt 10 for begrunnelse og alternativ løsning.

### Status i produksjon

- **Demomodus fungerer offentlig** på den publiserte siden, uten API-nøkkel –
  bekreftet manuelt i nettleseren.
- **Normalmodus er ikke tilgjengelig i den nåværende produksjonskonfigurasjonen.**
  Normalmodus **ble** testet med ekte OpenAI-analyse direkte i produksjon
  06.11.2026, under kontrollerte forhold (redusert forbrukstak og hard grense satt
  hos OpenAI først) – analysen fungerte, og resultatet ble vist korrekt i
  nettleseren (se `process-log.md`). `OPENAI_API_KEY` ble deretter **bevisst fjernet**
  fra Vercel igjen etter testen, for å unngå at en offentlig, uinnlogget side kan
  brukes av uvedkommende til å tømme forhåndsbetalte OpenAI-kreditter over tid. Et
  besøk i normalmodus på den publiserte siden gir derfor nå en ren 503-feilmelding
  ("ingen gyldig API-nøkkel"), ikke en krasj.
- For å teste normalmodus med ekte KI-analyse akkurat nå: kjør applikasjonen **lokalt**
  med din egen `OPENAI_API_KEY` (se "Kjøre applikasjonen lokalt" over).
- **Sikkerhetspunkt, nå løst:** nøkkelen som ble brukt i produksjonstesten er bekreftet
  (06.11.2026, manuell kontroll hos OpenAI) ikke lenger aktiv – kun en nyere, lokal
  nøkkel står som Active. Normalmodus forblir likevel avslått på den offentlige,
  uinnloggede Vercel-siden: en eventuell ny nøkkel skal ikke publiseres der uten at
  tilgangskontroll/innlogging er på plass først, siden v1 ikke har noe som hindrer
  uvedkommende fra å bruke opp forhåndsbetalte kreditter. Se
  [`.logs/sondre-tveit-amundsen/issues.md`](.logs/sondre-tveit-amundsen/issues.md).

### Manuelt i Vercel (for å aktivere normalmodus i produksjon på nytt)

1. **Sett opp tilgangskontroll/innlogging før en ny nøkkel publiseres** (se
   sikkerhetspunktet over) – den tidligere testnøkkelen er bekreftet ikke lenger
   aktiv, men det løser ikke det grunnleggende problemet med en offentlig,
   uinnlogget side.
2. Sett i tillegg et forbrukstak/budsjettgrense for den nye nøkkelen direkte i
   OpenAI sin plattform – et ekstra forsvar mot at uvedkommende bruker opp
   kredittene.
3. Sett deretter miljøvariabelen `OPENAI_API_KEY` for **Production**-miljøet i Vercel
   sitt dashbord (eller med `vercel env add`) – **aldri** i en fil som committes.
   `OPENAI_MODEL` og `OPENAI_TIMEOUT_SECONDS` er valgfrie (har standardverdier i koden).
4. Sett **ikke** `OPENAI_API_KEY` på Preview-miljøet – da fortsetter demomodus å
   fungere på alle forhåndsvisninger, mens normalmodus der gir en ren 503-feilmelding
   i stedet for å kunne bruke API-kreditter.
5. `VITE_API_BASE_URL` skal **ikke** settes i produksjon – frontend velger automatisk
   en relativ adresse der.
