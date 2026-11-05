# Frontend: normalmodus

## 2026-11-05 kl. 15:16 — Sondre Tveit Amundsen

### Oppgave
Implementere normalmodus i React-frontend, nå som backend-normalmodus er ferdig implementert, testet med ekte OpenAI-kall og pushet til GitHub (commit `43c863d`, 66/66 backend-tester). Brukeren skal kunne aktivere normalmodus i modusvalget, lime inn egen CV og stillingsannonse, koble til `POST /api/analyze`, gjenbruke eksisterende resultatkomponenter fra demomodus, se lastestatus og forståelige feilmeldinger (manglende input, API-feil, timeout), fortsatt kunne redigere søknadsutkastet, og demomodus skal fortsatt fungere uten API-nøkkel. Ingen API-nøkkel eller sensitiv konfigurasjon i frontend. Ingen ekte OpenAI-kall i denne økten.

### Plan
- Leste eksisterende frontend-kode (`App.jsx`, alle komponenter, `analyzeApi.js`/-test) og relevante krav i `prd.md`, `architecture.md`, `epics-and-stories.md`, `CLAUDE.md` på nytt, samt backendens oppdaterte `models.py` (for `MAX_CV_LENGTH`/`MAX_JOB_AD_LENGTH`-grensene).
- Omstrukturerte `analyzeApi.js` til en delt `requestJson()`-hjelpefunksjon med en `describeError()` som håndterer BÅDE FastAPI sin valideringsfeil-liste (422, `detail` er en array) og backendens egne tekstmeldinger (503/504/502, `detail` er en streng) – lagt til `fetchNormalAnalysis()` som POST-er `{cv_text, job_ad_text}` til `/api/analyze`.
- La til `frontend/src/constants.js` med `MAX_CV_LENGTH`/`MAX_JOB_AD_LENGTH`, bevisst duplisert fra backend sine grenser (kan ikke importeres direkte fra Python), med kommentar om at de må holdes i synk manuelt.
- Aktiverte normalmodus i `ModeSelector.jsx` (fjernet `disabled`/`is-disabled`).
- Bygde ny `NormalModeForm.jsx`: to tekstfelt (CV, stillingsannonse) med klientside-validering (tomt/kun mellomrom → tydelig feilmelding, ingen API-kall) før `onSubmit` kalles.
- Omstrukturerte `App.jsx`: innførte `pendingRequest`-state (`{kind:'demo'}` eller `{kind:'normal', cvText, jobAdText}`) slik at samme `useEffect` kan kjøre riktig API-funksjon for begge moduser, og "Prøv igjen" kan gjenta nøyaktig samme forespørsel uten at brukeren må skrive inn teksten på nytt. Modusbytte nullstiller status/resultat. Resultatkomponentene (`InputPreview`, `JobRequirementsList`, `TraceableItemList`, `ApplicationDraftEditor`) gjenbrukes helt uendret for begge moduser, siden `AnalyzeResponse`-formatet er identisk.
- La til CSS for det nye formet (`.normal-mode-form`, `.form-field`) i `App.css`, konsistent med eksisterende designsystem.
- Oppdaterte `App.test.jsx` (fjernet den utdaterte "normalmodus er disabled"-testen, la til 6 nye tester for normalmodus-flyten) og `analyzeApi.test.js` (la til tester for `fetchNormalAnalysis`, inkl. 422-parsing). Opprettet `NormalModeForm.test.jsx` med isolerte komponenttester.
- Kjørte ESLint og `vite build` – begge grønne.
- Gjorde en trygg, levende integrasjonsverifisering: startet backend (med brukerens ekte `.env` til stede, men sendte KUN forespørsler som stoppes av Pydantic-validering – tom `cv_text` → 422 – FØR noe LLM-kall), bekreftet CORS-preflight for `POST /api/analyze`, og bekreftet at alle nye frontend-moduler transformeres uten feil via Vite. Ingen ekte OpenAI-kall ble gjort. Begge serverne ble stoppet igjen etterpå.

### Resultat
Endrede filer:
- `frontend/src/api/analyzeApi.js` – ny `fetchNormalAnalysis()`, delt `requestJson()`/`describeError()`.
- `frontend/src/App.jsx` – `pendingRequest`-basert orkestrering for begge moduser, modusbytte nullstiller tilstand, betinget footer-tekst.
- `frontend/src/components/ModeSelector.jsx` – normalmodus aktivert.
- `frontend/src/App.css` – nye stiler for `.normal-mode-form`/`.form-field`.

Nye filer:
- `frontend/src/components/NormalModeForm.jsx`, `NormalModeForm.test.jsx`.
- `frontend/src/constants.js`.

Oppdaterte tester:
- `frontend/src/App.test.jsx`, `frontend/src/api/analyzeApi.test.js`.

Testresultat: `npx vitest run` → **21 av 21 bestått** (opp fra 8). `npx eslint .` → ingen feil. `npx vite build` → bygget uten feil (`dist/` fjernet igjen etterpå).

Backend er uendret (ingen filer i `backend/` er rørt denne økten) – demomodus og normalmodus i backend fungerer som før (ikke re-testet i detalj, siden det ble gjort og bekreftet i forrige økt med 66/66 bestått).

Ingen ekte OpenAI-kall ble gjort. Ingen git-commit/push er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Ekte, visuell klikk-gjennom-test av normalmodus i en nettleser er ikke gjort (ingen browser-tilgang tilgjengelig denne økten – brukeren avslo Claude-in-Chrome-utvidelsen i en tidligere økt i denne samtalen). Automatiserte tester (21 stk) dekker brukerflyten i jsdom; brukeren bør selv gjøre en rask visuell sjekk i nettleseren, se instruksjonene i sluttoppsummeringen.
- Det er ikke gjort et ekte `POST /api/analyze`-kall fra frontend mot en reell OpenAI-respons (bevisst, per instruks) – kun mot en validerings-422 for å bekrefte ruting/CORS. Den fulle, ekte happy-path-flyten (frontend → backend → OpenAI → visning av resultat) er derfor ikke sluttverifisert visuelt, bare gjennom mocket testdekning + backendens egne, tidligere ekte tester.
- Øvrige åpne punkter er uendret, se `issues.md`.
