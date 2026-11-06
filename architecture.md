# Architecture: Career Transition Assistant

## 1. Technology Stack

Første versjon bygges som en enkel webapplikasjon med separat frontend og backend.

### Frontend
- React
- Vite
- JavaScript
- NPM

Frontenden skal håndtere brukergrensesnittet, innliming av CV og stillingsannonse, visning av analyseresultater, CV-forslag og redigerbart søknadsutkast.

### Backend
- Python 3.12
- FastAPI
- uv

Backenden skal håndtere validering av input, kommunikasjon med språkmodell-API, strukturering av KI-svar og retur av resultater til frontenden.

### Kommunikasjon
Frontend og backend kommuniserer gjennom et REST-API med JSON.

### Utviklingsverktøy
- VS Code
- Claude Code
- Git og GitHub
- Docker brukes senere ved behov for reproduserbar lokal kjøring

### Begrunnelse
Stacken er valgt fordi den er vanlig, godt dokumentert og relativt enkel å utvikle og teste. Den følger også verktøyretningen i emnet, med JavaScript/Node.js på frontend og Python på backend.

## 2. Application Structure

Applikasjonen deles i tre hoveddeler:

### Frontend
Frontenden viser brukergrensesnittet og sender brukerens input til backenden.

Den skal blant annet håndtere:
- innliming av CV
- innliming av stillingsannonse
- valg mellom normal modus og demomodus
- visning av styrker og kompetansegap
- visning av CV-forslag
- visning av sporbarhet mellom forslag, CV og stillingsannonse
- visning og redigering av søknadsutkast
- feilmeldinger og status mens analysen pågår

### Backend
Backenden mottar og validerer input fra frontenden og håndterer applikasjonens logikk.

Den skal blant annet:
- kontrollere at nødvendig input er til stede
- bygge forespørsler til språkmodellen
- sende relevante data til språkmodell-API
- validere og strukturere KI-svar
- returnere resultatene til frontenden
- håndtere feil fra språkmodell-API
- støtte demomodus uten eksterne API-kall

### External Language Model API
I normal modus kommuniserer backenden med en ekstern språkmodell gjennom et API.

Språkmodellen brukes til:
- analyse av samsvar mellom CV og stillingsannonse
- identifisering av relevante styrker
- identifisering av kompetansegap
- forslag til CV-tilpasninger
- generering av søknadsutkast

Frontenden skal ikke kommunisere direkte med språkmodell-API-et. API-nøkkelen skal bare være tilgjengelig i backenden.

## 3. Language Model Integration

### Model Provider
Applikasjonen skal bruke én ekstern språkmodell gjennom et API i normal modus.

Valgt leverandør og modell: **OpenAI**, modellen **gpt-5.4-mini**, via den offisielle
Python-SDK-en (`openai`). Modellnavnet er konfigurerbart via miljøvariabelen
`OPENAI_MODEL` (se avsnitt 6), slik at det kan endres uten kodeendring.

Valget er basert på:
- kostnad (mini-variant av modellen)
- støtte for strukturert JSON-output direkte fra Pydantic-modeller («Structured
  Outputs»), som lar backenden gjenbruke `AnalysisResult` uendret som skjema
- god, offisiell dokumentasjon og en enkel, godt støttet Python-SDK
- mulighet for stabil testing: SDK-et har tydelige, dokumenterte feilklasser som kan
  mockes i automatiserte tester uten ekte, betalte API-kall

### Backend Integration
All kommunikasjon med språkmodellen skal skje fra backenden.

Backenden skal:
- hente API-nøkkel fra miljøvariabel
- bygge en kontrollert prompt basert på CV og stillingsannonse
- sende forespørselen til språkmodell-API-et
- motta svaret
- validere at svaret følger forventet struktur
- returnere et strukturert resultat til frontenden

API-nøkkelen skal ikke være tilgjengelig i frontend eller lagres i GitHub.

### Structured Output
Språkmodellen skal returnere et strukturert svar som kan behandles av applikasjonen.

Resultatet skal minst inneholde:
- relevante styrker
- kompetansegap
- sentrale krav fra stillingsannonsen
- forslag til CV-tilpasninger
- sporbarhet for de viktigste forslagene
- førsteutkast til søknadsbrev

Der det er mulig skal resultatet returneres som strukturert JSON i stedet for fri tekst.

### Grounding and Hallucination Control
Prompten skal tydelig instruere modellen om å kun bruke informasjon som finnes i brukerens CV og stillingsannonse.

Hvis nødvendig informasjon mangler, skal modellen si at informasjonen ikke finnes i input i stedet for å anta eller finne på erfaring, utdanning eller kvalifikasjoner.

Backenden skal i tillegg kontrollere at nødvendige felt finnes i KI-svaret før resultatet vises til brukeren.

## 4. Demo Mode

Demomodus skal gjøre det mulig å teste hovedflyten i applikasjonen uten ekstern språkmodell, API-nøkkel eller kostnad.

### Oppførsel
Når brukeren velger demomodus:
- brukes et fast, fiktivt CV-eksempel
- brukes en fast, fiktiv stillingsannonse
- returneres et ferdig eksempelresultat med samme struktur som et ekte KI-svar
- gjøres det ingen kall til ekstern språkmodell

### Formål
Demomodus skal:
- gjøre det mulig for sensor å teste applikasjonen uten egen API-nøkkel
- gjøre lokal kjøring enklere
- gi et stabilt eksempel som kan brukes i testing og demonstrasjon
- redusere avhengigheten av eksterne tjenester

### Teknisk løsning
Demodata og eksempelresultater skal lagres som lokale prosjektfiler.

Demomodus skal bruke samme frontend-komponenter og samme resultatstruktur som normal modus, slik at hovedflyten testes på en realistisk måte selv uten språkmodellkall.

## 5. Project Structure

Prosjektet skal organiseres slik at frontend, backend, dokumentasjon og testdata er tydelig skilt.

Faktisk struktur (oppdatert 06.11.2026 til å stemme med det ferdige prosjektet –
se avsnitt om `docs/`-mappen under):

```text
G02-amundsen/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── .env.example
│   └── package.json
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── test-data/
│   │   ├── demo-cv.txt
│   │   ├── demo-job-ad.txt
│   │   ├── demo-result.json
│   │   └── manual-qa/        (fiktive testsett for manuell KI-kvalitetssikring)
│   ├── .env.example
│   ├── pyproject.toml
│   └── uv.lock
│
├── .logs/<bruker>/           (sesjonslogger og issues.md, se README)
│
├── product-brief.md
├── tilbakemelding-product-brief.md
├── prd.md
├── architecture.md
├── epics-and-stories.md
├── process-log.md
│
├── CLAUDE.md
├── .gitignore
├── vercel.json
└── README.md
```

Planleggingsdokumentene ligger altså samlet på repo-roten, ikke i en egen
`docs/`-mappe som et tidligere utkast av dette avsnittet beskrev – det ble aldri
opprettet noen slik mappe. Det finnes heller ingen `.env.example` på selve
repo-roten; API-nøkler og annen lokal konfigurasjon er dokumentert separat for
frontend (`frontend/.env.example`) og backend (`backend/.env.example`), se
avsnitt 6.

### Prinsipper
- frontend og backend skal være tydelig separert
- testdata skal ligge samlet i egen mappe
- dokumentasjon skal være lett å finne
- API-nøkler og `.env` skal ikke lagres i repoet
- byggeartefakter, `node_modules`, virtuelle miljøer og midlertidige filer skal holdes utenfor Git med `.gitignore`

## 6. Local Development and Configuration

Applikasjonen skal kunne kjøres lokalt på en utviklingsmaskin.

### Frontend
Frontenden kjøres som en egen utviklingsserver gjennom Node.js og NPM.

Typisk oppstart:

```bash
cd frontend
npm install
npm run dev

```

### Backend
Backenden kjøres separat med Python og uv.

Typisk oppstart:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Environment Variables

Hemmeligheter og konfigurasjon som ikke skal ligge i GitHub lagres i en lokal `.env`-fil
i `backend/` (siden `uv run` kjøres med `backend/` som arbeidsmappe).

Repoet skal inneholde en `backend/.env.example`-fil som viser hvilke miljøvariabler som
kreves, uten ekte hemmeligheter.

Eksempel (`backend/.env.example`):

```
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4-mini
OPENAI_TIMEOUT_SECONDS=30
```

### Configuration Principles

- `.env` skal være inkludert i `.gitignore`
- ekte API-nøkler skal aldri committes
- applikasjonen skal kunne starte i demomodus uten API-nøkkel
- README skal senere inneholde eksakte oppstartskommandoer
- frontend og backend skal kunne startes separat under utvikling

### Docker

Docker skal ikke være et krav for første utviklingsfase.

Docker kan senere brukes dersom det gjør lokal kjøring og reproduksjon enklere, men løsningen skal først fungere uten Docker.

## 7. Testing and Quality Assurance

Testing skal brukes både for å kontrollere vanlig applikasjonslogikk og for å kvalitetssikre KI-genererte resultater.

### Automated Testing
Automatiserte tester skal brukes der resultatet kan forventes å være deterministisk.

Det gjelder blant annet:
- validering av manglende input
- struktur på backend-respons
- håndtering av ugyldige eller ufullstendige svar
- demomodus
- sentral backend-logikk

### Manual and AI Output Testing
KI-genererte resultater kan variere mellom kjøringer og skal derfor vurderes mot faste, fiktive testsett.

Testsettene skal inneholde:
- CV
- stillingsannonse
- forventede styrker
- forventede kompetansegap
- sentrale krav som analysen bør identifisere

### Quality Assurance
KI-generert kode skal gjennomgås og testes før den aksepteres.

Feil som oppdages i KI-generert kode skal dokumenteres i prosessloggen sammen med hvordan de ble rettet.

## 8. UX and Accessibility

Brukergrensesnittet skal være enkelt, tydelig og tilpasset brukere som ikke nødvendigvis har teknisk bakgrunn.

### UX Principles
- hovedflyten skal være lett å forstå uten forklaring
- brukeren skal tydelig se hvor CV og stillingsannonse skal limes inn
- det skal være tydelig når analysen pågår
- resultater skal presenteres i en logisk rekkefølge
- feilmeldinger skal være forståelige og konkrete
- tomtilstander skal forklare hva brukeren må gjøre videre

### Accessibility
Løsningen skal ta hensyn til grunnleggende universell utforming, blant annet:
- lesbar kontrast
- tydelige skjemaetiketter
- støtte for tastaturnavigasjon
- forståelig tekst og knapper
- responsivt grensesnitt for relevante skjermstørrelser

### UX Documentation
Det skal lages en enkel wireframe eller skisse av hovedflyten før implementering av frontend.

## 9. Security and Privacy

Løsningen skal behandle brukerdata på en enkel og bevisst måte.

### Data Handling
- CV og stillingsannonse skal bare brukes i den aktive økten
- data skal ikke lagres permanent i første versjon
- søknadsutkast og analyseresultater skal ikke lagres etter at økten avsluttes

### Secrets
- API-nøkler skal lagres lokalt i `.env`
- `.env` skal ikke pushes til GitHub
- `.env.example` skal kun inneholde navn på nødvendige variabler

### External API
I normal modus sendes nødvendig informasjon til språkmodellleverandøren gjennom API-et.

Brukeren skal ikke måtte opprette konto i applikasjonen.

### Privacy by Design
Første versjon skal bevisst unngå funksjoner som krever permanent lagring av personopplysninger.

## 10. Deployment (Vercel)

IBE160 bruker Vercel som offisiell publiseringsløsning, og grupperepoene er tilknyttet
Vercel-integrasjonen via GitHub.

> **Merk:** `backend/test-data/` (avsnitt 5) ligger bevisst inne i `backend/`, ikke på
> repo-roten. En Vercel Service bunter kun filer inne i sin egen `root`
> (`backend/`), så demodata utenfor denne mappen følger ikke med i produksjon – dette
> var årsaken til en reell feil ("Kunne ikke laste demodata") etter første
> publisering.

### Ett Vercel-prosjekt med Services

Frontend og backend publiseres som **ett Vercel-prosjekt**, ved hjelp av Vercel sin
**Services**-funksjon (beta). Oppsettet er definert i `vercel.json` i repo-roten:

- `frontend/` kjøres som en egen Vite-tjeneste (statisk bygg, auto-detektert).
- `backend/` kjøres som en egen Python/FastAPI-tjeneste (`app.main:app`, Vercel Function).
- Alle forespørsler til `/api/*` rutes til backend-tjenesten, resten rutes til frontend-tjenesten.

Siden begge tjenestene deler domene i produksjon, er det **ingen CORS-problematikk i
produksjon** – CORS-oppsettet i `backend/app/main.py` er kun nødvendig for lokal
utvikling, der frontend og backend kjører som separate utviklingsservere på hver sin
port (se avsnitt 6).

Alternativ løsning dersom Services (beta) skulle skape problemer: to separate
Vercel-prosjekter (ett for `frontend/`, ett for `backend/`), koblet sammen med Vercel
sin «Related Projects»-funksjon, og med produksjonsdomenet lagt til backendens
`allow_origins`.

### Hvordan frontend finner backend i produksjon

Frontenden velger adresse automatisk basert på om bygget er et utviklings- eller
produksjonsbygg (`import.meta.env.DEV`), ikke en miljøvariabel som må settes manuelt:

- **Lokalt** (`npm run dev`): kaller `http://127.0.0.1:8000` (backendens lokale adresse),
  som i dag.
- **I produksjon** (`npm run build`, kjørt av Vercel): kaller en relativ adresse
  (f.eks. `/api/analyze/demo`), som Vercel ruter til backend-tjenesten på samme domene.

`VITE_API_BASE_URL` finnes fortsatt som en eksplisitt overstyring (se
`frontend/.env.example`), men er ikke nødvendig å sette i produksjon.

### Miljøvariabler i produksjon

API-nøkkelen og annen konfigurasjon settes som **Vercel Environment Variables** i
Vercel-dashbordet (eller med `vercel env add`) – **aldri** i en fil som committes:

| Variabel | Miljø | Nødvendig? |
|---|---|---|
| `OPENAI_API_KEY` | Production | Ja, for at normalmodus skal fungere i produksjon |
| `OPENAI_MODEL` | Production | Nei – har standardverdi i koden (`gpt-5.4-mini`) |
| `OPENAI_TIMEOUT_SECONDS` | Production | Nei – har standardverdi i koden (`30`) |

**Anbefaling:** sett `OPENAI_API_KEY` kun på Production-miljøet, ikke på Preview.
Da fungerer demomodus på alle forhåndsvisnings-URL-er, mens normalmodus der svarer med
en tydelig 503-feilmelding ("ingen API-nøkkel") i stedet for å kunne bruke kreditter –
akkurat slik applikasjonen allerede er designet til å håndtere en manglende nøkkel.

### Hindre misbruk av API-kreditter

Siden v1 bevisst ikke har innlogging, kan hvem som helst med lenken bruke normalmodus.
Det viktigste forsvaret er **utenfor applikasjonskoden**: et forbrukstak/budsjettgrense
satt direkte i OpenAI sin plattform. I tillegg bidrar eksisterende grenser i koden
(`MAX_CV_LENGTH`/`MAX_JOB_AD_LENGTH`, 30 sekunders timeout, ingen automatiske retries)
til å begrense kostnaden per enkeltkall.