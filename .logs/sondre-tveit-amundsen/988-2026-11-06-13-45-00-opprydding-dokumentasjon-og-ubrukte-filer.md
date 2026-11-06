# Opprydding: dokumentasjonsfeil og ubrukte filer

## 2026-11-06 kl. 13:45 — Sondre Tveit Amundsen

### Oppgave
Oppfølging av IBE160-sluttkontrollen: en begrenset opprydding i prosjektet, fem konkrete punkter fra brukeren — (1) rett en uavsluttet Markdown-kodeblokk i `architecture.md` rundt linje 154, (2) rett referanser til en ikke-eksisterende `docs/`-mappe i prosjektdokumentene, (3) undersøk `product-brief.md`/`prd.md`/`process-log.md` for tidligere wireframe-arbeid og lag en tydelig merket rekonstruksjon hvis originalen ikke finnes, (4) fjern kun bekreftet ubrukte standardfiler fra Vite/React, (5) rett placeholder-beskrivelsen i `backend/pyproject.toml`. Eksplisitt ingen funksjonelle endringer, ingen endring av API-nøkler/.env/Vercel-konfig, ingen betalte API-kall, og ingen oppdiktet historikk.

### Plan
- `grep -n '```'` på `architecture.md` for å finne faktisk fence-paring, og fikset den uavsluttede ` ```text `-blokken fra linje 154.
- Verifiserte med `ls`/`test -e` at det ikke finnes noen `docs/`-mappe eller rot-`.env.example` i repoet, og at `frontend/.env.example`/`backend/.env.example` faktisk finnes — rettet project-structure-treet i `architecture.md` til å matche dette, med en forklarende setning.
- Søkte (`find`/`grep`) i `product-brief.md`, `prd.md`, `process-log.md`, `tilbakemelding-product-brief.md` og hele repoet etter wireframe/skisse/mockup-filer. Fant ingen original wireframe-fil, men fant detaljert beskrivelse av innholdet i `process-log.md` (08.10.2026) og i `tilbakemelding-product-brief.md` (linje 101).
- Skrev `wireframe-rekonstruksjon-2026-11-06.md` på repo-roten, eksplisitt merket som rekonstruksjon (ikke original), med kildesitater og enkle tekstbaserte skisser av nøyaktig de skjermbildene som er dokumentert: modusvalg, CV/annonse-innliming, status/feil, resultat (krav/styrker/gap/CV-forslag med sporbarhet), og redigerbart søknadsutkast.
- Kjørte `grep` for `hero.png`, `react.svg`, `vite.svg`, `icons.svg`, `favicon.svg` i `frontend/src`, `frontend/public` og `frontend/index.html` for å bekrefte faktisk bruk før noe ble slettet.
- Rettet placeholder-teksten i `backend/pyproject.toml`.
- Kjørte backend- og frontend-testene, samt en frontend-build, for å bekrefte at ingenting var brukket.

### Resultat
- **`architecture.md`** (endret): lukket den uavsluttede kodeblokken fra linje 154, og rettet project-structure-treet (avsnitt 5) som tidligere viste til en ikke-eksisterende `docs/`-mappe og rot-`.env.example`. Ny tekst viser korrekt at planleggingsdokumentene ligger på repo-roten og at `.env.example` finnes separat i `frontend/` og `backend/`.
- **`wireframe-rekonstruksjon-2026-11-06.md`** (ny fil, repo-rot): enkel tekstbasert wireframe, eksplisitt merket som en rekonstruksjon laget 06.11.2026 basert på `process-log.md` og `tilbakemelding-product-brief.md` — ikke en originalfil fra planleggingsfasen (den ble aldri lagret i repoet).
- **`frontend/src/assets/hero.png`, `react.svg`, `vite.svg`** (slettet med `git rm`): bekreftet null referanser i `src/`, `public/` eller `index.html`. Dette løser det åpne punktet fra `998-frontend-demomodus.md` (2026-11-05). `favicon.svg` er aktivt brukt (referert i `index.html`) og ble ikke rørt. `frontend/public/icons.svg` har også null treff, men er ikke en Vite/React-standardfil og faller utenfor denne oppgavens avgrensning — latt stå, se åpent punkt under.
- **`backend/pyproject.toml`** (endret): `description` rettet fra `"Add your description here"` til `"FastAPI-backend for Career Transition Assistant (IBE160-gruppeprosjekt G02)"`.
- Verifisering: `cd backend && uv run pytest` → 81/81 bestått. `cd frontend && npm test` → 23/23 bestått. `cd frontend && npm run build` → bygget uten feil (bekrefter at slettingen av de tre asset-filene ikke brøt noe).
- Ingen funksjonell kode er endret, ingen `.env`/API-nøkkel/Vercel-konfig er rørt, ingen ekte API-kall er gjort.
- Ingen av de fem endringene over er committet av meg — kun denne loggfila og `issues.md` committes nå, per brukerens eksplisitte instruks ("jeg gjør resten selv").

### Åpne punkter
- `frontend/public/icons.svg` har null funnet referanser i kildekoden (samme grep-metode som for de slettede filene), men er ikke en standard Vite/React-malfil og lå utenfor denne oppgavens avgrensning til «standardfiler fra Vite/React» — bør vurderes i en senere, bredere opprydding dersom den fortsatt er ubrukt.
- Øvrige, tidligere åpne punkter (sikkerhetsrisikoen med den ikke-tilbakekalte OpenAI-nøkkelen, KI-kvalitetsfunnene fra manuell-QA-runden, m.m.) er uendret, se `issues.md`.
