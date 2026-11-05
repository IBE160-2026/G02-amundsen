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

## 2026-11-05 kl. 14:50 — Sondre Tveit Amundsen

### Oppgave
Brukeren gjennomførte et nytt ekte `POST /api/analyze`-kall etter forrige fiks: Power BI-feilene var borte, men manuell kvalitetssikring fant to NYE problemer: (1) et korrekt SQL-kompetansegap (SQL er fortsatt et sentralt, udokumentert krav) forsvant helt, og (2) styrke S4 (kundeservice/opplæring av nyansatte) fikk `related_requirement_ids=[]` selv om den kan være relevant for et krav om kommunikasjonsevner. Brukeren konkluderte at forrige nøkkelordkontroll var for streng, og ba om: (1) en faktisk undersøkelse (ikke gjetting) av om SQL-gapet ble utelatt av modellen eller fjernet av `grounding.py`, (2) en vurdering av hvordan vi kan beholde semantisk relevante koblinger uten å godta åpenbart feilaktige (bacheloroppgave→Power BI), (3) en forenkling/begrensning av heuristikken i stedet for et mer komplisert regelverk, samtidig som (4) literal sitatkontroll og (5) eksisterende API-format/demomodus skulle bevares.

### Plan
- Undersøkte årsaken empirisk (ikke gjettet): kjørte `_shares_relevant_keyword`/`_significant_words` direkte med representativ SQL-tekst, og bekreftet at ordet "sql" (3 bokstaver) ble utelukket av en minstelengde på 4 i BÅDE gap-beskrivelsen og kravsitatet – dermed null delt nøkkelord, og gapet ble (under forrige kode) garantert fjernet av `_clean_gap`, uavhengig av hva modellen egentlig svarte. Siden selve rå-svaret fra modellen aldri logges (bevisst, for å unngå lagring av CV-/annonseinnhold), kan jeg ikke bekrefte 100 % at modellen *også* leverte gapet riktig i den spesifikke historiske sesjonen – men jeg har bevist at koden uansett ville slettet det. Dette er forklart ærlig i rapporten til brukeren, ikke fremstilt som en absolutt sikker konklusjon om den ene, konkrete hendelsen.
- Besluttet en forenkling i stedet for en mer komplisert regel: nøkkelord-heuristikken brukes nå BEGRENSET – den avgjør ALDRI om et obligatorisk kildesitat (`job_ad_excerpt` for kompetansegap/CV-forslag) beholdes (kun ordrett sitatkontroll gjør det der), men brukes fortsatt til å luke `related_requirement_ids` (lav kostnad å ta feil: funnet vises fortsatt) og til styrkers obligatoriske `cv_excerpt` og CV-forslags valgfrie `cv_excerpt` (uendret fra forrige økt, ikke rapportert som problematisk).
- Fjernet lengdekravet på 4 bokstaver (nå 3), og la samtidig korte norske grammatiske fyllord ("som", "for", "med", "har", ...) til den eksisterende, enkle ordlisten, slik at korte fagord som "SQL" kan telle uten å åpne for at vanlige småord skaper falske treff.
- Erkjente og dokumenterte en reell, akseptert begrensning i stedet for å late som den er løst: en ren nøkkelord-heuristikk kan ikke skille "åpenbart feilkoblet" fra "reelt relatert, men med andre ord" (kundeservice/opplæring vs. kommunikasjonsevner) – dette løses ikke her, siden en ordentlig løsning (semantisk sammenligning/synonymordbok) ville vært det brukeren eksplisitt ba om å unngå.
- La til logging i `analysis_service.py` av antall funn før/etter grunnlagskontrollen (kun tall, aldri innhold), slik at fremtidige ekte kall kan vise direkte om noe ble fjernet av grunnlagskontrollen – dette tetter nettopp det hullet som gjorde årsaksgranskningen denne gangen vanskelig.
- Skrev målrettede tester: en direkte regresjonstest på selve rotårsaken (SQL telles nå som nøkkelord), en test som speiler det konkrete SQL-gapet, en test som dokumenterer den aksepterte begrensningen (kundeservice/kommunikasjon), en regresjonstest for at korte norske fyllord fortsatt ikke gir falske treff, og tester for den nye loggingen (bekrefter at den faktisk logger antall, og aldri logger CV-/annonseinnhold).

### Resultat
Endrede filer:
- `backend/app/grounding.py` – nøkkelord-relevans er ikke lenger en del av om `job_ad_excerpt` (kompetansegap/CV-forslag) beholdes (kun ordrett kontroll); minstelengde senket fra 4 til 3; utvidet fyllord-/stoppordliste; utvidet docstring med årsaksgranskningen og de bevisste avveiningene.
- `backend/app/analysis_service.py` – ny `_log_grounding_effect()`, kalt etter `enforce_grounding`, logger kun antall funn før/etter (ingen tekstinnhold).
- `backend/tests/test_grounding.py` – nye/justerte tester (se Plan).
- `backend/tests/test_analysis_service.py` – to nye tester for logging av grunnlagskontroll-effekten.

Ingen endring av `AnalysisResult`/`SourceReference`/API-responsformatet, og demomodus (`GET /api/analyze/demo`) er urørt.

Testresultat: `uv run pytest -q` → **66 passed, 0 failed** (opp fra 59). Ingen ekte eller betalte OpenAI-kall ble gjort.

Bekreftet på nytt at `backend/.env` (brukerens ekte nøkkel, åpnet i IDE under denne økten også) fortsatt er korrekt gitignored og ikke er rørt av meg.

Ingen git-commit/push er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
- Den dokumenterte begrensningen (kundeservice/opplæring → kommunikasjonsevner forblir ukoblet) er IKKE løst, kun bevisst akseptert og testet som kjent oppførsel – hvis gruppen senere vil forbedre dette, er neste skritt utenfor denne øktens scope (f.eks. en liten synonym-/kategoriliste, eller en enkel LLM-basert "er denne koblingen rimelig?"-verifisering).
- Brukeren bør kjøre et nytt ekte kall for å bekrefte at SQL-gapet nå vises, og se i backend-loggen (`_log_grounding_effect`) om grunnlagskontrollen fjerner noe uventet.
- Øvrige åpne punkter er uendret, se `issues.md`.

## 2026-11-05 kl. 14:59 — Sondre Tveit Amundsen

### Oppgave
Tredje ekte API-test gjennomført: HTTP 200 OK, SQL og Power BI vises nå korrekt som manglende, udokumentert kompetanse, ingen tydelig oppdiktede kvalifikasjoner, Power BI-feilkoblingene er borte. Noen relevante funn har fortsatt tomme `related_requirement_ids` – dette aksepteres som en dokumentert v1-begrensning. Oppgaven var å avslutte denne fasen: oppdatere `process-log.md` med hele normalmodus-utviklingen og de tre ekte testene, kontrollere `git status`/`git diff`, bekrefte at `backend/.env` ikke spores, kjøre backend-testene én siste gang, og oppsummere hvilke filer som skal committes – uten selv å committe, pushe eller gjøre flere ekte API-kall.

### Plan
- Kjørte `git status`, `git status` (lesbar), `git diff --stat`/`--numstat` og bekreftet `backend/.env` sin gitignore-status med `git check-ignore -v` og `git ls-files` (tom liste = ikke spores).
- Kjørte `uv run pytest -v` en siste gang for å bekrefte full, grønn teststatus før oppsummering.
- Skrev en ny, omfattende datert seksjon i `process-log.md` («05.11.2026 – Implementering av normalmodus med OpenAI») som dekker planleggingsfasen, implementeringen, alle tre ekte API-tester (med funn), de to tekniske utfordringene (feilkoblinger, og den for strenge SQL-fiksen) med årsak/løsning/læring, den aksepterte begrensningen, KI-bruk/kritisk vurdering, og neste steg – i samme stil og detaljnivå som de to eksisterende seksjonene i loggen.

### Resultat
- `process-log.md` (endret) – ny seksjon lagt til, ingen eksisterende innhold fjernet eller omskrevet.
- `git status`: 8 endrede, sporede filer (`README.md`, `architecture.md`, `backend/README.md`, `backend/app/main.py`, `backend/app/models.py`, `backend/pyproject.toml`, `backend/tests/test_models.py`, `backend/uv.lock`, pluss nå `process-log.md` = 9) og 10 nye, usporede filer (`backend/.env.example`, `backend/app/{analysis_service,config,grounding,llm_client,prompts}.py`, `backend/tests/{test_analysis_service,test_analyze_endpoint,test_grounding,test_llm_client}.py`).
- `backend/.env` er bekreftet IKKE spores av Git (`git check-ignore -v` → matcher `.gitignore:42:.env`; `git ls-files backend/.env` → tom; `git status --porcelain -- backend/.env` → tom).
- Testresultat: `uv run pytest -v` → **66 passed, 0 failed**.
- Ingen ekte OpenAI-kall ble gjort i denne avsluttende gjennomgangen. Ingen git-commit/push av kodeendringene er gjort (på brukerens eksplisitte instruks) – kun denne loggfilen committes av `sesjonslogg`-skillen.

### Åpne punkter
Ingen nye. Øvrige åpne punkter er uendret, se `issues.md`.
