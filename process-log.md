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