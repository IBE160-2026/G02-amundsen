# Backend: Pydantic-modeller og demomodus

## 2026-11-05 kl. 12:02 — Sondre Tveit Amundsen

### Oppgave
Starte implementeringen av Career Transition Assistant-backenden: Pydantic-responsmodeller for analyseresultatet og et fungerende FastAPI-endepunkt for demomodus, innenfor v1-scope (ingen ekstern språkmodell, API-nøkkel, database eller frontend). Demomodus skal bruke en fiktiv CV, en fiktiv stillingsannonse og et fast eksempelresultat, med samme struktur som normal modus senere skal bruke.

### Plan
- Leste `prd.md`, `architecture.md`, `epics-and-stories.md` og `CLAUDE.md` for krav og struktur.
- Designet Pydantic-modeller (`AnalyzeResponse` → `AnalysisResult`) som dekker: sentrale krav fra stillingsannonsen, relevante styrker, kompetansegap, CV-forslag og søknadsutkast, samt en `SourceReference` for sporbarhet til CV/stillingsannonse (FR3–FR8, NFR8).
- La demodata (fiktiv CV, fiktiv stillingsannonse, fast eksempelresultat) i egne prosjektfiler under `test-data/`, slik `architecture.md` punkt 5 og "Demo Mode" beskriver, i stedet for å hardkode dem i Python.
- Bygde `app/demo_data.py` som leser og validerer disse filene til en `AnalyzeResponse`, og la til `GET /api/analyze/demo` i `app/main.py` (beholdt eksisterende `GET /`).
- La til `pytest` og `httpx` som dev-dependencies via `uv add --dev`, og skrev automatiserte tester for modeller, demo-datalasting og HTTP-endepunktene.

### Resultat
Endrede/nye filer:
- `backend/app/models.py` (ny) — Pydantic-modeller: `SourceReference`, `JobRequirement`, `Strength`, `CompetencyGap`, `CvSuggestion`, `AnalysisResult`, `AnalyzeResponse`.
- `backend/app/demo_data.py` (ny) — laster og cacher demodata fra `test-data/`.
- `backend/app/main.py` (endret) — la til `GET /api/analyze/demo`, beholdt `GET /`.
- `backend/app/__init__.py` (ny, tom) — gjør `app` til en eksplisitt pakke.
- `backend/tests/__init__.py`, `backend/tests/test_main.py`, `backend/tests/test_models.py`, `backend/tests/test_demo_data.py` (nye).
- `test-data/demo-cv.txt`, `test-data/demo-job-ad.txt`, `test-data/demo-result.json` (nye) — fiktiv CV ("Kari Nordmann"), fiktiv stillingsannonse ("Fjord Digital AS") og et fast eksempelresultat som matcher `AnalysisResult`.
- `backend/pyproject.toml`, `backend/uv.lock` (endret) — la til `pytest` og `httpx` i `[dependency-groups].dev`.

Testresultat: `uv run pytest -v` → **20 passed** (0 failed). Dekker blant annet: `GET /` fungerer som før, `GET /api/analyze/demo` returnerer 200 med `mode: "demo"`, resultatet har alle påkrevde seksjoner (krav, styrker, gap, forslag, søknadsutkast), styrker/gap/forslag er sporbare til CV- og annonseutdrag, krav-IDer referert fra styrker/gap faktisk finnes, og responsen er stabil mellom kall. Pydantic-modellene er også testet direkte (gyldig/ugyldig prioritet, påkrevde felt, `SourceReference` uten `cv_excerpt` for gap).

Manuell smoke-test: startet `uv run uvicorn app.main:app` på port 8001, bekreftet `GET /`, `GET /api/analyze/demo` og `GET /docs` med `curl`, og stoppet serveren igjen etterpå.

Ingen git-commit eller push er gjort (på brukerens eksplisitte instruks) — kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- `backend/src/backend/__init__.py` er en ubrukt rest fra `uv init` (inneholder bare en `main()`-funksjon som ikke kalles av applikasjonen). Vurder å fjerne den i en senere opprydding.
- `pytest` ga en `StarletteDeprecationWarning` om at `httpx` sammen med `starlette.testclient` er "deprecated" i favør av en pakke kalt `httpx2` i denne miljøkonfigurasjonen. Testene kjører og passerer likevel; vurder å bytte testklient-avhengighet når/if `httpx2` blir et reelt, stabilt alternativ.
- Neste steg i tråd med `process-log.md` sitt "Neste steg"-punkt: bygge React-grensesnittet, koble frontend mot `/api/analyze/demo`, og deretter velge språkmodell/API for normal modus (ikke del av denne økten).
