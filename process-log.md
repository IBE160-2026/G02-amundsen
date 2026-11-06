# Process and AI Log

Denne loggen dokumenterer utviklingsprosessen for Career Transition Assistant, inkludert viktige beslutninger, bruk av KI-verktøy, iterasjoner, problemer og kvalitetssikring.

## 10.09.2026 – Oppstart og Product Brief

### Arbeid utført
- Valgte prosjektidéen Career Transition Assistant.
- Avgrenset første versjon til en KI-basert jobbsøknadsassistent.
- Utarbeidet og pushet `product-brief.md` til GitHub.
- Installerte og verifiserte nødvendig verktøykjede:
  - VS Code
  - Git og GitHub
  - Node.js og NPM
  - Python 3.12 via uv
  - Docker Desktop og WSL 2
  - Claude Code

### KI-bruk
ChatGPT ble brukt til idéutvikling, avgrensning av scope, formulering av Product Brief og veiledning i teknisk oppsett. Claude Code ble installert og testet med en enkel prøvefil.

### Viktige beslutninger
- Prosjektet skal være realistisk for én student.
- Første versjon skal fokusere på én konkret stillingsannonse om gangen.
- Automatisk jobbsøk, automatisk innsending og avansert ATS ble plassert utenfor v1.
- Appen skal ikke finne på kvalifikasjoner eller erfaringer.

## 08.10.2026 – Revisjon, planlegging og teknisk oppsett

### Arbeid utført

**Revisjon av Product Brief og utarbeidelse av PRD**
- Reviderte `product-brief.md` etter faglig tilbakemelding.
- Snevrerte inn primærbrukeren til studenter i avsluttende fase av bachelor- eller masterstudium som søker sin første faste jobb.
- Endret v1 slik at CV og stillingsannonse limes inn som tekst.
- Flyttet PDF/Word-opplasting og støttedokumentasjon ut av v1.
- Bestemte at v1 ikke skal ha innlogging eller permanent lagring av personopplysninger.
- La til demomodus slik at sensor kan teste løsningen uten egen API-nøkkel.
- La til `Technical Assumptions` i Product Brief.
- Opprettet og pushet `prd.md` med:
  - Product Overview
  - Product Goals
  - Non-Goals / Out of Scope
  - User Flow
  - Functional Requirements (FR1–FR12)
  - Non-Functional Requirements (NFR1–NFR8)
  - Acceptance Criteria and Testing
  - Open Decisions

**Arkitektur og videre planlegging**
- Opprettet `architecture.md` med beskrivelse av teknologistakk, applikasjonsstruktur, API-kommunikasjon, strukturert KI-output, sporbarhet, demomodus, testing og sikkerhet.
- Valgte React, Vite og JavaScript til frontend.
- Valgte Python 3.12, FastAPI og uv til backend.
- Planla kommunikasjon mellom frontend og backend gjennom REST API og JSON.
- Bestemte at språkmodell-API kun skal kontaktes fra backend, og at API-nøkkelen skal lagres i `.env`.
- Utsatte endelig valg av språkmodell/API til implementeringen.
- Opprettet `epics-and-stories.md` med fem epics:
  1. Input og modusvalg
  2. Analyse
  3. CV-forslag og sporbarhet
  4. Søknadsutkast
  5. Demo, feil og kvalitet

**UX og wireframe**
- Utarbeidet en første KI-generert wireframe for applikasjonens brukergrensesnitt.
- Oppdaget at wireframen foreslo PDF-/Word-opplasting og PDF-nedlasting, selv om dette var flyttet ut av v1.
- Kontrollerte forslaget mot PRD og avviste funksjonene som lå utenfor prosjektets scope.
- Utarbeidet en korrigert wireframe basert på tekstinnliming av CV og stillingsannonse, modusvalg, analyse, styrker, kompetansegap, CV-forslag og søknadsutkast.
- Den korrigerte wireframen bør senere lagres i prosjektets repository som dokumentasjon av UX-prosessen.

**Oppsett av frontend**
- Opprettet `frontend/` med React og Vite.
- Installerte nødvendige NPM-avhengigheter og valgte ESLint.
- Installasjonen ble fullført uten rapporterte sårbarheter.
- Startet utviklingsserveren og åpnet `http://localhost:5173/` i Chrome.
- Bekreftet at standardapplikasjonen fra Vite/React fungerte.
- Stoppet utviklingsserveren etter testing.
- Selve grensesnittet til Career Transition Assistant er foreløpig ikke implementert.

**Oppsett av backend**
- Opprettet `backend/` som et Python-prosjekt med uv.
- Installerte FastAPI og Uvicorn.
- Opprettet `backend/app/main.py` med en enkel FastAPI-applikasjon og et testendepunkt.
- Startet backend med `uv run uvicorn app.main:app --reload`.
- Testet `http://127.0.0.1:8000/` i Chrome og fikk forventet JSON-respons:
  `{"message":"Career Transition Assistant backend is running"}`
- Åpnet `http://127.0.0.1:8000/docs` og bekreftet at FastAPIs automatiske API-dokumentasjon fungerte.

### Tekniske utfordringer og løsninger

**1. PowerShell blokkerte npm**
- Problem: `npm.ps1` kunne ikke kjøres på grunn av PowerShells gjeldende Execution Policy.
- Løsning: Brukte `npm.cmd` i stedet for `npm`, uten å endre sikkerhetsinnstillingene.
- Læring: En teknisk feil kan ofte løses uten å endre systeminnstillinger eller redusere sikkerheten.

**2. Backend ble opprettet i feil mappe**
- Problem: Backend ble først opprettet i `C:\Users\sondr\backend`, utenfor prosjektets repository.
- Løsning: Flyttet backend til `C:\Users\sondr\G02-amundsen\backend`.
- Læring: Kontroll av arbeidsmappe og prosjektstruktur er viktig før terminalkommandoer kjøres.

**3. FastAPI startet med en ASGI-feil**
- Problem: Ved oppstart oppstod feilen `Attribute "app" not found in module "app.main"`.
- Mulig årsak: `main.py` var ikke lagret da serveren forsøkte å laste applikasjonen.
- Løsning: Kontrollerte innholdet i `main.py`, lagret filen og lot Uvicorn laste applikasjonen på nytt.
- Resultat: Serveren startet korrekt, og endepunktet returnerte forventet JSON-respons.
- Læring: Før kode eller prosjektstruktur endres, bør enkle årsaker som ulagrede filer kontrolleres.

**4. Backend hadde sitt eget Git-repository**
- Problem: `git status` inne i backend viste `master` og `No commits yet`, mens hovedprosjektet brukte `main`.
- Undersøkte problemet og bekreftet at `backend/.git` eksisterte.
- Løsning: Fjernet kun den ekstra `.git`-mappen i backend etter å ha kontrollert at den ikke inneholdt commits.
- Verifiserte at `Test-Path .\backend\.git` returnerte `False`.
- Kontrollerte deretter at hovedprosjektet registrerte både `backend/` og `frontend/`.
- Læring: Utilsiktede Git-repositories kan komplisere versjonskontrollen. Prosjektets Git-struktur bør kontrolleres før commits.

**5. Advarsler om linjeskift**
- Problem: Git viste advarsler om at LF ville bli erstattet med CRLF i enkelte filer.
- Vurdering: Dette var knyttet til håndtering av linjeskift på Windows og hindret ikke Git-operasjonen.
- Resultat: Filene ble lagt til og committet uten feil.

### KI-bruk og kvalitetssikring

- ChatGPT ble brukt som sparringspartner til å tolke den faglige tilbakemeldingen, foreslå konkrete endringer og formulere PRD-krav.
- KI ble brukt som støtte ved utarbeidelse av arkitektur, epics, stories og UX-wireframe.
- KI-forslagene ble gjennomgått og vurdert opp mot kravene før de ble tatt videre.
- Wireframen er et konkret eksempel på en KI-feil: KI foreslo funksjoner som var utenfor prosjektets scope. Forslaget ble kontrollert mot PRD, endret og korrigert.
- ChatGPT ble brukt til teknisk veiledning, feilsøking og forklaring av terminalkommandoer.
- Arbeidet ble gjennomført stegvis. Terminalresultater og skjermbilder ble kontrollert før neste handling.
- Ved Git-oppryddingen ble eksisterende struktur og historikk undersøkt før den ekstra `.git`-mappen ble slettet.
- Testresultater ble kontrollert manuelt i nettleser og terminal, fremfor å stole på at KI-generert kode automatisk fungerte.
- Det ble lagt vekt på å forstå hva kommandoene gjorde, og å unngå unødvendige eller risikable endringer.

### Viktige beslutninger

- Demomodus skal være en del av v1 og fungere uten ekstern API-request.
- API-nøkler skal lagres lokalt i `.env` og aldri pushes til GitHub.
- Endelig valg av språkmodell/API utsettes til senere i implementeringen.
- KI-kvalitet skal vurderes mot faste, fiktive testsett.
- Ingen database skal brukes i v1.
- Frontend og backend skal utvikles som separate deler som senere kobles sammen gjennom et API.
- Demomodus skal implementeres før integrasjon med en ekstern språkmodell.
- Prosjektet skal utvikles iterativt, med små, beskrivende Git-commits.
- Testing og kvalitetssikring skal gjennomføres underveis, ikke bare ved prosjektets avslutning.

### Testing og kvalitetssikring

**Frontend**
- React/Vite-prosjektet ble startet lokalt.
- Standardapplikasjonen ble åpnet i Chrome og fungerte som forventet.

**Backend**
- FastAPI startet korrekt etter at feilen i oppstartsprosessen ble løst.
- `GET /` returnerte forventet JSON-respons og HTTP-status 200.
- `/docs` og `/openapi.json` returnerte HTTP-status 200.
- FastAPIs dokumentasjon viste det registrerte `GET /`-endepunktet.

**Git og sikkerhet**
- Kontrollerte hovedprosjektets Git-status.
- Gjennomgikk `.gitignore` og kontrollerte at blant annet `.venv`, `node_modules` og `.env` var ekskludert.
- Brukte `git add -n` til å forhåndsvise hvilke filer som ville bli lagt til.
- Kontrollerte filene på nytt etter `git add`.
- Opprettet commit `7353ca4` med meldingen `Set up React frontend and FastAPI backend`.
- Pushet commiten til GitHub-repositoryet `IBE160-2026/G02-amundsen`.
- GitHub-pushen ble bekreftet som fullført.

### Status ved avslutning av arbeidsøkten

Planleggingsdokumentene er utarbeidet, og det grunnleggende tekniske oppsettet er på plass.

Frontend og backend er opprettet og testet hver for seg. Begge er lagt inn i prosjektets Git-repository.

Career Transition Assistant har foreløpig ikke et ferdig brukergrensesnitt eller fungerende analysefunksjonalitet. Frontend og backend er heller ikke koblet sammen.

### Neste steg

1. Implementere Pydantic-responsmodeller for strukturerte analyseresultater.
2. Implementere demomodus med fiktiv CV, stillingsannonse og fast eksempelresultat.
3. Bygge React-grensesnittet basert på den korrigerte wireframen.
4. Koble frontend og backend sammen.
5. Teste demomodus fra input til resultat.
6. Velge språkmodell/API og deretter implementere normalmodus.
7. Fortsette kvalitetssikring, testing, Git-commits og dokumentasjon av KI-bruk.


## 05.11.2026 – Implementering av backend, frontend og fungerende demomodus

### Arbeid utført

**Oppstart og oppdatering av prosjektet**
- Åpnet prosjektet `G02-amundsen` i VS Code.
- Kontrollerte Git-status og kjørte `git pull` i tråd med foreleserens instruksjoner.
- Mottok nye prosjektfiler, blant annet `CLAUDE.md` og `.claude/skills/sesjonslogg/SKILL.md`.
- Gjennomgikk instruksjonene for sesjonslogging og fortsatte utviklingen med utgangspunkt i eksisterende PRD, arkitektur og epics/stories.
- Kontrollerte at PRD-en allerede var utarbeidet før fristen 05.11.2026.

**Implementering av backend**
- Brukte Claude Code til å implementere Pydantic-responsmodeller for strukturerte analyseresultater.
- Opprettet et demo-endepunkt i FastAPI: `GET /api/analyze/demo`.
- La til fiktive eksempeldata med CV for Kari Nordmann og stillingsannonse fra Fjord Digital AS.
- Demoresponsen inneholder stillingskrav, relevante styrker, kompetansegap, CV-forslag, kildereferanser og søknadsutkast.
- Demomodus fungerer uten ekstern språkmodell eller API-nøkkel.
- Opprettet automatiserte tester. Alle 20 backend-testene bestod.
- Lagret backend-implementeringen i Git med commit `ad9bfa9`.

**Implementering av frontend**
- Brukte Claude Code til å bygge React-grensesnittet med utgangspunkt i PRD og arkitekturen.
- Implementerte valg mellom demomodus og normalmodus. Normalmodus er foreløpig deaktivert.
- Opprettet komponenter for visning av CV, stillingsannonse, stillingskrav, styrker, kompetansegap, CV-forslag, sporbarhet og søknadsutkast.
- Implementerte et redigerbart søknadsutkast.
- Knyttet frontend til FastAPI gjennom en egen API-klient.
- Implementerte visning av lastestatus og feilmeldinger.
- Oppdaterte designet med responsiv styling.
- La til Vitest og automatiserte frontend-tester.
- Alle 8 frontend-testene bestod.
- ESLint og produksjonsbygg ble rapportert som vellykket.
- Oppdaterte README-filene med informasjon om lokal kjøring.
- Lagret frontend-implementeringen i Git med commit `fb2e5e4`.

### Tekniske utfordringer og løsninger

**1. Utgått innlogging i Claude Code**
- Problem: Claude Code viste `Login expired` og kunne ikke starte programmeringsoppgaven.
- Løsning: Gjennomførte ny innlogging og kontrollerte at Claude Code fikk tilgang til prosjektet.
- Læring: Innlogging og tilgang til KI-verktøy må kontrolleres før utviklingsarbeidet starter.

**2. Feil port mellom frontend og backend**
- Problem: Demoanalysen viste feilmeldingen «Kunne ikke nå backend-tjeneren».
- Årsak: Backend kjørte på port 8001, mens frontend opprinnelig var konfigurert til å kontakte port 8000.
- Løsning: Endret midlertidig frontend til port 8001 og bekreftet at demoanalysen fungerte. Standardiserte deretter prosjektet på port 8000 og startet backend på nytt.
- Resultat: Demoanalysen fungerte også etter standardiseringen.
- Læring: Frontend og backend må ha samsvarende API-konfigurasjon. Automatiske tester alene avdekket ikke denne lokale konfigurasjonsfeilen.

**3. Begrenset nettlesertesting fra Claude Code**
- Claude Code foreslo å koble seg til Chrome for å gjennomføre nettlesertesting.
- Valgte å ikke gi denne tilgangen, og gjennomførte i stedet den manuelle funksjonstesten selv.
- Dette ga mulighet til å kontrollere brukeropplevelsen og vurdere resultatene direkte.

### Testing og kvalitetssikring

**Automatisert testing**
- Backend: 20 av 20 tester bestått.
- Frontend: 8 av 8 tester bestått.
- ESLint og Vite-produksjonsbygg gjennomført uten rapporterte feil.

**Manuell funksjonstesting**
- Startet FastAPI og React/Vite lokalt i separate terminaler.
- Åpnet Career Transition Assistant på `http://localhost:5173/`.
- Bekreftet at demomodus kunne startes fra grensesnittet.
- Kontrollerte at fiktiv CV og stillingsannonse ble vist.
- Kontrollerte at stillingskrav, relevante styrker, kompetansegap, CV-forslag og søknadsutkast ble vist.
- Kontrollerte at CV-forslagene hadde henvisninger til CV og stillingsannonse.
- Testet at søknadsutkastet kunne redigeres direkte.
- Testet at kommunikasjonen fortsatt fungerte etter korrigering av API-porten.

**Kvalitetssikring av analyseresultatet**
- Gjennomgikk tre CV-forslag knyttet til agile arbeidsmetoder, Python/JavaScript og SQL/databaseerfaring.
- Vurderte at forslagene var relevante for stillingen, men identifiserte behov for å kontrollere at brukeren ikke oppfordres til å legge til udokumentert erfaring.
- Dette blir viktig ved senere implementering av normalmodus med en ekte språkmodell.

### KI-bruk og kritisk vurdering

- Claude Code ble brukt til å generere backend-modeller, demo-endepunkt, React-komponenter, API-integrasjon, tester og dokumentasjon.
- ChatGPT ble brukt til å avgrense utviklingsoppgaver, vurdere fremdrift, feilsøke, kontrollere testresultater og veilede i Git.
- KI-generert kode ble kontrollert gjennom automatiserte tester og manuell funksjonstesting.
- Portfeilen viste at beståtte automatiserte tester ikke nødvendigvis betyr at hele applikasjonen fungerer i brukerens faktiske utviklingsmiljø.
- Testing av CV-forslagene synliggjorde risikoen for at KI kan foreslå opplysninger som ikke er dokumentert i brukerens CV.
- Utviklingen ble delt inn i separate oppgaver for backend og frontend, slik at resultatene kunne testes og lagres underveis.
- Claude Code ble instruert om ikke å opprette commits eller pushe applikasjonskoden automatisk. Kodeendringene ble kontrollert og committet separat.

### Git og versjonskontroll

- Opprettet commit `ad9bfa9` for backend og demomodus.
- Opprettet commit `fb2e5e4` med meldingen `Build React frontend and connect demo API`.
- Kontrollerte endrede og nye filer med `git status`.
- Pushet implementeringen til GitHub-repositoryet `IBE160-2026/G02-amundsen`.
- Sesjonslogging fra Claude Code ble tatt i bruk som supplerende dokumentasjon.

### Status ved avslutning av denne utviklingsfasen

Career Transition Assistant har nå en fungerende demomodus med React-frontend og FastAPI-backend.

Brukeren kan starte demoanalysen, se strukturerte resultater med kildereferanser og redigere søknadsutkastet.

Normalmodus med ekte KI-analyse er foreløpig ikke implementert. Den fungerende demomodusen gir et grunnlag for videre utvikling og testing.

### Neste steg

1. Velge språkmodell/API med hensyn til kvalitet, kostnader, strukturert output og Python-integrasjon.
2. Implementere normalmodus med brukerens egen CV og stillingsannonse som tekst.
3. Implementere kontroll av KI-genererte påstander mot brukerens faktiske opplysninger.
4. Teste løsningen mot flere fiktive testsett.
5. Forbedre feilhåndtering og kvalitetssikre brukergrensesnittet.
6. Vurdere publisering på Vercel.
7. Ferdigstille README, prosessdokumentasjon og refleksjonsrapport.


## 05.11.2026 – Implementering av normalmodus med OpenAI (ekte språkmodell)

### Arbeid utført

**Planlegging før implementering**
- Ba Claude Code lese PRD, arkitektur, epics/stories, `CLAUDE.md` og eksisterende backend-kode, og legge fram en plan for normalmodus før noe kode ble endret.
- Valgte OpenAI med modellen `gpt-5.4-mini` som språkmodell-leverandør.
- Lot Claude Code verifisere, uten nettverkskall, at de eksisterende Pydantic-modellene fra demomodus (`AnalysisResult` m.fl.) allerede var kompatible med OpenAI sin strukturerte JSON-output («Structured Outputs») – ingen endring av selve skjemaet var nødvendig.
- Godkjente planen før implementeringen startet.

**Implementering av normalmodus (backend)**
- La til `POST /api/analyze` i FastAPI, ved siden av det uendrede demo-endepunktet `GET /api/analyze/demo`.
- Opprettet `config.py` (innstillinger fra `backend/.env`), `llm_client.py` (lager OpenAI-klienten først når den trengs, uten automatiske retries), `prompts.py` (systemprompt med strenge regler mot oppdiktet informasjon og krav om ordrette sitater) og `analysis_service.py` (orkestrerer kallet og egne feiltyper).
- Opprettet `grounding.py`: en egen kontroll som sjekker at kildesitater i KI-svaret faktisk finnes ordrett i CV-en/stillingsannonsen, med normalisering av mellomrom og store/små bokstaver.
- Satte rimelige grenser for inputlengde (CV og stillingsannonse), timeout (30 sekunder) og ingen automatiske retries ved API-feil.
- Opprettet `backend/.env.example` og oppdaterte `architecture.md` med valg av modell og miljøvariabler (erstattet det tidligere, generiske `LLM_API_KEY`-eksempelet).
- Skrev automatiserte tester som mocker OpenAI-klienten – ingen ekte eller betalte API-kall i testsuiten. Testantallet økte fra 20 til 66 gjennom denne fasen.
- Frontend for normalmodus ble bevisst IKKE implementert i denne omgangen – backenden skulle kvalitetssikres med ekte kall først, slik faglærer/plan tilsa.

**Tre ekte API-tester mot OpenAI**

1. **Første ekte kall:** HTTP 200 OK. Søknadsutkastet inneholdt ingen oppdiktede kvalifikasjoner. Manuell kvalitetssikring avdekket tre feilkoblinger: en styrke om en bacheloroppgave ble koblet til et krav om Power BI som oppgaven ikke dokumenterte; et kompetansegap ble koblet til feil stillingskrav på samme måte; og et CV-forslag hadde et reelt, men irrelevant CV-sitat som kildehenvisning.
2. **Andre ekte kall (etter fiks):** HTTP 200 OK. Power BI-feilene var borte. Men et korrekt SQL-kompetansegap forsvant helt, og en styrke om kundeservice/opplæring mistet en relevant krav-kobling. Årsaken ble undersøkt i koden (ikke gjettet): en nøkkelord-heuristikk som skulle hindre feilkoblinger krevde minst 4 bokstaver for at et ord skulle telle, og utelukket dermed det korte, men presise ordet «SQL» fra sammenligningen.
3. **Tredje ekte kall (etter justering):** HTTP 200 OK. SQL og Power BI vises nå begge korrekt som manglende, udokumentert kompetanse. Ingen tydelig oppdiktede kvalifikasjoner ble funnet. De tidligere feilkoblingene til Power BI er borte. Noen relevante funn har fortsatt tomme `related_requirement_ids` – dette er en kjent, dokumentert begrensning som aksepteres i v1 (se under). Søknadsutkastet fungerer funksjonelt, men kan forbedres språklig senere.

### Tekniske utfordringer og løsninger

**1. Et sitat kan være ekte uten at koblingen er riktig**
- Problem: Grunnlagskontrollen kontrollerte opprinnelig bare at kildesitater fantes ordrett i CV/annonse, ikke at koblingen (hvilket krav et funn ble knyttet til) faktisk var riktig.
- Løsning: La til en enkel, deterministisk nøkkelord-overlapp-kontroll for å luke bort åpenbart feilaktige koblinger (f.eks. bacheloroppgave koblet til Power BI).
- Læring: Et korrekt, ordrett sitat er ikke det samme som en korrekt tolkning eller kobling.

**2. Den første fiksen var for streng (SQL-gapet forsvant)**
- Problem: Den nye nøkkelord-kontrollen krevde minst 4 bokstaver for at et ord skulle telle som et treff, og utelukket dermed «SQL» (3 bokstaver) – et korrekt kompetansegap ble slettet helt, uavhengig av om språkmodellen faktisk leverte det riktig.
- Undersøkelse: Årsaken ble bekreftet ved å kjøre koden direkte på representativ tekst, ikke ved å gjette. Det var derimot ikke mulig å fastslå med 100 % sikkerhet hva språkmodellen opprinnelig svarte i den konkrete sesjonen, siden selve rå-svaret aldri logges (for å unngå å lagre CV-/annonseinnhold).
- Løsning: Senket minstelengden til 3 bokstaver, la til flere korte, grammatiske fyllord i unntakslisten, og – viktigst – gjorde nøkkelord-kontrollen IKKE lenger avgjørende for om et obligatorisk kildesitat beholdes. Kun selve, ordrette sitatkontrollen avgjør nå dette; nøkkelord-heuristikken brukes bare der kostnaden ved en feilvurdering er lav (krav-koblinger, og et valgfritt CV-sitat).
- La også til logging av antall funn før/etter grunnlagskontrollen (kun antall, aldri innhold), slik at et lignende spørsmål kan besvares direkte neste gang.
- Læring: En sikkerhetsmekanisme kan selv bli en feilkilde. Det er ikke tilstrekkelig å teste at en fiks løser det rapporterte problemet – den må også testes mot at den ikke skaper nye, utilsiktede problemer.

**3. En gjenværende, bevisst akseptert begrensning**
- En ren nøkkelord-heuristikk kan ikke skille perfekt mellom en «åpenbart feilaktig» kobling og en «reelt relatert, men annerledes formulert» kobling (f.eks. kundeservice/opplæring vs. kommunikasjonsevner) – begge mangler delt ordforråd.
- Besluttet å IKKE bygge en mer komplisert løsning (f.eks. en synonymordbok eller semantisk sammenligning) for å løse dette, i tråd med ønsket om et enkelt og forståelig regelverk i v1.
- Dette er dokumentert i koden og dekket av en egen automatisert test, slik at det er en kjent, synlig begrensning – ikke en skjult feil.

**4. Ekte API-nøkkel i lokal `.env`**
- Satte opp en ekte OpenAI API-nøkkel lokalt i `backend/.env` for å kunne kjøre de tre ekte testene.
- Kontrollerte flere ganger i løpet av arbeidet at `backend/.env` er dekket av `.gitignore`, ikke er spores av Git, og at nøkkelen aldri ble gjengitt i kode, tester eller logger.

### Testing og kvalitetssikring

**Automatisert testing**
- Backend: alle 66 av 66 tester bestått (opp fra 20 etter forrige fase), inkludert nye, målrettede tester for grunnlagskontrollen, SQL-regresjonen, den aksepterte begrensningen og den nye loggingen.
- Ingen av de automatiserte testene gjør ekte eller betalte API-kall – OpenAI-klienten mockes gjennomgående.
- Demomodus er verifisert uendret og fortsatt fungerende gjennom hele denne fasen.

**Manuell kvalitetssikring av ekte KI-svar**
- Tre ekte kall mot OpenAI, med manuell gjennomgang av stillingskrav, styrker, kompetansegap, CV-forslag, kildehenvisninger og søknadsutkast for hvert svar (se over).
- Kontrollerte spesifikt at ingen oppdiktede kvalifikasjoner ble presentert som fakta – et kjernekrav i PRD (FR10).

### KI-bruk og kritisk vurdering

- Claude Code ble brukt til å planlegge, implementere og rette normalmodus-integrasjonen, samt til å skrive og kjøre automatiserte tester.
- Claude Code ble bedt om å undersøke årsaken til SQL-feilen i koden i stedet for å gjette, og rapporterte selv tydelig hvor sikker/usikker konklusjonen var (bekreftet i koden, men ikke bekreftet for den ene, historiske KI-forespørselen, siden rå-svar ikke logges).
- KI-genererte forslag til fiks ble ikke akseptert blindt: den første fiksen (nøkkelord-kontroll på alle kildesitater) viste seg å være for streng ved reell testing, og ble korrigert i en egen runde etter at feilen ble rapportert.
- Det ble en eksplisitt beslutning å IKKE la KI-en bygge et mer komplisert regelverk (f.eks. synonymer/semantikk) for å jage den siste begrensningen, men heller akseptere og dokumentere den – en avveining tatt av studenten, ikke overlatt til KI-en.
- Claude Code ble instruert om ikke å gjøre ekte, betalte API-kall selv, og ikke å opprette en reell API-nøkkel – dette ble gjort manuelt av studenten.
- Claude Code ble instruert om ikke å committe eller pushe kodeendringer i denne fasen; endringene er kontrollert med `git status`/`git diff` og committes separat av studenten.

### Git og versjonskontroll

- `git status` viser 8 endrede, sporede filer (`README.md`, `architecture.md`, `backend/README.md`, `backend/app/main.py`, `backend/app/models.py`, `backend/pyproject.toml`, `backend/tests/test_models.py`, `backend/uv.lock`) og 10 nye, usporede filer (`backend/.env.example`, `backend/app/{analysis_service,config,grounding,llm_client,prompts}.py`, `backend/tests/{test_analysis_service,test_analyze_endpoint,test_grounding,test_llm_client}.py`).
- Bekreftet med `git check-ignore -v backend/.env` og `git ls-files backend/.env` at den ekte `.env`-filen med API-nøkkelen ikke er, og aldri har vært, spores av Git.
- Ingen av disse endringene er committet eller pushet ennå – dette gjøres av studenten i en egen commit etter denne gjennomgangen.

### Status ved avslutning av denne utviklingsfasen

Backend for Career Transition Assistant har nå en fungerende normalmodus som kommuniserer med OpenAI (`gpt-5.4-mini`), validert mot tre ekte API-kall. Demomodus er uendret og fortsatt fungerende. Frontend har ikke støtte for normalmodus ennå – normalmodus kan foreløpig bare testes direkte mot backend-API-et (curl eller `/docs`).

### Neste steg

1. Koble frontend til `POST /api/analyze` og legge til et skjema for innliming av CV og stillingsannonse (aktivere normalmodus i grensesnittet).
2. Forbedre den språklige kvaliteten på søknadsutkastet.
3. Vurdere om den dokumenterte begrensningen rundt krav-koblinger (`related_requirement_ids`) bør forbedres senere, f.eks. med en enkel kategoriliste.
4. Teste løsningen mot flere fiktive/ekte testsett for å bygge videre erfaring med KI-kvaliteten.
5. Vurdere publisering på Vercel.
6. Ferdigstille README, prosessdokumentasjon og refleksjonsrapport.


## 05.11.2026 – CORS-feil under manuell testing av normalmodus

### Arbeid utført

- Testet normalmodus manuelt i nettleseren med backend på `http://127.0.0.1:8001` og frontend på `http://localhost:5174`.
- Fikk følgende feil i nettleserkonsollen når frontend kalte `GET /api/analyze/demo`:
  `Access to fetch at 'http://127.0.0.1:8001/api/analyze/demo' from origin 'http://localhost:5174' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present.`
- Bemerket at samme endepunkt fungerte fint når det ble åpnet direkte i nettleserens adressefelt – feilen gjaldt altså kun skript-initierte `fetch()`-kall fra frontend, ikke vanlig navigasjon.

### Undersøkelse, årsak og løsning

- Kontrollerte eksisterende CORS-konfigurasjon i `backend/app/main.py`: `allow_origins` tillot kun `http://localhost:5173` og `http://127.0.0.1:5173`.
- Årsak: Vite velger automatisk en annen port (5174, osv.) hvis standardporten 5173 allerede er i bruk – det var nettopp det som skjedde under denne testen. Backendens CORS-liste var ikke oppdatert til å dekke denne alternative porten, så nettleseren blokkerte responsen selv om selve API-kallet fungerte på serversiden.
- Bekreftet årsaken ved å undersøke Starlette sin faktiske oppførsel: et `GET`-kall fra et ikke-tillatt origin besvares fortsatt med HTTP 200 av backenden, men UTEN `Access-Control-Allow-Origin`-headeren – det er dette som gjør at nettleseren avviser svaret på klientsiden.
- Løsning: La til `http://localhost:5174` og `http://127.0.0.1:5174` i `allow_origins`, i tillegg til de eksisterende oppføringene for port 5173. CORS ble bevisst IKKE åpnet for alle domener (`allow_origins=["*"]`) – listen er fortsatt en eksplisitt, begrenset liste over lokale utviklingsadresser.
- La til 11 nye automatiserte tester (`backend/tests/test_cors.py`) som bekrefter at alle fire tillatte origins (localhost/127.0.0.1 på port 5173 og 5174) faktisk får CORS-tillatelse på både vanlige kall og CORS-preflight, at et ukjent origin (f.eks. `http://evil.example.com`) ikke får det, og at konfigurasjonen fortsatt er en konkret liste og ikke et jokertegn.

### Testing og kvalitetssikring

- Backend: alle 77 av 77 tester bestått (opp fra 66), inkludert de 11 nye CORS-testene.
- Ingen ekte, betalte OpenAI-kall ble gjort under denne feilsøkingen.

### KI-bruk og kritisk vurdering

- Claude Code ble bedt om å undersøke den eksisterende CORS-konfigurasjonen og den faktiske årsaken (Vite sin automatiske portvalg) før noe ble endret, i stedet for å anta at feilen lå et annet sted (f.eks. i backendens adresse eller port).
- Endringen ble gjort minimal og målrettet: kun CORS-listen ble utvidet med de to nye origin-oppføringene som faktisk var nødvendige, ingen andre deler av konfigurasjonen ble rørt.
- Claude Code ble instruert om ikke å committe eller pushe denne fiksen selv; endringen kontrolleres og committes separat.

### Status

CORS-feilen er rettet og dekket av automatiserte tester. Normalmodus og demomodus kan nå nås fra frontend uavhengig av om Vite kjører på port 5173 eller 5174.


## 05.11.2026 – Vellykket manuell ende-til-ende-test i nettleseren

### Arbeid utført

Gjennomførte en fullstendig manuell ende-til-ende-test av Career Transition Assistant i nettleseren, med frontend på `http://localhost:5174` og backend på `http://127.0.0.1:8001`, etter at CORS-feilen samme dag var rettet.

**Testflyt (normalmodus, ekte OpenAI API-kall)**
- Bekreftet først at demomodus fungerte som forventet etter CORS-fiksen.
- Byttet til normalmodus og limte inn en fiktiv CV og stillingsannonse.
- Kjørte analysen mot den ekte språkmodellen (`gpt-5.4-mini`) via `POST /api/analyze`.

**Resultater**
- Analysen identifiserte relevante styrker, hver med kildehenvisning til CV-en og/eller stillingsannonsen.
- SQL og Power BI ble korrekt identifisert som manglende, udokumentert kompetanse (kompetansegap) – i tråd med fiksene fra de tre foregående ekte testene samme dag.
- CV-forslagene var relevante for stillingen.
- Søknadsutkastet var basert på faktisk innhold i CV-en, uten oppdiktede kvalifikasjoner.

### Kritisk vurdering

- Dette bekrefter at hele kjeden – frontend → CORS → backend → OpenAI → grunnlagskontroll → visning i grensesnittet – fungerer sammen i praksis, ikke bare i automatiserte tester med mockede kall.
- De tidligere oppdagede feilene (feilkoblede krav, et SQL-gap som forsvant) er ikke gjenoppstått: SQL og Power BI vises nå korrekt som kompetansegap, og CV-forslagene fremstår som relevante.
- En gjenværende, mindre begrensning: søknadsutkastet er noe generelt formulert. Dette påvirker ikke kravet om at applikasjonen ikke skal finne på kvalifikasjoner (FR10) – utkastet er fortsatt faktabasert – men det er et forbedringspunkt for hvor nyttig/personlig utkastet oppleves av brukeren.
- Denne testen dekker én fiktiv CV/stillingsannonse-kombinasjon. Den sier derfor noe om at løsningen fungerer, men ikke at den fungerer like godt for alle typer CV-er og stillinger – det krever testing mot flere, varierte testsett (se "Neste steg" i tidligere seksjoner).

### Testing og kvalitetssikring

- Manuell ende-til-ende-test i nettleser, med ekte OpenAI API-kall (det fjerde ekte kallet denne dagen, etter de tre foregående rapportert i seksjonen "Implementering av normalmodus med OpenAI").
- Ingen ytterligere automatiserte tester ble kjørt eller endret i denne gjennomgangen – kun dokumentasjon av resultatet av den manuelle testen.

### KI-bruk og kritisk vurdering

- Claude Code ble brukt kun til å dokumentere testresultatet og den kritiske vurderingen i denne loggen – ingen kode ble endret, og ingen nye API-kall ble gjennomført av Claude Code selv.

### Status ved avslutning av denne testrunden

Career Transition Assistant fungerer nå ende-til-ende i nettleseren for begge moduser, verifisert med et ekte OpenAI-kall. Gjenværende kjente begrensninger:

1. Søknadsutkastet kan oppleves som noe generelt – språklig/stilistisk forbedring er et mulig forbedringspunkt, ikke en korrekthetsfeil.
2. Den tidligere dokumenterte begrensningen i krav-koblinger (`related_requirement_ids` kan gå glipp av en reelt relevant, men annerledes formulert kobling) står fortsatt, akseptert som en v1-begrensning.
3. Testingen er så langt gjort med ett testsett (en fiktiv CV og stillingsannonse) – bredere testing mot flere, varierte CV-er/stillinger er ikke gjort.
4. Ingen automatisert test kan verifisere en ekte, levende OpenAI-respons – kvaliteten på KI-genererte resultater må fortsatt vurderes manuelt, slik PRD-en (avsnitt 7) forutsetter.


## 05.11.2026 – Forberedelse av publisering på Vercel (fase 1)

### Arbeid utført

Etter at en publiseringsplan ble gjennomgått og godkjent (Vercel **Services** valgt som arkitektur – ett Vercel-prosjekt for frontend og backend, i stedet for to separate prosjekter), ble første fase av det konkrete oppsettet gjennomført. Ingen Vercel-prosjekt er opprettet, og ingen ekte OpenAI-kall er gjort.

**Ny fil: `vercel.json` (repo-rot)**
- Definerer `frontend/` og `backend/` som to Vercel Services.
- Backend-tjenesten får `entrypoint: "app.main:app"`, som peker direkte på den eksisterende FastAPI-instansen i `backend/app/main.py` – ingen restrukturering av backend-koden var nødvendig.
- To rewrite-regler: `/api/*` → backend-tjenesten, alt annet → frontend-tjenesten.
- Konfigurasjonen er hentet fra og verifisert mot gjeldende offisiell Vercel-dokumentasjon (`/docs/services`, `/docs/services/routing`, `/docs/services/config-reference`), ikke gjettet.

**Frontend: automatisk relativ adresse i produksjon**
- `frontend/src/api/analyzeApi.js` endret slik at adressen til backend velges automatisk basert på om bygget er et utviklings- eller produksjonsbygg (`import.meta.env.DEV`), i stedet for å kreve at noen manuelt setter en miljøvariabel riktig i Vercel-dashbordet. Lokalt: `http://127.0.0.1:8000` (uendret). I et produksjonsbygg: en relativ adresse, som Vercel Services ruter til backend-tjenesten på samme domene.
- Dette ble bevisst valgt fremfor en ren miljøvariabel-basert løsning, siden en glemt/feilsatt miljøvariabel ellers ville gitt en brutt produksjonsapplikasjon.
- Bekreftet empirisk (ikke bare med enhetstest) ved å bygge frontend og søke i det ferdige bygget: ingen referanse til `127.0.0.1:8000` finnes i produksjonsbygget, mens den relative adressen `/api/analyze/demo` gjør.

**Opprydding i `backend/pyproject.toml`**
- Fjernet den ubrukte `[project.scripts] backend = "backend:main"`-resten fra `uv init` (pekte på en modul som aldri er brukt av selve applikasjonen). Bekreftet med `uv sync` og full testkjøring at dette ikke påvirker noe.

**Dokumentasjon**
- `architecture.md`: ny seksjon 10 "Deployment (Vercel)" – beskriver Services-arkitekturen, hvordan frontend finner backend i produksjon, nødvendige miljøvariabler, og hvordan man forhindrer misbruk av API-kreditter. `vercel.json` lagt til i filstruktur-oversikten (avsnitt 5).
- `README.md`: rettet to utdaterte linjer som fortsatt sa at normalmodus ikke var koblet til frontend (dette ble gjort i en tidligere økt). Ny seksjon "Publisering på Vercel" med en konkret, nummerert sjekkliste for det som må gjøres manuelt i Vercel sitt dashbord.

### Testing og kvalitetssikring

- Backend: `uv run pytest -q` → **77 av 77 bestått** (uendret – oppryddingen i `pyproject.toml` påvirket ingen testresultater).
- Frontend: `npx vitest run` → **23 av 23 bestått** (opp fra 21 – to nye tester for den DEV-avhengige adressevalget, pluss én test for eksplisitt overstyring via `VITE_API_BASE_URL`).
- `npx eslint .` → ingen feil. `npx vite build` → bygget uten feil, og inspisert direkte for å bekrefte riktig adressevalg (se over).
- Ingen ekte, betalte OpenAI-kall ble gjort.

### KI-bruk og kritisk vurdering

- Claude Code ble bedt om å hente og bruke *gjeldende* offisiell Vercel-dokumentasjon for `vercel.json`-skjemaet, i stedet for å basere konfigurasjonen på eldre eller antatt kunnskap – viktig siden Vercel sin Services-funksjon er relativt ny (beta).
- Et forsøk på å teste produksjons-adressevalget med et vanlig mocket enhetstest (ved å stubbe `import.meta.env.DEV`/`PROD`) fungerte ikke som forventet, fordi Vite erstatter disse verdiene statisk ved bygging snarere enn å lese dem dynamisk. Claude Code identifiserte dette selv i stedet for å late som testen var gyldig, og verifiserte oppførselen empirisk ved å inspisere det faktiske produksjonsbygget i stedet.
- Ingen Vercel-prosjekt ble opprettet og ingen kode ble pushet av Claude Code, i tråd med instruksjonene.

### Status

Repoet er klart for at et Vercel-prosjekt kan opprettes og kobles til. Gjenstår (manuelt, i Vercel): opprette prosjektet, sette `OPENAI_API_KEY` på Production-miljøet, sette et forbrukstak hos OpenAI, og gjennomføre første publisering.


## 05.11.2026 – Feil i demomodus etter publisering på Vercel

### Feilen

Career Transition Assistant ble publisert på `https://g02-amundsen.vercel.app/` – selve
publiseringen var vellykket, og React-frontenden lastet riktig. Men et klikk på
«Kjør demoanalyse» ga feilmeldingen:

> "Kunne ikke laste demodata. Kontroller at test-data-filene finnes."

Demomodus fungerte uten problemer lokalt før publisering.

### Undersøkelse og årsak

Backenden leser demodata (fiktiv CV, stillingsannonse og eksempelresultat) fra disk i
`app/demo_data.py`, via en sti beregnet relativt til modulfilen
(`Path(__file__).resolve().parents[N] / "test-data"`). Filene selv lå i en `test-data/`-mappe
på **repo-roten**, altså utenfor `backend/`.

Årsaken ble bekreftet mot gjeldende Vercel-dokumentasjon (ikke gjettet): en Vercel
Service bygges og bunter **kun** filer som ligger inne i tjenestens egen `root`
(`backend/`, se `vercel.json`). En sti som peker utenfor denne mappen – som den
gamle `../test-data/` – finnes rett og slett ikke i det produksjonsbyggede
funksjonsmiljøet, selv om den fungerer helt fint lokalt (der hele repoet ligger samlet
på disk). Det er nøyaktig dette som ga `FileNotFoundError` → feilmeldingen over.

### Løsningen

Minst mulig endring som løser problemet fullt ut:

- Flyttet `test-data/` fra repo-roten til **`backend/test-data/`** (med `git mv`, for å
  bevare filhistorikken).
- Endret `TEST_DATA_DIR` i `app/demo_data.py` til å peke på `backend/test-data/` i stedet
  for repo-roten (én linje).
- Oppdaterte prosjektstruktur-oversikten i `architecture.md` og lenken i `README.md`
  til den nye plasseringen, samt la til en kort forklaring i `architecture.md` sin
  publiseringsseksjon om hvorfor demodata må ligge inne i `backend/`.
- La til en ny test (`test_test_data_dir_is_inside_backend_service_root`) som
  kontrollerer at demodata-mappen faktisk ligger inne i `backend/` – denne ville fanget
  opp akkurat denne feilen før publisering, i motsetning til de eksisterende testene
  (som alltid kjører lokalt, der hele repoet er tilgjengelig uansett).
- Ingen endring i selve demodataene, API-et, eller frontend – kun hvor filene bor og
  hvordan backenden finner dem.

### Testing og kvalitetssikring

- Backend: `uv run pytest -q` → **78 av 78 bestått** (opp fra 77 – én ny, målrettet
  regresjonstest).
- Frontend: `npx vitest run` → **23 av 23 bestått** (uendret – ingen frontend-kode
  påvirket).
- `npx eslint .` → ingen feil. `npx vite build` → bygget uten feil.
- Manuell smoke-test lokalt: startet backenden på nytt og bekreftet at
  `GET /api/analyze/demo` fortsatt svarer korrekt med den fiktive CV-en fra den nye
  plasseringen.
- Ingen ekte, betalte OpenAI-kall ble gjort.

### KI-bruk og kritisk vurdering

- Claude Code ble bedt om å fastslå den konkrete årsaken før noe ble endret, og gjorde
  dette ved å lese Vercel sin dokumentasjon om fil-bunting for Python-tjenester, i
  stedet for å gjette basert på feilmeldingens ordlyd alene.
- Løsningen (flytte datamappen inn i tjenesten) retter selve rotårsaken direkte, i
  stedet for en omvei (f.eks. en kopieringsscript i byggetrinnet), i tråd med ønsket
  om minst mulig, men korrekt, endring.
- Den nye testen er bevisst utformet for å fange opp nettopp denne feilklassen på
  nytt (data flyttet ut av tjenesten igjen), ikke bare at dagens filer finnes.

### Status

Feilen er rettet lokalt og dekket av en ny test. Gjenstår: publisere denne endringen på
nytt til det eksisterende Vercel-prosjektet (ingen nytt prosjekt opprettes), og bekrefte
at demomodus fungerer i produksjon etterpå.


## 05.11.2026 – Vellykket publisering bekreftet, normalmodus bevisst holdt av i produksjon

### Status

Career Transition Assistant er publisert på **https://g02-amundsen.vercel.app/**
(siste applikasjonscommit `c10c0f7`). Frontend og FastAPI-backend kjører sammen som
to Vercel Services i ett prosjekt, slik planlagt.

**Manuell bekreftelse:** åpnet den publiserte siden i nettleseren, kjørte demomodus og
bekreftet at resultatet (krav, styrker, kompetansegap, CV-forslag, søknadsutkast) vises
riktig – demodatafeilen fra forrige fase er dermed bekreftet rettet i produksjon, ikke
bare lokalt.

**Normalmodus med ekte OpenAI er bevisst IKKE aktivert i produksjon.**
`OPENAI_API_KEY` er ikke lagt inn i Vercel, nettopp for å beskytte gruppens
forhåndsbetalte OpenAI-kreditter mot at en offentlig, uinnlogget side kan bli brukt av
uvedkommende før et forbrukstak er satt hos OpenAI. Normalmodus med ekte KI-analyse er
testet grundig lokalt i tidligere økter (se seksjonene over), og kan testes lokalt med
egen API-nøkkel når som helst – den er ikke utestet, bare bevisst ikke eksponert
offentlig ennå.

### Oppsummering: demodata-feilen (se også forrige seksjon)

Etter første publisering viste demomodus feilmeldingen "Kunne ikke laste demodata."
Årsaken var at `test-data/`-mappen lå utenfor `backend/`-tjenestens rot, og derfor ikke
ble inkludert i Vercel sin Python-funksjonsbunt. Feilen ble oppdaget ved manuell testing
i produksjon rett etter publisering, rettet ved å flytte mappen inn i
`backend/test-data/` og justere én filsti i `demo_data.py`, dekket av en ny
regresjonstest, og er nå bekreftet rettet ved en ny, manuell test av den publiserte
siden (se "Manuell bekreftelse" over).

### Kritisk refleksjon: lokal testing vs. produksjon

Denne publiseringsrunden er et konkret eksempel på at lokal testing ikke fanger opp
alle feil en reell driftsplattform kan introdusere: alle 78 backend-testene og alle
manuelle lokale forsøk fungerte fint, fordi de kjører med hele repoet samlet på disk.
Først da applikasjonen faktisk kjørte som en isolert, bundlet Vercel-funksjon, ble det
synlig at en antakelse i koden (at `test-data/` alltid ligger tilgjengelig relativt til
repo-roten) ikke holdt i en serverless produksjonsplattform. Lærdommen tas med videre:
en automatisert test kan bekrefte at koden gjør det den skal *i det miljøet den kjører
i* – den kan ikke alene bevise at den fungerer i et annet, strukturelt forskjellig
miljø (som en serverless funksjon med et begrenset filsystem). Manuell testing direkte
mot den publiserte applikasjonen var derfor nødvendig, ikke bare en formalitet.

### KI-bruk og kritisk vurdering

- Claude Code ble brukt til å dokumentere status, ikke til å gjøre nye kodeendringer –
  ingen avvik mellom dokumentert og faktisk oppførsel ble funnet ved gjennomgang av
  `architecture.md`, så den ble latt uendret.
- Claude Code ble instruert om ikke å legge inn `OPENAI_API_KEY` i Vercel selv, og ikke
  å gjøre ekte API-kall – dette forblir en bevisst, manuell beslutning hos gruppen.

### Neste steg

1. Sette et forbrukstak/budsjettgrense for API-nøkkelen hos OpenAI.
2. Deretter legge `OPENAI_API_KEY` inn på Production-miljøet i Vercel, for å aktivere
   normalmodus i produksjon.
3. Gjøre én bevisst, villet ekte testforespørsel mot normalmodus i produksjon etterpå,
   for å bekrefte hele kjeden der.


## 06.11.2026 – Kontrollert produksjonstest av normalmodus med ekte OpenAI

### Forberedelser hos OpenAI (sikkerhetstiltak før testen)

- API-saldoen før testen var **$4,98**.
- Automatisk påfyll av saldo var deaktivert.
- Organisasjonens månedlige forbruksgrense ble redusert fra $100 til **$3**, for å
  begrense det maksimale tapet dersom noe skulle gå galt under den korte perioden
  nøkkelen var aktiv i produksjon.
- "Enforce a hard limit" ble aktivert og bekreftet hos OpenAI.
- OpenAI advarer selv om at grensen i praksis kan overskrides litt (håndheving av
  harde grenser er ikke alltid helt eksakt i sanntid) – dette ble tatt til
  etterretning som en kjent, akseptert restrisiko for denne korte, kontrollerte
  testen.

### Gjennomføring i Vercel

1. `OPENAI_API_KEY` ble lagt inn i Vercel som en **Secret**, kun for
   **Production**-miljøet.
2. En ny produksjonspublisering ble gjort og fikk status **Ready**.
3. Normalmodus ble testet direkte på **https://g02-amundsen.vercel.app/**, med en
   fiktiv CV og stillingsannonse (se testresultat under). Analysen fungerte, og
   resultatet ble vist korrekt i nettleseren.
4. Umiddelbart etter testen ble `OPENAI_API_KEY` **slettet** fra Vercel igjen.
5. En ny publisering uten den konfigurerte nøkkelen ble gjort, og fikk status
   **Ready** og **Current** – normalmodus er dermed deaktivert i produksjon igjen,
   på samme måte som før testen.

### Kjent, åpen sikkerhetsrisiko

Den opprinnelige OpenAI API-nøkkelen som ble brukt i testen er **ikke tilbakekalt
(revoked)** hos OpenAI. Selv om nøkkelen er fjernet fra det nåværende Vercel-miljøet,
kan **eldre Vercel-deployments** (tidligere bygg som ble laget mens nøkkelen var
konfigurert) i prinsippet fortsatt ha tilgang til den, siden miljøvariabler i Vercel
er bakt inn i det enkelte bygget på byggetidspunktet. Dette er en reell, uløst
sikkerhetsrisiko, og føres som et eget, åpent punkt (se `issues.md`). Risikoen
reduseres i praksis av det lave forbrukstaket ($3) og at auto-påfyll er deaktivert,
men den fjernes ikke før nøkkelen faktisk tilbakekalles/roteres hos OpenAI.

### Testresultat

**Fiktiv kandidat:** Emma Hansen. **Fiktiv arbeidsgiver:** Fjord Analyse AS.
**Stilling:** Junior analytiker.

Resultatet fra den ekte analysen inneholdt:
- 6 identifiserte stillingskrav
- 5 relevante styrker
- 5 kompetansegap
- 4 forslag til CV-tilpasning
- Et generert søknadsutkast

**Kvalitetskontroll:**
- Bachelorgrad og Excel-erfaring ble riktig identifisert som dokumenterte styrker.
- SQL og Power BI ble korrekt vurdert som **ikke** dokumenterte ferdigheter
  (kompetansegap) – samme korrekte oppførsel som ble bekreftet i de tidligere, lokale
  testrundene (05.11.2026).
- Styrkene hadde relevante, sporbare kildeutdrag.
- Søknadsutkastet diktet ikke opp SQL- eller Power BI-erfaring – ingen oppdiktede
  kvalifikasjoner ble funnet (FR10 holder).

**To mindre kvalitetsbegrensninger:**
1. En språklig feil i resultatet (en seksjon ble omtalt som "språkendelig seksjon" –
   et uklart/feilformulert uttrykk fra språkmodellen).
2. Søknadsutkastet var igjen ganske generelt formulert – samme kjente begrensning som
   ble notert etter den lokale ende-til-ende-testen 05.11.2026, nå bekreftet å gjelde
   også i produksjon.

### Kritisk refleksjon

Denne testen bekrefter at hele den ekte kjeden – frontend på Vercel → Services-ruting
→ FastAPI-backend → OpenAI → grunnlagskontroll → visning i nettleseren – fungerer i en
reell produksjonsplattform, ikke bare lokalt. Samtidig viser testen at det å aktivere
en ekte, betalt integrasjon midlertidig i produksjon introduserer en ny type risiko
som ikke fantes mens nøkkelen kun lå lokalt: en API-nøkkel som har vært konfigurert i
et Vercel-miljø kan leve videre i tidligere bygg selv etter at den er fjernet fra
gjeldende konfigurasjon. Å fjerne en miljøvariabel er derfor ikke det samme som å
trekke tilbake tilgangen til den – kun selve nøkkelen (hos leverandøren) kan gjøre
det. Lærdommen tas med videre: en "slett nøkkelen fra Vercel"-rutine er ikke
tilstrekkelig i seg selv for å stenge tilgangen fullstendig; en fullverdig
sikkerhetsrutine må inkludere at nøkkelen tilbakekalles/roteres hos leverandøren når
en midlertidig eksponering avsluttes.

### Status

Normalmodus er bekreftet fungerende i produksjon gjennom en kontrollert, tidsavgrenset
test, men er **deaktivert** igjen i den nåværende produksjonskonfigurasjonen. Den
opprinnelige nøkkelen står fortsatt som et åpent, dokumentert sikkerhetspunkt til den
tilbakekalles hos OpenAI.


## 06.11.2026 – Manuell kvalitetssikring mot tre nye fiktive testsett (ekte OpenAI)

### Gjennomføring

Kjørte normalmodus lokalt (`uv run uvicorn app.main:app`, egen `backend/.env`) mot
testsett 2–4 i `backend/test-data/manual-qa/`, ett ekte `POST /api/analyze`-kall per
sett (3 kall totalt, ingen retries). Forventningene var låst og committet (commit
`75df966`) før noe av disse tre kallene ble gjort. Rå JSON-svar og en skriftlig
vurdering er lagret i hvert testsetts mappe (`resultat-2026-11-06.json` og
`vurdering-2026-11-06.md`).

### Resultater

| Testsett | Kandidat | Utfall |
|---|---|---|
| 2 | Markus Eide (tydelige kompetansegap) | Bestått med mindre avvik |
| 3 | Sara Lund (overførbar deltidserfaring) | Bestått, uten avvik av betydning |
| 4 | Thomas Berg (uklare kvalifikasjoner) | **Avvik funnet** |

**Felles, positivt funn for alle tre:** ingen av «må aldri påstås»-listene ble
brutt i fri tekst (styrkebeskrivelser eller søknadsutkast) – søknadsutkastene diktet
ikke opp SQL, Python, Power BI, et CRM-system, et tredje fremmedspråk, Jira, Trello
eller Excel. Alle kildesitater i alle tre svar ble kontrollert manuelt mot CV-en og
stillingsannonsen, og var uten unntak ekte og ordrette.

**Testsett 2 (Markus Eide):** to sentrale/ønskelige krav (interesse for data;
kommunikasjon/presentasjon) ble ikke tydelig koblet til en bekreftet styrke, og ett
krav (statistikk/metode) som var forventet som gap ble i stedet koblet til en
kundetilfredshetsundersøkelse – et ekte sitat, men et i overkant velvillig skjønn.

**Testsett 3 (Sara Lund):** den bevisste gråsonen (saksbehandlingssystem vs.
CRM-system) ble håndtert eksemplarisk – verken overdrevet eller ignorert, men
presentert som et korrekt, betinget forslag.

**Testsett 4 (Thomas Berg) – bekreftet avvik:** en styrke beskrevet som "Har
erfaring med digitale verktøy i daglig arbeid" (ekte, ordrett sitat) ble koblet via
`related_requirement_ids` til kravet "Erfaring med prosjektstyringsverktøy som Jira
eller Trello" – nøyaktig den sammenblandingen testsettet var designet for å avdekke.
Årsaken ble undersøkt i koden: modellen satte `job_ad_excerpt` til nøyaktig samme
tekst som selve kravbeskrivelsen, noe som gjør `grounding.py` sin
nøkkelord-overlapp-kontroll selvreferensiell og dermed virkningsløs for dette
tilfellet – den kontrollerer aldri CV-sitatet isolert mot kravet. Samme krav opptrer
også selvmotsigende, både som bekreftet gap og som koblet styrke, i samme svar.

**Gjennomgående mønster (testsett 2 og 4):** reelt, allerede dokumentert CV-innhold
ble i flere tilfeller ikke anerkjent som en bekreftet styrke, og endte i stedet som
et "forslag om å fremheve" – ikke en sikkerhetsfeil, men en kvalitetssvakhet verdt å
følge med på.

### Kritisk vurdering

Dette er nøyaktig den typen funn den fjerde testsett-arketypen («uklare
kvalifikasjoner») skulle avdekke, og bekrefter verdien av å ha bygget flere,
varierte testsett i stedet for å stole på ett. Funnet i testsett 4 er en reell,
presis identifisert svakhet i `grounding.py` – ikke i selve språkmodellkallet eller
prompten – og peker på en konkret, avgrenset kodeendring (stram inn
`_filter_related_requirement_ids` slik at den ikke kan bekrefte seg selv via et
`job_ad_excerpt` som gjentar kravteksten). Denne endringen er **ikke gjort** i denne
økten, i tråd med instruksen om ikke å endre applikasjonskode under selve testingen.

### Status

Tre av tre planlagte ekte kall er brukt (grensen på tre uten ny godkjenning). Ett
bekreftet avvik i `grounding.py` er identifisert og dokumentert, med en konkret,
avgrenset anbefalt fiks som ikke er implementert. Testsett 1 (Kari Nordmann) er ikke
kjørt denne runden, siden det gjenbruker det eksisterende, allerede validerte
demotestsettet.


## 06.11.2026 – Målrettet retting av krav-koblingsfeilen fra testsett 4

### Feilen og årsaken

Som dokumentert i forrige seksjon: en styrke om "digitale verktøy" (ekte,
ordrett sitert fra CV-en) ble i testsett 4 (Thomas Berg) koblet via
`related_requirement_ids` til et spesifikt krav om "prosjektstyringsverktøy
som Jira eller Trello", selv om CV-en ikke navngir noe slikt verktøy.

Årsaken ble bekreftet i koden (ikke gjettet): `_filter_related_requirement_ids`
i `backend/app/grounding.py` kontrollerte om kravets beskrivelse delte et
"betydningsfullt" nøkkelord med funnets egen påstand OG BÅDE `cv_excerpt` OG
`job_ad_excerpt` samlet. Språkmodellen hadde satt `job_ad_excerpt` til
nøyaktig samme tekst som kravets egen beskrivelse – da "deler" kravet
nødvendigvis nøkkelord med seg selv, helt uavhengig av om `cv_excerpt`
("digitale verktøy") faktisk har noe å gjøre med kravet ("Jira eller
Trello"). Kontrollen var dermed selvbekreftende i dette tilfellet.

### Rettingen

Minst mulig, målrettet endring: `job_ad_excerpt` er fjernet fra
sammenligningsgrunnlaget i `_filter_related_requirement_ids`. Kun funnets
egen påstand og dets faktiske CV-dokumentasjon (`cv_excerpt`) avgjør nå om en
krav-kobling beholdes. Selve sitatkontrollen (at `cv_excerpt`/`job_ad_excerpt`
må finnes ordrett i riktig kildetekst) er **uendret**.

### Testing

- Ny regresjonstest (`test_strength_followup_fix_job_ad_excerpt_cannot_self_confirm_requirement_link`)
  gjenskaper testsett 4-tilfellet nøyaktig. Bekreftet at den **feilet før
  rettingen** (koblingen ble feilaktig beholdt) og **består etter** (koblingen
  fjernes, styrken selv forblir gyldig).
- To nye regresjonstester bekrefter at legitime koblinger fortsatt fungerer
  uten at `job_ad_excerpt` trengs: et kort, presist fagord ("SQL") og
  overførbar erfaring (kundeservice fra deltidsjobb) – begge kobles korrekt
  via `cv_excerpt` alene, uavhengig av om et urelatert `job_ad_excerpt` er
  satt.
- Full backend-testsuite: **81 av 81 bestått** (opp fra 78 – de tre nye
  testene). Ingen eksisterende tester ble endret eller fjernet; den tidligere
  dokumenterte, aksepterte begrensningen (kundeservice/opplæring vs.
  "kommunikasjonsevner", uten delt ordforråd) er fortsatt dekket av sin egen
  test og uendret i oppførsel.
- Ingen ekte OpenAI-kall ble gjort. Ingen endring av modell, prompts, Vercel
  eller de forhåndsdefinerte testforventningene i `backend/test-data/manual-qa/`.

### Status

Avviket fra testsett 4 er rettet med en minimal, godt avgrenset endring, og
dekket av en regresjonstest som beviselig fanger opp nøyaktig denne
feilklassen. De to øvrige, mindre funnene fra samme testrunde (mangelfull
anerkjennelse av enkelte reelle styrker i testsett 2 og 4) er fortsatt åpne
og ikke del av denne rettingen.

## 06.11.2026 – Reell brukertest i lokal normalmodus (anonymisert CV, Statnett-annonse)

### Gjennomføringen

Brukeren gjennomførte en reell test av normalmodus lokalt, med en
anonymisert, ekte CV og en ekte stillingsannonse fra Statnett (rådgiver/
seniorrådgiver økonomi og kostnadsoptimalisering). Selve CV-en og
stillingsannonsen er, som alltid, ikke lagret noe sted i repositoriet
(NFR3) – kun de funnene som ble rapportert, er dokumentert her, uten
personopplysninger.

Søknadsutkastet inneholdt ingen tydelig oppdiktet erfaring – selve
hallusinasjonskontrollen fungerte altså som tiltenkt denne gangen. Tre mer
spesifikke kvalitetsproblemer ble funnet:

1. En styrke om generell arbeidskapasitet og evne til å håndtere flere
   oppgaver/tidsfrister ble koblet (via `related_requirement_ids`) til et
   spesifikt fagkrav om IT-økonomistyring og analyse av store datamengder –
   en faglig svak kobling mellom en generell personlig egenskap og et
   konkret fagkrav.
2. Et sammensatt krav (IT-kostnadsmodeller, lisensforvaltning, analyse av
   store datamengder) ble ikke tydelig fanget opp som manglende
   dokumentasjon i CV-en – ingen av disse spesifikke, udokumenterte delene
   ble presentert som egne kompetansegap.
3. Et mastergrad-krav ble identifisert som et kompetansegap, men
   stillingsannonsen åpnet selv for at relevant erfaring kunne kompensere
   for en manglende mastergrad. Denne nyansen gikk tapt i resultatet.

### Undersøkelse og årsak

Funn 1 er, i likhet med de tidligere feilkoblingene (se forrige seksjoner),
en svakhet i den deterministiske nøkkelord-heuristikken i
`backend/app/grounding.py`. Siden rå-svaret fra språkmodellen bevisst ikke
logges (NFR3), er det ikke mulig å fastslå det eksakte delte ordet med
100 % sikkerhet. Det som ER bekreftet ved å kjøre koden direkte: heuristikken
talte fortsatt flere brede, generiske ord om personlig kapasitet/mengde
(bl.a. "stor"/"store", "håndtere", "tidsfrister") som et gyldig tematisk
treff, uavhengig av fagområde – nøyaktig den typen svakhet som kan forklare
at en helt generell styrke matchet et helt spesifikt, teknisk krav.

Funn 2 og 3 kan derimot IKKE rettes i `grounding.py`: modulen luker bare bort
feilaktige koblinger og ugrunnede sitater i et svar som allerede er
mottatt – den kan ikke få modellen til å nevne noe den har utelatt helt
(funn 2), eller til å beholde en nyanse den har glattet over (funn 3).
Begge er egenskaper ved selve språkmodell-svaret, og kan derfor kun
adresseres i prompten (`backend/app/prompts.py`).

### Endringene

- **`backend/app/grounding.py`**: `_GENERIC_WORDS` er utvidet med ord om
  personlig kapasitet/arbeidsmengde ("stor", "store", "flere", "håndtere",
  "håndtering", "håndterer", "kapasitet", "tidsfrist", "tidsfrister",
  "mengde", "mengder", "samtidig"), slik at disse ikke lenger kan utløse en
  krav-kobling på egen hånd. Minimal endring, samme prinsipp som tidligere
  utvidelser av samme liste.
- **`backend/app/prompts.py`**: to nye regler (9 og 10) i systemprompten.
  Regel 9 ber modellen vurdere hvert krav for seg, og presentere hver
  spesifikke, udokumenterte del av et sammensatt krav som et eget
  kompetansegap – ikke utelate eller dekke det vagt. Regel 10 ber modellen
  ta med en eventuell "kan kompenseres av relevant erfaring"-nyanse fra
  stillingsannonsen i kravets og/eller gapets beskrivelse, i stedet for å
  fremstille kravet som absolutt.

### Testing og kvalitetssikring

- Ny regresjonstest (`test_strength_real_user_test_case_generic_capacity_is_not_linked_to_specific_requirement`)
  gjenskaper funn 1 med syntetisk, oppdiktet CV-/annonsetekst (ikke den
  virkelige CV-en). Bekreftet manuelt at testen **feilet før** utvidelsen av
  `_GENERIC_WORDS` (koblingen ble feilaktig beholdt) og **består etter**.
  En egen, direkte test av `_shares_relevant_keyword` dekker samme
  rotårsak uten omveien via `enforce_grounding`.
- Full backend-testsuite: **83 av 83 bestått** (opp fra 81 – de to nye
  testene). Frontend-testsuiten: **23 av 23 bestått** (uendret, ingen
  frontend-endringer i denne rettingen).
- Ingen nye OpenAI-kall ble gjort i denne økten, og ingen betalt tjeneste ble
  brukt.

### Kritisk vurdering – hva som IKKE kan garanteres uten en ny KI-test

Rettingen av funn 1 (`grounding.py`) er deterministisk og bevist med en
regresjonstest, på samme måte som tidligere rettinger i denne modulen.

Rettingen av funn 2 og 3 (nye regler i `prompts.py`) er derimot **ikke**
verifisert mot et nytt, ekte OpenAI-kall i denne økten, fordi oppgaven
eksplisitt forbød nye API-kall. Det kan derfor IKKE garanteres at
språkmodellen faktisk følger de to nye reglene bedre enn før – kun at
reglene er lagt til, er språklig presise, og er direkte motivert av de
konkrete funnene over. Dette må bekreftes med en ny, reell test i
normalmodus (lokalt, med en betalt API-nøkkel) før man kan si noe sikkert om
effekten. Dette er bevisst dokumentert som en åpen begrensning, ikke
underslått.

### Status

Funn 1 er rettet og bevist med en regresjonstest. Funn 2 og 3 er adressert
med målrettede, begrunnede promptendringer, men virkningen av disse er
ubekreftet til en ny, reell KI-test er kjørt. Ingen eksisterende
funksjonalitet eller sporbarhet er endret – kun `_GENERIC_WORDS` og
systemprompten er utvidet.

## 06.11.2026 – Oppfølgende reell brukertest: samme CV/annonse, etter forrige retting

### Gjennomføringen

Brukeren testet lokal normalmodus på nytt med samme anonymiserte CV og
Statnett-annonse som i forrige runde, nå etter forrige kvalitetsforbedring.
Den tidligere feilaktige koblingen mellom generell arbeidskapasitet og
IT-økonomistyring under «Relevante styrker» var borte – den rettingen
fungerte altså i et ekte, nytt svar, ikke bare i regresjonstesten. Tre nye
svakheter ble funnet:

1. Under «Forslag til CV-tilpasning» ble erfaring med å kombinere
   fulltidsjobb og studier koblet til kravet om analyse av store
   datamengder – en faglig ikke-holdbar kobling.
2. Analysen viste fortsatt bare manglende mastergrad som kompetansegap,
   selv om CV-en heller ikke dokumenterte erfaring med IT-controlling,
   lisensforvaltning, IT-kostnadsmodeller eller analyse av store
   datamengder.
3. Erfaring med fulltidsjobb og studier ble koblet til muligheten for at
   relevant erfaring kan kompensere for mastergrad – også en svak kobling.

### Undersøkelse og årsak

**Funn 1** er samme feilfamilie som tidligere, nå i CV-forslag
(`CvSuggestion`) i stedet for styrker. Årsaken ble bekreftet i koden: i
`_filter_related_requirement_ids` (`backend/app/grounding.py`) inkluderte
sammenligningsgrunnlaget forslagets EGEN fritekst (`suggestion`-feltet).
Et forslag begrunner ofte seg selv med stillingsannonsens egne, spesifikke
fagord («... siden stillingen krever analyse av store datamengder»), helt
uavhengig av om det faktiske CV-innholdet forslaget peker på har noe med
dette å gjøre – samme grunnleggende svakhet som gjorde at `job_ad_excerpt`
ble fjernet fra grunnlaget i en tidligere runde, nå i et nytt felt.

**Funn 2** kan ikke rettes i `grounding.py` (den luker bare ut feil i et
allerede mottatt svar). Siden rå-modellsvar ikke logges (NFR3), kan ikke
den eksakte årsaken bekreftes, men den mest nærliggende forklaringen,
sammenholdt med funn 1 i samme svar: det (feilaktige) CV-forslaget var
koblet til nøyaktig det samme IT-kravet som skulle vært et eget
kompetansegap. Det er nærliggende at modellen, når den "ser" et krav som
adressert av ETT funn (uansett hvor svakt), ikke også oppretter et eget
kompetansegap for samme krav. Forrige økts regel 9 ba modellen vurdere hver
navngitte del av et sammensatt krav for seg, men sa ikke eksplisitt at dette
gjelder uavhengig av om kravet allerede er (svakt) koblet et annet sted.

**Funn 3** er en beslektet, men egen svakhet: en generell, udokumentert
egenskap (å kombinere jobb og studier) ble brukt som om den i seg selv var
den "relevante erfaringen" som kunne kompensere for et fagspesifikt
mastergrad-krav – uten at egenskapen faktisk er relevant for kravets eget
fagområde (økonomi/IT). Dette er en innholdsmessig/resonnementsmessig
svakhet i selve svaret, ikke noe en deterministisk sitatkontroll kan avgjøre.

### Endringene

- **`backend/app/grounding.py`**: `_filter_related_requirement_ids` bruker
  nå KUN `cv_excerpt` (ikke forslagsteksten) som grunnlag for CV-forslagets
  krav-koblinger – en direkte utvidelse av det samme prinsippet som
  tidligere fjernet `job_ad_excerpt` fra grunnlaget. Styrker og
  kompetansegap er IKKE endret (ingen tilsvarende feil funnet for styrker
  denne runden, og kompetansegap har aldri noe `cv_excerpt` å falle tilbake
  på).
- **`backend/app/prompts.py`**: regel 9 er omskrevet til å si eksplisitt at
  et sammensatt krav skal brytes ned i de navngitte delene, og hver del
  vurderes for seg. Ny regel 11 sier at en svak/indirekte krav-kobling
  ALDRI fritar fra plikten i regel 9 – et krav kan ha både en relatert
  styrke/forslag OG et eget kompetansegap samtidig. Ny regel 12 presiserer
  at en "kan kompenseres av relevant erfaring"-nyanse (regel 10) ikke kan
  oppfylles av en generell, udokumentert egenskap – kompenserende erfaring
  må være relevant for kravets eget fagområde.

### Testing og kvalitetssikring

- Ny regresjonstest (`test_suggestion_own_text_cannot_self_confirm_requirement_link`)
  gjenskaper funn 1 med syntetisk, oppdiktet CV-/annonsetekst. Bekreftet
  manuelt at testen **feilet før** endringen (koblingen ble feilaktig
  beholdt) og **består etter**.
- Ny regresjonstest (`test_suggestion_related_requirement_link_survives_via_relevant_cv_excerpt`)
  bekrefter at en legitim CV-forslag-kobling fortsatt fungerer når det er
  det faktiske CV-sitatet (ikke forslagsteksten) som deler et presist
  fagord med kravet.
- Full backend-testsuite: **85 av 85 bestått** (opp fra 83 – de to nye
  testene). Frontend-testsuiten: **23 av 23 bestått** (uendret).
- Ingen nye OpenAI-kall. Ingen ekte CV, personopplysninger eller
  stillingsannonsetekst er lagt i repoet – kun syntetisk, oppdiktet
  eksempeltekst i testfilen.

### Kritisk vurdering – hva som er bevist, og hva som fortsatt er usikkert

**Bevist, deterministisk:** fiksen for funn 1 i `grounding.py`. Dette er
verifisert med fail-before/pass-after på samme måte som alle tidligere
rettinger i denne modulen – testen feiler garantert uten endringen og
består garantert med den, uavhengig av hva en språkmodell gjør i neste
ekte kall.

**IKKE bevist, kun begrunnet:** promptendringene for funn 2 og 3 (regel 9
omskrevet, regel 11 og 12 nye). Disse er IKKE testet mot et nytt, ekte
OpenAI-kall i denne økten, fordi oppgaven eksplisitt forbød dette. At den
tidligere regel 9 (fra forrige økt) beviselig IKKE løste funn 2 i et ekte
svar, er i seg selv et konkret datapunkt om at promptjusteringer alene ikke
kan garanteres å fungere – kun observeres i etterkant, med en ny reell test.
Det kan derfor ikke, og skal ikke, påstås at de nye promptreglene faktisk
løser funn 2 og 3 før en slik test er kjørt.

### Status

Funn 1 (CV-forslag koblet til urelatert fagkrav) er rettet og bevist med en
regresjonstest, som en direkte utvidelse av den tidligere styrke-fiksen til
CV-forslag. Funn 2 og 3 er adressert med mer konkrete, begrunnede
promptregler, men – i tråd med erfaringen fra forrige runde, der regel 9
beviselig ikke løste funn 2 i praksis – er det eksplisitt IKKE påstått at
disse nye reglene faktisk virker mot en ekte språkmodell. Dette gjenstår å
bekrefte med en ny, reell test.

## 06.11.2026 – Tredje reelle Statnett-test (etter siste grounding-/promptforbedringer)

### Gjennomføringen

Brukeren gjennomførte en tredje reell test av normalmodus lokalt, med samme
anonymiserte CV og samme Statnett-stillingsannonse som de to foregående
testene denne dagen – nå etter at både grounding-fiksen for CV-forslag
(`backend/app/grounding.py`) og de omskrevne/nye promptreglene 9, 11 og 12
(`backend/app/prompts.py`) var på plass. Dette er den tredje og siste
reelle API-testen i prosjektperioden mot nøyaktig dette CV-/annonseparet.

### Hva som faktisk ble observert

**Bekreftet forbedring (sammenlignet med forrige test):**
- Den tidligere feilaktige koblingen mellom generell arbeidskapasitet og
  analyse av store datamengder var borte. Dette er den ENE promptrelaterte
  endringen fra forrige runde som nå er bekreftet å faktisk ha effekt i et
  ekte svar, ikke bare i en regresjonstest.

**I hovedsak positivt, men ikke en garanti om perfeksjon:**
- Styrkene knyttet til økonomi, budsjett, offentlige anskaffelser og
  kommunikasjon var i hovedsak relevante.
- To CV-forslag var forsiktig formulert og støttet av CV-innholdet.
- Søknadsutkastet var sammenhengende og inneholdt ingen åpenbare oppdiktede
  kvalifikasjoner.

**Fortsatt en reell, ubekreftet-løst begrensning:**
- Kompetansegapene var fortsatt ufullstendige: kun manglende mastergrad ble
  identifisert, mens IT-controlling, IT-drift/lisenser, analyse av store
  datamengder og andre udokumenterte kvalifikasjoner IKKE kom frem som egne
  gap. Dette er nøyaktig funn 2 fra forrige test, og det er dermed nå
  bekreftet, over tre reelle tester i rad, at verken den opprinnelige regel
  9, eller den omskrevne regel 9 + nye regel 11, har løst dette i praksis.
  **Det skal derfor ikke påstås at kompetansegap-problemet er løst** – kun
  at én annen, beslektet feil (funn 1 fra forrige test) er borte.

**Nye, mindre presise funn (samme grunnleggende svakhetsklasse, nye konkrete utslag):**
- Enkelte styrkebeskrivelser var fortsatt noe for bastante – f.eks. ble
  presentasjon av løsninger fremstilt som erfaring med analyser, en noe for
  sterk tolkning av det CV-en faktisk dokumenterer.
- Bachelorutdanning ble koblet som en relevant styrke til mastergrad-kravet,
  samtidig som manglende mastergrad korrekt sto oppført som et eget
  kompetansegap. Dette er ikke nødvendigvis feil i seg selv (en bachelor ER
  relevant bakgrunn for et krav der mastergrad er ønskelig), men resultatet
  fremstår som et motstridende signal i samme svar, uten at noen eksplisitt
  nyanse forklarer forholdet mellom de to.

### Kritisk vurdering – hva er observert, hva er fortsatt usikkert

**Faktisk observert, i dette ene ekte svaret:** alle punktene over. Dette er
ett (det tredje) datapunkt mot ett og samme CV-/annonsepar, ikke en
statistisk bekreftelse mot en bredere populasjon av CV-er/annonser. Som i
alle tidligere runder logges ikke rå-modellsvar (NFR3), så ingenting av
dette kan etterprøves i detalj senere – kun det brukeren selv rapporterte,
er grunnlaget for denne seksjonen.

**Bekreftet, med rimelig sikkerhet:** grounding-fiksen for CV-forslag
(forrige runde) hadde den tiltenkte effekten i et ekte svar.

**IKKE bekreftet, og skal ikke påstås bekreftet:** at regel 9/11 (sammensatte
krav skal brytes ned og gap skal opprettes uavhengig av svake koblinger
andre steder) faktisk endrer modellens oppførsel for kompetansegap. Tre
reelle tester i rad har nå vist samme mangel. Det mest sannsynlige, men
ikke bekreftbare, er at dette krever en annen type tiltak enn
prompt-presisering alene (f.eks. en strukturert, trinnvis kravsjekk i
prompten, eller en helt annen tilnærming) – men det er en hypotese for en
eventuell senere versjon, ikke noe som utredes eller implementeres nå (se
beslutning under).

### Beslutning: videre funksjonsutvikling avsluttes her

Etter denne tredje reelle testen avsluttes videre funksjonell utvikling av
analyselogikken (prompt og grounding) for denne prosjektleveransen. Dette
er en bevisst beslutning, ikke en konsekvens av tidsnød alene, og
begrunnes med:

- **Kjernefunksjonaliteten fungerer.** Alle FR1–FR12 i `prd.md` er
  implementert og verifisert (automatisert testdekning + fire manuelle
  testsett + tre reelle produksjonsnære tester), og de mest alvorlige,
  konkrete feilene som ble funnet underveis (feilaktige krav-koblinger,
  forsvinnende SQL-gap, selvbekreftende sitater) er rettet og dekket av
  regresjonstester.
- **De kjente begrensningene er forstått og dokumentert**, ikke oversett:
  nøkkelord-heuristikkens grunnleggende grense (kan ikke skille perfekt
  mellom "åpenbart feilkoblet" og "reelt relatert med andre ord"), og at
  modellen – over tre reelle tester – konsekvent underrapporterer
  kompetansegap for sammensatte, tekniske krav.
- **Videre promptjustering har ikke dokumentert sikker effekt.** Den
  forrige rundens regel 9/11/12 var en velbegrunnet, målrettet innsats, men
  løste beviselig IKKE hovedfunnet (manglende IT-relaterte kompetansegap) i
  praksis. Å fortsette å justere prompten ytterligere, uten en ny
  arbeidshypotese utover "presiser reglene enda mer", vurderes som lav
  sannsynlighet for å lønne seg innenfor gjenværende prosjekttid, og risikerer
  i stedet å introdusere nye, utestede regresjoner i en prompt som allerede
  er relativt omfattende.
- Dette er en v1-begrensning på linje med de som allerede er akseptert og
  dokumentert tidligere i denne loggen (f.eks. nøkkelord-heuristikkens grense
  for "kundeservice/opplæring" vs. "kommunikasjonsevner", akseptert
  05.11.2026) – ikke en skjult mangel, men en bevisst grense for hva v1
  leverer, synlig for både bruker og sensor i README, `issues.md` og her.

## 06.11.2026 – Manuell mobiltest av den publiserte applikasjonen

### Gjennomføring

Den publiserte applikasjonen (`https://g02-amundsen.vercel.app/`) ble åpnet i
Google Chrome, og mobilvisning ble simulert i Chrome DevTools ved 375 px
bredde (sammenlignbart med en vanlig smarttelefonskjerm).

### Observasjoner

- Startsiden, modusvalgene og forklaringene fremsto lesbare og tilpasset
  bredden.
- Demomodus ble kjørt og produserte analyseresultater.
- Resultatkort, kompetansegap, CV-forslag og søknadsutkast ble undersøkt
  visuelt.
- Søknadsutkastet var synlig i et redigerbart tekstfelt.
- Det ble ikke observert åpenbare overlapp eller avkuttet tekst i de
  kontrollerte områdene.

### Begrensninger ved denne testen

- Ingen full WCAG-kontrastmåling er utført.
- Ikke alle skjermstørrelser eller faktiske mobilenheter er testet – kun
  DevTools-simulering ved én bredde (375 px) i én nettleser.
- Ingen fullstendig skjermlesertest er utført.
- Normalmodus ble ikke testet i mobilvisning i denne runden (kun demomodus),
  siden normalmodus ikke er offentlig aktivert i produksjon (se tidligere
  seksjon "Vellykket publisering bekreftet, normalmodus bevisst holdt av i
  produksjon" og README).

Det skal ikke påstås at noe utover dette faktisk er testet.

## 06.11.2026 – Sluttstatus for applikasjonsdelen

Dette er den avsluttende statusen for Career Transition Assistant ved
slutten av applikasjonsdelen (70 %) av IBE160-prosjektet.

### Hva som faktisk er implementert

Alle funksjonelle krav FR1–FR12 og ikke-funksjonelle krav NFR1–NFR8 i
`prd.md` er implementert: innliming av CV og stillingsannonse som tekst,
analyse mot stillingskrav, identifisering av styrker og kompetansegap,
konkrete CV-forslag med sporbarhet til CV og/eller stillingsannonse, et
redigerbart førsteutkast til søknadsbrev, en demomodus uten API-nøkkel, og
en normalmodus mot en ekte språkmodell (OpenAI). Ingen lagring av CV,
stillingsannonse, analyse eller søknadsutkast skjer noe sted i koden.
Scope-grensene fra `product-brief.md`/`prd.md` ("Out for v1") er
respektert – ingen funksjon utenfor avgrenset scope er lagt til.

### Hvordan sensor kan teste løsningen

Se README.md, avsnittene "Forutsetninger" og "Kjøre applikasjonen lokalt":
demomodus (punkt 3) krever ingen API-nøkkel eller kostnad og kan testes
direkte, både lokalt og på den publiserte siden
(`https://g02-amundsen.vercel.app/`). Normalmodus (punkt 4) krever en egen
`OPENAI_API_KEY` i `backend/.env` og kan kun testes lokalt, siden den
bevisst ikke er aktivert i produksjon (se eget punkt under).

### Hva kvalitetssikringen har bekreftet

- Automatisert testsuite: backend **85/85 bestått** (`uv run pytest`),
  frontend **23/23 bestått** (`npm test`), begge kjørt på nytt og bekreftet
  i forbindelse med denne sluttkontrollen.
- `npm run lint` (ESLint): ingen feil.
- `npm run build` (produksjonsbygg): bygger uten feil.
- Fire fiktive, forhåndsdefinerte testsett (`backend/test-data/manual-qa/`)
  er kjørt mot ekte OpenAI-svar og vurdert mot forhåndsdefinerte
  forventninger.
- Tre reelle tester av normalmodus mot samme anonymiserte CV og
  Statnett-stillingsannonse (se de tre seksjonene over) har gradvis avdekket
  og rettet konkrete feil i grunnlagskontrollen (`grounding.py`), bekreftet
  med fail-before/pass-after-regresjonstester for hver av dem.
- En avgrenset manuell mobiltest (se forrige seksjon) fant ingen åpenbare
  visningsfeil i demomodus ved 375 px bredde, med de begrensningene som er
  dokumentert der.

### Kjente begrensninger som gjenstår

- **Kompetansegap for sammensatte, tekniske krav identifiseres ikke
  fullstendig.** Over tre reelle tester har analysen konsekvent fanget opp
  mastergrad-kravet som gap, men ikke alltid de øvrige, mer spesifikke
  tekniske kompetansene i samme stillingsannonse. Dette er IKKE løst, og
  skal ikke fremstilles som løst – se forrige seksjon for beslutningen om
  å avslutte videre promptjustering på dette punktet.
- Nøkkelord-heuristikken i `grounding.py` kan i noen tilfeller fjerne en
  reelt relevant, men annerledes formulert krav-kobling (akseptert
  begrensning, se `app/grounding.py` og `issues.md`).
- Normalmodus er ikke offentlig aktivert i produksjon på Vercel: v1 har
  ingen innlogging, og uten tilgangskontroll kan en offentlig, uinnlogget
  normalmodus i prinsippet brukes av uvedkommende til å tømme
  forhåndsbetalte OpenAI-kreditter. Se README, avsnittet "Publisering på
  Vercel", for full begrunnelse og status på API-nøkkelen som ble brukt i
  en tidligere, kontrollert produksjonstest.
- Mobilvisning er kun avgrenset manuelt testet (se forrige seksjon) – ingen
  WCAG-kontrastmåling, ingen test på faktiske mobilenheter, ingen
  skjermlesertest.
- Mindre, allerede dokumenterte kvalitetsfunn fra manuell QA (se
  `issues.md`) er aksepterte v1-begrensninger, ikke rettet.

### Hvorfor videre funksjonsutvikling bevisst er avsluttet

Som dokumentert i seksjonen "Tredje reelle Statnett-test" over:
kjernefunksjonaliteten fungerer og er testet, de kjente begrensningene er
forstått og dokumentert i stedet for oversett, og videre promptjustering
har over tre reelle tester IKKE dokumentert sikker effekt på det
gjenværende hovedfunnet (kompetansegap for sammensatte krav). Å fortsette å
justere prompten ytterligere uten en ny arbeidshypotese vurderes som lav
sannsynlighet for å lønne seg innenfor gjenværende prosjekttid, og risikerer
å introdusere nye, utestede regresjoner. Dette er en bevisst, begrunnet
beslutning – ikke en konsekvens av tidsnød alene.

### Refleksjonsrapporten

Refleksjonsrapporten er en separat del av eksamensarbeidet, utenfor denne
loggen og utenfor applikasjonsdelen (70 %) som denne sluttstatusen gjelder.

### Avsluttende presisering

Denne sluttstatusen påstår ikke at løsningen er feilfri, eller at alle
kompetansegap identifiseres korrekt. Den beskriver hva som faktisk er
implementert og verifisert, og hvilke konkrete, kjente begrensninger som
gjenstår – i tråd med prosjektets gjennomgående prinsipp om å dokumentere
reelle funn i stedet for en kunstig positiv fremstilling.