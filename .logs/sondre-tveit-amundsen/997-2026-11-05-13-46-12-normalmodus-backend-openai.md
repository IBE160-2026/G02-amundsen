# Normalmodus: OpenAI-integrasjon i backend

## 2026-11-05 kl. 13:46 — Sondre Tveit Amundsen

### Oppgave
Forberede og deretter implementere normalmodus i backend med en ekte språkmodell (OpenAI, `gpt-5.4-mini`), som et tillegg til den fungerende demomodusen (se [[999-2026-11-05-12-02-03-backend-pydantic-og-demomodus]], [[998-2026-11-05-12-32-31-frontend-demomodus]]). Normalmodus skal bruke strukturert JSON-output, sporbare kildehenvisninger kontrollert mot originalteksten, sikker API-nøkkel-håndtering, ingen oppdiktede kvalifikasjoner, bevart demomodus, og automatiserte tester uten ekte API-kall. Frontend for normalmodus skal ikke implementeres i denne omgangen – kun backend skal kvalitetssikres først.

### Plan
- Leste `prd.md`, `architecture.md`, `epics-and-stories.md`, `CLAUDE.md` og eksisterende backend-kode på nytt, og la først fram en ren plan (ingen kodeendring) over filer, anbefalt løsning og tekniske utfordringer – brukeren godkjente planen før implementering startet.
- Verifiserte eksperimentelt, uten nettverkskall, at eksisterende `AnalysisResult` (fra forrige økt) allerede er kompatibel med OpenAI sin strukturerte output i strict-modus (riktig `required`, `additionalProperties: false`, nullable felt som `anyOf [string, null]`, og at den norske literal-verdien "ønskelig" bevares korrekt) – ingen endring av eksisterende modeller var nødvendig for selve skjemaet.
- Installerte `openai` (3.46.0) og `pydantic-settings` (2.16.2) via `uv add` i `backend/`.
- Bygde et nytt lag rundt eksisterende kode: `config.py` (innstillinger fra miljøvariabler/`.env`), `llm_client.py` (lager OpenAI-klienten lazy, `max_retries=0`), `prompts.py` (system-/brukerprompt med strenge regler mot oppdiktet informasjon og krav om ordrette sitater), `grounding.py` (normaliserer mellomrom/store-små bokstaver og luker bort funn hvis kildesitat ikke faktisk finnes i CV/annonse), `analysis_service.py` (orkestrerer kall + egne feiltyper), og la til `POST /api/analyze` i `main.py` (ved siden av det uendrede `GET /api/analyze/demo`).
- La til `AnalyzeRequest` i `models.py` med lengdegrenser (`MAX_CV_LENGTH=20000`, `MAX_JOB_AD_LENGTH=10000`) og en valideringsregel mot tomt/kun-mellomrom input.
- Utvidet CORS i `main.py` til å tillate `POST` i tillegg til `GET`.
- Kontrollerte at `.gitignore` på rot-nivå allerede dekker `backend/.env` (med `git check-ignore -v`) – ingen endring var nødvendig der.
- La til `backend/.env.example` (`OPENAI_API_KEY`, `OPENAI_MODEL=gpt-5.4-mini`, `OPENAI_TIMEOUT_SECONDS=30`), og oppdaterte `architecture.md` (avsnitt om modellvalg og miljøvariabler, som tidligere brukte det generiske `LLM_API_KEY`-eksempelet) samt `README.md` og `backend/README.md` med oppstarts- og testinstruksjoner for normalmodus.
- Skrev automatiserte tester som mocker OpenAI-klienten/servicelaget på riktig sted, uten noen ekte eller betalte API-kall.

### Resultat
Nye filer:
- `backend/app/config.py`, `llm_client.py`, `prompts.py`, `grounding.py`, `analysis_service.py`.
- `backend/.env.example`.
- `backend/tests/test_grounding.py`, `test_analysis_service.py`, `test_analyze_endpoint.py`, `test_llm_client.py`.

Endrede filer:
- `backend/app/models.py` – ny `AnalyzeRequest` med lengdegrenser og tomt-felt-validering.
- `backend/app/main.py` – nytt `POST /api/analyze` (normalmodus), CORS utvidet med `POST`. `GET /api/analyze/demo` og `GET /` er uendret.
- `backend/pyproject.toml`, `backend/uv.lock` – la til `openai` og `pydantic-settings` (pluss `python-dotenv` transitivt).
- `backend/tests/test_models.py` – nye tester for `AnalyzeRequest`.
- `architecture.md` – oppdatert modellvalg (OpenAI/`gpt-5.4-mini`) og miljøvariabel-eksempel/plassering (`backend/.env.example` i stedet for generisk rot-`LLM_API_KEY`).
- `README.md`, `backend/README.md` – lagt til instruksjoner for å sette opp og teste normalmodus direkte mot backend (curl/`\docs`).

Testresultat: `uv run pytest -v` → **58 passed, 0 failed** (opp fra 20 ved starten av økten). Ingen av testene gjør ekte eller betalte API-kall – OpenAI-klienten og `run_normal_mode_analysis` mockes med `unittest.mock`/`monkeypatch`. Dekker blant annet: manglende/tomt/for langt input (422), manglende/ugyldig API-nøkkel (503), tidsavbrudd (504), API-/svarfeil (502), at hemmelige/interne feildetaljer ikke lekkes i HTTP-responsen, at grunnlagskontrollen normaliserer mellomrom/store-små bokstaver korrekt, og at den faktisk luker bort oppdiktede kildesitater fra både tjenestelaget og hele endepunktflyten.

Manuell smoke-test: startet backend på port 8002 og bekreftet `GET /`, `GET /api/analyze/demo`, `POST /api/analyze` uten nøkkel (503 med forståelig norsk feilmelding) og CORS-preflight for `POST` – alt som forventet. Serveren ble stoppet igjen.

Som en sidegevinst forsvant den tidligere loggede `httpx2`-deprecation-advarselen fra Starlette (se `issues.md`), siden `openai`-pakken trekker inn `httpx2` som transitiv avhengighet og Starlette nå ser ut til å velge den automatisk.

Ingen reell API-nøkkel ble opprettet, og ingen `backend/.env`-fil ble laget (kontrollert med `test -f`) – kun `.env.example`. Ingen git-commit/push av kodeendringene er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Frontend har ikke støtte for normalmodus ennå (bevisst utelatt denne økten) – normalmodus kan foreløpig bare testes direkte mot backend (curl eller `/docs`), se `README.md`.
- Normalmodus er ikke testet mot en ekte, betalt OpenAI-nøkkel – dette gjør brukeren manuelt senere (se README for fremgangsmåte når nøkkelen er klar).
- Grunnlagskontrollen (`grounding.py`) kontrollerer kun at kildesitater faktisk finnes i input (luker bort oppdiktede sitater), ikke at selve *tolkningen* av et ekte sitat er riktig – dette er en kjent og bevisst begrensning, ikke en feil.
- `job_requirements` og `application_draft` har ingen egen sporbarhets-/grunnlagskontroll i skjemaet (kun styrker, kompetansegap og CV-forslag kontrolleres), siden `JobRequirement` ikke har et `source`-felt – dette er uendret fra forrige økts skjemadesign.
- Fra tidligere økter: ubrukt `backend/src/backend/__init__.py`, ekte browser-klikk-test av frontend er ikke gjort, og en moderate `minimatch`-sårbarhet i frontendens eslint-avhengighetskjede står fortsatt åpen.
