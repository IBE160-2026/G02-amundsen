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

## 2026-11-05 kl. 14:32 — Sondre Tveit Amundsen

### Oppgave
Brukeren gjennomførte sitt første ekte `POST /api/analyze`-kall mot OpenAI (200 OK, ingen oppdiktede kvalifikasjoner i søknadsutkastet), men fant ved manuell kvalitetssikring tre feilkoblinger: (1) en styrke (S5, om en bacheloroppgave om kundetilfredshet) var koblet til et krav om Power BI (JR5) som ikke er dokumentert i CV-en, (2) et kompetansegap (G3, om rapportering/presentasjon) var koblet til feil krav (JR4, kommunikasjonsevner), og (3) et CV-forslag (C5) var korrekt formulert som betinget, men `cv_excerpt` dokumenterte ikke Power BI. Oppgaven var å forbedre prompt og backend-validering slik at funn kobles riktig til krav, og tydelig skille dokumentert kompetanse / manglende kompetansedokumentasjon / betingede forslag – uten å endre API-responsformatet.

### Plan
- Analyserte de tre feilene som ett felles problem: et sitat kan være ordrett ekte (bestått av eksisterende `enforce_grounding`) uten at *koblingen* det brukes til (krav-ID, eller hvilken påstand det underbygger) er riktig. Eksisterende grunnlagskontroll fanget bare opp oppdiktede sitater, ikke feilkoblinger.
- Skrev om `backend/app/grounding.py`: la til en enkel, deterministisk nøkkelord-overlapp-heuristikk (`_shares_relevant_keyword`, med en liste over generiske fyllord som "erfaring"/"kompetanse" unntatt fra å telle som treff), og brukte den til å (a) luke `related_requirement_ids` for krav som ikke tematisk handler om samme sak som funnet, og (b) luke bort kildesitater som er ordrett ekte men irrelevante for funnets egen påstand.
- Innførte type-spesifikke regler for å skille de tre kategoriene tydelig innenfor eksisterende skjema (ingen nye felt): `Strength.source.cv_excerpt` er obligatorisk (dokumentert kompetanse); `CompetencyGap.source.cv_excerpt` settes alltid til `None` (manglende dokumentasjon per definisjon), `job_ad_excerpt` er obligatorisk; `CvSuggestion.source.job_ad_excerpt` er obligatorisk, `cv_excerpt` er valgfritt og fjernes hvis irrelevant (representerer et betinget forslag om noe som ikke er dokumentert).
- Oppdaterte `backend/app/prompts.py` med tre nye regler (6–8) som eksplisitt forbyr generiske krav-koblinger og instruerer modellen om riktig bruk av `cv_excerpt`/`job_ad_excerpt` per kategori.
- Skrev om `backend/tests/test_grounding.py` fullstendig, inkludert tre tester som speiler nøyaktig de rapporterte feilene (S5/JR5, G3/JR4, C5/Power BI), og justerte to eksisterende tester (`test_successful_analysis_returns_parsed_result` i `test_analysis_service.py`, og begge testene i `test_llm_client.py`) som sluttet å stemme med ny, strengere oppførsel.
- Oppdaget og fikset en reell test-isolasjonsfeil underveis: `test_llm_client.py` leste faktisk den virkelige `backend/.env`-filen (som nå finnes med brukerens ekte nøkkel, opprettet mellom øktene) i stedet for å være uavhengig av miljøet – fikset ved å mocke `get_settings` direkte med `Settings(..., _env_file=None)` i stedet for å sette/fjerne miljøvariabler.

### Resultat
Endrede filer:
- `backend/app/grounding.py` – fullstendig omskrevet med nøkkelord-relevans-kontroll og type-spesifikke regler (se Plan).
- `backend/app/prompts.py` – tre nye regler (6–8) i systemprompten.
- `backend/tests/test_grounding.py` – omskrevet, inkludert tre tester som speiler de konkrete rapporterte feilene.
- `backend/tests/test_analysis_service.py`, `backend/tests/test_llm_client.py` – justerte to fixtures/tester til ny, strengere oppførsel (ikke funksjonelle feil i produksjonskoden, bare utdaterte testfixtures).

Ingen endring av `AnalysisResult`/`SourceReference`/API-responsformatet – kun validerings- og promptlogikk.

Testresultat: `uv run pytest -v` → **59 passed, 0 failed** (opp fra 58). Ingen ekte eller betalte OpenAI-kall ble gjort – alt mockes som før.

Bekreftet at `backend/.env` (med brukerens ekte nøkkel) fortsatt er korrekt dekket av `.gitignore` (`git check-ignore -v`), at den ikke vises i `git status`, og at nøkkelen ikke er gjengitt eller logget noe sted i denne økten.

Ingen git-commit/push er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Den nye nøkkelord-relevans-heuristikken er en tilnærming, ikke semantisk forståelse: den kan i prinsippet avvise en riktig kobling formulert med helt andre ord, eller slippe gjennom en feilkobling som tilfeldigvis deler et vanlig ord – dokumentert som en kjent begrensning i `grounding.py`.
- Den konkrete, ekte OpenAI-analysen som avdekket de tre feilene er ikke lagret/retestet mot den nye koden (bruker har ikke gjenkjørt det samme virkelige kallet) – neste reelle test bør kontrollere at de samme tre feilkoblingene faktisk forsvinner i praksis, ikke bare i de syntetiske testene.
- Øvrige åpne punkter er uendret, se over og `issues.md`.
