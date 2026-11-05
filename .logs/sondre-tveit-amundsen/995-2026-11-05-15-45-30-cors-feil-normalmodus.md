# CORS-feil i normalmodus

## 2026-11-05 kl. 15:45 — Sondre Tveit Amundsen

### Oppgave
Brukeren fant en CORS-feil under manuell testing av normalmodus: backend kjørte på `http://127.0.0.1:8001` og frontend på `http://localhost:5174`, og `fetch()`-kall fra frontend til `GET /api/analyze/demo` ble blokkert av nettleseren med "No 'Access-Control-Allow-Origin' header is present", selv om samme URL fungerte ved direkte navigasjon i adressefeltet. Oppgaven var å undersøke eksisterende CORS-konfigurasjon, tillate localhost/127.0.0.1 på port 5173 OG 5174 (ikke åpne for alle domener), legge til automatiserte tester for tillatte/ukjente origins, kjøre backend-testene, og oppdatere `process-log.md` med feilen/årsaken/løsningen – uten commit/push og uten ekte OpenAI-kall.

### Plan
- Leste `backend/app/main.py` sin eksisterende CORS-middleware: `allow_origins` inneholdt kun `http://localhost:5173` og `http://127.0.0.1:5173`.
- Bekreftet årsaken empirisk (ikke gjettet) med `TestClient`: et `GET`-kall fra et ikke-tillatt origin besvares av Starlette med HTTP 200, men UTEN `Access-Control-Allow-Origin`-headeren (derav at direkte navigasjon fungerer, men `fetch()` blokkeres av nettleseren); en CORS-preflight (`OPTIONS`) fra et ikke-tillatt origin avvises derimot med HTTP 400 "Disallowed CORS origin".
- Konkluderte at årsaken er at Vite automatisk velger en annen port (5174) når 5173 allerede er i bruk, og at backendens CORS-liste ikke dekket denne alternative porten.
- La til nøyaktig de to nye origin-oppføringene (`http://localhost:5174`, `http://127.0.0.1:5174`) i `allow_origins` – ingen andre endringer i CORS-konfigurasjonen, og ingen bruk av `["*"]`.
- Skrev `backend/tests/test_cors.py` med tester (parametrisert over alle fire tillatte origins) for: CORS-header på vanlig `GET`, CORS-header og tillatt metode på `OPTIONS`-preflight, at et ukjent origin (`http://evil.example.com`) IKKE får CORS-header på `GET` og får 400 på preflight, og en regresjonstest som kontrollerer at `allow_origins` faktisk er en konkret liste (ikke et jokertegn).
- Oppdaterte `process-log.md` med en ny, egen seksjon om feilen, årsaken og løsningen.

### Resultat
Endrede filer:
- `backend/app/main.py` – `allow_origins` utvidet med `http://localhost:5174` og `http://127.0.0.1:5174`.
- `process-log.md` – ny seksjon «CORS-feil under manuell testing av normalmodus».

Nye filer:
- `backend/tests/test_cors.py` – 11 nye tester.

Testresultat: `uv run pytest -q` → **77 passed, 0 failed** (opp fra 66). Ingen ekte OpenAI-kall ble gjort.

Ingen git-commit/push av kodeendringene er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
Ingen nye. Øvrige åpne punkter er uendret, se `issues.md`.

## 2026-11-05 kl. 15:54 — Sondre Tveit Amundsen

### Oppgave
Brukeren gjennomførte en vellykket, fullstendig manuell ende-til-ende-test i nettleseren (frontend `http://localhost:5174`, backend `http://127.0.0.1:8001`) etter CORS-fiksen: demomodus fungerte, normalmodus fikk et ekte OpenAI-svar med relevante, kildehenviste styrker, SQL og Power BI korrekt som kompetansegap, relevante CV-forslag, og et faktabasert søknadsutkast (uten oppdiktede kvalifikasjoner) – med den mindre observasjonen at utkastet er noe generelt. Oppgaven var rent dokumentasjon: oppdatere `process-log.md` med testen, resultatene og en kort kritisk vurdering, og registrere gjenværende begrensninger – ingen kodeendringer, ingen nye API-kall.

### Plan
- Leste slutten av `process-log.md` (CORS-seksjonen fra samme dag) for å finne riktig sted å fortsette.
- Skrev en ny, egen seksjon «Vellykket manuell ende-til-ende-test i nettleseren» med testflyt/resultater, en kort kritisk vurdering (bekrefter hele kjeden frontend→CORS→backend→OpenAI→grunnlagskontroll→visning fungerer i praksis; den generelle søknadsutkast-formuleringen er et forbedringspunkt, ikke en korrekthetsfeil; testingen dekker kun ett testsett), og en liste over fire gjenværende, kjente begrensninger.
- Kontrollerte med `git status` at ingen applikasjonskode ble rørt denne økten – kun `process-log.md`.

### Resultat
- `process-log.md` (endret) – ny seksjon lagt til, ingen eksisterende innhold fjernet.
- Ingen kode- eller testfiler endret. Ingen nye (ekte eller mockede) API-kall ble gjort av Claude Code i denne gjennomgangen.
- Ingen git-commit/push er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Søknadsutkastet oppleves som noe generelt – mulig forbedringspunkt (språklig kvalitet), ikke en korrekthetsfeil.
- Testingen er så langt gjort med ett testsett (én fiktiv CV/stillingsannonse) – bredere testing mot flere, varierte CV-er/stillinger gjenstår.
- Øvrige åpne punkter (inkl. den aksepterte `related_requirement_ids`-begrensningen) er uendret, se `issues.md`.
