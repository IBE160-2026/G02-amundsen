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

Endelig leverandør og modell velges før implementering, basert på:
- kostnad
- kvalitet på strukturerte svar
- dokumentasjon
- enkel integrasjon med Python
- hvor godt modellen kan følge krav om å ikke finne på kvalifikasjoner
- mulighet for stabil testing

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

Foreslått struktur:

```text
G02-amundsen/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   └── uv.lock
│
├── test-data/
│   ├── demo-cv.txt
│   ├── demo-job-ad.txt
│   └── demo-result.json
│
├── docs/
│   ├── product-brief.md
│   ├── prd.md
│   ├── architecture.md
│   └── process-log.md
│
├── .env.example
├── .gitignore
└── README.md

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

Hemmeligheter og konfigurasjon som ikke skal ligge i GitHub lagres i en lokal `.env`-fil.

Repoet skal inneholde en `.env.example`-fil som viser hvilke miljøvariabler som kreves, uten ekte hemmeligheter.

Eksempel:

LLM_API_KEY=

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