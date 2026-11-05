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